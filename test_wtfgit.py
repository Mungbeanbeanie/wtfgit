#!/usr/bin/env python3
"""Tests for wtfgit. Run: python3 test_wtfgit.py (also pytest-compatible)."""
import importlib.util
import os
import subprocess
import tempfile
from importlib.machinery import SourceFileLoader
from pathlib import Path

HERE = Path(__file__).parent
_loader = SourceFileLoader("wtfgit", str(HERE / "wtfgit"))
_spec = importlib.util.spec_from_loader("wtfgit", _loader)
w = importlib.util.module_from_spec(_spec)
import sys; sys.modules["wtfgit"] = w  # dataclasses resolve annotations via sys.modules
_loader.exec_module(w)


# ----------------------------------------------------------- parser tests ---

def test_parse_clean():
    s = w.parse_status_v2("# branch.oid abc123\n# branch.head main\n"
                          "# branch.upstream origin/main\n# branch.ab +0 -0")
    assert s.branch == "main" and s.upstream == "origin/main"
    assert s.ahead == 0 and s.behind == 0
    assert not (s.staged or s.modified or s.untracked or s.conflicted)


def test_parse_diverged_and_files():
    raw = "\n".join([
        "# branch.oid abc123",
        "# branch.head feature",
        "# branch.upstream origin/feature",
        "# branch.ab +2 -3",
        "1 .M N... 100644 100644 100644 aaa bbb src/app.py",
        "1 M. N... 100644 100644 100644 aaa bbb staged.py",
        "1 MM N... 100644 100644 100644 aaa bbb both.py",
        "2 R. N... 100644 100644 100644 aaa bbb R100 new name.py\told.py",
        "u UU N... 100644 100644 100644 100644 aaa bbb ccc conflict.py",
        "? notes.txt",
    ])
    s = w.parse_status_v2(raw)
    assert s.ahead == 2 and s.behind == 3
    assert s.modified == ["src/app.py", "both.py"]
    assert s.staged == ["staged.py", "both.py", "new name.py"]  # rename keeps new path
    assert s.conflicted == ["conflict.py"]
    assert s.untracked == ["notes.txt"]


def test_parse_detached_and_unborn():
    assert w.parse_status_v2("# branch.oid abc\n# branch.head (detached)").detached
    assert w.parse_status_v2("# branch.oid (initial)\n# branch.head main").unborn


# ----------------------------------------------------------- triage tests ---

def _diag(**kw):
    return w.diagnose(w.GitState(**kw))


def test_clean_repo_no_issues():
    assert _diag(branch="main", upstream="origin/main", remotes=["origin"]) == []


def test_merge_conflict_beats_everything():
    issues = _diag(branch="main", merging=True, conflicted=["a.py"],
                   untracked=["x"], ahead=2, upstream="origin/main",
                   remotes=["origin"], stash_count=1)
    assert "Merge in progress" in issues[0].title
    assert len(issues) > 1  # secondary issues still reported


def test_detached_with_orphans_warns():
    issues = _diag(detached=True, head_short="abc1234", orphan_commits=2, remotes=["origin"])
    assert "Detached HEAD" in issues[0].title
    assert "rescue-branch" in issues[0].fixes[0][0]


def test_diverged_outranks_behind_and_ahead():
    d = _diag(branch="m", upstream="origin/m", ahead=1, behind=1, remotes=["origin"])
    assert "diverged" in d[0].title
    b = _diag(branch="m", upstream="origin/m", behind=3, remotes=["origin"])
    assert "Behind" in b[0].title
    a = _diag(branch="m", upstream="origin/m", ahead=3, remotes=["origin"])
    assert "unpushed" in a[0].title


def test_no_upstream_only_when_remote_exists():
    assert any("no upstream" in i.title for i in _diag(branch="feat", remotes=["origin"]))
    assert not any("no upstream" in i.title for i in _diag(branch="feat"))


# ------------------------------------------------------------- e2e smoke ----

def _run_wtfgit(cwd):
    env = dict(os.environ, NO_COLOR="1")
    return subprocess.run(["python3", str(HERE / "wtfgit")],
                          capture_output=True, text=True, cwd=cwd, env=env)


def _sh(cwd, *cmd):
    subprocess.run(cmd, cwd=cwd, capture_output=True, check=True)


def test_e2e_not_a_repo():
    with tempfile.TemporaryDirectory() as d:
        r = _run_wtfgit(d)
        assert r.returncode == 1 and "not in a git repository" in r.stdout


def test_e2e_merge_conflict():
    with tempfile.TemporaryDirectory() as d:
        _sh(d, "git", "init", "-b", "main")
        _sh(d, "git", "config", "user.email", "t@t.co")
        _sh(d, "git", "config", "user.name", "t")
        Path(d, "f.txt").write_text("base\n")
        _sh(d, "git", "add", "."); _sh(d, "git", "commit", "-m", "base")
        _sh(d, "git", "switch", "-c", "other")
        Path(d, "f.txt").write_text("theirs\n")
        _sh(d, "git", "commit", "-am", "theirs")
        _sh(d, "git", "switch", "main")
        Path(d, "f.txt").write_text("ours\n")
        _sh(d, "git", "commit", "-am", "ours")
        subprocess.run(["git", "merge", "other"], cwd=d, capture_output=True)  # conflicts
        out = _run_wtfgit(d).stdout
        assert "Merge in progress" in out and "git merge --abort" in out


def test_e2e_clean_and_detached():
    with tempfile.TemporaryDirectory() as d:
        _sh(d, "git", "init", "-b", "main")
        _sh(d, "git", "config", "user.email", "t@t.co")
        _sh(d, "git", "config", "user.name", "t")
        Path(d, "f.txt").write_text("hi\n")
        _sh(d, "git", "add", "."); _sh(d, "git", "commit", "-m", "one")
        assert "No remote configured" in _run_wtfgit(d).stdout
        with tempfile.TemporaryDirectory() as rd:  # bare remote outside the worktree
            _sh(d, "git", "init", "--bare", rd)
            _sh(d, "git", "remote", "add", "origin", rd)
            _sh(d, "git", "push", "-u", "origin", "main")
            assert "Nothing wtf here" in _run_wtfgit(d).stdout
        _sh(d, "git", "checkout", "--detach")
        assert "Detached HEAD" in _run_wtfgit(d).stdout


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"✓ {fn.__name__}")
    print(f"\n{len(fns)} tests passed")
