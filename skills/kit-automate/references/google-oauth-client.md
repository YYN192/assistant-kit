# One-time: a Google OAuth client for the scripts (Claude Code only)

Only needed for `gmail_readonly.py`, `gtasks.py` and `feed_to_tasks.py`. About ten
minutes. The person clicks through Google Cloud Console in their own browser; you guide
and never handle the downloaded secret's contents.

1. Open https://console.cloud.google.com/ with the **home** Google account (or the account
   that owns the data; any account works for the client itself) and create a project,
   e.g. "My Assistant".
2. **APIs & Services → Library**: enable **Gmail API** (for the read-only inbox) and/or
   **Google Tasks API**.
3. **Google Auth Platform → Branding** (older consoles: OAuth consent screen): app name
   "My Assistant", their own email as support and developer contact. Don't upload a logo
   (that triggers Google's verification).
4. **Audience**: User type **External**. Either keep it in **Testing** and add every
   Google account the scripts will sign in as under **Test users**, or click **Publish
   app**. In Testing mode, sign-ins expire after 7 days; published but unverified apps
   keep working, and every sign-in shows "Google hasn't verified this app": click
   **Advanced → Go to My Assistant (unsafe)**. It's their own app, so that's expected.
   A Google Workspace school or company may block unverified apps entirely; then use
   forwarding instead.
5. **Clients → Create client → Desktop app**, name "assistant scripts", **Create**,
   **Download JSON**.
6. In their own terminal they move it into the secrets folder:
   `mkdir -p ~/.config/<hub> && mv ~/Downloads/client_secret_*.json ~/.config/<hub>/google-oauth-client.json && chmod 600 ~/.config/<hub>/google-oauth-client.json`
7. They run the sign-in in their own terminal, for example
   `<home>/.venv/bin/python <home>/scripts/gmail_readonly.py auth --account school --expect-domain uni.edu`.
   A browser opens; they pick the right account and allow access. You then run
   `gmail_readonly.py check --account school` to confirm the account domain.

Scopes used: `gmail.readonly` (cannot send, draft, label or delete) and `tasks`. Nothing
else.
