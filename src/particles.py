"""Photo -> particle point cloud.

Brightness-weighted stippling on a 280x280 canvas with a minimum spacing
(cheap blue noise), so dots read as light on a dark panel. Deterministic
for a given photo and settings.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

SIZE = 280          # canvas edge in SVG units
GRID = 200          # working resolution of the photo


@dataclass
class Point:
    x: float
    y: float
    lum: float      # 0..1


def placeholder() -> Image.Image:
    """Neutral bust silhouette, used until source/portrait.jpg exists."""
    img = Image.new("L", (GRID, GRID), 0)
    d = ImageDraw.Draw(img)
    d.ellipse((62, 22, 138, 116), fill=230)                     # head
    d.rounded_rectangle((88, 104, 112, 134), radius=8, fill=170)  # neck
    d.pieslice((14, 122, 186, 300), 180, 360, fill=200)          # shoulders
    return img.filter(ImageFilter.GaussianBlur(6)).convert("RGB")


def load(path: Path, cfg: dict) -> Image.Image:
    """Square crop of the photo. RGBA is kept, so a cut-out PNG carries its own mask."""
    if not path.exists():
        return placeholder()
    img = ImageOps.exif_transpose(Image.open(path))
    img = img.convert("RGBA") if "A" in img.getbands() else img.convert("RGB")
    w, h = img.size
    side = int(min(w, h) / max(float(cfg.get("zoom", 1.0)), 1.0))
    left = int((w - side) * min(max(float(cfg.get("focus_x", 0.5)), 0), 1))
    top = int((h - side) * min(max(float(cfg.get("focus_y", 0.4)), 0), 1))
    return img.crop((left, top, left + side, top + side)).resize((GRID, GRID), Image.LANCZOS)


def _smoothstep(x: np.ndarray, lo: float, hi: float) -> np.ndarray:
    t = np.clip((x - lo) / (hi - lo), 0, 1)
    return t * t * (3 - 2 * t)


def _backdrop(arr: np.ndarray) -> tuple[np.ndarray, float]:
    """Median colour of the photo's border ring, and how much the ring varies."""
    ring = np.concatenate([arr[:8].reshape(-1, 3), arr[-8:].reshape(-1, 3),
                           arr[:, :8].reshape(-1, 3), arr[:, -8:].reshape(-1, 3)])
    return np.median(ring, axis=0), float(ring.std(axis=0).mean())


def density(img: Image.Image, cfg: dict) -> np.ndarray:
    """0..1 map of where marks (dots or characters) should be."""
    alpha = None
    if img.mode == "RGBA":
        alpha = np.asarray(img.getchannel("A"), dtype=np.float32) / 255.0
    rgb = img.convert("RGB")
    lum0 = np.asarray(rgb.convert("L"), dtype=np.float32) / 255.0

    # Stretch contrast over the subject only, so a dark backdrop or shirt does not skew it.
    sel = (alpha > 0.5) if alpha is not None else np.ones_like(lum0, dtype=bool)
    lead = sel.copy()                        # the part of the crop that leads (above the fade)
    ff = cfg.get("fade_from")
    if ff is not None:
        lead[int(float(ff) * GRID):, :] = False
    ref = lead if lead.sum() > 200 else sel
    lo, hi = np.percentile(lum0[ref], (2, 98)) if ref.any() else (0.0, 1.0)
    g = np.clip((lum0 - lo) / max(hi - lo, 1e-3), 0, 1)
    eq = float(cfg.get("equalize", 0.5))     # spread the tones a face actually uses
    if eq and ref.any():
        m = Image.fromarray((ref * 255).astype(np.uint8))
        flat = np.asarray(ImageOps.equalize(Image.fromarray((g * 255).astype(np.uint8)), mask=m),
                          dtype=np.float32) / 255.0
        g = (1 - eq) * g + eq * flat
    if cfg.get("invert"):
        g = 1 - g

    # Local contrast: push features (eyes, jaw, glasses) away from their surroundings.
    detail = float(cfg.get("detail", 0.6))
    if detail:
        fill = np.where(sel, g, g[sel].mean() if sel.any() else 0.5).astype(np.float32)
        soft = np.asarray(Image.fromarray((fill * 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(GRID / 16)), dtype=np.float32) / 255.0
        g = np.clip(g + detail * (g - soft), 0, 1)
    lum = g ** float(cfg.get("gamma", 1.25))

    arr = np.asarray(rgb, dtype=np.float32)
    bg, spread = _backdrop(arr)
    mode = cfg.get("mode", "auto")
    if alpha is not None:
        mode = "cutout"
    elif mode == "auto":                     # plain wall -> isolate the subject; busy scene -> brightness
        mode = "subject" if spread < 28 else "luminance"

    floor = float(cfg.get("floor", 0.3))
    if mode == "cutout":
        a = alpha * (floor + (1 - floor) * lum)
    elif mode == "luminance":
        a = lum
    else:
        diff = np.sqrt(((arr - bg) ** 2).sum(-1)) / 441.7
        mask = _smoothstep(diff, 0.05, 0.20)
        mask_img = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))
        a = (np.asarray(mask_img, dtype=np.float32) / 255.0) * (floor + (1 - floor) * lum)

    if cfg.get("vignette", True):
        yy, xx = np.mgrid[0:GRID, 0:GRID]
        r = np.hypot(xx - GRID / 2, yy - GRID / 2) / (GRID / 2)
        a = a * np.clip((1.02 - r) / 0.42, 0, 1)

    # Let the lower part of the crop (chest, hands) fade out so the face leads.
    fade_from = cfg.get("fade_from")
    if fade_from is not None:
        y = np.linspace(0, 1, GRID, dtype=np.float32)[:, None]
        a = a * np.clip(1 - (y - float(fade_from)) / max(1 - float(fade_from), 1e-3) * 0.85, 0.15, 1)
    return a


def sample(cfg: dict, root: Path) -> list[Point]:
    a = density(load(root / cfg["file"], cfg), cfg)

    target = int(cfg.get("points", 1200))
    rng = random.Random(412)
    scale = SIZE / GRID
    min_d = 3.4                      # SVG units between dot centres
    cell = min_d
    grid: dict[tuple[int, int], list[tuple[float, float]]] = {}
    out: list[Point] = []

    tries = 0
    while len(out) < target and tries < target * 60:
        tries += 1
        gx, gy = rng.random() * (GRID - 1), rng.random() * (GRID - 1)
        lum = float(a[int(gy), int(gx)])
        if rng.random() > lum:
            continue
        x, y = gx * scale, gy * scale
        cx, cy = int(x // cell), int(y // cell)
        near = False
        for i in (cx - 1, cx, cx + 1):
            for j in (cy - 1, cy, cy + 1):
                for px, py in grid.get((i, j), ()):
                    if math.hypot(px - x, py - y) < min_d:
                        near = True
                        break
                if near:
                    break
            if near:
                break
        if near:
            continue
        grid.setdefault((cx, cy), []).append((x, y))
        out.append(Point(round(x, 1), round(y, 1), lum))
    return out


def ascii_rows(cfg: dict, root: Path) -> list[str]:
    """Photo -> rows of ASCII characters filling the 280x280 portrait box.

    Cell shape follows the monospace font: width 0.6em, height 1em, so the picture
    keeps its proportions.
    """
    acfg = cfg.get("ascii", {})
    size = float(acfg.get("font_size", 7))
    cols, rows = int(SIZE // (size * 0.6)), int(SIZE // size)
    a = density(load(root / cfg["file"], cfg), cfg)
    img = Image.fromarray((a * 255).astype(np.uint8)).resize((cols, rows), Image.BOX)
    m = np.asarray(img, dtype=np.float32) / 255.0
    lit = m[m > 0.03]
    hi = float(np.percentile(lit, 97)) if lit.size else 1.0
    m = np.clip(m / max(hi, 1e-3), 0, 1) ** float(acfg.get("gamma", 0.85))
    ramp = acfg.get("ramp", " .:-=+*#%@")
    idx = np.minimum((m * len(ramp)).astype(int), len(ramp) - 1)
    return ["".join(ramp[i] for i in row).rstrip() for row in idx]
