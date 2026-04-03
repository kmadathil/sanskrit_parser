---
name: gen-vibhakti-test
description: Generate and add vibhakti test entries for a Sanskrit parser generator pratipadika. Use when asked to add a new pratipadika test, generate vibhakti forms, or test a new inflection paradigm.
argument-hint: "[pratipadika-name] [linga?]"
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Generator Vibhakti Test Generator

Generate a complete vibhakti test entry for `$ARGUMENTS` in the Sanskrit parser generator.

## Codebase Context

- **Pratipadika definitions**: `sanskrit_parser/generator/pratipadika.py`
- **Test entries**: `sanskrit_parser/generator/test/vibhaktis_list.py`
- **Test runner**: `sanskrit_parser/generator/test/test_vibhaktis.py`
- **Encoding**: pratipadika strings in **SLP1**; viBakti forms in **Devanagari**
- **Implemented sutras**: `sanskrit_parser/generator/sutras_antaranga.yaml`
- **Rule status**: `sanskrit_parser/generator/generator_status.md`
- **Developer guide**: `Generator.md` — module structure, core objects, engine loop, YAML DSL, rule priority

## Step 1 — Identify the Pratipadika

1. Search `pratipadika.py` for an existing definition of `$ARGUMENTS`. If found, note its linga, tags, and stem string.
2. If not found, determine:
   - **linga**: pum / strI / napum (from context or user)
   - **stem string** (SLP1): the pratipadika form
   - **other_tags**: e.g. `["rAjan"]` for special rules, `["DAtu", "kvip"]` for kvip derivatives, or empty
3. If no pratipadika definition exists, append one to `pratipadika.py` after the last entry:
   ```python
   <name> = Pratipadika("<stem-in-SLP1>", "<linga>", other_tags=["<stem>"])
   ```
   **`other_tags` convention**: give each pratipadika a tag matching its stem string
   (e.g. `rAjan` → `["rAjan"]`, `yajvan` → `["yajvan"]`). This lets sutra rules
   target the stem by tag (`?yajvan`). Omit `other_tags` only for napumsaka stems
   that have no stem-specific sutra rules (e.g. `parvan_napum` needs none).

## Step 2 — Identify the Stem Type and Applicable Rules

Determine the stem type from the final character(s):

| Ending | Type | Template to look at |
|--------|------|---------------------|
| a, ā, i, ī, u, ū, e, o, ai, au | ajanta (vowel-final) | rAma, sItA, hari, etc. |
| n (after a) = -an | halanta -an stem | rAjan (pum), parvan (napum) |
| n after consonant | other halanta | — |
| s/h (kvip) | kvip derivative | div_kvip, praSAm_kvip |
| Other consonant | halanta | — |

**Key rules to check** (from `generator_status.md` and `sutras_antaranga.yaml`):

- **SK234 (6.4.134)** — al-lopa for -an stems: deletes 'a' before vowel-initial suffix when lp has aNga+Ba tags and stem ends in -an. Produces forms like rājñā.
- **SK355 (6.4.137)** — blocks SK234 when saMyoga ending in v/m precedes 'an'.
  Check on the **full stem string** (including final n): `stem[-3] ∈ [v, m]` and
  `isHal(stem[-4])` in SLP1. SK355 overrides 6.4.134, 6.4.135, and 6.4.136.

  | Stem | stem[-4] | stem[-3] | SK355? | ṇatva? | Inst sg |
  |------|----------|----------|--------|--------|---------|
  | rAjan | A (not hal) | j (∉[v,m]) | no → SK234 | — | राज्ञा |
  | parvan | r (hal) | v (∈[v,m]) | **yes** | **yes** (r before v) | पर्वणा |
  | yajvan | j (hal) | v (∈[v,m]) | **yes** | no (no r/ṣ) | यज्वना |

- **SK354 (8.2.77)** — upadhā-ik lengthening for r/v-final dhātu before hal suffix.
- **ṇatva (8.4.2)** — n → ṇ after r/ṣ (with kavarga/pavarga/h/y/v intervening).
  Check if the 'n' in the stem is preceded by r through allowable interveners.
  If ṇatva forms are uncertain, **disable** the test by commenting out only the
  `prAtipadika["name"]` line while leaving the `viBakti["name"]` block intact:
  ```python
  # prAtipadika["parvan"] = parvan_napum   # disabled: ṇatva forms not yet verified
  ```

### añcatir compound paradigm

For stems of the form `[prefix_pada, aYc_u, kvin]`:

| Component | Role | Tags |
|-----------|------|------|
| `prefix_pada` | left prefix prātipadika | `?prefix`, `pada`; plus substitution tags like `sam`, `saha`, `sarvanAma_pada` as needed |
| `aYc_u` | aYc prātipadika | `?aYc` |
| `kvin` | kvin suffix | `kvin_pada`, `kvip_pada` |

**Stem alternation in paradigm:**

| Context | Form produced | Rules involved |
|---------|--------------|----------------|
| Strong (nom/acc sg/du + nom pl) | prefix+ryaYc | SK361 nUM → yaṇ (i+a→y) |
| Weak (inst du/pl, dat/abl du/pl etc.) | prefix+ryac | direct |
| Bha (inst/dat/abl/gen/loc sg; gen/loc du) | prefix+drīc (ṭi→adri, then i→ī) | SK418 + SK417 |
| Loc pl (non-bha) | prefix+ryak+ṣu | kutvam (c→k) + ṣatva |

**Existing examples in vibhaktis_list.py:**

| Key | prAtipadika | Prefix substitution | Bha sg inst |
|-----|------------|---------------------|------------|
| `pratyac` | `[prati_pada, aYc_u, kvin]` | prati→prat (ṭi del) | pratīcā |
| `samyac` | `[sam_pada, aYc_u, kvin]` | sam→sami (SK421) | samīcā |
| `saDryac` | `[saha_pada, aYc_u, kvin]` | saha→saDrI (SK422) | saDrīcā |
| `vizvadryac` | `[vizvag_pada, aYc_u, kvin]` | vizvag→vizvadri (SK418) | viṣvadrīcā |

Use the closest example as template for new añcatir entries. Import the prefix prātipadika and
`aYc_u`, `kvin` from `pratipadika.py` at the top of `vibhaktis_list.py`.

## Step 3 — Find a Similar Template

Use the closest existing viBakti entry as a template:

```bash
grep -n "^prAtipadika\[" sanskrit_parser/generator/test/vibhaktis_list.py
```

For -an stems: use `rAjan` (pum, SK234 fires) or `yajvan` (pum, SK355 fires, no ṇatva)
or `parvan` (napum, SK355 fires + ṇatva) as the template depending on which rules apply.
For ajanta stems: find the closest linga/ending match.

Read the template entry to understand the form pattern.

## Step 4 — Generate the 8×3 viBakti Table

The table has **8 rows** (vibhaktis) × **3 columns** (sg, du, pl):

```
Row 1: Prathama (Nominative)
Row 2: Dvitīyā (Accusative)
Row 3: Tṛtīyā (Instrumental)
Row 4: Caturthī (Dative)
Row 5: Pañcamī (Ablative)
Row 6: Ṣaṣṭhī (Genitive)
Row 7: Saptamī (Locative)
Row 8: Sambodhana (Vocative)
```

Rules:
- Each cell is a **Devanagari string** (single form) or a **list of strings** (alternatives)
- For neuter (napum): rows 1, 2, 8 are identical (nom=acc=voc)
- Suffix-based shortcuts: bhyām/bhiḥ/bhyaḥ forms (du/pl of rows 3–5) follow stem + suffix directly, no SK234/SK355 involved

### Marking diagnostic forms
Add inline comments marking which rows/cells exercise the rule being tested:
```python
['पर्वणा', 'पर्वभ्याम्', 'पर्वभिः'],  # 3 Instrumental  * SK355 fires for sg
```

### If ṇatva status is uncertain
If the stem contains 'r' or 'ṣ' before the inflectional 'n', note it:
```python
# Note: ṇatva (8.4.2) required for ṇ forms; use dental न if not yet implemented
```

## Step 5 — Insert into vibhaktis_list.py

Insert **before** the `ajanta = {...}` line (the classification block near the end of file):

```python
prAtipadika["<name>"] = <variable_name>
viBakti["<name>"] = [
    [...],  # 1 Nominative
    [...],  # 2 Accusative
    [...],  # 3 Instrumental
    [...],  # 4 Dative
    [...],  # 5 Ablative
    [...],  # 6 Genitive
    [...],  # 7 Locative
    [...],  # 8 Vocative
]
```

## Step 6 — Verify

Run the test for just this pratipadika:
```bash
source ~/venv/sanskrit/bin/activate
cd /Users/karthik/personal_projects/sanskrit_parser
source sourceme
python -m pytest sanskrit_parser/generator/test/ -k <name> -v
```

If tests fail:
1. Check the actual output vs expected: examine which forms differ
2. If a rule is not yet implemented, adjust expected forms and add a `# TODO` comment
3. If unexpected rule interactions occur, check `sutras_antaranga.yaml` for conflicting rules
