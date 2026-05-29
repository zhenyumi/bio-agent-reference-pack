# bio-agent-reference-pack

This repository is a source-first, version-pinned, license-aware reference pack for bioinformatics coding agents.

It is intended to help agents know which original upstream sources to read before planning, reviewing, or modifying bioinformatics analysis projects. It is not a scientific summary repository, a RAG system, or a database-first knowledge base.

Original upstream guides, official package documentation, dataset papers, supplementary methods, and author code are authoritative. The files in `indexes/` only route agents to relevant sources; they must not replace, paraphrase, or reinterpret original scientific guidance.

Project-specific instructions in a downstream repository override this central reference pack. In particular, downstream `AGENTS.md`, `PLAN.md`, existing scripts, previous outputs, dataset documentation, and project-specific constraints must be read before applying this pack.

The intended workflow is:

- Codex GPT designs architecture, writes and reviews plans, reviews policies, checks licenses and source strategy, and reviews future diffs.
- OpenCode execution agents perform scoped mechanical tasks, such as creating files, validating metadata, and running narrow checks.

Execution agents must not summarize scientific guidelines, infer best practices, choose source priority, or decide redistribution rights.

