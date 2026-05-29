"""Integration test for the full export pipeline.

Runs all 4 export scripts end-to-end, then verifies:
- verifier passes on the generated bundle
- key output files exist
- forbidden directories are absent
- manifest safety assertions hold
- verifier catches tampering (negative tests)
"""

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
EXPORT_DIR = REPO_ROOT / "exports" / "project-reference"

CATALOG_SCRIPT = REPO_ROOT / "scripts" / "build_link_catalog.py"
EXPORT_SCRIPT = REPO_ROOT / "scripts" / "export_project_reference.py"
MANIFEST_SCRIPT = REPO_ROOT / "scripts" / "build_release_manifest.py"
VERIFY_SCRIPT = REPO_ROOT / "scripts" / "verify_export_bundle.py"

ALLOWED_REF_FIELDS = {"source_id", "title", "source_type", "upstream", "license", "notes"}


def run_script(script_path, cwd=REPO_ROOT):
    return subprocess.run(
        [sys.executable, str(script_path)],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


@unittest.skipIf(yaml is None, "PyYAML not installed")
class TestExportPipeline(unittest.TestCase):
    """End-to-end export pipeline integration tests."""

    @classmethod
    def setUpClass(cls):
        for script in [CATALOG_SCRIPT, EXPORT_SCRIPT, MANIFEST_SCRIPT]:
            result = run_script(script)
            if result.returncode != 0:
                raise RuntimeError(
                    f"Pipeline script {script.name} failed:\n"
                    f"stderr: {result.stderr}\nstdout: {result.stdout}"
                )
        cls._verify_result = run_script(VERIFY_SCRIPT)

    def test_verifier_passes(self):
        """The verifier should exit 0 on a valid bundle."""
        self.assertEqual(
            self._verify_result.returncode, 0,
            f"Verifier failed:\n{self._verify_result.stderr}",
        )

    def test_manifest_exists(self):
        """MANIFEST.yaml must be present in the export."""
        manifest_path = EXPORT_DIR / "MANIFEST.yaml"
        self.assertTrue(manifest_path.exists(), "MANIFEST.yaml not found")

    def test_references_link_only_exists(self):
        """references.link-only.yaml must be present in the export."""
        refs_path = EXPORT_DIR / "references.link-only.yaml"
        self.assertTrue(refs_path.exists(), "references.link-only.yaml not found")

    def test_references_have_only_allowed_fields(self):
        """Exported references must not leak local_path, version, or acquisition metadata."""
        refs_path = EXPORT_DIR / "references.link-only.yaml"
        self.assertTrue(refs_path.exists(), "references.link-only.yaml not found")
        with open(refs_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        entries = data.get("entries", [])
        self.assertGreater(len(entries), 0, "No entries in references.link-only.yaml")
        for entry in entries:
            extra = set(entry.keys()) - ALLOWED_REF_FIELDS
            self.assertEqual(
                extra, set(),
                f"Entry '{entry.get('source_id')}' has extra fields: {extra}",
            )

    def test_no_sources_or_acquisition_in_export(self):
        """sources/ and acquisition/ must not be present in the export."""
        self.assertFalse(
            (EXPORT_DIR / "sources").exists(),
            "sources/ should NOT be exported",
        )
        self.assertFalse(
            (EXPORT_DIR / "acquisition").exists(),
            "acquisition/ should NOT be exported",
        )

    def test_includes_upstream_source_files_is_false(self):
        """Manifest must declare includes_upstream_source_files: false."""
        manifest_path = EXPORT_DIR / "MANIFEST.yaml"
        self.assertTrue(manifest_path.exists(), "MANIFEST.yaml not found")
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = yaml.safe_load(f)
        self.assertIs(
            manifest.get("includes_upstream_source_files"), False,
            "includes_upstream_source_files should be False",
        )

    def test_verifier_fails_tampered_hash(self):
        """Verifier should detect a tampered file hash."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_export = Path(tmpdir) / "project-reference"
            shutil.copytree(EXPORT_DIR, tmp_export)
            tamper_file = tmp_export / "AGENTS.reference.md"
            with open(tamper_file, "a", encoding="utf-8") as f:
                f.write("\n# tampered\n")
            # Run verifier against temp dir
            result = subprocess.run(
                [sys.executable, str(VERIFY_SCRIPT), str(tmp_export)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(
                result.returncode, 0,
                "Verifier should fail when file is tampered",
            )

    def test_verifier_fails_extra_file(self):
        """Verifier should detect an extra file not listed in manifest."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_export = Path(tmpdir) / "project-reference"
            shutil.copytree(EXPORT_DIR, tmp_export)
            (tmp_export / "EXTRA.txt").write_text("not in manifest\n")
            result = subprocess.run(
                [sys.executable, str(VERIFY_SCRIPT), str(tmp_export)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(
                result.returncode, 0,
                "Verifier should fail when extra file is not listed in manifest",
            )
            self.assertIn(
                "not listed in manifest", result.stderr,
                f"Expected 'not listed in manifest' in stderr:\n{result.stderr}",
            )

    def test_verifier_fails_forbidden_dir(self):
        """Verifier should detect a forbidden sources/ directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_export = Path(tmpdir) / "project-reference"
            shutil.copytree(EXPORT_DIR, tmp_export)
            os.makedirs(tmp_export / "sources")
            result = subprocess.run(
                [sys.executable, str(VERIFY_SCRIPT), str(tmp_export)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(
                result.returncode, 0,
                "Verifier should fail when sources/ is present",
            )
            self.assertIn(
                "Forbidden directory present", result.stderr,
                f"Expected 'Forbidden directory present' in stderr:\n{result.stderr}",
            )


if __name__ == "__main__":
    unittest.main()
