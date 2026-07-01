import sys
from src.scanner import git_ops
from src.models.state import GitState


def main():
    print("🔍 wtfgit is analyzing your repository...\n")

    # 1. Pre-flight check: Are we in a git repo?
    git_dir = git_ops.get_git_dir()
    if "fatal: not a git repository" in git_dir.lower():
        print("❌ Relax. You aren't even in a Git repository right now.")
        sys.exit(1)

    # 2. SCAN: Gather raw data
    raw_branch = git_ops.get_current_branch()
    raw_status = git_ops.get_status_porcelain()

    # 3. INITIALIZE STATE
    state = GitState(
        current_branch=raw_branch
    )

    # Temporary printout to verify our scanner works
    print(f"Current Branch: {state.current_branch}")
    print("-" * 30)
    print("Raw '--porcelain' Status:")
    if raw_status:
        print(raw_status)
    else:
        print("(Working directory is clean)")


if __name__ == "__main__":
    main()
