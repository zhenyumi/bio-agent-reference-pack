# OpenCode Execution Prompt Template

You are executing a narrow scoped task in bio-agent-reference-pack.

Scope:

- Task:
- Files allowed to edit:
- Files allowed to read:
- Acceptance criteria:
- Commands to run:

Rules:

- Do only the requested mechanical work.
- Do not summarize scientific guidelines.
- Do not infer best practices.
- Do not choose source priority.
- Do not invent licenses, versions, citations, URLs, or acquisition status.
- Do not download or vendor upstream sources unless the task explicitly allows it after review.
- Do not commit secrets, tokens, credentials, local absolute paths, IP addresses, private locations, proxy addresses, or private server URLs.
- Keep `PLAN.md`, `AGENTS.md`, `.codex/`, and `.opencode/` version-controlled.
- Stop and report if acceptance criteria are unclear or if the task requires scientific, license, or source-priority judgment.

Output:

- Files changed
- Commands run
- Whether acceptance criteria passed
- Any blockers requiring Codex review

