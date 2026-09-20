"""signals.svg: the latest visitor transmissions, written by the signal workflow."""
from __future__ import annotations

import datetime as dt
from zoneinfo import ZoneInfo

from .. import tokens as T
from ..svgkit import Doc

H = 216


def build(cfg: dict, entries: list[dict]) -> str:
    try:
        tz = ZoneInfo(cfg["timezone"])
    except Exception:
        tz = dt.timezone(dt.timedelta(hours=5, minutes=30))
    sc = cfg["signals"]
    shown = sorted(entries, key=lambda e: e["t"], reverse=True)[: sc["show"]]

    desc = "No signals yet." if not shown else "Latest signals: " + "; ".join(f"{e['u']}: {e['m']}" for e in shown)
    d = Doc(T.W, H, title="Signal board", desc=desc)
    d.frame()

    d.text(T.PAD, 40, "latest signals", size=T.T_XS, fill=T.MUTED)
    d.text(T.W - T.PAD, 40, f"{len(entries)} received", size=T.T_S, fill=T.AMBER, bold=True, anchor="end")

    if not shown:
        d.text(T.PAD, 76, "No signals yet. Post the first one.", size=T.T_S, fill=T.PAPER, opacity=0.86)
    for i, e in enumerate(shown):
        y = 70 + i * 25
        when = dt.datetime.fromisoformat(e["t"]).astimezone(tz).strftime("%d %b %H:%M").lstrip("0")
        user = e["u"] if len(e["u"]) <= 18 else e["u"][:17] + "\u2026"
        d.text(T.PAD, y, when, size=T.T_S, fill=T.MUTED)
        d.text(140, y, user, size=T.T_S, fill=T.CYAN)
        d.text(290, y, e["m"][: sc["max_chars"]], size=T.T_S, fill=T.PAPER, opacity=0.9)

    d.hline(T.PAD, T.W - T.PAD, 188)
    d.text(T.PAD, 207, f"one line, {sc['max_chars']} characters, plain ascii, no links", size=T.T_XS, fill=T.MUTED)
    d.text(T.W - T.PAD, 207, "redrawn after each post", size=T.T_XS, fill=T.MUTED, anchor="end")
    return d.render(ascii_all=True)
