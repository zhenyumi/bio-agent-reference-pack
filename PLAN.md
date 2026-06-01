# PLAN

This plan records the current state of `bio-agent-reference-pack` after the Stage 2 lightweight completion and Stage 3 reading-map phase. The repository is now a source-first, license-aware routing/reference pack. No package source trees are vendored locally.

## 1. Governance and Scope

- Original upstream sources are authoritative.
- `indexes/` files are routing aids only and must not summarize scientific guidance.
- `policies/` constrain agent behavior but do not replace upstream materials.
- `PLAN.md`, `AGENTS.md`, `.codex/`, and `.opencode/` are intentional project files.
- Future source-priority, license, or acquisition-mode changes require review before execution.

## 2. Current Metadata State

- `references.yaml`: 55 entries.
- `sources.lock.yaml`: 0 acquired entries (`sources: []`).
- `sources/upstream/`: only `.gitkeep` (no local source content).
- `.gitmodules`: absent.
- `git submodule status`: empty.

## 3. Acquisition Modes

| Mode | Count | Meaning |
|------|-------|---------|
| `link_only` | 50 | Official URL recorded; no source files acquired. Agents read upstream documentation on demand. |
| `metadata_only` | 4 | Routing entry only; points agents toward related link-only sources. |
| `defer` | 1 | Deferred until a concrete project need or clearer upstream scope exists. |
| `git_submodule` | 0 | Not used in current state. |
| `pinned_vendor_snapshot` | 0 | Not used in current state. |
| `do_not_include` | 0 | Excluded from this pack. |

## 4. Stage 2 Acquisition Outcome (Lightweight)

Stage 2 was completed in lightweight/on-demand form. An earlier over-broad acquisition attempt that vendored 39 package source trees under `sources/upstream/` was slimmed down to match the repository's intended design: a reference pack, not an archive museum.

All real upstream sources are now `link_only` with reviewed status. License strings and evidence URLs are preserved from the original license verification pass. No commit hashes, local paths, or snapshot manifests remain.

Agents should read upstream official documentation on demand using `references.yaml` and indexes.

## 5. Link-Only Sources (50)

All actual upstream package/documentation/agent sources are recorded as `link_only`. A full list with upstream URLs, licenses, and reading priority is maintained in `references.yaml` and `LICENSES.md`.

## 6. Metadata-Only Sources (4)

seurat-integration, seurat-reference-mapping, seurat-spatial, pseudobulk-de-guidance

## 7. Deferred Sources (1)

gptomics-bioskills

## 8. Stable Identifiers

- `nichenet` remains the stable source ID. The upstream URL may point to the `nichenetr` repository.
- No `nichenetr` source ID exists in the registry, indexes, or lock file.

## 9. Validation and CI

Current validation covers metadata, repository hygiene, and export pipeline:

- `scripts/validate_metadata.py` validates YAML/JSON schema conformance, registry/index cross-references, lock entries, upstream directory contents, and `.gitmodules`/gitlink consistency.
- `scripts/scan_repo_hygiene.py --all` scans tracked and untracked files for secrets, private machine data, and forbidden extensions.
- The export pipeline (`export_project_reference.py`, `build_release_manifest.py`, `verify_export_bundle.py`) produces a link-only project reference bundle for downstream projects.

## 10. Reading Maps (Stage 3)

- Core official docs/guides are `must_read` or `optional_read`.
- Platform/product docs and project-specific sources are `optional_read` or `project_specific_read`.
- Metadata-only and deferred entries are `project_specific_read`.
- Indexes remain routing maps only; they are not scientific guidance.
- `policies/agent-reading-protocol.md` directs agents to retrieve upstream documentation on demand rather than relying on vendored local copies.

## 11. Stage 4 – Lightweight Update-Review Scaffolding (Current)

Update checks are now local, deterministic, and safe by default:

- `scripts/check_upstream_updates.py` reports repository state without network access, URL fetching, source downloads, or git clones.
- Upstream changes are visible through metadata reports (mode counts, license status, missing URLs, index cross-references, unused IDs), not silently applied to downstream projects.
- Any future change to source versions, source priority, license fields, or acquisition modes requires review before implementation.
- The `--online` flag is reserved for future reviewed implementation; currently it only prints a stub message and exits.
- CI runs `check_upstream_updates.py` after metadata validation and hygiene scan, before export generation.

## 12. Next Phase

After Stage 4 is reviewed and committed, future phases may:

- Build downstream project reference bundles using the link-only catalog and the existing export pipeline.
- Implement reviewed online update checks under the `--online` flag (requires Codex/review approval before any network code is added).
- Re-acquire sources under a strict snapshot policy if a future project requires local acquisition, reusing the existing `pinned_vendor_snapshot` schema and manifest format.

## Stage 2 Acceptance Criteria

- `references.yaml` entries have correct modes (50 link_only, 4 metadata_only, 1 defer).
- `sources.lock.yaml` has `sources: []`.
- `sources/upstream/` contains only `.gitkeep`.
- `.gitmodules` is absent and `git submodule status` is empty.
- All license strings and evidence URLs are preserved verbatim.
- No commit hashes, local paths, or snapshot manifests remain in metadata files.
- The full verification command set passes.
- No commit is made until review approves the resulting diff.
