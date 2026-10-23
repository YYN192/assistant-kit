# Scheduling in Claude Code

## Contents
1. Desktop scheduled task (local)
2. Cloud scheduled task
3. launchd (macOS) with wake handling
4. cron / systemd (Linux), Task Scheduler (Windows)
5. GitHub Actions for script syncs
6. Notifications

## 1. Desktop scheduled task (local)

Runs on the person's machine with the system folder, scripts and connectors. Only fires
while the Claude Desktop app is open and the computer is awake; after a sleep, exactly one
catch-up run happens for the most recent missed time.

Create it (ask first):
- **By asking** in a Desktop session: "Create a scheduled task named `<hub>-briefing` that
  runs weekdays at 07:00 in `<home>` with this prompt: …". Desktop stores the prompt in
  `~/.claude/scheduled-tasks/<task-name>/SKILL.md` (frontmatter `name` and `description`,
  prompt as the body). Schedule, folder, model and enabled state are not in that file.
- **By hand:** Code tab → **Scheduled** → **New task** → **Set up manually** → Name →
  instructions → Advanced settings → **Only on this computer** on → **Local folder** =
  `<home>` → Trigger: Weekdays 07:00 → permission mode → **Create**.

Each task has **one** schedule: a weekday run and a different weekend run are two tasks
(e.g. `<hub>-briefing` and `<hub>-briefing-weekend`, the second saying "weekend variant:
lighter, at most one focus item").

Then click **Run now** (in stage 6, with the person) and approve the tools it needs with
"always allow", so later runs don't stall on a permission prompt. Read the run's session.

Reliability tips for the person (a laptop closed overnight runs the task when it's opened
and Claude is running; say so in the plan):
- Keep the app open; Settings → This computer → System → **Keep computer awake** stops
  idle sleep (closing the lid still sleeps).
- On a Mac, a scheduled wake helps: `sudo pmset repeat wakeorpoweron MTWRF 06:55:00`.
  This needs their admin password, so **they** run it in their own terminal, if they want.

## 2. Cloud scheduled task

Runs on Anthropic's cloud, even with the computer off. Needs a GitHub repository (it
clones it each run), uses only claude.ai connectors (no local files, no local tokens), at
most hourly, and runs every included connector tool without asking.

- Create with `/schedule` in Claude Code, or at claude.ai/code/routines → **New task**.
- The system folder must be a **private** GitHub repo: ask before creating it and before
  pushing. Secrets never go in the repo.
- In the task's **Connectors** tab, remove every connector the workflow doesn't need.
- The prompt says "Use the `<hub>` skill" only if the skill is in the repo
  (`.claude/skills/<hub>/` in the repo works for cloud runs). Otherwise point the prompt at
  `skill/<hub>/SKILL.md` in the clone.

## 3. launchd (macOS) with wake handling

For scripts only (no Claude in the loop): feed → tasks, inbox digest, etc.

1. Copy `assets/run_job.sh` to `<home>/scripts/run_job.sh` and make it executable.
   It waits up to 10 minutes for a **full wake** (`pmset -g systemstate` lists Graphics),
   because a laptop on battery can start a job in a "dark wake" and sleep again within
   seconds, which made syncs time out. It runs the command under `caffeinate -i`, logs to
   `~/Library/Logs/<hub>-<job>.log`, and on failure calls `notify.py alert`.
2. Fill `assets/launchd.plist` (label `com.<hub>.<job>`, time, paths) and save it to
   `~/Library/LaunchAgents/com.<hub>.<job>.plist`.
3. Load: `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.<hub>.<job>.plist`
   and test now: `launchctl kickstart -k gui/$(id -u)/com.<hub>.<job>`, then read the log.
4. Remove later with `launchctl bootout gui/$(id -u)/com.<hub>.<job>` (ask first).

## 4. cron / systemd (Linux), Task Scheduler (Windows)

- cron: `crontab -e` and add
  `0 7 * * 1-5 <home>/scripts/run_job.sh feed-sync <home>/.venv/bin/python <home>/scripts/feed_to_tasks.py sync`
  (`run_job.sh` skips the macOS wake check on other systems).
- systemd user timer: a `.service` running the same command and a `.timer` with
  `OnCalendar=Mon..Fri 07:00`, `Persistent=true` (catches up after sleep).
- Windows: Task Scheduler → Create Basic Task → Daily → Start a program:
  `<home>\.venv\Scripts\python.exe` with arguments `<home>\scripts\feed_to_tasks.py sync`;
  tick "Run task as soon as possible after a scheduled start is missed".

## 5. GitHub Actions for script syncs

For API syncs that should run with the computer off (e.g. a calendar feed → Google Tasks
twice a day). Not for anything that needs a home IP or the person's local files.

1. Private repo only; ask before creating it and before pushing.
2. Copy `assets/github-workflow.yml` to `<home>/.github/workflows/sync.yml`.
3. Secrets go to the repo's **Settings → Secrets and variables → Actions**. The person
   pastes them there themselves (token file contents, feed URLs). You never print them.
4. Run it once with **Run workflow** and read the log (it must not print secrets).

## 6. Notifications

`notify.py` posts to one place, one way: a Discord or Slack incoming webhook, or an ntfy
topic. It never reads anything back, so nobody can send the assistant instructions through
that channel.

- Setup: the person runs `<home>/.venv/bin/python <home>/scripts/notify.py setup` in
  their own terminal and pastes the webhook URL or topic there (hidden input). It's saved
  to `<secrets>/notify.json` with mode 600.
- `notify.py test` posts "test"; `notify.py post --title Briefing < file` posts a file;
  `notify.py alert "text"` posts ❗ text.
- No channel configured → it prints a note and exits 0, so jobs don't fail because of it.
- Quiet hours from `assistant.json` hold back everything except alerts.
