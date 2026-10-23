# Scheduling in the Claude app

Scheduled tasks are on paid plans (Pro, Max, Team, Enterprise). Each run is a fresh
session that can use the person's connectors, skills and plugins. Menus move between app
versions; if the person sees different labels, follow what they see.

## Create a scheduled task

**Which option?** Ask the person: "Do you see **Scheduled** in the left sidebar?" If yes
(Claude Desktop, Cowork, or claude.ai in a browser where it's rolled out), use option B.
If not, try option A. If neither works on their plan or app, fall back to option C.

**Option A, ask in a chat (new Claude experience):** in any chat, the person can describe
it ("every weekday at 7:00, run my morning briefing"); Claude proposes a name, schedule and
instructions, and the person clicks **Schedule**. If you can create or propose scheduled
tasks yourself in this chat, do that after showing the settings and getting a yes.

**Option B, the Scheduled page:**
1. Click **Scheduled** in the left sidebar, then **New task** (top right).
2. Choose **Set up manually**.
3. **Name:** `<hub>-briefing` (or `-weekly-review`, `-weekly-status`).
4. **Prompt:** paste the text from `assets/scheduled-prompt.md`, filled in, including the
   "Use only these connectors" line.
5. **Frequency:** Daily / Weekdays / Weekly, and the time. (Options are hourly, daily,
   weekdays, weekly or manual.)
6. **Approval mode** (labels vary by version): pick the setting that asks before actions
   rather than the one that allows everything. The run only reads, plus its one approved
   delivery (e.g. a draft to self); if that delivery stalls waiting for approval, the
   person approves it once from the run's page.
7. **Connectors:** if the form lists connectors or tools for the task, switch off every
   one the workflow doesn't use. If it doesn't, the prompt's "Use only these connectors"
   line is the limit; say so to the person.
8. Click **Save**. Don't press **Run now** yet: stage 6 (testing) does that with the
   person watching. If you're adding a schedule after setup, press **Run now** once and
   check the result.

**Option C, no scheduler available:** make it a one-tap habit instead: a recurring
calendar event "☀️ Ask for my briefing" at the briefing time, and the person types "brief
me" when it pops up. Say plainly that this isn't automatic.

## Limits to tell the person

- Tasks run remotely and keep their schedule while the computer sleeps, **unless** they
  need local files or apps; then they run only on the computer, while it's awake and
  Claude is open, and a missed run is done later.
- Each run uses the connectors that are enabled; a signed-out connector makes the
  briefing incomplete. The briefing's "Needs you" section reports it.
- Runs count against the plan's usage. One short daily run is cheap; hourly runs aren't.
- To pause: Scheduled → the task → pause. To change the time: edit the task. To change
  what it does: edit `SYSTEM.md` / the workflow in the skill (tune-up), not the schedule.

## Weekly review

Same steps, weekly at their review time, with the weekly-review workflow. The run only
prepares the table; the person approves it in a normal chat ("plan ok").

## Reminders

For a single deadline, a calendar event with a notification is simpler and more reliable
than a scheduled task. Offer that first (table + OK as usual).
