# ref-bio

## Trigger

Activate this skill only when the user message begins with `/ref-bio`.

Do not activate this skill for ordinary bioinformatics requests. For example,
`Help me design a QC plan for this Visium project.` must use the normal project
workflow unless the user explicitly prefixes the request with `/ref-bio`.

When triggered, strip the `/ref-bio` prefix and treat the remaining text as the
task. If `/ref-bio` is used without a task, ask the user to provide the
bioinformatics planning, review, or implementation task.

## Purpose

This skill helps agents identify which official upstream bioinformatics sources
should be read before planning, reviewing, or modifying analysis code.

It is source-routing, not scientific summarization. It must not turn the
reference pack into a RAG system, a scientific summary database, or a local
mirror of upstream documentation.

## Current reference model

The bundled reference pack is link-only / metadata-only.

Agents must not assume upstream source files are vendored locally. Use
`reference-pack/references.link-only.yaml` to resolve source IDs to official
upstream URLs. Use files under `reference-pack/indexes/` only as routing aids.
Project-specific instructions override this skill.

## Required reading order

After this skill is triggered, read in this order:

1. Downstream project `AGENTS.md`
2. Downstream project `PLAN.md`
3. Existing scripts relevant to the task
4. Metadata, sample sheets, outputs, project notes, original paper,
   supplementary methods, and author code if present
5. `.opencode/skills/ref-bio/reference-pack/AGENTS.reference.md`
6. `.opencode/skills/ref-bio/reference-pack/indexes/workflow-stage-map.yaml`
7. `.opencode/skills/ref-bio/reference-pack/indexes/topic-map.yaml`
8. `.opencode/skills/ref-bio/reference-pack/indexes/package-map.yaml`
9. `.opencode/skills/ref-bio/reference-pack/references.link-only.yaml`
10. Relevant official upstream URLs listed in the registry

## Task routing workflow

When triggered, classify the task by:

- Data modality:
  - scRNA-seq
  - snRNA-seq
  - spatial transcriptomics
  - bulk RNA-seq
  - mixed
  - unknown
- Workflow stage:
  - loading
  - QC
  - normalization
  - integration
  - clustering
  - annotation
  - differential expression
  - enrichment
  - trajectory
  - cell-cell communication
  - reproducibility
- Package/tool:
  - Seurat
  - SingleCellExperiment
  - scater
  - scuttle
  - scran
  - edgeR
  - limma
  - DESeq2
  - MAST
  - CellChat
  - LIANA
  - NicheNet
  - Monocle3
  - Slingshot
  - tradeSeq
  - other detected tools
- Platform where relevant:
  - Visium
  - Xenium
  - CosMx
  - other

## Source resolution workflow

Use `workflow-stage-map.yaml`, `topic-map.yaml`, and `package-map.yaml` to
identify source IDs. Resolve those source IDs in `references.link-only.yaml`.

Group resolved sources by `reading_priority` when the field is available:

- `must_read`
- `optional_read`
- `project_specific_read`

Use official upstream URLs or rendered documentation URLs from the registry. If
no source IDs are matched, report that explicitly and continue using project
context only.

## Required pre-answer report

Before producing a plan, review, or code modification, report:

- detected task category
- detected modality
- detected workflow stage
- detected package/tool/platform
- matched source IDs
- must-read sources
- optional sources
- project-specific sources
- missing project context, if any
- upstream sources that are inaccessible or not yet read

## Forbidden behavior

- Do not summarize scientific guidelines as authoritative rules.
- Do not infer thresholds from memory.
- Do not choose analysis methods without project context.
- Do not vendor, download, or copy upstream source files.
- Do not modify the reference pack.
- Do not modify source metadata, license fields, acquisition modes, or reading
  priorities.
- Do not treat indexes as scientific authority.
- Do not ignore project-specific paper, metadata, author code, or existing
  scripts.
- Do not claim to have read upstream URLs if they were inaccessible.

## Safe behavior

- Route a task to relevant source IDs.
- Identify official upstream URLs.
- Ask the user to provide inaccessible source text if needed.
- Produce a source-grounded plan or review.
- Recommend that implementation wait until required upstream sources are read.
- Continue with project-specific context when the user explicitly accepts
  incomplete upstream access.

## If upstream URLs are inaccessible

State which URLs or source IDs could not be accessed. Do not fabricate content
from those sources.

Ask the user to provide the relevant source text or allow the work to proceed
with limited confidence. Clearly label any resulting plan or review as not
fully source-verified.

## Examples

User:

```text
/ref-bio Help me design a QC plan for this Visium project.
```

Expected behavior:

- Trigger this skill.
- Route to spatial transcriptomics, QC, Visium, and
  Seurat/SpatialExperiment/OSTA-related sources if present.
- Report matched source IDs before planning.

User:

```text
/ref-bio Review this pseudobulk edgeR script for replicate and design-matrix problems.
```

Expected behavior:

- Trigger this skill.
- Route to pseudobulk DE, edgeR, and limma/DESeq2 if relevant.
- Emphasize project metadata and biological replicate structure.

User:

```text
Help me design a QC plan for this Visium project.
```

Expected behavior:

- Do not trigger this skill unless the user explicitly used `/ref-bio`.
