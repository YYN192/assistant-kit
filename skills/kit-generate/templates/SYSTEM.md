# {{Name}}'s assistant: SYSTEM

> Single source of truth for {{Name}}'s assistant. Read all of it before acting.
> version {{1}} · built {{YYYY-MM-DD}} with assistant-kit · surface: {{claude-code | claude-app}}
> Change this file (not the workflows) when a fact changes, then re-package (Claude app) or
> just save (Claude Code).

## 0. Who

- **Name:** {{Name}} · **Language:** briefing {{en}}, task titles {{…}}, drafts {{match the thread}}
- **Time zone:** {{Europe/…}} · **Roles:** {{…}}
- **What this system is for (their words):**
  1. "{{…}}"
  2. "{{…}}"

## 1. Architecture

```
{{ASCII diagram: sources → how (connector/forward/script) → where things land → automations}}
e.g.
Personal Gmail ───────────── Gmail connector ─┐
School Gmail ── forwarded, label "school" ────┤
Canvas feed ─── subscribed in Google Calendar ┼─► briefing / task capture ─► Todoist "Uni"
Google Calendar ─────── Calendar connector ───┘                         └─► Calendar "Assistant"
Scheduled task, weekdays 07:00 ─► workflows/briefing.md ─► result in the Scheduled page
```

## 2. Accounts and inboxes

| Inbox | Account (domain) | Reached by | Access | What matters | Skip |
|---|---|---|---|---|---|
| {{personal}} | {{@gmail.com}} | {{Gmail connector}} | read + drafts | {{…}} | {{newsletters, promotions}} |

**Important senders** (never miss): {{name · role · address/domain}}

**Search rules:** {{e.g. school mail = `label:school`; skip `category:promotions`}}

## 3. Calendars

| Calendar | Account | Contains | Assistant may |
|---|---|---|---|
| {{primary}} | {{@gmail.com}} | fixed events | read |
| {{Assistant}} | {{@gmail.com}} | everything the assistant creates | read + create + update its own |
| {{Canvas (subscribed)}} | | deadlines | read |

Events the assistant creates start with {{an emoji or tag, e.g. "◆ "}} and live in
**{{Assistant}}**, so they're easy to spot.

## 4. Tasks

- **Destination:** {{Todoist → project "Uni" (sections: …)}}
- **Title style:** {{"[Course] what to do"}} in {{language}}, in {{Name}}'s own words.
- **Due date when none given:** {{…}}
- **Sources of deadlines:** {{…}}
- **Duplicates:** search the destination for the same course + similar title before adding.

## 5. Work tracking
<!-- delete this section if not used -->
- **Tool:** {{Jira via Atlassian connector}} · site {{…}} · project {{KEY}}
- **Mine:** `{{assignee = currentUser() AND statusCategory != Done}}`
- **Stand-up:** {{when, where, format}}

## 6. Time rules

| Rule | Value |
|---|---|
| Busy anyway | {{…}} |
| **Protected (never plan into)** | {{…}} |
| No-go days | {{…}} |
| Quiet hours | {{…}} |
| Daily cap on planned work/study | {{…}} |
| Travel buffer | {{…}} |
| Briefing | {{weekdays 07:00}} |
| Weekly review | {{Sunday 18:00}} |

## 7. Modules

| Module | File | Runs | May write |
|---|---|---|---|
| {{Morning briefing}} | `workflows/briefing.md` | {{scheduled weekdays 07:00 + on demand}} | {{nothing}} |
| Help | `workflows/help.md` | on demand | nothing |
| Tune-up | `workflows/tune-up.md` | on demand, monthly | `SYSTEM.md` after OK |

## 8. Automations

| What | When | Mechanism | Where it lives | Limitation |
|---|---|---|---|---|
| {{Morning briefing}} | {{…}} | {{Desktop scheduled task "sam-briefing"}} | {{~/.claude/scheduled-tasks/sam-briefing/SKILL.md}} | {{only while the computer is awake and the app is open}} |

## 9. Files and secrets
<!-- Claude Code only; Claude app: write "No local files. Everything lives in this skill and the connected services." -->
- System folder: `{{~/assistant}}` (git, local; never pushed without asking)
- Skill source: `{{~/assistant/skill/<hub>}}`, linked from `~/.claude/skills/<hub>`
- Scripts: `{{~/assistant/scripts/}}`, run with `{{~/assistant/.venv/bin/python}}`
- State (handled message ids only): `{{~/assistant/state/}}` (gitignored)
- Secrets: `{{~/.config/<hub>/}}`, never committed, never printed. Contents: {{list of file
  names only, e.g. google-oauth-client.json, gmail-school-token.json, notify.json}}

## 10. Hard rules

{{Paste the ten rules from SAFETY.md here word for word, all ten, numbered 1–10 (the
packaging script checks each one is present). Claude app: add one line under rule 9, "On
this setup there are no local files: sign-ins live in the connectors."}}

### Personal rules

- {{protected time, no-go days, quiet hours, privacy limits, tone, people never to contact}}

## 11. Known limits and workarounds

- {{e.g. One Gmail connector account: school mail arrives by forwarding, about a minute late.}}
- {{e.g. The Microsoft 365 connector can't create drafts: replies to work mail are written in the chat.}}

## 12. Change log

| Date | Change |
|---|---|
| {{YYYY-MM-DD}} | Built with assistant-kit |
