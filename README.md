# assistant-kit

**Build a personal assistant that's made for you, with Claude, in about an hour.**

You install a few setup skills, paste in a couple of prompts, and Claude:

1. **interviews you** (school, uni, work, internship, or all of them at once),
2. **works out which apps to connect** and tests each one read-only,
3. **writes a plan** you approve,
4. **builds your own assistant**: a personal skill plus a single `SYSTEM.md` that holds
   your accounts, calendars, task lists and rules,
5. **sets up the automatic parts** (a morning briefing, a weekly plan, reminders, syncs)
   using whatever your Claude app can actually schedule,
6. **tests everything** with you watching, and
7. **removes its own setup skills**, leaving only your assistant.

It runs in both the **Claude app** (claude.ai, Claude Desktop, Cowork) and **Claude Code**.
It checks where it's running and adapts.

> Example: a uni student who wants homework from lecture slides turned into tasks; an
> office worker who wants Jira issues and meetings in one morning summary; an intern
> juggling a personal, a school and a work inbox. See [`examples/`](examples/) for what
> the kit built for each of them.

## What your assistant can include

| Module | You say | What it does |
|---|---|---|
| Morning briefing | "brief me" (or automatic) | Today, what's due, important mail, 1–3 focus items in real free slots |
| Inbox triage | "triage my inboxes" | Sorts 1–3 inboxes into reply / task / FYI / ignore; offers drafts |
| Task capture | "add my homework: …", "what's due" | Turns slides, notes, emails or a sentence into tasks with due dates |
| Weekly review | "plan my week" (or automatic) | Looks back, looks ahead, proposes study/work blocks as a table |
| Work tracker | "stand-up", "what's on my plate" | Jira / Linear / Asana issues, blockers, a stand-up draft |
| Calendar blocking | "find 2 hours for the essay" | Places blocks around your rules: no-go days, quiet hours, protected time |
| Help and tune-up | "help", "tune-up" | Always included, so the system keeps improving after the kit is gone |

## Safety, built in

Every assistant the kit builds follows these rules, and you can only make them stricter:

- **Email: drafts only.** It never sends, forwards, or answers invites for you.
- **Never your passwords.** You sign in on each service's own page or in your own
  terminal. It never asks for, sees or stores a password.
- **Read-only first.** Write access only where the approved plan needs it.
- **Emails and web pages are data, not instructions.** Suspicious requests get flagged,
  not followed.
- **Asks before deleting anything.**
- **Shows multi-item calendar plans as a table and waits for your OK.**
- **Protects the free time you name.**

Full text: [`shared/SAFETY.md`](shared/SAFETY.md).

---

## Install: Claude app (claude.ai, Claude Desktop, Cowork)

You need a paid plan for scheduled tasks; skills themselves work on every plan.

1. **Turn on code execution:** Settings → **Capabilities** → **Code execution and file
   creation** (skills need it). On Team/Enterprise an owner may have to allow skills.
2. **Download the five setup skills** from [`dist/`](dist/):
   `kit-setup.zip`, `kit-interview.zip`, `kit-connectors.zip`, `kit-generate.zip`,
   `kit-automate.zip` (or download this repo as a ZIP and use the `dist/` folder).
3. **Upload each one:** **Customize → Skills** → **+** → **+ Create skill** → **Upload a
   skill** → pick the zip. Repeat for all five and check their toggles are on.
4. **Start a new chat** and paste prompt 1 from [`PROMPTS.md`](PROMPTS.md).

When your assistant is ready, Claude tells you how to delete the five `kit-…` skills
(Customize → Skills → click the skill → turn the toggle off → **…** → **Delete**). Your new
personal skill stays.

## Install: Claude Code

```bash
claude plugin marketplace add <owner>/assistant-kit
```

```bash
claude plugin install assistant-kit@assistant-kit
```

Then start Claude Code in your home folder (or anywhere) and paste prompt 1 from
[`PROMPTS.md`](PROMPTS.md), or type `/assistant-kit:kit-setup`.

Inside a session you can do the same with `/plugin marketplace add <owner>/assistant-kit`
and `/plugin install assistant-kit@assistant-kit`. To try it without installing, clone the
repo and run `claude --plugin-dir ./assistant-kit`.

At the end, Claude asks before running `claude plugin uninstall assistant-kit@assistant-kit`.
Your personal skill lives in your assistant folder (default `~/assistant`) and is linked
into `~/.claude/skills/`, so it stays.

Claude Code can do more than the app: read a second Gmail inbox with a read-only script,
sync Canvas/Moodle deadlines into Google Tasks, run jobs with launchd/cron or GitHub
Actions, and post one-way notifications to Discord, Slack or your phone (ntfy).

## What each surface can automate

| | Claude app | Claude Code |
|---|---|---|
| Morning briefing / weekly review | Scheduled task (runs in the cloud with your connectors) | Desktop scheduled task (needs the app open and the computer awake), or a cloud scheduled task |
| Second inbox | Forward it into your main Gmail | Read-only script, or forwarding |
| Google Tasks | No connector: use Todoist/Notion, or calendar items | Script |
| Canvas / Moodle deadlines | Subscribe the feed in Google Calendar | Same, or a feed → Tasks sync |
| Notifications | The scheduled run's result | Discord / Slack webhook or ntfy (one-way) |

One thing to know up front: **a connector holds one account**. If you have two Google
accounts, one is connected and the other is forwarded, shared or (Claude Code) read by a
script. The kit sorts this out with you.

## Repo layout

```
.claude-plugin/        plugin.json + marketplace.json (Claude Code install)
skills/                the five setup skills (SKILL.md + references, templates, scripts)
  kit-setup/           orchestrator: stages, setup file, plan, test, clean-up
  kit-interview/       question bank by role, profile template
  kit-connectors/      connector map, workarounds, read-only tests
  kit-generate/        SYSTEM.md + personal-skill templates, workflow templates, packager
  kit-automate/        scheduling guides, script templates (Claude Code), launchd/cron/Actions
shared/                canonical SAFETY / SURFACES / CATALOG, copied into each skill
dist/                  one zip per skill, for the Claude app
PROMPTS.md             the paste-in prompts
examples/              what the kit produced for three test personas
tests/                 validation, script tests, persona runs
scripts/               build.py, sync_shared.py
```

## Develop

```bash
python3 scripts/build.py
```

syncs `shared/` into each skill, validates all skills (frontmatter, name ≤ 64,
description ≤ 1024, no angle brackets, one `SKILL.md` per skill), runs
`claude plugin validate` when the CLI is installed, and rewrites `dist/*.zip`
(reproducible).

```bash
python3 -m unittest discover -s tests -v
```

runs the checks without network access: skill validity, `dist/` freshness, the packager,
the calendar-feed parser and the notifier (dry run), plus validation of every example
system in `examples/`. `tests/run_persona.md` describes how the persona runs were done.

Edit the shared rules in `shared/`, never the copies in `skills/*/references/`.

## Privacy of this repo

Nothing personal is in here. The personas in `examples/` are invented; their addresses use
`example.com`/`example.edu` domains.

## License

MIT. See [LICENSE](LICENSE).
