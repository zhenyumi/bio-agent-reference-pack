# Batch 1 Source Evidence Collection

This document records evidence collected by browsing official public web pages.

- No source has been acquired.
- No license or redistribution conclusion is final.
- All evidence is pending Codex audit.
- Evidence confidence categories: `sufficient_for_review`, `partial`, `not_found`.

---

## single-cell-best-practices

- **source_id:** single-cell-best-practices
- **reviewed official upstream URL(s):**
  - `https://www.sc-best-practices.org/` — rendered book; page returned empty or minimal markdown when fetched
  - `https://github.com/theislab/single-cell-best-practices` — source repo; confirmed via GitHub search
- **how URL was found:** GitHub repo README links to `https://www.sc-best-practices.org/`
- **license evidence URL(s):**
  - `https://github.com/theislab/single-cell-best-practices/blob/main/LICENSE`
- **exact location of license evidence:** GitHub repo LICENSE file
- **short quoted snippet:** "Licensed under the Apache License, Version 2.0"
- **rendered docs and source repo have separate evidence locations:** yes — rendered book at sc-best-practices.org, license at GitHub LICENSE file
- **candidate acquisition mode:** link_only_candidate
- **evidence confidence:** sufficient_for_review
- **unresolved questions for Codex audit:**
  - Is the rendered book under the same Apache 2.0 license as the repo?
  - Should the reference point to the rendered book URL or the GitHub repo?

---

## osca

- **source_id:** osca
- **reviewed official upstream URL(s):**
  - `https://bioconductor.org/books/release/OSCA/` — rendered book; page opened and verified
- **how URL was found:** listed on `https://bioconductor.org/help/bioconductor-books/`
- **license evidence URL(s):**
  - `https://bioconductor.org/books/release/OSCA/` — license field in book page header
- **exact location of license evidence:** rendered book page header metadata section
- **short quoted snippet:** "License: CC BY 4.0"
- **rendered docs and source repo have separate evidence locations:** yes — rendered book at bioconductor.org, source repo at `https://github.com/OSCA-source/OSCA` (observed on book page as "Source:")
- **candidate acquisition mode:** link_only_candidate
- **evidence confidence:** sufficient_for_review
- **unresolved questions for Codex audit:**
  - Does the GitHub repo have a separate LICENSE file, and does it match CC BY 4.0?
  - Does the CC BY 4.0 license apply to the book content only, or also to code in the repo?

---

## osca-advanced

- **source_id:** osca-advanced
- **reviewed official upstream URL(s):**
  - `https://bioconductor.org/books/release/OSCA.advanced/` — rendered book; page opened and verified
  - `https://github.com/OSCA-source/OSCA.advanced` — source repo; observed on rendered book page as "Source:"
- **how URL was found:** rendered URL from Bioconductor books pattern; source repo link observed on rendered book page
- **license evidence URL(s):**
  - `https://bioconductor.org/books/release/OSCA.advanced/` — license field in book page metadata section
- **exact location of license evidence:** rendered book page metadata section
- **short quoted snippet:** "License: CC BY 4.0"
- **rendered docs and source repo have separate evidence locations:** yes — rendered book at bioconductor.org, source repo at `https://github.com/OSCA-source/OSCA.advanced` (observed on book page)
- **candidate acquisition mode:** link_only_candidate
- **evidence confidence:** sufficient_for_review
- **unresolved questions for Codex audit:**
  - Do the GitHub repo code or datasets have separate license terms from the rendered book?
  - Does the GitHub repo carry the same CC BY 4.0 as the rendered book?

---

## osta

- **source_id:** osta
- **reviewed official upstream URL(s):**
  - `https://bioconductor.org/books/release/OSTA/` — rendered book; page opened and verified
- **how URL was found:** listed on `https://bioconductor.org/help/bioconductor-books/`
- **license evidence URL(s):**
  - not_found — no license field observed on the rendered book page
- **exact location of license evidence:** not_found
- **short quoted snippet:** (none)
- **rendered docs and source repo have separate evidence locations:** only rendered book page observed; no source repo URL found on page
- **candidate acquisition mode:** link_only_candidate
- **evidence confidence:** partial
- **unresolved questions for Codex audit:**
  - What license applies to the OSTA book content?
  - Does the book page link to a source repo (e.g., in footer or hidden metadata)?
  - Is the source repo `https://github.com/lmweber/OSTA` (candidate from batch-1-review.md)?

---

## seurat

- **source_id:** seurat
- **reviewed official upstream URL(s):**
  - `https://satijalab.org/seurat/` — official Satija Lab site; page opened and verified
- **how URL was found:** Satija Lab is the official lab developing Seurat
- **license evidence URL(s):**
  - `https://satijalab.org/seurat/` — license section in site footer
- **exact location of license evidence:** site footer, license section
- **short quoted snippet:** "License: MIT + file LICENSE"
- **rendered docs and source repo have separate evidence locations:** yes — rendered docs at satijalab.org, source repo at `https://github.com/satijalab/seurat/` (observed in site footer as "Browse source code:")
- **candidate acquisition mode:** link_only_candidate
- **evidence confidence:** sufficient_for_review
- **unresolved questions for Codex audit:**
  - Does the GitHub repo have a separate LICENSE file, and does it match MIT?
  - What license applies to the vignettes/articles on satijalab.org vs. the source code?

---

## bioconductor-package-vignettes

- **source_id:** bioconductor-package-vignettes
- **reviewed official upstream URL(s):**
  - `https://bioconductor.org/help/package-vignettes/` — vignettes listing page; page opened and verified
  - `https://bioconductor.org/about/legal/` — returned 404
- **how URL was found:** Bioconductor Help section links to package vignettes
- **license evidence URL(s):**
  - `https://bioconductor.org/help/package-vignettes/` — terms-of-use statement on page
- **exact location of license evidence:** terms-of-use text on the vignettes page
- **short quoted snippet:** "you may not include these in separately published works (articles, books, websites)"
- **rendered docs and source repo have separate evidence locations:** N/A — this is an umbrella reference covering multiple packages
- **candidate acquisition mode:** link_only_candidate
- **evidence confidence:** partial
- **unresolved questions for Codex audit:**
  - The terms-of-use text restricts redistribution ("you may not include these in separately published works"). Is this an open license?
  - The Bioconductor legal page (`/about/legal/`) returns 404. Where is the authoritative legal statement?
  - Should this umbrella source be split into per-package entries with individual licenses?
  - Do individual package vignettes carry their own package-level licenses (e.g., GPL-3, MIT)?

---

## scuttle

- **source_id:** scuttle
- **reviewed official upstream URL(s):**
  - `https://bioconductor.org/packages/release/bioc/html/scuttle.html` — Bioconductor package page; page opened and verified
- **how URL was found:** Bioconductor packages > release > bioc > scuttle
- **license evidence URL(s):**
  - `https://bioconductor.org/packages/release/bioc/html/scuttle.html` — license field on package page
- **exact location of license evidence:** package page metadata section
- **short quoted snippet:** "License: GPL-3"
- **rendered docs and source repo have separate evidence locations:** yes — package page at bioconductor.org, source repo at `git clone https://git.bioconductor.org/packages/scuttle` (observed on page)
- **candidate acquisition mode:** link_only_candidate
- **evidence confidence:** sufficient_for_review
- **unresolved questions for Codex audit:**
  - Does the source repo have a separate LICENSE file?
  - What license applies to vignettes vs. package code?

---

## scran

- **source_id:** scran
- **reviewed official upstream URL(s):**
  - `https://bioconductor.org/packages/release/bioc/html/scran.html` — Bioconductor package page; page opened and verified
- **how URL was found:** Bioconductor packages > release > bioc > scran
- **license evidence URL(s):**
  - `https://bioconductor.org/packages/release/bioc/html/scran.html` — license field on package page
- **exact location of license evidence:** package page metadata section
- **short quoted snippet:** "License: GPL-3"
- **rendered docs and source repo have separate evidence locations:** yes — package page at bioconductor.org, source repo at `https://github.com/MarioniLab/scran/` (observed on package page as "URL:")
- **candidate acquisition mode:** link_only_candidate
- **evidence confidence:** sufficient_for_review
- **unresolved questions for Codex audit:**
  - Does the GitHub repo have a separate LICENSE file?
  - What license applies to vignettes vs. package code?

---

## scater

- **source_id:** scater
- **reviewed official upstream URL(s):**
  - `https://bioconductor.org/packages/release/bioc/html/scater.html` — Bioconductor package page; page opened and verified
- **how URL was found:** Bioconductor packages > release > bioc > scater
- **license evidence URL(s):**
  - `https://bioconductor.org/packages/release/bioc/html/scater.html` — license field on package page
- **exact location of license evidence:** package page metadata section
- **short quoted snippet:** "License: GPL-3"
- **rendered docs and source repo have separate evidence locations:** no — URL field on package page points back to `http://bioconductor.org/packages/scater/` (not external repo); source repo at `git clone https://git.bioconductor.org/packages/scater` (observed on page)
- **candidate acquisition mode:** link_only_candidate
- **evidence confidence:** sufficient_for_review
- **unresolved questions for Codex audit:**
  - Is there an external GitHub repo for scater, or only the Bioconductor git repo?
  - What license applies to vignettes vs. package code?

---

## singlecellexperiment

- **source_id:** singlecellexperiment
- **reviewed official upstream URL(s):**
  - `https://bioconductor.org/packages/release/bioc/html/SingleCellExperiment.html` — Bioconductor package page; page opened and verified
- **how URL was found:** Bioconductor packages > release > bioc > SingleCellExperiment
- **license evidence URL(s):**
  - `https://bioconductor.org/packages/release/bioc/html/SingleCellExperiment.html` — license field on package page
- **exact location of license evidence:** package page metadata section
- **short quoted snippet:** "License: GPL-3"
- **rendered docs and source repo have separate evidence locations:** yes — package page at bioconductor.org, source repo at `git clone https://git.bioconductor.org/packages/SingleCellExperiment` (observed on page)
- **candidate acquisition mode:** link_only_candidate
- **evidence confidence:** sufficient_for_review
- **unresolved questions for Codex audit:**
  - Does the source repo have a separate LICENSE file?
  - What license applies to vignettes vs. package code?

---

## scdblfinder

- **source_id:** scdblfinder
- **reviewed official upstream URL(s):**
  - `https://bioconductor.org/packages/release/bioc/html/scDblFinder.html` — Bioconductor package page; page opened and verified
- **how URL was found:** Bioconductor packages > release > bioc > scDblFinder
- **license evidence URL(s):**
  - `https://bioconductor.org/packages/release/bioc/html/scDblFinder.html` — license field on package page
- **exact location of license evidence:** package page metadata section
- **short quoted snippet:** "License: GPL-3 + file LICENSE"
- **rendered docs and source repo have separate evidence locations:** yes — package page at bioconductor.org, source repo at `https://github.com/plger/scDblFinder` and pkgdown site at `https://plger.github.io/scDblFinder/` (both observed on page)
- **candidate acquisition mode:** link_only_candidate
- **evidence confidence:** sufficient_for_review
- **unresolved questions for Codex audit:**
  - Does the GitHub repo have a separate LICENSE file, and does it match GPL-3?
  - What does the "file LICENSE" exception contain?

---

## decontx-celda

- **source_id:** decontx-celda
- **reviewed official upstream URL(s):**
  - `https://bioconductor.org/packages/release/bioc/html/celda.html` — Bioconductor package page (DecontX is within celda); page opened and verified
- **how URL was found:** Bioconductor packages > release > bioc > celda
- **license evidence URL(s):**
  - `https://bioconductor.org/packages/release/bioc/html/celda.html` — license field on package page
- **exact location of license evidence:** package page metadata section
- **short quoted snippet:** "License: MIT + file LICENSE"
- **rendered docs and source repo have separate evidence locations:** yes — package page at bioconductor.org, bug reports at `https://github.com/campbio/celda/issues` (observed on page); source repo at `git clone https://git.bioconductor.org/packages/celda` (observed on page)
- **candidate acquisition mode:** link_only_candidate
- **evidence confidence:** sufficient_for_review
- **unresolved questions for Codex audit:**
  - Should this source cover all of celda or only DecontX-specific documentation?
  - Does the GitHub repo have a separate LICENSE file?
  - What does the "file LICENSE" exception contain?

---

## sctransform

- **source_id:** sctransform
- **reviewed official upstream URL(s):**
  - `https://CRAN.R-project.org/package=sctransform` — CRAN package page; page opened and verified
  - `https://github.com/satijalab/sctransform` — GitHub repo (observed on CRAN page as "URL:")
- **how URL was found:** CRAN package search; NOT a Bioconductor package (`https://bioconductor.org/packages/release/bioc/html/sctransform.html` returned 404)
- **license evidence URL(s):**
  - `https://CRAN.R-project.org/package=sctransform` — license field on CRAN page
- **exact location of license evidence:** CRAN package page metadata section
- **short quoted snippet:** "GPL-3 | file LICENSE"
- **rendered docs and source repo have separate evidence locations:** yes — CRAN page (license), GitHub repo (source); vignette hosted on Seurat site at `https://satijalab.org/seurat/articles/sctransform_vignette`
- **candidate acquisition mode:** link_only_candidate
- **evidence confidence:** sufficient_for_review
- **unresolved questions for Codex audit:**
  - Does the GitHub repo have a separate LICENSE file?
  - What does the "file LICENSE" exception contain?
  - What license applies to the vignette hosted on satijalab.org (separate from CRAN/GitHub)?

---

## renv

- **source_id:** renv
- **reviewed official upstream URL(s):**
  - `https://rstudio.github.io/renv/` — official documentation site; page opened and verified
- **how URL was found:** official renv documentation site (Posit/RStudio)
- **license evidence URL(s):**
  - `https://rstudio.github.io/renv/` — license section in site footer
- **exact location of license evidence:** site footer, license section
- **short quoted snippet:** "License: MIT + file LICENSE"
- **rendered docs and source repo have separate evidence locations:** yes — docs at rstudio.github.io, source repo at `https://github.com/rstudio/renv/` (observed in site footer as "Browse source code:")
- **candidate acquisition mode:** link_only_candidate
- **evidence confidence:** sufficient_for_review
- **unresolved questions for Codex audit:**
  - Does the GitHub repo have a separate LICENSE file?
  - What does the "file LICENSE" exception contain?
  - Are Posit/RStudio documentation terms different from the repo license?

---

## github-actions

- **source_id:** github-actions
- **reviewed official upstream URL(s):**
  - `https://docs.github.com/en/actions` — official GitHub documentation; page opened and verified
  - `https://docs.github.com/en/site-policy` — GitHub site policies (referenced from docs)
- **how URL was found:** official GitHub documentation site
- **license evidence URL(s):**
  - not_found — no explicit license or documentation redistribution terms found on the Actions page or site-policy page
- **exact location of license evidence:** not_found
- **short quoted snippet:** (none)
- **rendered docs and source repo have separate evidence locations:** N/A — documentation only, no separate source repo
- **candidate acquisition mode:** link_only_candidate
- **evidence confidence:** partial
- **unresolved questions for Codex audit:**
  - What license or terms govern redistribution of GitHub Actions documentation?
  - Is link_only the only permissible mode?
  - Where are the authoritative terms for GitHub documentation reuse?

---

## git-submodule-documentation

- **source_id:** git-submodule-documentation
- **reviewed official upstream URL(s):**
  - `https://git-scm.com/docs/gitsubmodules` — official Git reference documentation; page opened and verified
  - `https://git-scm.com/site` — site license breakdown page (linked from footer)
- **how URL was found:** official Git reference documentation at git-scm.com
- **license evidence URL(s):**
  - `https://git-scm.com/site` — license breakdown for git-scm.com content sections
- **exact location of license evidence:** site page, "Open Source" section
- **short quoted snippet:** "The reference manual is imported from the Git project, and is available under the GPL"
- **rendered docs and source repo have separate evidence locations:** yes — gitsubmodules page (reference manual), site license page (license breakdown); three license categories on git-scm.com:
  - Base site content: MIT license
  - Pro Git book: CC-BY-NC-SA 3.0
  - Reference manual (manpages): GPL
- **candidate acquisition mode:** link_only_candidate
- **evidence confidence:** sufficient_for_review
- **unresolved questions for Codex audit:**
  - The gitsubmodules page is part of the reference manual (GPL). Does this mean the page content is GPL-licensed?
  - Should this source be scoped to only the gitsubmodules reference page, not the Pro Git book?
