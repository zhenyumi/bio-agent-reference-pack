# Licenses

This repository is license-aware. License fields are metadata records derived from official source/package evidence and do not grant permission to vendor unrelated full text. No scientific guidance is summarized here.

## Current State

The repository is link-only/on-demand by default. No package source trees are vendored locally. All real upstream sources are recorded as `link_only` with their official URLs, licenses, and license evidence URLs. Agents should retrieve and read upstream documentation on demand using `references.yaml` and indexes, not from local copies.

## Source Acquisition Modes

- `link_only` — official upstream URL recorded; no source files acquired.
- `metadata_only` — routing entry only; no source files acquired.
- `defer` — deferred until a concrete need or clearer scope exists.
- `git_submodule` — full upstream worktree pinned by commit. Not used in current state.
- `pinned_vendor_snapshot` — filtered source/documentation-source snapshot pinned by upstream commit. Not used in current state.
- `do_not_include` — excluded from this pack.

## Link-Only Sources (50)

All actual upstream sources are link-only. License strings and evidence URLs are preserved from the original license verification pass. No package source trees are vendored.

### Guides and Books

| Source ID | License | Upstream | Evidence URL |
|-----------|---------|----------|-------------|
| single-cell-best-practices | unknown_pending_review | https://www.sc-best-practices.org/ | — |
| osca | CC BY 4.0 | https://bioconductor.org/books/release/OSCA/ | https://github.com/OSCA-source/OSCA/blob/master/LICENSE |
| osca-advanced | CC BY 4.0 | https://bioconductor.org/books/release/OSCA.advanced/ | https://github.com/OSCA-source/OSCA.advanced/blob/master/LICENSE |
| osta | unknown_pending_review | https://bioconductor.org/books/release/OSTA/ | — |

### Bioconductor Packages

| Source ID | License | Upstream | Evidence URL |
|-----------|---------|----------|-------------|
| scuttle | GPL-3 | https://bioconductor.org/packages/release/bioc/html/scuttle.html | https://github.com/Bioconductor/scuttle/blob/master/DESCRIPTION |
| scran | GPL-3 | https://bioconductor.org/packages/release/bioc/html/scran.html | https://github.com/Bioconductor/scran/blob/master/DESCRIPTION |
| scater | GPL-3 | https://bioconductor.org/packages/release/bioc/html/scater.html | https://github.com/Bioconductor/scater/blob/master/DESCRIPTION |
| singlecellexperiment | GPL-3 | https://bioconductor.org/packages/release/bioc/html/SingleCellExperiment.html | https://github.com/Bioconductor/SingleCellExperiment/blob/master/DESCRIPTION |
| scdblfinder | GPL-3 + file LICENSE | https://bioconductor.org/packages/release/bioc/html/scDblFinder.html | https://github.com/plger/scDblFinder/blob/master/LICENSE |
| decontx-celda | MIT + file LICENSE | https://bioconductor.org/packages/release/bioc/html/celda.html | https://github.com/campbio/celda/blob/master/LICENSE |
| clusterprofiler | Artistic-2.0 | https://bioconductor.org/packages/release/bioc/html/clusterProfiler.html | https://github.com/YuLab-SMU/clusterProfiler/blob/master/LICENSE |
| mast | GPL (>= 2) | https://bioconductor.org/packages/release/bioc/html/MAST.html | https://github.com/RGLab/MAST/blob/master/DESCRIPTION |
| singler | GPL-3 | https://bioconductor.org/packages/release/bioc/html/SingleR.html | https://github.com/SingleR-inc/SingleR/blob/master/DESCRIPTION |
| batchelor | GPL-3 | https://bioconductor.org/packages/release/bioc/html/batchelor.html | https://github.com/Bioconductor/batchelor/blob/master/DESCRIPTION |
| celldex | GPL-3 | https://bioconductor.org/packages/release/data/experiment/html/celldex.html | https://github.com/LTLA/celldex/blob/master/DESCRIPTION |
| enrichplot | Artistic-2.0 | https://bioconductor.org/packages/release/bioc/html/enrichplot.html | https://github.com/GuangchuangYu/enrichplot/blob/master/LICENSE |
| fgsea | MIT + file LICENCE | https://bioconductor.org/packages/release/bioc/html/fgsea.html | https://github.com/alserglab/fgsea/blob/master/DESCRIPTION |
| limma | GPL (>=2) | https://bioconductor.org/packages/release/bioc/html/limma.html | https://github.com/cran/limma/blob/master/DESCRIPTION |
| edger | GPL (>=2) | https://bioconductor.org/packages/release/bioc/html/edgeR.html | https://github.com/Bioconductor/edgeR/blob/master/DESCRIPTION |
| deseq2 | LGPL (>= 3) | https://bioconductor.org/packages/release/bioc/html/DESeq2.html | https://github.com/thelovelab/DESeq2/blob/master/DESCRIPTION |
| spatialexperiment | GPL-3 | https://bioconductor.org/packages/release/bioc/html/SpatialExperiment.html | https://github.com/drighelli/SpatialExperiment/blob/master/DESCRIPTION |
| spatialfeatureexperiment | Artistic-2.0 | https://bioconductor.org/packages/release/bioc/html/SpatialFeatureExperiment.html | https://github.com/pachterlab/SpatialFeatureExperiment/blob/master/DESCRIPTION |
| slingshot | Artistic-2.0 | https://bioconductor.org/packages/release/bioc/html/slingshot.html | https://github.com/kstreet13/slingshot/blob/master/DESCRIPTION |
| tradeseq | MIT + file LICENSE | https://bioconductor.org/packages/release/bioc/html/tradeSeq.html | https://github.com/statOmics/tradeSeq/blob/master/DESCRIPTION |
| bayesspace | MIT + file LICENSE | https://bioconductor.org/packages/release/bioc/html/BayesSpace.html | https://github.com/edward130603/BayesSpace/blob/master/DESCRIPTION |
| bioconductor-package-vignettes | unknown_pending_review | https://bioconductor.org/help/package-vignettes/ | — |

### CRAN and GitHub Packages

| Source ID | License | Upstream | Evidence URL |
|-----------|---------|----------|-------------|
| seurat | MIT + file LICENSE | https://satijalab.org/seurat/ | https://github.com/satijalab/seurat/blob/master/LICENSE |
| sctransform | GPL-3 \| file LICENSE | https://CRAN.R-project.org/package=sctransform | https://github.com/satijalab/sctransform/blob/master/LICENSE |
| azimuth | GPL-3 \| file LICENSE | https://github.com/satijalab/azimuth | https://github.com/satijalab/azimuth/blob/master/LICENSE |
| harmony | GPL-3 | https://github.com/immunogenomics/harmony | https://github.com/immunogenomics/harmony/blob/master/DESCRIPTION |
| liana | GPL-3 + file LICENSE | https://github.com/saezlab/liana | https://github.com/saezlab/liana/blob/master/LICENSE |
| cellchat | GPL-3 | https://github.com/sqjin/CellChat | https://github.com/sqjin/CellChat/blob/master/LICENSE |
| monocle3 | MIT + file LICENSE | https://github.com/cole-trapnell-lab/monocle3 | https://github.com/cole-trapnell-lab/monocle3/blob/master/LICENSE |
| renv | MIT + file LICENSE | https://rstudio.github.io/renv/ | https://github.com/rstudio/renv/blob/main/LICENSE |
| msigdbr | MIT + file LICENSE | https://github.com/igordot/msigdbr | https://github.com/igordot/msigdbr/blob/master/LICENSE |
| nnsvg | MIT + file LICENSE | https://github.com/lmweber/nnSVG | https://github.com/lmweber/nnSVG/blob/master/LICENSE |
| spark-x | GPL-3 | https://github.com/xzhoulab/SPARK | https://github.com/xzhoulab/SPARK/blob/master/DESCRIPTION |
| soupx | GPL-2 | https://github.com/constantAmateur/SoupX | https://github.com/constantAmateur/SoupX/blob/master/DESCRIPTION |
| giotto | MIT \| file LICENSE | https://github.com/drieslab/Giotto | https://github.com/drieslab/Giotto/blob/master/DESCRIPTION |
| stutility | MIT + file LICENSE | https://github.com/ludvigla/STUtility | https://github.com/ludvigla/STUtility/blob/master/LICENSE |
| banksy | unknown_pending_review | https://github.com/prabhakarlab/Banksy | https://github.com/prabhakarlab/Banksy/blob/master/LICENSE |
| nichenet | GPL-3 | https://github.com/saeyslab/nichenetr | https://github.com/saeyslab/nichenetr/blob/master/DESCRIPTION |
| squidpy | BSD-3-Clause | https://github.com/scverse/squidpy | https://github.com/scverse/squidpy/blob/master/pyproject.toml |

### Platform and Agent Documentation

| Source ID | License | Upstream | Evidence URL |
|-----------|---------|----------|-------------|
| github-actions | unknown_pending_review | https://docs.github.com/en/actions | — |
| codex-agents-guidance | unknown_pending_review | https://github.com/openai/codex/blob/main/AGENTS.md | — |
| opencode-documentation | unknown_pending_review | https://opencode.ai/docs | — |
| visium | unknown_pending_review | https://www.10xgenomics.com/platforms/visium | — |
| xenium | unknown_pending_review | https://www.10xgenomics.com/platforms/xenium | — |
| cosmx | unknown_pending_review | https://nanostring.com/products/cosmx-spatial-molecular-imager/ | — |
| git-submodule-documentation | GPL | https://git-scm.com/docs/gitsubmodules | https://git-scm.com/site/license |

## Metadata-Only Sources (4)

| Source ID | Upstream | Notes |
|-----------|----------|-------|
| seurat-integration | https://satijalab.org/seurat/articles/integration_introduction | routes to source_id=seurat; metadata only; no separate acquisition |
| seurat-reference-mapping | https://satijalab.org/seurat/articles/reference_mapping | routes to source_id=seurat; metadata only; no separate acquisition |
| pseudobulk-de-guidance | https://www.nature.com/articles/s41587-021-01037-z | routes to source_id=limma,edger,deseq2; metadata only; no separate acquisition |
| seurat-spatial | https://satijalab.org/seurat/ | routes to source_id=seurat; no specific standalone page verified; metadata only; no separate acquisition |

## Deferred Sources (1)

| Source ID | Notes |
|-----------|-------|
| gptomics-bioskills | deferred; no clear single public upstream; not required by this reference pack |

## Notable Governance Decisions

- The stable registry ID is `nichenet`; the upstream repository recorded for that source may be `saeyslab/nichenetr`. The source ID itself is not renamed.
- `banksy` remains `link_only` because its license is non-standard (MIT for academic, restrictions for commercial) and not treated as a vendoring permit.
- Platform/documentation sources without clear redistribution terms remain `link_only`.
- All license strings were verified from raw upstream files (LICENSE, DESCRIPTION, pyproject.toml) during Stage 2, not from page-rendered text or assumptions.

## Privacy and Redistribution Guardrails

The repository must not commit secrets, credentials, local-machine paths, private network locations, raw datasets, generated outputs, or cache files. License fields are metadata records only and do not constitute a redistribution grant.
