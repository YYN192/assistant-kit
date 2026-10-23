# Question bank

Pick from these; never ask them all. Defaults are in brackets. Questions marked ★ are on
the "must know" list.

## Contents
1. Core (everyone)
2. School (secondary school)
3. University
4. Work (office, engineering, ops)
5. Intern / mixed lives
6. Accounts and email
7. Calendars
8. Task tools
9. Time rules
10. Language and tone
11. Notifications
12. Privacy limits
13. Claude Code extras

## 1. Core (everyone)
- ★ What should I call you, and in which language should the assistant write to you? [English]
- ★ Which time zone are you in? [from the computer, if visible]
- ★ What are the 1–3 things that slip most often, or that you'd most like off your plate?
- What does a good day look like, and what wrecks one?
- How do you track things today (app, paper, memory, email flags)?
- How much do you want it to do on its own versus suggest? [suggest; writes after OK]

## 2. School (secondary school)
- ★ Where does homework come from: the teacher says it in class, an online platform
  (Google Classroom, a school diary app, Moodle), email, or a group chat?
- ★ Where are tests and their dates announced?
- Is there a timetable I can copy from a photo or a PDF?
- Private lessons, clubs, sports? Fixed times or changing every week?
- Do your parents or tutors email you, or does it all go through you?
- Do you want study blocks planned, or just reminders?

## 3. University
- ★ Which learning platform (Canvas, Moodle, Blackboard, Brightspace, Google Classroom)?
  Can you find its "calendar feed" or "export calendar" link? (I'll show you where.)
- ★ Do lectures give homework in the slides or out loud? Do you get slides as PDFs?
  (Task capture can read a slide deck and pull out readings, problem sets and due dates.)
- Exams and coursework deadlines: published once per term (a PDF/handbook) or ad hoc?
- Your uni email: Google (Gmail), Microsoft (Outlook), or something else?
- Part-time job or society commitments with fixed hours?
- Group projects? Where does the group coordinate (Slack, Discord, WhatsApp, Notion)?

## 4. Work (office, engineering, ops)
- ★ Where is your work assigned: Jira, Linear, Asana, GitHub issues, Notion, email?
  Which project or board, and do you want only issues assigned to you?
- ★ Work email and calendar: Google Workspace or Microsoft 365? Does your company allow
  connecting it to Claude? (If unsure: we test it read-only and see.)
- Recurring meetings you need to prepare for (stand-up, 1:1, weekly review)?
- Do you write a stand-up or weekly status update? To whom, and in what format?
- What counts as urgent at work (manager, specific clients, on-call)?
- Is there anything your company forbids sending to outside tools? (We'll respect it.)
- Which chat channels carry real requests (Slack/Teams)? Read only; it never posts there.
- Labels or projects to keep out of summaries (e.g. "confidential")?
- Meetings you'd like prep notes for?

## 5. Intern / mixed lives
- ★ List your inboxes: personal, school, work. Which one would you check first if you
  could only check one?
- ★ Who are the 3–5 senders who must never be missed (manager, supervisor, professor,
  HR, parent)?
- Do school and work deadlines go in the same task list, or separate ones?
- Which hours belong to work, to school and to you?
- Anything the work side must not see from the school/personal side, or vice versa?

## 6. Accounts and email
- ★ For each inbox: address domain (e.g. "@gmail.com", "@company.com"), provider, and
  whether it may be read by the assistant.
- Which one is "home": the account the Gmail or Google Calendar connector should hold?
  [the personal Google account] (Only one account per connector.)
- Could the other inboxes forward to the home account, or to a label in it?
  [forwarding works for most school and personal accounts; work often forbids it]
- Labels or folders that matter? Senders to always skip (newsletters, notifications)?
- Should it draft replies, and in what tone (formal, friendly, short)?

## 7. Calendars
- ★ Where are your fixed events (classes, shifts, meetings)? One calendar or several?
- ★ Which calendar may the assistant add events to? [a new calendar called "Assistant"
  so its events are easy to spot and remove]
- Should it colour-code? [no; keep it simple unless they love colours]
- Travel time between places? [15 min before and after anything off-site]

## 8. Task tools
- ★ Where should tasks live? Options: Todoist, Notion, Asana, Linear, Jira, Google Tasks
  (Claude Code only, through a script), Microsoft To Do (no connector: we'd use calendar
  items instead), or "calendar all-day items" if they use nothing.
- One list or several (school / work / personal)?
- Due dates when none is given: [the day before the next class/meeting with that person,
  or ask]
- How should a task title look? [their own words, with a short [Course] or [Project] tag]

## 9. Time rules
- ★ Hours when you're busy anyway (school/work/commute)?
- ★ Protected free time the assistant must never plan into (evenings, a weekend day,
  sports, family time)?
- ★ Any no-go days for a kind of activity (e.g. "never Wednesday for extra lessons")?
- Quiet hours for notifications? [22:00–07:00] (Notifications only. If the briefing time
  falls inside them, ask which wins.)
- Maximum focused work/study per day the assistant may plan? [2 hours on school/work days]
- When do you want the morning briefing? Weekends too? [weekdays 07:00, none on weekends]
- Weekly review: which day and time? [Sunday 18:00]

## 10. Language and tone
- Language for the briefing and for task titles (they can differ: "titles in German,
  briefing in English").
- Short and punchy, or a bit more explanation? [short]
- Emoji in briefings? [a few, as section markers]
- Weather in the briefing (which city)? News (which topics)? [neither]

## 11. Notifications
- ★ Where should the briefing reach you?
  - Claude app: in the scheduled task's own chat (default), optionally a Slack DM to self
    or an email draft to self.
  - Claude Code: the run's session, optionally a private Discord/Slack channel webhook or
    an ntfy topic on the phone (one-way: the assistant never reads replies there).
- Do you want alerts when a sync fails? [yes, short]

## 12. Privacy limits
- ★ Anything it must never read or summarise (health, bank, a specific person, a label)?
- Anything it must never write anywhere (grades, salary, medical)?
- Is it fine to keep a small state file of which emails were already handled? [yes,
  ids only, no content]

## 13. Claude Code extras (only on Claude Code)
- Are you OK running one command in your own terminal to sign in to Google for a
  read-only script? (You type the login yourself in the browser; I never see it.)
- Is your computer usually on and awake at the briefing time? [if no: cloud scheduled task]
- Do you already have a GitHub account? (Only needed for cloud syncs; optional.)
