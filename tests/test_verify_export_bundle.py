"""Tests for verify_export_bundle.py."""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


REPO_ROOT = Path(__file__).resolve().parent.parent
EXPORT_SCRIPT = REPO_ROOT / "scripts" / "export_project_reference.py"
MANIFEST_SCRIPT = REPO_ROOT / "scripts" / "build_release_manifest.py"
VERIFY_SCRIPT = REPO_ROOT / "scripts" / "verify_export_bundle.py"


@unittest.skipIf(yaml is None, "PyYAML not installed")
class TestVerifyExportBundle(unittest.TestCase):
    """Test verify_export_bundle.py."""

    @classmethod
    def setUpClass(cls):
        # Run export and manifest builder
        subprocess.run(
            [sys.executable, str(EXPORT_SCRIPT)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [sys.executable, str(MANIFEST_SCRIPT)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )

    def test_verify_passes(self):
        result = subprocess.run(
            [sys.executable, str(VERIFY_SCRIPT)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.returncode, 0,
            f"Verify failed:\nstderr: {result.stderr}\nstdout: {result.stdout}",
        )

    def test_verify_fails_missing_manifest(self):
        """Verifier should fail if MANIFEST.yaml is missing."""
        export_src = REPO_ROOT / "exports" / "project-reference"
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_export = Path(tmpdir) / "project-reference"
            shutil.copytree(export_src, tmp_export)
            (tmp_export / "MANIFEST.yaml").unlink()

            result = subprocess.run(
                [sys.executable, str(VERIFY_SCRIPT), str(tmp_export)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(
                result.returncode, 0,
                "Verify should fail when MANIFEST.yaml is missing",
            )

    def test_verify_fails_tampered_hash(self):
        """Verifier should fail if a file is tampered."""
        export_src = REPO_ROOT / "exports" / "project-reference"
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_export = Path(tmpdir) / "project-reference"
            shutil.copytree(export_src, tmp_export)
            # Tamper with a file
            tamper_file = tmp_export / "AGENTS.reference.md"
            with open(tamper_file, "a", encoding="utf-8") as f:
                f.write("\n# tampered\n")

            result = subprocess.run(
                [sys.executable, str(VERIFY_SCRIPT), str(tmp_export)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(
                result.returncode, 0,
                "Verify should fail when file hash is tampered",
            )

    def test_verify_detects_forbidden_sources_dir(self):
        """Verifier should fail if sources/ is present in export."""
        export_src = REPO_ROOT / "exports" / "project-reference"
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_export = Path(tmpdir) / "project-reference"
            shutil.copytree(export_src, tmp_export)
            # Keep MANIFEST.yaml; just add forbidden directory
            os.makedirs(tmp_export / "sources")

            result = subprocess.run(
                [sys.executable, str(VERIFY_SCRIPT), str(tmp_export)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(
                result.returncode, 0,
                "Verify should fail when sources/ is present",
            )
            self.assertIn(
                "Forbidden directory present", result.stderr,
                f"Expected 'Forbidden directory present' in stderr:\n{result.stderr}",
            )

    def test_verify_fails_extra_file_not_in_manifest(self):
        """Verifier should fail if an extra file exists not listed in manifest."""
        export_src = REPO_ROOT / "exports" / "project-reference"
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_export = Path(tmpdir) / "project-reference"
            shutil.copytree(export_src, tmp_export)
            # Add an extra file
            extra_file = tmp_export / "EXTRA.txt"
            extra_file.write_text("this file is not in the manifest\n")

            result = subprocess.run(
                [sys.executable, str(VERIFY_SCRIPT), str(tmp_export)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(
                result.returncode, 0,
                "Verify should fail when extra file is not listed in manifest",
            )
            self.assertIn(
                "not listed in manifest", result.stderr,
                f"Expected 'not listed in manifest' in stderr:\n{result.stderr}",
            )


if __name__ == "__main__":
    unittest.main()
