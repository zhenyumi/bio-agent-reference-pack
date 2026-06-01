# bio-agent-reference-pack

## What this is

`bio-agent-reference-pack` is a source-first, link-resolved, license-aware
reference registry for bioinformatics coding agents.

It helps agents identify which original upstream sources should be read before
planning, reviewing, or modifying bioinformatics analysis code.

`/ref-bio` is explicit-trigger only and does source routing, not scientific
summarization. It activates only when a user message begins with `/ref-bio`;
ordinary bioinformatics requests use the normal project workflow. The
authoritative registry is `references.yaml`; files in `indexes/` route tasks
to source IDs; files in `policies/` constrain agent behavior.

## What this is not

This repository is not a RAG system, a scientific summary repository, a
database-first knowledge base, or a vendored mirror of upstream documentation.

It does not vendor upstream source files. It does not automatically update
source metadata, license fields, source priorities, reading priorities, or
acquisition modes. It does not override downstream project instructions.

## Usage modes

### Mode 1: install the lightweight reference bundle

The current repository provides an export workflow for a lightweight
downstream-ready reference bundle:

```sh
python3 scripts/export_project_reference.py
python3 scripts/build_release_manifest.py
python3 scripts/verify_export_bundle.py
```

The generated bundle is written to `exports/project-reference/`. It contains
`AGENTS.reference.md`, `references.link-only.yaml`, `indexes/`, `policies/`,
and `MANIFEST.yaml`.

There is currently no `scripts/install_project_reference.py`; direct
installation of the reference bundle is separate from `/ref-bio` skill
installation.

### Mode 2: install the explicit `/ref-bio` OpenCode skill

The recommended installation path uses the top-level `install-opencode.sh`
wrapper:

```sh
./install-opencode.sh --project ../my-analysis-project
./install-opencode.sh --project ../my-analysis-project --dry-run --verbose
./install-opencode.sh --project ../my-analysis-project --update
./install-opencode.sh --project ../my-analysis-project --uninstall
./install-opencode.sh --list
./install-opencode.sh --validate
```

The skill is installed at `.opencode/skills/ref-bio/`.

For direct Python control, the underlying scripts are available:

```sh
python3 scripts/install_opencode_skill.py --target ../my-analysis-project
python3 scripts/install_opencode_skill.py --target ../my-analysis-project --dry-run
python3 scripts/install_opencode_skill.py --target ../my-analysis-project --force
```

Example usage in the downstream project:

```text
/ref-bio Help me design a QC plan for this Visium project.
```

Without `/ref-bio`, the agent uses the normal project workflow. With
`/ref-bio`, the agent performs source routing through the bundled reference pack
before planning, reviewing, or modifying bioinformatics analysis code.

## How `/ref-bio` works

`/ref-bio` is explicit-trigger only. It activates only when the user message
begins with `/ref-bio`.

When triggered, the skill:

- strips the `/ref-bio` prefix and treats the remaining text as the task
- classifies the task by modality, workflow stage, package/tool, and platform
- uses `reference-pack/indexes/` as routing aids
- resolves source IDs through `reference-pack/references.link-only.yaml`
- reports matched source IDs and reading priorities before producing a plan,
  review, or code modification
- directs the agent to official upstream URLs instead of local vendored copies

## Downstream project reading order

Project-specific instructions override this central reference pack. Agents using
`/ref-bio` should read in this order:

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

## Updating and checking the registry

Stage 4 update-review tooling is lightweight and local by default:

```sh
python3 scripts/check_upstream_updates.py
```

The script reports registry mode counts, unresolved license review items,
metadata-only/deferred entries, lock state, upstream directory state, index
cross-references, and unused source IDs. It does not fetch URLs, clone
repositories, or acquire source files.

Full local validation:

```sh
python3 scripts/validate_metadata.py
python3 scripts/scan_repo_hygiene.py --all
python3 scripts/check_upstream_updates.py
python3 scripts/build_link_catalog.py
python3 scripts/export_project_reference.py
python3 scripts/build_release_manifest.py
python3 scripts/verify_export_bundle.py
python3 scripts/export_opencode_skill.py
python3 -m unittest discover -s tests
git diff --check
```

## Safety and license rules

- Do not reintroduce submodules without review.
- Do not vendor upstream documentation or source files by default.
- Do not copy PDFs, archives, raw datasets, generated documentation, or analysis
  outputs.
- Do not add scientific summaries.
- Do not infer license status, source priority, or analysis guidance from
  memory.
- Do not treat indexes as scientific authority.
- Do not claim to have read upstream URLs if they were inaccessible.
