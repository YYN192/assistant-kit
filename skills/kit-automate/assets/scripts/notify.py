#!/usr/bin/env python3
"""One-way notifications: Discord webhook, Slack incoming webhook, or an ntfy topic.

It only posts. Nothing is ever read back, so no instructions can reach the assistant
this way. The webhook URL / topic lives in the secrets folder (notify.json, mode 600).
No channel configured → prints a note and exits 0, so jobs never fail because of it.

  notify.py setup                 (in your own terminal; paste hidden)
  notify.py test
  notify.py post [--title T] < file
  notify.py alert "text"          (sent even in quiet hours)
  add --dry-run to any command to print instead of sending
"""

import argparse
import datetime as dt
import getpass
import json
import sys
import urllib.request

from common import load_config, now, read_secret_json, write_secret_json

CONF = "notify.json"
LIMITS = {"discord": 1900, "slack": 3500, "ntfy": 3500}


def in_quiet_hours():
    quiet = load_config().get("quiet_hours")  # e.g. "22:00-07:00"
    if not quiet:
        return False
    start, end = (dt.time.fromisoformat(x) for x in quiet.split("-"))
    t = now().time()
    return (start <= t or t < end) if start > end else (start <= t < end)


def chunks(text, size):
    parts, buf = [], ""
    for line in text.splitlines(keepends=True):
        while len(line) > size:
            parts.append(line[:size])
            line = line[size:]
        if len(buf) + len(line) > size:
            parts.append(buf)
            buf = ""
        buf += line
    if buf.strip():
        parts.append(buf)
    return parts or [""]


def send(text, title=None, dry_run=False):
    conf = read_secret_json(CONF)
    if not conf:
        if dry_run:
            print(f"[dry run, no channel configured yet] {title or ''}\n{text}")
        else:
            print("notify: no channel configured (run notify.py setup); nothing sent.")
        return
    kind = conf["kind"]
    for part in chunks(text, LIMITS[kind]):
        if kind == "discord":
            body = json.dumps({"content": (f"**{title}**\n" if title else "") + part}).encode()
            req = urllib.request.Request(conf["url"], data=body, headers={"Content-Type": "application/json", "User-Agent": "assistant-kit"})
        elif kind == "slack":
            body = json.dumps({"text": (f"*{title}*\n" if title else "") + part}).encode()
            req = urllib.request.Request(conf["url"], data=body, headers={"Content-Type": "application/json"})
        else:  # ntfy
            headers = {"Title": title.encode("utf-8").decode("latin-1", "ignore")} if title else {}
            req = urllib.request.Request(f"{conf.get('server', 'https://ntfy.sh')}/{conf['topic']}", data=part.encode(), headers=headers)
        if dry_run:
            print(f"[dry run → {kind}] {title or ''}\n{part}")
            continue
        with urllib.request.urlopen(req, timeout=20) as resp:
            if resp.status >= 300:
                sys.exit(f"notify: {kind} answered {resp.status}")
        title = None  # only on the first chunk
    if not dry_run:
        print(f"notify: sent to {kind}.")


def cmd_setup(_):
    kind = input("Channel: discord, slack or ntfy? ").strip().lower()
    if kind in ("discord", "slack"):
        url = getpass.getpass("Paste the webhook URL (hidden): ").strip()
        if not url.startswith("https://"):
            sys.exit("A webhook URL starts with https://")
        write_secret_json(CONF, {"kind": kind, "url": url})
    elif kind == "ntfy":
        topic = getpass.getpass("ntfy topic name (long and random; hidden): ").strip()
        server = input("Server [https://ntfy.sh]: ").strip() or "https://ntfy.sh"
        write_secret_json(CONF, {"kind": "ntfy", "topic": topic, "server": server})
    else:
        sys.exit("Choose discord, slack or ntfy.")
    print("Saved. Try: notify.py test")


def main():
    ap = argparse.ArgumentParser(description="One-way notifications")
    ap.add_argument("--dry-run", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("setup")
    sub.add_parser("test")
    p = sub.add_parser("post")
    p.add_argument("--title")
    p = sub.add_parser("alert")
    p.add_argument("text")
    args = ap.parse_args()

    if args.cmd == "setup":
        cmd_setup(args)
    elif args.cmd == "test":
        send("✅ test from your assistant", dry_run=args.dry_run)
    elif args.cmd == "post":
        text = sys.stdin.read().strip()
        if not text:
            sys.exit("notify: nothing on stdin")
        if in_quiet_hours():
            print("notify: quiet hours; not sent.")
            return
        send(text, args.title, args.dry_run)
    elif args.cmd == "alert":
        send("❗ " + args.text, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
