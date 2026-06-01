# bio-agent-reference-pack

This repository is a source-first, link-resolved, license-aware reference registry for bioinformatics coding agents.

It is intended to help agents know which original upstream sources to read before planning, reviewing, or modifying bioinformatics analysis projects. It is not a scientific summary repository, a RAG system, or a database-first knowledge base.

Sources are recorded in `references.yaml` as `link_only` or `metadata_only` entries with official upstream URLs. No package source trees are vendored locally under `sources/upstream/`. Agents should use `references.yaml` and `indexes/` to identify the relevant official upstream sources, then read those upstream sources before planning, reviewing, or modifying downstream bioinformatics analysis code.

Original upstream guides, official package documentation, dataset papers, supplementary methods, and author code are authoritative. The files in `indexes/` only route agents to relevant sources; they must not replace, paraphrase, or reinterpret original scientific guidance.

Project-specific instructions in a downstream repository override this central reference pack. In particular, downstream `AGENTS.md`, `PLAN.md`, existing scripts, previous outputs, dataset documentation, and project-specific constraints must be read before applying this pack.

The intended workflow is:

- Codex GPT designs architecture, writes and reviews plans, reviews policies, checks licenses and source strategy, and reviews future diffs.
- OpenCode execution agents perform scoped mechanical tasks, such as creating files, validating metadata, and running narrow checks.

Execution agents must not summarize scientific guidelines, infer best practices, choose source priority, or decide redistribution rights.

