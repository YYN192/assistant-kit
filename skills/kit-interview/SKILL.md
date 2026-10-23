---
name: kit-interview
description: Interviews a person to learn what their personal assistant should do, as stage 1 of the assistant-kit setup. Covers their role (school, university, work, intern or a mix), email accounts, calendars, task tools (Google Tasks, Todoist, Notion, Jira, Linear, Asana, Canvas, Moodle, Classroom), time rules and no-go days, language, how they want to be notified, and privacy limits, then writes a structured profile. Use it when the kit-setup flow reaches the interview, when someone says "interview me" or "ask me questions for my assistant", or when an existing assistant profile needs updating after a life change such as a new job, term or inbox.
license: MIT
---

# Assistant kit: interview

Goal: a profile complete enough to plan from, gathered in **three or four short rounds**,
not a questionnaire. People quit long forms; they enjoy a good conversation.

## How to run it

1. **Open with one broad question** and let them talk:
   "Tell me about a normal week: what you do, what keeps slipping, and what you'd love an
   assistant to take off your plate." From the answer, guess their role(s) and fill
   whatever you can.
2. **Pick the question set** for their role(s) in `references/question-bank.md`. Mixed
   lives (intern = school + work + personal) take the core set once plus the parts that
   differ per role.
3. **Ask in rounds of at most five questions.** Skip anything already answered. Offer a
   default in brackets so they can answer "fine" ("Morning briefing time? [07:00 on
   weekdays]"). Number the questions so they can answer "1 yes, 2 Todoist, 3 skip".
4. **Read the answers back as decisions**, not as a transcript: "So: school Gmail is the
   one with deadlines, personal is mostly noise, work is Outlook." Correct on the spot.
5. **Stop when the "must know" list is complete** (below). Anything else gets a sensible
   default, marked `(default)` in the profile so the tune-up can revisit it.

## Must know before planning

- Name to use, language(s), time zone.
- Roles and the 1–3 pains they most want fixed (their words, quoted).
- Every inbox: provider, which account, what matters in it, whether it can be connected.
- Calendars: where fixed events live (classes, shifts, meetings) and which calendar the
  assistant may write to.
- Where tasks should live (one destination if possible) and where deadlines come from.
- Time rules: working/study hours, protected free time, no-go days, quiet hours, travel
  buffers. Quiet hours mean **no notifications**; "no study after 21:30" is a separate
  rule. **Check the briefing time is outside quiet hours**; if not, ask which wins and
  record the exception.
- Notification: where the morning briefing should arrive and when; weather and news in
  it or not (default: neither).
- Chat apps (Slack, Teams, Discord) that carry real work or study requests: which
  channels to read, and that the assistant never posts there.
- Privacy limits: senders, labels or topics never to read or summarise; things never to
  write anywhere.
- Surface (from kit-setup) and, for Claude Code, whether they're comfortable running a
  command in a terminal now and then.

## Rules while interviewing

- **Never ask for passwords, codes or tokens**, not even "just the app password". If they
  offer one, decline and say why (SAFETY.md rule 2). Ask for account *names* only, like
  "your school Google account (the @uni.edu one)".
- Don't ask for data you won't use. No birthdays, addresses or IDs.
- Email addresses go into the profile only when the plan needs them (for example to
  recognise a teacher's or manager's mail). Write them exactly as given.
- Respect "skip". A skipped topic gets a default or is left out of the plan.
- If they're overwhelmed, shrink scope: "Let's start with just the morning briefing and
  homework capture. We can add the rest in a tune-up."

## Writing the profile

Fill `references/profile-template.md` into the Profile section of the setup file. Quote
their pain points verbatim; the plan ties each module to a quote. Mark guesses with
`(default)` or `(guess)`. Then show a five-line summary and ask "Did I get that right?"

Read `references/SAFETY.md` once before starting so you know which requests to refuse.
