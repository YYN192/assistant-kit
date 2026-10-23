# Paste-in prompts

Four prompts take you from nothing to a working assistant. Paste them one at a time, in
the same chat if you can. If you start a new chat in the Claude app, attach your
`assistant-setup.md` file first (Claude gives it to you after each step). In Claude Code,
open Claude in your assistant folder (default `~/assistant`) and it finds the file itself.

Edit the parts in [square brackets] or delete them. Everything else can stay as it is.

---

## 1. Start: interview me

```
I want to build a personal assistant that's made for me, using the assistant-kit setup
skills. Start the setup: check where we're running, then interview me. Ask only a few
questions at a time and suggest sensible defaults.

A bit about me to begin with: [e.g. "I'm a second-year economics student with a part-time
job; homework from lectures keeps slipping and I have two inboxes"].

After the interview, work out which connectors I need, help me connect them one at a time
with a read-only test each, and then write a plan for me to approve. Don't build anything
yet.
```

What happens: about 10 minutes of questions, then connecting your apps (you sign in on
each service's own page; Claude never sees your passwords), then a one-page plan.

---

## 2. Approve the plan

Read the plan. Then either:

```
Approve. Build it.
```

or ask for changes first, for example:

```
Change the plan: [briefing at 07:30 instead of 07:00; no news; put tasks in my "Uni"
project; Saturdays are completely off-limits]. Show me only what changed, then I'll
approve.
```

Nothing is built until you approve.

---

## 3. Build and test

```
Build my assistant from the approved plan: write SYSTEM.md and my personal skill, set up
the automations, then test everything with me watching: a dry run of each workflow, one
test write per destination (ask me first), the safety checks, and one "run now" of each
scheduled task. Fix what fails and write the test report.

When everything passes, give me a short card of what I can say to my assistant, and then
remove the setup kit's own skills (ask me before removing anything; don't touch any other
skill I have).
```

In the Claude app you'll download one `.zip` (your personal skill) and upload it in
**Customize → Skills**; Claude walks you through it. In Claude Code it installs itself.

---

## 4. Monthly tune-up (optional)

Your assistant keeps a tune-up built in, so this works even after the kit is gone:

```
Tune-up. Check that all my connections and scheduled runs still work, then ask me what's
been useful, what I ignore, and what changed in my life. Propose changes to SYSTEM.md,
and apply them only after I say OK.
```

---

## Handy later

- "What can you do?": the help card.
- "Add another inbox to my assistant: [my work Outlook]": re-runs the connector, plan,
  build and test steps for just that addition (needs the kit still installed, or ask in
  a tune-up).
- "Pause my morning briefing until [date]": Claude shows you where to pause it.
