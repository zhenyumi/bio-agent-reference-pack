# Scripts

Future scripts should perform narrow mechanical checks, such as schema validation, forbidden-file detection, privacy scanning, and lock-file consistency checks.

Scripts must not summarize scientific guidelines or decide source priority, license status, or redistribution rights.

## validate_metadata.py

Run: `python3 scripts/validate_metadata.py`

Validates:

- YAML metadata files parse correctly
- JSON schema files parse correctly
- Reference IDs in `references.yaml` are unique
- `planned_source_ids` in all `indexes/*.yaml` files reference valid reference IDs
- `sources.lock.yaml` acquired sources reference valid reference IDs
- `sources/upstream/` contains only `.gitkeep`
- Required project-control paths are not git-ignored
