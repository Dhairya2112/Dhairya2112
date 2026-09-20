"""Handle one "signal" issue.

Reads the issue from environment variables (never from shell interpolation),
validates it, and appends it to data/signals.json. Writes `status` and `reason`
to $GITHUB_OUTPUT. The visitor's text is only ever treated as data.

Env: ISSUE_NUMBER, ISSUE_TITLE, ISSUE_BODY, ISSUE_USER, ISSUE_USER_TYPE, REPO_OWNER
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
LINKISH = re.compile(
    r"(https?:|www\.|://|\S+@\S+\.\S+|\b\w[\w-]*\.(?:com|net|org|io|in|dev|me|app|co|xyz|ly|gg|ai|to)\b)",
    re.I,
)


def parse_message(title: str, body: str) -> str:
    m = re.search(r"###\s*message\s*\n+(.+?)(?:\n+###|\Z)", body or "", re.I | re.S)
    text = (m.group(1) if m else "").strip()
    if not text or text.lower() == "_no response_":
        text = re.sub(r"^\s*signal\s*:\s*", "", title or "", flags=re.I)
    return " ".join(text.split())


def check(msg: str, user: str, user_type: str, owner: str, entries: list[dict], sc: dict,
          now: dt.datetime) -> str | None:
    """Return a rejection reason, or None when the signal is fine."""
    if user_type.lower() == "bot":
        return "Bots are not accepted."
    if not 1 <= len(msg) <= sc["max_chars"]:
        return f"Signals must be 1 to {sc['max_chars']} characters."
    if not all(0x20 <= ord(c) <= 0x7E for c in msg):
        return "Signals must be plain ASCII: letters, digits and basic punctuation."
    if LINKISH.search(msg):
        return "Links and email addresses are not accepted."
    if any(e["m"].lower() == msg.lower() for e in entries[-5:]):
        return "That line is already on the board."
    if user.lower() != owner.lower():
        cutoff = now - dt.timedelta(hours=sc["cooldown_hours"])
        if any(e["u"].lower() == user.lower() and dt.datetime.fromisoformat(e["t"]) > cutoff for e in entries):
            return f"One signal per {sc['cooldown_hours']} hours. Try again later."
    return None


def emit(status: str, reason: str) -> None:
    line = f"status={status}\nreason={reason}\n"
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as f:
            f.write(line)
    print(line, end="")


def main() -> int:
    cfg = yaml.safe_load((ROOT / "data" / "config.yml").read_text(encoding="utf-8"))
    sc = cfg["signals"]
    path = ROOT / "data" / "signals.json"
    entries = json.loads(path.read_text(encoding="utf-8"))
    env = os.environ
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)

    user = env.get("ISSUE_USER", "")
    msg = parse_message(env.get("ISSUE_TITLE", ""), env.get("ISSUE_BODY", ""))
    reason = check(msg, user, env.get("ISSUE_USER_TYPE", "User"), env.get("REPO_OWNER", cfg["user"]),
                   entries, sc, now)
    if reason:
        emit("rejected", reason)
        return 0

    entries.append({"t": now.isoformat(), "u": user, "m": msg, "n": int(env.get("ISSUE_NUMBER", "0") or 0)})
    entries = entries[-sc["keep"]:]
    path.write_text(json.dumps(entries, indent=1, ensure_ascii=True) + "\n", encoding="utf-8")
    emit("accepted", "Posted to the signal board.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
