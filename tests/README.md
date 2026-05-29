# Tests

Future tests should verify repository mechanics, including schemas, policy file presence, prompt templates, forbidden file types, and privacy hygiene.

Tests must not encode scientific best-practice summaries.

## test_metadata_validation.py

Run: `python3 -m unittest tests/test_metadata_validation.py`

Tests that the validation script passes against the current repository state.

## test_repo_hygiene.py

Run: `python3 -m unittest tests/test_repo_hygiene.py`

Tests that the repository hygiene scanner passes against the current repository state.
