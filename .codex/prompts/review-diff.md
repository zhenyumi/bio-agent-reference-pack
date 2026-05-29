# Codex Review Prompt: Reference-Pack Diff

Review this diff for the bio-agent-reference-pack repository.

Check whether the change:

- Preserves the source-first design.
- Avoids scientific summaries, inferred best practices, and replacement guidance.
- Keeps original upstream sources authoritative.
- Uses indexes only as routing aids.
- Handles licenses conservatively and avoids invented license metadata.
- Avoids vendoring full text, PDFs, or large archives without explicit approval.
- Protects privacy and avoids secrets, credentials, local absolute paths, IP addresses, private locations, proxy addresses, and private server URLs.
- Keeps `.gitignore` from excluding required tracked controls such as `PLAN.md`, `AGENTS.md`, `references.yaml`, `sources.lock.yaml`, `indexes/`, `policies/`, `schemas/`, `scripts/`, `tests/`, `.codex/`, and `.opencode/`.
- Keeps schemas consistent with placeholder metadata.
- Checks whether OpenCode or another execution agent exceeded its scoped task.

Lead with findings ordered by severity. If no issues are found, say so and note residual risks or test gaps.

