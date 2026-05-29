# Agent Reading Protocol

Agents should use indexes as routing maps, not as scientific guidance.

Protocol:

1. Read the downstream project instructions first.
2. Identify the task topic, package, and workflow stage.
3. Use `indexes/` files to locate planned or acquired source IDs.
4. Check `sources.lock.yaml` for acquired source version, commit, local path, license, and acquisition mode.
5. Read the original upstream source when it is available.
6. Apply downstream project instructions and source-priority policy.
7. If a needed source is only planned, report that it has not been acquired.

Do not summarize scientific guidelines into this repository. Record routing, metadata, and review needs instead.

