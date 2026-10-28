#!/usr/bin/env python3
"""Spaced-repetition queue for problems DataDriven syncs into practice/.

DataDriven owns each problem's README.md and solution.sql. This script only
reads those, and keeps its own state in a review.md beside them.

  python3 review.py                          show what's due and rebuild REVIEW.md
  python3 review.py rate <problem> <rating>  log a redo-from-blank and reschedule
                     [-n "what tripped you"]

<problem> is any unique part of the folder name, e.g. "rolling" or "10-lowest".
<rating> is again, hard, good or easy.
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PRACTICE = ROOT / "practice"
QUEUE = ROOT / "REVIEW.md"

# Days until the next redo. A rating moves you along this ladder:
# again -> back to the start, hard -> stay, good -> one step, easy -> two steps.
# Stepping past the end means the problem is mastered and leaves the queue.
LADDER = [1, 3, 7, 14, 30]
MOVES = {"again": None, "hard": 0, "good": 1, "easy": 2}
FIRST_STEP = 1  # a first solve is scored as if it sat on the 3-day rung


def read_front_matter(path):
    text = path.read_text()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return meta, text[m.end():]


def write_front_matter(path, meta, body):
    head = "\n".join(f"{k}: {v}" for k, v in meta.items())
    path.write_text(f"---\n{head}\n---\n{body}")


def load_problems():
    problems = []
    for readme in sorted(PRACTICE.glob("*/*/README.md")):
        folder = readme.parent
        text = readme.read_text()
        title = re.search(r"^# (.+)$", text, re.M)
        level = re.search(r"\[\w+ · (\w+) · on DataDriven\]", text)
        review = folder / "review.md"
        meta = read_front_matter(review)[0] if review.exists() else {}
        problems.append({
            "slug": folder.name,
            "domain": folder.parent.name.upper(),
            "title": title.group(1) if title else folder.name,
            "difficulty": level.group(1) if level else "?",
            "path": folder.relative_to(ROOT).as_posix(),
            "review": review,
            "meta": meta,
        })
    return problems


def link(p, target="review.md"):
    return f"[{p['title']}](./{p['path']}/{target})"


def build_queue(problems, today):
    due, upcoming, unrated, mastered = [], [], [], []
    for p in problems:
        nxt = p["meta"].get("next_review")
        if not p["meta"]:
            unrated.append(p)
        elif nxt == "mastered":
            mastered.append(p)
        elif dt.date.fromisoformat(nxt) <= today:
            due.append(p)
        else:
            upcoming.append(p)
    by_date = lambda p: p["meta"]["next_review"]
    due.sort(key=by_date)
    upcoming.sort(key=by_date)

    def table(rows):
        out = ["| Problem | Level | Last rating | Redo on |", "|---|---|---|---|"]
        for p in rows:
            m = p["meta"]
            out.append(f"| {link(p)} | {p['difficulty']} | {m.get('rating', '')} | {m['next_review']} |")
        return "\n".join(out)

    lines = [
        "# Review queue",
        "",
        f"Built by `review.py` on {today.isoformat()}. Run `python3 review.py` to refresh it; don't edit it by hand.",
        "",
        f"## Due now ({len(due)})",
        "",
        table(due) if due else "Nothing due.",
        "",
        f"## Coming up ({len(upcoming)})",
        "",
        table(upcoming) if upcoming else "Nothing scheduled.",
    ]
    if unrated:
        lines += ["", f"## Needs a rating ({len(unrated)})", "",
                  "Synced from DataDriven with no review notes yet. Rate the first solve to schedule it.", ""]
        lines += [f"- {link(p, '')} ({p['difficulty']}): `python3 review.py rate {p['slug']} <rating>`" for p in unrated]
    if mastered:
        lines += ["", f"## Mastered ({len(mastered)})", ""]
        lines += [f"- {link(p)}" for p in mastered]
    lines += [
        "",
        "## How the schedule works",
        "",
        "Every review is a redo from a blank editor, without looking at `solution.sql`. Then rate it:",
        "",
        "| Rating | Meaning | Next gap |",
        "|---|---|---|",
        "| again | couldn't finish without looking | back to 1 day |",
        "| hard | finished, but had to look something up or got stuck | same gap again |",
        "| good | finished cold with small hesitations | next rung |",
        "| easy | wrote it straight through | skip a rung |",
        "",
        f"Gaps run {', '.join(str(d) for d in LADDER)} days. Clearing the {LADDER[-1]}-day rung marks a problem mastered.",
        "",
    ]
    QUEUE.write_text("\n".join(lines))
    return due, upcoming, unrated


def find(problems, query):
    hits = [p for p in problems if query in p["slug"]]
    if len(hits) != 1:
        names = ", ".join(p["slug"] for p in hits) or "none"
        sys.exit(f"'{query}' matches {len(hits)} problems ({names}). Use more of the folder name.")
    return hits[0]


NEW_NOTES = """
# Review: {title}

[Problem]({path_up}README.md) · [Accepted solution]({path_up}solution.sql)

## How it went

## On the redo

## Review log

| Date | Rating | Next redo | Notes |
|---|---|---|---|
"""


def rate(problems, query, rating, note, today):
    p = find(problems, query)
    review = p["review"]
    if review.exists():
        meta, body = read_front_matter(review)
    else:
        meta, body = {}, NEW_NOTES.format(title=p["title"], path_up="./")
    step = int(meta.get("step", FIRST_STEP))
    step = 0 if MOVES[rating] is None else step + MOVES[rating]
    if step >= len(LADDER):
        nxt = "mastered"
    else:
        nxt = (today + dt.timedelta(days=LADDER[step])).isoformat()
    meta.update(rating=rating, step=str(min(step, len(LADDER))),
                last_reviewed=today.isoformat(), next_review=nxt)
    body = body.rstrip("\n") + f"\n| {today.isoformat()} | {rating} | {nxt} | {note} |\n"
    write_front_matter(review, meta, body)
    print(f"{p['title']}: rated {rating}, next redo {nxt}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--today", type=dt.date.fromisoformat, default=dt.date.today(), help=argparse.SUPPRESS)
    sub = ap.add_subparsers(dest="cmd")
    r = sub.add_parser("rate")
    r.add_argument("problem")
    r.add_argument("rating", choices=MOVES)
    r.add_argument("-n", "--note", default="")
    args = ap.parse_args()

    problems = load_problems()
    if args.cmd == "rate":
        rate(problems, args.problem, args.rating, args.note, args.today)
        problems = load_problems()
    due, upcoming, unrated = build_queue(problems, args.today)

    print(f"\nDue now ({len(due)}):")
    for p in due:
        print(f"  {p['meta']['next_review']}  {p['title']}  [{p['slug']}]")
    if upcoming:
        p = upcoming[0]
        print(f"Next up: {p['title']} on {p['meta']['next_review']}")
    if unrated:
        print(f"Needs a rating: {', '.join(p['slug'] for p in unrated)}")


if __name__ == "__main__":
    main()
