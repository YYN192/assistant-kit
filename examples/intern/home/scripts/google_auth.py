"""Google OAuth for the assistant's scripts.

The person runs `<script> auth` in their own terminal. A browser opens, they sign in on
Google's page, and only the resulting token is saved (mode 600) in the secrets folder.
No password ever passes through this code. Tokens are never printed.
"""

import sys

from common import read_secret_json, secrets_dir, write_secret_json

CLIENT_FILE = "google-oauth-client.json"


def _libs():
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError:
        sys.exit("Google libraries missing. Run: <home>/.venv/bin/pip install -r <home>/requirements.txt")
    return Request, Credentials, InstalledAppFlow, build


def sign_in(token_name, scopes):
    """Interactive browser sign-in. Saves the token; returns credentials."""
    Request, Credentials, InstalledAppFlow, _ = _libs()
    client = secrets_dir() / CLIENT_FILE
    if not client.exists():
        sys.exit(f"No OAuth client at {client}. See kit-automate references/google-oauth-client.md.")
    flow = InstalledAppFlow.from_client_secrets_file(str(client), scopes)
    creds = flow.run_local_server(port=0, prompt="consent", open_browser=True)
    write_secret_json(token_name, _to_dict(creds))
    return creds


def load(token_name, scopes):
    """Load saved credentials, refreshing when needed. Exits with a hint if not signed in."""
    Request, Credentials, _, _ = _libs()
    data = read_secret_json(token_name)
    if not data:
        sys.exit("Not signed in. Run this script's `auth` command in your own terminal.")
    creds = Credentials.from_authorized_user_info(data, scopes)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            write_secret_json(token_name, _to_dict(creds))
        else:
            sys.exit("Sign-in expired. Run this script's `auth` command in your own terminal.")
    return creds


def service(name, version, creds):
    _, _, _, build = _libs()
    return build(name, version, credentials=creds, cache_discovery=False)


def _to_dict(creds):
    import json
    return json.loads(creds.to_json())
