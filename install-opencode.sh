#!/usr/bin/env bash
set -euo pipefail

if [ -z "${BASH_VERSION:-}" ]; then
    echo "ERROR: This script requires bash." >&2
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found in PATH." >&2
    exit 1
fi

check_repo_root() {
    if [ ! -f "references.yaml" ]; then
        echo "ERROR: Cannot find references.yaml. Run from the repository root." >&2
        exit 1
    fi
}

resolve_path() {
    if command -v realpath &>/dev/null; then
        realpath "$1"
    elif command -v readlink &>/dev/null && readlink -f . &>/dev/null; then
        readlink -f "$1"
    else
        python3 -c "import os,sys; print(os.path.realpath(sys.argv[1]))" "$1"
    fi
}

show_help() {
    cat <<EOF
Usage: install-opencode.sh [COMMAND]

Install, update, validate, or uninstall the /ref-bio OpenCode skill.

Commands:
  --project PATH                  Install the /ref-bio skill into a downstream
                                  project at PATH/.opencode/skills/ref-bio/
  --target PATH                   Alias for --project PATH
  --project PATH --force          Overwrite an existing installation
  --project PATH --dry-run        Print actions without writing
  --project PATH --verbose        Print detailed actions
  --project PATH --update         Reinstall (requires existing installation)
  --project PATH --uninstall      Remove the /ref-bio skill from a project
  --list                          List available skills (ref-bio only)
  --validate                      Run repository validation checks
  --help                          Show this help message

Examples:
  ./install-opencode.sh --project ../my-analysis-project
  ./install-opencode.sh --project ../my-analysis-project --dry-run --verbose
  ./install-opencode.sh --project ../my-analysis-project --update
  ./install-opencode.sh --project ../my-analysis-project --uninstall
  ./install-opencode.sh --list
  ./install-opencode.sh --validate
EOF
}

run_validate() {
    check_repo_root
    if $VERBOSE; then
        echo "[verbose] Running validation sequence (6 steps)"
    fi
    echo "[1/6] validate_metadata.py"
    python3 scripts/validate_metadata.py
    echo "[2/6] scan_repo_hygiene.py --all"
    python3 scripts/scan_repo_hygiene.py --all
    echo "[3/6] export_project_reference.py"
    python3 scripts/export_project_reference.py
    echo "[4/6] build_release_manifest.py"
    python3 scripts/build_release_manifest.py
    echo "[5/6] verify_export_bundle.py"
    python3 scripts/verify_export_bundle.py
    echo "[6/6] export_opencode_skill.py"
    python3 scripts/export_opencode_skill.py
    echo ""
    echo "All validations passed. Generated exports/ is intentionally git-ignored."
}

do_install() {
    local project="$1"
    local dest="$project/.opencode/skills/ref-bio"
    if $VERBOSE; then
        echo "[verbose] Target project: $project"
        echo "[verbose] Install destination: $dest"
    fi

    local -a cmd=(python3 scripts/install_opencode_skill.py --target "$project")
    $FORCE && cmd+=(--force)
    $DRY_RUN && cmd+=(--dry-run)
    if $VERBOSE; then
        echo "[verbose] Running: ${cmd[*]}"
    fi

    "${cmd[@]}"
}

do_update() {
    local project="$1"
    local dest="$project/.opencode/skills/ref-bio"

    if $VERBOSE; then
        echo "[verbose] Checking for existing installation at: $dest"
    fi

    if [ ! -d "$dest" ]; then
        echo "ERROR: /ref-bio is not currently installed at: $dest" >&2
        echo "To install for the first time, run:" >&2
        echo "  ./install-opencode.sh --project $project" >&2
        exit 1
    fi

    if $VERBOSE; then
        echo "[verbose] Existing installation found. Reinstalling with --force."
    fi
    echo "Reinstalling /ref-bio skill at $dest"
    python3 scripts/install_opencode_skill.py --target "$project" --force
}

do_uninstall() {
    local project="$1"
    local dest="$project/.opencode/skills/ref-bio"

    if $VERBOSE; then
        echo "[verbose] Uninstall destination: $dest"
    fi

    if [ ! -d "$dest" ]; then
        echo "ERROR: /ref-bio is not currently installed at: $dest" >&2
        exit 1
    fi

    if $DRY_RUN; then
        echo "Would remove: $dest"
    else
        rm -rf "$dest"
        echo "Removed: $dest"
        if $VERBOSE; then
            echo "[verbose] Directory removed successfully."
        fi
    fi
}

# --- Parse arguments ---
PROJECT=""
FORCE=false
DRY_RUN=false
VERBOSE=false
UPDATE=false
UNINSTALL=false
LIST=false
VALIDATE=false
HELP=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --project|--target)
            if [ -z "${2:-}" ]; then
                echo "ERROR: --project requires a path argument." >&2
                exit 1
            fi
            PROJECT="$(resolve_path "$2")"
            shift 2
            ;;
        --force) FORCE=true; shift ;;
        --dry-run) DRY_RUN=true; shift ;;
        --verbose) VERBOSE=true; shift ;;
        --update) UPDATE=true; shift ;;
        --uninstall) UNINSTALL=true; shift ;;
        --list) LIST=true; shift ;;
        --validate) VALIDATE=true; shift ;;
        --help) HELP=true; shift ;;
        *)
            echo "ERROR: Unknown option: $1" >&2
            show_help
            exit 1
            ;;
    esac
done

# --- Dispatch ---
if $HELP; then
    show_help
    exit 0
fi

if $LIST; then
    check_repo_root
    echo "ref-bio  /ref-bio  (explicit-trigger only)"
    echo "  Source-first, link-resolved, license-aware bioinformatics reference registry."
    exit 0
fi

if $VALIDATE; then
    run_validate
    exit 0
fi

if [ -n "$PROJECT" ]; then
    if $UNINSTALL; then
        do_uninstall "$PROJECT"
        exit 0
    fi

    if $UPDATE; then
        do_update "$PROJECT"
        exit 0
    fi

    do_install "$PROJECT"
    exit $?
fi

show_help
exit 1
