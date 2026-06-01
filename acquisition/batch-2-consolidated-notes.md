# Stage 2 — Lightweight Completion Notes

## Summary

Stage 2 was completed in lightweight/on-demand form. An earlier over-broad acquisition pass that vendored 39 package source trees under `sources/upstream/` (32 MB) has been slimmed down to match the repository's intended design: a source-first, license-aware routing/reference pack, not an archive museum of downloaded package source trees.

## Final Tally

| Category | Count |
|----------|-------|
| `references.yaml` entries | 55 |
| `sources.lock.yaml` acquired entries | 0 |
| `link_only` entries | 50 |
| `metadata_only` entries | 4 |
| `defer` entries | 1 |
| `sources/upstream/` content | `.gitkeep` only |

No local source content is vendored. No `.gitmodules` exists. `git submodule status` is empty.

## Slim-Down Rationale

The central repository should keep metadata, source IDs, upstream URLs, license evidence, policies, schemas, scripts, and reading maps. It should not vendor package repositories by default.

Most real upstream sources are `link_only` and read on demand by agents from official upstream URLs. The registry (`references.yaml`) remains the complete 55-entry reference catalog with preserved license strings and evidence URLs.

## Notable Governance Decisions

- `nichenet` remains the stable source ID. The upstream URL may point to the `nichenetr` repository.
- `banksy` remains `link_only` because its license is non-standard (MIT for academic, restrictions for commercial).
- Platform/documentation sources without clear redistribution terms remain `link_only`.
- All license strings were verified from raw upstream files (LICENSE, DESCRIPTION, pyproject.toml) and are preserved verbatim.
- If a future project requires local acquisition, the existing `pinned_vendor_snapshot` schema and manifest format can be used to re-acquire sources under a strict snapshot policy.
