#!/usr/bin/env python3
"""
Build a release manifest for the link-only export bundle.

Walks exports/project-reference/, computes SHA-256 hashes and sizes,
and writes MANIFEST.yaml. Excludes MANIFEST.yaml itself from the
hashed file list to avoid self-referential instability.

Does not include timestamps, machine paths, usernames, or absolute paths.
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


def find_repo_root():
    path = Path(__file__).resolve().parent.parent
    if not (path / "references.yaml").exists():
        print("ERROR: Cannot find repository root (references.yaml not found).", file=sys.stderr)
        sys.exit(1)
    return path


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def write_yaml(path, data):
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def compute_sha256(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(HASH_CHUNK_SIZE)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def posix_relpath(path, base):
    """Return a POSIX-style relative path (forward slashes)."""
    return Path(path).relative_to(base).as_posix()


def build_release_manifest(repo_root=None):
    if repo_root is None:
        repo_root = find_repo_root()

    export_dir = repo_root / "exports" / "project-reference"

    if not export_dir.exists():
        print(
            "ERROR: exports/project-reference/ does not exist. "
            "Run export_project_reference.py first.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Load source_count from references.link-only.yaml
    refs_path = export_dir / "references.link-only.yaml"
    if not refs_path.exists():
        print(
            "ERROR: references.link-only.yaml not found in export directory.",
            file=sys.stderr,
        )
        sys.exit(1)

    refs_data = load_yaml(refs_path)
    source_count = len(refs_data.get("entries", []))

    # Walk files, excluding MANIFEST.yaml itself
    file_entries = []
    for root, dirs, files in os.walk(export_dir):
        dirs.sort()
        for fname in sorted(files):
            if fname == MANIFEST_NAME:
                continue
            fpath = Path(root) / fname
            rel = posix_relpath(fpath, export_dir)
            file_entries.append({
                "path": rel,
                "sha256": compute_sha256(fpath),
                "size_bytes": fpath.stat().st_size,
            })

    manifest = {
        "schema_version": "0.1",
        "generated_from": "bio-agent-reference-pack",
        "export_type": "link_only_project_reference",
        "includes_upstream_source_files": False,
        "source_count": source_count,
        "files": file_entries,
    }

    manifest_path = export_dir / MANIFEST_NAME
    write_yaml(manifest_path, manifest)

    print(f"Wrote MANIFEST.yaml with {len(file_entries)} files, source_count={source_count}")
    return manifest_path


def main():
    build_release_manifest()


if __name__ == "__main__":
    main()
