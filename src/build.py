"""Build every panel into dist/.  Usage: python -m src.build [--offline]

--offline skips the GitHub API and uses sample numbers (for local layout work).
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import requests
import yaml

from . import particles
from .fetch import Stats, collect
from .panels import hero, telemetry

ROOT = Path(__file__).resolve().parent.parent
BUDGET = {"hero.svg": 150_000, "telemetry.svg": 60_000}


def offline_stats() -> Stats:
    now = dt.datetime.now(dt.timezone.utc)
    return Stats(
        weeks=[3, 9, 0, 14, 22, 11, 5, 18, 27, 9, 16, 21],
        activity_source="contributions",
        languages=[("Python", 640_000), ("JavaScript", 410_000), ("Java", 90_000), ("SQL", 30_000), ("CSS", 22_000)],
        repos=14, stars=3, last_push=now - dt.timedelta(days=2),
    )


def main() -> int:
    cfg = yaml.safe_load((ROOT / "data" / "config.yml").read_text(encoding="utf-8"))
    try:
        st = offline_stats() if "--offline" in sys.argv else collect(cfg)
    except requests.HTTPError as e:
        print(f"GitHub API error: {e}\nRate limited or bad token. Locally, set GH_TOKEN or run with --offline.", file=sys.stderr)
        return 1
    style = cfg["portrait"].get("style", "ascii")
    art = particles.ascii_rows(cfg["portrait"], ROOT) if style == "ascii" else particles.sample(cfg["portrait"], ROOT)

    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    files = {
        "hero.svg": hero.build(cfg, art, style),
        "telemetry.svg": telemetry.build(cfg, st),
    }
    for name, svg in files.items():
        (out / name).write_text(svg, encoding="utf-8")
        size = len(svg.encode())
        flag = "" if size <= BUDGET[name] else "  <-- over budget"
        print(f"{name:15s}{size / 1024:7.1f} KB{flag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
