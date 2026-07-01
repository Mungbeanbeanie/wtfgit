from dataclasses import dataclass, field
from typing import List


@dataclass
class GitState:
    """Holds the current diagnostic state of the Git repository."""
    current_branch: str = ""
    is_merging: bool = False
    is_rebasing: bool = False
    untracked_files: List[str] = field(default_factory=list)
    modified_files: List[str] = field(default_factory=list)
    staged_files: List[str] = field(default_factory=list)
    conflicted_files: List[str] = field(default_factory=list)

    # We will add more fields (commits behind/ahead) as we expand the parser
