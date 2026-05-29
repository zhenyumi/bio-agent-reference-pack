# PLAN

This plan initializes a durable reference-pack foundation before any upstream sources are acquired.

## 1. Governance and Scope

- Define the repository as source-first and license-aware.
- Keep original upstream sources authoritative.
- Separate Codex planning/review work from OpenCode scoped execution work.
- Prevent summaries, inferred best practices, or unreviewed source-priority decisions from entering the pack.

## 2. Metadata, Schemas, and Validation

- Maintain `references.yaml` as the planned source registry.
- Maintain `sources.lock.yaml` as the future acquisition lock file.
- Define JSON Schemas for references, lock entries, and topic maps.
- Add validation scripts only after the placeholder formats are reviewed.

## 3. Source Acquisition

- Add upstream material only after license and redistribution checks.
- Prefer official documentation URLs, release tags, commits, and package-version-specific sources.
- Vendor full text only when redistribution is permitted.
- Record acquisition mode, checked date, version or commit, license, and local path.

## 4. Reading Maps Instead of Summaries

- Use `indexes/` files to route agents to source IDs.
- Do not summarize scientific guidelines in indexes.
- Keep topic, package, and workflow-stage maps as navigation aids only.

## 5. Update, Locking, and CI

- Add update checks that report upstream changes without silently applying them to downstream projects.
- Lock acquired source versions in `sources.lock.yaml`.
- Add CI for schema validation, privacy checks, and forbidden file types.
- Keep review gates for license and source-priority changes.

## 6. Export to Downstream Projects

- Define a small export format for downstream bioinformatics analysis repositories.
- Include reading instructions, source IDs, and policy references.
- Let downstream project instructions override central pack guidance.

## 7. Iterative Review and Expansion

- Review every new source category before acquisition.
- Expand indexes only when source IDs and license metadata are ready.
- Keep the repository useful for weaker execution agents by making scope boundaries explicit.

## Initial Milestone Acceptance Criteria

- Required directory skeleton exists.
- `README.md`, `PLAN.md`, `AGENTS.md`, `.gitignore`, `references.yaml`, `sources.lock.yaml`, and `LICENSES.md` exist.
- Policy files exist and distinguish authoritative sources from navigation aids.
- Placeholder indexes exist and contain planned source IDs only.
- Schemas exist for future metadata validation.
- `.codex/` and `.opencode/` prompt areas are intentionally version-controlled.
- No upstream full text, PDFs, large archives, credentials, local machine paths, or private infrastructure details are added.
- No scientific guideline summaries are added.
- Git is initialized, but no commit is created.

## Future Reference-Source Checklist

- Single-cell best practices
- OSCA
- OSCA Advanced
- OSTA
- Seurat
- Bioconductor package vignettes
- scDblFinder
- DecontX/celda
- scuttle
- scran
- scater
- SingleCellExperiment
- clusterProfiler
- MAST
- SingleR
- LIANA
- CellChat
- monocle3
- renv
- GitHub Actions
- Codex AGENTS.md guidance
- OpenCode documentation
- GPTomics/bioSkills

