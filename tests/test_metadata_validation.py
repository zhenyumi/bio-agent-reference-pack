"""Tests for metadata validation script."""

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "validate_metadata.py"


class TestMetadataValidation(unittest.TestCase):
    """Test that validate_metadata.py passes against the current repository state."""

    def test_validation_passes(self):
        """The validation script should exit 0 with a success message."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.returncode, 0, f"Validation failed:\n{result.stderr}"
        )
        self.assertIn("passed", result.stdout.lower())
        self.assertEqual(result.stderr, "", f"Unexpected stderr:\n{result.stderr}")


if __name__ == "__main__":
    unittest.main()
