"""Tests for installing the /ref-bio OpenCode skill bundle."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "install_opencode_skill.py"


def read_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return None
    return yaml.safe_load(parts[1])


class TestOpenCodeSkillInstall(unittest.TestCase):
    """Verify deterministic local installation behavior."""

    def run_install(self, target, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--target", str(target), *args],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )

    def test_dry_run_does_not_write_destination(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir)
            result = self.run_install(target, "--dry-run")
            self.assertEqual(
                result.returncode, 0,
                f"Dry run failed:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertFalse(
                (target / ".opencode" / "skills" / "ref-bio").exists(),
                "Dry run should not create installation destination",
            )

    def test_install_creates_skill_bundle(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir)
            result = self.run_install(target)
            self.assertEqual(
                result.returncode, 0,
                f"Install failed:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            dest = target / ".opencode" / "skills" / "ref-bio"
            self.assertTrue((dest / "SKILL.md").is_file())
            self.assertTrue((dest / "reference-pack" / "references.link-only.yaml").is_file())
            frontmatter = read_frontmatter(dest / "SKILL.md")
            self.assertIsNotNone(frontmatter, "Installed SKILL.md must start with frontmatter")
            self.assertEqual(frontmatter.get("name"), "ref-bio")
            self.assertIsInstance(frontmatter.get("description"), str)
            self.assertGreater(len(frontmatter["description"]), 0)
            self.assertIn("/ref-bio", result.stdout)

    def test_install_refuses_overwrite_without_force(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir)
            first = self.run_install(target)
            self.assertEqual(first.returncode, 0, first.stderr)
            second = self.run_install(target)
            self.assertNotEqual(second.returncode, 0, "Install should refuse overwrite")
            self.assertIn("Destination already exists", second.stderr)

    def test_install_overwrites_with_force(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir)
            first = self.run_install(target)
            self.assertEqual(first.returncode, 0, first.stderr)
            marker = target / ".opencode" / "skills" / "ref-bio" / "marker.txt"
            marker.write_text("remove me\n", encoding="utf-8")
            forced = self.run_install(target, "--force")
            self.assertEqual(
                forced.returncode, 0,
                f"Forced install failed:\nstdout:\n{forced.stdout}\nstderr:\n{forced.stderr}",
            )
            self.assertFalse(marker.exists(), "Forced install should replace destination")

    def test_installed_skill_excludes_forbidden_directories(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir)
            result = self.run_install(target)
            self.assertEqual(result.returncode, 0, result.stderr)
            dest = target / ".opencode" / "skills" / "ref-bio"
            for name in ("sources", "acquisition", "exports"):
                self.assertFalse((dest / name).exists(), f"Forbidden directory installed: {name}")
                self.assertFalse(
                    (dest / "reference-pack" / name).exists(),
                    f"Forbidden reference-pack directory installed: {name}",
                )


if __name__ == "__main__":
    unittest.main()
