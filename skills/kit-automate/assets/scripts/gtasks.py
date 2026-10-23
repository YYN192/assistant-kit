#!/usr/bin/env python3
"""Google Tasks for the assistant (scope tasks). There is no Google Tasks connector, so
Claude Code uses this script. It never deletes: "done" ticks a task off.

  gtasks.py auth                                        (in your own terminal)
  gtasks.py check
  gtasks.py lists
  gtasks.py list [--list NAME] [--completed] [--json]   (no --list = every list)
  gtasks.py add "title" [--list NAME] [--due YYYY-MM-DD] [--notes "..."] [--dry-run]
  gtasks.py done <id-or-text> [--list NAME]
"""

import argparse
import datetime as dt
import json
import sys

import google_auth
from common import load_config

SCOPES = ["https://www.googleapis.com/auth/tasks"]
TOKEN = "google-tasks-token.json"


def svc():
    return google_auth.service("tasks", "v1", google_auth.load(TOKEN, SCOPES))


def default_list():
    return load_config().get("tasks", {}).get("default_list", "My Tasks")


def find_list(service, name):
    lists = service.tasklists().list(maxResults=100).execute().get("items", [])
    for tl in lists:
        if tl["title"].lower() == name.lower():
            return tl["id"]
    sys.exit(f"No task list called '{name}'. Lists: " + ", ".join(t["title"] for t in lists))


def all_tasks(service, list_id, show_completed=False):
    out, token = [], None
    while True:
        res = service.tasks().list(tasklist=list_id, showCompleted=show_completed, showHidden=show_completed,
                                   maxResults=100, pageToken=token).execute()
        out += res.get("items", [])
        token = res.get("nextPageToken")
        if not token:
            return out


def cmd_auth(_):
    google_auth.sign_in(TOKEN, SCOPES)
    print("Signed in to Google Tasks.")


def cmd_check(_):
    lists = svc().tasklists().list(maxResults=100).execute().get("items", [])
    print(json.dumps({"lists": [t["title"] for t in lists], "scope": "tasks"}, ensure_ascii=False))


def cmd_lists(_):
    for tl in svc().tasklists().list(maxResults=100).execute().get("items", []):
        print(tl["title"])


def collect(service, list_name=None, completed=False):
    """Tasks from one list, or from every list when list_name is None."""
    lists = service.tasklists().list(maxResults=100).execute().get("items", [])
    if list_name:
        lists = [{"id": find_list(service, list_name), "title": list_name}]
    out = []
    for tl in lists:
        for t in all_tasks(service, tl["id"], completed):
            out.append({"list": tl["title"], "id": t["id"], "title": t["title"],
                        "due": (t.get("due") or "")[:10], "status": t.get("status"), "notes": t.get("notes")})
    return sorted(out, key=lambda t: t["due"] or "9999")


def cmd_list(args):
    tasks = collect(svc(), args.list, args.completed)
    if args.json:
        print(json.dumps(tasks, ensure_ascii=False))
        return
    today = dt.date.today().isoformat()
    for t in tasks:
        flag = "!" if t["due"] and t["due"] < today and t["status"] != "completed" else " "
        tick = "✓" if t["status"] == "completed" else " "
        print(f"{flag}{tick} {t['due'] or '----------'}  [{t['list']}] {t['title']}  [{t['id'][:8]}]")


def cmd_add(args):
    body = {"title": args.title}
    if args.due:
        dt.date.fromisoformat(args.due)
        body["due"] = f"{args.due}T00:00:00.000Z"
    if args.notes:
        body["notes"] = args.notes
    if args.dry_run:
        print("would add:", json.dumps(body, ensure_ascii=False))
        return
    service = svc()
    lid = find_list(service, args.list or default_list())
    for t in all_tasks(service, lid):
        if t["title"].strip().lower() == args.title.strip().lower() and (t.get("due") or "")[:10] == (args.due or ""):
            print(f"= already there: {t['title']}")
            return
    t = service.tasks().insert(tasklist=lid, body=body).execute()
    print(f"+ {t['title']}  {(t.get('due') or '')[:10]}  [{t['id'][:8]}]")


def cmd_done(args):
    service = svc()
    lid = find_list(service, args.list or default_list())
    key = args.target.lower()
    matches = [t for t in all_tasks(service, lid) if t["id"].startswith(args.target) or key in t["title"].lower()]
    if len(matches) != 1:
        sys.exit(f"{len(matches)} tasks match '{args.target}'; be more specific." + "".join(f"\n  {t['title']} [{t['id'][:8]}]" for t in matches))
    t = matches[0]
    service.tasks().patch(tasklist=lid, task=t["id"], body={"status": "completed"}).execute()
    print(f"✓ {t['title']}")


def main():
    ap = argparse.ArgumentParser(description="Google Tasks (never deletes)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("auth")
    sub.add_parser("check")
    sub.add_parser("lists")
    p = sub.add_parser("list")
    p.add_argument("--list")
    p.add_argument("--completed", action="store_true", help="include completed tasks")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("add")
    p.add_argument("title")
    p.add_argument("--list")
    p.add_argument("--due")
    p.add_argument("--notes")
    p.add_argument("--dry-run", action="store_true")
    p = sub.add_parser("done")
    p.add_argument("target")
    p.add_argument("--list")
    args = ap.parse_args()
    {"auth": cmd_auth, "check": cmd_check, "lists": cmd_lists, "list": cmd_list,
     "add": cmd_add, "done": cmd_done}[args.cmd](args)


if __name__ == "__main__":
    main()
