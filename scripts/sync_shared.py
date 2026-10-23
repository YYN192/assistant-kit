#!/usr/bin/env python3
"""Copy the canonical files in shared/ into every kit skill's references/ folder.

Each skill has to be self-contained (a claude.ai skill can't read another skill's
files), so the shared safety rules, surface facts and catalog are copied, not linked.
Edit shared/*.md, then run this. `--check` only reports drift (used by the tests).
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = ["SAFETY.md", "SURFACES.md", "CATALOG.md"]
SKILLS = ["kit-setup", "kit-interview", "kit-connectors", "kit-generate", "kit-automate"]
BANNER = "<!-- Copied from shared/{name} by scripts/sync_shared.py. Edit the original, not this copy. -->\n\n"


def expected(name):
    return BANNER.format(name=name) + (ROOT / "shared" / name).read_text(encoding="utf-8")


def main():
    check = "--check" in sys.argv
    drift = []
    for skill in SKILLS:
        ref = ROOT / "skills" / skill / "references"
        ref.mkdir(parents=True, exist_ok=True)
        for name in SHARED:
            target = ref / name
            want = expected(name)
            if not target.exists() or target.read_text(encoding="utf-8") != want:
                drift.append(str(target.relative_to(ROOT)))
                if not check:
                    target.write_text(want, encoding="utf-8")
    if check and drift:
        print("Out of date (run scripts/sync_shared.py):\n  " + "\n  ".join(drift))
        return 1
    print("shared files " + ("in sync" if check else f"synced ({len(drift)} updated)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
