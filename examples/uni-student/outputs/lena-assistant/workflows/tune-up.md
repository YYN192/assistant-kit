# Tune-up

**Runs:** on demand ("tune-up", "monthly check", "this isn't working"), ideally monthly.
**May write:** `SYSTEM.md` and workflow files, only after Lena approves each change.

This is how the system keeps fitting Lena after the setup kit is gone.

## 1. Health check (read-only)
- Each connector in SYSTEM.md §2–4, one tiny read: Gmail `newer_than:2d` (max 3), Gmail
  `label:uni newer_than:7d` (max 3), Google Calendar: list calendars (primary, Assistant,
  Canvas present?) and today's events, Todoist: project "Uni" exists. ✅/❌ each.
- If `label:uni` is empty for 7 days, the forwarding or filter may have stopped: ask Lena
  to check uni Gmail → Settings → Forwarding.
- Ask Lena to open the **Scheduled** page and say whether the last runs show "skipped" or
  errors, or paste the last briefing.

## 2. Ask (at most 5 questions)
1. Which parts did you actually use? Which did you ignore?
2. Anything that was wrong, late, too long or annoying?
3. Anything new: term, timetable, café shifts, modules, inbox, tool?
4. Do your time rules still fit (Friday evening, Sunday morning, quiet hours, 3 h cap, 08:15 briefing)?
5. One thing you wish it did?

## 3. Propose changes
A short list, each with the exact edit ("Briefing: move to 08:30"; "SYSTEM.md §6:
protected time adds Thursday 18–20"). Prefer removing things nobody uses over adding more.
New term: update the course list in SYSTEM.md §3.

## 4. Apply after OK
Edit SYSTEM.md (bump the version, add a change-log line) and the affected workflows.
Then re-package: if a code tool is available, zip the skill folder (folder at the top
level) and give Lena the new zip with the upload steps (Customize → Skills → + → Upload a
skill; replace the old one). If not, show the changed files and ask Lena to run the
tune-up in a chat with code execution on. If a schedule time changed, tell her to edit the
task on the Scheduled page.
