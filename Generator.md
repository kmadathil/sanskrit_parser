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

#### Tag propagation in `join_objects` (compound lifecycle)

Tags ride from the constituent elements (`first` = parts[0], `last` = parts[-1]) onto the merged result `so` through several gated `_propagate` calls. The interesting propagations are organised as follows:

| Direction | Gate | Tags | Why |
|-----------|------|------|-----|
| `first → so` | **unconditional** | `samAsa`, `samAsaPurva`, `adas`, `vasupada` | Samāsa-lifecycle markers needed by the compound-completion logic. `adas`/`vasupada` strictly belong in the aṅga-gated tier but are propagated unconditionally as a workaround for 6.1.87 (*AdguRaH*) and 6.1.88, and cleaned up on `pada+pada` merge. |
| `first → so` | `first.hasTag("aNga")` | `udanc`, `viSva` | Stem-identity tags that only matter when first acts as an aṅga. |
| `first → so` | `last.hasTag("tadDita")` | `bahuvrIhi`, `dvigu`, `parimARa`, `bistAdi`, `kARqa`, `puruza`, `kzetre`, `pramARe` | Compound-type and SK480/481/482 semantic-class tags ride forward **only** through a tadDita-affix merge. For direct strī-suffix merges (e.g. `loka | strI_abs` → त्रिलोकी) the strī-block already copies all of `first.tags` onto `so`, so no separate riding is needed. The narrow gate prevents stale compound-type tags from leaking into ordinary pada formation. |
| `last → so` | `first.hasTag("aNga")` | `trc`, `trn`, `kaY`, `suc`, `van`, `ka_pratyaya`, `NIp_taddhita`, `yaY`, `tadDita_ya`, `luk_tadDita` | Kṛt/taddhita classifier tags ride from the suffix onto the merged stem so downstream rules can identify the affix class on a derived prātipadika. |
| `last → so` | `last.hasTag("samAsa")` | `ajAdi` | SK454 / 4.1.4.1 (ajādi-prabalatva) — the ajādi flag rides from the uttara-pada onto the compound stem. The SK480/481/482 semantic tags do *not* need an entry here; they reach the right window via the tadDita-gated first-propagation above. |

`join_objects` also runs an iterative settling pass at each window: the engine may call it more than once on the same `(first, last)` pair, and a tag set by one pass (e.g. `?aNga` via 1.4.13) becomes the gate for another tag in the next pass (e.g. `?luk_tadDita` riding from `last` under the aṅga gate). This convergence is essential for chains like *(compound-stem | luk_tadDita)*, where the compound stem doesn't carry `?aNga` until the second pass and `?luk_tadDita` therefore propagates only on the third.

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

Priority is managed at two distinct levels:

**Level 1 — Sutra-vs-sutra competition** (multiple sutras trigger at the same window position): `sutra_priority()` uses the per-sutra `bahiranga` field from `sutras_antaranga.yaml` to pick the winner. Convention (lower wins):
  - `0` — saMjñā sutras
  - `1` — prakṛti kāryas (modifications of stems)
  - `2` — pratyaya kāryas (modifications of suffixes)
  - (default `99` when `bahiranga` is unspecified)

**Level 2 — Window-position priority** (which window to examine first): the engine scans the sequence in a fixed order, giving pratyaya-adjacent windows highest priority. This ensures anga kāryas and anga-pratyaya sandhi fire before pada kāryas without a per-sutra `bahiranga` tag — which would be impractical since the same rule may operate on an anga in one context and a pada in another.

Execution loop:
1. Start with the initial `PrakriyaVakya`.
2. Slide a **window of 2 adjacent objects** across the sequence.
3. **Select the highest-priority window** by scanning left to right in this order:
   - **Pratyaya-adjacent** pairs (anga + pratyaya): highest priority; if multiple, leftmost wins
   - **Samāsa-adjacent** pairs: next; if multiple, leftmost wins
   - **Any other pair** (leftmost): fallback when neither pratyaya nor samāsa is present
4. Collect all sutras whose `isTriggered(left, right)` returns True at that window.
5. If multiple sutras trigger, apply `sutra_priority()` to select the winner.
6. Call `winner.operate(left, right)` → `(out_left, out_right)`.
7. Call `winner.update(...)` to set tags on outputs; `winner.insert(...)` to inject āgamas.
8. Record this step as a `PrakriyaNode` in the `PrakriyaTree`.
9. If the rule is optional, branch: one child node has the rule applied, the current node has it disabled and continues without it.
10. Repeat from step 2 on the new `PrakriyaVakya` until nothing fires.
11. Leaf nodes of the tree are the final outputs.

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

This feature is currently unused in the `AntarangaPrakriya` framework

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

`insert` adds āgamas (augment elements) to the prakriya sequence. It fires **after** `xform`
and `update` in the execution loop (step 7 above).

```yaml
insert:
  <position>: <expression>   # one key–value pair per insertion
```

**Eval context.** Expressions are Python strings evaluated at rule-trigger time. The following
variables are bound (canonical SLP1 strings):

| Variable | Value |
|----------|-------|
| `l` | Last character of the left operand |
| `r` | First character of the right operand |
| `lc` | Left operand minus its last character |
| `rc` | Right operand minus its first character |

All names from `pratyaya`, `paribhasha`, `maheshvara`, and `pratipadika` are in scope
(star-imported by `process_yaml.py`), so pre-defined Pratyaya objects (e.g., `tuk`, `UW`) and
helper functions (e.g., `shcutva`, `zwutva`) can be referenced directly.

**Position keys and their effect on the sequence:**

| Key | Effect |
|-----|--------|
| `"m"` with **kit** (`its=["k"]`) | Appends āgama after left operand: `[left, āgama]` |
| `"m"` with **wit** (`its=["w"]`) | Prepends āgama before right operand: `[āgama, right]` |
| `"l"` | Appends āgama after left operand: `[left, āgama]` |
| `"r"` | Prepends āgama before right operand: `[āgama, right]` |
| `0` (integer) | Prepends āgama before left operand: `[āgama, left]` |
| `1` (integer) | Prepends āgama before right operand: `[āgama, right]` |

The key determines *where* in the sequence the āgama lands; for the `"m"` key the kit/wit
markers on the inserted object itself decide which side to attach to.

**Hierarchical prakriya.** When `insert` produces a list (non-scalar result), `AntarangaPrakriya`
runs recursively on the expanded pair before continuing. This ensures the āgama undergoes its own
phonological transformations before being merged back into the main sequence. After hierarchical
execution, the pair is collapsed into a single `PaninianObject` with the merged string.

> **Samprasāraṇa exception:** when a position-`0` insert places an object carrying the
> `samprasAraRam` tag before the left operand, the hierarchical output uses the first element of
> the first output (`hpo[0][0]`) rather than the normal sub-object selection. This drives the
> vowel-grade alternation in roots like `√vah`.

**Common pattern — ādeśa and lopa via delete-and-replace.** `xform` nulls out a character (lopa)
and `insert` provides its replacement (ādeśa) as a fresh `Pratyaya` or `PaninianObject`. This
is the correct way to implement both substitutions and deletions where sandhi may subsequently
apply. Because the replacement is a new object, the engine detects a non-scalar result and runs
a **hierarchical prakriya** on the expanded pair — any sandhi rules that can apply between the
newly inserted object and its neighbours will fire. A simple varna substitution in `xform` alone
would not create a list, so no hierarchical prakriya would run and post-insertion sandhi would be
silently skipped.

```yaml
# 8.4.40 — स्तोः श्चुना श्चुः (L): s / dental-stop → palatal equivalent
# The palatal replacement fires a hierarchical prakriya; subsequent ścu/ṣṭu sandhi
# rules can then operate on the newly inserted palatal if needed.
xform:
  l: null         # lopa: delete the original s or dental-stop
insert:
  l: shcutva(l)  # ādeśa: insert the palatal equivalent as a new object
```

**Examples:**

```yaml
# 6.1.73 — छे च: insert tuk (kit) after a short vowel, before cha
# tuk = Pratyaya("t", its=["k"]) — kit, so appended to left operand
insert:
  m: tuk

# 8.4.40/41 — श्चुत्व / ष्टुत्व: delete and re-insert as the appropriate class
xform:
  l: null
insert:
  l: shcutva(l)   # or zwutva(l) for ष्टुत्व

# 6.4.134 — अल्लोपोऽनः: delete ā, re-insert n as a fresh object
xform:
  lc: lc[:-1]
  l: null
insert:
  l: str("n")     # fresh n; subsequent rules see it as a new token

# 6.4.133 — अयादीनामायः: insert UW (samprasāraṇa-tagged) before left operand
xform:
  lc: lc[1:]
insert:
  0: UW           # integer key → prepend before left operand
```

---

## Rule Priority

When multiple sutras trigger at the same window position, `sutra_priority()` selects the winner using the Paninian principle *pūrvaparanityāntaraṅgāpavādānām uttarottaraṃ balīyaḥ*:

1. **Apavāda** (exception): a rule explicitly listed as overriding another wins
2. **Antaranga** (more internal): lower `bahiranga` score wins
3. **Saṃjñā rules** (numbered < 1.4.2 / `_aps_num < 14000`): earlier number wins
4. **Tripadi** (numbered in 8th adhyaya, `_aps_num > 82000`): earlier number wins
5. **Para** (later rule): higher `_aps_num` wins (default)

### Siddha / Asiddha

Rule priority determines *which* sutra wins when multiple fire at the same window. Siddha/asiddha determines *what state* each sutra sees — i.e. which earlier outputs are visible to it.

Every sutra's view of the derivation is computed by `view()` in `antaranga_prakriya.py`. It walks back up the `PrakriyaTree` and returns the outputs of the most recent node that the current sutra is allowed to see. The key rule is:

**TripāḍÄ« sutras (8.2.1–8.4.68, `_aps_num > 82000`) are asiddha with respect to sāpadasaptādhyāyī (SPSA) sutras (`_aps_num < 82000`).**

In practice:

| Current sutra | Can see |
|---|---|
| SPSA (`_aps_num < 82000`) | Outputs of SPSA sutras only — tripāḍī outputs are invisible (asiddha) |
| TripāḍÄ« (`_aps_num ≥ 82000`) | Outputs of all SPSA sutras + earlier tripāḍī sutras (lower `_aps_num`) |

This is implemented by walking up the tree and skipping nodes whose sutra `_aps_num` falls outside the visible range. The walk stops at the first visible node, and that node's `outputs` become the view.

**Special siddha exceptions** (`_special_siddha()` in `antaranga_prakriya.py`): certain tripāḍī outputs must be visible to specific later rules even across the SPSA/tripāḍī boundary:

| Producer sutra | Visible to | Reason |
|---|---|---|
| ṣṭutva 8.4.41 | ḍ-lopa 8.3.13 | ṣṭutva output must be seen before ḍ-lopa fires |
| ḍ-lopa 8.3.13, r-lopa 8.3.14 | pūrva-dīrgha 6.3.111 | lopa must be visible for dīrgha to apply correctly |
| n-lopa 8.2.7, 7.4.33 | 7.4.25 | n-lopa siddha for inter-pada and rājīyati/rājāyate forms |
| saṃyogānta-lopa 8.2.23 | maGavan upadhā-dīrgha 6.4.8.1 | final cluster lopa must be visible for upadhā-dīrgha to fire correctly for maGavan before sarvanamasthāna |

**Partially implemented:** *ābhīya asiddhavat* (6.4.22 असिद्धवदत्राभात्) — see the next subsection. **Not yet implemented:** *ṣṭutokora-siddhaḥ* (a further sub-boundary within tripāḍī). This and the broader scope of 6.4.22 are noted as FIXMEs in the code.

### Ābhīya asiddhavat (6.4.22, partial)

Pāṇini 6.4.22 declares that outputs of rules within the *ābhīya* section (6.4.x for x > 22, up to the end of pāda 6.4) are **asiddha (invisible) to each other** when they are *samanāśraya* (apply to the same locus). Two specific shapes drive the implementation:

1. **One rule's output must not trigger another rule.** E.g. गार्ग्यायणी: 6.4.148 (यस्येति च) drops the final 'a' of *gārgyāyana* → *gārgyāyan*; 6.4.134 (अल्लोपोऽनः) must **not** then misfire on the artificial 'an' tail (giving गार्ग्याय्णी). Per 6.4.22, 6.4.134 should never see 148's output.
2. **Both rules' edits must compose into the final output.** E.g. गार्गी: 6.4.148 drops the final 'a' of *gārgya*; 6.4.150 (हलस्तद्धितस्य) drops the upadhā 'य'. Both are asiddha to each other for condition-checking, but the merged stem must show **both** edits → *gārg* → गार्गी.

Naive view-walking (just hiding peer outputs from `view()`) deadlocks: if the xform also reads the view, each rule operates on the pre-section snapshot and overwrites its peer's edit, oscillating forever. The lesson — **condition-view and xform-input must diverge** — drives the design below.

#### Mechanism (snapshot + diff composition)

In `antaranga_prakriya.py`:

- **Predicate** `_in_abhiya(aps_num)` — `64022 < aps_num < 64176`. Drop-in for the ābhīya scope.
- **Static peer table** `_ASIDDHA_PEERS: dict[str, frozenset[str]]` — symmetric adjacency: `rule_aps → set of peers it does NOT see`. Currently:
  - `6.4.148 ↔ {6.4.150, 6.4.134}`
  - `6.4.134 ↔ {6.4.148}`
  - `6.4.150 ↔ {6.4.148}`

  Static rather than dynamic-via-window because the rule set is small and we want auditable, peer-specific scope. Add a pair when you find/design a new samanāśraya interaction; do **not** blanket-enable section-wide (some same-section pairs are intentionally not samanāśraya and over-firing breaks them — e.g. 6.4.128 optional + 6.4.133 samprasāraṇa).
- **Per-window snapshot.** `view()` for an ābhīya rule walks the PrakriyaTree up past any parent node whose sutra is an `_is_asiddha_peer` of the current rule, and returns that ancestor's outputs as the snapshot. The snapshot is **what the rule's condition sees** *and* **what its `operate()` receives** — so the rule's own xform produces a snapshot-relative result (`target`).
- **Diff composition.** `_compose_abhiya(snapshot_str, current_str, target_str)`:
  - Uses `difflib.SequenceMatcher` to derive per-snapshot-position edit dicts for *prior peer edits* (snapshot → current) and *this rule's edits* (snapshot → target).
  - Merges the two edit dicts position-by-position. Same-position conflicts raise `AssertionError` — surface them rather than silently picking, since our peer table is supposed to guarantee non-overlapping edits.
  - Replays the merged edits over the snapshot to produce the new current state.
- The composed string overwrites `lc + l` (or `rc + r`) on the current output objects, so subsequent rules (ābhīya or not) see the cumulative state.

Walk of गार्गी (window `gārgya | ī`, snapshot `gārgya`):

| step | what evaluates against | what fires | current after |
|------|------------------------|------------|----------------|
| 1 | 6.4.148, 6.4.150 both trigger on snapshot | 6.4.148 wins (lower aps_num) | `gārgy` |
| 2 | 6.4.150 condition checked against snapshot (148 hidden); still matches (`l='a', ll='y'`, hal upadhā) | 6.4.150; diff vs snapshot = "drop upadhā य"; compose with prior diff ("drop final a") → `gārg` | `gārg` |
| 3 | no further ābhīya triggers | — | merge with ī → गार्गी |

Walk of गार्ग्यायणी (window `gārgyāyana | ī`, snapshot `gārgyāyana`):

| step | what evaluates against | what fires |
|------|------------------------|------------|
| 1 | 6.4.148 triggers (snapshot l='a'); 6.4.134 does NOT trigger (snapshot l='a', not 'n') | 6.4.148 → current = `gārgyāyan` |
| 2 | 6.4.134 re-checked against snapshot (148 hidden) — snapshot l still 'a' → no match | — |
| 3 | no more ābhīya triggers, merge with ī, ṇatva via 8.4.x | → गार्ग्यायणी ✓ |

#### How to add an ābhīya rule

1. Write the rule's condition against the **original (pre-section) state**, not against the post-148 (or post-other-peer) state. E.g. SK472's 6.4.150 detects `lp ends in hal+y+a` via helper `hal_taddhita_ya_upaDa` in `paribhasha.py` — it does *not* assume the final 'a' has been dropped.
2. The xform should produce a clean snapshot-relative edit (a single delete / replace / insert, ideally one character). `_compose_abhiya` handles position remapping when peers have already edited.
3. **If your new rule needs to be invisible to (or invisible from) an existing peer**, add the pair to `_ASIDDHA_PEERS` symmetrically: `A → {B}` *and* `B → {A}`. Asymmetric entries are accepted but rarely correct.
4. Run the targeted test for your rule and the **full regression** — over-broad peer entries silently regress unrelated paths (we caught this with `maGavan` and `BAt_strI` during development). If a same-position conflict surfaces in `_compose_abhiya`, treat it as a real samanāśraya violation: re-check whether the two rules genuinely apply to the same locus.

#### Limits of the current implementation

- **No vārttika carve-outs.** Pāṇini's *वुग्युटावुवङ्यणोः सिद्धौ वक्तव्यौ* declares vuk-augment, yuṭ-augment, *uvaṅ*, and *yaṇ* as siddha within the ābhīya section. Our peer table doesn't currently include them, so the carve-out is unneeded; when extending into rules that use these, add explicit `_special_siddha` entries (existing mechanism in `view()`) instead of relying on the predicate alone.
- **No tag-level diff composition.** `_compose_abhiya` operates on the canonical string only. If two ābhīya peers need to make non-overlapping *tag* edits (set/clear), extend the diff representation or move that semantics to `update:`.

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

Input-construction flags (each takes one or more globally-defined object names from `pratyaya.py` / `pratipadika.py` / `dhatu.py` / `avyaya.py`):

| Flag | Action | Equivalent in code |
|------|--------|---------------------|
| `-p`, `--pratyaya` | Add a pratyaya as-is | `pratyaya` |
| `-d`, `--dhatu` | Add a dhātu as-is | `dhatu` |
| `-t`, `--pratipadika` | Add a prātipadika as-is | `pratipadika` |
| `-m`, `--samasta-pratipadika` | Wrap uttara-pada(s) with `?samAsa` | `in_compound(p)` |
| `-u`, `--purva-pada` | Wrap pūrva-pada(s) with `?samAsaPurva` | `as_purva_pada(p)` |
| `-D`, `--dvigu` | Wrap uttara-pada(s) with `?samAsa + ?dvigu` | `in_context(in_compound(p), "dvigu")` |
| `-B`, `--bahuvrihi` | Wrap uttara-pada(s) with `?samAsa + ?bahuvrIhi` | `in_context(in_compound(p), "bahuvrIhi")` |
| `-s`, `--string` | Raw SLP1 string; trailing `*` → aṅga, `_` → pada | `PaninianObject(...)` |
| `-o`, `-c` | Open / close bracket (hierarchical input) | nested list |
| `-a` | Avasāna marker (ends the input chain) | `avasAna` |

Examples (manual testing of compound rules):

```bash
# SK479 ṅīp on Dvigu: tri+loka → त्रिलोकी
sanskrit_generator -u tri -p luk_sup -D loka -p strI_abs --vibhakti

# SK480 ṭāp on Dvigu+tadDita-luk: dvi+bista → द्विबिस्ता
sanskrit_generator -u dvi -p luk_sup -D bista -p luk_tadDita -p strI_abs --vibhakti

# parimāṇa counter to SK480: dvi+AQaka → द्व्याढकी (ṅīp survives)
sanskrit_generator -u dvi -p luk_sup -D AQaka -p luk_tadDita -p strI_abs --vibhakti
```

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

To run all tests

```bash
source ~/venv/sanskrit/bin/activate
source sourceme
pytest -n 6 sanskrit_parser/generator/test/
```

To run one test file (for example)

```bash
source ~/venv/sanskrit/bin/activate
source sourceme
pytest -n 6 sanskrit_parser/generator/test/test_halanta.py
```

To run tests for one pratipadika (for example)
```bash
source ~/venv/sanskrit/bin/activate
source sourceme
pytest -k "rAma" sanskrit_parser/generator/test/test_ajanta_pum.py
```


Use the `--verbose-prakriya` and `--tag-display` options for more
details when tests fail
