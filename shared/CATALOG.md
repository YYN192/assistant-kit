# Catalog: what a personal system can contain

Every system is one **personal skill** (the "hub", named like `sam-assistant`) with a
`SYSTEM.md` and one workflow file per module below, plus the automations that run some of
those workflows on a schedule. One skill keeps one source of truth: claude.ai skills can't
read each other's files, so separate skills would each need their own copy of the rules.

Pick modules from the interview, not from this list: three modules that fit beat six that
don't. `help` and `tune-up` are always included.

## Modules

| Module | Workflow file | What it does | Typical people | Needs |
|---|---|---|---|---|
| Morning briefing | `briefing.md` | Today's calendar, what's due, new important mail, 1–3 focus items in real free slots, prep notes for today's meetings, optional weather and news (ask; many people want neither). Short. | everyone who wants "fully automatic" | calendar + one task source; mail optional |
| Inbox triage | `inbox-triage.md` | Sorts new mail from 1–3 inboxes into: needs reply (draft offered), action → task, FYI, ignore. Senders that matter come from the profile. | interns, office workers, anyone with 2+ inboxes | mail connector and/or read-only script per inbox |
| Task capture | `task-capture.md` | Turns pasted text, a lecture slide deck, notes, a photo of a whiteboard, or an email into tasks with due dates, in the person's own words. "add my homework", "add: report draft Friday". | students, everyone | task destination (Todoist, Notion, Asana, Linear, Jira, Google Tasks via script, or calendar all-day items) |
| What's due | inside `task-capture.md` | "what's due", "what's overdue", "this week": one line per item, grouped by day. | everyone | task source |
| Weekly review / planner | `weekly-review.md` | On the chosen day: sync, review the past week, list next week's deadlines, propose work blocks in free time as a table, write them after OK. | students, anyone juggling deadlines | calendar write + task source |
| Work tracker | `work-tracker.md` | Pulls assigned issues from Jira / Linear / Asana / GitHub (and named Slack channels), flags due or blocked ones, drafts a stand-up and a weekly status update, prepares notes for today's meetings. | office workers, engineers, interns | the tracker's connector |
| Calendar blocking with rules | `calendar-blocking.md` | Places focus, study or prep blocks around fixed events, honouring no-go days, quiet hours, travel buffers and a daily cap. Always a table first. | everyone who asks to "plan my week" | calendar write |
| Help | `help.md` (always) | Lists what the assistant can do and the exact phrases to use. | everyone | — |
| Tune-up | `tune-up.md` (always) | Monthly check: what worked, what was ignored, broken connectors, rule changes; edits `SYSTEM.md` after OK. Lets the system keep improving after the kit is gone. | everyone | — |

## Automations

| Automation | Claude Code | Claude app |
|---|---|---|
| Morning briefing on weekdays (and a later one on weekends if wanted) | Desktop scheduled task pointing at the hub skill; or a cloud scheduled task if the person's computer is often off and the briefing needs connectors only | Scheduled task ("Scheduled" page in Claude Desktop / Cowork, or ask in a chat in the new Claude experience) |
| Weekly review reminder | Desktop or cloud scheduled task on the review day | Scheduled task, weekly |
| Weekly status update for a manager (prepared, not posted) | Desktop or cloud scheduled task, weekly | Scheduled task, weekly |
| Data sync with no AI in it (a calendar feed into tasks, a second inbox digest) | Python script + launchd (macOS), cron or systemd timer (Linux), Task Scheduler (Windows), or GitHub Actions for cloud API syncs | Not available; use calendar subscriptions and mail forwarding instead |
| Push notification | `notify.py` to a private Discord/Slack webhook or an ntfy topic (one-way: nothing is ever read back, so no instructions can arrive that way) | The scheduled run itself; optionally a Slack message to self through the Slack connector, or an email draft to self |
| Reminders for one deadline | One-off scheduled task, or a calendar event with a notification | Calendar event with a notification, or a one-off scheduled task |

## Cost guardrails for automations

- One run, one pass: gather first (a script, or 2–4 connector calls), then write.
- Give an unattended run only the connectors its workflow names.
- Keep state (which emails were handled) in a small file (Claude Code) or rely on time
  windows like "newer_than:1d" (Claude app), so runs don't reread old mail.
- Hourly runs are almost never worth it for a personal system; daily or twice daily is
  plenty.
