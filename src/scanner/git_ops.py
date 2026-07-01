import subprocess

def _run_git_command(args: list[str]) -> str:
    """Executes a git command and returns the standard output."""
    try:
        # check=False allows us to handle errors manually if needed
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        # If the command fails (e.g., fatal: not a git repository)
        return e.stderr.strip()

def get_current_branch() -> str:
    """Returns the name of the current branch."""
    return _run_git_command(["branch", "--show-current"])

def get_status_porcelain() -> str:
    """
    Returns machine-readable status output. 
    Crucial for identifying modified, untracked, and conflicted files safely.
    """
    return _run_git_command(["status", "--porcelain"])

def get_git_dir() -> str:
    """Checks if we are actually in a git repository."""
    return _run_git_command(["rev-parse", "--git-dir"])

def get_merge_state() -> str:
    """Checks if the repository is currently in a merge state."""
    return _run_git_command(["rev-parse", "--is-merging"])

def get_rebase_state() -> str:
    """Checks if the repository is currently in a rebase state."""
    return _run_git_command(["rev-parse", "--is-rebasing"])

def get_log_ahead_behind(branch: str) -> tuple[int, int]:
    """
    Returns a tuple (ahead_count, behind_count) for the given branch.
    This is useful for determining how many commits the local branch is ahead or behind its remote counterpart.
    """
    output = _run_git_command(["rev-list", "--left-right", "--count", f"{branch}...origin/{branch}"])
    if output:
        ahead, behind = map(int, output.split())
        return ahead, behind
    return 0, 0