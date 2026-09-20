"""GitHub data for the telemetry panel.

Uses GraphQL for the contribution calendar when a token is available, and falls
back to public push events otherwise. The profile repo itself is excluded from
every number so the bot's own commits never count as your activity.
"""
from __future__ import annotations

import datetime as dt
import os
from dataclasses import dataclass, field

import requests

API = "https://api.github.com"


@dataclass
class Stats:
    weeks: list[int]
    activity_source: str                       # "contributions" | "pushes"
    languages: list[tuple[str, int]]
    repos: int
    stars: int
    last_push: dt.datetime | None
    generated: dt.datetime = field(default_factory=lambda: dt.datetime.now(dt.timezone.utc))


def _session(token: str | None) -> requests.Session:
    s = requests.Session()
    s.headers.update({"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28",
                      "User-Agent": "profile-readme-build"})
    if token:
        s.headers["Authorization"] = f"Bearer {token}"
    return s


def _get(s: requests.Session, url: str, **params):
    r = s.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def _bucket(days_ago: int, n: int) -> int | None:
    i = n - 1 - days_ago // 7
    return i if 0 <= i < n else None


def _contributions(s, user: str, n: int) -> list[int] | None:
    now = dt.datetime.now(dt.timezone.utc)
    q = """query($login:String!,$from:DateTime!,$to:DateTime!){user(login:$login){
      contributionsCollection(from:$from,to:$to){contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}"""
    r = s.post(f"{API}/graphql", timeout=30, json={"query": q, "variables": {
        "login": user, "from": (now - dt.timedelta(days=n * 7 + 7)).isoformat(), "to": now.isoformat()}})
    if r.status_code != 200 or "errors" in r.json():
        return None
    weeks = r.json()["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    out = [0] * n
    today = now.date()
    for w in weeks:
        for day in w["contributionDays"]:
            ago = (today - dt.date.fromisoformat(day["date"])).days
            i = _bucket(ago, n) if ago >= 0 else None
            if i is not None:
                out[i] += day["contributionCount"]
    return out


def _pushes(s, user: str, profile_repo: str, n: int) -> list[int]:
    out = [0] * n
    today = dt.datetime.now(dt.timezone.utc).date()
    for page in (1, 2, 3):
        try:
            events = _get(s, f"{API}/users/{user}/events/public", per_page=100, page=page)
        except requests.HTTPError:
            break
        if not events:
            break
        for e in events:
            if e["type"] != "PushEvent" or e["repo"]["name"].lower().endswith("/" + profile_repo.lower()):
                continue
            ago = (today - dt.datetime.fromisoformat(e["created_at"].replace("Z", "+00:00")).date()).days
            i = _bucket(ago, n)
            if i is not None:
                p = e["payload"]
                out[i] += p.get("distinct_size", p.get("size", len(p.get("commits", [])))) or 1
    return out


def collect(cfg: dict, token: str | None = None) -> Stats:
    token = token or os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    user = cfg["user"]
    n = cfg["telemetry"]["weeks"]
    s = _session(token)

    repos, page = [], 1
    while page <= 3:
        chunk = _get(s, f"{API}/users/{user}/repos", per_page=100, page=page, type="owner", sort="pushed")
        repos += chunk
        if len(chunk) < 100:
            break
        page += 1
    repos = [r for r in repos if not r["fork"] and r["name"].lower() != user.lower()]

    weeks = _contributions(s, user, n) if token else None
    source = "contributions"
    if weeks is None:
        weeks, source = _pushes(s, user, user, n), "pushes"

    exclude = set(cfg["telemetry"]["languages"].get("exclude", []))
    totals: dict[str, int] = {}
    for r in repos[:40]:
        try:
            langs = _get(s, r["languages_url"])
        except requests.HTTPError:
            continue
        for name, b in langs.items():
            if name not in exclude:
                totals[name] = totals.get(name, 0) + b
    languages = sorted(totals.items(), key=lambda kv: -kv[1])

    pushed = [dt.datetime.fromisoformat(r["pushed_at"].replace("Z", "+00:00")) for r in repos if r.get("pushed_at")]
    return Stats(
        weeks=weeks,
        activity_source=source,
        languages=languages,
        repos=len(repos),
        stars=sum(r["stargazers_count"] for r in repos),
        last_push=max(pushed) if pushed else None,
    )
