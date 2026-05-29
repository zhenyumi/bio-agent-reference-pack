# Tests

Future tests should verify repository mechanics, including schemas, policy file presence, prompt templates, forbidden file types, and privacy hygiene.

Tests must not encode scientific best-practice summaries.

## test_metadata_validation.py

Run: `python3 -m unittest tests/test_metadata_validation.py`

Tests that the validation script passes against the current repository state.

## test_repo_hygiene.py

Run: `python3 -m unittest tests/test_repo_hygiene.py`

Tests that the repository hygiene scanner passes against the current repository state.

## test_link_catalog.py

Run: `python3 -m unittest tests/test_link_catalog.py`

Tests that `build_link_catalog.py` produces a catalog with exactly 16 reviewed link-only entries and no planned entries.

## test_export_project_reference.py

Run: `python3 -m unittest tests/test_export_project_reference.py`

Tests that `export_project_reference.py` produces the expected export structure and excludes `sources/upstream/` and `acquisition/`.

## test_release_manifest.py

Run: `python3 -m unittest tests/test_release_manifest.py`

Tests that `build_release_manifest.py` produces a valid MANIFEST.yaml with correct fields, hashes, sizes, and no absolute paths.

## test_verify_export_bundle.py

Run: `python3 -m unittest tests/test_verify_export_bundle.py`

Tests that `verify_export_bundle.py` passes on a valid bundle and correctly fails on missing manifest, tampered hashes, and forbidden directories.
