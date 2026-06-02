"""Offline tests for scripts/check_links_online.py.

All HTTP responses are mocked — no real network requests.
"""

import subprocess
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import MagicMock, patch

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "check_links_online.py"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import check_links_online


def _make_response(code=200, url=None):
    resp = MagicMock()
    resp.getcode.return_value = code
    resp.geturl.return_value = url or "https://example.com"
    resp.read.return_value = b""
    return resp


class TestCheckUrl(unittest.TestCase):
    """Unit tests for check_url()."""

    @patch("check_links_online.urllib.request.urlopen")
    def test_head_success(self, mock_urlopen):
        mock_urlopen.return_value = _make_response(200, "https://example.com")
        result = check_links_online.check_url("https://example.com")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["http_status"], 200)
        self.assertFalse(result["redirected"])

    @patch("check_links_online.urllib.request.urlopen")
    def test_head_405_falls_back_to_get(self, mock_urlopen):
        mock_urlopen.side_effect = [
            urllib.error.HTTPError(
                "https://example.com", 405, "Method Not Allowed", {}, None
            ),
            _make_response(200, "https://example.com"),
        ]
        result = check_links_online.check_url("https://example.com")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["http_status"], 200)

    @patch("check_links_online.urllib.request.urlopen")
    def test_head_404_is_failure(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.HTTPError(
            "https://example.com", 404, "Not Found", {}, None
        )
        result = check_links_online.check_url("https://example.com")
        self.assertEqual(result["status"], "unreachable")
        self.assertEqual(result["http_status"], 404)

    @patch("check_links_online.urllib.request.urlopen")
    def test_redirect_detected(self, mock_urlopen):
        mock_urlopen.return_value = _make_response(200, "https://example.com/new")
        result = check_links_online.check_url("https://example.com/old")
        self.assertEqual(result["status"], "redirect")
        self.assertTrue(result["redirected"])
        self.assertEqual(result["final_url"], "https://example.com/new")


class TestRunExitBehavior(unittest.TestCase):
    """Tests for run() exit code policy."""

    def _make_temp_repo(self, entries):
        tmpdir = Path(tempfile.mkdtemp())
        refs = {"schema_version": "0.1", "entries": entries}
        with open(tmpdir / "references.yaml", "w") as f:
            yaml.dump(refs, f)
        return tmpdir

    def _broken_result(self, url="https://x.com"):
        return {
            "original_url": url,
            "final_url": url,
            "http_status": 404,
            "status": "unreachable",
            "redirected": False,
            "error": "HTTP 404",
        }

    def _ok_result(self, url="https://x.com"):
        return {
            "original_url": url,
            "final_url": url,
            "http_status": 200,
            "status": "ok",
            "redirected": False,
            "error": None,
        }

    @patch("check_links_online.check_url")
    def test_link_only_upstream_failure_exits_1(self, mock_check):
        mock_check.return_value = self._broken_result()
        tmpdir = self._make_temp_repo([
            {"id": "a", "acquisition_mode": "link_only", "upstream": "https://x.com"}
        ])
        self.assertEqual(check_links_online.run(tmpdir), 1)

    @patch("check_links_online.check_url")
    def test_metadata_only_upstream_failure_exits_0(self, mock_check):
        mock_check.return_value = self._broken_result()
        tmpdir = self._make_temp_repo([
            {"id": "a", "acquisition_mode": "metadata_only", "upstream": "https://x.com"}
        ])
        self.assertEqual(check_links_online.run(tmpdir), 0)

    @patch("check_links_online.check_url")
    def test_license_evidence_failure_exits_0(self, mock_check):
        mock_check.return_value = self._broken_result()
        tmpdir = self._make_temp_repo([
            {"id": "a", "acquisition_mode": "link_only",
             "upstream": "https://ok.com",
             "license_evidence_url": "https://x.com/LICENSE"}
        ])
        mock_check.return_value = self._ok_result()
        # Override to return broken for the license URL
        def side_effect(url, timeout=15):
            if "LICENSE" in url:
                return self._broken_result(url)
            return self._ok_result(url)
        mock_check.side_effect = side_effect
        self.assertEqual(check_links_online.run(tmpdir), 0)

    @patch("check_links_online.check_url")
    def test_report_writes_yaml(self, mock_check):
        mock_check.return_value = self._ok_result()
        tmpdir = self._make_temp_repo([
            {"id": "a", "acquisition_mode": "link_only", "upstream": "https://x.com"}
        ])
        check_links_online.run(tmpdir, report=True)
        report_path = tmpdir / "reports" / "links-check.yaml"
        self.assertTrue(report_path.exists())
        with open(report_path) as f:
            data = yaml.safe_load(f)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["source_id"], "a")


class TestSubprocessSmoke(unittest.TestCase):
    """Minimal subprocess smoke test (no network access)."""

    def test_help_flag(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--help"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("--no-fail", result.stdout)
        self.assertIn("--report", result.stdout)


if __name__ == "__main__":
    unittest.main()
