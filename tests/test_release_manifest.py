"""Tests for build_release_manifest.py."""

import os
import subprocess
import sys
import unittest
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


REPO_ROOT = Path(__file__).resolve().parent.parent
EXPORT_SCRIPT = REPO_ROOT / "scripts" / "export_project_reference.py"
MANIFEST_SCRIPT = REPO_ROOT / "scripts" / "build_release_manifest.py"
MANIFEST_PATH = REPO_ROOT / "exports" / "project-reference" / "MANIFEST.yaml"


@unittest.skipIf(yaml is None, "PyYAML not installed")
class TestBuildReleaseManifest(unittest.TestCase):
    """Test build_release_manifest.py."""

    @classmethod
    def setUpClass(cls):
        # Run export first
        subprocess.run(
            [sys.executable, str(EXPORT_SCRIPT)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        # Run manifest builder
        cls._result = subprocess.run(
            [sys.executable, str(MANIFEST_SCRIPT)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        if cls._result.returncode == 0 and MANIFEST_PATH.exists():
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                cls._manifest = yaml.safe_load(f)
        else:
            cls._manifest = None

    def test_script_exits_zero(self):
        self.assertEqual(
            self._result.returncode, 0,
            f"Script failed:\nstderr: {self._result.stderr}\nstdout: {self._result.stdout}",
        )

    def test_manifest_exists(self):
        self.assertTrue(MANIFEST_PATH.exists(), "MANIFEST.yaml not found")

    def test_manifest_has_required_fields(self):
        self.assertIsNotNone(self._manifest, "Manifest was not loaded")
        expected_keys = {
            "schema_version",
            "generated_from",
            "export_type",
            "includes_upstream_source_files",
            "source_count",
            "files",
        }
        self.assertEqual(
            set(self._manifest.keys()), expected_keys,
            f"Missing or extra top-level keys",
        )

    def test_manifest_includes_upstream_false(self):
        self.assertIsNotNone(self._manifest, "Manifest was not loaded")
        self.assertIs(
            self._manifest.get("includes_upstream_source_files"), False,
            "includes_upstream_source_files should be False",
        )

    def test_manifest_no_absolute_paths(self):
        self.assertIsNotNone(self._manifest, "Manifest was not loaded")
        for file_entry in self._manifest.get("files", []):
            p = file_entry.get("path", "")
            self.assertFalse(
                p.startswith("/"),
                f"Absolute path in manifest: {p}",
            )
            self.assertFalse(
                len(p) >= 2 and p[1] == ":",
                f"Windows drive path in manifest: {p}",
            )
            parts = Path(p).parts
            self.assertNotIn(
                "..", parts,
                f"Path traversal in manifest: {p}",
            )

    def test_manifest_source_count_matches(self):
        self.assertIsNotNone(self._manifest, "Manifest was not loaded")
        refs_path = REPO_ROOT / "exports" / "project-reference" / "references.link-only.yaml"
        self.assertTrue(refs_path.exists(), "references.link-only.yaml not found")
        with open(refs_path, "r", encoding="utf-8") as f:
            refs_data = yaml.safe_load(f)
        expected_count = len(refs_data.get("entries", []))
        self.assertEqual(
            self._manifest.get("source_count"), expected_count,
            f"source_count mismatch",
        )

    def test_manifest_file_hashes_valid(self):
        self.assertIsNotNone(self._manifest, "Manifest was not loaded")
        export_dir = REPO_ROOT / "exports" / "project-reference"
        for file_entry in self._manifest.get("files", []):
            rel = file_entry.get("path", "")
            fpath = export_dir / rel
            self.assertTrue(fpath.exists(), f"Manifest references missing file: {rel}")
            import hashlib
            h = hashlib.sha256()
            with open(fpath, "rb") as f:
                while True:
                    chunk = f.read(65536)
                    if not chunk:
                        break
                    h.update(chunk)
            self.assertEqual(
                h.hexdigest(), file_entry.get("sha256"),
                f"Hash mismatch for {rel}",
            )
            self.assertEqual(
                fpath.stat().st_size, file_entry.get("size_bytes"),
                f"Size mismatch for {rel}",
            )

    def test_manifest_excludes_itself(self):
        self.assertIsNotNone(self._manifest, "Manifest was not loaded")
        paths = {e.get("path") for e in self._manifest.get("files", [])}
        self.assertNotIn(
            "MANIFEST.yaml", paths,
            "MANIFEST.yaml should not be in its own file list",
        )


if __name__ == "__main__":
    unittest.main()
