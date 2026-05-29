# AGENTS.md

Codex reads this repository as an agent-readable project.

## Authority Model

- `PLAN.md` controls current repository development.
- `sources/upstream/` is authoritative when source files are present.
- `indexes/` files are navigation aids only. They route agents to source IDs and must not summarize or replace original sources.
- `policies/` govern agent behavior in this repository, but they do not replace original upstream guides.
- Downstream project `AGENTS.md`, `PLAN.md`, existing scripts, dataset papers, supplementary methods, author code, and previous outputs override this central reference pack for that downstream project.

## Codex Role

Codex GPT may:

- Design repository architecture.
- Write or review `PLAN.md`.
- Review `AGENTS.md`.
- Review source policy, license policy, update strategy, and source-priority decisions.
- Review future diffs for scope, privacy, license, and source-first integrity.

## OpenCode and Execution-Agent Role

Execution agents may:

- Create files requested by a scoped task.
- Implement validation scripts after schema and policy decisions are reviewed.
- Run narrow mechanical checks.
- Update placeholders only when exact instructions and acceptance criteria are provided.

Execution agents must not:

- Summarize scientific guidelines.
- Infer best practices.
- Choose source priority.
- Decide redistribution rights.
- Invent licenses, versions, citations, or acquisition status.
- Treat indexes as scientific guidance.

Source metadata, license policy, update policy, and source priority require higher-level review.

## Privacy and Git Hygiene

No secrets, API keys, tokens, credentials, proxy addresses, private server URLs, local absolute paths, home directories, IP addresses, private locations, or other private machine-specific information may be committed.

Public author names, citation metadata, public institutional affiliations, and public URLs are acceptable when they are part of public source metadata.

`PLAN.md`, `AGENTS.md`, `.codex/`, and `.opencode/` are intentionally version-controlled and must not be ignored.

## Mandatory Pre-Publish Review

Before any commit, push, release, publication, or repository review request:

Perform a read-only repository audit.

Review:

- git status
- staged changes
- unstaged changes
- untracked files
- .gitignore

Check for:

- secrets
- API keys
- tokens
- credentials
- .env files
- private keys
- local machine paths
- usernames embedded in paths
- private IP addresses
- internal URLs
- unpublished identifiers
- raw datasets
- generated outputs
- cache files
- IDE artifacts

Never perform:

- git add
- git commit
- git push
- file modifications

until the audit is completed and reported.

If risks are found, stop and report them.
