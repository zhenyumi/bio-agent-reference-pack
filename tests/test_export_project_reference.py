"""Tests for export_project_reference.py."""

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
SCRIPT = REPO_ROOT / "scripts" / "export_project_reference.py"
EXPORT_DIR = REPO_ROOT / "exports" / "project-reference"

REVIEWED_LINK_ONLY_IDS = {
    "single-cell-best-practices",
    "osca",
    "osca-advanced",
    "osta",
    "seurat",
    "bioconductor-package-vignettes",
    "scuttle",
    "scran",
    "scater",
    "singlecellexperiment",
    "scdblfinder",
    "decontx-celda",
    "sctransform",
    "renv",
    "github-actions",
    "git-submodule-documentation",
}

EXPECTED_AGENTS_PHRASES = [
    "downstream project instructions override this pack",
    "link-only",
    "routing aids only",
    "no scientific summaries",
    "no upstream source files",
]


@unittest.skipIf(yaml is None, "PyYAML not installed")
class TestExportProjectReference(unittest.TestCase):
    """Test export_project_reference.py."""

    @classmethod
    def setUpClass(cls):
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        cls._result = result

    def test_script_exits_zero(self):
        self.assertEqual(
            self._result.returncode, 0,
            f"Script failed:\nstderr: {self._result.stderr}\nstdout: {self._result.stdout}",
        )

    def test_export_directory_exists(self):
        self.assertTrue(
            EXPORT_DIR.exists(),
            f"exports/project-reference/ does not exist",
        )

    def test_agents_reference_exists(self):
        agents_path = EXPORT_DIR / "AGENTS.reference.md"
        self.assertTrue(agents_path.exists(), "AGENTS.reference.md not found")

    def test_agents_reference_content(self):
        agents_path = EXPORT_DIR / "AGENTS.reference.md"
        self.assertTrue(agents_path.exists(), "AGENTS.reference.md not found")
        content = agents_path.read_text(encoding="utf-8").lower()
        for phrase in EXPECTED_AGENTS_PHRASES:
            self.assertIn(
                phrase, content,
                f"AGENTS.reference.md missing phrase: '{phrase}'",
            )

    def test_references_link_only_yaml_exists(self):
        refs_path = EXPORT_DIR / "references.link-only.yaml"
        self.assertTrue(refs_path.exists(), "references.link-only.yaml not found")

    def test_references_link_only_has_reviewed_entries(self):
        refs_path = EXPORT_DIR / "references.link-only.yaml"
        self.assertTrue(refs_path.exists(), "references.link-only.yaml not found")
        with open(refs_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        entries = data.get("entries", [])
        found_ids = {e["source_id"] for e in entries}
        self.assertEqual(found_ids, REVIEWED_LINK_ONLY_IDS)

    def test_policies_directory_exists(self):
        policies_dir = EXPORT_DIR / "policies"
        self.assertTrue(policies_dir.exists(), "policies/ directory not exported")
        md_files = list(policies_dir.glob("*.md"))
        self.assertGreater(len(md_files), 0, "No policy .md files found in export")

    def test_policies_copies_match_source(self):
        policies_src = REPO_ROOT / "policies"
        policies_dst = EXPORT_DIR / "policies"
        self.assertTrue(policies_dst.exists(), "policies/ not exported")
        src_names = {f.name for f in policies_src.glob("*.md")}
        dst_names = {f.name for f in policies_dst.glob("*.md")}
        self.assertEqual(src_names, dst_names, "Exported policies do not match source")

    def test_indexes_directory_exists(self):
        indexes_dir = EXPORT_DIR / "indexes"
        self.assertTrue(indexes_dir.exists(), "indexes/ directory not exported")
        yaml_files = list(indexes_dir.glob("*.yaml"))
        self.assertGreater(len(yaml_files), 0, "No index .yaml files found in export")

    def test_indexes_copies_match_source(self):
        indexes_src = REPO_ROOT / "indexes"
        indexes_dst = EXPORT_DIR / "indexes"
        self.assertTrue(indexes_dst.exists(), "indexes/ not exported")
        src_names = {f.name for f in indexes_src.glob("*.yaml")}
        dst_names = {f.name for f in indexes_dst.glob("*.yaml")}
        self.assertEqual(src_names, dst_names, "Exported indexes do not match source")

    def test_no_sources_upstream_exported(self):
        sources_dir = EXPORT_DIR / "sources"
        self.assertFalse(
            sources_dir.exists(),
            "sources/ should NOT be exported",
        )

    def test_no_acquisition_exported(self):
        acq_dir = EXPORT_DIR / "acquisition"
        self.assertFalse(
            acq_dir.exists(),
            "acquisition/ should NOT be exported",
        )

    def test_references_all_link_only(self):
        refs_path = EXPORT_DIR / "references.link-only.yaml"
        self.assertTrue(refs_path.exists(), "references.link-only.yaml not found")
        with open(refs_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        for entry in data.get("entries", []):
            self.assertIsNotNone(
                entry.get("upstream"),
                f"Entry '{entry.get('source_id')}' has null upstream",
            )


if __name__ == "__main__":
    unittest.main()
