# Generator Developer Guide

The generator is a Sanskrit word form generator that derives surface forms from underlying roots and stems by applying Paninian (Ashtadhyayi) grammar rules. It lives on the `generator` branch and is not yet merged to master.

> **Branch note:** All generator development should happen on the `generator` branch. See the Active Branches section of [CLAUDE.md](CLAUDE.md).

---

## Table of Contents

1. [Conceptual Overview](#conceptual-overview)
2. [Module Structure](#module-structure)
3. [Core Objects](#core-objects)
4. [The Prakriya Engine](#the-prakriya-engine)
5. [Sutras (Rules)](#sutras-rules)
6. [The YAML Rule DSL](#the-yaml-rule-dsl)
7. [Domains](#domains)
8. [Rule Priority](#rule-priority)
9. [Worked Example](#worked-example)
10. [CLI and Tests](#cli-and-tests)

---

## Conceptual Overview

Sanskrit grammar does not simply look words up in a table — it derives them through a sequence of rule applications. Panini's Ashtadhyayi defines roughly 4000 such rules (sutras). The generator models this derivation process:

```
Input: prākriti (root/stem) + pratyaya (suffix)
       ↓
Prakriya engine applies sutras in sequence
       ↓
Output: derived pada (inflected word form)
```

For example, to generate the nominative singular of `rāma`:
- Input: `rAma` (prātipadika) + `su` (nominative singular vibhakti suffix)
- Sutras fire to drop the anubandha `u~` from `su`, then handle the final `a` + `s` phonology
- Output: `rAmaH`

The process is recorded in a **derivation tree** (`PrakriyaTree`) that shows every rule that fired, in order — analogous to Panini's "prakriya" (derivational procedure).

---

## Module Structure

```
sanskrit_parser/generator/
├── paninian_object.py      # Base class for all objects in a derivation
├── dhatu.py                # Dhatu (verb root) class + predefined roots
├── pratipadika.py          # Pratipadika (nominal stem) class + predefined stems
├── pratyaya.py             # Pratyaya (suffix) class + predefined suffixes (sup, tiN, krt, ...)
│
├── sutra.py                # Sutra base class, LRSutra, GlobalDomains
├── maheshvara.py           # Pratyahara/savarna checks via Maheshvara sutras
├── paribhasha.py           # Meta-rules (paribhāṣā)
├── operations.py           # Phonological operation helpers (dīrgha, etc.)
│
├── prakriya.py             # PrakriyaVakya, PrakriyaBase, HierPrakriya, PrakriyaNode, PrakriyaTree
├── antaranga_prakriya.py   # AntarangaPrakriya — the current default engine
├── prakriya_factory.py     # PrakriyaFactory — selects which engine to instantiate
│
├── sutras.yaml             # ac-sandhi and general sutra definitions (YAML DSL)
├── sutras_antaranga.yaml   # Sutra set for AntarangaPrakriya engine
├── sutras_hier.yaml        # Sutra set for HierPrakriya engine
├── sutra_domains.yaml      # Domain-level sutra definitions
├── sutras_yaml.py          # SutraFactory — loads a YAML file into a sutra list
├── process_yaml.py         # Converts raw YAML dicts into LRSutra objects
│
├── cmd_line.py             # CLI entry point; generate_vibhakti() helper
└── test/                   # pytest test suite (see below)
```

---

## Core Objects

All objects that pass through a derivation derive from `PaninianObject`.

### `PaninianObject` — `paninian_object.py`

Extends `SanskritObject` (from `base/sanskrit_base.py`) with:

- **Tags** (`self.tags`): a list of grammatical labels (`"DAtu"`, `"aNga"`, `"pada"`, `"sup"`, `"tiN"`, etc.). Tags encode grammatical identity and are used by sutra conditions.
- **`disabled_sutras`**: list of sutra ids that have already been applied to this object and must not re-fire (enforces *lakṣye lakṣaṇaṃ sakṛdeva pravartate*).
- **`inPrakriya`**: flag indicating the object is mid-derivation (not yet a final *pada*).

Key methods: `hasTag()`, `setTag()`, `deleteTag()`, `isPada()`, `join_objects()`.

`join_objects()` assembles a list of component objects into a single `PaninianObject`, propagating tags according to Paninian rules (e.g., 1.4.14 *suptiṇantaṃ padam*, 1.4.13 *yasmāt pratyayavidhis tad ādi pratyaye'ṅgam*).

### `Dhatu` — `dhatu.py`

Represents a verb root. Carries:
- **Its** (`self.its`): anubandhas (indicatory letters like `"R"`, `"Y"`, `"qu"`, `"~a"`) that determine which rules apply but are not pronounced in the final form.
- Tag `"DAtu"` and `"aNga"` set automatically.

Predefined roots are module-level constants: `BU`, `as_dhatu`, `iR`, `guhU`, `sTA`, etc.

### `Pratipadika` — `pratipadika.py`

Represents a nominal stem. Carries:
- **`linga`**: grammatical gender (`"pum"`, `"strI"`, `"napum"`), set as a tag.
- Tag `"prAtipadika"` set automatically.

Predefined stems: `rAma`, `kavi`, `hari`, `pitf`, `rAjan`, `mahat`, etc.

### `Pratyaya` — `pratyaya.py`

Represents a suffix. Carries:
- **Its** (`self.its`): anubandhas (e.g., `"p"` in `tip`, `"k"` in `ktvA`).
- **Other tags**: grammatical identity of the suffix (`"sup"`, `"tiN"`, `"sArvaDAtuka"`, `"ArDaDAtuka"`, etc.).

Predefined suffixes span:
- **sup** (nominal case endings): `su`, `O`, `jas`, `am`, `Ow`, `Sas`, `wA`, `ByAm`, `Bis`, `Ne`, `Nasi`, `Nas`, `os`, `Am`, `Ni` — organised as `sups[8][3]` (8 vibhaktis × 3 vacanas)
- **tiN** (verbal endings): `tip`, `sip`, ...
- **kṛt suffixes**: `tfc`, `ktvA`, `kta`, `Ryat`, `GaY`, `Ric`, ...
- **taddhita suffixes**: `yat_t`, `aR_t`, ...
- **strī pratyayas**: `NIp`, `NIz`, `Ap`
- **nipātas/upasargas**: `AN`, `pra`, `upa`, `ud`, `ati`

---

## The Prakriya Engine

The engine takes a `PrakriyaVakya` (a sequence of `PaninianObject`s) and iteratively applies sutras until no more rules fire.

### `PrakriyaVakya`

A thin wrapper around a list of `PaninianObject`s. Supports copy-on-write mutation (`copy_replace_at`, `copy_insert_at`) to enable branching for optional rules without mutating shared state.

### `PrakriyaBase` (abstract)

Defines the interface: `execute()`, `describe()`, `output()`. Holds the `PrakriyaTree` (derivation history).

### `AntarangaPrakriya` — default engine

Implements the antaranga algorithm based on Patanjali's commentary: antaranga (more internal) operations take priority over bahiranga (more external) ones.

Execution loop:
1. Start with the initial `PrakriyaVakya`.
2. Slide a **window of 2 adjacent objects** across the sequence.
3. At each window position, collect all sutras whose `isTriggered(left, right)` returns True.
4. If multiple sutras trigger, apply `sutra_priority()` to select the winner.
5. Call `winner.operate(left, right)` → `(out_left, out_right)`.
6. Call `winner.update(...)` to set tags on outputs; `winner.insert(...)` to inject āgamas.
7. Record this step as a `PrakriyaNode` in the `PrakriyaTree`.
8. If the rule is optional, branch: one child node has the rule applied, the current node has it disabled and continues without it.
9. Repeat from step 2 on the new `PrakriyaVakya` until nothing fires.
10. Leaf nodes of the tree are the final outputs.

### `HierPrakriya`

An earlier engine variant. Handles hierarchical inputs (nested lists, used for āgama insertion) but uses a simpler priority model. Currently available but non-default.

### `PrakriyaFactory`

```python
p = PrakriyaFactory("AntarangaPrakriya", sutra_list, PrakriyaVakya([dhatu, pratyaya]))
p.execute()
outputs = p.output()  # list of PrakriyaVakyas (one per derivation branch)
```

Pass `"HierPrakriya"` to use the older engine. Any unrecognized name falls back to the default.

### `PrakriyaTree` and `PrakriyaNode`

The tree records the full derivation history. Each `PrakriyaNode` stores:
- `inputs`: the `PrakriyaVakya` before the rule fired
- `outputs`: the `PrakriyaVakya` after
- `sutra`: the rule that fired
- `index`: the window position where it fired
- `other_sutras`: rules that triggered but lost priority

`p.describe()` prints the full tree. `p.dict()` returns it as a JSON-serialisable dict.

---

## Sutras (Rules)

### `Sutra` base class — `sutra.py`

Holds:
- `name`: the sutra text (SanskritImmutableString)
- `aps`: Adhyaya.Pada.Sutra id string (e.g. `"6.1.77"`)
- `_aps_num`: integer encoding of the id used for ordering (e.g. tripadi sutras > 82000)
- `optional`: whether the rule is optional (vikalpa)
- `overrides`: list of sutra ids that this rule overrides (apavāda relationship)

### `LRSutra` — the primary rule class

Takes a left and right `PaninianObject` and transforms them. Parameters:

| Parameter | Purpose |
|---|---|
| `cond` | Callable `(env) -> bool`: trigger condition |
| `xform` | Callable `(env) -> (str, str)`: phonological transformation of (left, right) |
| `update` | Callable `(env)`: sets/removes tags on outputs after transformation |
| `insert` | Callable `(env) -> dict`: injects āgama objects |
| `domain` | Callable `(GlobalDomains) -> bool`: controls which domain activates this rule |
| `bahiranga` | int: bahiranga score; lower = more antaranga = higher priority |
| `optional` | bool: rule is optional (vikalpa) |
| `overrides` | list of aps strings this rule is an apavāda of |

The execution environment `env` exposes:

| Key | Meaning |
|---|---|
| `lp` | left `PaninianObject` |
| `rp` | right `PaninianObject` |
| `l` | last varna of `lp` |
| `r` | first varna of `rp` |
| `ll` | second-last varna of `lp` |
| `rr` | second varna of `rp` |
| `lc` | `lp` minus last varna |
| `rc` | `rp` minus first varna |

### `GlobalDomains`

Controls which rules are active. Domains are processed in order:

```
saMjYA → upadeSa → prakfti → pratyaya → aNga → standard → pada → saMhitA
```

Each execution pass activates one domain at a time. Rules can also trigger domain changes via their `update` function.

### Supporting modules

- **`maheshvara.py`**: `isInPratyahara(pratyahara, varna)` and `isSavarna(v1, v2)` — used in sutra conditions to check phonological class membership via Maheshvara sutras.
- **`paribhasha.py`**: meta-rules (paribhāṣā) like *sthānivad ādeśa*.
- **`operations.py`**: helpers like `dirgha()` (vowel lengthening).

---

## The YAML Rule DSL

Sutras are defined in YAML and compiled to `LRSutra` objects by `process_yaml.py`. This allows new rules to be added without writing Python.

### Basic structure

```yaml
-   sutra: इको यणचि          # Sutra name (Devanagari)
    id: 6.1.77               # Adhyaya.Pada.Sutra number
    condition:               # Trigger condition (see below)
    xform:                   # Phonological transformation
    update:                  # Tag updates on outputs
    insert:                  # Agama insertion
    domain:                  # Activation domain
    bahiranga: 9             # Priority class (lower = more antaranga)
    optional: false          # Vikalpa
    overrides:               # Apavada relationship
```

### Condition syntax

Conditions are dicts whose keys are environment variable names and values are match specifications:

| Value syntax | Meaning |
|---|---|
| `_ac` | variable is in pratyahara "ac" |
| `$r` | variable is savarna of `r` |
| `=naam` | variable is exactly the string "naam" |
| `=!naam` | variable is not the string "naam" |
| `?pada` | variable has tag "pada" |
| `?!pada` | variable does not have tag "pada" |
| `+Y` | variable is a pratyaya with it Y |
| `$$fname` | call `fname(variable)` |

### Xform syntax

```yaml
xform:
  l: dirgha(l)   # Replace last varna of lp with its dīrgha
  r: ""          # Delete first varna of rp
```

### Update syntax

```yaml
update:
  olp: +ru       # Set tag "ru" on output lp
  olp: ++R       # Set it "R" on output lp
  orp: -pada     # Remove tag "pada" from output rp
  olp: --Y       # Remove it "Y" from output lp
  olp: =krozwf   # Replace output lp with predefined object krozwf
```

### Insert syntax

```yaml
insert:
  m:             # Middle insert
    kit: tuk     # Insert predefined object tuk as kit (appended to left context)
```

---

## Rule Priority

When multiple sutras trigger at the same window position, `sutra_priority()` selects the winner using the Paninian principle *pūrvaparanityāntaraṅgāpavādānām uttarottaraṃ balīyaḥ*:

1. **Apavāda** (exception): a rule explicitly listed as overriding another wins
2. **Antaranga** (more internal): lower `bahiranga` score wins
3. **Saṃjñā rules** (numbered < 1.4.2 / `_aps_num < 14000`): earlier number wins
4. **Tripadi** (numbered in 8th adhyaya, `_aps_num > 82000`): earlier number wins
5. **Para** (later rule): higher `_aps_num` wins (default)

---

## Worked Example

Generating all vibhakti forms of `rāma` (masculine a-stem):

```python
from sanskrit_parser.generator.pratipadika import rAma
from sanskrit_parser.generator.pratyaya import sups
from sanskrit_parser.generator.sutras_yaml import SutraFactory
from sanskrit_parser.generator.cmd_line import generate_vibhakti

sutra_list = SutraFactory("sutras_antaranga.yaml")
forms = generate_vibhakti(rAma, "AntarangaPrakriya", sutra_list)
# forms[0] = [nom.sg, nom.du, nom.pl] = ["rAmaH", "rAmO", "rAmAH"]
# forms[1] = [acc.sg, acc.du, acc.pl] = ["rAmam", "rAmO", "rAmAn"]
# ...
```

For each vibhakti/vacana, the engine runs:
1. Input: `[rAma (prātipadika), su (sup, nominative sg)]`
2. Rules fire to: strip anubandha `u~` from `su` → `s`; handle `a + s` → `aH` (visarga sandhi)
3. Output: `rAmaH`

---

## CLI and Tests

### CLI (`cmd_line.py`)

The main helper is `generate_vibhakti(pratipadika, prakriya, sutra_list)`, which generates all 8×3 vibhakti forms. The entry point is registered as `sanskrit_generator`.

`run_pp(inputs, prakriya, sutra_list)` runs a single prakriya on an arbitrary input list, useful for testing individual derivations.

### Tests (`generator/test/`)

| File | Coverage |
|---|---|
| `test_ajanta_pum.py` | Ajanta (vowel-final) masculine nominals |
| `test_ajanta_stri.py` | Ajanta feminine nominals |
| `test_ajanta_napum.py` | Ajanta neuter nominals |
| `test_halanta.py` | Halanta (consonant-final) nominals |
| `test_vibhakti.py` | Vibhakti generation across stem classes |
| `test_list.py` / `manual_tests.py` | Regression and manual test cases |

Run from the `generator` branch:

```bash
cd sanskrit_parser/generator/test
pytest
```
