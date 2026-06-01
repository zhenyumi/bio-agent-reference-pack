"""Tests for exporting the /ref-bio OpenCode skill bundle."""

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "export_opencode_skill.py"
EXPORT_DIR = REPO_ROOT / "exports" / "opencode-skill" / "ref-bio"


class TestOpenCodeSkillExport(unittest.TestCase):
    """Verify that the skill export contains only the expected lightweight bundle."""

    @classmethod
    def setUpClass(cls):
        cls.result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )

    def test_export_script_passes(self):
        self.assertEqual(
            self.result.returncode, 0,
            f"Export failed:\nstdout:\n{self.result.stdout}\nstderr:\n{self.result.stderr}",
        )

    def test_export_directory_exists(self):
        self.assertTrue(EXPORT_DIR.is_dir(), "Skill export directory was not created")

    def test_export_contains_skill(self):
        skill_path = EXPORT_DIR / "SKILL.md"
        self.assertTrue(skill_path.is_file(), "Exported SKILL.md missing")
        self.assertIn("/ref-bio", skill_path.read_text(encoding="utf-8"))

    def test_export_contains_reference_pack(self):
        reference_pack = EXPORT_DIR / "reference-pack"
        self.assertTrue((reference_pack / "AGENTS.reference.md").is_file())
        self.assertTrue((reference_pack / "references.link-only.yaml").is_file())
        self.assertTrue((reference_pack / "indexes").is_dir())
        self.assertTrue((reference_pack / "policies").is_dir())
        self.assertTrue((reference_pack / "MANIFEST.yaml").is_file())

    def test_export_excludes_forbidden_directories(self):
        forbidden = ["sources", "acquisition", "exports"]
        for name in forbidden:
            self.assertFalse(
                (EXPORT_DIR / name).exists(),
                f"Forbidden top-level directory exported: {name}",
            )
            self.assertFalse(
                (EXPORT_DIR / "reference-pack" / name).exists(),
                f"Forbidden reference-pack directory exported: {name}",
            )


if __name__ == "__main__":
    unittest.main()
