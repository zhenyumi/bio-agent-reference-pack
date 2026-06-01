#!/usr/bin/env python3
"""
Deterministic local validation for bio-agent-reference-pack metadata.

Checks:
- YAML metadata files parse correctly
- JSON schema files parse correctly
- Reference IDs in references.yaml are unique
- planned_source_ids in indexes reference valid reference IDs
- sources.lock.yaml acquired sources reference valid reference IDs
- pinned_vendor_snapshot manifests match disk state and snapshot policy
- .gitmodules/gitlink state matches git_submodule entries in sources.lock.yaml
- sources/upstream/ contains only .gitkeep and recorded acquisition dirs
- Required project-control paths are not git-ignored
"""

import json
import hashlib
import os
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required for YAML parsing.", file=sys.stderr)
    print("Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    print("ERROR: jsonschema is required for schema validation.", file=sys.stderr)
    print("Install with: pip install jsonschema", file=sys.stderr)
    sys.exit(1)

SCHEMA_MAP = {
    "references.yaml": "schemas/references.schema.json",
    "sources.lock.yaml": "schemas/sources-lock.schema.json",
    "indexes/topic-map.yaml": "schemas/topic-map.schema.json",
    "indexes/package-map.yaml": "schemas/package-map.schema.json",
    "indexes/workflow-stage-map.yaml": "schemas/workflow-stage-map.schema.json",
}

# Per-policy: sources.lock.yaml only records actually acquired sources
# (git_submodule or pinned_vendor_snapshot). Other modes belong in references.yaml only.
LOCK_ACQUISITION_MODES = {"git_submodule", "pinned_vendor_snapshot"}

SNAPSHOT_FORBIDDEN_DIRS = {
    "data",
    "extdata",
    "testdata",
    "tests",
    "docs",
    "outdated",
    "pkgdown",
    "site",
    "build",
    "dist",
    "__pycache__",
    ".cache",
    ".tox",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".git",
    ".github",
    ".dev",
    ".idea",
    ".vscode",
    ".ipynb_checkpoints",
}

SNAPSHOT_FORBIDDEN_EXTENSIONS = {
    ".pdf",
    ".zip",
    ".tar",
    ".tar.gz",
    ".tgz",
    ".7z",
    ".rar",
    ".h5ad",
    ".h5",
    ".hdf5",
    ".loom",
    ".bam",
    ".bai",
    ".sam",
    ".fastq",
    ".fastq.gz",
    ".fq",
    ".fq.gz",
    ".fasta",
    ".fasta.gz",
    ".fa",
    ".fa.gz",
    ".gtf",
    ".gff",
    ".gff3",
    ".bed",
    ".wig",
    ".bigwig",
    ".bw",
    ".parquet",
    ".npz",
    ".npy",
    ".csv.gz",
    ".tsv.gz",
    ".rda",
    ".rdata",
    ".rds",
    ".csv",
    ".tsv",
    ".gmt",
    ".mtx",
    ".pickle",
    ".pkl",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".svg",
    ".nb",
    ".ipynb",
    ".html",
    ".htm",
    ".rel",
    ".rproj",
}

SNAPSHOT_TOP_LEVEL_PREFIXES = ("README", "NEWS", "LICENSE", "LICENCE", "COPYING")
SNAPSHOT_TOP_LEVEL_NAMES = {
    "DESCRIPTION",
    "NAMESPACE",
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
}
SNAPSHOT_VIGNETTE_EXTENSIONS = {".rmd", ".qmd", ".md", ".bib"}
SNAPSHOT_INST_BOOK_EXTENSIONS = {".rmd", ".qmd", ".md", ".bib", ".yml", ".yaml", ".css"}


def find_repo_root():
    """Find the repository root by looking for references.yaml."""
    path = Path(__file__).resolve().parent.parent
    if not (path / "references.yaml").exists():
        print("ERROR: Cannot find repository root (references.yaml not found).", file=sys.stderr)
        sys.exit(1)
    return path


def load_yaml(path):
    """Load and return a YAML file."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path):
    """Load and return a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def file_sha256(path):
    """Return the SHA-256 digest for a file."""
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def forbidden_snapshot_reason(rel_path):
    """Return a reason if a pinned snapshot path violates the snapshot allowlist."""
    if rel_path == "MANIFEST.yaml":
        return None
    lower = rel_path.lower()
    parts = lower.split("/")
    for part in parts:
        if part in SNAPSHOT_FORBIDDEN_DIRS:
            return f"forbidden snapshot directory '{part}'"
    for ext in sorted(SNAPSHOT_FORBIDDEN_EXTENSIONS, key=len, reverse=True):
        if lower.endswith(ext):
            return f"forbidden snapshot extension '{ext}'"

    path = Path(rel_path)
    original_parts = rel_path.split("/")
    if len(original_parts) == 1:
        name = original_parts[0]
        if name in SNAPSHOT_TOP_LEVEL_NAMES:
            return None
        if any(name.startswith(prefix) for prefix in SNAPSHOT_TOP_LEVEL_PREFIXES):
            return None
        return "outside snapshot allowlist"

    if original_parts[0] in {"R", "src", "man"}:
        return None
    if original_parts[0] == "vignettes" and path.suffix.lower() in SNAPSHOT_VIGNETTE_EXTENSIONS:
        return None
    if rel_path == "inst/CITATION":
        return None
    if original_parts[:2] == ["inst", "book"] and path.suffix.lower() in SNAPSHOT_INST_BOOK_EXTENSIONS:
        return None

    return "outside snapshot allowlist"


def source_lock_entries(repo_root):
    """Return entries from sources.lock.yaml."""
    return load_yaml(repo_root / "sources.lock.yaml").get("sources", [])
    return None


def check_unique_reference_ids(repo_root, errors):
    """Check that all reference IDs in references.yaml are unique."""
    refs_path = repo_root / "references.yaml"
    data = load_yaml(refs_path)
    entries = data.get("entries", [])
    seen = set()
    for entry in entries:
        ref_id = entry.get("id")
        if ref_id in seen:
            errors.append(f"Duplicate reference ID in references.yaml: {ref_id}")
        seen.add(ref_id)
    return seen


def check_index_source_ids(repo_root, ref_ids, errors):
    """Check that all planned_source_ids in indexes exist in references.yaml."""
    indexes_dir = repo_root / "indexes"
    for yaml_file in sorted(indexes_dir.glob("*.yaml")):
        data = load_yaml(yaml_file)
        # package-map uses "packages", others use different keys
        for key in ("topics", "workflow_stages", "packages"):
            items = data.get(key, [])
            for item in items:
                source_ids = item.get("planned_source_ids", [])
                for sid in source_ids:
                    if sid not in ref_ids:
                        errors.append(
                            f"Index {yaml_file.name}: planned_source_id '{sid}' "
                            f"not found in references.yaml"
                        )


def check_sources_lock(repo_root, ref_ids, errors):
    """Check that sources.lock.yaml acquired sources reference valid IDs and modes."""
    lock_path = repo_root / "sources.lock.yaml"
    data = load_yaml(lock_path)
    manifest_schema = load_json(repo_root / "schemas" / "vendor-snapshot-manifest.schema.json")
    format_checker = FormatChecker()
    sources = data.get("sources", [])
    for source in sources:
        sid = source.get("source_id")
        if sid not in ref_ids:
            errors.append(
                f"sources.lock.yaml: source_id '{sid}' not found in references.yaml"
            )
        mode = source.get("acquisition_mode")
        if mode not in LOCK_ACQUISITION_MODES:
            errors.append(
                f"sources.lock.yaml: source_id '{sid}' has acquisition_mode "
                f"'{mode}'; only {sorted(LOCK_ACQUISITION_MODES)} are permitted in lock"
            )
        # Manifest consistency for pinned_vendor_snapshot
        if mode == "pinned_vendor_snapshot":
            for required_field in ("upstream_url", "license_evidence_url"):
                if not source.get(required_field):
                    errors.append(
                        f"sources.lock.yaml: source_id '{sid}' has acquisition_mode "
                        f"pinned_vendor_snapshot but no {required_field} set"
                    )
            manifest_path = source.get("manifest_path")
            if not manifest_path:
                errors.append(
                    f"sources.lock.yaml: source_id '{sid}' has acquisition_mode "
                    f"pinned_vendor_snapshot but no manifest_path set"
                )
            else:
                full_manifest = repo_root / manifest_path
                if not full_manifest.exists():
                    errors.append(
                        f"sources.lock.yaml: source_id '{sid}' manifest_path "
                        f"'{manifest_path}' does not exist on disk"
                    )
                else:
                    check_snapshot_manifest(
                        repo_root,
                        source,
                        full_manifest,
                        manifest_schema,
                        format_checker,
                        errors,
                    )


def check_snapshot_manifest(repo_root, source, manifest_path, manifest_schema, format_checker, errors):
    """Validate a pinned_vendor_snapshot manifest against schema, disk state, and hashes."""
    sid = source.get("source_id")
    local_path = source.get("local_path")
    snapshot_root = repo_root / local_path

    try:
        manifest = load_yaml(manifest_path)
    except Exception as e:
        errors.append(f"{manifest_path.relative_to(repo_root)}: failed to parse YAML: {e}")
        return

    validator = Draft202012Validator(manifest_schema, format_checker=format_checker)
    for error in sorted(validator.iter_errors(manifest), key=lambda e: list(e.absolute_path)):
        path = ".".join(str(p) for p in error.absolute_path) or "(root)"
        errors.append(
            f"Schema validation failed for {manifest_path.relative_to(repo_root)} "
            f"at {path}: {error.message}"
        )

    if manifest.get("source_id") != sid:
        errors.append(
            f"{manifest_path.relative_to(repo_root)}: source_id '{manifest.get('source_id')}' "
            f"does not match sources.lock.yaml source_id '{sid}'"
        )
    if manifest.get("source_commit") != source.get("version_or_commit"):
        errors.append(
            f"{manifest_path.relative_to(repo_root)}: source_commit does not match "
            f"sources.lock.yaml version_or_commit for '{sid}'"
        )
    if manifest.get("upstream_url") != source.get("upstream_url"):
        errors.append(
            f"{manifest_path.relative_to(repo_root)}: upstream_url does not match "
            f"sources.lock.yaml upstream_url for '{sid}'"
        )
    if manifest.get("license") != source.get("license"):
        errors.append(
            f"{manifest_path.relative_to(repo_root)}: license does not match "
            f"sources.lock.yaml license for '{sid}'"
        )
    if manifest.get("license_evidence_url") != source.get("license_evidence_url"):
        errors.append(
            f"{manifest_path.relative_to(repo_root)}: license_evidence_url does not match "
            f"sources.lock.yaml license_evidence_url for '{sid}'"
        )

    included_files = manifest.get("included_files", [])
    included_paths = {item.get("path") for item in included_files}
    if "MANIFEST.yaml" in included_paths:
        errors.append(f"{manifest_path.relative_to(repo_root)}: MANIFEST.yaml is listed in included_files")

    actual_paths = {
        p.relative_to(snapshot_root).as_posix()
        for p in snapshot_root.rglob("*")
        if p.is_file() and p.name != "MANIFEST.yaml"
    }

    extra_paths = sorted(actual_paths - included_paths)
    missing_paths = sorted(included_paths - actual_paths)
    for rel_path in extra_paths:
        errors.append(
            f"{manifest_path.relative_to(repo_root)}: file exists but is not listed in included_files: {rel_path}"
        )
    for rel_path in missing_paths:
        errors.append(
            f"{manifest_path.relative_to(repo_root)}: included_files lists missing file: {rel_path}"
        )

    for item in included_files:
        rel_path = item.get("path")
        if not rel_path or rel_path not in actual_paths:
            continue
        reason = forbidden_snapshot_reason(rel_path)
        if reason:
            errors.append(
                f"{manifest_path.relative_to(repo_root)}: included file violates snapshot policy: "
                f"{rel_path} ({reason})"
            )
        full_path = snapshot_root / rel_path
        actual_size = full_path.stat().st_size
        actual_hash = file_sha256(full_path)
        if item.get("size_bytes") != actual_size:
            errors.append(
                f"{manifest_path.relative_to(repo_root)}: size mismatch for {rel_path}"
            )
        if item.get("sha256") != actual_hash:
            errors.append(
                f"{manifest_path.relative_to(repo_root)}: sha256 mismatch for {rel_path}"
            )


def check_upstream_dir(repo_root, errors):
    """Check that sources/upstream/ contains only .gitkeep and recorded acquisition dirs."""
    upstream_dir = repo_root / "sources" / "upstream"
    if not upstream_dir.exists():
        errors.append("sources/upstream/ directory does not exist")
        return

    # Load allowed acquisition dirs from sources.lock.yaml
    allowed_submodule_dirs = set()
    lock_path = repo_root / "sources.lock.yaml"
    try:
        lock_data = load_yaml(lock_path)
        for source in lock_data.get("sources", []):
            mode = source.get("acquisition_mode")
            if mode not in LOCK_ACQUISITION_MODES:
                continue
            local_path = source.get("local_path", "")
            expected_prefix = "sources/upstream/"
            if local_path.startswith(expected_prefix):
                dir_name = local_path[len(expected_prefix):]
                if dir_name and "/" not in dir_name:
                    allowed_submodule_dirs.add(dir_name)
    except Exception:
        pass  # If lock file can't be parsed, no dirs are allowed

    allowed = {".gitkeep"} | allowed_submodule_dirs
    for item in sorted(upstream_dir.iterdir()):
        if item.name not in allowed:
            errors.append(
                f"sources/upstream/ contains unexpected file: {item.name}"
            )


def check_gitmodules_consistency(repo_root, errors):
    """Check that .gitmodules and gitlink entries match git_submodule locks."""
    sources = source_lock_entries(repo_root)
    expected_paths = {
        source.get("local_path")
        for source in sources
        if source.get("acquisition_mode") == "git_submodule"
    }
    expected_paths.discard(None)

    gitmodules_path = repo_root / ".gitmodules"
    actual_gitmodules_paths = set()
    if gitmodules_path.exists():
        result = subprocess.run(
            ["git", "config", "--file", ".gitmodules", "--get-regexp", r"^submodule\..*\.path$"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                parts = line.split(maxsplit=1)
                if len(parts) == 2:
                    actual_gitmodules_paths.add(parts[1].strip())
        elif result.returncode == 1 and gitmodules_path.read_text(encoding="utf-8").strip() == "":
            pass
        else:
            stderr_msg = result.stderr.strip() if result.stderr else "unknown error"
            errors.append(f"Unable to parse .gitmodules: {stderr_msg}")

    if actual_gitmodules_paths != expected_paths:
        errors.append(
            ".gitmodules paths do not match sources.lock.yaml git_submodule paths: "
            f"expected {sorted(expected_paths)}, found {sorted(actual_gitmodules_paths)}"
        )

    result = subprocess.run(
        ["git", "ls-files", "--stage", "sources/upstream"],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        stderr_msg = result.stderr.strip() if result.stderr else "unknown error"
        errors.append(f"git ls-files failed while checking submodule gitlinks: {stderr_msg}")
        return

    gitlink_paths = set()
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 4 and parts[0] == "160000":
            gitlink_paths.add(parts[3])

    if gitlink_paths != expected_paths:
        errors.append(
            "Git index gitlinks do not match sources.lock.yaml git_submodule paths: "
            f"expected {sorted(expected_paths)}, found {sorted(gitlink_paths)}"
        )


def check_git_not_ignored(repo_root, errors):
    """Check that required project-control paths are not git-ignored."""
    required_paths = [
        "PLAN.md",
        "AGENTS.md",
        "references.yaml",
        "sources.lock.yaml",
        "indexes/",
        "policies/",
        "schemas/",
        "scripts/",
        "tests/",
        ".codex/",
        ".opencode/",
    ]
    for rel_path in required_paths:
        result = subprocess.run(
            ["git", "check-ignore", rel_path],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            # returncode 0 means the path IS ignored
            errors.append(
                f"Required path '{rel_path}' is git-ignored. "
                f"Check .gitignore exclusions."
            )
        elif result.returncode == 1:
            # returncode 1 means the path is NOT ignored - this is correct
            pass
        else:
            # Any other returncode is a command error
            stderr_msg = result.stderr.strip() if result.stderr else "unknown error"
            errors.append(
                f"git check-ignore failed for '{rel_path}': {stderr_msg}"
            )


def check_schema_conformance(repo_root, errors):
    """Validate YAML files against their corresponding JSON schemas."""
    format_checker = FormatChecker()
    for yaml_rel, schema_rel in SCHEMA_MAP.items():
        yaml_path = repo_root / yaml_rel
        schema_path = repo_root / schema_rel
        if not yaml_path.exists() or not schema_path.exists():
            continue
        try:
            data = load_yaml(yaml_path)
            schema = load_json(schema_path)
            validator = Draft202012Validator(schema, format_checker=format_checker)
            for error in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
                path = ".".join(str(p) for p in error.absolute_path) or "(root)"
                errors.append(
                    f"Schema validation failed for {yaml_rel} at {path}: {error.message}"
                )
        except Exception as e:
            errors.append(f"Error validating {yaml_rel} against {schema_rel}: {e}")


def validate(repo_root=None):
    """Run all validation checks. Returns list of errors (empty = pass)."""
    if repo_root is None:
        repo_root = find_repo_root()
    errors = []

    # Check YAML files parse
    yaml_files = [
        repo_root / "references.yaml",
        repo_root / "sources.lock.yaml",
    ] + sorted((repo_root / "indexes").glob("*.yaml"))

    for yf in yaml_files:
        try:
            load_yaml(yf)
        except Exception as e:
            errors.append(f"Failed to parse {yf.name}: {e}")

    # Check JSON schema files parse
    schemas_dir = repo_root / "schemas"
    for jf in sorted(schemas_dir.glob("*.json")):
        try:
            load_json(jf)
        except Exception as e:
            errors.append(f"Failed to parse {jf.name}: {e}")

    if errors:
        return errors

    # Check YAML files conform to their JSON schemas
    check_schema_conformance(repo_root, errors)

    if errors:
        return errors

    # Check unique reference IDs
    ref_ids = check_unique_reference_ids(repo_root, errors)

    # Check index cross-references
    check_index_source_ids(repo_root, ref_ids, errors)

    # Check sources.lock.yaml consistency
    check_sources_lock(repo_root, ref_ids, errors)

    # Check upstream directory
    check_upstream_dir(repo_root, errors)

    # Check .gitmodules and git index consistency for git_submodule acquisitions
    check_gitmodules_consistency(repo_root, errors)

    # Check git ignore status
    check_git_not_ignored(repo_root, errors)

    return errors


def main():
    repo_root = find_repo_root()
    errors = validate(repo_root)

    if errors:
        print("VALIDATION FAILED", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    print("All metadata validation checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
