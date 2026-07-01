import sys
from src.scanner import git_ops
from src.models.state import GitState


def main():
    print("🔍 wtfgit is analyzing your repository...\n")

    # 1. Pre-flight check: Are we in a git repo?
    git_dir = git_ops.get_git_dir()
    if "fatal: not a git repository" in git_dir.lower():
        print("buddy ur not even in a git repo. Make sure to do git clone [ssh/https link] or git init first.")
        sys.exit(1)

    # 2. SCAN: Gather raw data
    raw_branch = git_ops.get_current_branch()
    raw_status = git_ops.get_status_porcelain()
    commits_ahead, commits_behind = git_ops.get_log_ahead_behind(raw_branch)
    

    # 3. INITIALIZE STATE
    files = git_ops.parse_porcelain(raw_status)
    state = GitState(
        current_branch=raw_branch,
        untracked_files=files["untracked"],
        modified_files=files["modified"],
        staged_files=files["staged"],
        conflicted_files=files["conflicted"],
        commits_ahead=commits_ahead,
        commits_behind=commits_behind
    )



if __name__ == "__main__":
    main()
