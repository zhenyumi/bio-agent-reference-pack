# Scripts

Future scripts should perform narrow mechanical checks, such as schema validation, forbidden-file detection, privacy scanning, and lock-file consistency checks.

Scripts must not summarize scientific guidelines or decide source priority, license status, or redistribution rights.

## validate_metadata.py

Run: `python3 scripts/validate_metadata.py`

Validates:

- YAML metadata files parse correctly
- JSON schema files parse correctly
- YAML files conform to their JSON schemas
- Reference IDs in `references.yaml` are unique
- `planned_source_ids` in all `indexes/*.yaml` files reference valid reference IDs
- `sources.lock.yaml` acquired sources reference valid reference IDs
- `sources/upstream/` contains only `.gitkeep`
- Required project-control paths are not git-ignored

## scan_repo_hygiene.py

Run: `python3 scripts/scan_repo_hygiene.py`

Scans tracked files for:

- Forbidden binary/archive extensions (`.pdf`, `.zip`, `.tar`, `.tar.gz`, `.tgz`, `.7z`, `.rar`)
- High-confidence secret tokens (OpenAI, GitHub, GitLab, AWS formats)
- Private IP addresses (10.x, 172.16-31.x, 192.168.x)
- Localhost and private URLs
- Absolute home directory paths (POSIX and Windows formats)
- Unexpected files under `sources/upstream/` other than `.gitkeep`

Add `--all` to also scan untracked non-ignored files:

    python3 scripts/scan_repo_hygiene.py --all
