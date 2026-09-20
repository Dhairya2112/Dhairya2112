"""Small SVG toolkit.

Doc            collects elements and text, then renders one self-contained SVG
               (embedded, subsetted JetBrains Mono as base64 woff2).
outline_text   turns display text into vector paths (Space Grotesk Bold), so the
               name never depends on a font loading.
"""
from __future__ import annotations

import base64
import html
import io
from functools import lru_cache
from pathlib import Path

import uharfbuzz as hb
from fontTools import subset
from fontTools.pens.svgPathPen import SVGPathPen

from . import tokens as T

FONTS = Path(__file__).parent / "fonts"
MONO_FILES = {400: FONTS / "JetBrainsMono-Regular.ttf", 700: FONTS / "JetBrainsMono-Bold.ttf"}
DISPLAY_FILE = FONTS / "SpaceGrotesk.ttf"

ASCII = "".join(chr(c) for c in range(0x20, 0x7F))


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def fmt(n: float) -> str:
    """Compact number for SVG attributes."""
    s = f"{n:.1f}"
    return s[:-2] if s.endswith(".0") else s


@lru_cache(maxsize=16)
def _subset_b64(weight: int, chars: str) -> str:
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = []      # no ligatures, no kerning tables: smaller
    opts.hinting = False
    opts.name_IDs = []
    opts.notdef_outline = False
    opts.drop_tables += ["DSIG", "GDEF", "GPOS", "GSUB", "MATH", "STAT"]
    font = subset.load_font(str(MONO_FILES[weight]), opts)
    sub = subset.Subsetter(opts)
    sub.populate(text=chars)
    sub.subset(font)
    buf = io.BytesIO()
    subset.save_font(font, buf, opts)
    return base64.b64encode(buf.getvalue()).decode("ascii")


class Doc:
    def __init__(self, width: int, height: int, title: str, desc: str):
        self.w, self.h = width, height
        self.title, self.desc = title, desc
        self.body: list[str] = []
        self.chars: set[str] = set(" ")
        self.css: list[str] = []
        self.bold_used = False

    # -- primitives ---------------------------------------------------
    def raw(self, s: str) -> None:
        self.body.append(s)

    def frame(self) -> None:
        self.raw(
            f'<rect x=".5" y=".5" width="{self.w - 1}" height="{self.h - 1}" rx="{T.RADIUS}" '
            f'fill="{T.INK}" stroke="{T.SLATE}" stroke-opacity=".45"/>'
        )

    def hline(self, x1: float, x2: float, y: float, opacity: float = 0.4) -> None:
        self.raw(
            f'<path d="M{fmt(x1)} {fmt(y)}H{fmt(x2)}" stroke="{T.SLATE}" '
            f'stroke-opacity="{opacity}" stroke-width="1" shape-rendering="crispEdges"/>'
        )

    def rect(self, x, y, w, h, fill, opacity: float | None = None) -> None:
        op = f' fill-opacity="{opacity}"' if opacity is not None else ""
        self.raw(f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" fill="{fill}"{op}/>')

    def text(self, x, y, s: str, size=T.T_S, fill=T.PAPER, bold=False,
             anchor="start", opacity: float | None = None) -> None:
        self.chars.update(s)
        self.bold_used = self.bold_used or bold
        attrs = f'x="{fmt(x)}" y="{fmt(y)}" font-size="{size}" fill="{fill}"'
        if bold:
            attrs += ' class="b"'
        if anchor != "start":
            attrs += f' text-anchor="{anchor}"'
        if opacity is not None:
            attrs += f' fill-opacity="{opacity}"'
        self.raw(f"<text {attrs}>{esc(s)}</text>")

    # -- output -------------------------------------------------------
    def render(self, ascii_all: bool = False) -> str:
        chars = set(self.chars)
        if ascii_all:
            chars.update(ASCII)
        chars_s = "".join(sorted(chars))
        faces = [f"@font-face{{font-family:'JBM';font-weight:400;src:url(data:font/woff2;base64,{_subset_b64(400, chars_s)}) format('woff2')}}"]
        if self.bold_used:
            faces.append(f"@font-face{{font-family:'JBM';font-weight:700;src:url(data:font/woff2;base64,{_subset_b64(700, chars_s)}) format('woff2')}}")
        base = (
            f"text{{font-family:{T.MONO};font-variant-ligatures:none;font-kerning:none}}"
            ".b{font-weight:700}"
        )
        style = "".join(faces) + base + "".join(self.css)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
            f'width="{self.w}" height="{self.h}" role="img" aria-labelledby="t d">'
            f'<title id="t">{esc(self.title)}</title><desc id="d">{esc(self.desc)}</desc>'
            f"<style>{style}</style>" + "".join(self.body) + "</svg>"
        )


# -- outlined display text ------------------------------------------------
@lru_cache(maxsize=1)
def _display_font() -> tuple[hb.Font, int]:
    blob = hb.Blob.from_file_path(str(DISPLAY_FILE))
    face = hb.Face(blob)
    font = hb.Font(face)
    font.set_variations({"wght": 700})
    return font, face.upem


def outline_text(s: str, x: float, baseline: float, size: float, tracking: float = -0.015) -> tuple[str, float]:
    """Return (svg <g> markup, advance width) for `s` set in Space Grotesk Bold."""
    font, upem = _display_font()
    buf = hb.Buffer()
    buf.add_str(s)
    buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": True})
    scale = size / upem
    pen_x = 0.0
    paths = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        pen = SVGPathPen(None, ntos=lambda v: f"{v:g}")
        font.draw_glyph_with_pen(info.codepoint, pen)
        d = pen.getCommands()
        if d:
            paths.append(f'<path transform="translate({fmt(pen_x + pos.x_offset)} 0)" d="{d}"/>')
        pen_x += pos.x_advance + tracking * upem
    g = (
        f'<g transform="translate({fmt(x)} {fmt(baseline)}) scale({scale:.5f} {-scale:.5f})" '
        f'fill="{T.PAPER}">' + "".join(paths) + "</g>"
    )
    return g, pen_x * scale
