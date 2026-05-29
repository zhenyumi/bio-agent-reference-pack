#!/usr/bin/env python3
"""
Build a link-only reference catalog from reviewed references.

Selects entries from references.yaml where:
- status == reviewed
- acquisition_mode == link_only
- upstream is not null

Writes exports/link-catalog.yaml with only the allowed fields.
Fails if any selected entry has local_path or version set.
"""

import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required.", file=sys.stderr)
    print("Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


ALLOWED_FIELDS = {"source_id", "title", "source_type", "upstream", "license", "notes"}
RENAME_FIELDS = {"id": "source_id"}


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
    os.makedirs(path.parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def select_reviewed_link_only(entries):
    selected = []
    for entry in entries:
        if (
            entry.get("status") == "reviewed"
            and entry.get("acquisition_mode") == "link_only"
            and entry.get("upstream") is not None
        ):
            selected.append(entry)
    return selected


def build_catalog_entry(entry):
    catalog_entry = {}
    for key, value in entry.items():
        new_key = RENAME_FIELDS.get(key, key)
        if new_key in ALLOWED_FIELDS:
            catalog_entry[new_key] = value
    return catalog_entry


def validate_selected_entries(selected, errors):
    for entry in selected:
        source_id = entry.get("id", "unknown")
        if entry.get("local_path") is not None:
            errors.append(
                f"Entry '{source_id}' has local_path set. "
                f"Link-only catalog requires local_path to be null."
            )
        if entry.get("version") is not None:
            errors.append(
                f"Entry '{source_id}' has version set. "
                f"Link-only catalog requires version to be null."
            )


def build_link_catalog(repo_root=None):
    if repo_root is None:
        repo_root = find_repo_root()

    refs_path = repo_root / "references.yaml"
    data = load_yaml(refs_path)
    entries = data.get("entries", [])

    selected = select_reviewed_link_only(entries)

    errors = []
    validate_selected_entries(selected, errors)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(1)

    catalog_entries = [build_catalog_entry(e) for e in selected]

    catalog = {
        "schema_version": "0.1",
        "description": (
            "Link-only reference catalog. "
            "Entries link to upstream official URLs. "
            "No source content has been acquired."
        ),
        "entries": catalog_entries,
    }

    output_path = repo_root / "exports" / "link-catalog.yaml"
    write_yaml(output_path, catalog)

    print(f"Wrote {len(catalog_entries)} entries to exports/link-catalog.yaml")
    return output_path


def main():
    build_link_catalog()


if __name__ == "__main__":
    main()
