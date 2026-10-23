# Read-only tests

One small read per connector, enough to prove it's the right account and it works. Show
the person only counts, dates, sender names and subjects, never message bodies. Tool names
differ between versions; use whichever read tool the connector offers.

| Source | Test | Pass looks like |
|---|---|---|
| Gmail | Search `newer_than:2d`, max 3 results. | "3 messages since yesterday; newest from <sender>, subject <…>." The sender domain matches the account they meant. Skip private senders/labels from the profile: "1 private, skipped". |
| Gmail, forwarded inbox | Search `label:<label> newer_than:7d` (or `deliveredto:<address>`), max 3. | At least one forwarded message. If none, ask the person to send a test mail to the other address themselves, then search again (you never send mail). |
| Google Calendar | List calendars; list events for today and tomorrow in the fixed-events calendar. | Calendar names match what they described; today's first event is right. |
| Shared / subscribed calendar | List calendars and find it; list the next 5 events. | Deadlines from the platform appear. A feed added minutes ago may still be empty (Google refreshes URL feeds every few hours): mark ⏳ and re-test in stage 6. |
| Microsoft 365 | Search mail from the last 2 days (max 3); search calendar for today. | As Gmail. If an "admin approval required" error appears, it's an organisation block: record it. |
| Todoist | List projects; list today's and overdue tasks. | The project they named exists. |
| Notion | Search for the task database by name; fetch its properties. | Properties for title, due date and status are identified. |
| Asana | List projects / my tasks (first 5). | The project they named exists. |
| Linear | List issues assigned to me (first 5). | Matches what they see in Linear. |
| Atlassian (Jira) | Get accessible resources (sites); search issues `assignee = currentUser() AND statusCategory != Done` (first 5). | Their site and issues appear. |
| Slack | Search the channel they named for the last day (first 3). | |
| Google Drive | Search for a file they name. | |
| Script (Claude Code) | Run the script's `check` command (`gmail_readonly.py check --account X`, `gtasks.py check`, `ics_feed.py list`). | Mail: the account domain; Tasks: the list names; feeds: names and hosts. It must not print tokens or feed URLs. |

## Afterwards

- Write the result line into the Connectors table.
- Don't create, change or delete anything during these tests. Write tests happen in
  stage 6, after the plan is approved, with the person's OK.
