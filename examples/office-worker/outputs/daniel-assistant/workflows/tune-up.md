# Tune-up

**Runs:** on demand ("tune-up", "monthly check", "this isn't working"), ideally monthly.
**May write:** `SYSTEM.md` and workflow files, only after Daniel approves each change.

This is how the system keeps fitting Daniel after the setup kit is gone.

## 1. Health check (read-only)
- Each connector in SYSTEM.md §2–5, one tiny read: Google Calendar (list calendars; is
  "Outlook (work)" still there and showing this week's stand-ups?), Atlassian (first 5 of
  "Mine"), Slack (#analytics-team, last day, first 3). ✅/❌.
- Microsoft 365: ask whether IT has approved it since; if yes, offer to add Outlook mail
  (read only) in a new plan step.
- Ask Daniel to open the **Scheduled** page and say whether the last runs of
  `daniel-assistant-briefing` and `daniel-assistant-friday-update` show "skipped" or errors,
  or paste the last briefing.

## 2. Ask (at most 5 questions)
1. Which parts did you actually use? Which did you ignore?
2. Anything that was wrong, late, too long or annoying?
3. Anything new: team, project, tool, manager, schedule?
4. Do your time rules still fit (18:30 cut-off, lunch, Wednesday, 08:30 briefing)?
5. One thing you wish it did?

## 3. Propose changes
A short list, each with the exact edit ("Briefing: drop meeting prep for the stand-up";
"SYSTEM.md §6: lunch moves to 13:30–14:30"). Prefer removing things nobody uses over adding
more.

## 4. Apply after OK
Edit SYSTEM.md (bump the version, add a change-log line) and the affected workflows.
Then re-package: if a code tool is available, zip the skill folder (folder at the top
level) and give Daniel the new zip with the upload steps (Customize → Skills → +
→ Upload a skill; replace the old one). If not, show the changed files and ask Daniel to
run the tune-up in a chat with code execution on. If a scheduled time changes, tell Daniel
to edit that task on the Scheduled page.
