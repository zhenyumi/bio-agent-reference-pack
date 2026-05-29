# Update Policy

Upstream updates should be checked and reviewed, not silently applied to downstream projects.

Future update checks should:

- Report source ID, current locked version, detected upstream version, checked date, and review status.
- Avoid changing downstream analysis behavior automatically.
- Require review before lock-file updates that affect source priority, licenses, or analysis guidance.
- Keep old lock metadata available in Git history.

Execution agents may run update checks when scoped to do so, but they must not decide whether an upstream change should alter downstream projects.

