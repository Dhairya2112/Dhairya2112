"""hero.svg: ASCII (or particle) portrait + identity + setu runtime values."""
from __future__ import annotations

import math
import random
from collections import defaultdict

from .. import tokens as T
from ..particles import Point
from ..svgkit import Doc, esc, fmt, outline_text

H = 328
PORTRAIT = 280
COL_X = 336
COL_W = T.W - T.PAD - COL_X          # 480

# (min luminance, fill-opacity, radius)
BUCKETS = [(0.0, 0.32, 1.1), (0.25, 0.55, 1.3), (0.5, 0.8, 1.5), (0.75, 1.0, 1.7)]
N_CLASSES = 32


def _scatter_css() -> str:
    rng = random.Random(7)
    rules = []
    for i in range(N_CLASSES):
        ang = rng.random() * math.tau
        dist = 70 + rng.random() * 170
        rules.append(
            f".s{i}{{--x:{fmt(math.cos(ang) * dist)}px;--y:{fmt(math.sin(ang) * dist)}px;--d:{rng.random() * 0.5:.2f}s}}"
        )
    return "".join(rules)


def _ascii_portrait(d: Doc, cfg: dict, rows: list[str]) -> None:
    size = float(cfg["portrait"].get("ascii", {}).get("font_size", 7))
    d.css.append(
        ".r{animation:rv .5s ease-out both;animation-delay:calc(var(--i)*28ms)}"
        "@keyframes rv{from{opacity:0}to{opacity:1}}"
    )
    out = [f'<g fill="{T.PAPER}" fill-opacity="1" font-size="{fmt(size)}">']
    for i, row in enumerate(rows):
        if not row.strip():
            continue
        lead = len(row) - len(row.lstrip(" "))
        txt = row.lstrip(" ")
        d.chars.update(txt)
        y = T.PAD + size * (i + 1) - size * 0.22
        x = T.PAD + lead * size * 0.6
        # textLength pins each row to cols x cell width, so browsers that round glyph
        # advances (Chrome on Linux) cannot stretch the picture.
        out.append(
            f'<text class="r" style="--i:{i}" x="{fmt(x)}" y="{fmt(y)}" '
            f'textLength="{fmt(len(txt) * size * 0.6)}" lengthAdjust="spacing">{esc(txt.replace(" ", chr(160)))}</text>'
        )
        d.chars.add(chr(160))
    out.append("</g>")
    d.raw("".join(out))


def _particle_portrait(d: Doc, points: list[Point]) -> None:
    d.css.append(_scatter_css())
    d.css.append(
        "circle{animation:asm 1s cubic-bezier(.22,.8,.24,1) var(--d,0s) both}"
        "@keyframes asm{from{transform:translate(var(--x),var(--y));opacity:0}"
        "55%{opacity:1}to{transform:translate(0,0);opacity:1}}"
    )
    rng = random.Random(11)
    groups: dict[int, list[str]] = defaultdict(list)
    for p in points:
        b = max(i for i, (lo, _, _) in enumerate(BUCKETS) if p.lum >= lo)
        groups[b].append(
            f'<circle class="s{rng.randrange(N_CLASSES)}" cx="{fmt(p.x)}" cy="{fmt(p.y)}" r="{BUCKETS[b][2]}"/>'
        )
    d.raw(f'<clipPath id="pc"><rect width="{COL_X - 12}" height="{H - 2}" x="1" y="1"/></clipPath>')
    d.raw(f'<g clip-path="url(#pc)"><g transform="translate({T.PAD} {T.PAD})" fill="{T.PAPER}">')
    for b in sorted(groups):
        d.raw(f'<g fill-opacity="{BUCKETS[b][1]}">' + "".join(groups[b]) + "</g>")
    d.raw("</g></g>")


def build(cfg: dict, art: list, style: str = "ascii") -> str:
    h = cfg["hero"]
    pitch = h["pitch"][:3]
    strip = h["strip"][:4]

    d = Doc(
        T.W, H,
        title=f"{h['name']}, {h['role']}",
        desc=(f"{h['name']}: {h['role']}, {h['status']}. " + " ".join(pitch) + " Setu runtime values: "
              + ", ".join(f"{c['label']} {c['value']}" for c in strip) + "."),
    )
    d.frame()

    # ---- portrait: the one memorable thing --------------------------------
    d.css.append(
        ".led{animation:pulse 3s ease-in-out 3}"
        "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.2}}"
    )
    if style == "ascii":
        _ascii_portrait(d, cfg, art)
    else:
        _particle_portrait(d, art)
    d.css.append("@media (prefers-reduced-motion:reduce){circle,.led,.r{animation:none}}")

    # ---- identity -----------------------------------------------------------
    d.raw(f'<circle class="led" cx="{COL_X + 4}" cy="43" r="4" fill="{T.AMBER}"/>')
    d.text(COL_X + 16, 47, h["status"], size=T.T_S, fill=T.MUTED)

    name_svg, _ = outline_text(h["name"], COL_X - 2, 112, T.T_NAME)
    d.raw(name_svg)

    d.text(COL_X, 146, h["role"], size=T.T_L, fill=T.AMBER)
    for i, line in enumerate(pitch):
        d.text(COL_X, 180 + i * 22, line, size=T.T_M, fill=T.PAPER, opacity=0.86)

    # ---- runtime values -------------------------------------------------------
    d.hline(COL_X, T.W - T.PAD, 240)
    d.text(COL_X, 262, h["strip_title"], size=T.T_XS, fill=T.MUTED)
    cell = COL_W / 4
    for i, c in enumerate(strip):
        x = COL_X + i * cell
        d.text(x, 286, c["label"], size=T.T_XS, fill=T.MUTED)
        d.text(x, 310, c["value"], size=T.T_XL, fill=T.AMBER, bold=True)
    return d.render()
