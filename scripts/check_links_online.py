#!/usr/bin/env python3
"""
Online link checker for bio-agent-reference-pack.

Checks upstream and license_evidence_url fields in references.yaml.
Uses urllib (stdlib only). No new dependencies.

Default behavior:
  - HEAD requests, fallback to GET only for 403/405/501/method-related HTTPError
  - 404 and most 5xx are treated as failures (no GET fallback)
  - Exit 1 on unreachable upstream URLs for link_only entries only
  - metadata_only upstream and license_evidence_url failures are warnings only (no exit 1)
  - Prints human-readable summary to stdout

Flags:
  --no-fail     Always exit 0 (for CI)
  --report      Write structured report to reports/links-check.yaml
  --timeout     Request timeout in seconds (default 15)

Usage:
    python3 scripts/check_links_online.py
    python3 scripts/check_links_online.py --no-fail --report
    python3 scripts/check_links_online.py --help
"""

import argparse
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

SKIP_ACQUISITION_MODES = {"defer"}


def find_repo_root():
    path = Path(__file__).resolve().parent.parent
    if not (path / "references.yaml").exists():
        print("ERROR: references.yaml not found at repo root", file=sys.stderr)
        sys.exit(1)
    return path


def load_references(repo_root):
    with open(repo_root / "references.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def collect_urls(references):
    """Collect (source_id, field, url, acquisition_mode) tuples for non-deferred entries."""
    urls = []
    for entry in references.get("entries", []):
        sid = entry.get("id", "unknown")
        mode = entry.get("acquisition_mode", "")
        if mode in SKIP_ACQUISITION_MODES:
            continue
        upstream = entry.get("upstream")
        if upstream:
            urls.append((sid, "upstream", upstream, mode))
        evidence = entry.get("license_evidence_url")
        if evidence:
            urls.append((sid, "license_evidence_url", evidence, mode))
    return urls


def check_url(url, timeout=15):
    """Check a URL with HEAD, falling back to GET only for specific failures."""
    result = {
        "original_url": url,
        "final_url": url,
        "http_status": None,
        "status": "error",
        "redirected": False,
        "error": None,
    }

    # Try HEAD first
    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "bio-agent-reference-pack/1.0 link-checker")
        resp = urllib.request.urlopen(req, timeout=timeout)
        result["http_status"] = resp.getcode()
        result["final_url"] = resp.geturl()
        result["redirected"] = resp.geturl() != url
        result["status"] = "ok" if not result["redirected"] else "redirect"
        return result
    except urllib.error.HTTPError as e:
        code = e.code
        result["http_status"] = code
        # Fall back to GET for method-not-supported errors
        if code in (403, 405, 501):
            return _try_get(url, timeout, result)
        # 404 and other HTTP errors: treat as failure
        result["status"] = "unreachable"
        result["error"] = f"HTTP {code}"
        return result
    except urllib.error.URLError as e:
        result["status"] = "unreachable"
        result["error"] = str(e.reason)
        return result
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        return result


def _try_get(url, timeout, result):
    """Fallback: try GET request."""
    try:
        req = urllib.request.Request(url, method="GET")
        req.add_header("User-Agent", "bio-agent-reference-pack/1.0 link-checker")
        resp = urllib.request.urlopen(req, timeout=timeout)
        result["http_status"] = resp.getcode()
        result["final_url"] = resp.geturl()
        result["redirected"] = resp.geturl() != url
        result["status"] = "ok" if not result["redirected"] else "redirect"
        return result
    except urllib.error.HTTPError as e:
        result["http_status"] = e.code
        result["status"] = "unreachable"
        result["error"] = f"HTTP {e.code}"
        return result
    except urllib.error.URLError as e:
        result["status"] = "unreachable"
        result["error"] = str(e.reason)
        return result
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        return result


def run(repo_root, timeout=15, no_fail=False, report=False):
    references = load_references(repo_root)
    urls = collect_urls(references)

    if not urls:
        print("No URLs to check.")
        return 0

    print(f"Checking {len(urls)} URLs...")
    print()

    checked_at = datetime.now(timezone.utc).isoformat()
    results = []
    has_broken_upstream = False

    for source_id, field, url, mode in urls:
        result = check_url(url, timeout=timeout)
        result["source_id"] = source_id
        result["field"] = field
        result["acquisition_mode"] = mode
        result["checked_at"] = checked_at
        results.append(result)

        # Determine if this is a failure
        is_failure = result["status"] not in ("ok", "redirect")
        is_strict_failure = (
            is_failure
            and field == "upstream"
            and mode == "link_only"
        )

        # Print status line
        status_icon = "OK" if result["status"] == "ok" else (
            "REDIRECT" if result["status"] == "redirect" else "FAIL"
        )
        print(f"  [{status_icon}] {source_id} ({field}): {url}")
        if result["redirected"]:
            print(f"         -> {result['final_url']}")
        if result["error"]:
            print(f"         error: {result['error']}")

        # Track failures for exit code
        if is_strict_failure:
            has_broken_upstream = True
        elif is_failure:
            print(f"         (warning only)")

    print()

    # Summary
    ok_count = sum(1 for r in results if r["status"] == "ok")
    redirect_count = sum(1 for r in results if r["status"] == "redirect")
    fail_count = sum(1 for r in results if r["status"] not in ("ok", "redirect"))

    print(f"Results: {ok_count} ok, {redirect_count} redirected, {fail_count} failed")

    # Write report if requested
    if report:
        reports_dir = repo_root / "reports"
        reports_dir.mkdir(exist_ok=True)
        report_path = reports_dir / "links-check.yaml"
        with open(report_path, "w", encoding="utf-8") as f:
            yaml.dump(results, f, default_flow_style=False, allow_unicode=True)
        print(f"Report written to {report_path}")

    # Exit code
    if no_fail:
        return 0
    if has_broken_upstream:
        print("\nLINK CHECK FAILED: broken upstream URLs detected", file=sys.stderr)
        return 1
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Check upstream links in references.yaml"
    )
    parser.add_argument(
        "--no-fail",
        action="store_true",
        help="Always exit 0 (for CI report generation)",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Write structured report to reports/links-check.yaml",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="Request timeout in seconds (default: 15)",
    )
    args = parser.parse_args()

    repo_root = find_repo_root()
    return run(repo_root, timeout=args.timeout, no_fail=args.no_fail, report=args.report)


if __name__ == "__main__":
    sys.exit(main())
