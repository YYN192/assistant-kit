#!/usr/bin/env python3
"""Turn deadlines from calendar feeds into Google Tasks, without duplicates.

Each task created gets a marker line "feed-uid: <uid>" in its notes, so later runs skip
it. Never deletes or edits existing tasks. Prints one line per change (+ new, = known).

  feed_to_tasks.py sync [--days 21] [--list NAME] [--dry-run]

Config (assistant.json):  "feed_to_tasks": {"list": "Uni", "match": ["due", "assignment", "quiz"]}
"match" keeps only feed items whose title contains one of the words (case-insensitive);
leave it out to take everything.
"""

import argparse
import json

import gtasks
import ics_feed
from common import load_config


def wanted(item, words):
    title = item.get("title", "").lower()
    return not words or any(w.lower() in title for w in words)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("sync")
    p.add_argument("--days", type=int, default=21)
    p.add_argument("--list")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--file", help="read a local .ics file instead of the saved feeds (testing)")
    args = ap.parse_args()

    cfg = load_config().get("feed_to_tasks", {})
    list_name = args.list or cfg.get("list") or gtasks.default_list()
    items, errors = ics_feed.upcoming(days=args.days, file=args.file)
    items = [i for i in items if wanted(i, cfg.get("match", [])) and i.get("uid")]

    known = set()
    if not args.dry_run:
        service = gtasks.svc()
        lid = gtasks.find_list(service, list_name)
        for t in gtasks.all_tasks(service, lid, show_completed=True):
            for line in (t.get("notes") or "").splitlines():
                if line.startswith("feed-uid: "):
                    known.add(line[len("feed-uid: "):].strip())

    for i in items:
        if i["uid"] in known:
            print(f"= {i['date']} {i['title']}")
            continue
        body = {"title": f"[{i['source']}] {i['title']}", "due": f"{i['date']}T00:00:00.000Z",
                "notes": f"{i.get('url', '')}\nfeed-uid: {i['uid']}".strip()}
        if args.dry_run:
            print("+ (dry run)", json.dumps({k: body[k] for k in ("title", "due")}, ensure_ascii=False))
        else:
            service.tasks().insert(tasklist=lid, body=body).execute()
            print(f"+ {i['date']} {body['title']}")
    for e in errors:
        print(f"❗ feed {e['feed']}: {e['error']}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
