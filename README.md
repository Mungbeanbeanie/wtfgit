# wtfgit

For when you go **"wtf, git?"**

Run `wtfgit` in any repository and it tells you, in plain English:

- **What's wrong** — the most urgent problem first (merge conflict? detached HEAD? diverged branch?), plus everything else it found
- **Why it happened** — a short explanation so you actually learn git, not just copy-paste
- **Exactly how to fix it** — the commands to run, each with a one-line note on what it does
- **Where you are** — a visual graph of your recent commit history

wtfgit is **read-only**. It never touches your repo — it just tells you what to type.

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/Mungbeanbeanie/wtfgit/main/install.sh | bash
```

That's it. Requires `git` and `python3` (already on virtually every dev machine).

## Use

```bash
cd your-repo
wtfgit
```

Example output:

```
 wtfgit — here's what's going on

 On: main  → origin/main ↑2 ↓3

 ▶ MOST URGENT: Branch diverged from origin/main
   You have 2 local commit(s) the remote doesn't have, and the remote has
   3 commit(s) you don't have. This happens when you and someone else both
   committed since the last sync. A plain `git push` will be rejected until
   you combine the two histories.

   How to fix it:
     $ git pull --rebase
       replay your commits on top of the remote's (clean, linear history)
     $ git pull
       or merge the remote's commits into yours (creates a merge commit)
     $ git push
       then push the combined result

 ── recent history ──────────────────────────────────────────
   * a1b2c3d (HEAD -> main) my local work
   | * e4f5g6h (origin/main) teammate's change
   |/
   * 9i8j7k6 last common commit
```

## What it detects

Merge conflicts · rebase / cherry-pick / revert / bisect stuck mid-operation ·
detached HEAD (and commits stranded on it) · diverged / behind / ahead of remote ·
missing upstream · no remote · staged-but-uncommitted, unstaged, and untracked
files · forgotten stashes · brand-new repos with no commits · stale `index.lock` ·
not being in a repo at all.

## Uninstall

```bash
rm ~/.local/bin/wtfgit
```

## Development

Everything lives in one file: [`wtfgit`](wtfgit). Tests: `python3 test_wtfgit.py`.
