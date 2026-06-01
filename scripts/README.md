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
- `pinned_vendor_snapshot` manifests parse, match schema, and match disk hashes/sizes
- Snapshot contents stay inside the strict source/documentation-source allowlist
- `.gitmodules` and git index gitlinks match `git_submodule` entries in `sources.lock.yaml`
- `sources/upstream/` contains only `.gitkeep` and recorded acquisition directories
- Required project-control paths are not git-ignored

## scan_repo_hygiene.py

Run: `python3 scripts/scan_repo_hygiene.py`

Scans tracked files for:

- Forbidden binary/archive extensions (`.pdf`, `.zip`, `.tar`, `.tar.gz`, `.tgz`, `.7z`, `.rar`)
- High-confidence secret tokens (OpenAI, GitHub, GitLab, AWS formats)
- Private IP addresses (10.x, 172.16-31.x, 192.168.x)
- Localhost and private URLs
- Absolute home directory paths (POSIX and Windows formats)
- Unexpected files under `sources/upstream/` other than `.gitkeep` and recorded acquisition directories
- Forbidden raw/test/generated content inside acquired source directories

Add `--all` to also scan untracked non-ignored files:

    python3 scripts/scan_repo_hygiene.py --all

## check_upstream_updates.py

Run: `python3 scripts/check_upstream_updates.py`

Lightweight update-review and lock-policy check. Local, deterministic, safe by default.

Reports:
- Total references by `acquisition_mode`
- Entries with `license: unknown_pending_review`
- Entries missing upstream URLs or `license_evidence_url`
- `metadata_only` and `defer` entries with routing notes
- `sources.lock.yaml` state (empty or acquired)
- `sources/upstream/` state (`.gitkeep`-only or unexpected files)
- Index cross-reference consistency (`planned_source_ids` vs `references.yaml`)
- Unused source IDs (not referenced by any index)

Default behavior is offline only:
- No network access
- No URL fetching
- No source downloads
- No git clone
- No scientific summaries

Add `--online` for a reserved stub. Online upstream checks are intentionally not implemented in this lightweight stage.

Exit 0 for internal consistency. Exit 1 only for mechanical errors (invalid YAML, missing upstream for `link_only`, unexpected files in `sources/upstream/`). Warnings (missing evidence URLs, unused IDs) are reported but do not fail.

## build_link_catalog.py

Run: `python3 scripts/build_link_catalog.py`

Reads `references.yaml`, selects entries with `status: reviewed` and `acquisition_mode: link_only` and non-null `upstream`, and writes `exports/link-catalog.yaml`. Fails if any selected entry has `local_path` or `version` set.

## export_project_reference.py

Run: `python3 scripts/export_project_reference.py`

Exports a downstream-ready project reference bundle to `exports/project-reference/`. Includes `AGENTS.reference.md`, `references.link-only.yaml`, `policies/`, and `indexes/`. Does not include `sources/upstream/` or `acquisition/`.

## build_release_manifest.py

Run: `python3 scripts/build_release_manifest.py`

Builds a release manifest at `exports/project-reference/MANIFEST.yaml` with SHA-256 hashes and sizes for all files in the export bundle. Excludes `MANIFEST.yaml` itself from the file list. Requires the export bundle to already exist.

## verify_export_bundle.py

Run: `python3 scripts/verify_export_bundle.py`

Verifies the export bundle integrity: checks required files exist, forbidden directories are absent, reference entries have only allowed fields, and manifest hashes/sizes match current files. Accepts optional CLI argument for custom export directory path.
