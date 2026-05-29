"""Tests for build_link_catalog.py."""

import subprocess
import sys
import unittest
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "build_link_catalog.py"
CATALOG_PATH = REPO_ROOT / "exports" / "link-catalog.yaml"

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

PLANNED_IDS = {
    "clusterprofiler",
    "mast",
    "singler",
    "liana",
    "cellchat",
    "monocle3",
    "codex-agents-guidance",
    "opencode-documentation",
    "gptomics-bioskills",
    "seurat-integration",
    "seurat-reference-mapping",
    "azimuth",
    "batchelor",
    "harmony",
    "celldex",
    "enrichplot",
    "fgsea",
    "msigdbr",
    "limma",
    "edger",
    "deseq2",
    "pseudobulk-de-guidance",
    "spatialexperiment",
    "spatialfeatureexperiment",
    "seurat-spatial",
    "visium",
    "xenium",
    "cosmx",
    "stutility",
    "banksy",
    "nnsvg",
    "squidpy",
    "giotto",
    "bayesspace",
    "spark-x",
    "nichenet",
    "slingshot",
    "tradeseq",
    "soupx",
}

ALLOWED_FIELDS = {"source_id", "title", "source_type", "upstream", "license", "notes"}


@unittest.skipIf(yaml is None, "PyYAML not installed")
class TestBuildLinkCatalog(unittest.TestCase):
    """Test build_link_catalog.py."""

    @classmethod
    def setUpClass(cls):
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        cls._result = result
        if result.returncode == 0 and CATALOG_PATH.exists():
            with open(CATALOG_PATH, "r", encoding="utf-8") as f:
                cls._catalog = yaml.safe_load(f)
        else:
            cls._catalog = None

    def test_script_exits_zero(self):
        self.assertEqual(
            self._result.returncode, 0,
            f"Script failed:\nstderr: {self._result.stderr}\nstdout: {self._result.stdout}",
        )

    def test_catalog_file_exists(self):
        self.assertTrue(
            CATALOG_PATH.exists(),
            f"exports/link-catalog.yaml does not exist after running script",
        )

    def test_catalog_has_16_entries(self):
        self.assertIsNotNone(self._catalog, "Catalog was not loaded")
        entries = self._catalog.get("entries", [])
        self.assertEqual(
            len(entries), 16,
            f"Expected 16 entries, got {len(entries)}",
        )

    def test_catalog_contains_all_reviewed_ids(self):
        self.assertIsNotNone(self._catalog, "Catalog was not loaded")
        entries = self._catalog.get("entries", [])
        found_ids = {e["source_id"] for e in entries}
        missing = REVIEWED_LINK_ONLY_IDS - found_ids
        self.assertEqual(
            missing, set(),
            f"Missing reviewed source IDs: {missing}",
        )

    def test_catalog_excludes_planned_ids(self):
        self.assertIsNotNone(self._catalog, "Catalog was not loaded")
        entries = self._catalog.get("entries", [])
        found_ids = {e["source_id"] for e in entries}
        unexpected = found_ids & PLANNED_IDS
        self.assertEqual(
            unexpected, set(),
            f"Unexpected planned source IDs in catalog: {unexpected}",
        )

    def test_catalog_entries_have_only_allowed_fields(self):
        self.assertIsNotNone(self._catalog, "Catalog was not loaded")
        for entry in self._catalog.get("entries", []):
            extra = set(entry.keys()) - ALLOWED_FIELDS
            self.assertEqual(
                extra, set(),
                f"Entry '{entry.get('source_id')}' has extra fields: {extra}",
            )

    def test_catalog_no_local_path_or_version(self):
        self.assertIsNotNone(self._catalog, "Catalog was not loaded")
        for entry in self._catalog.get("entries", []):
            self.assertNotIn(
                "local_path", entry,
                f"Entry '{entry.get('source_id')}' should not have local_path",
            )
            self.assertNotIn(
                "version", entry,
                f"Entry '{entry.get('source_id')}' should not have version",
            )

    def test_catalog_upstream_not_null(self):
        self.assertIsNotNone(self._catalog, "Catalog was not loaded")
        for entry in self._catalog.get("entries", []):
            self.assertIsNotNone(
                entry.get("upstream"),
                f"Entry '{entry.get('source_id')}' has null upstream",
            )


if __name__ == "__main__":
    unittest.main()
