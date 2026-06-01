"""Tests for the upstream update check script."""

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "check_upstream_updates.py"


class TestCheckUpstreamUpdates(unittest.TestCase):
    """Test that check_upstream_updates.py passes against the current repository state."""

    def _run_script(self):
        return subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )

    def test_script_runs_successfully(self):
        result = self._run_script()
        self.assertEqual(
            result.returncode, 0,
            f"Script failed with exit {result.returncode}:\n{result.stderr}"
        )

    def test_reports_mode_counts(self):
        result = self._run_script()
        self.assertIn("link_only", result.stdout,
                       "Expected 'link_only' in mode summary")
        self.assertIn("metadata_only", result.stdout,
                       "Expected 'metadata_only' in mode summary")
        self.assertIn("defer", result.stdout,
                       "Expected 'defer' in mode summary")

    def test_reports_unknown_pending_review(self):
        result = self._run_script()
        self.assertIn("unknown_pending_review", result.stdout,
                       "Expected unknown_pending_review section")

    def test_confirms_sources_lock_empty(self):
        result = self._run_script()
        stdout_lower = result.stdout.lower()
        self.assertTrue(
            "no acquired sources" in stdout_lower
            or "sources: []" in result.stdout,
            "Expected confirmation that sources.lock.yaml has 0 acquired sources"
        )

    def test_confirms_upstream_only_gitkeep(self):
        result = self._run_script()
        self.assertIn(".gitkeep", result.stdout,
                       "Expected reporting that sources/upstream/ contains .gitkeep")


if __name__ == "__main__":
    unittest.main()
