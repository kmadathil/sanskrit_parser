---
name: gen-debug
description: Debug unexpected rule firing or wrong output in the Sanskrit parser generator. Use when a prakriya produces the wrong form, a rule fires unexpectedly, or a rule fails to fire when expected.
argument-hint: "[pratipadika+pratyaya or description of wrong output]"
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Generator Prakriya Debugger

Debug the generator output for `$ARGUMENTS`.

## Codebase Context

| File | Role |
|------|------|
| `sanskrit_parser/generator/sutras_antaranga.yaml` | Sutra rules DSL |
| `sanskrit_parser/generator/paribhasha.py` | Helper functions (`$$fname`) |
| `sanskrit_parser/generator/process_yaml.py` | DSL evaluator — condition/xform dispatch |
| `sanskrit_parser/generator/antaranga_prakriya.py` | Prakriya engine and override enforcement |
| `sanskrit_parser/generator/paninian_object.py` | PaninianObject class (tags, canonical, hasTag) |
| `sanskrit_parser/generator/test/debug.py` | Manual debug runner (verbose output) |
| `sanskrit_parser/generator/cmd_line.py` | `sanskrit_generator` CLI |
| `Generator.md` | Developer guide: module structure, core objects, engine loop, YAML DSL, rule priority |

---

## Step 1 — Reproduce the Issue

### Option A: CLI (quick single-form check)

```bash
# Activate the venv and set PYTHONPATH first:
source /Users/karthik/venvs/sanskrit/bin/activate
export PYTHONPATH=/Users/karthik/personal_projects/sanskrit_parser

cd /Users/karthik/personal_projects/sanskrit_parser
# Single form: pratipadika + pratyaya
python scripts/sanskrit_generator -t <pratipadika> -p <pratyaya> -a --verbose --show-tags

# All vibhaktis for a pratipadika
python scripts/sanskrit_generator -t <pratipadika> --vibhakti --verbose 

# Generate vibhakti test skeleton
python scripts/sanskrit_generator -t <pratipadika> --vibhakti --gen-test

# Add --debug for full file logging (SanskritGenerator.log)
rm -f SanskritGenerator.log && python scripts/sanskrit_generator -t <pratipadika> -p <pratyaya> -a --verbose --debug
```

CLI flags reference:
| Flag | Meaning |
|------|---------|
| `-t <name>` | Use a named pratipadika (must be importable from pratipadika.py) |
| `-p <name>` | Use a named pratyaya (from pratyaya.py) |
| `-d <name>` | Use a named dhatu |
| `-s <slp1-string*>` | Use a raw SLP1 string with aNga tag (`*`) or pada tag (`_`) |
| `-a` | Append avasāna (required to terminate the prakriya) |
| `--vibhakti` | Run all 8×3 vibhakti combinations |
| `--verbose` | Print each sutra step to console |
| `--debug` | Enable DEBUG-level file logging |
| `--gen-test` | Print viBakti[] test skeleton |

### Option B: debug.py (for complex or multi-step cases)

Edit `sanskrit_parser/generator/test/debug.py` to add the failing case:

```python
# For a pratipadika + pratyaya pair:
test_list = [
    (parvan_napum, am, "पर्वण"),  # <- add failing case; expected in last slot
]

# For a vibhakti table:
prAtipadika["parvan"] = parvan_napum
viBakti["parvan"] = [...]   # your expected table
```

Run it:
```bash
cd /Users/karthik/personal_projects/sanskrit_parser/sanskrit_parser/generator/test
python debug.py
```

debug.py enables `enable_file_logger(level=logging.DEBUG)` automatically — check `sanskrit_generator.log` for full trace.

---

## Step 2 — Read the Verbose Trace

`--verbose` output shows each step of the prakriya. Example trace format:

```
INFO  Applying 7.1.23 अमि पूर्वः  lp=parvan rp=am → luk
INFO  Applying 8.4.2.1 अट्कुप्वाङ्नुम्व्यवायेऽपि  lp=parvan rp='' → l: R
```

For each step, note:
1. Which sutra id fired
2. What the `lp`/`rp` values were at that moment
3. What xform was applied

**Key question**: Is the rule firing *before* or *after* another rule that should have changed the state?

---

## Step 3 — Locate the Firing Rule in the YAML

```bash
grep -n "<sutra-id>" sanskrit_parser/generator/sutras_antaranga.yaml
# Read 20 lines around it:
grep -n -A 15 "id: <sutra-id>" sanskrit_parser/generator/sutras_antaranga.yaml
```

Check:
- `condition:` fields — which fields are tested (`lp`, `rp`, `l`, `r`, `ll`, `rc`, etc.)
- `overrides:` — what this rule blocks
- `xform:` — what it does when it fires

---

## Step 4 — Trace Each Condition

For each condition field in the rule, evaluate it manually:

### Condition type quick reference

| Syntax in YAML | Evaluation in process_yaml.py | What to check |
|----------------|-------------------------------|---------------|
| `lp: $$fname` | `fname(env["lp"])` — passes **PaninianObject** | Read `fname` in paribhasha.py; PaninianObject comparison pitfalls (see §5) |
| `rp: $$fname` | `fname(env["rp"])` — passes **PaninianObject** | Same pitfalls as above |
| `l: $$fname`  | `fname(env["l"])` — passes **SanskritImmutableString** (single char) | Works correctly for null/notnull |
| `r: $$fname`  | `fname(env["r"])` — passes **SanskritImmutableString** (single char) | Works correctly for null/notnull |
| `lp: ?tag` | `env["lp"].hasTag("tag")` | Does the PaninianObject carry this tag? |
| `rp: ?!tag` | `not env["rp"].hasTag("tag")` | Tag must be *present* to block; absent = True = rule can fire |
| `lp: _ik` | `isInPratyahara("ik", env["lp"])` | String pratyāhāra check |
| `lp: [and, ...]` | AND of all sub-conditions on `env["lp"]` | Each sub-checked individually |
| `condition: [dict1, dict2]` | OR of all condition dicts | List of dicts = any one must be satisfied |

**Critical distinction — `env` field types:**

| Field | Type | Has `__eq__`? | Use `$$null`? |
|-------|------|---------------|---------------|
| `lp`, `rp` | **PaninianObject** | ✗ (always True/False for == checks) | ✗ broken |
| `l`, `r`, `lc`, `rc`, `ll`, `rr` | **SanskritImmutableString** | ✓ | ✓ works |

**Rule**: For null/notnull checks on a full token, always prefer `r: $$null` over `rp: $$null`. The former uses SanskritImmutableString (correct); the latter uses PaninianObject (broken).

### Manually simulate for the failing case

```bash
# In a Python REPL:
cd /Users/karthik/personal_projects/sanskrit_parser
python
>>> from sanskrit_parser.generator.paribhasha import *
>>> from sanskrit_parser.generator.paninian_object import PaninianObject
>>> rz_vyavaya_n("parvan")    # True or False?
>>> notnull(PaninianObject("", None))  # See §5 — likely True even for empty!
```

---

## Step 5 — Known Pitfalls (from 8.4.2.1 / parvan investigation)

### Pitfall 1: `$$notnull` / `$$null` on a PaninianObject is always wrong

**`notnull` and `null` in paribhasha.py** (original, unfixed form):
```python
def notnull(s):
    return ((s is not None) and (s != ""))

def null(s):
    return ((s is None) or (s == ""))
```

When called via `rp: $$notnull` or `rp: $$null`, `s` is `env["rp"]` — a **PaninianObject**.
- PaninianObject has no `__eq__`, so `PaninianObject != ""` uses identity → **always True**
- Therefore `notnull(PaninianObject)` → **always True** (even for empty/luk-deleted rp)
- And `null(PaninianObject)` → **always False** (even for empty/luk-deleted rp)

**Correct fix** (already applied in this codebase):
```python
def notnull(s):
    if hasattr(s, 'canonical'):
        return s.canonical() != ""
    return ((s is not None) and (s != ""))

def null(s):
    if hasattr(s, 'canonical'):
        return s.canonical() == ""
    return (s is None) or (s == "")
```

**Better alternative in YAML**: use `r: $$null` (SanskritImmutableString, correct `__eq__`) instead of `rp: $$null` (PaninianObject, broken). This avoids calling `null` on a PaninianObject entirely.

### Pitfall 2: `?!avasAna` does not fire for luk-deleted suffixes

8.4.2.1's condition `rp: [and, ?!avasAna, $$notnull]` is intended to prevent ṇatva at word-end. But:

- `avasāna` is a **separate PaninianObject** appended to terminate the prakriya (see `generate_vibhakti` in cmd_line.py line 75: `t = [*pratipadika, ss, avasAna]`)
- When a suffix is **luk-deleted** (e.g., 7.1.23 deletes 'am'), the luk'd PaninianObject becomes empty-canonical but **does not inherit the avasāna tag**
- So `?!avasAna` on a luk'd rp = `not False` = True → the rule fires even though the form is at word-end in effect

**Diagnosis**: After any luk, check whether the rp object has the avasāna tag. It almost certainly does not.

### Pitfall 3: `rz_vyavaya_n` — what stems trigger it

```python
def rz_vyavaya_n(s: str):
    # Returns True if s ends in 'n' and walking backward finds r/ṣ/ṛ
    # through allowable interveners: awkupvaNnum = aw + ku + pu + M
```

For SLP1 stem "parvan":
- s[-1]='n' ✓, s[-2]='a' (aw-intervener ✓), s[-3]='v' (pu-intervener ✓), s[-4]='r' → **True**

For SLP1 stem "yajvan":
- s[-1]='n' ✓, s[-2]='a' (aw ✓), s[-3]='v' (pu ✓), s[-4]='j' — not r/ṣ/ṛ, not awkupvaNnum → **False** → 8.4.2.1 does NOT fire for yajvan

For SLP1 stem "rAjan":
- s[-1]='n' ✓, s[-2]='a' (aw ✓), s[-3]='j' — not r/ṣ/ṛ, not awkupvaNnum → **False** → 8.4.2.1 does NOT fire for rAjan

**Summary**: 8.4.2.1 unexpectedly fires for any stem where r/ṣ/ṛ precedes the 'n' through valid interveners (e.g., parvan, brahman). It should only fire in non-avasāna contexts, but Pitfalls 1 and 2 prevent the guards from working.

### Pitfall 4: Rule ordering — earlier luk vs later ṇatva

8.4.2.1 fires on `lp` content, not rp. Even if rp is luk-deleted (empty), the lp still contains "parvan" with its r. The engine doesn't know that the prakriya has effectively reached word-end. The fix requires either:
1. Making `?!avasAna` work for luk-deleted rp (engine fix: tag luk-deleted objects with avasāna when no more rp follows), or
2. Making `$$notnull` work correctly for PaninianObject (now fixed in paribhasha.py — see Pitfall 1), or
3. Adding an `overrides:` on a dedicated blocking rule

### Pitfall 5: Tag propagation at `join_objects` — inner vs outer level

The **AntarangaPrakriya** uses hierarchical processing for nested prakriyas:
- Inner prakriya processes `[stem, suffix]` → joined via `join_objects` → outer sees single `PaninianObject`
- `join_objects` sets "pada" on the joined object when the last element had "sup"/"tiN"/"pada"
- `join_objects` does **NOT** propagate "prAtipadika" from the first element by default

**Consequence**: A rule requiring `lp: [?prAtipadika, ?pada]` will **fail** at the outer level (on the joined object) because "prAtipadika" was not propagated — even though the original stem had it.

**Anti-pattern** (causes regressions): propagating "prAtipadika" in `join_objects` unconditionally/with weak guards makes outer-level rules fire for forms where they shouldn't.

**Correct pattern**: add a second OR branch to the rule that fires at the **inner** level, while the stem and luk'd suffix are still separate tokens. Use `rp: ?sup` + `r: $$null` to target luk-deleted suffixes specifically.

### Pitfall 6: 6.1.68 vs 7.1.23 — "pada" tag on lp

Two common luk paths behave differently w.r.t. "pada" on lp:

| Rule | Trigger | Sets "pada" on lp? | How |
|------|---------|-------------------|-----|
| 6.1.68 (halaṅyāb...) | pum sū/tiP/siP deletion | **Yes** | `update: olp: +pada` |
| 7.1.23 (amipūrvaḥ) | napuṃsaka am-luk | **No** | only sets `orp: =luk_sup` |

Rules conditioned on `lp: [?prAtipadika, ?pada]` fire for 6.1.68 cases but **not** for 7.1.23 cases. Add a second branch without `?pada` (conditioned on `rp: ?sup, r: $$null`) to cover napuṃsaka luk.

### Pitfall 7: no-op rule firing self-disables the rule for transformed elements

`operate()` (sutra.py) uses `deepcopy` when chaining elements. When rule A fires — even as a
**no-op** (e.g. `dirgha('m') = 'm'`, no phonological change) — it appends itself to
`r0.disabled_sutras`. All subsequent elements inherit this list via deepcopy.

**Effect**: Rule A fires as a no-op at `(prefix | consonant)`. Later, rule B fires and
transforms `prefix → prefix'`. The new `prefix'` inherits `disabled_sutras = [A]`, so rule A
can **never** fire at `(prefix' | consonant)` — even when the condition is satisfied.

**Symptom**: Rule A fires correctly for one class of prefixes but silently fails for prefixes
that were themselves substituted by another rule B.

**Fix**: add `bahiranga: 1` to rule B (the substitution rule) so it fires *before* A. The
new `prefix'` is created before A ever touches `(prefix | c)`, so `disabled_sutras` is empty
when A evaluates `(prefix' | c)`.

**Example (SK421/SK417)**:
- SK417 (dirgha, default bahiranga=99) fires as no-op at `(sam | c)` → appends itself to disabled_sutras.
- SK421 (sam→sami, default 99) then fires → new prefix `sami` inherits `disabled_sutras=[SK417]`.
- SK417 cannot fire at `(sami | c)` even though `i` is now a valid ik vowel.
- Fix: `bahiranga: 1` on SK421. Now SK421 fires first; SK417 evaluates fresh at `(sami | c)`. ✓

---

## Step 6 — Find Which Rule *Should* Have Prevented This

```bash
# Search for rules that override the problem rule
grep -n "overrides.*<problem-id>" sanskrit_parser/generator/sutras_antaranga.yaml

# Search for rules that would fire before it (by proximity / SK order)
grep -n "id: <problem-id>" sanskrit_parser/generator/sutras_antaranga.yaml
# Then read the surrounding rules
```

Check `generator_status.md` for the SK number of the problem rule and its neighbors.

---

## Step 7 — Determine the Fix

| Root cause | Fix location | Fix approach |
|------------|-------------|--------------|
| `$$notnull` always True for PaninianObject | `paribhasha.py` | Add `hasattr(s,'canonical')` guard (already fixed) |
| `$$null` always False for PaninianObject | `paribhasha.py` | Add `hasattr(s,'canonical')` guard (already fixed) |
| `rp: $$null` needed but PaninianObject is broken | YAML | Use `r: $$null` (SanskritImmutableString path) instead |
| `?!tag` fails for luk-deleted suffix | Engine (antaranga_prakriya.py) or YAML | Add avasāna tag to luk-deleted objects, or use different blocking rule |
| Rule fires before a prerequisite lopa | YAML order or explicit `overrides:` | Add missing overrides or reorder |
| Rule fails for napuṃsaka luk (7.1.23) but works for pum (6.1.68) | YAML | Add second OR-branch without `?pada` requirement: `lp: ?prAtipadika, l: n, rp: ?sup, r: $$null` |
| `rz_vyavaya_n` matches unexpectedly | `paribhasha.py` | Tighten the intervener check or scope |
| Wrong condition scope | YAML | Tighten condition (add lp tag checks, etc.) |
| Propagating tag in `join_objects` causes outer-level regression | `paninian_object.py` + YAML | Rollback `join_objects` change; add inner-level OR branch to rule instead |

### OR-branch pattern for luk-deleted suffix

To fire rule R at the inner level (before samhitā) when rp is a luk-deleted sup:

```yaml
- sutra: <name>
  id: R
  condition:
    - <existing-condition-dict>      # retain original branch
    - lp: ?prAtipadika               # stem has prAtipadika tag
      l: n                           # last char of lp is 'n' (or whatever char R needs)
      rp: ?sup                       # rp is a sup (even luk-deleted ones keep this tag)
      r: $$null                      # first char of rp is empty (luk-deleted)
  xform:
     l: null
```

This follows the 6.1.68 OR-condition pattern already in `sutras_antaranga.yaml`.

---

## Step 8 — Verify After Fix

```bash
source /Users/karthik/venvs/sanskrit/bin/activate
export PYTHONPATH=/Users/karthik/personal_projects/sanskrit_parser
cd /Users/karthik/personal_projects/sanskrit_parser

# Test the specific form
python scripts/sanskrit_generator -t <pratipadika> -p <pratyaya> -a --verbose

# All vibhaktis for a pratipadika
python scripts/sanskrit_generator -t <pratipadika> --vibhakti

# Run all vibhakti tests to catch regressions
# CORRECT way (run.sh uses pytest-xdist -n 6 for parallel execution):
source /Users/karthik/personal_projects/sanskrit_parser/sourceme   # sets PYTHONPATH
cd /Users/karthik/personal_projects/sanskrit_parser/sanskrit_parser/generator/test
bash run.sh
# Expected: 136 + 645 + 304 + 144 + 368 = 1597 passed

# Alternative (slower, single-threaded, from project root):
PYTHONPATH=/Users/karthik/personal_projects/sanskrit_parser \
  python -m pytest sanskrit_parser/generator/test/test_halanta.py \
         sanskrit_parser/generator/test/test_ajanta_pum.py \
         sanskrit_parser/generator/test/test_ajanta_stri.py \
         sanskrit_parser/generator/test/test_ajanta_napum.py \
         sanskrit_parser/generator/test/test_list.py -v
# NOTE: `pytest sanskrit_parser/generator/test/` directly fails with conftest
# ImportError unless PYTHONPATH is set. Always use sourceme or explicit PYTHONPATH.
```

---

## Quick Diagnostic Checklist

When a rule fires unexpectedly:

1. [ ] Read the rule's YAML block: which conditions must all be True?
2. [ ] For each `$$fname` condition: call the function manually in Python with the actual value
3. [ ] For `?!tag` conditions: verify that the PaninianObject actually has/lacks the tag at firing time
4. [ ] Check if the rp was luk-deleted earlier — if so, expect `$$notnull`/`$$null` on `rp` and `?!avasAna` to malfunction (Pitfalls 1 & 2)
5. [ ] Check `rz_vyavaya_n` for the specific stem (Pitfall 3 table above)
6. [ ] Check if an expected blocking rule (`overrides:`) is absent or not yet implemented
7. [ ] Check if a `join_objects` tag-propagation patch is causing the rule to fire at the outer (post-samhitā) level when it should not (Pitfall 5)

When a rule fails to fire:

1. [ ] Verify the condition field names match what the engine provides (`lp`, `rp`, `l`, `r`, `lc`, `rc`, `ll`, `rr`)
2. [ ] Verify the tag checks: does the PaninianObject have the required tag **at this point** in the prakriya?
3. [ ] Check if another rule's `overrides:` is blocking this rule
4. [ ] Verify SK order — the rule may be in the wrong position relative to a rule that changes the state it needs
5. [ ] If the rule requires `?pada` on lp but only 7.1.23 fired (napuṃsaka luk), lp will NOT have "pada" — add a second OR branch without `?pada` (Pitfall 6)
6. [ ] If the rule is supposed to fire at the outer level but the joined object lacks a tag (e.g., "prAtipadika" not propagated by `join_objects`), the fix is an inner-level OR branch, NOT tag propagation in `join_objects` (Pitfall 5)
7. [ ] Check for the no-op self-disable trap (Pitfall 7): if a substitution rule B runs before rule A, and A can fire as a no-op at the pre-substitution form, add `bahiranga: 1` to B so it runs first and A evaluates fresh on the new form
