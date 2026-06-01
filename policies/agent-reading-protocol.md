# Agent Reading Protocol

## Default: On-Demand Reading

No package source trees are vendored locally. Agents must retrieve and read official upstream documentation on demand using `references.yaml` and indexes. The repository provides metadata, source IDs, upstream URLs, license records, reading priority hints, and routing maps — not local copies of upstream source files.

## Protocol

1. Read the downstream project instructions first.
2. Identify the task topic, package, and workflow stage.
3. Use `indexes/` files to locate relevant source IDs.
4. Check `references.yaml` for the source's upstream URL, license record, and reading priority.
5. Retrieve the upstream documentation from the official URL. Do not rely on vendored local copies.
6. Apply downstream project instructions and source-priority policy.
7. Record any new license observations, route corrections, or acquisition needs in the appropriate metadata files. Do not summarize scientific guidance into this repository.

## Indexes

Indexes in `indexes/` are routing maps only. They map topics, packages, and workflow stages to source IDs. They must not summarize scientific methods, package behavior, or analysis guidance.

## Reading Priority

`references.yaml` entries include a `reading_priority` field:

- `must_read` — core official documentation or guidance needed often.
- `optional_read` — supplementary documentation, platform pages, or conceptually relevant sources.
- `project_specific_read` — routing-only or deferred entries; read only when a concrete project need exists.

## Acquisition Modes

- `link_only` — official URL recorded; no source files acquired locally. Agents read from the upstream URL.
- `metadata_only` — routing entry only; points agents toward related link-only sources.
- `defer` — deferred until a concrete project need or clearer upstream scope exists.
- `git_submodule` / `pinned_vendor_snapshot` — reserved for future local acquisition; not used in current state.
