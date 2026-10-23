# Surfaces: where the kit is running and what each one can do

The kit runs in two kinds of place. What you can build depends on which one you're in, so
work it out once at the start, write it into the setup notes, and plan with it.

## 1. Detect the surface

Check these signals in order and stop at the first clear answer.

| Signal | How to check | Means |
|---|---|---|
| A shell on the person's own computer | Run `echo "$CLAUDECODE"`, `uname -s`, `echo $HOME`. `CLAUDECODE=1`, or a home folder like `/Users/<name>` or `/home/<name>` with a `~/.claude/` folder in it | **Claude Code** (terminal, IDE, or the Code tab of Claude Desktop) |
| A shell in a temporary sandbox | Home is `/home/claude` or similar, outputs go to `/mnt/user-data/outputs/`, nothing of the person's own files is there | **Claude app** with code execution (claude.ai, Claude Desktop chat, mobile) |
| A selected local folder plus the Scheduled sidebar, no `~/.claude/` | The person says they're in Cowork, or you see a mounted work folder | **Cowork** in Claude Desktop: treat as Claude app, but files can be saved into the folder they picked |
| No shell or file tools at all | No code-execution tool is available | **Claude app without code execution**: ask them to turn on Settings → Capabilities → "Code execution and file creation" (skills need it), then start a new chat |

If the signals disagree, ask one question: "Are you using Claude Code (the terminal or the
Code tab), or the Claude app (claude.ai, the Desktop chat, or Cowork)?"

Write the answer in the Progress section of the setup file (`assistant-setup.md`) as
`surface: claude-code` or `surface: claude-app`.

## 2. What each surface can do

| Capability | Claude Code | Claude app (claude.ai / Desktop chat / Cowork) |
|---|---|---|
| Connectors (Gmail, Google Calendar, Drive, Notion, Todoist, Asana, Linear, Atlassian/Jira, Slack, Microsoft 365…) | Yes: claude.ai connectors on the same account, plus local MCP servers | Yes: Customize → Connectors |
| One Google account per connector | Yes, one per connector | Yes, one per connector |
| Install personal skills | Writes `~/.claude/skills/<name>/` itself | Claude builds a `.zip`; the person uploads it in Customize → Skills |
| Remove the kit's setup skills | `claude plugin uninstall assistant-kit@assistant-kit` after confirmation | The person deletes them in Customize → Skills (exact steps in kit-setup) |
| Python scripts (read-only second inbox, calendar feeds, gather-then-brief) | Yes, in a venv in the system folder | No lasting scripts (the sandbox is wiped) |
| Morning briefing / reminders on a schedule | Desktop scheduled task (local, needs the app open and the computer awake), cloud scheduled task (`/schedule`, runs with the computer off, connectors only), launchd/cron for scripts, GitHub Actions for API syncs | Scheduled tasks (paid plans): the "Scheduled" page in the sidebar (Claude Desktop, Cowork, and claude.ai in a browser where the person's account has it), or ask in a chat in the new Claude experience. Runs remotely with connectors; tasks that need local files run only on the computer |
| Notifications | Webhook to a private Discord/Slack channel or ntfy topic (one-way), plus the run's own session | The scheduled run's result in Claude; optionally an email **draft** to self, or a Slack message to self through the Slack connector |
| Second inbox (school / work / personal) | Read-only script (`gmail.readonly`) for a second Google account, or forwarding | Forwarding or a filter into the connected account only |

## 3. Facts that shape plans (verified October 2026)

- **A claude.ai connector holds one account.** The Gmail connector reads one Gmail; the
  Google Calendar connector reads that account's calendars (plus calendars shared with it).
  A second Google inbox needs forwarding into the first account, or, in Claude Code, a
  read-only script. Calendars are easier: share or subscribe the other calendar into the
  connected account.
- **There is no Google Tasks connector**, and no Canvas, Moodle or Google Classroom connector
  in the directory. Workarounds: Google Tasks through a script (Claude Code); Canvas and
  Moodle publish a calendar feed (ICS) that Google Calendar can subscribe to ("Other
  calendars → From URL"), after which the Calendar connector sees every deadline; Google
  Classroom puts due dates into a class calendar in the school account, which can be
  shared with the connected account, and sends email notifications.
- **Desktop scheduled tasks run only while the computer is awake and the app is open.** A
  missed run is caught up once on wake (the most recent one). Write briefing prompts that
  check the time and say "running late" instead of pretending it's 07:00.
- **A laptop that's closed overnight** runs its Desktop scheduled tasks when it's opened
  and Claude is running, not at the scheduled time (a scheduled wake doesn't help, since
  the app must be open too). If the briefing must be ready earlier and needs connectors
  only, use a cloud scheduled task; otherwise say "it arrives when you open your laptop".
- **Each Desktop scheduled task has one schedule.** A weekday 07:40 run plus a Saturday
  10:00 run is two tasks pointing at the same workflow.
- **launchd jobs can start in a "dark wake"** on a laptop on battery and then lose the
  network after a few seconds. Scripts wait for a full wake (`pmset -g systemstate` shows
  Graphics) or run on the charger.
- **Cloud scheduled tasks** (`/schedule`, claude.ai/code/routines) need a GitHub repo for
  Claude Code tasks, use only connectors (no local files), allow at most hourly runs, and
  every connector tool runs without asking. Remove connectors the task doesn't need.
- **Briefings get expensive.** One unattended briefing with many connectors loaded can
  re-read a large context 10–15 times (about 1–2M tokens). Keep them lean: gather data in
  one script or a few connector calls first, give the run only the connectors it needs,
  and write the briefing in one pass.

If the person's app shows something different from this file (menus move), trust what they
see and adapt.
