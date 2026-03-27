---
name: gen-branch-audit
description: Audit all claude/* branches in the Sanskrit parser repo and show their status. Use when the user asks to audit branches, check which sessions are active, see which branches have unmerged generator changes, check branch status, or runs /gen-branch-audit. Shows three columns per branch: active session (worktree present), uncommitted changes, and unmerged commits into the generator branch. Optional arguments: branch suffixes to skip (e.g. "ecstatic-colden wizardly-shaw").
argument-hint: "[branch-suffix-to-skip ...]"
allowed-tools: Bash
---

# Generator Branch Audit

Audit all `claude/*` branches and report their status across three dimensions.

## Arguments

`$ARGUMENTS` is an optional space-separated list of branch suffixes (or full `claude/foo` names) to exclude from the report.

---

## Step 1 — List branches

```bash
REPO=/Users/karthik/personal_projects/sanskrit_parser
git -C "$REPO" branch --list 'claude/*' --format='%(refname:short)' --sort=-committerdate
```

Parse `$ARGUMENTS` to build a skip list. For each branch name in the output, skip it if:
- The full name (e.g. `claude/ecstatic-colden`) matches a skip argument, OR
- The suffix (e.g. `ecstatic-colden`) matches a skip argument.

---

## Step 2 — For each branch, check three things

Derive `session` = branch name with `claude/` stripped (e.g. `claude/heuristic-elion` → `heuristic-elion`).
Set `WORKTREE="$REPO/.claude/worktrees/$session"`.

### a) Active session
```bash
[ -d "$WORKTREE" ] && echo "yes" || echo "no"
```

### b) Uncommitted changes (only if active session = yes)
```bash
git -C "$WORKTREE" status --short 2>/dev/null
```
- Empty output → **clean**
- Non-empty output → **dirty** (show the count or a brief summary)
- If no active session → show `—`

### c) Unmerged into generator
```bash
git -C "$REPO" log generator.."$branch" --oneline 2>/dev/null
```
- Empty → **none**
- Non-empty → show commit count (e.g. **3 commits**) and the first line of the most recent commit
- If local `generator` branch is absent, fall back to `origin/generator` and note the fallback.

---

## Step 3 — Present as a table

Output a markdown table sorted by most-recently-committed branch first:

| Branch | Active Session | Uncommitted | Unmerged into generator |
|--------|---------------|-------------|------------------------|
| `claude/heuristic-elion` | yes | clean | none |
| `claude/gifted-khorana` | yes | clean | none |
| `claude/elated-noether` | no | — | none |
| `claude/wizardly-shaw` | no | — | 2 commits — "Implement SK..." |

After the table, call out any branches that need attention:
- **Has unmerged changes** — these should be merged into `generator` or investigated
- **Has uncommitted changes** — the session is active with pending work

If all branches are clean and fully merged, say so briefly.
