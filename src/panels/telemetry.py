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

    # ---- column dividers ----------------------------------------------------
    d.raw(f'<path d="M312 32V176" stroke="{T.SLATE}" stroke-opacity=".35" stroke-width="1" shape-rendering="crispEdges"/>')
    d.raw(f'<path d="M592 32V176" stroke="{T.SLATE}" stroke-opacity=".35" stroke-width="1" shape-rendering="crispEdges"/>')

    # ---- column A: activity graph -------------------------------------------
    d.text(A_X, 40, f"CADENCE: {st.activity_source.upper()} (12 WEEKS)", size=T.T_XS, fill=T.MUTED)
    d.text(296, 40, f"{total} total", size=T.T_S, fill=T.AMBER, bold=True, anchor="end")
    peak = max(st.weeks) if st.weeks and max(st.weeks) > 0 else 1
    avg = total / max(n, 1)
    avg_h = max(2, round(BAR_MAX * avg / peak))
    bw, gap = 15, (272 - 15 * n) / max(n - 1, 1)

    # Average baseline
    d.raw(f'<line x1="{A_X}" y1="{BASE_Y - avg_h}" x2="296" y2="{BASE_Y - avg_h}" stroke="{T.SLATE}" stroke-opacity=".45" stroke-dasharray="2 3" stroke-width="1"/>')

    for i, v in enumerate(st.weeks):
        x = A_X + i * (bw + gap)
        if v == 0:
            d.rect(x, BASE_Y - 2, bw, 2, T.SLATE, 0.5)
            continue
        h = max(3, round(BAR_MAX * v / peak))
        last = i == n - 1
        d.rect(x, BASE_Y - h, bw, h, T.AMBER if last else T.PAPER, None if last else 0.6)
    d.text(A_X, 172, f"12w ago", size=T.T_XS, fill=T.MUTED)
    d.text(160, 172, f"avg {avg:.1f}/wk", size=T.T_XS, fill=T.MUTED, anchor="middle")
    d.text(296, 172, "this week", size=T.T_XS, fill=T.MUTED, anchor="end")

    # ---- column B: languages & distribution ---------------------------------
    B_X, B_W = 328, 248
    d.text(B_X, 40, "LANGUAGE DISTRIBUTION", size=T.T_XS, fill=T.MUTED)
    all_bytes = sum(b for _, b in st.languages)
    top = st.languages[: tcfg["languages"]["top"]]
    if not top or all_bytes == 0:
        d.text(B_X, 68, "no public code yet", size=T.T_S, fill=T.MUTED)
    else:
        # Stacked proportional bar
        seg_x = B_X
        for i, (_, b) in enumerate(top):
            seg_w = max(2, (b / all_bytes) * B_W)
            d.rect(seg_x, 48, seg_w, 4, T.AMBER if i == 0 else T.PAPER, None if i == 0 else max(0.2, 0.8 - i * 0.15))
            seg_x += seg_w

        max_pct = top[0][1] / all_bytes
        for i, (name, b) in enumerate(top):
            y = 74 + i * 20
            pct = b / all_bytes
            d.text(B_X, y, name[:12], size=T.T_S, fill=T.PAPER)
            w = max(2, 110 * pct / max_pct)
            d.rect(B_X + 90, y - 8, w, 6, T.AMBER if i == 0 else T.PAPER, None if i == 0 else 0.5)
            d.text(B_X + B_W, y, f"{pct * 100:.0f}%", size=T.T_S, fill=T.MUTED, anchor="end")

    # ---- column C: repository facts & systems --------------------------------
    C_X, C_W = 608, 208
    d.text(C_X, 40, "SYSTEMS & TELEMETRY", size=T.T_XS, fill=T.MUTED)
    last = st.last_push.astimezone(tz).strftime("%d %b").lstrip("0") if st.last_push else "none"
    rows = [
        ("public repos", str(st.repos)),
        ("github stars", str(st.stars)),
        ("latest push", last),
        ("live systems", "2 active"),
    ]
    for i, (k, v) in enumerate(rows):
        y = 74 + i * 22
        d.text(C_X, y, k, size=T.T_S, fill=T.PAPER, opacity=0.8)
        d.text(C_X + C_W, y, v, size=T.T_S, fill=T.AMBER, bold=True, anchor="end")

    # ---- footer --------------------------------------------------------------
    d.hline(T.PAD, T.W - T.PAD, 188)
    d.text(T.PAD, 207, f"telemetry • verified github metrics for {cfg['user']}", size=T.T_XS, fill=T.MUTED)
    d.text(T.W - T.PAD, 207, f"synced {synced}", size=T.T_XS, fill=T.MUTED, anchor="end")
    return d.render()
