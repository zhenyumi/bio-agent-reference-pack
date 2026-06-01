"""Tests for the install-opencode.sh Bash installer."""

import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
INSTALLER = REPO_ROOT / "install-opencode.sh"


class TestInstallOpencodeSh(unittest.TestCase):
    """Verify the Bash installer wrapper behaves correctly."""

    def _run_installer(self, *args):
        return subprocess.run(
            ["bash", str(INSTALLER), *args],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )

    def test_no_args_shows_help_and_exits_non_zero(self):
        result = self._run_installer()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Usage:", result.stdout)

    def test_help_works(self):
        result = self._run_installer("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Usage:", result.stdout)
        self.assertIn("--project", result.stdout)
        self.assertIn("--validate", result.stdout)

    def test_list_shows_ref_bio(self):
        result = self._run_installer("--list")
        self.assertEqual(result.returncode, 0)
        self.assertIn("ref-bio", result.stdout)
        self.assertIn("/ref-bio", result.stdout)

    def test_validate_runs(self):
        result = self._run_installer("--validate")
        self.assertEqual(
            result.returncode, 0,
            f"Validation failed:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn("All validations passed", result.stdout)

    def test_project_installs_skill(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "my-project"
            target.mkdir()
            result = self._run_installer("--project", str(target))
            self.assertEqual(
                result.returncode, 0,
                f"Install failed:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            dest = target / ".opencode" / "skills" / "ref-bio"
            self.assertTrue((dest / "SKILL.md").is_file())
            self.assertTrue(
                (dest / "reference-pack" / "references.link-only.yaml").is_file()
            )
            self.assertIn("/ref-bio", result.stdout)

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "my-project"
            target.mkdir()
            result = self._run_installer(
                "--project", str(target), "--dry-run"
            )
            self.assertEqual(
                result.returncode, 0,
                f"Dry-run failed:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            dest = target / ".opencode" / "skills" / "ref-bio"
            self.assertFalse(dest.exists())

    def test_uninstall_removes_only_skill(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "my-project"
            target.mkdir()
            install_result = self._run_installer("--project", str(target))
            self.assertEqual(install_result.returncode, 0, install_result.stderr)

            dest = target / ".opencode" / "skills" / "ref-bio"
            self.assertTrue(dest.is_dir())

            custom = target / ".opencode" / "custom.txt"
            custom.parent.mkdir(exist_ok=True)
            custom.write_text("keep me\n", encoding="utf-8")

            uninstall_result = self._run_installer(
                "--project", str(target), "--uninstall"
            )
            self.assertEqual(
                uninstall_result.returncode, 0,
                f"Uninstall failed:\nstdout:\n{uninstall_result.stdout}\nstderr:\n{uninstall_result.stderr}",
            )
            self.assertFalse(dest.exists())
            self.assertTrue(target.exists())
            self.assertTrue(
                (target / ".opencode").is_dir(),
                "Should not delete .opencode/ directory itself",
            )
            self.assertTrue(
                custom.exists(),
                "Should not delete other .opencode/ files",
            )

    def test_project_and_target_are_aliases(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "my-project"
            target.mkdir()
            result = self._run_installer("--target", str(target))
            self.assertEqual(result.returncode, 0, result.stderr)
            dest = target / ".opencode" / "skills" / "ref-bio"
            self.assertTrue((dest / "SKILL.md").is_file())

    def test_force_overwrites(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "my-project"
            target.mkdir()
            first = self._run_installer("--project", str(target))
            self.assertEqual(first.returncode, 0, first.stderr)

            marker = target / ".opencode" / "skills" / "ref-bio" / "marker.txt"
            marker.write_text("custom content\n", encoding="utf-8")

            forced = self._run_installer(
                "--project", str(target), "--force"
            )
            self.assertEqual(
                forced.returncode, 0,
                f"Forced install failed:\nstdout:\n{forced.stdout}\nstderr:\n{forced.stderr}",
            )
            self.assertFalse(marker.exists())

    def test_update_when_not_installed_reports_error(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "my-project"
            target.mkdir()
            result = self._run_installer("--project", str(target), "--update")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not currently installed", result.stderr)


if __name__ == "__main__":
    unittest.main()
