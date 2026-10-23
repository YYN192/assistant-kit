# Tune-up

**Runs:** on demand ("tune-up", "monthly check", "this isn't working"), ideally monthly.
**May write:** `SYSTEM.md` and workflow files, only after Priya approves each change; commit
locally in `~/assistant`, never push without asking.

This is how the system keeps fitting Priya after the setup kit is gone.

## 1. Health check (read-only)
- Each connector in SYSTEM.md §2–5 (Gmail, Google Calendar incl. the shared work calendar,
  Linear): one tiny read (the same tests used at setup). ✅/❌.
- Each script: `--help` runs; `gmail_readonly.py check --account uni` (and `work` if used) print the account
  domain, `gtasks.py check` prints the number of lists; token files exist in `~/.config/priya-assistant/`
  (by file name and age only, never contents).
- Each scheduled task: last runs and whether any were skipped (Mac asleep, app closed) or
  failed. Desktop: Code tab → Scheduled → each task's history; launchd: the log
  `~/Library/Logs/priya-assistant-moodle-sync.log`.
- Semester change? Check the Moodle feed still returns items (`ics_feed.py upcoming --days 30`).

## 2. Ask (at most 5 questions)
1. Which parts did you actually use? Which did you ignore?
2. Anything that was wrong, late, too long or annoying?
3. Anything new in your life: term, job, inbox, tool, schedule? (Internship ending?)
4. Do your time rules still fit (Sundays off, 21:30, 2.5 h, briefing time)?
5. One thing you wish it did?

## 3. Propose changes
A short list, each with the exact edit ("Briefing: move to 08:00"; "SYSTEM.md §6: protected
time adds Thursday 18–20"). Prefer removing things nobody uses over adding more.

## 4. Apply after OK
Edit SYSTEM.md (bump the version, add a change-log line) and the affected workflows.
Then `git -C ~/assistant commit -am "Tune-up <date>: …"` (local only). Update any scheduled
task whose time changed (Code tab → Scheduled → edit), and the launchd plist if the sync
time changed (show the commands; ask before reloading).
