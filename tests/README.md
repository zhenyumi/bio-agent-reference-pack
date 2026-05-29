# Tests

Tests verify repository mechanics, including schemas, policy file presence, forbidden file types, and privacy hygiene.

Tests must not encode scientific best-practice summaries.

## test_metadata_validation.py

Run: `python3 -m unittest tests/test_metadata_validation.py`

Tests that the validation script passes against the current repository state.

## test_repo_hygiene.py

Run: `python3 -m unittest tests/test_repo_hygiene.py`

Tests that the repository hygiene scanner passes against the current repository state. Includes regression tests ensuring secrets in comment lines, absolute paths, and clean files are handled correctly by the scanner.

## test_export_pipeline.py

Run: `python3 -m unittest tests/test_export_pipeline.py`

End-to-end integration test that runs the full export pipeline (build_link_catalog, export_project_reference, build_release_manifest, verify_export_bundle) and asserts:
- verifier passes on the generated bundle
- key output files exist
- exported references contain only allowed fields (no leaked local_path, version, or acquisition metadata)
- forbidden directories (sources/, acquisition/) are absent
- manifest declares includes_upstream_source_files: false
- verifier catches tampered hashes, extra files, and forbidden directories
