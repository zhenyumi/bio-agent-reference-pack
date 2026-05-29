# Batch 1 Source Acquisition Review

This document is a review package for Codex. It is not authoritative source metadata.

- All URLs are candidates for Codex review.
- "verified official candidate" means a public-facing official documentation/package/book page.
  It does not mean that license or redistribution has been verified.
- No candidate URL has been written to authoritative metadata (references.yaml, sources.lock.yaml, or sources/upstream/).
- No source has been acquired.
- All license and redistribution assessments are preliminary and pending Codex review.

---

## single-cell-best-practices

- **source_id:** single-cell-best-practices
- **current title:** single-cell best practices
- **candidate official upstream URL(s):**
  - verified official candidate: `https://www.sc-best-practices.org/`
  - unverified candidate requiring Codex review: source repo — verify from rendered book's source link
- **candidate license evidence URL(s):**
  - `https://www.sc-best-practices.org/` (check rendered book for license statement)
  - source repo LICENSE (URL to be determined by Codex from rendered book's source link)
- **observed license text/location:** Not verified by this agent
- **candidate acquisition mode:** link_only_candidate
- **preliminary redistribution risk:** unknown pending Codex review
- **full-text vendoring appears unsafe pending review:** yes
- **uncertainty notes:** Rendered book and source repo may carry different license terms. Codex must verify both.
- **recommended Codex review question:** What license applies to the rendered book content vs. the source repository code? Is link_only sufficient?

---

## osca

- **source_id:** osca
- **current title:** OSCA
- **candidate official upstream URL(s):**
  - verified official candidate: `https://bioconductor.org/books/release/OSCA/`
  - unverified candidate requiring Codex review: source repo URL — not assumed; Codex must verify from the rendered book's Source link
- **candidate license evidence URL(s):**
  - `https://bioconductor.org/books/release/OSCA/` (check rendered book for license statement)
  - source repo LICENSE (URL to be determined by Codex from rendered book's Source link)
- **observed license text/location:** Not verified by this agent
- **candidate acquisition mode:** link_only_candidate
- **preliminary redistribution risk:** unknown pending Codex review
- **full-text vendoring appears unsafe pending review:** yes
- **uncertainty notes:** Do not assume the same license across rendered book, source repo, code, and datasets.
- **recommended Codex review question:** What license applies to the rendered book? Does the Bioconductor book page link to a source repo? What license governs that repo?

---

## osca-advanced

- **source_id:** osca-advanced
- **current title:** OSCA Advanced
- **candidate official upstream URL(s):**
  - verified official candidate: `https://bioconductor.org/books/release/OSCA.advanced/`
  - unverified candidate requiring Codex review: source repo URL — not assumed; may be part of OSCA repo or separate; Codex must verify from rendered book's Source link
- **candidate license evidence URL(s):**
  - `https://bioconductor.org/books/release/OSCA.advanced/` (check rendered book for license statement)
  - source repo LICENSE (URL to be determined by Codex from rendered book's Source link)
- **observed license text/location:** Not verified by this agent
- **candidate acquisition mode:** link_only_candidate
- **preliminary redistribution risk:** unknown pending Codex review
- **full-text vendoring appears unsafe pending review:** yes
- **uncertainty notes:** May share infrastructure with OSCA but license terms are not assumed identical. Separate GitHub repo existence unverified.
- **recommended Codex review question:** Is OSCA Advanced a separate repo or a section within the OSCA repo? What license applies to the Advanced book content?

---

## osta

- **source_id:** osta
- **current title:** OSTA
- **candidate official upstream URL(s):**
  - verified official candidate: `https://bioconductor.org/books/release/OSTA/`
  - unverified candidate requiring Codex review: `https://github.com/lmweber/OSTA` (requires Codex verification from book's Source link)
- **candidate license evidence URL(s):**
  - `https://bioconductor.org/books/release/OSTA/` (check rendered book for license statement)
  - source repo LICENSE (URL to be determined by Codex from rendered book's Source link)
- **observed license text/location:** Not verified by this agent
- **candidate acquisition mode:** link_only_candidate
- **preliminary redistribution risk:** unknown pending Codex review
- **full-text vendoring appears unsafe pending review:** yes
- **uncertainty notes:** Do not assume the same license across rendered book, source repo, code, and datasets.
- **recommended Codex review question:** What license applies to the OSTA rendered book? Does the book page link to a confirmed source repo?

---

## seurat

- **source_id:** seurat
- **current title:** Seurat
- **candidate official upstream URL(s):**
  - verified official candidate: `https://satijalab.org/seurat/`
  - unverified candidate requiring Codex review: source repo — verify from official site's links
- **candidate license evidence URL(s):**
  - `https://satijalab.org/seurat/` (check for license statement)
  - source repo LICENSE (URL to be verified by Codex from official site)
- **observed license text/location:** Not verified by this agent
- **candidate acquisition mode:** link_only_candidate
- **preliminary redistribution risk:** unknown pending Codex review
- **full-text vendoring appears unsafe pending review:** yes
- **uncertainty notes:** Package vignettes on the official site may have different terms than GitHub source code.
- **recommended Codex review question:** What license applies to the Seurat vignettes on satijalab.org vs. the source code on GitHub?

---

## bioconductor-package-vignettes

- **source_id:** bioconductor-package-vignettes
- **current title:** Bioconductor package vignettes
- **candidate official upstream URL(s):**
  - verified official candidate: `https://bioconductor.org/packages/release/BiocViews.html#___Software` (package listing)
  - unverified candidate requiring Codex review: none — this is an umbrella reference; individual package pages vary
- **candidate license evidence URL(s):**
  - `https://bioconductor.org/about/legal/` (Bioconductor legal page)
- **observed license text/location:** Not verified by this agent
- **candidate acquisition mode:** link_only_candidate
- **preliminary redistribution risk:** unknown pending Codex review
- **full-text vendoring appears unsafe pending review:** yes
- **uncertainty notes:** Umbrella scope unclear. Individual packages may carry different licenses. No single blanket license applies. Codex must decide whether to split this source into package-specific entries.
- **recommended Codex review question:** Should this umbrella source be split into per-package entries? What is the scope of this source ID? Do all included vignettes share a common license?

---

## scuttle

- **source_id:** scuttle
- **current title:** scuttle
- **candidate official upstream URL(s):**
  - verified official candidate: `https://bioconductor.org/packages/release/bioc/html/scuttle.html`
  - unverified candidate requiring Codex review: source repo URL — not assumed; Codex must verify from package page's Source links or Developer tab
- **candidate license evidence URL(s):**
  - `https://bioconductor.org/packages/release/bioc/html/scuttle.html` (package page license field)
  - source repo LICENSE (URL to be determined by Codex from package page)
- **observed license text/location:** Not verified by this agent
- **candidate acquisition mode:** link_only_candidate
- **preliminary redistribution risk:** unknown pending Codex review
- **full-text vendoring appears unsafe pending review:** yes
- **uncertainty notes:** Bioconductor package page license field and source repo LICENSE should both be checked by Codex.
- **recommended Codex review question:** Do the Bioconductor package page license field and the source repo LICENSE agree? Which governs vignette redistribution?

---

## scran

- **source_id:** scran
- **current title:** scran
- **candidate official upstream URL(s):**
  - verified official candidate: `https://bioconductor.org/packages/release/bioc/html/scran.html`
  - unverified candidate requiring Codex review: source repo URL — not assumed; Codex must verify from package page
- **candidate license evidence URL(s):**
  - `https://bioconductor.org/packages/release/bioc/html/scran.html` (package page license field)
  - source repo LICENSE (URL to be determined by Codex from package page)
- **observed license text/location:** Not verified by this agent
- **candidate acquisition mode:** link_only_candidate
- **preliminary redistribution risk:** unknown pending Codex review
- **full-text vendoring appears unsafe pending review:** yes
- **uncertainty notes:** Same as scuttle.
- **recommended Codex review question:** Do the Bioconductor package page license field and the source repo LICENSE agree? Which governs vignette redistribution?

---

## scater

- **source_id:** scater
- **current title:** scater
- **candidate official upstream URL(s):**
  - verified official candidate: `https://bioconductor.org/packages/release/bioc/html/scater.html`
  - unverified candidate requiring Codex review: source repo URL — not assumed; Codex must verify from package page
- **candidate license evidence URL(s):**
  - `https://bioconductor.org/packages/release/bioc/html/scater.html` (package page license field)
  - source repo LICENSE (URL to be determined by Codex from package page)
- **observed license text/location:** Not verified by this agent
- **candidate acquisition mode:** link_only_candidate
- **preliminary redistribution risk:** unknown pending Codex review
- **full-text vendoring appears unsafe pending review:** yes
- **uncertainty notes:** Same as scuttle.
- **recommended Codex review question:** Do the Bioconductor package page license field and the source repo LICENSE agree? Which governs vignette redistribution?

---

## singlecellexperiment

- **source_id:** singlecellexperiment
- **current title:** SingleCellExperiment
- **candidate official upstream URL(s):**
  - verified official candidate: `https://bioconductor.org/packages/release/bioc/html/SingleCellExperiment.html`
  - unverified candidate requiring Codex review: source repo URL — not assumed; Codex must verify from package page (do not assume GitHub org/repo path)
- **candidate license evidence URL(s):**
  - `https://bioconductor.org/packages/release/bioc/html/SingleCellExperiment.html` (package page license field)
  - source repo LICENSE (URL to be determined by Codex from package page)
- **observed license text/location:** Not verified by this agent
- **candidate acquisition mode:** link_only_candidate
- **preliminary redistribution risk:** unknown pending Codex review
- **full-text vendoring appears unsafe pending review:** yes
- **uncertainty notes:** Same as scuttle — do not assume GitHub org/repo path.
- **recommended Codex review question:** Do the Bioconductor package page license field and the source repo LICENSE agree? Which governs vignette redistribution?

---

## scdblfinder

- **source_id:** scdblfinder
- **current title:** scDblFinder
- **candidate official upstream URL(s):**
  - verified official candidate: `https://bioconductor.org/packages/release/bioc/html/scDblFinder.html`
  - unverified candidate requiring Codex review: source repo URL — not assumed; Codex must verify from package page
- **candidate license evidence URL(s):**
  - `https://bioconductor.org/packages/release/bioc/html/scDblFinder.html` (package page license field)
  - source repo LICENSE (URL to be determined by Codex from package page)
- **observed license text/location:** Not verified by this agent
- **candidate acquisition mode:** link_only_candidate
- **preliminary redistribution risk:** unknown pending Codex review
- **full-text vendoring appears unsafe pending review:** yes
- **uncertainty notes:** Same as scuttle.
- **recommended Codex review question:** Do the Bioconductor package page license field and the source repo LICENSE agree? Which governs vignette redistribution?

---

## decontx-celda

- **source_id:** decontx-celda
- **current title:** DecontX/celda
- **candidate official upstream URL(s):**
  - verified official candidate: `https://bioconductor.org/packages/release/bioc/html/celda.html` (DecontX is within celda)
  - unverified candidate requiring Codex review: source repo URL — not assumed; Codex must verify from package page
- **candidate license evidence URL(s):**
  - `https://bioconductor.org/packages/release/bioc/html/celda.html` (package page license field)
  - source repo LICENSE (URL to be determined by Codex from package page)
- **observed license text/location:** Not verified by this agent
- **candidate acquisition mode:** link_only_candidate
- **preliminary redistribution risk:** unknown pending Codex review
- **full-text vendoring appears unsafe pending review:** yes
- **uncertainty notes:** DecontX is a function within the celda package. Source ID `decontx-celda` scope may need clarification.
- **recommended Codex review question:** Should this source cover all of celda or only DecontX-specific documentation? What license applies?

---

## sctransform

- **source_id:** sctransform
- **current title:** SCTransform
- **candidate official upstream URL(s):**
  - unverified candidate requiring Codex review: official upstream not confirmed; possible CRAN, Bioconductor, Satija documentation, or GitHub candidates require Codex verification
- **candidate license evidence URL(s):**
  - unknown — requires Codex review
- **observed license text/location:** Not verified by this agent
- **candidate acquisition mode:** link_only_candidate
- **preliminary redistribution risk:** unknown pending Codex review
- **full-text vendoring appears unsafe pending review:** yes
- **uncertainty notes:** Upstream uncertain. sctransform may be hosted on Bioconductor, CRAN, or the Satija lab site. This agent has not verified which is the primary official source. Codex must determine the correct upstream and license.
- **recommended Codex review question:** What is the official upstream for sctransform documentation? Is it a Bioconductor package, CRAN package, or hosted on satijalab.org? What license applies?

---

## renv

- **source_id:** renv
- **current title:** renv
- **candidate official upstream URL(s):**
  - verified official candidate: `https://rstudio.github.io/renv/`
  - unverified candidate requiring Codex review: source repo — verify from official docs site links
- **candidate license evidence URL(s):**
  - `https://rstudio.github.io/renv/` (check for license statement)
  - source repo LICENSE (URL to be verified by Codex from official docs site)
- **observed license text/location:** Not verified by this agent
- **candidate acquisition mode:** link_only_candidate
- **preliminary redistribution risk:** unknown pending Codex review
- **full-text vendoring appears unsafe pending review:** yes
- **uncertainty notes:** Documentation site and source repo may have different license terms. Posit/RStudio corporate documentation may have terms beyond the repo license.
- **recommended Codex review question:** What license applies to the renv documentation on rstudio.github.io vs. the source code? Are Posit documentation terms different from the repo license?

---

## github-actions

- **source_id:** github-actions
- **current title:** GitHub Actions
- **candidate official upstream URL(s):**
  - verified official candidate: `https://docs.github.com/en/actions`
  - unverified candidate requiring Codex review: none
- **candidate license evidence URL(s):**
  - `https://docs.github.com/en/site-policy` (GitHub site policies) — specific documentation redistribution terms unknown
- **observed license text/location:** Not verified by this agent
- **candidate acquisition mode:** link_only_candidate
- **preliminary redistribution risk:** unknown pending Codex review
- **full-text vendoring appears unsafe pending review:** yes
- **uncertainty notes:** GitHub site policy governs use but may not explicitly permit redistribution of documentation text.
- **recommended Codex review question:** What are the specific terms governing redistribution of GitHub Actions documentation? Is link_only the only safe mode?

---

## git-submodule-documentation

- **source_id:** git-submodule-documentation
- **current title:** Git submodule documentation
- **candidate official upstream URL(s):**
  - verified official candidate: `https://git-scm.com/docs/gitsubmodules`
  - unverified candidate requiring Codex review: `https://github.com/git/git-scm.com` (site source repo — verify from git-scm.com), `https://git-scm.com/book/en/v2` (Pro Git book, includes submodule chapter)
- **candidate license evidence URL(s):**
  - `https://git-scm.com/book/en/v2` (check for license statement; reported mixed licensing; exact terms require Codex verification)
  - source repo LICENSE (URL to be determined by Codex)
- **observed license text/location:** Not verified by this agent
- **candidate acquisition mode:** link_only_candidate
- **preliminary redistribution risk:** unknown pending Codex review
- **full-text vendoring appears unsafe pending review:** yes
- **uncertainty notes:** Mixed licensing reported for Pro Git but unverified. Git reference documentation (manpage-style) may have different terms.
- **recommended Codex review question:** What license applies to the git reference documentation on git-scm.com/docs? Is it the same as Pro Git? Should this source be scoped to only the gitsubmodules reference page?
