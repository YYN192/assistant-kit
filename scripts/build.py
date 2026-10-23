#!/usr/bin/env python3
"""Build the kit: sync shared files, validate every skill, validate the plugin, and write
one zip per skill into dist/ for upload to the Claude app.

  python3 scripts/build.py            build
  python3 scripts/build.py --check    fail if dist/ or shared copies are out of date

Standard library only. `claude plugin validate` runs too when the claude CLI is installed.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "kit-generate" / "scripts"))
sys.path.insert(0, str(ROOT / "scripts"))

import package_skill  # noqa: E402
import sync_shared  # noqa: E402

DIST = ROOT / "dist"


def main():
    check = "--check" in sys.argv
    ok = True

    sys.argv = [sys.argv[0]] + (["--check"] if check else [])
    if sync_shared.main() != 0:
        ok = False

    for skill in sync_shared.SKILLS:
        errors = package_skill.validate(ROOT / "skills" / skill)
        if errors:
            ok = False
            print(f"✗ {skill}")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"✓ {skill}: valid")

    if shutil.which("claude"):
        res = subprocess.run(["claude", "plugin", "validate", str(ROOT)], capture_output=True, text=True)
        verdict = [line for line in res.stdout.splitlines() if "Validation" in line]
        print("✓ " if res.returncode == 0 else "✗ ", "claude plugin validate:", verdict[-1] if verdict else res.stdout.strip()[-200:])
        if res.returncode != 0:
            ok = False
            print(res.stdout + res.stderr)
    else:
        print("· claude CLI not found; skipped `claude plugin validate`")

    if not ok:
        print("Build failed.")
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        for skill in sync_shared.SKILLS:
            package_skill.make_zip(ROOT / "skills" / skill, tmp)
        fresh = {p.name: p.read_bytes() for p in Path(tmp).glob("*.zip")}
    if check:
        stale = [n for n, data in fresh.items() if not (DIST / n).exists() or (DIST / n).read_bytes() != data]
        if stale:
            print("dist/ is out of date: " + ", ".join(stale) + " (run scripts/build.py)")
            return 1
        print("dist/ up to date")
        return 0
    DIST.mkdir(exist_ok=True)
    for old in DIST.glob("*.zip"):
        old.unlink()
    for name, data in sorted(fresh.items()):
        (DIST / name).write_bytes(data)
        print(f"  dist/{name}  ({len(data) // 1024} KB)")
    print("Build OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
