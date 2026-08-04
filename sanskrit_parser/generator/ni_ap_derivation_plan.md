# Deriving ङी / आप् instead of pre-tagging them — migration plan

**Status: NOT STARTED.** Written 2026-08-03 from an exploration pass; findings below are
measured against the tree at commit `f524e44` unless marked as inference.

## Context

`pratipadika.py` carries **38 stems pre-tagged `?NI` / `?Ap` / `?NIp` / `?nadI`** — ब्राह्मणी,
अजा, सेना, गङ्गा … — i.e. feminines stored ready-formed with a marker saying which feminine
affix produced them. The goal is to delete those tags (and, where possible, the stems), and
derive every feminine live as `[base, strI_abs]`, letting the ~55 rules of the 4.1.x
ṭāp/ṅīp machine decide the affix.

Two forces make this worth doing:

1. **The pre-tagging drifts, and it has already caused bugs.** ब्राह्मणी was missing `?NI`
   although it is a ङीप् formation (4.1.15); सुकेशी carries only `?svAnga_I`. Phase X2 hit
   this directly — सुकेशीभार्यः also came out as सुकेशिभार्यः — and it is why SK999/6.3.61
   had to be scoped to an opt-in marker instead of running on its own condition
   (`generator_status.md`, the 6.3.61 Skipped row). The standing 5.4.153 नदी-arm note has
   the same root cause.
2. **It is redundant with work already done.** `vibhaktis_list.py` uses `strI_abs`
   **177 times**; `prAtipadika["aja_A"] = [aja, strI_abs]` already sits beside the
   pre-formed `ajA`.

**The headline finding: the feminine derivation is NOT the obstacle.** With SK985/6.3.43
relocated to `bahiranga: 3` and its uttara content-check dropped, the live derivation
produced the correct form — `[brAhmaRa, strI_abs] + गोत्र → ब्राह्मणिगोत्रम्`, identical to
the pre-formed stem; likewise `[aja, strI_abs] + क्षीर → अजक्षीरम्`. What blocks the
migration is the **uttara content-match**, which is the same obstacle phases X4/X5 met.

---

## 1. Why the pre-tagging exists (the bahiranga argument)

| bahiranga | contents |
|---|---|
| **−2** | kāraka pre-pass (112 rules) |
| **−1** | **samāsa pre-pass (203 rules)** — where the ṅyanta/ābanta rules currently live |
| **0** | 1.4.3 यू स्त्र्याख्यौ नदी — the nadī saṁjñā (22 rules) |
| **1** | 30 rules |
| **2** | **ṭāp / ṅīp selection — ~55 rules (4.1.4/5/6/15/40/41/54 …), and 2.4.71 sup-luk** (69 rules) |
| **3** | 1 rule |
| default 9 | main scan (310 rules) |

A pre-pass rule at −1 runs three levels before the affix is chosen. **Verified:** at −1 the
live-derived member is the bare base — `brAhmaRa`, a-final, no `?NI`, no `?Ap`, and the
`strI_abs` element is not part of the member at all. There is no ī to shorten. So `?NI` on a
stem is a device for smuggling a bahiranga-2 outcome into a bahiranga-−1 condition.

Note the two tags are not synonyms and should not be merged: `?NI` means *"the ī is a ङी
affix"* (the ङ्यः / अङ्यः condition of 6.3.43 / 6.3.61), while `?nadI` — **derived at runtime**
by 1.4.3, hence always complete — means *"has the nadī saṁjñā"*, which covers any feminine
ī/ū whatever its origin (तन्त्री, लक्ष्मी, श्री included). Conflating them **is** the 5.4.153 bug.

---

## 2. Inventory

**11 stems are deletable today** — a base stem already exists, so `[base, strI_abs]`
replaces them with no new stems:

`brAhmaRI` (← brAhmaRa) · `kalyARI` (← kalyARa) · `kumArI` (← kumAra) · `mAlA` (← mAla) ·
`kuSA` (← kuSa) · `karRI` (← karRa) · `naKI` (← naKa) · `haMsI` (← haMsa) · `ajA` (← aja) ·
`gOrI` (← gaura) · `ekA` (← eka)

**27 have no base stem present.** Each needs a base added — गङ्गा ← गङ्ग, सेना ← सेन,
इष्टका ← इष्टक, वडवा ← वडव, यूका ← यूक, राक्षसी ← राक्षस, रेवती ← रेवत, रोहिणी ← रोहित (4.1.39!),
प्रवाणी, प्रमाणी, पञ्चमी, नाडी, नासिका, निशा, प्रजा, मेधा, जाया, जटा, रमा, स्थाली, लिक्षा, इषीका,
दुह्यमाना, `dvi_s` — **or is genuinely lexical and must keep its stored vowel**:
`nadI`, `strI`, `lakzmI`, `SrI`, `tantrI`, `pfTivI`.

**Independent of the migration, these are latent bugs to fix either way:**
- `sukeSI` (`:134`) lacks `?NI` — सुकेश + ङीष् by 4.1.54. *This is the one that broke X2.*
- `strI_pUrva` (`:828`) lacks `?NI` while its duplicate-surface twin `strI` (`:809`) has it.
- `haMsI` (`:1232`) carries **`?NIp`, which no rule reads** — a dead tag (the three
  `NIp_taddhita` hits are a different, affix-side tag). Should be `?NI`.
- `pfTivI` carries a **lexical `?nadI`**, the only stem doing so, and redundant since 1.4.3
  derives it.
- `dAsI` (`:527`) — probably ङीष् via गौरादि; check the gaṇa before asserting.
- **The `?Ap` side has the same gap:** five ā-final feminines lack `?Ap` — खट्वा, **दत्ता**,
  पाचिका, सुपर्णा, विद्या. दत्ता is pointed: it is SK's own ङ्यः-किम् counter-example for
  6.3.43 (दत्तातरा — ṭāp, not ṅīp).

---

## 3. What the migration takes

### Step A — vibhakti tests (easy; mostly already done)

Delete the 11 deletable stems and repoint their `vibhaktis_list.py` entries to
`[base, strI_abs]`, following the 177 existing uses. Self-contained: no rule changes, no
bahiranga questions. `aja_A` shows the target shape and can absorb `ajA` outright.

### Step B — pin down where `?NI` is lost (DO THIS BEFORE COSTING STEP C)

**The one genuine unknown.** A `?NI` gate at bahiranga 3 fails for *both* the pre-formed and
the live path, yet the vocabulary is consistent: `NIp`/`NIz`/`NIn` all carry tag `NI`
(`pratyaya.py:175-180`), `Ap` carries `Ap` (`:181`), and `paninian_object.py:336`
propagates `["NI", "Ap", "UN", "strI_abs"]` from the affix to the merged stem. A probe of the
merged stem showed only `?strI` surviving. So this is a tag **surviving** problem at a
subsequent merge, not a naming mismatch — *inferred from code reading, not isolated.*

Isolate it with a two-element merge (`[brAhmaRa, strI_abs]`, no sup) instrumented inside
`join_objects`, then the same with a sup, then inside a compound. The answer decides
everything:

- **If `?NI` merely needs adding to a propagation list** → step C is modest and the
  migration completes.
- **If `?NI` is structurally unavailable post-merge** → step C's marker would have to carry
  the ṅī-ness itself, but that marker can only be set at −1, where ṅī-ness is not yet
  known. That is circular, and **the pre-tagged stems must stay for the pre-pass rules
  specifically** — in which case stop after step A and treat §2's latent bugs as the
  deliverable.

### Step C — relocate the ṅyanta/ābanta rules (verified viable)

1. **Move them from `bahiranga: -1` to `~3`** — the near-empty slot just after ṭāp/ṅīp
   selection. Verified: the hrasva fires there on both paths.
2. **Convert every uttara CONTENT check to a TAG check.** At bahiranga 3 the uttara has
   merged with its sup, so `rp: =gotra` and `r: s` can no longer match — the X4/X5 lesson.
   A −1 marker rule tags the uttara (`?ghrupakalpa_uttara` and friends); the relocated rule
   reads the marker. This is the 8.4.12 → 8.4.1 two-step lever, so it is the **same
   machinery X6 builds for ṇatva** — sequence this after X6 and reuse it.

Affected rules: SK985/6.3.43, SK999/6.3.61, SK1000/6.3.62, SK1001/6.3.63, SK1006/6.3.65
(all X2), plus SK/5.4.110 and SK833/5.4.153 which also read `?NI` at −1.

### Step D — payoff

With C in place, delete `?NI`/`?Ap` from the 11 + add bases for as many of the 27 as are
worth it, and **un-scope SK999/6.3.61** (drop `?gAlava_hrasva`), which is the standing
Skipped row this whole exercise buys back.

---

## 4. Recommended order

1. §2's latent bugs — but **only for the 27 stems that keep a lexical form**; adding `?NI`
   to a stem step A will delete is wasted motion.
2. Step A (vibhakti tests).
3. Step B (the probe). Ten minutes, and it decides whether to continue.
4. Step C — **after X6**, reusing its marker lever.

## 5. Verification

```bash
cd sanskrit_parser/generator/test && PYTHONPATH=<repo root> /Users/karthik/venvs/sanskrit/bin/pytest -n 8 --dist worksteal
```

Baseline at `f524e44`: **8422 passed**. Step A should be surface-neutral — any change in a
vibhakti table means the live derivation and the stored form disagree, which is itself the
bug worth finding. Step C must additionally re-check the forms 6.3.61 damaged when
unscoped: केशाकेशि / मुष्टीमुष्टि / बाहूबाहवि (6.3.137), अग्नीवरुणौ (6.3.27), ऊरीकृतम् (avyaya),
सुकेशीभार्यः (ङीष्).
