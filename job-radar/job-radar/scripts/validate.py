"""Checks data/jobs.json for mistakes. Run: python3 scripts/validate.py"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATUSES = {"New", "Interested", "Applied", "Interview", "Rejected"}
LIVE = {"verified", "unverified", "closed"}
REQUIRED = ["id", "title", "company", "score", "url", "status", "live", "added"]
LISTS = ["why", "gaps", "flags", "bullets"]


def main() -> int:
    data = json.loads((ROOT / "data" / "jobs.json").read_text(encoding="utf-8"))
    jobs = data.get("jobs", [])
    problems = []
    seen_ids, seen_urls = set(), {}
    for j in jobs:
        jid = j.get("id", "?")
        for f in REQUIRED:
            if j.get(f) in (None, ""):
                problems.append(f"{jid}: missing '{f}'")
        if j.get("status") not in STATUSES:
            problems.append(f"{jid}: status '{j.get('status')}' is not one of {sorted(STATUSES)}")
        if j.get("live") not in LIVE:
            problems.append(f"{jid}: live '{j.get('live')}' is not one of {sorted(LIVE)}")
        s = j.get("score")
        if not isinstance(s, (int, float)) or not 0 <= s <= 100:
            problems.append(f"{jid}: score '{s}' must be a number 0-100")
        for f in LISTS:
            if f in j and not isinstance(j[f], list):
                problems.append(f"{jid}: '{f}' must be a list")
        if jid in seen_ids:
            problems.append(f"{jid}: duplicate id")
        seen_ids.add(jid)
        url = (j.get("url") or "").rstrip("/")
        if url and url in seen_urls:
            problems.append(f"{jid}: same url as {seen_urls[url]}")
        seen_urls[url] = jid
        parts = j.get("scoreParts")
        if isinstance(parts, dict):
            raw = sum(v for k, v in parts.items() if k != "cap" and isinstance(v, (int, float)))
            cap = parts.get("cap")
            expected = min(round(raw), cap if isinstance(cap, (int, float)) else 100, 100)
            if abs(expected - s) > 1:
                problems.append(f"{jid}: score {s} does not match scoreParts (expected about {expected})")
    if problems:
        print(f"{len(problems)} problem(s):")
        for p in problems:
            print(" -", p)
        return 1
    print(f"OK: {len(jobs)} jobs, no problems found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
