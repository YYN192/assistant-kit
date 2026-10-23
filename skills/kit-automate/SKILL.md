---
name: kit-automate
description: Sets up the automatic parts of a personal assistant built with assistant-kit, matched to what the surface can really schedule. Creates the morning briefing, weekly review and reminder schedules (Claude app scheduled tasks, Claude Code Desktop scheduled tasks or cloud scheduled tasks), and on Claude Code also read-only sync scripts (second Gmail inbox, Google Tasks, Canvas or Moodle calendar feeds), launchd, cron or GitHub Actions jobs, and one-way Discord, Slack or ntfy notifications. Use it in stage 5 of the setup after the personal skill exists, or whenever someone asks to schedule, change or fix their briefing, reminders, syncs or notifications.
license: MIT
---

# Assistant kit: automations

Input: the approved Plan's "Automatic runs" table and the personal skill (hub) built by
kit-generate. Read `references/SURFACES.md` and `references/SAFETY.md` first.

Principles:
- **Every automation calls the hub skill**; the scheduled prompt stays a few lines long.
  Facts live in `SYSTEM.md`, so changing a rule never means editing a schedule.
- **Unattended runs never ask questions** and only do what their workflow allows.
- **Lean runs:** only the connectors the workflow needs; gather first, write once.
- **Honest limits:** tell the person what will make a run skip (computer asleep, app
  closed, a connector signed out) and write it in `SYSTEM.md` §8.
- **Ask before creating each schedule** (show name, time, prompt), and log it in the
  setup file's Build log and in `SYSTEM.md` §8.

## Claude app (claude.ai, Desktop chat, Cowork)

Read `references/claude-app.md`. In short:
1. Write the scheduled prompt from `assets/scheduled-prompt.md` (fill the hub name and
   workflow).
2. If a scheduled-task tool is available in this chat (for example one that creates or
   lists scheduled tasks), offer to create it, show the exact settings, and create it after
   a yes. Otherwise give the click-by-click steps from the reference and wait while the
   person does it.
3. During setup, the first **Run now** belongs to stage 6 (testing), with the person
   watching. When kit-automate is used on its own later, ask them to press **Run now**
   once and paste or describe the result; fix and repeat.

## Claude Code

Read `references/claude-code.md`. Choose per automation:

| Need | Use |
|---|---|
| Briefing/review that needs local scripts or files | **Desktop scheduled task** (Code tab → Scheduled), folder = the system folder |
| Briefing with connectors only, computer often off | **Cloud scheduled task** (`/schedule` or claude.ai/code/routines); needs the system folder pushed to a private GitHub repo: ask first |
| Data sync with no AI (feed → tasks, inbox digest) | Script + **launchd** (macOS) / **cron** or systemd timer (Linux) / Task Scheduler (Windows) via `assets/run_job.sh`; or **GitHub Actions** for cloud API syncs |
| Push notification | `assets/scripts/notify.py` (Discord/Slack webhook or ntfy topic; one-way) |

Scripts in `assets/scripts/` are templates to copy into `<home>/scripts/`:

| Script | Does | Access |
|---|---|---|
| `common.py` | config (`<home>/assistant.json`), secrets and state folders | — |
| `google_auth.py` | OAuth sign-in in the browser; token saved with mode 600 | — |
| `gmail_readonly.py` | `auth`, `check`, `list`, `read` for a **second** Google inbox | `gmail.readonly` |
| `gtasks.py` | `auth`, `check`, `lists`, `list`, `add`, `done` | `tasks` |
| `ics_feed.py` | `add` (URL typed hidden in the person's own terminal), `list`, `upcoming` | read a calendar feed |
| `feed_to_tasks.py` | deadlines from a feed → Google Tasks, no duplicates | feed + `tasks` |
| `gather.py` | one compact JSON for the briefing: feeds, read-only inboxes, weather | read only |
| `notify.py` | `setup`, `post`, `alert`, `test` | posts only, reads nothing back |

Setup order for scripts:
1. Copy the scripts you need, `requirements.txt` and `assets/gitignore` (as
   `<home>/.gitignore`) into the system folder; create `<home>/assistant.json` from
   `assets/assistant.example.json`.
2. Create the venv: `python3 -m venv <home>/.venv && <home>/.venv/bin/pip install -r <home>/requirements.txt`.
   (Python packages in the system's own venv are fine; ask before installing anything else.)
3. Google scripts need an OAuth client. Walk the person through
   `references/google-oauth-client.md` (they click; you never see secrets), then have them
   run the `auth` command **in their own terminal**. Afterwards run `check` yourself.
4. Run each script once by hand (`--help`, `check`, a `--dry-run` where offered).
5. Schedule it, then run the job once immediately and read its log.

## After setting up

- Fill `SYSTEM.md` §8 (what, when, mechanism, where, limitation) and §9 (files and secret
  file *names*).
- Commit the system folder locally (`git add -A && git commit`); confirm with
  `git status --ignored` that nothing under the secrets folder or `state/` is tracked.
- Script jobs (launchd, cron, Actions): run each once now and read its log. Scheduled
  Claude runs get their first **Run now** in stage 6, unless kit-automate is used on its own.
