#!/usr/bin/env python3
"""
Repository hygiene scanner for bio-agent-reference-pack.

Detects forbidden file types and high-confidence secret patterns
in tracked files. Uses high-confidence patterns only to avoid
flagging policy prose that merely discusses forbidden concepts.

Checks:
- Forbidden binary/archive file extensions
- High-confidence secret tokens (OpenAI, GitHub, GitLab, AWS formats)
- Private IP addresses (10.x, 172.16-31.x, 192.168.x)
- Localhost and private URLs
- Absolute home directory paths (POSIX and Windows)
- Unexpected files under sources/upstream/ other than .gitkeep
- Forbidden file types inside acquired submodule working trees

Usage:
    python3 scripts/scan_repo_hygiene.py         # scan tracked files only
    python3 scripts/scan_repo_hygiene.py --all   # scan tracked + untracked files
"""

import re
import subprocess
import sys
from pathlib import Path

FORBIDDEN_EXTENSIONS = {
    ".pdf", ".zip", ".tar", ".tar.gz", ".tgz", ".7z", ".rar",
}

SECRET_PATTERNS = [
    ("openai_api_key", re.compile(r"sk-(?:proj|svcacct|live)-[a-zA-Z0-9\-]{20,}")),
    ("github_pat", re.compile(r"ghp_[a-zA-Z0-9]{36}")),
    ("github_oauth", re.compile(r"gho_[a-zA-Z0-9]{36}")),
    ("gitlab_pat", re.compile(r"glpat-[a-zA-Z0-9\-]{20,}")),
    ("aws_access_key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("private_ip", re.compile(
        r"(?:^|[^0-9.])(?:(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        r"|(?:(?:172\.(?:1[6-9]|2[0-9]|3[01]))\.\d{1,3}\.\d{1,3})"
        r"|(?:192\.168\.\d{1,3}\.\d{1,3}))(?:[^0-9]|$)"
    )),
    ("localhost_url", re.compile(r"https?://(?:127\.\d{1,3}\.\d{1,3}\.\d{1,3}|localhost)(?:[:/\s]|$)")),
    ("absolute_home_path", re.compile(
        r"(?:^|[\s\"'=:])"
        r"(?:"
        r"(?:/Users/[^/\\\s]+(?:/[^/\\\s]+)+)"
        r"|"
        r"(?:/home/[^/\\\s]+(?:/[^/\\\s]+)+)"
        r"|"
        r"(?:[A-Za-z]:\\Users\\[^/\\\s]+(?:\\[^/\\\s]+)+)"
        r")"
    )),
]


def find_repo_root():
    path = Path(__file__).resolve().parent.parent
    if not (path / "references.yaml").exists():
        print("ERROR: Cannot find repository root (references.yaml not found).", file=sys.stderr)
        sys.exit(1)
    return path


def is_binary_file(path):
    try:
        with open(path, "rb") as f:
            chunk = f.read(8192)
        if b"\x00" in chunk:
            return True
        try:
            chunk.decode("utf-8")
        except UnicodeDecodeError:
            return True
        return False
    except (OSError, PermissionError):
        return True


def get_git_files(repo_root, include_untracked=False):
    """Get file paths from git. Returns list of relative path strings."""
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git ls-files failed: {result.stderr.strip()}")

    files = [line for line in result.stdout.splitlines() if line.strip()]

    if include_untracked:
        result2 = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        if result2.returncode != 0:
            raise RuntimeError(f"git ls-files --others failed: {result2.stderr.strip()}")
        untracked = [line for line in result2.stdout.splitlines() if line.strip()]
        seen = set(files)
        for f in untracked:
            if f not in seen:
                files.append(f)
                seen.add(f)

    return files


def scan_forbidden_extensions(file_paths, repo_root, errors):
    """Check for forbidden file extensions."""
    for rel_path in file_paths:
        full_path = repo_root / rel_path
        ext = ""
        lower = rel_path.lower()
        for candidate in sorted(FORBIDDEN_EXTENSIONS, key=len, reverse=True):
            if lower.endswith(candidate):
                ext = candidate
                break
        if ext:
            errors.append(f"Forbidden file type '{ext}': {rel_path}")


def scan_upstream_dir(repo_root, errors):
    """Check that sources/upstream/ contains only .gitkeep and recorded submodule dirs."""
    upstream_dir = repo_root / "sources" / "upstream"
    if not upstream_dir.exists():
        return

    # Load allowed submodule dirs from sources.lock.yaml
    allowed_submodule_dirs = set()
    lock_path = repo_root / "sources.lock.yaml"
    try:
        import yaml
        with open(lock_path, "r", encoding="utf-8") as f:
            lock_data = yaml.safe_load(f)
        for source in lock_data.get("sources", []):
            if source.get("acquisition_mode") == "git_submodule":
                local_path = source.get("local_path", "")
                expected_prefix = "sources/upstream/"
                if local_path.startswith(expected_prefix):
                    dir_name = local_path[len(expected_prefix):]
                    if dir_name and "/" not in dir_name:
                        allowed_submodule_dirs.add(dir_name)
    except Exception:
        pass  # If lock file can't be parsed, no dirs are allowed

    allowed = {".gitkeep"} | allowed_submodule_dirs
    for item in upstream_dir.iterdir():
        if item.name not in allowed:
            errors.append(
                f"sources/upstream/ contains unexpected file: {item.name}"
            )


def scan_submodule_forbidden_files(repo_root, errors):
    """Check acquired submodule working trees for forbidden file extensions."""
    import os

    # Load allowed submodule dirs from sources.lock.yaml
    allowed_submodule_dirs = set()
    lock_path = repo_root / "sources.lock.yaml"
    try:
        import yaml
        with open(lock_path, "r", encoding="utf-8") as f:
            lock_data = yaml.safe_load(f)
        for source in lock_data.get("sources", []):
            if source.get("acquisition_mode") == "git_submodule":
                local_path = source.get("local_path", "")
                if local_path:
                    allowed_submodule_dirs.add(repo_root / local_path)
    except Exception:
        pass  # If lock file can't be parsed, no dirs are scanned

    for submodule_dir in allowed_submodule_dirs:
        if not submodule_dir.exists() or not submodule_dir.is_dir():
            continue
        for root, dirs, files in os.walk(submodule_dir):
            # Skip .git directory
            dirs[:] = [d for d in dirs if d != ".git"]
            for filename in files:
                file_path = Path(root) / filename
                rel_path = file_path.relative_to(repo_root)
                lower = filename.lower()
                for candidate in sorted(FORBIDDEN_EXTENSIONS, key=len, reverse=True):
                    if lower.endswith(candidate):
                        errors.append(
                            f"Forbidden file type '{candidate}' in submodule: {rel_path}"
                        )
                        break


def scan_file_contents(file_paths, repo_root, errors):
    """Scan text files for secret patterns and forbidden content."""
    for rel_path in file_paths:
        full_path = repo_root / rel_path
        if not full_path.is_file():
            continue
        if is_binary_file(full_path):
            continue

        try:
            text = full_path.read_text(encoding="utf-8", errors="replace")
        except (OSError, PermissionError):
            continue

        for line_num, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            if not stripped:
                continue
            for pattern_name, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    errors.append(
                        f"{pattern_name} in {rel_path}:{line_num}"
                    )


def scan(repo_root=None, file_paths=None, check_upstream=True):
    """
    Run all hygiene checks. Returns list of errors (empty = pass).

    Args:
        repo_root: Repository root path. Auto-detected if None.
        file_paths: List of relative file path strings to scan.
                    If None, uses git ls-files (tracked files only).
        check_upstream: Whether to check sources/upstream/ directory.
    """
    if repo_root is None:
        repo_root = find_repo_root()
    errors = []

    # Determine file list
    if file_paths is None:
        try:
            file_paths = get_git_files(repo_root, include_untracked=False)
        except RuntimeError as e:
            errors.append(str(e))
            return errors

    # Scan for forbidden extensions
    scan_forbidden_extensions(file_paths, repo_root, errors)

    # Check upstream directory
    if check_upstream:
        scan_upstream_dir(repo_root, errors)

    # Check submodule working trees for forbidden file types
    scan_submodule_forbidden_files(repo_root, errors)

    # Scan file contents for secret patterns
    scan_file_contents(file_paths, repo_root, errors)

    return errors


def main():
    repo_root = find_repo_root()
    include_untracked = "--all" in sys.argv

    if include_untracked:
        try:
            file_paths = get_git_files(repo_root, include_untracked=True)
        except RuntimeError as e:
            print("HYGIENE CHECK FAILED", file=sys.stderr)
            print(f"  - {e}", file=sys.stderr)
            sys.exit(1)
        errors = scan(repo_root, file_paths=file_paths)
    else:
        errors = scan(repo_root)

    if errors:
        print("HYGIENE CHECK FAILED", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    print("All repository hygiene checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
