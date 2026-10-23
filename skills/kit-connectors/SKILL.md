---
name: kit-connectors
description: Plans and checks the connections a personal assistant needs, as stage 2 of the assistant-kit setup. Maps each inbox, calendar and task or work tool from the profile to a claude.ai connector (Gmail, Google Calendar, Drive, Microsoft 365, Notion, Todoist, Asana, Linear, Atlassian Jira, Slack) or a workaround (mail forwarding, calendar feed subscription, read-only script), asks the person to connect each one, and proves it works with a read-only test. Use it when the setup reaches connectors, when someone asks "which connectors do I need", "connect my second inbox", "why can't Claude see my school email", or when a connector in an existing assistant stopped working.
license: MIT
---

# Assistant kit: connectors

Goal: every source in the profile is either **connected and read-tested**, **covered by a
workaround**, or **consciously left out**, and the Connectors section of the setup file says
which.

Read `references/SURFACES.md` (facts about each surface) and `references/SAFETY.md`
(rule 2: never handle passwords; rule 3: read-only first) before starting.

## 1. Build the needs list

From the Profile, list every source and sink: each inbox, each calendar (read and write),
the task destination, work trackers, and the notification channel. One row each.

## 2. Map each need

Use `references/connector-map.md`. For each row choose, in this order of preference:

1. a **connector** the person can add themselves (Customize → Connectors in the Claude
   app; the same list is used by Claude Code, and `claude mcp add` adds local ones);
2. a **no-code workaround**: forwarding a second inbox into the home account, sharing or
   subscribing a calendar into the connected account, a learning platform's calendar feed;
3. on Claude Code only, a **read-only script** from kit-automate (second Gmail account,
   Google Tasks, calendar feed reader);
4. **leave it out** and say what the person loses.

Remember the hard limit: **one account per connector.** Decide which Google (or Microsoft)
account is "home" first; everything else is forwarded, shared or scripted.

Before telling someone a connector exists, check: if you have a connector-search tool
(for example a registry search or "suggest connectors" tool), search for it; otherwise ask
them to look in Customize → Connectors → Browse. Directories change; don't promise a
connector you haven't seen.

## 3. Ask them to connect

Give click-by-click steps (from the map) and wait. Steps the person does on their own
(connecting two connectors, setting up forwarding, subscribing a feed) can go in one
message, numbered, up to three at a time; then test each one separately. Say plainly:

> "Sign in on the service's own page. I never see or need your password."

If their organisation blocks a connector (common for work Microsoft 365 or Atlassian),
don't push; switch to the next option and note it.

## 4. Read-only test each one

Run the test from `references/read-only-tests.md` for that connector. Show the person the
smallest proof that it's the **right account**, such as "I can see 3 mails from today; the
newest is from Canvas Notifications", without dumping content. Record:

```
| Source | Method | Account (domain only) | Access | Test | Date |
| Personal mail | Gmail connector | @gmail.com | read + drafts | ✅ 3 msgs today | 2026-10-22 |
```

Apply the profile's privacy limits even here: a message from a "never read" sender is
reported as "1 private, skipped", not by sender and subject.

If a test fails: check it's enabled for this chat (the connector toggle under the "+" or
tools menu), reconnect, then try once more. After two failures, mark it ❌ with the error
and move on. Never retry in a loop. A calendar feed that was just subscribed can stay
empty for several hours: mark it ⏳ "pending, re-test in stage 6", not ❌.

## 5. Workarounds, step by step

Give the steps in the map for forwarding, calendar sharing and feed subscriptions. After
the person says it's done, test through the home account (search for a forwarded mail,
list events from the subscribed calendar).

For a **read-only script** (Claude Code), test the risky part now, before the plan: if the
person is up for it, do the one-time OAuth client (kit-automate
`references/google-oauth-client.md`) and have them run the script's `auth` in their own
terminal now. Organisations often block unverified apps (`admin_policy_enforced`), and
it's better to learn that before the plan is approved. If they'd rather wait, mark the
source "⏳ untested script" and the plan must give it a fallback.

## 6. Write the Connectors section

Use the table above, plus:

- **Home account** for each connector.
- **Write access** that the plan will need, still unused ("Todoist: will create tasks in
  project Uni after you approve the plan").
- **Not connected** and why, with the workaround or what is lost.
- **Connectors to leave out of unattended runs** (anything the briefing doesn't need).

Then tell kit-setup (or the person) that stage 2 is done.
