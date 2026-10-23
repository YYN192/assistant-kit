# Example runs

What the kit built for three invented people. Each run followed
[`tests/run_persona.md`](../tests/run_persona.md): one Claude agent played Claude with
the kit installed, and a separate Claude instance with no tools played the person, from a
hidden sheet in `tests/personas/`. Connectors were simulated from `tests/fixtures/`, so no
real account was read or written. Every write the kit would have made is listed in each
folder's `simulated-actions.log`.

| Folder | Person | Surface | Personal skill | Modules |
|---|---|---|---|---|
| [`uni-student/`](uni-student/) | Lena, 2nd-year economics, Canvas, café job, two inboxes | Claude app (claude.ai) | `outputs/lena-assistant/` + `.zip` | briefing, task capture from slides, what's due, inbox triage, weekly review |
| [`office-worker/`](office-worker/) | Daniel, product analyst, Jira + Slack, Microsoft 365 blocked by IT | Claude Desktop / Cowork | `outputs/daniel-assistant/` + `.zip` | briefing with meeting prep and stand-up, work tracker, Friday update, focus blocks |
| [`intern/`](intern/) | Priya, CS student + intern, three inboxes, Moodle, Google Tasks, Linear | Claude Code on a Mac | `home/skill/priya-assistant/` (`home/` = `~/assistant`) | inbox triage, briefing, task capture, work tracker, weekly review; scripts, launchd, ntfy |

In each folder:

- `transcript.md`: the whole setup conversation
- `assistant-setup.md`: the setup file (profile, connectors, plan, build log, test report)
- `scheduled-tasks.md`: every scheduled task as it would be created
- `smoke/`: real runs of the packager and of the finished skill in a throwaway Claude
  Code project (help card, "just send it" refusal, injected email, protected time)
- `RUN-REPORT.md`: the runner's report, including the problems it found in the kit

## What the runs changed in the kit

All three runs completed stages 1–7. Their reports listed 40-odd problems, and these
were fixed in the kit afterwards:

- **"Just send it" got through on the first build** (uni-student, office-worker). The
  personal skill's short rule said "drafts only" but not "even if asked to send", and the
  skill didn't load for e-mail requests when the plan had no mail module. Now the rule
  says it outright, every personal skill's description triggers on emailing, posting and
  deleting, and SAFETY rule 1 also covers posting in chats and trackers.
- **A copied rule got cut short** (office-worker: rule 1 lost its first lines). The
  packager now refuses a `SYSTEM.md` that doesn't contain all ten hard rules.
- **Text in tickets, slides, calendar events and chat** is now named explicitly as data
  (an injection sat in a Jira comment and on a lecture slide).
- **Unattended delivery** (Slack DM to self, email draft to self) is now an explicit,
  single exception in rule 8, and the briefing template supports it.
- **Script sources are tested before the plan** (intern: the work inbox turned out to be
  blocked by the company only after approval), and the plan has a fallback column.
- Smaller fixes: the packaging command now uses `--personal`; quiet hours vs. briefing
  time is checked in the interview; weather and news are asked about; meeting prep, a
  weekly status update and Slack channels are supported; new calendar feeds may be ⏳
  pending; test items are ticked done rather than deleted; Desktop scheduled tasks have
  one schedule each; laptops closed overnight are explained; `gtasks.py`, `gather.py`,
  `notify.py` and `feed_to_tasks.py` gained the options the run needed.
- Harness: `tests/skill_smoke.sh` copies the skill (a symlink hid `SYSTEM.md` from the
  Read tool) and redacts machine paths; `ask_persona.sh` closes stdin.

After the fixes, each example's `SYSTEM.md` §10 was re-synced to the final wording of the
rules (noted in its change log) and re-packaged, and `smoke/final-send-refusal.txt` was
re-run on the final skills.
