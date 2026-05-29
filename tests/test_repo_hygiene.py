"""Tests for repository hygiene scanner."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "scan_repo_hygiene.py"


class TestRepoHygiene(unittest.TestCase):
    """Test that scan_repo_hygiene.py passes against the current repository state."""

    def test_hygiene_scan_passes(self):
        """The hygiene scanner should exit 0 with a success message."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.returncode, 0, f"Hygiene scan failed:\n{result.stderr}"
        )
        self.assertIn("passed", result.stdout.lower())
        self.assertEqual(result.stderr, "", f"Unexpected stderr:\n{result.stderr}")


class TestSecretPatternRegression(unittest.TestCase):
    """Regression tests ensuring the scanner catches secrets and paths in temp files."""

    @classmethod
    def setUpClass(cls):
        import importlib.util
        spec = importlib.util.spec_from_file_location("scan_repo_hygiene", SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        cls._mod = mod

    def test_comment_line_with_secret_is_detected(self):
        """A comment line containing a secret token must be detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            secret_file = tmpdir / "bad.txt"
            key = "sk-" + "proj-" + "a" * 30
            secret_file.write_text("# " + key + "\n")
            errors = self._mod.scan(
                repo_root=tmpdir,
                file_paths=["bad.txt"],
                check_upstream=False,
            )
            self.assertTrue(
                any("openai_api_key" in e for e in errors),
                f"Scanner should detect OpenAI key in comment line. Errors: {errors}",
            )

    def test_absolute_path_in_file_is_detected(self):
        """A file containing an absolute home path must be detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            bad_file = tmpdir / "paths.txt"
            path = "/".join(["", "Users", "alice", "project", "file.txt"])
            bad_file.write_text('config = "' + path + '"\n')
            errors = self._mod.scan(
                repo_root=tmpdir,
                file_paths=["paths.txt"],
                check_upstream=False,
            )
            self.assertTrue(
                any("absolute_home_path" in e for e in errors),
                f"Scanner should detect absolute path. Errors: {errors}",
            )

    def test_clean_file_has_no_errors(self):
        """A clean file should produce no scan errors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            clean_file = tmpdir / "clean.txt"
            clean_file.write_text("This is a clean file with no secrets.\n")
            errors = self._mod.scan(
                repo_root=tmpdir,
                file_paths=["clean.txt"],
                check_upstream=False,
            )
            self.assertEqual(errors, [], f"Clean file should have no errors: {errors}")


if __name__ == "__main__":
    unittest.main()
