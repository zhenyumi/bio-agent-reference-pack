# Batch 1 — Metadata Update Notes

This file documents the update of 16 Batch 1 source entries in `references.yaml` from `planned` to `reviewed` status.

## Update Summary

- **Date**: 2026-05-29
- **Sources updated**: 16
- **Status change**: planned → reviewed
- **Acquisition mode**: link_only (no source files acquired)
- **Evidence source**: `acquisition/batch-1-evidence.md`

## Per-Source Update Table

| Source ID | Field | Old Value | New Value |
|-----------|-------|-----------|-----------|
| single-cell-best-practices | status | planned | reviewed |
| single-cell-best-practices | upstream | null | https://www.sc-best-practices.org/ |
| single-cell-best-practices | license | null | unknown_pending_review |
| single-cell-best-practices | acquisition_mode | not_acquired | link_only |
| single-cell-best-practices | notes | Planned placeholder only. | repo LICENSE observed, but rendered book license applicability remains unresolved; link-only; no source acquired |
| osca | status | planned | reviewed |
| osca | upstream | null | https://bioconductor.org/books/release/OSCA/ |
| osca | license | null | CC BY 4.0 |
| osca | acquisition_mode | not_acquired | link_only |
| osca | notes | Planned placeholder only. | link-only; no source acquired; rendered book and source repo have separate evidence locations |
| osca-advanced | status | planned | reviewed |
| osca-advanced | upstream | null | https://bioconductor.org/books/release/OSCA.advanced/ |
| osca-advanced | license | null | CC BY 4.0 |
| osca-advanced | acquisition_mode | not_acquired | link_only |
| osca-advanced | notes | Planned placeholder only. | link-only; no source acquired; rendered book and source repo have separate evidence locations |
| osta | status | planned | reviewed |
| osta | upstream | null | https://bioconductor.org/books/release/OSTA/ |
| osta | license | null | unknown_pending_review |
| osta | acquisition_mode | not_acquired | link_only |
| osta | notes | Planned placeholder only. | license not observed on rendered book page; partial evidence confidence; link-only; no source acquired |
| seurat | status | planned | reviewed |
| seurat | upstream | null | https://satijalab.org/seurat/ |
| seurat | license | null | MIT + file LICENSE |
| seurat | acquisition_mode | not_acquired | link_only |
| seurat | notes | Planned placeholder only. | link-only; no source acquired; rendered docs and source repo have separate evidence locations |
| bioconductor-package-vignettes | status | planned | reviewed |
| bioconductor-package-vignettes | upstream | null | https://bioconductor.org/help/package-vignettes/ |
| bioconductor-package-vignettes | license | null | unknown_pending_review |
| bioconductor-package-vignettes | acquisition_mode | not_acquired | link_only |
| bioconductor-package-vignettes | notes | Planned placeholder only. | umbrella scope; redistribution restricted per terms-of-use; partial evidence confidence; link-only; no source acquired |
| scuttle | status | planned | reviewed |
| scuttle | upstream | null | https://bioconductor.org/packages/release/bioc/html/scuttle.html |
| scuttle | license | null | GPL-3 |
| scuttle | acquisition_mode | not_acquired | link_only |
| scuttle | notes | Planned placeholder only. | link-only; no source acquired; rendered docs and source repo have separate evidence locations |
| scran | status | planned | reviewed |
| scran | upstream | null | https://bioconductor.org/packages/release/bioc/html/scran.html |
| scran | license | null | GPL-3 |
| scran | acquisition_mode | not_acquired | link_only |
| scran | notes | Planned placeholder only. | link-only; no source acquired; rendered docs and source repo have separate evidence locations |
| scater | status | planned | reviewed |
| scater | upstream | null | https://bioconductor.org/packages/release/bioc/html/scater.html |
| scater | license | null | GPL-3 |
| scater | acquisition_mode | not_acquired | link_only |
| scater | notes | Planned placeholder only. | link-only; no source acquired; source repo URL points to bioconductor.org only |
| singlecellexperiment | status | planned | reviewed |
| singlecellexperiment | upstream | null | https://bioconductor.org/packages/release/bioc/html/SingleCellExperiment.html |
| singlecellexperiment | license | null | GPL-3 |
| singlecellexperiment | acquisition_mode | not_acquired | link_only |
| singlecellexperiment | notes | Planned placeholder only. | link-only; no source acquired; rendered docs and source repo have separate evidence locations |
| scdblfinder | status | planned | reviewed |
| scdblfinder | upstream | null | https://bioconductor.org/packages/release/bioc/html/scDblFinder.html |
| scdblfinder | license | null | GPL-3 + file LICENSE |
| scdblfinder | acquisition_mode | not_acquired | link_only |
| scdblfinder | notes | Planned placeholder only. | link-only; no source acquired; rendered docs and source repo have separate evidence locations |
| decontx-celda | status | planned | reviewed |
| decontx-celda | upstream | null | https://bioconductor.org/packages/release/bioc/html/celda.html |
| decontx-celda | license | null | MIT + file LICENSE |
| decontx-celda | acquisition_mode | not_acquired | link_only |
| decontx-celda | notes | Planned placeholder only. | link-only; no source acquired; rendered docs and source repo have separate evidence locations |
| sctransform | status | planned | reviewed |
| sctransform | upstream | null | https://CRAN.R-project.org/package=sctransform |
| sctransform | license | null | GPL-3 \| file LICENSE |
| sctransform | acquisition_mode | not_acquired | link_only |
| sctransform | notes | Planned placeholder only. | link-only; no source acquired; not a Bioconductor package; CRAN is primary distribution |
| renv | status | planned | reviewed |
| renv | upstream | null | https://rstudio.github.io/renv/ |
| renv | license | null | MIT + file LICENSE |
| renv | acquisition_mode | not_acquired | link_only |
| renv | notes | Planned placeholder only. | link-only; no source acquired; rendered docs and source repo have separate evidence locations |
| github-actions | status | planned | reviewed |
| github-actions | upstream | null | https://docs.github.com/en/actions |
| github-actions | license | null | unknown_pending_review |
| github-actions | acquisition_mode | not_acquired | link_only |
| github-actions | notes | Planned placeholder only. | no license terms found on documentation page; partial evidence confidence; link-only; no source acquired |
| git-submodule-documentation | status | planned | reviewed |
| git-submodule-documentation | upstream | null | https://git-scm.com/docs/gitsubmodules |
| git-submodule-documentation | license | null | GPL |
| git-submodule-documentation | acquisition_mode | not_acquired | link_only |
| git-submodule-documentation | notes | Planned placeholder only. | link-only; no source acquired; reference manual page; GPL per git-scm.com/site license breakdown |

## License Categories

| License | Sources |
|---------|---------|
| CC BY 4.0 | osca, osca-advanced |
| MIT + file LICENSE | seurat, decontx-celda, renv |
| GPL-3 | scuttle, scran, scater, singlecellexperiment |
| GPL-3 + file LICENSE | scdblfinder |
| GPL-3 \| file LICENSE | sctransform |
| GPL | git-submodule-documentation |
| unknown_pending_review | single-cell-best-practices, osta, bioconductor-package-vignettes, github-actions |

## Unresolved Questions for Codex Audit

1. **single-cell-best-practices**: Does the GitHub repo's Apache-2.0 license apply to the rendered book at sc-best-practices.org?
2. **osca-advanced**: Do the GitHub repo code or datasets have separate license terms from the rendered book?
3. **osta**: What license applies to this Bioconductor book? No license field visible on rendered page.
4. **bioconductor-package-vignettes**: What is the full legal status of the terms-of-use restriction? Should this source remain link-only, and should future acquisition split it into per-package entries with package-specific evidence?
5. **github-actions**: What license terms apply to GitHub's documentation? No explicit license found.
