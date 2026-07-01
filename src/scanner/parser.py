def parse_porcelain(raw_status: str) -> dict[str, list[str]]:
    """
    Parses `git status --porcelain` output into categorized file lists.

    Each line is 'XY <path>' where X is the index (staged) state and Y is
    the working-tree state.
    """
    categories: dict[str, list[str]] = {
        "untracked": [],
        "modified": [],
        "staged": [],
        "conflicted": [],
    }

    for line in raw_status.splitlines():
        if not line:
            continue
        code = line[:2]
        path = line[3:]
        index_state, worktree_state = code[0], code[1]

        # Untracked files
        if code == "??":
            categories["untracked"].append(path)
            continue

        # Merge conflicts: any 'U', or both sides added/deleted
        if "U" in code or code in ("AA", "DD"):
            categories["conflicted"].append(path)
            continue

        # Staged: the index side has a change
        if index_state not in (" ", "?"):
            categories["staged"].append(path)

        # Modified/deleted in the working tree
        if worktree_state in ("M", "D"):
            categories["modified"].append(path)

    return categories
