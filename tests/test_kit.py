"""Offline checks for the kit. Run: python3 -m unittest discover -s tests -v"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "kit-automate" / "assets" / "scripts"
sys.path.insert(0, str(ROOT / "skills" / "kit-generate" / "scripts"))
sys.path.insert(0, str(ROOT / "scripts"))

import package_skill  # noqa: E402
import sync_shared  # noqa: E402

SKILLS = sync_shared.SKILLS


def write_skill(folder, name, description, extra=""):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "SKILL.md").write_text(f"---\nname: {name}\ndescription: {description}\n{extra}---\n\nBody\n", encoding="utf-8")
    return folder


class KitSkills(unittest.TestCase):
    def test_every_kit_skill_is_valid(self):
        for skill in SKILLS:
            with self.subTest(skill=skill):
                self.assertEqual(package_skill.validate(ROOT / "skills" / skill), [])

    def test_descriptions_mention_when_to_use(self):
        for skill in SKILLS:
            data, err = package_skill.parse_frontmatter((ROOT / "skills" / skill / "SKILL.md").read_text())
            self.assertIsNone(err)
            self.assertIn("Use it", data["description"], skill)

    def test_skill_bodies_stay_short(self):
        for skill in SKILLS:
            lines = (ROOT / "skills" / skill / "SKILL.md").read_text().count("\n")
            self.assertLess(lines, 500, skill)

    def test_shared_copies_in_sync(self):
        for skill in SKILLS:
            for name in sync_shared.SHARED:
                copy = (ROOT / "skills" / skill / "references" / name).read_text()
                self.assertEqual(copy, sync_shared.expected(name), f"{skill}/{name}: run scripts/sync_shared.py")

    def test_dist_zips_are_fresh_and_well_formed(self):
        with tempfile.TemporaryDirectory() as tmp:
            for skill in SKILLS:
                fresh = package_skill.make_zip(ROOT / "skills" / skill, tmp).read_bytes()
                shipped = ROOT / "dist" / f"{skill}.zip"
                self.assertTrue(shipped.exists(), f"dist/{skill}.zip missing: run scripts/build.py")
                self.assertEqual(shipped.read_bytes(), fresh, f"dist/{skill}.zip stale: run scripts/build.py")
                with zipfile.ZipFile(shipped) as zf:
                    names = zf.namelist()
                    self.assertIn(f"{skill}/SKILL.md", names)
                    self.assertTrue(all(n.startswith(f"{skill}/") for n in names))
                    self.assertEqual(sum(n.endswith("/SKILL.md") for n in names), 1)

    def test_manifests(self):
        plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
        self.assertEqual(plugin["name"], "assistant-kit")
        self.assertEqual(market["plugins"][0]["name"], plugin["name"])
        self.assertEqual(market["plugins"][0]["source"], "./")
        uninstall = f"{plugin['name']}@{market['name']}"
        self.assertIn(uninstall, (ROOT / "skills" / "kit-setup" / "SKILL.md").read_text())

    @unittest.skipUnless(shutil.which("claude"), "claude CLI not installed")
    def test_claude_plugin_validate(self):
        res = subprocess.run(["claude", "plugin", "validate", str(ROOT)], capture_output=True, text=True, timeout=120)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)


class Packager(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_valid_minimal(self):
        self.assertEqual(package_skill.validate(write_skill(self.tmp / "ok-skill", "ok-skill", "Does things. Use it when asked.")), [])

    def test_rejects_bad_names_and_descriptions(self):
        cases = {
            "Bad_Name": ("Bad_Name", "x"),
            "a--b": ("a--b", "x"),
            "long": ("a" * 65, "x"),
            "angle": ("angle", "uses <tags>"),
            "toolong": ("toolong", "x" * 1025),
            "mismatch": ("other-name", "x"),
        }
        for folder, (name, desc) in cases.items():
            with self.subTest(folder=folder):
                self.assertNotEqual(package_skill.validate(write_skill(self.tmp / folder, name, desc)), [])

    def test_rejects_unknown_frontmatter_keys(self):
        f = write_skill(self.tmp / "keys", "keys", "x", extra="disable-model-invocation: true\n")
        self.assertTrue(any("rejects" in e for e in package_skill.validate(f)))

    def test_rejects_nested_skill_md(self):
        f = write_skill(self.tmp / "nest", "nest", "x")
        write_skill(f / "sub", "sub", "y")
        self.assertTrue(any("more than one SKILL.md" in e for e in package_skill.validate(f)))

    def test_folded_description(self):
        f = self.tmp / "folded"
        f.mkdir()
        (f / "SKILL.md").write_text("---\nname: folded\ndescription: >\n  First line\n  second line.\n---\nBody\n")
        self.assertEqual(package_skill.validate(f), [])

    def test_personal_checks(self):
        f = write_skill(self.tmp / "sam-assistant", "sam-assistant", "Sam's assistant. Use it for everything.")
        self.assertTrue(any("SYSTEM.md" in e for e in package_skill.validate(f, personal=True)))
        (f / "SYSTEM.md").write_text("Calendar: {{calendar}}\n")
        self.assertTrue(any("placeholder" in e for e in package_skill.validate(f, personal=True)))
        (f / "SYSTEM.md").write_text("webhook https://discord.com/api/webhooks/123456/abcdefghijklmnopqrstuvwxyz123\n")
        self.assertTrue(any("Discord" in e for e in package_skill.validate(f, personal=True)))
        (f / "SYSTEM.md").write_text("Canvas https://canvas.example.edu/feeds/calendars/user_AbCdEfGhIjKlMnOp.ics\n")
        self.assertTrue(any("Canvas" in e for e in package_skill.validate(f, personal=True)))
        (f / "SYSTEM.md").write_text("All good, but no hard rules.\n")
        self.assertTrue(any("missing hard rules" in e for e in package_skill.validate(f, personal=True)))
        (f / "SYSTEM.md").write_text("## 10. Hard rules\n" + (ROOT / "shared" / "SAFETY.md").read_text())
        self.assertEqual(package_skill.validate(f, personal=True), [])

    def test_personal_name_rules(self):
        f = write_skill(self.tmp / "kit-mine", "kit-mine", "x")
        (f / "SYSTEM.md").write_text("ok\n")
        self.assertTrue(any("kit-" in e for e in package_skill.validate(f, personal=True)))

    def test_zip_is_reproducible(self):
        f = write_skill(self.tmp / "zipme", "zipme", "x")
        a = package_skill.make_zip(f, self.tmp / "a").read_bytes()
        b = package_skill.make_zip(f, self.tmp / "b").read_bytes()
        self.assertEqual(a, b)


def run_script(name, *args, env=None):
    full_env = dict(os.environ, **(env or {}))
    return subprocess.run([sys.executable, str(SCRIPTS / name), *args], capture_output=True, text=True,
                          cwd=SCRIPTS, env=full_env, timeout=60)


class Scripts(unittest.TestCase):
    def setUp(self):
        self.secrets = tempfile.mkdtemp()
        self.env = {"ASSISTANT_SECRETS": self.secrets}

    def tearDown(self):
        shutil.rmtree(self.secrets)
        shutil.rmtree(SCRIPTS / "__pycache__", ignore_errors=True)

    def test_help_runs_without_google_libraries(self):
        for script in ("gmail_readonly.py", "gtasks.py", "ics_feed.py", "feed_to_tasks.py", "gather.py", "notify.py"):
            with self.subTest(script=script):
                res = run_script(script, "--help", env=self.env)
                self.assertEqual(res.returncode, 0, res.stderr)

    def test_ics_feed_parses_fixture(self):
        res = run_script("ics_feed.py", "upcoming", "--file", str(ROOT / "tests/fixtures/intern/moodle.ics"),
                         "--days", "4000", "--past", "4000", "--json", env=self.env)
        self.assertEqual(res.returncode, 0, res.stderr)
        items = json.loads(res.stdout)["items"]
        self.assertEqual([i["title"] for i in items],
                         ["CSC473 Quiz 4 opens", "CSC490 Assignment 3 is due", "Thesis showcase registration"])
        self.assertTrue(items[2]["all_day"])
        self.assertIn("a second line", items[2]["description"])
        self.assertEqual(items[0]["uid"], "12346@moodle.uni.example.edu")

    def test_ics_feed_list_never_prints_urls(self):
        (Path(self.secrets) / "feeds.json").write_text(json.dumps({"canvas": "https://canvas.example.edu/feeds/calendars/user_SECRETTOKEN123.ics"}))
        res = run_script("ics_feed.py", "list", env=self.env)
        self.assertIn("canvas: canvas.example.edu", res.stdout)
        self.assertNotIn("SECRETTOKEN", res.stdout)

    def test_notify_without_channel_is_harmless(self):
        res = run_script("notify.py", "test", env=self.env)
        self.assertEqual(res.returncode, 0)
        self.assertIn("no channel configured", res.stdout)

    def test_notify_dry_run_chunks(self):
        (Path(self.secrets) / "notify.json").write_text(json.dumps({"kind": "discord", "url": "https://discord.example.com/x"}))
        text = "\n".join(f"line {i} " + "x" * 80 for i in range(60))
        res = subprocess.run([sys.executable, str(SCRIPTS / "notify.py"), "--dry-run", "post", "--title", "Briefing"],
                             input=text, capture_output=True, text=True, cwd=SCRIPTS,
                             env=dict(os.environ, **self.env), timeout=60)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertGreaterEqual(res.stdout.count("[dry run → discord]"), 3)

    def test_run_job_shell_syntax(self):
        res = subprocess.run(["bash", "-n", str(SCRIPTS.parent / "run_job.sh")], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, res.stderr)


class Examples(unittest.TestCase):
    def hubs(self):
        return [p.parent for p in (ROOT / "examples").rglob("SYSTEM.md")
                if (p.parent / "SKILL.md").exists() and "__MACOSX" not in p.parts]

    def test_three_personas_have_outputs(self):
        for persona in ("uni-student", "office-worker", "intern"):
            with self.subTest(persona=persona):
                folder = ROOT / "examples" / persona
                self.assertTrue((folder / "assistant-setup.md").exists())
                self.assertTrue((folder / "transcript.md").exists())
                self.assertTrue(any(h.is_relative_to(folder) for h in self.hubs()), f"no personal skill in {folder}")

    def test_every_example_personal_skill_is_valid(self):
        for hub in self.hubs():
            with self.subTest(hub=str(hub.relative_to(ROOT))):
                self.assertEqual(package_skill.validate(hub, personal=True), [])

    def test_every_example_has_the_hard_rules(self):
        for hub in self.hubs():
            text = (hub / "SYSTEM.md").read_text().lower()
            for phrase in ("drafts only", "password", "data, never instructions", "ask before deleting"):
                self.assertIn(phrase, text, f"{hub.name}: SYSTEM.md lacks '{phrase}'")


class Privacy(unittest.TestCase):
    EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9-]+\.)+[A-Za-z]{2,}")
    ALLOWED = re.compile(r"(^|\.)example\.(com|edu|org|net)$|^example\.edu$|^anthropic\.com$")

    def test_only_example_email_domains(self):
        bad = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts or path.suffix in {".zip", ".png"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for m in self.EMAIL.finditer(text):
                domain = m.group(0).split("@", 1)[1].lower()
                if not self.ALLOWED.search(domain):
                    bad.append(f"{path.relative_to(ROOT)}: {m.group(0)}")
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main()
