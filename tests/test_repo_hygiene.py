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


class TestSecretPatterns(unittest.TestCase):
    """Test that secret patterns detect expected values using temp files."""

    @classmethod
    def setUpClass(cls):
        import importlib.util
        spec = importlib.util.spec_from_file_location("scan_repo_hygiene", SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        cls._mod = mod
        cls.PATTERNS = {name: pat for name, pat in mod.SECRET_PATTERNS}

    def _match(self, pattern_name, text):
        pat = self.PATTERNS[pattern_name]
        return pat.search(text)

    def _make_openai_key(self):
        return "sk-" + "proj-" + "a" * 30

    def _make_posix_users_path(self):
        return "/".join(["", "Users", "alice", "project", "file.txt"])

    def _make_posix_home_path(self):
        return "/".join(["", "home", "alice", "project", "file.txt"])

    def _make_windows_path(self):
        return "C:" + "\\" + "Users" + "\\" + "alice" + "\\" + "project" + "\\" + "file.txt"

    def test_openai_key_in_comment(self):
        key = self._make_openai_key()
        self.assertIsNotNone(
            self._match("openai_api_key", "# " + key),
            "OpenAI key in a comment line should be detected",
        )

    def test_openai_key_standard(self):
        key = self._make_openai_key()
        self.assertIsNotNone(
            self._match("openai_api_key", key),
            "OpenAI proj key should be detected",
        )

    def test_posix_users_path(self):
        path = self._make_posix_users_path()
        self.assertIsNotNone(
            self._match("absolute_home_path", path),
            "POSIX /Users/ path should be detected",
        )

    def test_posix_home_path(self):
        path = self._make_posix_home_path()
        self.assertIsNotNone(
            self._match("absolute_home_path", path),
            "POSIX /home/ path should be detected",
        )

    def test_windows_path(self):
        path = self._make_windows_path()
        self.assertIsNotNone(
            self._match("absolute_home_path", path),
            "Windows C:\\Users\\ path should be detected",
        )

    def test_no_false_positive_skip_attribute(self):
        self.assertIsNone(
            self._match("openai_api_key", "skip-attribute"),
            "skip-attribute should not match OpenAI key pattern",
        )

    def test_scan_detects_secrets_in_temp_file(self):
        """Full scan pipeline: temp file with secret is detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            secret_file = tmpdir / "bad.txt"
            key = self._make_openai_key()
            secret_file.write_text("# " + key + "\n")
            rel = "bad.txt"
            errors = self._mod.scan(
                repo_root=tmpdir,
                file_paths=[rel],
                check_upstream=False,
            )
            self.assertTrue(
                any("openai_api_key" in e for e in errors),
                f"Scanner should detect OpenAI key in temp file. Errors: {errors}",
            )

    def test_scan_detects_path_in_temp_file(self):
        """Full scan pipeline: temp file with absolute path is detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            bad_file = tmpdir / "paths.txt"
            path = self._make_posix_users_path()
            bad_file.write_text('config = "' + path + '"\n')
            rel = "paths.txt"
            errors = self._mod.scan(
                repo_root=tmpdir,
                file_paths=[rel],
                check_upstream=False,
            )
            self.assertTrue(
                any("absolute_home_path" in e for e in errors),
                f"Scanner should detect absolute path in temp file. Errors: {errors}",
            )

    def test_scan_clean_file_has_no_errors(self):
        """Full scan pipeline: clean temp file produces no errors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            clean_file = tmpdir / "clean.txt"
            clean_file.write_text("This is a clean file with no secrets.\n")
            rel = "clean.txt"
            errors = self._mod.scan(
                repo_root=tmpdir,
                file_paths=[rel],
                check_upstream=False,
            )
            self.assertEqual(errors, [], f"Clean file should have no errors: {errors}")


if __name__ == "__main__":
    unittest.main()
