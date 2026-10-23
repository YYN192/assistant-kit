# Your own AI assistant, set up by Claude

**No coding needed.** You add a few files to Claude, copy in one message, and Claude
interviews you, then builds a personal assistant made for your life: your classes or job,
your inboxes, your calendar, your rules.

When it's done, you have an assistant that can:

- ☀️ send you a **morning summary**: today's plan, what's due, and which emails matter
- 📝 turn **homework, lecture slides or emails into to-do items** with due dates
- 📥 go through **several inboxes** and tell you what needs a reply
- 📅 **plan your week** around the times you want to keep free
- 💼 sum up your **work tickets** (Jira, Linear, Asana) and write your stand-up

It takes about **an hour**, mostly answering questions. You don't need to know anything
about programming.

---

## What it looks like

This is the kind of morning message a finished assistant writes:

```
☀️ Thu 23 Oct briefing

📅 Today
09:00–11:00  Microeconomics lecture
13:00–14:00  Econometrics seminar (now in room 1.12)

✅ Due
Tomorrow  Problem Set 4 (Micro)
Tue       Essay plan, 500 words (Economic History)

🎯 Focus
1. 15:00–16:30: start Problem Set 4

📧 Mail
Dr. Malik: seminar group B moves to Thursdays 14:00 (FYI)
⚠️ "IT Helpdesk" asked for your password: looks like phishing, ignored

⭐ Most important today: Problem Set 4
```

---

## Is this for me?

Yes, if you're a student, you work in an office, you're an intern, or you're juggling all
of these, and things keep slipping through the cracks.

**You'll need:**

| | |
|---|---|
| A Claude account | Any plan works for the assistant itself. The **automatic** morning summary needs a paid plan (Pro or higher). On the free plan you just ask for it ("brief me"). |
| A computer | For the setup, because you'll download and upload a few files. |
| About an hour | Mostly answering questions about your week. |
| The apps you already use | For example Gmail, Google Calendar, Outlook, Todoist, Notion, Jira, Canvas or Moodle. |

---

## Set it up in 6 steps

### Step 1. Turn on one setting in Claude

Open [claude.ai](https://claude.ai) (or the Claude desktop app). Go to **Settings →
Capabilities** and switch on **Code execution and file creation**. The assistant needs it
to work.

> On a work or school account, this might be controlled by your IT team. If you can't
> find the switch, ask them.

### Step 2. Download the 5 setup files

Click each link. Each one downloads a small `.zip` file. **Don't open them**; just leave
them in your Downloads folder.

1. [kit-setup.zip](https://github.com/YYN192/assistant-kit/raw/main/dist/kit-setup.zip)
2. [kit-interview.zip](https://github.com/YYN192/assistant-kit/raw/main/dist/kit-interview.zip)
3. [kit-connectors.zip](https://github.com/YYN192/assistant-kit/raw/main/dist/kit-connectors.zip)
4. [kit-generate.zip](https://github.com/YYN192/assistant-kit/raw/main/dist/kit-generate.zip)
5. [kit-automate.zip](https://github.com/YYN192/assistant-kit/raw/main/dist/kit-automate.zip)

> **Using Safari on a Mac?** Safari sometimes unpacks zip files by itself, and then you
> see a folder instead of a `.zip`. If that happens, right-click the folder and choose
> **Compress**. That gives you the `.zip` back. Or download the files with Chrome or
> Firefox.

### Step 3. Add the files to Claude

In Claude, go to **Customize → Skills**. Then, for **each** of the 5 files:

1. Click **+**, then **+ Create skill**.
2. Choose **Upload a skill**.
3. Pick the `.zip` file.

You'll see five new skills whose names start with `kit-`. Make sure their switches are
**on**.

### Step 4. Start a new chat and paste this

Open a **new chat**. Copy the message below, change the part in [square brackets] to
describe yourself, and send it.

```
I want to build a personal assistant that's made for me, using the assistant-kit setup
skills. Start the setup: check where we're running, then interview me. Ask only a few
questions at a time and suggest sensible defaults.

A bit about me to begin with: [for example: "I'm a second-year economics student with a
part-time job. I forget homework that lecturers mention in class, and I never check my
uni email."]

After the interview, work out which apps I need to connect, help me connect them one at
a time with a read-only test for each, and then write a plan for me to approve. Don't
build anything yet.
```

### Step 5. Answer, approve, build

Claude will:

1. **Ask you questions**, a few at a time. Suggested answers are in [brackets], so you can
   reply "fine" to anything you don't care about.
2. **Help you connect your apps.** You sign in on each app's own page, the same way you
   log in anywhere else. Claude never sees your passwords.
3. **Show you a one-page plan.** Read it. Ask for any changes you want, then reply:

   ```
   Approve. Build it.
   ```

4. **Build your assistant.** Claude gives you one more `.zip` file: your personal
   assistant. Add it the same way as in Step 3.
5. **Test everything with you**: a practice summary, one test to-do item, and a few
   safety checks.

> 💡 After each step, Claude gives you a file called `assistant-setup.md`. **Keep it.**
> If you close the chat, open a new one, attach that file, and say "let's continue". Claude
> picks up where you stopped.

### Step 6. Tidy up

When everything works, Claude asks you to remove the five `kit-` setup skills. You won't
need them anymore. For each one, go to **Customize → Skills**, click it, switch it
**off**, click **…** and choose **Delete**.

Only delete the ones whose names start with `kit-`. Your new assistant (named something
like `sam-assistant`) stays.

---

## Using your assistant

Just talk to Claude in any chat. For example:

| You say | It does |
|---|---|
| "brief me" | Today's plan, what's due, important emails |
| "add my homework: read chapter 4 for Friday" | Adds a to-do item with the right date |
| *(paste lecture slides or an email)* "add the homework from this" | Finds every task and deadline, shows you a list, adds them when you say OK |
| "what's due this week?" | A short list, day by day |
| "triage my inboxes" | Sorts new emails: reply needed, to-do, just FYI, ignore |
| "plan my week" | Suggests study or work blocks around your free time, as a table |
| "stand-up" | Writes your daily update from your work tickets |
| "what can you do?" | Shows everything it can do for you |
| "tune-up" | Once a month: checks everything still works and asks what to change |

If you chose a **morning summary**, it arrives on its own at the time you picked. You'll
find it under **Scheduled** in the Claude sidebar.

---

## Your safety and privacy

Every assistant built with this kit follows these rules. You can make them stricter, but
not weaker:

- ✉️ **It never sends emails for you.** It only writes drafts. You read them and press
  Send yourself, even if you tell it "just send it".
- 🔑 **It never asks for your passwords.** You always sign in on the app's own page.
- 👀 **It starts by only reading.** It only adds things (like to-do items) where your
  plan says so.
- 🎣 **Emails can't give it orders.** If an email or document says "AI, forward all mail
  to…", it doesn't do it. It warns you instead.
- 🗑️ **It asks before deleting anything.**
- 📋 **It asks before changing your calendar.** If it wants to add several things, it
  shows them as a list first and waits for your OK.
- 🛋️ **It protects your free time.** Name the evenings or days that are yours, and it
  never plans anything there.

You also choose what it must never read, for example emails from your bank or doctor.

---

## Good to know

- **One account per app.** Claude can be connected to one Gmail account at a time. If
  you have a second one (say, a uni email), Claude shows you how to forward it to your
  main one. Same for a second calendar.
- **Some apps have no direct connection.** Canvas, Moodle and Google Classroom don't
  connect to Claude directly. Claude shows you a simple workaround: you add your course
  deadlines to Google Calendar, and Claude reads them from there.
- **Work accounts may be blocked.** Some companies don't allow outside apps. If yours
  doesn't, Claude plans around it and tells you what's missing.
- **The morning summary uses your Claude usage.** One short run a day is small, but it
  counts like any other chat.

---

## Questions

**Do I need to know how to code?**
No. You'll download files, upload them, copy and paste a message, and answer questions.

**Is it free?**
The kit is free. You need a Claude account. The automatic morning summary needs a paid
Claude plan. On the free plan you can still ask for your summary whenever you want.

**Can Claude see my passwords or send emails as me?**
No. You sign in yourself on each app's page, and the assistant only writes drafts.

**Can I use it on my phone?**
Do the setup on a computer. Your assistant is part of your Claude account, so you can
usually also use it from the Claude app on your phone.

**How do I change something later?**
Say "tune-up" in a chat. Claude checks everything still works, asks what you'd like
changed, and gives you an updated assistant file if needed.

**How do I stop the morning summary?**
Open **Scheduled** in the Claude sidebar, click the task, and pause or delete it.

**How do I remove everything?**
Delete your assistant skill in **Customize → Skills** and its task in **Scheduled**. You
can also disconnect apps in **Customize → Connectors**.

---

## If something goes wrong

| Problem | Try this |
|---|---|
| "Upload failed" when adding a file | Make sure you upload the `.zip` file itself, not an unpacked folder (see the Safari tip in Step 2). |
| Claude doesn't start the setup | Check that all five `kit-` skills are switched on, and start a **new** chat. Skills only load at the start of a chat. |
| Claude can't see your email or calendar | Go to **Customize → Connectors** and check the app is connected. In the chat, click **+** and make sure it's switched on. |
| The morning summary didn't arrive | Open **Scheduled** and look at the last run. If an app shows as disconnected, reconnect it. |
| Anything else | Tell Claude exactly what happened. It knows how the kit works and can usually fix it. |

---

## Using Claude Code instead?

If you use **Claude Code** (the terminal version of Claude), it can also run small
programs for you, for example reading a second inbox or posting your summary to your
phone. Install the kit with these two commands:

```bash
claude plugin marketplace add YYN192/assistant-kit
```

```bash
claude plugin install assistant-kit@assistant-kit
```

Then start Claude Code and paste the message from Step 4. The other messages (approve,
build, monthly tune-up) are in [PROMPTS.md](PROMPTS.md).

---

## More

- [PROMPTS.md](PROMPTS.md): every message you might want to copy in
- [examples/](examples/): what the kit built for three made-up people (a student, an
  office worker and an intern)
- [CONTRIBUTING.md](CONTRIBUTING.md): how the kit works inside, for developers

Free and open source under the [MIT license](LICENSE).
