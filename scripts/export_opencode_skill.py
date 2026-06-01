#!/usr/bin/env python3
"""Export the explicit-trigger /ref-bio OpenCode skill bundle."""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_OUT = Path("exports") / "opencode-skill" / "ref-bio"
REFERENCE_EXPORT = Path("exports") / "project-reference"
FORBIDDEN_EXPORT_NAMES = {"sources", "acquisition", "exports", "reports", ".git"}


def find_repo_root():
    path = Path(__file__).resolve().parent.parent
    if not (path / "references.yaml").exists():
        print("ERROR: Cannot find repository root (references.yaml not found).", file=sys.stderr)
        sys.exit(1)
    return path


def run_script(repo_root, script_name):
    result = subprocess.run(
        [sys.executable, str(repo_root / "scripts" / script_name)],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        print(f"ERROR: {script_name} failed.", file=sys.stderr)
        sys.exit(result.returncode)


def safe_to_replace(path, repo_root):
    """Return True only for the generated default export subtree."""
    try:
        resolved = path.resolve()
        expected = (repo_root / DEFAULT_OUT).resolve()
    except OSError:
        return False
    return resolved == expected or expected in resolved.parents


def copytree_clean(src, dst):
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def assert_no_forbidden_dirs(bundle_dir):
    errors = []
    for path in bundle_dir.rglob("*"):
        if path.is_dir() and path.name in FORBIDDEN_EXPORT_NAMES:
            errors.append(path.relative_to(bundle_dir).as_posix())
    if errors:
        for rel in errors:
            print(f"ERROR: Forbidden directory in skill export: {rel}", file=sys.stderr)
        sys.exit(1)


def export_opencode_skill(out_path=None, force=False):
    repo_root = find_repo_root()
    if out_path is None:
        out_path = repo_root / DEFAULT_OUT
    else:
        out_path = Path(out_path)
        if not out_path.is_absolute():
            out_path = repo_root / out_path

    skill_source = repo_root / "skills" / "ref-bio" / "SKILL.md"
    if not skill_source.exists():
        print(f"ERROR: Missing skill source: {skill_source}", file=sys.stderr)
        sys.exit(1)

    # Generate and verify the lightweight reference bundle first.
    run_script(repo_root, "export_project_reference.py")
    run_script(repo_root, "build_release_manifest.py")
    run_script(repo_root, "verify_export_bundle.py")

    reference_export = repo_root / REFERENCE_EXPORT
    if not reference_export.exists():
        print(f"ERROR: Missing generated reference export: {reference_export}", file=sys.stderr)
        sys.exit(1)

    if out_path.exists():
        if not force and not safe_to_replace(out_path, repo_root):
            print(
                f"ERROR: Refusing to replace existing non-default export path without --force: {out_path}",
                file=sys.stderr,
            )
            sys.exit(1)
        if not safe_to_replace(out_path, repo_root):
            print(f"ERROR: Refusing to delete arbitrary existing path: {out_path}", file=sys.stderr)
            sys.exit(1)
        shutil.rmtree(out_path)

    out_path.mkdir(parents=True, exist_ok=True)
    shutil.copy2(skill_source, out_path / "SKILL.md")
    copytree_clean(reference_export, out_path / "reference-pack")
    assert_no_forbidden_dirs(out_path)

    print(f"Exported /ref-bio OpenCode skill to {out_path.relative_to(repo_root)}")
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Export the /ref-bio OpenCode skill bundle.")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Output path for the skill bundle.")
    parser.add_argument("--force", action="store_true", help="Replace an existing generated export path.")
    args = parser.parse_args()

    export_opencode_skill(args.out, force=args.force)


if __name__ == "__main__":
    main()
