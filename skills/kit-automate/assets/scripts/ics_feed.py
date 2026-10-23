#!/usr/bin/env python3
"""Read calendar feeds (ICS) such as Canvas, Moodle, Blackboard or a published Outlook
calendar. Standard library only.

Feed URLs usually contain a private token, so they're kept in the secrets folder
(feeds.json, mode 600), typed in hidden by the person in their own terminal, and never
printed.

  ics_feed.py add <name>                     prompts for the URL (hidden)
  ics_feed.py list                           names and hosts only
  ics_feed.py upcoming [--name N] [--days 14] [--past 0] [--json]
  ics_feed.py upcoming --file some.ics       read a local file instead (testing)
"""

import argparse
import datetime as dt
import getpass
import json
import sys
import urllib.parse
import urllib.request

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None

from common import load_config, read_secret_json, write_secret_json

FEEDS = "feeds.json"


def local_tz():
    name = load_config().get("timezone")
    if name and ZoneInfo:
        try:
            return ZoneInfo(name)
        except Exception:
            pass
    return dt.datetime.now().astimezone().tzinfo


def unfold(text):
    lines = []
    for raw in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        if raw[:1] in (" ", "\t") and lines:
            lines[-1] += raw[1:]
        else:
            lines.append(raw)
    return lines


def unescape(value):
    return (value.replace("\\n", "\n").replace("\\N", "\n").replace("\\,", ",")
            .replace("\\;", ";").replace("\\\\", "\\"))


def parse_time(value, params, tz):
    """Return (aware datetime, all_day)."""
    value = value.strip()
    if params.get("VALUE") == "DATE" or (len(value) == 8 and value.isdigit()):
        d = dt.date(int(value[:4]), int(value[4:6]), int(value[6:8]))
        return dt.datetime(d.year, d.month, d.day, tzinfo=tz), True
    fmt = "%Y%m%dT%H%M%S"
    if value.endswith("Z"):
        return dt.datetime.strptime(value[:-1], fmt).replace(tzinfo=dt.timezone.utc).astimezone(tz), False
    naive = dt.datetime.strptime(value[:15], fmt)
    zone = tz
    if "TZID" in params and ZoneInfo:
        try:
            zone = ZoneInfo(params["TZID"])
        except Exception:
            zone = tz
    return naive.replace(tzinfo=zone).astimezone(tz), False


def parse_ics(text, tz, source=""):
    items, cur = [], None
    for line in unfold(text):
        if line in ("BEGIN:VEVENT", "BEGIN:VTODO"):
            cur = {"kind": "event" if line.endswith("VEVENT") else "todo", "source": source}
            continue
        if line in ("END:VEVENT", "END:VTODO"):
            if cur and cur.get("when"):
                items.append(cur)
            cur = None
            continue
        if cur is None or ":" not in line:
            continue
        head, value = line.split(":", 1)
        name, *rawparams = head.split(";")
        params = dict(p.split("=", 1) for p in rawparams if "=" in p)
        name = name.upper()
        if name == "UID":
            cur["uid"] = value.strip()
        elif name == "SUMMARY":
            cur["title"] = unescape(value).strip()
        elif name == "DESCRIPTION":
            cur["description"] = unescape(value).strip()[:300]
        elif name == "URL":
            cur["url"] = value.strip()
        elif name == "LOCATION":
            cur["location"] = unescape(value).strip()
        elif name in ("DTSTART", "DUE") and ("when" not in cur or name == "DUE"):
            when, all_day = parse_time(value, params, tz)
            cur["when"], cur["all_day"] = when, all_day
    return items


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "assistant-kit-ics/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", "replace")


def cmd_add(args):
    url = getpass.getpass(f"Paste the calendar feed URL for '{args.name}' (hidden): ").strip()
    if url.startswith("webcal://"):
        url = "https://" + url[len("webcal://"):]
    if not url.startswith("https://"):
        sys.exit("The URL must start with https:// or webcal://")
    feeds = read_secret_json(FEEDS, {})
    feeds[args.name] = url
    write_secret_json(FEEDS, feeds)
    print(f"Saved feed '{args.name}' ({urllib.parse.urlparse(url).hostname}).")


def cmd_list(_):
    feeds = read_secret_json(FEEDS, {})
    if not feeds:
        print("No feeds. Add one with: ics_feed.py add <name>")
    for name, url in feeds.items():
        print(f"{name}: {urllib.parse.urlparse(url).hostname}")


def upcoming(days=14, past=0, name=None, file=None):
    tz = local_tz()
    now = dt.datetime.now(tz)
    start = (now - dt.timedelta(days=past)).replace(hour=0, minute=0, second=0, microsecond=0)
    end = now + dt.timedelta(days=days)
    items, errors = [], []
    if file:
        with open(file, encoding="utf-8") as f:
            items += parse_ics(f.read(), tz, source=file)
    else:
        for fname, url in read_secret_json(FEEDS, {}).items():
            if name and fname != name:
                continue
            try:
                items += parse_ics(fetch(url), tz, source=fname)
            except Exception as exc:  # report without the URL
                errors.append({"feed": fname, "error": type(exc).__name__})
    items = [i for i in items if start <= i["when"] <= end]
    items.sort(key=lambda i: i["when"])
    for i in items:
        i["date"] = i["when"].strftime("%Y-%m-%d")
        i["time"] = "" if i["all_day"] else i["when"].strftime("%H:%M")
        i["when"] = i["when"].isoformat()
    return items, errors


def cmd_upcoming(args):
    items, errors = upcoming(args.days, args.past, args.name, args.file)
    if args.json:
        print(json.dumps({"items": items, "errors": errors}, ensure_ascii=False))
        return
    for i in items:
        print(f"{i['date']} {i['time'] or 'all-day':>7}  [{i['source']}] {i.get('title', '(no title)')}")
    for e in errors:
        print(f"❗ feed {e['feed']}: {e['error']}")
    if not items and not errors:
        print("Nothing in that window.")


def main():
    ap = argparse.ArgumentParser(description="Calendar feeds (ICS)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("add")
    p.add_argument("name")
    sub.add_parser("list")
    p = sub.add_parser("upcoming")
    p.add_argument("--name")
    p.add_argument("--days", type=int, default=14)
    p.add_argument("--past", type=int, default=0)
    p.add_argument("--file")
    p.add_argument("--json", action="store_true")
    args = ap.parse_args()
    {"add": cmd_add, "list": cmd_list, "upcoming": cmd_upcoming}[args.cmd](args)


if __name__ == "__main__":
    main()
