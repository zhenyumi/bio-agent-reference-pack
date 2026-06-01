# Tests

Tests verify repository mechanics, including schemas, policy file presence, forbidden file types, and privacy hygiene.

Tests must not encode scientific best-practice summaries.

## test_metadata_validation.py

Run: `python3 -m unittest tests/test_metadata_validation.py`

Tests that the validation script passes against the current repository state.

## test_repo_hygiene.py

Run: `python3 -m unittest tests/test_repo_hygiene.py`

Tests that the repository hygiene scanner passes against the current repository state. Includes regression tests ensuring secrets in comment lines, absolute paths, and clean files are handled correctly by the scanner.

## test_check_upstream_updates.py

Run: `python3 -m unittest tests/test_check_upstream_updates.py`

Tests that the upstream update check script runs successfully against the current repository state. Verifies that stdout includes mode counts, `unknown_pending_review` summary, `sources.lock.yaml` empty state, and `sources/upstream/` `.gitkeep`-only confirmation.

## test_export_pipeline.py

Run: `python3 -m unittest tests/test_export_pipeline.py`

End-to-end integration test that runs the full export pipeline (build_link_catalog, export_project_reference, build_release_manifest, verify_export_bundle) and asserts:
- verifier passes on the generated bundle
- key output files exist
- exported references contain only allowed fields (no leaked local_path, version, or acquisition metadata)
- forbidden directories (sources/, acquisition/) are absent
- manifest declares includes_upstream_source_files: false
- verifier catches tampered hashes, extra files, and forbidden directories

## test_opencode_skill_export.py

Run: `python3 -m unittest tests/test_opencode_skill_export.py`

Tests that `scripts/export_opencode_skill.py` creates the `/ref-bio` skill
bundle with `SKILL.md`, a lightweight `reference-pack/`, indexes, policies, and
no forbidden source/acquisition/export directories.

## test_opencode_skill_install.py

Run: `python3 -m unittest tests/test_opencode_skill_install.py`

Tests that `scripts/install_opencode_skill.py` supports dry runs, installs into
a temporary downstream project, refuses accidental overwrite, supports
`--force`, and does not install forbidden source/acquisition/export directories.

## test_install_opencode_sh.py

Run: `python3 -m unittest tests/test_install_opencode_sh.py`

Tests that `install-opencode.sh` behaves correctly:

- Shows help on `--help` and no-args
- Lists `ref-bio` and `/ref-bio` on `--list`
- Runs validation checks on `--validate`
- Installs the skill on `--project`
- Does not write on `--dry-run`
- Supports `--target` as alias for `--project`
- Overwrites on `--project ... --force`
- Reports error on `--update` when not installed
- Removes only `.opencode/skills/ref-bio/` on `--uninstall`, preserving other
  `.opencode/` files
