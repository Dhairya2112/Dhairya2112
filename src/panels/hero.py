"""hero.svg: ASCII (or particle) portrait + identity + setu runtime values."""
from __future__ import annotations

import math
import random
from collections import defaultdict

from .. import tokens as T
from ..particles import Point
from ..svgkit import Doc, esc, fmt, outline_text

H = 348
PORTRAIT = 280
COL_X = 336
COL_W = T.W - T.PAD - COL_X          # 480
PAD_Y = (H - PORTRAIT) // 2          # 34

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
        y = PAD_Y + size * (i + 1) - size * 0.22
        x = T.PAD + lead * size * 0.6
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
    d.raw(f'<g clip-path="url(#pc)"><g transform="translate({T.PAD} {PAD_Y})" fill="{T.PAPER}">')
    for b in sorted(groups):
        d.raw(f'<g fill-opacity="{BUCKETS[b][1]}">' + "".join(groups[b]) + "</g>")
    d.raw("</g></g>")


def build(cfg: dict, art: list, style: str = "ascii") -> str:
    h = cfg["hero"]
    pitch = h.get("pitch", [])[:3]
    stack_grid = h.get("stack_grid", [])

    desc = f"{h['name']}: {h['role']}, {h.get('status', '')}. " + " ".join(pitch)
    d = Doc(
        T.W, H,
        title=f"{h['name']} — {h['role']}",
        desc=desc,
    )
    d.frame()

    # ---- portrait: memorable ASCII / particles ---------------------------
    d.css.append(
        ".led{animation:pulse 3s ease-in-out 3}"
        "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.2}}"
    )
    if style == "ascii":
        _ascii_portrait(d, cfg, art)
    else:
        _particle_portrait(d, art)
    d.css.append("@media (prefers-reduced-motion:reduce){circle,.led,.r{animation:none}}")

    # ---- top status pill & location -----------------------------------------
    status_str = h.get("status", "open to internships & roles").upper()
    location_str = h.get("location", "AHMEDABAD, IN • B.TECH '28").upper()

    # Status pill container
    d.raw(
        f'<rect x="{COL_X}" y="22" width="224" height="22" rx="11" '
        f'fill="#121722" stroke="{T.SLATE}" stroke-opacity=".4" stroke-width="1"/>'
    )
    d.raw(f'<circle class="led" cx="{COL_X + 11}" cy="33" r="3.5" fill="{T.AMBER}"/>')
    d.text(COL_X + 22, 36.5, status_str, size=9.5, fill=T.MUTED, bold=True)
    d.text(COL_X + COL_W, 36.5, location_str, size=9.5, fill=T.MUTED, anchor="end")

    # ---- identity -----------------------------------------------------------
    name_svg, _ = outline_text(h["name"], COL_X - 2, 94, 46)
    d.raw(name_svg)

    d.text(COL_X, 120, h["role"], size=T.T_L, fill=T.AMBER, bold=True)

    # ---- detailed personal introduction --------------------------------------
    for i, line in enumerate(pitch):
        d.text(COL_X, 142 + i * 18, line, size=12, fill=T.PAPER, opacity=0.88)

    # ---- divider & section title ---------------------------------------------
    d.hline(COL_X, T.W - T.PAD, 202, opacity=0.35)
    d.text(COL_X, 218, "CORE TECHNICAL STACK", size=9.5, fill=T.MUTED, bold=True)

    # ---- prominent Bento tech stack matrix ----------------------------------
    card_w = (COL_W - 12) / 2  # 234 px
    card_h = 44                # 44 px

    for i, item in enumerate(stack_grid[:4]):
        col = i % 2
        row = i // 2
        bx = COL_X + col * (card_w + 12)
        by = 228 + row * (card_h + 10)

        # Subtle card container
        d.raw(
            f'<rect x="{fmt(bx)}" y="{fmt(by)}" width="{fmt(card_w)}" height="{fmt(card_h)}" rx="6" '
            f'fill="#121722" stroke="{T.SLATE}" stroke-opacity=".45" stroke-width="1"/>'
        )

        # Category label tag
        d.text(bx + 10, by + 16, item["category"], size=9, fill=T.AMBER, bold=True)

        # Tech stack items
        d.text(bx + 10, by + 34, item["items"], size=11, fill=T.PAPER, bold=True)

    return d.render()
