#!/usr/bin/env python3
"""Install the exported /ref-bio OpenCode skill into a downstream project."""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_DEST = Path(".opencode") / "skills" / "ref-bio"
EXPORT_DIR = Path("exports") / "opencode-skill" / "ref-bio"
FORBIDDEN_INSTALL_NAMES = {"sources", "acquisition", "exports", "reports", ".git"}


def find_repo_root():
    path = Path(__file__).resolve().parent.parent
    if not (path / "references.yaml").exists():
        print("ERROR: Cannot find repository root (references.yaml not found).", file=sys.stderr)
        sys.exit(1)
    return path


def run_export(repo_root):
    result = subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "export_opencode_skill.py"), "--force"],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        print("ERROR: export_opencode_skill.py failed.", file=sys.stderr)
        sys.exit(result.returncode)


def resolve_destination(target, dest):
    target = Path(target).resolve()
    dest_path = Path(dest)
    if dest_path.is_absolute():
        resolved = dest_path.resolve()
    else:
        resolved = (target / dest_path).resolve()

    if resolved != target and target not in resolved.parents:
        print(
            f"ERROR: Destination must be inside target project: {resolved}",
            file=sys.stderr,
        )
        sys.exit(1)
    return target, resolved


def assert_no_forbidden_dirs(bundle_dir):
    errors = []
    for path in bundle_dir.rglob("*"):
        if path.is_dir() and path.name in FORBIDDEN_INSTALL_NAMES:
            errors.append(path.relative_to(bundle_dir).as_posix())
    if errors:
        for rel in errors:
            print(f"ERROR: Forbidden directory in skill bundle: {rel}", file=sys.stderr)
        sys.exit(1)


def install_opencode_skill(target, dest=DEFAULT_DEST, force=False, dry_run=False):
    repo_root = find_repo_root()
    target_path, destination = resolve_destination(target, dest)
    export_path = repo_root / EXPORT_DIR

    run_export(repo_root)

    if not export_path.exists():
        print(f"ERROR: Missing exported skill bundle: {export_path}", file=sys.stderr)
        sys.exit(1)
    assert_no_forbidden_dirs(export_path)

    print(f"Target project: {target_path}")
    print(f"Install destination: {destination}")

    if dry_run:
        print("Dry run: no files copied.")
        return destination

    if destination.exists():
        if not force:
            print(
                f"ERROR: Destination already exists. Use --force to overwrite: {destination}",
                file=sys.stderr,
            )
            sys.exit(1)
        shutil.rmtree(destination)

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(export_path, destination)
    assert_no_forbidden_dirs(destination)

    print(f"Installed /ref-bio OpenCode skill to {destination}")
    print()
    print("Usage example:")
    print("/ref-bio Help me design a QC plan for this Visium project.")
    return destination


def main():
    parser = argparse.ArgumentParser(description="Install the /ref-bio OpenCode skill.")
    parser.add_argument("--target", required=True, help="Downstream project path.")
    parser.add_argument(
        "--dest",
        default=str(DEFAULT_DEST),
        help="Install destination relative to target project.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite an existing installation.")
    parser.add_argument("--dry-run", action="store_true", help="Report actions without copying.")
    args = parser.parse_args()

    install_opencode_skill(args.target, args.dest, force=args.force, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
