# Calendar blocking with rules

**Runs:** on demand ("block 2 hours for the essay this week", "find time to study for the
exam", "add my timetable").
**May write:** events in **{{Assistant}}** only, after OK when there are 2 or more (rule 6).
Never moves or deletes {{Name}}'s own events.

## Rules (from SYSTEM.md §6, apply all)
- Busy anyway: {{…}}
- **Protected, never:** {{…}}
- No-go days: {{…}}
- Quiet hours: {{…}} (no blocks and no reminders)
- Daily cap on planned work/study: {{…}}
- Travel buffer: {{…}} before and after off-site events
- Block length: {{25–90}} minutes; breaks of {{10}} minutes between back-to-back blocks

## Steps
1. Read the busy times from {{calendars}} for the requested range (default: next 7 days).
2. List candidate slots that pass every rule. Prefer {{their preference, e.g. afternoons
   after 15:00, the same time each day}}.
3. Propose a table:

   | # | Day | Time | Title | Calendar | Reminder |
   |---|---|---|---|---|---|

   Title prefix "{{◆ }}". If the request can't fit, say so and offer the nearest options
   outside the rules only as a question, never as a booking.
4. After OK, create them, then list what was created.

## Recurring blocks and timetables
For a timetable (photo, PDF, pasted): build the weekly table, ask for the start and end
dates (term end), show it, and after OK create recurring events in **{{Assistant}}** that
end on that date.

## Moving things
"Move my study block to tomorrow": only blocks the assistant created (title prefix
"{{◆ }}"). Update, don't delete-and-recreate.
