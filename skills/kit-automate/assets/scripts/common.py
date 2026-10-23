"""Shared helpers: config, secrets folder, state folder.

Config lives in <home>/assistant.json (no secrets in it). The secrets folder is outside
the repo: $ASSISTANT_SECRETS, else the "secrets_dir" in assistant.json, else
~/.config/<name>/. Files written there get mode 600.
"""

import json
import os
from pathlib import Path

HOME = Path(__file__).resolve().parent.parent  # <home>/scripts/common.py -> <home>


def load_config():
    path = HOME / "assistant.json"
    if not path.exists():
        return {"name": "my-assistant"}
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def now():
    """Current time in the configured time zone (assistant.json "timezone")."""
    import datetime as dt
    name = load_config().get("timezone")
    if name:
        try:
            from zoneinfo import ZoneInfo
            return dt.datetime.now(ZoneInfo(name))
        except Exception:
            pass
    return dt.datetime.now().astimezone()


def secrets_dir():
    cfg = load_config()
    raw = os.environ.get("ASSISTANT_SECRETS") or cfg.get("secrets_dir") or f"~/.config/{cfg.get('name', 'my-assistant')}"
    path = Path(raw).expanduser()
    path.mkdir(parents=True, exist_ok=True)
    try:
        path.chmod(0o700)
    except OSError:
        pass
    return path


def state_dir():
    path = HOME / "state"
    path.mkdir(exist_ok=True)
    return path


def read_secret_json(name, default=None):
    path = secrets_dir() / name
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def write_secret_json(name, data):
    path = secrets_dir() / name
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    tmp.chmod(0o600)
    tmp.replace(path)
    return path


def load_state(name, default=None):
    path = state_dir() / name
    if not path.exists():
        return default if default is not None else {}
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def save_state(name, data):
    path = state_dir() / name
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
