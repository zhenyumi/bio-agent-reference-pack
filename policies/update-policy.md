# Update Policy

Upstream updates should be checked and reviewed, not silently applied to downstream projects.

## Current Acquisition State

- `git_submodule` is not used in the current state.
- `pinned_vendor_snapshot` is reserved for future reviewed local acquisition only.
- No upstream source files should be vendored unless explicitly reviewed.

## Future Update Checks

- Report source ID, current locked version, detected upstream version, checked date, and review status.
- Avoid changing downstream analysis behavior automatically.
- Require review before lock-file updates that affect source priority, licenses, or analysis guidance.
- Keep old lock metadata available in Git history.

Execution agents may run update checks when scoped to do so, but they must not decide whether an upstream change should alter downstream projects.

