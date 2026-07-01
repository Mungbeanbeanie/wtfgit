import subprocess


def _run_git_command(args: list[str]) -> str:
    """Executes a git command and returns the standard output."""
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
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
