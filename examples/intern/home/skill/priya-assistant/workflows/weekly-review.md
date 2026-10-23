# Weekly review and planner

**Runs:** Saturday 11:00 as a scheduled run (`priya-weekly-review`, unattended: prepare only)
and on demand ("plan my week", "weekly review"; "plan ok" applies the last proposal).
**May write:** calendar blocks in **Assistant** (personal account) and tasks in Google Tasks,
only after Priya approves the table. This is the only workflow that creates calendar blocks.

## Unattended (scheduled) run
Do steps 1–3, post the proposal with
`~/assistant/.venv/bin/python ~/assistant/scripts/notify.py post --title "Week plan" < file`,
save it to `~/assistant/state/week-proposal.md`, and end with: "Reply 'plan ok' in a chat
with your assistant to put these in your calendar." Don't write anything else.

## 1. Look back (last 7 days)
- Google Tasks completed vs. still open (`gtasks.py list --list <L> --all --json` for Uni, Work, Life;
  `--all` includes completed); anything overdue.
- Linear: issues moved to Done this week (read only).
- One line of honest encouragement, no lecture.

## 2. Look ahead (next 14 days)
- Deadlines from Google Tasks, the Moodle feed (`ics_feed.py upcoming --days 14`) and Linear
  due dates; tests and quizzes 🎯.
- Busy times per day from the personal primary calendar and the shared work calendar.
- Free slots: not busy, **never Sunday**, not after 21:30, not in quiet hours (22:00–07:30),
  not in the 20 min before work (Mon/Tue/Thu 08:40–09:00), not Wed/Fri lecture mornings.

## 3. Propose
- One block per task chunk, 25–90 minutes, 10 min break between back-to-back blocks; split
  anything over 90 minutes into sessions on different days; finish one day before each
  deadline; start test prep ~7 days ahead.
- Daily cap: **2.5 h** of planned study. Nothing on Sunday, nothing after 21:30.
- If it doesn't fit: say what doesn't fit and ask what to drop or move. Never squeeze into
  protected time; offer nearest options outside the rules only as a question.

| # | Day | Time | Block | For | Calendar |
|---|---|---|---|---|---|
| 1 | Sat 24 Oct | 13:00–14:30 | ◆ Thesis ch. 2 (1/2) | Dr. Chen, due Mon 26 Oct | Assistant |

"Reply 'ok', or tell me what to change."

## 4. After OK
If the **Assistant** calendar doesn't exist yet, say so and create it in the personal account
(first write: ask once). Create each block there with the title prefix "◆ " and a reminder
10 min before (no reminders on Sunday or in quiet hours). Reply with a one-line summary per
day. Moving a block later: only blocks starting with "◆ "; update, don't delete-and-recreate.
If anything else is due soon and has no task yet, offer to add it (task-capture).
