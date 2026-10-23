# How the kit works (for developers)

The [README](README.md) is written for people who don't code. This page is for anyone who
wants to change the kit, test it, or understand how it fits together.

## The flow

The kit is five skills. `kit-setup` drives the whole flow and calls the others:

| Stage | Skill | Output |
|---|---|---|
| 1. Interview | `kit-interview` | Profile section of `assistant-setup.md` |
| 2. Connectors | `kit-connectors` | Connector plan, connected and read-tested |
| 3–4. Plan and approval | `kit-setup` | Plan section, approved by the person |
| 5. Build | `kit-generate` | `SYSTEM.md` + one personal skill (the "hub") |
| 5. Automate | `kit-automate` | Scheduled tasks, scripts, notifications |
| 6. Test | `kit-setup` + `kit-generate` | Test report |
| 7. Clean up | `kit-setup` | Kit skills removed |

The kit works out which surface it's running on: the Claude app (claude.ai, Desktop,
Cowork) or Claude Code. See `shared/SURFACES.md`.

Each personal system is **one** skill: `SKILL.md` (router + short rules), `SYSTEM.md`
(the single source of truth) and one workflow file per module. Claude-app skills can't
read each other's files, and a scheduled task only has to name one skill.

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
dist/                  one zip per skill, for the Claude app (linked from the README)
PROMPTS.md             the paste-in prompts
examples/              outputs of three simulated persona runs
tests/                 unit tests, persona harness, fixtures
scripts/               build.py, sync_shared.py
```

## Editing

- Edit the shared rules in `shared/`, never the copies in `skills/*/references/`.
  `scripts/sync_shared.py` copies them into every skill (each skill must be
  self-contained).
- Keep `SKILL.md` frontmatter to `name`, `description` and `license`. The Claude app
  rejects other keys. Names are kebab-case, at most 64 characters, and match the folder.
  Descriptions are at most 1024 characters, with no angle brackets.
- Exactly one `SKILL.md` per skill. Templates use other file names (`hub-skill.md`).

## Build

```bash
python3 scripts/build.py
```

This syncs `shared/`, validates every skill, runs `claude plugin validate` if the CLI is
installed, and rewrites `dist/*.zip`. The zips are reproducible, and the tests fail if
they're stale, so commit them with your change.

## Test

```bash
python3 -m unittest discover -s tests -v
```

This runs offline, using only the Python standard library. It covers:

- skill validity and `dist/` freshness
- the packager, including its personal-system checks: all ten hard rules, no leftover
  placeholders, no secrets
- the calendar-feed parser and the notifier (dry run)
- validation of every example system
- a privacy check: only `example.*` email domains

## Persona runs

`tests/run_persona.md` describes how the examples were made. One Claude agent plays
Claude with the kit installed. A separate tool-less Claude instance
(`tests/ask_persona.sh`) plays the person, from a hidden sheet in `tests/personas/`.
Connectors are simulated from `tests/fixtures/`. `tests/skill_smoke.sh` loads a finished
personal skill into a throwaway Claude Code project and checks how it behaves, for
example that it refuses "just send it". These runs use the `claude` CLI and your Claude
usage.

## Privacy

Nothing personal goes into this repo. Use invented people and `example.*` domains.
Secrets (tokens, webhook URLs, private calendar feed URLs) never go into any file here.

## Install from a local checkout (Claude Code)

```bash
claude --plugin-dir ./assistant-kit
```
