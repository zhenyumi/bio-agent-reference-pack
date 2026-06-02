#!/usr/bin/env python3
"""
Lightweight update-review and lock-policy tooling for bio-agent-reference-pack.

Local, deterministic, safe by default:
- No network access
- No URL fetching
- No source downloads
- No git clone
- No scientific summaries

Reports:
- Total references by acquisition_mode
- Entries with license: unknown_pending_review
- Entries missing upstream URLs
- Entries missing license_evidence_url (warning only; not an error)
- metadata_only entries and their routing notes
- defer entries
- sources.lock.yaml state (empty or contains acquired sources)
- sources/upstream/ state (only .gitkeep or unexpected files)
- Index cross-reference consistency (planned_source_ids vs references.yaml)
- Unused source IDs (warning only; not an error)

Exit behavior:
- exit 0: repository is internally consistent
- exit 1: mechanical error (invalid YAML, missing upstream for link_only,
           non-acquired modes in sources.lock.yaml, unexpected files in
           sources/upstream/)

Usage:
    python3 scripts/check_upstream_updates.py
    python3 scripts/check_upstream_updates.py --online   # prints stub; no network
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

LOCK_ACQUISITION_MODES = {"git_submodule", "pinned_vendor_snapshot"}


def find_repo_root():
    path = Path(__file__).resolve().parent.parent
    if not (path / "references.yaml").exists():
        print("ERROR: Cannot find repository root (references.yaml not found).", file=sys.stderr)
        sys.exit(1)
    return path


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def collect_index_source_ids(indexes_dir):
    all_ids = set()
    for yaml_file in sorted(indexes_dir.glob("*.yaml")):
        data = load_yaml(yaml_file)
        for key in ("topics", "workflow_stages", "packages"):
            for item in data.get(key, []):
                for sid in item.get("planned_source_ids", []):
                    all_ids.add(sid)
    return all_ids


def run(repo_root):
    errors = []
    warnings = []

    # --- Load references ---
    try:
        refs_data = load_yaml(repo_root / "references.yaml")
    except Exception as e:
        print(f"FATAL: Failed to parse references.yaml: {e}", file=sys.stderr)
        return 1

    entries = refs_data.get("entries", [])
    ref_ids = {e.get("id") for e in entries}
    ref_by_id = {e.get("id"): e for e in entries}

    # --- Load sources.lock.yaml ---
    try:
        lock_data = load_yaml(repo_root / "sources.lock.yaml")
    except Exception as e:
        print(f"FATAL: Failed to parse sources.lock.yaml: {e}", file=sys.stderr)
        return 1

    lock_sources = lock_data.get("sources", [])

    # --- Load indexes ---
    try:
        index_ids = collect_index_source_ids(repo_root / "indexes")
    except Exception as e:
        print(f"FATAL: Failed to load indexes: {e}", file=sys.stderr)
        return 1

    # =================================================================
    # Report: Acquisition mode counts
    # =================================================================
    mode_counts = {}
    for e in entries:
        mode = e.get("acquisition_mode", "unknown")
        mode_counts[mode] = mode_counts.get(mode, 0) + 1

    print("=== Acquisition Mode Summary ===")
    for mode in sorted(mode_counts.keys()):
        print(f"  {mode}: {mode_counts[mode]}")
    print()

    # =================================================================
    # Report: unknown_pending_review
    # =================================================================
    upr_entries = [e for e in entries if e.get("license") == "unknown_pending_review"]
    print(f"=== License: unknown_pending_review ({len(upr_entries)}) ===")
    for e in upr_entries:
        print(f"  {e.get('id')}: {e.get('title')} (mode: {e.get('acquisition_mode')})")
    print()

    # =================================================================
    # Report: missing upstream URLs
    # =================================================================
    missing_upstream = [e for e in entries if not e.get("upstream")]
    print(f"=== Missing Upstream URLs ({len(missing_upstream)}) ===")
    if missing_upstream:
        for e in missing_upstream:
            print(f"  {e.get('id')} ({e.get('acquisition_mode')})")
    else:
        print("  (none)")
    print()

    # =================================================================
    # Report: missing license_evidence_url (warning only)
    # =================================================================
    missing_evidence = [
        e for e in entries
        if not e.get("license_evidence_url")
        and e.get("license") != "unknown_pending_review"
        and e.get("license") is not None
    ]
    print(f"=== Missing license_evidence_url ({len(missing_evidence)}) ===")
    if missing_evidence:
        for e in missing_evidence:
            print(f"  {e.get('id')}: license={e.get('license')} (mode: {e.get('acquisition_mode')})")
    else:
        print("  (none)")
    print()

    # =================================================================
    # Report: metadata_only entries
    # =================================================================
    metadata = [e for e in entries if e.get("acquisition_mode") == "metadata_only"]
    print(f"=== Metadata-Only Entries ({len(metadata)}) ===")
    for e in metadata:
        notes = e.get("notes", "")
        print(f"  {e.get('id')}: {e.get('title')}")
        if notes:
            print(f"    notes: {notes}")
        else:
            print(f"    (no routing notes)")
    print()

    # =================================================================
    # Report: defer entries
    # =================================================================
    deferred = [e for e in entries if e.get("acquisition_mode") == "defer"]
    print(f"=== Deferred Entries ({len(deferred)}) ===")
    if deferred:
        for e in deferred:
            print(f"  {e.get('id')}: {e.get('title')}")
    else:
        print("  (none)")
    print()

    # =================================================================
    # Report: sources.lock.yaml state
    # =================================================================
    print("=== Sources Lock State ===")
    if len(lock_sources) == 0:
        print("  sources.lock.yaml: sources: [] (no acquired sources)")
    else:
        print(f"  sources.lock.yaml: {len(lock_sources)} acquired source(s)")
        for s in lock_sources:
            print(f"    {s.get('source_id')}: {s.get('acquisition_mode')}")
    print()

    # =================================================================
    # Report: sources/upstream/ state
    # =================================================================
    upstream_dir = repo_root / "sources" / "upstream"
    print("=== sources/upstream/ State ===")
    if upstream_dir.exists():
        contents = sorted(upstream_dir.iterdir())
        names = {p.name for p in contents}
        if names == {".gitkeep"}:
            print("  sources/upstream/: only .gitkeep (no local source content)")
        else:
            for p in contents:
                print(f"  {p.name}")
    else:
        print("  sources/upstream/: directory does not exist")
        errors.append("sources/upstream/ directory does not exist")
    print()

    # =================================================================
    # Report: Index cross-reference consistency
    # =================================================================
    print("=== Index Cross-Reference Check ===")
    missing_from_refs = index_ids - ref_ids
    if missing_from_refs:
        for sid in sorted(missing_from_refs):
            msg = f"Index references source_id '{sid}' not found in references.yaml"
            errors.append(msg)
            print(f"  ERROR: {msg}")
    else:
        print("  All index planned_source_ids match references.yaml entries.")
    print()

    # =================================================================
    # Report: Unused source IDs (warning only)
    # =================================================================
    print("=== Unused Source IDs ===")
    unused = ref_ids - index_ids
    if unused:
        for sid in sorted(unused):
            entry = ref_by_id.get(sid, {})
            mode = entry.get("acquisition_mode", "?")
            warnings.append(f"source_id '{sid}' ({mode}) is not referenced by any index")
            print(f"  {sid} ({mode}): not referenced by any index")
    else:
        print("  All reference IDs are used by at least one index.")
    print()

    # =================================================================
    # Mechanical error checks
    # =================================================================
    for s in lock_sources:
        mode = s.get("acquisition_mode")
        if mode not in LOCK_ACQUISITION_MODES:
            sid = s.get("source_id", "?")
            errors.append(
                f"sources.lock.yaml contains non-acquired mode '{mode}' "
                f"for source_id '{sid}'; only {sorted(LOCK_ACQUISITION_MODES)} are permitted"
            )

    for e in entries:
        if e.get("acquisition_mode") == "link_only" and not e.get("upstream"):
            errors.append(f"link_only entry '{e.get('id')}' has no upstream URL")

    if upstream_dir.exists():
        allowed_lock_dirs = set()
        for s in lock_sources:
            local_path = s.get("local_path", "")
            prefix = "sources/upstream/"
            if local_path.startswith(prefix):
                dir_name = local_path[len(prefix):]
                if dir_name and "/" not in dir_name:
                    allowed_lock_dirs.add(dir_name)
        allowed = {".gitkeep"} | allowed_lock_dirs
        for p in upstream_dir.iterdir():
            if p.name not in allowed:
                errors.append(f"Unexpected file in sources/upstream/: {p.name}")

    # =================================================================
    # Output summary
    # =================================================================
    if warnings:
        print("=== Warnings ===")
        for w in warnings:
            print(f"  {w}")
        print()

    if errors:
        print("=== Errors ===")
        for e in errors:
            print(f"  {e}")
        print()
        print("UPDATE CHECK FAILED", file=sys.stderr)
        return 1

    print("Update check passed. Repository is internally consistent.")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Check upstream updates and lock-policy consistency"
    )
    parser.add_argument(
        "--online",
        action="store_true",
        help="Online upstream checks (reserved for future reviewed implementation)",
    )
    args = parser.parse_args()

    if args.online:
        print(
            "Online upstream checks are not implemented in this script.\n"
            "Use the dedicated online link checker instead:\n"
            "  python3 scripts/check_links_online.py --help"
        )
        return 0

    repo_root = find_repo_root()
    return run(repo_root)


if __name__ == "__main__":
    sys.exit(main())
