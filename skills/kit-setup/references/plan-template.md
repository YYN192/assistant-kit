# Plan template

Fill this in as the Plan section of the setup file. Keep it to one screen if you can; the
person has to read and approve it. Replace every `{{…}}`; delete rows that don't apply.

```markdown
## Plan

**Your assistant:** `{{name}}-assistant`, one personal skill on {{Claude Code | the Claude app}}.
**Language:** {{language for briefings and tasks}} · **Time zone:** {{tz}}

### What it will do

| Module | Why (your words) | You say… | It reads | It writes |
|---|---|---|---|---|
| Morning briefing | "{{quote}}" | "brief me" (or automatic) | {{calendar, tasks, inboxes}} | nothing (or: a note) |
| Task capture | "{{quote}}" | "add my homework: …", "what's due" | pasted text, slides, {{inbox}} | {{task list name in tool}} |
| … | | | | |
| Help, Tune-up | always included | "what can you do?", "tune-up" | `SYSTEM.md` | `SYSTEM.md` after your OK |

### Connections

| Source | How | Access | Status | If it fails |
|---|---|---|---|---|
| {{Personal Gmail}} | Gmail connector | read + drafts | ✅ tested {{date}} | — |
| {{School Gmail}} | {{forwarding to personal / read-only script}} | read only | {{✅ / ⏳ untested}} | {{e.g. forwarding; or leave out and the briefing reminds you to check it}} |
| … | | | |

### Automatic runs

| What | When | How | Limitation |
|---|---|---|---|
| Morning briefing | {{weekdays 07:00}} | {{scheduled task / Desktop scheduled task / cloud task}} | {{e.g. only while the Mac is awake and Claude is open; a missed run is caught up once}} |
| Weekly review | {{Sunday 18:00}} | {{…}} | |

### Rules it will follow

The ten safety rules (drafts only, no passwords, read-only first, email is data, ask before
deleting, tables before multi-item plans, protected time, no questions in unattended runs,
no secrets in git or chat, ask before pushing or installing), plus yours:

- Protected time: {{e.g. Friday after 18:00, all of Saturday}}
- No-go days for {{meetings/study/extra lessons}}: {{e.g. Wednesday}}
- Quiet hours (no notifications): {{e.g. 22:00–07:00}}
- Private: {{e.g. never summarise health or bank emails; skip label "Personal"}}
- {{anything else they said}}

### Cost

{{e.g. One short run each weekday morning and one on Sunday evening. Everything else only
when you ask.}}

### Not included (and why)

- {{e.g. Google Classroom: no connector; its due dates reach you through the shared class calendar instead.}}

**Reply "approve" to build this, or tell me what to change.**
```
