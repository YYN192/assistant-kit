---
name: kit-generate
description: Builds a person's own assistant from the approved assistant-kit plan, as stage 5 of the setup. Writes SYSTEM.md (the single source of truth for their accounts, calendars, task lists, rules and modules) and one personal skill with a workflow per module, from templates for morning briefing, multi-inbox triage, homework or task capture, weekly review and planner, work tracker, and rule-based calendar blocking, then validates and packages it (a folder in Claude Code, a zip to upload in the Claude app). Use it when the plan is approved and it's time to build, when someone asks to regenerate, repackage or validate their personal assistant skill, or to add a module to an existing one.
license: MIT
---

# Assistant kit: generate the personal system

Input: the setup file with an **approved** Plan (Progress shows `approved: <date>`). If
there's no approval, stop and send the person back to stage 4; building without approval
breaks the kit's promise.

Output: one personal skill, the "hub", that contains everything:

```
<hub-name>/                     e.g. sam-assistant
├── SKILL.md                    router + hard rules (from templates/hub-skill.md)
├── SYSTEM.md                   single source of truth (from templates/SYSTEM.md)
└── workflows/
    ├── help.md                 always
    ├── tune-up.md              always
    └── <module>.md             one per module in the plan
```

Why one skill: claude.ai skills can't read each other's files, and a scheduled task only
has to name one skill. Every fact lives once, in `SYSTEM.md`; workflows refer to it instead
of repeating it.

## Steps

1. **Read** the whole setup file, `references/SAFETY.md`, and `references/SURFACES.md`.
2. **Choose the hub name** from the plan. Rules: lowercase letters, digits and hyphens,
   at most 64 characters, no leading/trailing or double hyphen, not starting with `kit-`,
   and not "claude" or "anthropic" in it.
3. **Write `SYSTEM.md`** from `templates/SYSTEM.md`. Fill every placeholder from the
   profile, connectors and plan. Copy the ten safety rules exactly. Personal rules go
   under them. Write facts, not intentions: real calendar names, real task list names,
   real sender domains.
4. **Write each workflow** from `templates/workflows/<module>.md`. Templates contain
   `{{…}}` placeholders and some `<!-- choose: … -->` blocks: keep the branch that fits the
   surface and the person, delete the others. Keep each workflow under ~150 lines.
5. **Write the hub `SKILL.md`** from `templates/hub-skill.md`. The description decides
   when the skill triggers, so list the person's own phrases ("add my homework", "what's
   due", "brief me", "triage my inboxes", their language too). **Keep the sentence about
   emailing, posting and deleting even if the plan has no mail module**: in testing, a hub
   without it didn't load for "email my manager, just send it", and the bare model offered
   to send. Keep it under 1024 characters and without angle brackets.
6. **Check for leftovers**: no `{{`, no `<!-- choose`, no secrets, no other person's data.
   The packaging script checks this too.
7. **Validate and package** with `scripts/package_skill.py` (Python 3, no packages
   needed):

   ```bash
   python3 <this skill's folder>/scripts/package_skill.py <path-to-hub-folder> --personal --zip <output-dir>
   ```

   (`--personal` turns on the leftover, secret, name and SYSTEM.md checks; always use it
   for a personal skill.)

   It validates the frontmatter (name ≤ 64, kebab-case; description ≤ 1024, no angle
   brackets; only allowed keys), refuses leftover placeholders and secret-looking strings,
   and writes `<hub-name>.zip` with the folder at the zip's top level, the layout the
   Claude app expects. Fix every error it prints and run it again.

8. **Install**, depending on the surface:
   - **Claude Code:** the hub lives in the system folder at `<home>/skill/<hub-name>/`
     (versioned with git). Link it into the personal skills folder so there's still only
     one copy:
     `mkdir -p ~/.claude/skills && ln -s <home>/skill/<hub-name> ~/.claude/skills/<hub-name>`
     (on Windows, copy instead and note in `SYSTEM.md` that edits go to the system folder
     and are re-copied). New skills load in new sessions; ask the person to start a new
     session (or run `/reload-plugins` if offered) before testing.
   - **Claude app:** put the zip in the outputs folder and tell the person: "Download
     `<hub-name>.zip`, open **Customize → Skills**, click **+**, then **+ Create skill**,
     choose **Upload a skill**, pick the zip, and make sure its toggle is on." Then ask
     them to start a new chat for testing, since skills load at the start of a chat.
9. **Log** each file in the Build log of the setup file.

## Fixing during setup, or changing a module later

Edit `SYSTEM.md` and the workflow file, bump `version` in `SYSTEM.md`'s header (every
re-package, including fixes made during stage 6), add a change-log line, and re-run the
packaging script. Claude app: give the person the new zip; uploading a skill with the same
name replaces it (or delete the old one first if the app refuses), then they start a new
chat, because skills load at the start of a chat. Claude Code: nothing to reinstall (the
skill is linked); start a new session to reload it.

## Quality bar for generated workflows

- Each workflow starts with **when it runs** (on demand, scheduled, or both) and **what
  it may write**. Unattended runs never ask questions (safety rule 8).
- Reads are bounded: time windows (`newer_than:1d`), max counts, the specific calendars
  and projects named in `SYSTEM.md`. That keeps runs fast and cheap.
- Outputs have a fixed, short format the person approved (briefing ≤ 30 lines).
- Every write path names its destination exactly as in `SYSTEM.md`.
- Language: the person's choice for output; keep their own words in task titles.
