#!/usr/bin/env python3
"""
Deterministic local validation for bio-agent-reference-pack metadata.

Checks:
- YAML metadata files parse correctly
- JSON schema files parse correctly
- Reference IDs in references.yaml are unique
- planned_source_ids in indexes reference valid reference IDs
- sources.lock.yaml acquired sources reference valid reference IDs
- sources/upstream/ contains only .gitkeep
- Required project-control paths are not git-ignored
"""

import json
import os
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required for YAML parsing.", file=sys.stderr)
    print("Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def find_repo_root():
    """Find the repository root by looking for references.yaml."""
    path = Path(__file__).resolve().parent.parent
    if not (path / "references.yaml").exists():
        print("ERROR: Cannot find repository root (references.yaml not found).", file=sys.stderr)
        sys.exit(1)
    return path


def load_yaml(path):
    """Load and return a YAML file."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path):
    """Load and return a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_unique_reference_ids(repo_root, errors):
    """Check that all reference IDs in references.yaml are unique."""
    refs_path = repo_root / "references.yaml"
    data = load_yaml(refs_path)
    entries = data.get("entries", [])
    seen = set()
    for entry in entries:
        ref_id = entry.get("id")
        if ref_id in seen:
            errors.append(f"Duplicate reference ID in references.yaml: {ref_id}")
        seen.add(ref_id)
    return seen


def check_index_source_ids(repo_root, ref_ids, errors):
    """Check that all planned_source_ids in indexes exist in references.yaml."""
    indexes_dir = repo_root / "indexes"
    for yaml_file in sorted(indexes_dir.glob("*.yaml")):
        data = load_yaml(yaml_file)
        # package-map uses "packages", others use different keys
        for key in ("topics", "workflow_stages", "packages"):
            items = data.get(key, [])
            for item in items:
                source_ids = item.get("planned_source_ids", [])
                for sid in source_ids:
                    if sid not in ref_ids:
                        errors.append(
                            f"Index {yaml_file.name}: planned_source_id '{sid}' "
                            f"not found in references.yaml"
                        )


def check_sources_lock(repo_root, ref_ids, errors):
    """Check that sources.lock.yaml acquired sources reference valid IDs."""
    lock_path = repo_root / "sources.lock.yaml"
    data = load_yaml(lock_path)
    sources = data.get("sources", [])
    for source in sources:
        sid = source.get("source_id")
        if sid not in ref_ids:
            errors.append(
                f"sources.lock.yaml: source_id '{sid}' not found in references.yaml"
            )


def check_upstream_dir(repo_root, errors):
    """Check that sources/upstream/ contains only .gitkeep."""
    upstream_dir = repo_root / "sources" / "upstream"
    if not upstream_dir.exists():
        errors.append("sources/upstream/ directory does not exist")
        return
    allowed = {".gitkeep"}
    for item in sorted(upstream_dir.iterdir()):
        if item.name not in allowed:
            errors.append(
                f"sources/upstream/ contains unexpected file: {item.name}"
            )


def check_git_not_ignored(repo_root, errors):
    """Check that required project-control paths are not git-ignored."""
    required_paths = [
        "PLAN.md",
        "AGENTS.md",
        "references.yaml",
        "sources.lock.yaml",
        "indexes/",
        "policies/",
        "schemas/",
        "scripts/",
        "tests/",
        ".codex/",
        ".opencode/",
    ]
    for rel_path in required_paths:
        result = subprocess.run(
            ["git", "check-ignore", rel_path],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            # returncode 0 means the path IS ignored
            errors.append(
                f"Required path '{rel_path}' is git-ignored. "
                f"Check .gitignore exclusions."
            )
        elif result.returncode == 1:
            # returncode 1 means the path is NOT ignored - this is correct
            pass
        else:
            # Any other returncode is a command error
            stderr_msg = result.stderr.strip() if result.stderr else "unknown error"
            errors.append(
                f"git check-ignore failed for '{rel_path}': {stderr_msg}"
            )


def validate(repo_root=None):
    """Run all validation checks. Returns list of errors (empty = pass)."""
    if repo_root is None:
        repo_root = find_repo_root()
    errors = []

    # Check YAML files parse
    yaml_files = [
        repo_root / "references.yaml",
        repo_root / "sources.lock.yaml",
    ] + sorted((repo_root / "indexes").glob("*.yaml"))

    for yf in yaml_files:
        try:
            load_yaml(yf)
        except Exception as e:
            errors.append(f"Failed to parse {yf.name}: {e}")

    # Check JSON schema files parse
    schemas_dir = repo_root / "schemas"
    for jf in sorted(schemas_dir.glob("*.json")):
        try:
            load_json(jf)
        except Exception as e:
            errors.append(f"Failed to parse {jf.name}: {e}")

    if errors:
        return errors

    # Check unique reference IDs
    ref_ids = check_unique_reference_ids(repo_root, errors)

    # Check index cross-references
    check_index_source_ids(repo_root, ref_ids, errors)

    # Check sources.lock.yaml consistency
    check_sources_lock(repo_root, ref_ids, errors)

    # Check upstream directory
    check_upstream_dir(repo_root, errors)

    # Check git ignore status
    check_git_not_ignored(repo_root, errors)

    return errors


def main():
    repo_root = find_repo_root()
    errors = validate(repo_root)

    if errors:
        print("VALIDATION FAILED", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    print("All metadata validation checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
