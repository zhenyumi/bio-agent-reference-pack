#!/usr/bin/env python3
"""
Verify the link-only export bundle integrity.

Checks:
- Required files/directories exist
- Forbidden directories (sources/, acquisition/) are absent
- references.link-only.yaml has only allowed fields and non-null upstream
- MANIFEST.yaml file hashes and sizes match current files
- No absolute local paths in manifest

Accepts optional CLI argument: path to export directory.
Default: exports/project-reference/
"""

import hashlib
import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required.", file=sys.stderr)
    print("Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

MANIFEST_NAME = "MANIFEST.yaml"
HASH_CHUNK_SIZE = 65536

REQUIRED_FILES = [
    "AGENTS.reference.md",
    "references.link-only.yaml",
    "MANIFEST.yaml",
]

REQUIRED_DIRS = [
    "policies",
    "indexes",
]

FORBIDDEN_DIRS = [
    "sources",
    "acquisition",
]

ALLOWED_REF_FIELDS = {"source_id", "title", "source_type", "upstream", "license", "notes"}


def find_repo_root():
    path = Path(__file__).resolve().parent.parent
    if not (path / "references.yaml").exists():
        print("ERROR: Cannot find repository root (references.yaml not found).", file=sys.stderr)
        sys.exit(1)
    return path


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def compute_sha256(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(HASH_CHUNK_SIZE)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def has_absolute_path(p):
    """Check if a path string is absolute or contains dangerous components."""
    # POSIX absolute
    if p.startswith("/"):
        return True
    # Windows drive letter
    if len(p) >= 2 and p[1] == ":":
        return True
    # Path traversal
    parts = Path(p).parts
    if ".." in parts:
        return True
    return False


def verify_export_bundle(export_dir=None):
    errors = []

    if export_dir is None:
        repo_root = find_repo_root()
        export_dir = repo_root / "exports" / "project-reference"
    else:
        export_dir = Path(export_dir)

    if not export_dir.exists():
        print(f"ERROR: Export directory does not exist: {export_dir}", file=sys.stderr)
        sys.exit(1)

    # Check required files
    for rel in REQUIRED_FILES:
        p = export_dir / rel
        if not p.exists():
            errors.append(f"Required file missing: {rel}")

    # Check required directories
    for rel in REQUIRED_DIRS:
        p = export_dir / rel
        if not p.is_dir():
            errors.append(f"Required directory missing: {rel}")

    # Check forbidden directories
    for rel in FORBIDDEN_DIRS:
        p = export_dir / rel
        if p.exists():
            errors.append(f"Forbidden directory present: {rel}")

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(1)

    # Verify references.link-only.yaml
    refs_path = export_dir / "references.link-only.yaml"
    refs_data = load_yaml(refs_path)
    for entry in refs_data.get("entries", []):
        sid = entry.get("source_id", "unknown")
        extra = set(entry.keys()) - ALLOWED_REF_FIELDS
        if extra:
            errors.append(f"Entry '{sid}' has extra fields: {extra}")
        if entry.get("upstream") is None:
            errors.append(f"Entry '{sid}' has null upstream")

    # Verify MANIFEST.yaml
    manifest_path = export_dir / MANIFEST_NAME
    if not manifest_path.exists():
        errors.append("MANIFEST.yaml not found")
    else:
        manifest = load_yaml(manifest_path)

        # Validate no absolute paths
        for file_entry in manifest.get("files", []):
            p = file_entry.get("path", "")
            if has_absolute_path(p):
                errors.append(f"Manifest has absolute or dangerous path: {p}")

        # Build set of manifest-listed paths
        manifest_paths = set()

        # Validate hashes and sizes
        for file_entry in manifest.get("files", []):
            rel = file_entry.get("path", "")
            manifest_paths.add(rel)
            expected_hash = file_entry.get("sha256", "")
            expected_size = file_entry.get("size_bytes", -1)

            actual_path = export_dir / rel
            if not actual_path.exists():
                errors.append(f"Manifest references missing file: {rel}")
                continue

            actual_hash = compute_sha256(actual_path)
            actual_size = actual_path.stat().st_size

            if actual_hash != expected_hash:
                errors.append(f"Hash mismatch for {rel}")
            if actual_size != expected_size:
                errors.append(f"Size mismatch for {rel}: expected {expected_size}, got {actual_size}")

        # Collect actual files in export dir, excluding MANIFEST.yaml
        actual_files = set()
        for root, dirs, files in os.walk(export_dir):
            dirs.sort()
            for fname in sorted(files):
                if fname == MANIFEST_NAME:
                    continue
                fpath = Path(root) / fname
                rel = fpath.relative_to(export_dir).as_posix()
                actual_files.add(rel)

        # Check for files not listed in manifest
        unlisted = actual_files - manifest_paths
        for rel in sorted(unlisted):
            errors.append(f"Export file not listed in manifest: {rel}")

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(1)

    print("Export bundle verification passed.")
    return True


def main():
    export_dir = sys.argv[1] if len(sys.argv) > 1 else None
    verify_export_bundle(export_dir)


if __name__ == "__main__":
    main()
