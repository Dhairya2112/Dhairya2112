"""telemetry.svg: weekly activity bars, language share, repository facts."""
from __future__ import annotations

from zoneinfo import ZoneInfo

from .. import tokens as T
from ..fetch import Stats
from ..svgkit import Doc

H = 216
A_X, B_X, C_X = 24, 344, 624
A_W, B_W, C_W = 280, 240, 192
BASE_Y = 156           # bar baseline
BAR_MAX = 96


def build(cfg: dict, st: Stats) -> str:
    try:
        tz = ZoneInfo(cfg["timezone"])
    except Exception:
        import datetime as _dt
        tz = _dt.timezone(_dt.timedelta(hours=5, minutes=30))
    tzl = cfg["tz_label"]
    tcfg = cfg["telemetry"]
    n = len(st.weeks)
    total = sum(st.weeks)

    synced = st.generated.astimezone(tz).strftime("%d %b %Y %H:%M").lstrip("0") + f" {tzl}"
    langs_txt = ", ".join(f"{k} {v / max(sum(b for _, b in st.languages), 1) * 100:.0f}%"
                          for k, v in st.languages[: tcfg["languages"]["top"]])
    d = Doc(
        T.W, H,
        title="GitHub telemetry",
        desc=(f"{total} {st.activity_source} in the last {n} weeks. Languages by bytes: {langs_txt or 'none yet'}. "
              f"{st.repos} public repositories, {st.stars} stars. Synced {synced}."),
    )
    d.frame()

    # ---- column A: activity -------------------------------------------------
    d.text(A_X, 40, f"{st.activity_source}, last {n} weeks", size=T.T_XS, fill=T.MUTED)
    d.text(A_X + A_W, 40, str(total), size=T.T_S, fill=T.AMBER, bold=True, anchor="end")
    peak = max(st.weeks) if st.weeks and max(st.weeks) > 0 else 1
    bw, gap = 16, (A_W - 16 * n) / max(n - 1, 1)
    for i, v in enumerate(st.weeks):
        x = A_X + i * (bw + gap)
        if v == 0:
            d.rect(x, BASE_Y - 2, bw, 2, T.SLATE, 0.7)
            continue
        h = max(3, round(BAR_MAX * v / peak))
        last = i == n - 1
        d.rect(x, BASE_Y - h, bw, h, T.AMBER if last else T.PAPER, None if last else 0.6)
    d.text(A_X, 174, f"{n} weeks ago", size=T.T_XS, fill=T.MUTED)
    d.text(A_X + A_W, 174, "this week", size=T.T_XS, fill=T.MUTED, anchor="end")

    # ---- column B: languages ------------------------------------------------
    d.text(B_X, 40, "languages by bytes", size=T.T_XS, fill=T.MUTED)
    all_bytes = sum(b for _, b in st.languages)
    top = st.languages[: tcfg["languages"]["top"]]
    if not top:
        d.text(B_X, 68, "no public code yet", size=T.T_S, fill=T.MUTED)
    else:
        max_pct = top[0][1] / all_bytes
        for i, (name, b) in enumerate(top):
            y = 68 + i * 22
            pct = b / all_bytes
            d.text(B_X, y, name[:12], size=T.T_S, fill=T.PAPER)
            w = max(2, 110 * pct / max_pct)
            d.rect(B_X + 92, y - 8, w, 7, T.AMBER if i == 0 else T.PAPER, None if i == 0 else 0.6)
            d.text(B_X + B_W, y, f"{pct * 100:.0f}%", size=T.T_S, fill=T.MUTED, anchor="end")

    # ---- column C: repository facts ------------------------------------------
    d.text(C_X, 40, "repositories", size=T.T_XS, fill=T.MUTED)
    last = st.last_push.astimezone(tz).strftime("%d %b").lstrip("0") if st.last_push else "none"
    rows = [("public repos", str(st.repos)), ("stars", str(st.stars)), ("last push", last)]
    sp = tcfg.get("sprint", {})
    if sp.get("enabled"):
        rows.append((sp["label"], f"{sp['solved']}/{sp['total']}"))
    for i, (k, v) in enumerate(rows):
        y = 68 + i * 22
        d.text(C_X, y, k, size=T.T_S, fill=T.PAPER, opacity=0.8)
        d.text(C_X + C_W, y, v, size=T.T_S, fill=T.AMBER, bold=True, anchor="end")
    if sp.get("enabled"):
        y = 68 + 3 * 22 + 8
        d.rect(C_X, y, C_W, 4, T.SLATE, 0.5)
        d.rect(C_X, y, C_W * min(sp["solved"] / max(sp["total"], 1), 1), 4, T.AMBER)

    # ---- footer --------------------------------------------------------------
    d.hline(T.PAD, T.W - T.PAD, 188)
    d.text(T.PAD, 207, f"github api, non-fork repos owned by {cfg['user']}", size=T.T_XS, fill=T.MUTED)
    d.text(T.W - T.PAD, 207, f"synced {synced}", size=T.T_XS, fill=T.MUTED, anchor="end")
    return d.render()
