# Tune-up

**Runs:** on demand ("tune-up", "monthly check", "this isn't working"), ideally monthly.
**May write:** `SYSTEM.md` and workflow files, only after {{Name}} approves each change;
{{Claude Code: commit locally, never push without asking}}.

This is how the system keeps fitting {{Name}} after the setup kit is gone.

## 1. Health check (read-only)
- Each connector in SYSTEM.md §2–5: one tiny read (the same tests used at setup). ✅/❌.
<!-- choose: claude-code -->
- Each script: `--help` runs; tokens exist (by file name and age only, never contents).
- Each scheduled task: last runs and whether any were skipped (computer asleep, app
  closed) or failed. Desktop: the Scheduled page / history; launchd: the log file named in
  SYSTEM.md §8.
<!-- end choose -->
<!-- choose: claude-app -->
- Ask {{Name}} to open the **Scheduled** page and say whether the last runs show
  "skipped" or errors, or paste the last briefing.
<!-- end choose -->

## 2. Ask (at most 5 questions)
1. Which parts did you actually use? Which did you ignore?
2. Anything that was wrong, late, too long or annoying?
3. Anything new in your life: term, job, inbox, tool, schedule?
4. Do your time rules still fit (protected time, no-go days, briefing time)?
5. One thing you wish it did?

## 3. Propose changes
A short list, each with the exact edit ("Briefing: drop news, move to 07:30";
"SYSTEM.md §6: protected time adds Thursday 18–20 (football)"). Prefer removing things
nobody uses over adding more.

## 4. Apply after OK
Edit SYSTEM.md (bump the version, add a change-log line) and the affected workflows.
<!-- choose: claude-app -->
Then re-package: if a code tool is available, zip the skill folder (folder at the top
level) and give {{Name}} the new zip with the upload steps (Customize → Skills → +
→ Upload a skill; replace the old one). If not, show the changed files and ask {{Name}} to
run the tune-up in a chat with code execution on.
<!-- end choose -->
<!-- choose: claude-code -->
Then `git -C {{~/assistant}} commit -am "Tune-up <date>: …"` (local only). Update any
scheduled task whose time changed.
<!-- end choose -->
