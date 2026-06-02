# Stage 5: Online Link Checking and CI Validation

## Context

Stage 4 (Lightweight Update-Review Scaffolding) completed offline validation. Stage 5 adds online link checking and completes the CI validation pipeline by ensuring the export_opencode_skill pipeline is tested in CI.

## Scope

### 1. CI Validation for export_opencode_skill.py

**Current state**: `.github/workflows/validate.yml` does NOT run `scripts/export_opencode_skill.py`.

**Change**: Add a new step after `verify_export_bundle.py` and before unittest discovery:
```yaml
- name: Export OpenCode skill bundle
  run: python3 scripts/export_opencode_skill.py
```

### 2. scripts/check_links_online.py

**Purpose**: Report-only URL checker for references.yaml upstream and license_evidence_url fields.

**HTTP Strategy** (urllib stdlib):
- Prefer `HEAD` requests
- Fall back to `GET` only for: `403`, `405`, `501`, or method-related `HTTPError`
- Treat `404` and most `5xx` as failures (no GET fallback)
- urllib follows redirects automatically; detect by comparing `response.geturl()` with original URL

**Failure Policy by Field**:
- `upstream` for `link_only` entries: default exit 1 on unreachable
- `license_evidence_url`: warning-only (no exit 1)
- `--no-fail`: always exit 0 after printing/writing report

**Report Schema** (--report flag, opt-in):
```yaml
- source_id: string
  field: upstream | license_evidence_url
  original_url: string
  final_url: string
  http_status: int | null
  status: ok | redirect | unreachable | error
  redirected: boolean
  error: string | null
  checked_at: ISO-8601
```

**CLI**:
```
python3 scripts/check_links_online.py [--no-fail] [--report] [--timeout SECONDS] [--help]
```

**Default behavior**: Print human-readable stdout summary. `--report` writes `reports/links-check.yaml`.

### 3. Offline Tests (tests/test_check_links_online.py)

- Use `unittest.mock.patch` to mock urllib (no real HTTP)
- Test: successful HEAD, successful GET fallback (405), 404 failure, redirect detection, license_evidence_url warning-only, --no-fail exit 0, --report file writing
- Follow existing test patterns: unittest.TestCase, subprocess.run for integration

### 4. CI Workflow (check-upstream-links.yml)

- Triggers: monthly schedule + workflow_dispatch
- Runs: `python3 scripts/check_links_online.py --no-fail --report`
- Uploads: `reports/links-check.yaml` as artifact
- Does NOT fail the workflow

### 5. Downstream /ref-bio Trial

Validate the user-facing wrapper:
```bash
./install-opencode.sh --project /tmp/ref-bio-downstream-trial
./install-opencode.sh --project /tmp/ref-bio-downstream-trial --dry-run --verbose
./install-opencode.sh --project /tmp/ref-bio-downstream-trial --update
./install-opencode.sh --project /tmp/ref-bio-downstream-trial --uninstall
```

**Required installed files**:
- SKILL.md
- reference-pack/AGENTS.reference.md
- reference-pack/references.link-only.yaml
- reference-pack/indexes/
- reference-pack/policies/
- reference-pack/MANIFEST.yaml

**Forbidden directories**: sources/, acquisition/, exports/, reports/, .git/, node_modules/

### 6. PLAN.md Update

Add Stage 5 section documenting completed work.

### 7. check_upstream_updates.py Stub Update

Update `--online` stub message to point users to:
```
python3 scripts/check_links_online.py --help
```

Do NOT make `--online` run network checks automatically.

## Safety Constraints

- Do NOT modify: references.yaml, sources.lock.yaml, indexes/, license fields, source priorities, acquisition modes, upstream URLs
- Do NOT vendor/download upstream documents
- Do NOT parse or summarize scientific guidance
- Do NOT add submodules
- Do NOT commit generated exports/ or reports/
- Tests for check_links_online.py must be offline only (mocks or local HTTP server)
