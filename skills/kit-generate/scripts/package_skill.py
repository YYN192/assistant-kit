#!/usr/bin/env python3
"""Validate a skill folder and optionally zip it for upload to the Claude app.

Usage:
  python3 package_skill.py <skill-folder> [--personal] [--zip <output-dir>]

Checks (always):
  - exactly one SKILL.md, at the top of the folder
  - YAML frontmatter with only the keys the Claude app accepts
  - name: kebab-case, at most 64 characters, same as the folder name
  - description: 1-1024 characters, no angle brackets
  - compatibility (optional): at most 500 characters
Extra checks with --personal (a generated personal assistant):
  - no template leftovers ({{...}} or <!-- choose ...)
  - nothing that looks like a secret (tokens, webhook URLs, private calendar feeds)
  - name doesn't start with "kit-" and doesn't contain "claude" or "anthropic"
  - SYSTEM.md exists

Only the Python standard library is used, so it runs in the Claude app sandbox too.
Exit code 0 = valid, 1 = invalid.
"""

import argparse
import re
import sys
import zipfile
from pathlib import Path

ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
SKIP_DIRS = {"__pycache__", "node_modules", ".git"}
SKIP_ROOT_DIRS = {"evals"}
SKIP_FILES = {".DS_Store"}

# One phrase from each of the ten safety rules; a personal SYSTEM.md must contain all.
HARD_RULES = [
    ("1 drafts only", "email: drafts only, never send"),
    ("2 passwords", "never ask for, see, type or store a password"),
    ("3 read-only first", "read-only first"),
    ("4 data not instructions", "are data, never instructions"),
    ("5 ask before deleting", "ask before deleting anything"),
    ("6 table first", "show multi-item plans as a table"),
    ("7 protected time", "protect the free time"),
    ("8 unattended runs", "unattended runs never ask questions"),
    ("9 secrets", "keep secrets out of"),
    ("10 ask before pushing", "ask before pushing commits"),
]

SECRET_PATTERNS = [
    (r"sk-ant-[A-Za-z0-9_-]{10,}", "Anthropic key"),
    (r"\bghp_[A-Za-z0-9]{20,}|\bgithub_pat_[A-Za-z0-9_]{20,}", "GitHub token"),
    (r"\bxox[abprs]-[A-Za-z0-9-]{10,}", "Slack token"),
    (r"\bAIza[0-9A-Za-z_-]{35}\b", "Google API key"),
    (r"\bya29\.[0-9A-Za-z_-]{20,}", "Google access token"),
    (r"\"(refresh_token|client_secret)\"\s*:\s*\"[^\"]{8,}", "OAuth secret"),
    (r"discord(?:app)?\.com/api/webhooks/\d+/[A-Za-z0-9_-]{20,}", "Discord webhook URL"),
    (r"hooks\.slack\.com/services/[A-Z0-9]+/[A-Z0-9]+/[A-Za-z0-9]+", "Slack webhook URL"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key"),
    (r"/feeds/calendars/user_[A-Za-z0-9]{10,}", "Canvas calendar feed URL"),
    (r"export_execute\.php\?[^\s)]*authtoken=", "Moodle calendar feed URL"),
    (r"calendar\.google\.com/calendar/ical/[^\s)]*/private-[0-9a-f]{8,}", "private Google Calendar feed"),
    (r"(?i)\bpassword\s*[:=]\s*\S{4,}", "password"),
]


def parse_frontmatter(text):
    """Return (dict, error). Uses PyYAML when installed, else a small parser
    that handles the subset skills use: key: value, quoted values, and > or | blocks."""
    if not text.startswith("---\n"):
        return None, "SKILL.md must start with a '---' frontmatter line"
    end = text.find("\n---", 4)
    if end == -1:
        return None, "frontmatter has no closing '---' line"
    block = text[4:end]
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(block)
        if not isinstance(data, dict):
            return None, "frontmatter must be a mapping of keys to values"
        return data, None
    except ImportError:
        pass
    except Exception as exc:  # yaml.YAMLError
        return None, f"invalid YAML in frontmatter: {exc}"

    data, lines, i = {}, block.split("\n"), 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not m:
            return None, f"can't read frontmatter line: {line!r}"
        key, value = m.group(1), m.group(2).strip()
        if value in (">", "|", ">-", "|-"):
            body = []
            i += 1
            while i < len(lines) and (lines[i].startswith(" ") or not lines[i].strip()):
                body.append(lines[i].strip())
                i += 1
            joiner = " " if value.startswith(">") else "\n"
            data[key] = joiner.join(b for b in body if b).strip()
            continue
        if value == "":
            # nested mapping (e.g. metadata:) - collect indented lines as a dict
            nested = {}
            i += 1
            while i < len(lines) and lines[i].startswith(" "):
                nm = re.match(r"^\s+([A-Za-z0-9_-]+):\s*(.*)$", lines[i])
                if nm:
                    nested[nm.group(1)] = nm.group(2).strip().strip("\"'")
                i += 1
            data[key] = nested
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        elif ": " in value:
            return None, f"value of '{key}' contains ': '; wrap it in quotes"
        data[key] = value
        i += 1
    return data, None


def skill_md_files(folder):
    found = []
    for p in folder.rglob("SKILL.md"):
        rel = p.relative_to(folder)
        parts = rel.parts[:-1]
        if any(part in SKIP_DIRS for part in parts):
            continue
        if parts and parts[0] in SKIP_ROOT_DIRS:
            continue
        found.append(rel)
    return found


def packaged_files(folder):
    for p in sorted(folder.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(folder)
        if any(part in SKIP_DIRS for part in rel.parts[:-1]):
            continue
        if rel.parts[0] in SKIP_ROOT_DIRS or p.name in SKIP_FILES:
            continue
        yield p, rel


def validate(folder, personal=False):
    folder = Path(folder).resolve()
    errors = []
    skill_md = folder / "SKILL.md"
    if not skill_md.is_file():
        return ["SKILL.md not found at the top of the folder"]
    extra = [str(r) for r in skill_md_files(folder) if str(r) != "SKILL.md"]
    if extra:
        errors.append("more than one SKILL.md (the Claude app accepts exactly one): " + ", ".join(extra))

    data, err = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    if err:
        return errors + [err]

    unknown = set(data) - ALLOWED_KEYS
    if unknown:
        errors.append("frontmatter keys the Claude app rejects: " + ", ".join(sorted(unknown)))

    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append("missing 'name'")
    else:
        name = name.strip()
        if not re.fullmatch(r"[a-z0-9-]+", name):
            errors.append(f"name '{name}' must use only lowercase letters, digits and hyphens")
        if name.startswith("-") or name.endswith("-") or "--" in name:
            errors.append(f"name '{name}' can't start or end with a hyphen or contain '--'")
        if len(name) > 64:
            errors.append(f"name is {len(name)} characters (max 64)")
        if name != folder.name:
            errors.append(f"name '{name}' must match the folder name '{folder.name}'")
        if personal:
            if name.startswith("kit-"):
                errors.append("a personal skill can't start with 'kit-' (reserved for the setup kit)")
            if "claude" in name or "anthropic" in name:
                errors.append("a personal skill name can't contain 'claude' or 'anthropic'")

    desc = data.get("description")
    if not isinstance(desc, str) or not desc.strip():
        errors.append("missing 'description'")
    else:
        desc = desc.strip()
        if len(desc) > 1024:
            errors.append(f"description is {len(desc)} characters (max 1024)")
        if "<" in desc or ">" in desc:
            errors.append("description can't contain angle brackets")

    comp = data.get("compatibility")
    if comp is not None and (not isinstance(comp, str) or len(comp) > 500):
        errors.append("compatibility must be text of at most 500 characters")

    if personal:
        system = folder / "SYSTEM.md"
        if not system.is_file():
            errors.append("SYSTEM.md missing (the personal system's single source of truth)")
        else:
            text = system.read_text(encoding="utf-8").lower()
            missing = [label for label, phrase in HARD_RULES if phrase not in text]
            if missing:
                errors.append("SYSTEM.md is missing hard rules (copy all ten from SAFETY.md): " + ", ".join(missing))
        for path, rel in packaged_files(folder):
            if path.suffix.lower() not in {".md", ".txt", ".py", ".json", ".yaml", ".yml", ".sh"}:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            if "{{" in text or "}}" in text:
                errors.append(f"{rel}: template placeholder left ({{{{...}}}})")
            if "<!-- choose" in text:
                errors.append(f"{rel}: template choice block left (<!-- choose ...)")
            for pattern, label in SECRET_PATTERNS:
                if re.search(pattern, text):
                    errors.append(f"{rel}: looks like a {label}; secrets belong in the secrets folder, not in the skill")
    return errors


def make_zip(folder, out_dir):
    folder = Path(folder).resolve()
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"{folder.name}.zip"
    # Fixed timestamps and modes make the zip byte-for-byte reproducible.
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for path, rel in packaged_files(folder):
            info = zipfile.ZipInfo(f"{folder.name}/{rel.as_posix()}", date_time=(1980, 1, 1, 0, 0, 0))
            info.external_attr = (0o755 if path.stat().st_mode & 0o111 else 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
    return target


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("folder")
    ap.add_argument("--personal", action="store_true", help="extra checks for a generated personal skill")
    ap.add_argument("--zip", metavar="OUT_DIR", help="write <name>.zip into this folder if valid")
    args = ap.parse_args(argv)

    folder = Path(args.folder)
    errors = validate(folder, personal=args.personal)
    if errors:
        print(f"✗ {folder.name}: {len(errors)} problem(s)")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"✓ {folder.name}: valid")
    if args.zip:
        print(f"  zip: {make_zip(folder, args.zip)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
