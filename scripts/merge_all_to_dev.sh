#!/usr/bin/env bash
set -euo pipefail

REMOTE="origin"
TARGET_BRANCH="dev"
BASE_BRANCH="main"
PUSH_AFTER_MERGE=false
DELETE_MERGED=false

usage() {
  cat <<USAGE
Usage: ${0##*/} [options]

Options:
  -r, --remote <name>        Remote to operate against (default: origin)
  -t, --target <branch>      Target branch that receives all merges (default: dev)
  -b, --base <branch>        Fallback branch to create target from if missing (default: main)
      --push                 Push the updated target branch back to the remote when done
      --delete-merged        Delete remote branches that merge successfully into the target
  -h, --help                 Show this help message

The script expects a clean working tree and an existing Git remote. Conflicts
stop the current merge so you can resolve them manually.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -r|--remote)
      [[ $# -ge 2 ]] || { echo "Missing value for $1" >&2; exit 1; }
      REMOTE="$2"
      shift 2
      ;;
    -t|--target)
      [[ $# -ge 2 ]] || { echo "Missing value for $1" >&2; exit 1; }
      TARGET_BRANCH="$2"
      shift 2
      ;;
    -b|--base)
      [[ $# -ge 2 ]] || { echo "Missing value for $1" >&2; exit 1; }
      BASE_BRANCH="$2"
      shift 2
      ;;
    --push)
      PUSH_AFTER_MERGE=true
      shift
      ;;
    --delete-merged)
      DELETE_MERGED=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "This script must be run inside a Git repository." >&2
  exit 1
fi

if [[ -n $(git status --porcelain) ]]; then
  echo "Working tree is not clean. Commit or stash your changes before running this script." >&2
  exit 1
fi

if ! git remote get-url "$REMOTE" >/dev/null 2>&1; then
  echo "Remote '$REMOTE' is not configured." >&2
  exit 1
fi

echo "Fetching latest refs from $REMOTE..."
git fetch "$REMOTE" --prune

if ! git show-ref --verify --quiet "refs/remotes/$REMOTE/$BASE_BRANCH"; then
  echo "Base branch '$BASE_BRANCH' not found on remote '$REMOTE'." >&2
  exit 1
fi

checkout_target_branch() {
  if git show-ref --verify --quiet "refs/heads/$TARGET_BRANCH"; then
    git checkout "$TARGET_BRANCH"
  elif git show-ref --verify --quiet "refs/remotes/$REMOTE/$TARGET_BRANCH"; then
    git checkout -B "$TARGET_BRANCH" "$REMOTE/$TARGET_BRANCH"
  else
    echo "Target branch '$TARGET_BRANCH' missing locally and on remote; creating from $BASE_BRANCH." >&2
    git checkout -B "$TARGET_BRANCH" "$REMOTE/$BASE_BRANCH"
  fi
}

checkout_target_branch

mapfile -t REMOTE_BRANCHES < <(git for-each-ref --format='%(refname:strip=2)' "refs/remotes/$REMOTE")

if [[ ${#REMOTE_BRANCHES[@]} -eq 0 ]]; then
  echo "No remote branches found under '$REMOTE'."
  exit 0
fi

SKIPPED=()
MERGED=()
FAILED=()

for BRANCH in "${REMOTE_BRANCHES[@]}"; do
  if [[ "$BRANCH" == "HEAD" || "$BRANCH" == "$TARGET_BRANCH" || "$BRANCH" == "$BASE_BRANCH" ]]; then
    SKIPPED+=("$BRANCH")
    continue
  fi

  echo "\nMerging $REMOTE/$BRANCH into $TARGET_BRANCH..."
  git checkout "$TARGET_BRANCH"
  if git merge --no-ff --no-edit --log "$REMOTE/$BRANCH"; then
    MERGED+=("$BRANCH")
    if $DELETE_MERGED; then
      echo "Deleting remote branch $BRANCH..."
      git push "$REMOTE" --delete "$BRANCH"
    fi
  else
    echo "Merge of $REMOTE/$BRANCH failed. Aborting merge." >&2
    git merge --abort || true
    FAILED+=("$BRANCH")
  fi
done

echo "\nSummary:"
if [[ ${#MERGED[@]} -gt 0 ]]; then
  printf '  Merged:\n'
  printf '    - %s\n' "${MERGED[@]}"
fi
if [[ ${#SKIPPED[@]} -gt 0 ]]; then
  printf '  Skipped:\n'
  printf '    - %s\n' "${SKIPPED[@]}"
fi
if [[ ${#FAILED[@]} -gt 0 ]]; then
  printf '  Failed (requires manual resolution):\n'
  printf '    - %s\n' "${FAILED[@]}"
fi

if $PUSH_AFTER_MERGE; then
  echo "\nPushing $TARGET_BRANCH to $REMOTE..."
  git push "$REMOTE" "$TARGET_BRANCH"
fi

if [[ ${#FAILED[@]} -gt 0 ]]; then
  echo "Some merges failed. Resolve conflicts on $TARGET_BRANCH and rerun as needed." >&2
  exit 1
fi

echo "All requested branches processed successfully."
