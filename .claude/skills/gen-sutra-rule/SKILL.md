---
name: gen-sutra-rule
description: Implement a new Paninian sutra rule in the Sanskrit parser generator. Use when asked to implement an SK number, an Ashtadhyayi sutra id, or any new phonological/morphological rule.
argument-hint: "[SK-number or sutra-id] [description?]"
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Generator Sutra Rule Implementation

Implement sutra `$ARGUMENTS` in the Sanskrit parser generator.

## Codebase Context

| File | Role |
|------|------|
| `sanskrit_parser/generator/sutras_antaranga.yaml` | Primary sutra rules file (antaranga/inner operations) |
| `sanskrit_parser/generator/paribhasha.py` | Helper functions callable via `$$fname` in conditions/xforms |
| `sanskrit_parser/generator/generator_status.md` | Implementation tracking (Last/Next, status table) |
| `sanskrit_parser/generator/process_yaml.py` | DSL evaluator — check here if uncertain about semantics |
| `sanskrit_parser/generator/antaranga_prakriya.py` | Prakriya engine — see how `overrides` is enforced (~line 180) |
| `Generator.md` | Developer guide: module structure, core objects, engine loop, YAML DSL, rule priority |

> **If the sutra you're implementing is in the ābhīya section** (Ashtadhyayi id `6.4.x` with `x > 22`, i.e. `_aps_num ∈ (64022, 64176)`): read `Generator.md` → *Ābhīya asiddhavat (6.4.22, partial)* **before writing the rule**. The condition must target the pre-section snapshot (not a peer's output), and you may need to add a symmetric entry to `_ASIDDHA_PEERS` in `antaranga_prakriya.py` so the new rule and an existing peer are mutually invisible.

---

## Step 1 — Understand the Sutra

1. Read `generator_status.md` to find:
   - The SK number ↔ Ashtadhyayi id mapping
   - The **Last implemented** and **Next to implement** lines
   - Whether this sutra is already marked Implemented, Skipped, or Natural Siddha

2. Look up the sutra in the reference files (all under `.claude/skills/gen-sutra-rule/references/`):

   a) **`.claude/skills/gen-sutra-rule/references/vasu_english_summary.txt`** — SC Vasu's one-line
      summary; read this first for a quick sense of what the sutra says.

   b) **`.claude/skills/gen-sutra-rule/references/vasu_english.txt`** — Vasu's full commentary;
      read this for the detailed interpretation, examples, and scope.

   c) **`.claude/skills/gen-sutra-rule/references/siddhantakaumudi.html`** — Bhaṭṭoji Dīkṣita's
      Siddhāntakaumudī; read this for SK's explanation and the specific word-forms it generates.
      Search by SK number anchor: `id="SK<N>"` — e.g. for SK360 search `id="SK360"`.
      (The file does NOT index by Ashtadhyayi ID — use the SK number, not `6.4.128`.)

   > **Vasu numbering:** The files use dot-free integers. Convert the Ashtadhyayi id by
   > removing dots and zero-padding each component to 2 digits:
   > `A.B.C` → `A0B0C` — e.g. `1.1.1` → `11001`, `6.4.133` → `64133`, `8.2.7` → `82007`.

   > **If Vasu and Siddhāntakaumudī disagree** on scope, the forms generated, or the
   > interpretation of a word in the sūtra, **stop and ask the user** which reading to follow
   > before proceeding.

3. Identify the rule type:
   | Type | YAML marker | When |
   |------|-------------|------|
   | Regular | *(none)* | Fires unconditionally when conditions match |
   | Apavāda (exception) | `overrides: <id>` | Blocks a more general rule |
   | Vibhāṣā (optional) | `optional: true` | May or may not apply |
   | Blocking only | `xform: null` | Prevents another rule from firing, no change itself |
   | Tagging/saṁjñā | `update:` only | Just marks the output, no phonological change |

4. Identify what the rule **does** phonologically:
   - Deletion (lopa): `xform: l: null` or `lc: lc[:-1]`
   - Substitution (ādeśa): `xform: l: dirgha(l)` etc.
   - Lengthening (dīrgha): `xform: lc: lc[:-1]+dirgha(lc[-1])`
   - Insertion (āgama): `insert: m: tuk` etc.
   - Tag update: `update: olp: +tag`
   - No-op block: `xform: null` with `overrides:`

---

## Step 2 — Find the Insertion Point in the YAML

The YAML groups rules by SK thematic order. Find the right location:

```bash
# Find the SK comment lines around the target SK number
grep -n "^# [0-9]\+:" sanskrit_parser/generator/sutras_antaranga.yaml | grep -A2 -B2 "<SK-number>"

# Find by Ashtadhyayi id
grep -n "<id>" sanskrit_parser/generator/sutras_antaranga.yaml
```

**Insert position**: immediately after the preceding SK block (or before `# Skipping for now` if at a boundary). Maintain SK numerical order within each thematic group.

---

## Step 3 — Write the YAML Block

### YAML Block Template

```yaml
# <N>: <sutra-in-devanagari> (<adhyAya-pAda-sutra>)
- sutra: <sutra-in-devanagari>
  id: <adhyAya.pAda.sutra>
  [overrides: <id>]                    # apavāda: single override
  [overrides: [<id1>, <id2>, <id3>]]  # apavāda: override multiple rules
  [optional: true]            # vibhāṣā only
  [bahiranga: <int>]          # override priority; see Rule Priority section
  [domain: <domain>]          # saṁjñā domain rules only
  condition:
    <field>: <value>
  xform:                      # omit or use "xform: null" for tag-only / blocking rules
    <field>: <expression>
  [update:                    # tag modifications
    olp: +<tag>]
  [insert:                    # āgama
    m: <augment>]
```

### Condition Field Reference

| Field | Meaning | Example values |
|-------|---------|---------------|
| `l` | Final char of left element | `a`, `_ik`, `[v, r]`, `$r` |
| `r` | Initial char of right element | `_ac`, `_hal`, `[v, m]` |
| `ll` | Penultimate char of left element | `a`, `_ik` |
| `rr` | Second char of right element | — |
| `lc` | Left element minus final char | `$$saMyogapUrvaVamanta` |
| `rc` | Right element minus initial char | `$$null` |
| `lp` | Left PaninianObject (tags/content) | `?DAtu`, `[and, ?aNga, ?Ba]` |
| `rp` | Right PaninianObject (tags/content) | `?pratyaya`, `=naam`, `+Y` |

### Condition Value Syntax

| Syntax | Meaning |
|--------|---------|
| `a` | Savarna of 'a' (short a-class) |
| `_ik` | In pratyāhāra "ik" |
| `[v, r]` | Literal list (OR): 'v' or 'r' |
| `$r` | Savarna of variable r |
| `=naam` | Exact string "naam" |
| `!=strI` | Not exactly "strI" |
| `?tag` | Has tag |
| `?!tag` | Does not have tag |
| `+Y` | pratyaya with it Y |
| `$$fname` | Call `fname(value)` from paribhasha.py |
| `[and, cond1, cond2]` | AND of conditions |
| `[cond1, cond2]` | OR of conditions |

### Multiple condition blocks = OR at rule level

```yaml
condition:
  - l: _hal      # Block A
    rp: ?su
  - lp: ?NI      # Block B (OR with A)
    rp: ?su
```

### xform Expression Reference

| Expression | Effect |
|------------|--------|
| `dirgha(l)` | Lengthen l (a→A, i→I, u→U, ṛ→ṝ) |
| `hrasva(l)` | Shorten l |
| `guna(r)` | Apply guṇa to r |
| `vriddhi(r)` | Apply vṛddhi to r |
| `ikoyan(l)` | yaṇ sandhi (i→y, u→v, ṛ→r) |
| `ayavayav(l)` | e→ay, o→av |
| `lc[:-1]+dirgha(lc[-1])` | Lengthen penultimate (upadhā-dīrgha) |
| `han_kutva(lc+l)` | h→G for han-stems: replaces every 'h' in the combined lc+l string with 'G' |
| `lc[:-1]` | Delete penultimate |
| `str("n")` | Literal string "n" |
| `str("R")` | Literal string "R" (SLP1 ṇ = ण्) — for ṇatva output |
| `null` | Delete (set to empty) |
| `Ratva(r+rc)` | Apply ṇatva to combined right string |

---

## Step 4 — Decide if a New Helper Function is Needed

Use an existing `paribhasha.py` function if the condition can be expressed via the standard DSL fields (pratyāhāra, tag, literal list). Add a new helper only when the condition requires **string indexing** (e.g., lp[-3], lp[-4]) or **multi-character pattern matching** not expressible in YAML.

### Existing helpers (paribhasha.py)

| Function | Checks / Does |
|----------|--------------|
| `dirgha(s)` | Lengthen vowel |
| `hrasva(s)` | Shorten vowel |
| `guna(s)` / `vriddhi(s)` | Apply guṇa/vṛddhi |
| `ikoyan(s)` | yaṇ |
| `ayavayav(s)` | e/o → ay/av |
| `shcutva(s)` / `zwutva(s)` | ś/ṣ-conversion |
| `Ratva(s)` | n → ṇ |
| `kutva(s)` | `adesha(s,"cCjJYh","kKgGNG")` — c→k, j→g, Y→N, h→G; identity on other chars |
| `han_kutva(s)` | `s.replace("h","G")` — simpler whole-string h→G for han-stems (SK358) |
| `anekAc_asaMyogapUrva(s)` | Multi-vowel, not cluster-preceded |
| `saMyogapUrvaVamanta(lp)` | lp ends in hal+[v,m]+a+n |
| `rz_vyavaya_l(s)` / `rz_vyavaya_r(s)` | ṛ/ṣ/r intervening checks |
| `notnull(s)` / `null(s)` | Non-empty / empty |
| `numAgama(s)` | Insert n after last vowel |
| `ekAcDAtu(s)` | Single-vowel dhātu |
| `ticAdesha_adri(s)` | SK418: replace ṭi (from last vowel of s) with "adri"; e.g. vizvag→vizvadri, kim→kadri |

**Note on kutva vs han_kutva:** Both convert h→G but differ in scope. `kutva(s)` applies
the full kutvam substitution table (c→k, j→g, Y→N, h→G) and is used for general kutvam
contexts. `han_kutva(s)` is a simpler `s.replace("h","G")` that operates on the whole
combined lc+l string — used for 7.3.54 to avoid position arithmetic when the 'h' is always
the penultimate character of the han-stem.

### Calling a helper in xform (whole-lp replacement pattern)

When the xform must compute a **new lc string** from the full lp value (`lc+l` combined),
use `lc+l` in the xform expression. `process_yaml.py` evaluates xform fields via `eval()`
in a context that already has `from paribhasha import *`, so all helpers are available.

```yaml
xform:
  l: null              # delete the final char
  lc: myHelper(lc+l)   # pass full lp (lc+l) to helper; result becomes new lc
```

`lc+l` is a Python string concatenation available in the eval context.
`l: null` ensures the final char placeholder is cleared after lc is replaced.

### If a new helper is needed

Add it to `paribhasha.py` **after `saMyogapUrvaVamanta`** (line ~242), before `numAgama`. Follow the existing style:

```python
def myNewHelper(s):
    """One-line description."""
    if len(s) < N:
        return False
    return <condition using isInPratyahara('hal', s[-k]) etc.>
```

`$$` in a condition passes the **full string content** of the variable. Key index notes:
- `l` = final char of lp → `lp[-1]`
- `ll` = `lp[-2]`
- `lc` = lp content minus final char → `lp[:-1]`; so `lc[-1]` = `lp[-2]`
- When called via `lp: $$fname`, function receives full `lp` string (includes final char)
- When called via `lc: $$fname`, function receives `lc` string (excludes final char)

---

## Step 5 — Insert the YAML Block

Use the exact insertion point found in Step 2. Insert the full block including the `# <N>:` comment line.

---

## Step 6 — Update generator_status.md

1. Update the **Last/Next** header lines:
   ```
   **Last implemented:** SK <N> — <id> <sutra>
   **Next to implement:** SK <N+1> (<id> — <sutra>)
   ```

2. Add a row to **"Implemented Sutras (SK order)"** table (4 columns; after the preceding SK row):
   ```
   | <SK> | <id> | <sutra> | <brief description of what it does and which forms it affects> |
   ```
   Note: do **not** use the "Implemented Sutras (additional, with SK numbers)" table — that table
   is for sutras without a clear SK ordering. New sutras go in the main SK-order table.

3. If the sutra has a partial exception that is **not yet implemented** (e.g. a nañ-compound
   exception, a restricted scope, a bahulam option not fully handled), also add a row to the
   **"Skipped / Deferred Sutras"** table (5 columns: SK | Sutra ID | Sutra | Reason | Affects):
   ```
   | <SK> | <id> | <sutra> | Partial — <exception> pending | <what is deferred and why> |
   ```

4. Update the **Summary** counts:
   - Increment "SK-numbered sutras, implemented" by 1
   - If a Skipped/Deferred row was also added (step 3), increment "SK-numbered sutras,
     skipped/deferred" by 1 too
   - If new pratipadika stems were added to `vibhaktis_list.py` as part of this sutra,
     increment "Stems with full vibhakti test tables" accordingly

5. If new pratipadika stems were added to `vibhaktis_list.py`, add a row per stem to the
   **Test Coverage** table under "Stems with full 8×3 vibhakti tables":
   ```
   | <stem-key> | <linga> | <class/type> | <brief notes about which sutras affect it> |
   ```

### If the sutra is entirely skipped or deferred

Do **not** add a row to the Implemented table. Instead:

1. Add a row to **"Skipped / Deferred Sutras"** (5-column table):
   ```
   | <SK> | <id> | <sutra> | <reason> | <what it would affect, for future reference> |
   ```
   Common reason categories:
   - `For later` — will be needed eventually but not now (kṛt/verbal only, compounds, etc.)
   - `Natural` — falls out of engine behaviour without a YAML rule
   - `Natural + special siddha` — handled by the siddha mechanism in antaranga_prakriya.py
   - `Handled elsewhere` — logic is in a Python file, not the YAML

2. Update **Summary** counts:
   - Increment "SK-numbered sutras, skipped/deferred" by 1
   - Do **not** increment "SK-numbered sutras, implemented"

3. Update the **Last/Next** header to skip over this SK number:
   ```
   **Next to implement:** SK <N+1> (skipping SK <N> — <brief reason>)
   ```
   or simply advance to the next non-deferred SK.

---

## Step 7 — Verify

```bash
# Confirm the sutra id appears exactly once
grep -n "<id>" sanskrit_parser/generator/sutras_antaranga.yaml

# Confirm overrides field (for apavādas)
grep -n "overrides.*<overridden-id>" sanskrit_parser/generator/sutras_antaranga.yaml

# If a new helper was added
grep -n "<helperName>" sanskrit_parser/generator/paribhasha.py
grep -n "<helperName>" sanskrit_parser/generator/sutras_antaranga.yaml
```

If a vibhakti test exists for a relevant pratipadika, run it:
```bash
cd /Users/karthik/personal_projects/sanskrit_parser
python -m pytest sanskrit_parser/generator/test/test_vibhaktis.py -k <pratipadika> -v
```

---

## Common Patterns (Quick Reference)

### Pattern A — Simple phonological change
```yaml
# 354: हलि च (8.2.77) — upadhā-dīrgha for r/v-final dhātu before hal
- sutra: हलि च
  id: 8.2.77
  condition:
    lp: ?DAtu
    ll: _ik
    l: [v, r]
    r: _hal
  xform:
    lc: lc[:-1]+dirgha(lc[-1])
```

### Pattern B — Apavāda with no-op xform (blocks another rule, or multiple rules)
```yaml
# 355: न संयोगाद्वमन्तात् (6.4.137) — blocks al-lopa when saMyoga ends in v/m
# Overrides 6.4.134 (SK234), 6.4.135, and 6.4.136 (SK237)
- sutra: न संयोगाद्वमन्तात्
  id: 6.4.137
  overrides: [6.4.134, 6.4.135, 6.4.136]
  condition:
    lp:
      - and
      - ?aNga
      - ?Ba
      - $$saMyogapUrvaVamanta    # helper: lp ends in hal+[v,m]+a+n
  xform: null
```

Use `overrides: [id1, id2, ...]` (YAML list) when the apavāda simultaneously
blocks multiple parent rules (e.g. the basic rule + its own optional variant).

### Pattern C — Optional apavāda (vibhāṣā)
```yaml
# 237: विभाषा ङिश्योः (6.4.136) — optional al-lopa before Ni/SI
- sutra: विभाषा ङिश्योः
  id: 6.4.136
  overrides: 6.4.134
  optional: true
  condition:
    lp:
      - and
      - ?aNga
      - ?Ba
    ll: a
    l: n
    rp:
      - ?Ni
      - ?SI
  xform:
    lc: lc[:-1]
    1: str("n")
```

### Pattern D — Tag update only (saṁjñā)
```yaml
- sutra: <sutra>
  id: <id>
  domain: saMjYA
  condition:
    lp: ?someTag
  update:
    olp: +newTag
```

### Pattern E — Insertion (āgama)
```yaml
- sutra: छे च
  id: 6.1.73
  condition:
    l: [at, it, ut, ft, xt]
    r: C
  insert:
    m: tuk
```

### Pattern F — Generic extensible tag for a class of stems

When a rule applies to a **class** of stems (all pronouns, all kvip-derivatives, etc.),
use a shared class tag rather than one condition block per stem. This avoids YAML changes
when new members are added later.

1. Add the class tag to each member's prātipadika `other_tags`:
   ```python
   tad_pada = Pratipadika("tad", "pum", other_tags=["tad", "sarvanAma", "sarvanAma_pada", "pada"])
   ```
2. If the tag must also appear on **merged** (joined) forms, propagate it in `join_objects`
   (`paninian_object.py`), mirroring the existing kvin/kvip block:
   ```python
   for t in ["sarvanAma"]:
       if objects[0][0].hasTag(t):
           so.setTag(t + "_pada")
   ```
3. YAML uses a single condition block `lp: ?sarvanAma_pada` — all current and future members
   are covered automatically.

---

## SLP1 Encoding Reference

SLP1 (Sanskrit Library Phonetic basic encoding) is the internal representation used throughout
the generator. Every Devanagari letter maps to exactly one ASCII character.

### Vowels

| SLP1 | IAST | Devanagari | | SLP1 | IAST | Devanagari |
|------|------|------------|-|------|------|------------|
| `a`  | a    | अ          | | `A`  | ā    | आ          |
| `i`  | i    | इ          | | `I`  | ī    | ई          |
| `u`  | u    | उ          | | `U`  | ū    | ऊ          |
| `f`  | ṛ    | ऋ          | | `F`  | ṝ    | ॠ          |
| `x`  | ḷ    | ऌ          | | `X`  | ḹ    | ॡ          |
| `e`  | e    | ए          | | `E`  | ai   | ऐ          |
| `o`  | o    | ओ          | | `O`  | au   | औ          |

### Consonants

| SLP1 | IAST | Devanagari | Group            |
|------|------|------------|------------------|
| `k`  | k    | क          | velar            |
| `K`  | kh   | ख          | velar            |
| `g`  | g    | ग          | velar            |
| `G`  | gh   | घ          | velar            |
| `N`  | ṅ    | ङ          | velar nasal      |
| `c`  | c    | च          | palatal          |
| `C`  | ch   | छ          | palatal          |
| `j`  | j    | ज          | palatal          |
| `J`  | jh   | झ          | palatal          |
| `Y`  | ñ    | ञ          | palatal nasal    |
| `w`  | ṭ    | ट          | retroflex        |
| `W`  | ṭh   | ठ          | retroflex        |
| `q`  | ḍ    | ड          | retroflex        |
| `Q`  | ḍh   | ढ          | retroflex        |
| `R`  | **ṇ**| **ण**      | **retroflex nasal** ← ṇatva output |
| `t`  | t    | त          | dental           |
| `T`  | th   | थ          | dental           |
| `d`  | d    | द          | dental           |
| `D`  | dh   | ध          | dental           |
| `n`  | n    | न          | dental nasal     |
| `p`  | p    | प          | labial           |
| `P`  | ph   | फ          | labial           |
| `b`  | b    | ब          | labial           |
| `B`  | bh   | भ          | labial           |
| `m`  | m    | म          | labial nasal     |
| `y`  | y    | य          | semivowel        |
| `r`  | r    | र          | semivowel        |
| `l`  | l    | ल          | semivowel        |
| `v`  | v    | व          | semivowel        |
| `S`  | ś    | श          | sibilant         |
| `z`  | ṣ    | ष          | sibilant         |
| `s`  | s    | स          | sibilant         |
| `h`  | h    | ह          | aspirate         |
| `L`  | ḷ    | ळ          | retroflex lateral|

### Special Characters

| SLP1 | Meaning                      |
|------|------------------------------|
| `M`  | anusvāra (ṃ / ं)            |
| `H`  | visarga (ḥ / ः)             |
| `~`  | anunāsika / chandrabindu (ँ)|
| `3`  | pluta (prolonged vowel ३)   |

**Common confusions:**
- `N` = ṅ (ङ, velar nasal) — NOT ṇ
- `R` = ṇ (ण, retroflex nasal) — use `str("R")` for ṇatva output
- `n` = n (न, dental nasal)
- `f` = ṛ (ऋ, vocalic r) — NOT r
- `r` = r (र, semivowel r)

---

## Rule Priority Reference (antaranga_prakriya.py)

Priority is managed at **two distinct levels**:

**Level 1 — Sutra-vs-sutra** (multiple sutras trigger at the same window): `sutra_priority()`
picks the winner via `_aps_num = sutra_num[2] + sutra_num[1]*1000 + sutra_num[0]*10000`:

| Condition | Winner |
|-----------|--------|
| One rule has `overrides:` pointing to the other | The overriding rule |
| One rule has lower `bahiranga` value | Lower bahiranga (more antaranga) |
| Either `_aps_num > 82000` (tripadi = 8.2.0+) | **Lower** _aps_num |
| Both `_aps_num ≤ 82000` and saṁjñā (`< 14000`) | Lower _aps_num |
| Both SPSP (14000 ≤ _aps_num ≤ 82000) | **Higher** _aps_num (para kāryam) |

**Key implication:** YAML file position is irrelevant. A 7.3.x rule always fires before an
8.4.x rule when they compete, because 8.4.x is tripadi (> 82000) and lower wins.
Example: 7.3.54 (_aps_num=73054) fires before 8.4.22 (_aps_num=84022). ✓

**Level 2 — Window-position** (which window the engine examines first): the engine scans
the sequence in a fixed order, giving pratyaya-adjacent windows highest priority. This
ensures anga kāryas fire before pada kāryas without requiring a per-sutra `bahiranga` tag —
which would be impractical since the same rule may operate on an anga in one context and a
pada in another. Order: pratyaya-adjacent (leftmost wins) → samāsa-adjacent (leftmost wins)
→ any other pair (leftmost).

### `bahiranga` field — explicit priority override

`LRSutra.bahiranga` defaults to **99**. Lower value = more antaranga = fires **first**.
When two rules have the same `_aps_num`, the lower `bahiranga` value wins regardless of YAML
file position.

**Convention (current codebase):**

| Value | Category | When to use |
|-------|----------|-------------|
| 0 | Saṃjñā (naming) rules | Rules that only set tags, no phonological change |
| 1 | Left prātipadika substitution | Rules that substitute/replace the left element (lc/l) and must fire before pratyaya modification (e.g., SK418, SK421, SK422) |
| 2 | Pratyaya substitution | Rules that modify the right element and must fire before phonological cleanup |
| 3 | Special case | Used in one specific rule only |
| 99 | Default | All other rules — determined by _aps_num / SPSP |

**⚠ Consent required**: Whenever you use the `bahiranga` field to fix a priority problem,
explicitly inform the user of the value you intend to use, explain why, and get consent
before adding it.

**Common trigger**: A left-substitution rule A (e.g., sam→sami) needs to fire before a
phonological rule B (e.g., SK417 dirgha), but both have default bahiranga=99 and B's
`_aps_num` happens to win. Fix: add `bahiranga: 1` to A.

### disabled_sutras / no-op self-disable trap

`operate()` in `sutra.py` uses `deepcopy(s1)`. When rule A fires — even as a **no-op**
(e.g. `dirgha('m') = 'm'`, no phonological change) — it appends itself to
`r0.disabled_sutras`. Subsequent elements inherit this list via deepcopy.

**Consequence**: If rule A fires as a no-op at `(prefix | consonant)`, then rule B fires
`prefix → prefix'`, the new `prefix'` inherits `disabled_sutras = [A]` and A can **never**
fire at `(prefix' | consonant)` — even when it should.

**Fix**: give rule B `bahiranga: 1` so it fires *before* A. After B transforms the prefix,
A evaluates fresh on the new prefix — `disabled_sutras` is empty because A never ran there.

---

## ṅit (N-it) and ñit (Y-it) Sup Suffixes

> **N-it = ṅit** (N = ṅ = ṅ, NG/velar nasal, ङ) — **not** ṇit.
> **R-it = ṇit** (R = ṇ = ṇ, retroflex nasal, ण) — a separate suffix class.

Sup suffixes with `N` in their `its` list (verified: `Ne = Pratyaya("e", its=["N"], ...)`):

| Suffix | Content | Case |
|--------|---------|------|
| `Ne` | e | Dative sg |
| `Nasi` | as | Ablative sg |
| `Nas` | as | Genitive sg |
| `Ni` | i | Locative sg |

YAML condition for ṅit: `rp: +N`. YAML condition for ñit: `rp: +Y`.
The suw suffixes (su, O, jas, am, Ow) are NOT ṅit/ñit.

---
