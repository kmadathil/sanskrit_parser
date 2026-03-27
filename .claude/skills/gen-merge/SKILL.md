---
name: gen-merge
description: Sanskrit generator parallel-session merger. Invoke when a user has been running parallel worktree sessions to implement Sanskrit sutra rules and now wants those sessions merged into a single branch. The core trigger is finished parallel work awaiting combination — the user says their sessions are done/complete/finished and asks to merge or combine them. Works whether they name specific worktrees (elated-noether, gifted-khorana, etc.), say "the two sessions", or explicitly request a "gen-merge". Handles generator_status.md conflict resolution correctly. Do not invoke for general merge conflicts, implementing new sutras, adding tests, or running the test suite.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Generator Session Merge

Merge two (or more) parallel generator worktree branches into the current branch — resolving conflicts correctly and verifying all tests pass.

## Arguments

`$ARGUMENTS` should name the two (or more) sessions to merge, e.g. `elated-noether gifted-khorana`. If the session names aren't provided, look for recently active worktrees under `.claude/worktrees/`.

---

## Codebase context

| File | Conflict likelihood |
|------|-------------------|
| `generator/sutras_antaranga.yaml` | Low — additions are in disjoint SK-number regions |
| `generator/test/vibhaktis_list.py` | Low — each session adds/modifies different stems |
| `generator/test/conftest.py` | Medium — conflicts if both sessions added test infrastructure |
| `generator/generator_status.md` | **High** — always conflicts; see rules below |
| `generator/paribhasha.py`, `pratipadika.py`, `paninian_object.py`, `pratyaya.py`, `test/manual_list.py` | Low — sessions typically touch independent things |

---

## Step 1 — Identify branches and baseline

1. Find the branch name for each session:
   ```bash
   git -C .claude/worktrees/<session-name> branch --show-current
   ```
2. Note the master baseline: read the **Summary** table in `generator_status.md` on master (or the current HEAD before any merge) — you'll need the baseline `implemented` and `skipped` counts later.

---

## Step 2 — Merge branch 1 (expect no conflicts)

```bash
git merge <branch-1> --no-commit --no-ff
```

Verify it's clean (`git diff --stat --cached` shows only expected files, no conflict markers). Then commit:

```bash
git commit -m "Merge <branch-1>: <brief description of what it implemented>"
```

---

## Step 3 — Merge branch 2 (expect conflicts in generator_status.md)

```bash
git merge <branch-2> --no-commit --no-ff
```

Check which files conflict:
```bash
git diff --name-only --diff-filter=U
```

`sutras_antaranga.yaml`, `vibhaktis_list.py`, and most other files should auto-merge cleanly. If `conftest.py` conflicts, see the conftest section below.

---

## Step 4 — Resolve generator_status.md conflicts

This file almost always has three conflict regions. Resolve each as follows.

### 4a. "Last implemented" line

Find the `<<<<<<` block at the top of the file. Each branch has a different **Last implemented** SK number.

**Critical:** Do NOT just pick the higher of the two conflict sides. The target branch may already contain higher in-sequence entries that don't appear in the conflict block at all (e.g. if a session branched off from an older point and only updated the status file to reflect its own work).

**Correct procedure:**

1. Resolve the conflict markers (tentatively pick the higher side).
2. After resolving **all** conflicts, scan the `## Implemented Sutras (SK order)` table for the true highest in-sequence SK:
   ```bash
   grep "^| [0-9]" generator_status.md | awk -F'|' '{print $2+0}' | sort -n | tail -20
   ```
   The highest SK number present in the implemented table that is part of the main sequence (not an out-of-order addition) is the correct **Last implemented**.
3. Cross-check with the **Next to implement** value — `Last implemented + 1` (accounting for skipped/deferred) should equal `Next`.

> **Rule:** Last implemented = highest in-sequence SK present in the implemented table.
> Out-of-order sutras (e.g. SK438 added alongside SK419) are noted separately, not used as the "last".

Mention all sessions' contributions in the resolved line, e.g.:
```
**Last implemented:** SK 425 — 6.4.14 ... (in-sequence); also SK 415–420 añcatir cluster, SK 419/438/439 adas pronoun out of SK order
```

For **Next to implement**, use the "next" from whichever branch is furthest ahead in sequence.

### 4b. Summary count table

Find the `<<<<<<` block in the Summary table. Compute the merged counts:

- **Implemented**: `master_base + delta_branch1 + delta_branch2`
  Each branch's delta = its `implemented` count − master_base.
- **Skipped/deferred**: Do **not** compute arithmetically. After resolving all conflicts, count the actual rows in the `## Skipped / Deferred Sutras` table and use that number.

### 4c. Implemented sutras table

Find the `<<<<<<` block in the `## Implemented Sutras (SK order)` table. Keep **all rows from both branches** — one branch's new rows should not replace the other's. Arrange in SK number order; out-of-order sutras go at the end (after the highest in-sequence row).

### 4d. Deferred table (usually auto-merged correctly)

After all conflicts are resolved, verify:
- Sutras newly implemented by either branch are **absent** from the deferred table.
- Any sutras reclassified (e.g. to "Natural Siddha") by either branch reflect the more-accurate classification.

---

## Step 5 — Resolve conftest.py conflicts (if any)

If both sessions added test infrastructure, each feature is independent and both should survive. Common patterns:

| Session adds | Keep |
|---|---|
| `stem_key` parameter + `_VIBHAKTI_ROW_NAMES`/`_COL_NAMES` + `None` skip logic | Yes — richer test IDs |
| `!` suffix in `_gen_obj()` for raw phonetic input | Yes — needed for enclitic tests |

Take the version that has more features and manually splice in whatever the other session added.

---

## Step 6 — Commit and verify

```bash
git add -A
git commit -m "Merge <branch-2>: <brief description>"
```

Then run the full test suite:
```bash
cd sanskrit_parser/generator/test
PYTHONPATH=<worktree-root> /Users/karthik/venvs/sanskrit/bin/pytest -n 6
```

All tests must pass. If any fail, diagnose before proceeding — don't paper over failures.

---

## Checklist before declaring done

- [ ] All new sutras from both sessions present in `sutras_antaranga.yaml`
- [ ] All new pratipadika/vibhakti tests present in `vibhaktis_list.py`
- [ ] `generator_status.md` has correct Last/Next, correct implemented count, all new rows in the table, correct deferred table
- [ ] No `<<<<<<<` conflict markers remain anywhere
- [ ] All tests pass
