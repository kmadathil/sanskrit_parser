# Deriving ङी / आप् instead of pre-tagging them — migration plan

**Status: COMPLETE for the pūrva-hrasva family — steps 0, 1, A, B, C, D all done
(2026-08-05).** A live-derived `[brAhmaRa, strI_abs]`
pūrva now takes 6.3.43's hrasva — the mechanism the whole migration rests on — and all five
X2 pūrva rules have moved to the main-scan member window. §3 step C records the levers.
Step D is done too: 6.3.61 is un-scoped and **ten stored feminine stems are gone**; the
tooling blocks (dvandva / kāraka drivers) came down with it. §3 step D records the two real
boundaries that stop the migration going further. Written
2026-08-03 from an exploration pass; findings below are measured against the tree at commit
`f524e44` unless marked as inference or dated 2026-08-05.

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

**The headline finding: the feminine derivation is NOT the obstacle.** The live derivation
produces the correct form — `[brAhmaRa, strI_abs] + गोत्र → ब्राह्मणिगोत्रम्`, identical to the
pre-formed stem. What blocked it was the **uttara content-match**, the same obstacle phases
X4/X5 met. **Resolved 2026-08-05** (§3 step C): the five X2 pūrva rules moved to the
**main-scan member window** (not `bahiranga: 3`, as this paragraph originally guessed), each
uttara content check became a stem-class tag riding tier 2, and `?NI`/`?puMvat` reach that
window through the pūrva's sup-luk.

---

## 1. Why the pre-tagging exists (the bahiranga argument)

| bahiranga | contents |
|---|---|
| **−2** | kāraka pre-pass (112 rules) |
| **−1** | **samāsa pre-pass (203 rules)** — where the ṅyanta/ābanta rules used to live (moved to the main scan 2026-08-05) |
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

Three buckets, not two (revised 2026-08-05 — the original needs-a-base / genuinely-lexical
split did not survive contact with the stems):

**Bucket 1 — 12 stems deletable today**, a base stem already exists, so `[base, strI_abs]`
replaces them with no new stems:

`brAhmaRI` (← brAhmaRa) · `kalyARI` (← kalyARa) · `kumArI` (← kumAra) · `mAlA` (← mAla) ·
`kuSA` (← kuSa) · `karRI` (← karRa) · `naKI` (← naKa) · `haMsI` (← haMsa) · `ajA` (← aja) ·
`gOrI` (← gaura) · `ekA` (← eka) · **`rohiRI` (← rohita)**

`rohiRI` was originally filed under "no base present (4.1.39!)". It belongs here: `rohita`
exists (`:383`, already tagged `?varNa_topaDa`), 4.1.39 वर्णादनुदात्तात्तोपधात्तो नः is
implemented (`sutras_antaranga.yaml:6045`), and `vibhaktis_list.py:2602` **already** derives
`prAtipadika["rohiNI"] = [rohita, strI_abs]`. Its त्-final base — the one non-a-stem case in
the whole inventory, which is why the original entry flagged it — is the case already solved.

**Bucket 2 — base addable.** ~~गङ्गा ← गङ्ग · सेना ← सेन · इष्टका ← इष्टक · वडवा ← वडव ·
यूका ← यूक · राक्षसी ← राक्षस · रेवती ← रेवत · पञ्चमी ← पञ्चम · नाडी ← नाड · स्थाली ← स्थाल ·
दुह्यमाना ← दुह्यमान · नासिका ← नासिक~~ — **resolved in step D.** DONE: `izwakA`, `izIkA`,
`revatI`, `yUkA`, `duhyamAnA` (+ `ramA`, `jawA`, `niSA`, which this bucket had missed).
Still held, and by rules rather than by a missing base: गङ्गा, सेना, वडवा, राक्षसी, पञ्चमी,
नाडी, स्थाली, नासिका — all uttara-position (some also standalone). **`रेवती ← रेवत` was
wrong**: the base is the ugit रेवत्, since an a-stem gives *रेवता (see step D).

**Bucket 3 — lexical, keep the stored stem.** The six the plan named — `nadI`, `strI`,
`lakzmI`, `SrI`, `tantrI`, `pfTivI` — plus प्रवाणी / प्रमाणी, which are kṛt/nipātana formations
(प्र+वे+ल्युट्, cf. 5.4.160), not base + ङीप्, and जाया (nipātana).

**Correction (2026-08-05):** an earlier revision of this bucket also swept in निशा, प्रजा, रमा,
मेधा, जटा, लिक्षा, इषीका on the ground that their bases "would have to be invented"
(*निश, *प्रज …). **That reason does not hold.** A prātipadika is a grammatical object, not
necessarily an independently used word: for Pāṇini खट्वा *is* खट्व + टाप्, and 4.1.4
अजाद्यतष्टाप् applies to every a-final stem whether or not the masculine is attested. इषीका
was in that list and derives perfectly from `izIka` — it has since been converted and its
stored stem deleted. So lexical attestation of the base is **not** a blocker on the ā-side;
what decides an ā-stem's fate is only where it is USED (see step D). The ī-side is different
and is where the real per-stem question lives — the base's class has to trigger the right ङी
rule (रेवत् needed its ugit; लक्ष्मी/तन्त्री/श्री have no ङी at all, which is why they belong
here on the merits).

`dvi_s` was in the inventory in error — it is `Pratipadika("dvi", "strI", ?saMKyA,
?nityadvivacana)`, not an ī/ā feminine, and has no `?NI`/`?Ap` to delete.

**`?NI` on the bucket-3 stems — absence is usually CORRECT, not a gap:**

| stem | tags | why |
|---|---|---|
| `nadI` | `?NI` | ङीप् formation — keeps the tag |
| `strI` | `?NI`, `?strI_p` | the ī **is** ङीष् (hence 1.4.4's अस्त्री, hence अतिस्त्रि) — keeps it |
| `lakzmI` | `?uras_praBfti`, **no `?NI`** | unādi/nipātana ī → उरःप्रभृति कप् (5.4.151) |
| `SrI` | `?DAtu`, `?kvip`, **no `?NI`** | the ī is the root's own (श्रिञ् + क्विप्) |
| `tantrI` | none, **no `?NI`** | unādi ī (uṇ III.158) — why बहुतन्त्रीः keeps its long ī |
| `pfTivI` | **now `?NI`** (was `?nadI`) | ङीष् by the vārtika पृथिव्यां ङीष् — see the fix below |

So "lexical" covers two opposite encodings. **Do not work §2's latent-bug list from the shape
"ī-final feminine without `?NI` = bug"** — for लक्ष्मी/श्री/तन्त्री the missing `?NI` is
the correct encoding, and adding it breaks precisely the forms the tag exists to protect
(बहुतन्त्रीः, श्रीमदः). That is the `strI_pUrva` error below, in reverse. The **decider is
6.1.68 हल्ङ्याब्भ्यो दीर्घात् सुतिस्यपृक्तं हल्**, which elides the nom-sg `su` only after a
ङी/आप्: so a stem whose correct nom sg has a **visarga** (लक्ष्मीः, तन्त्रीः, श्रीः) must NOT
have the tag, and one whose nom sg is bare (नदी, दासी, पृथिवी) must have it. That is a
mechanical test, and it is how the fixes below were checked.

**§2 latent bugs — FIXED 2026-08-05** (step 1 of §4). Every one of them showed up as a
spurious nom-sg visarga, i.e. as a real wrong form, not just a missing marker:

| stem | was | now | nom sg before → after |
|---|---|---|---|
| `sukeSI` | `?svAnga_I` only | **`+?NI`** (ङीष् 4.1.54) | *सुकेशीः → सुकेशी. *This is the one that broke X2.* |
| `haMsI` | `?NIp` (dead tag) | **`?NI`** | *हंसीः → हंसी |
| `pfTivI` | `?nadI` (lexical) | **`?NI`** | *पृथिवीः → पृथिवी |
| `dAsI` | — | **`+?NI`** | *दासीः → दासी |
| `KawvA` | — | **`+?Ap`** | *खट्वाः → खट्वा |
| `dattA` | — | **`+?Ap`** | *दत्ताः → दत्ता |
| `pAcikA` | — | **`+?Ap`** | *पाचिकाः → पाचिका |
| `suparRA` | — | **`+?Ap`** | *सुपर्णाः → सुपर्णा |
| `vidyA` | — | **`+?Ap`** | *विद्याः → विद्या |

**The `?Ap` fixes flushed out a tag overload** (fixed in the same round): `?saMjYA` was doing
two jobs — SK839/6.3.38 संज्ञापूरण्योश्च reads it as *"this feminine WORD is a proper name"*
(दत्ता), while SK1001/6.3.63 ङ्यापोः संज्ञाछन्दसोर्बहुलम् and SK857/8.4.3 पूर्वपदात्संज्ञायामगः
read it as *"the COMPOUND is a name"*. दत्ता carries the word-level one lexically, so the
moment it got its (correct) `?Ap`, 6.3.63 matched and forked दत्ताभार्यः into a spurious
*दत्तभार्यः. Fix: the word-level sense is now `?strI_saMjYA` (6.3.38 + the दत्ता stem), leaving
bare `?saMjYA` to mean compound-level, as the other two rules already use it. Worth knowing
before the rest of the migration: **every stem that gains `?NI`/`?Ap` becomes newly visible to
the ṅyanta/ābanta rule set**, so a tag addition is never purely cosmetic.

`pfTivI` turned out NOT to be "drop the redundant `?nadI`": `?nadI` alone does not reach
6.1.68 (which wants ङी/आप्), so पृथिवी was declining with a visarga. It needs `?NI`, and then
the lexical `?nadI` really is redundant — 1.4.3 derives it. `dAsI` is tagged on the same
surface evidence; **which** sūtra supplies its ङीष् (गौरादि 4.1.41?) is still unchecked —
दास is not in the gaṇa list in `pratipadika.py`, so the plan's "probably गौरादि" stands
unconfirmed and is recorded in the stem's comment. दत्ता keeps its point: it is SK's own
ङ्यः-किम् counter-example for 6.3.43 (दत्तातरा — ṭāp, not ṅīp), and now carries the ṭāp tag
that makes that gate meaningful.

**`strI_pUrva` (`:830`) is not a tag gap — it is a duplicate to DELETE.** (Measured
2026-08-05; it was previously listed above as "lacks `?NI`", which is the wrong fix — adding
`?NI` is as much a no-op as removing it was.) It is a tag-stripped clone of `strI` (`:809`,
`?NI` + `?strI_p`), same surface and same liṅga, used by exactly one case —
`B3-strIpramARaH` (SK832/5.4.116, स्त्रीप्रमाणः) in `samasa_list.py`. It guards against
nothing:

- Its comment blames 6.3.34, but that rule gates on `lp: ?puMvat`, which is
  **composer-supplied and never derived** — the कल्याणीपञ्चमाः case beside it has to pass
  `"tags": ["puMvat"]` explicitly. A plain `strI` pūrva never has it. (The grammatical point
  — स्त्री is not bhāṣitapuṁska — is right; it just never needed a second stem, because the
  marker model already makes puṁvadbhāva opt-in.)
- 1.2.48 cannot reach a pūrva at all: arms 1–3 need `rp: ?pum_abs` (an explicitly inserted
  pratyaya element, used only by vibhakti tests), arm 4 needs the **uttara** plus its `?sup`,
  and a pūrva's sup luks by 2.4.71. That matches the grammar — 1.2.47's प्रातिपदिकस्य
  anuvṛtti makes 1.2.48 shorten the COMPOUND-FINAL (निष्कौशाम्बिः, अतिखट्वः, अतिस्त्रि),
  never a pūrva member.
- The other `?NI`-reading pūrva rules need more: 6.3.43 wants `?puMvat` + a
  चेलट्/ब्रुव/गोत्र/मत/हत uttara; 6.3.63 wants `?saMjYA`/`?Candas`. प्रमाणी is none of these.
- `?strI_p` is read only by 6.4.79/6.4.80 (iyaṅ) and 1.4.4 (nadī), all of which need a
  following ac-initial sup — so **both tags are structurally inert in pūrva position, for
  any stem**, which is why no pūrva-position clone is ever needed.

Measured: `strI_pUrva`, `strI`, and `strI_pUrva` + each tag re-added all give the identical
surface `strIpramARaH` and the identical fired trace `[1.2.43, 2.2.24, 5.4.116]`; a full
8×3 vibhakti/vacana sweep of the compound is byte-identical between the two stems.

Fix = delete `strI_pUrva`, repoint the one case at `strI`. Two reasons to do it rather than
leave it: it is exactly the duplicate-surface shadowing hazard (two `Pratipadika("strI", …)`,
one silently under-tagged); and it is a trap for **step D** — if 6.3.61 is ever un-scoped, a
`?NI`-less स्त्री is precisely the shape its `?!NI` (अङ्यः) gate looks for, and only the
`$$ik_dIrGa_anekAc` ekāc guard then stands between it and a wrong *स्त्रिप्रमाणः. Note this
is the opposite polarity from the rest of §2: those are stems that stay and need a tag added;
this is a stem that should not exist.

---

## 3. What the migration takes

### Step A — vibhakti tests (easy; mostly already done)

Delete the bucket-1 stems and repoint their `vibhaktis_list.py` entries to
`[base, strI_abs]`, following the 177 existing uses. Self-contained: no rule changes, no
bahiranga questions. `aja_A` shows the target shape and can absorb `ajA` outright.

**Caveat (2026-08-05):** "delete the stem" only holds for stems used *solely* as a
`vibhaktis_list.py` paradigm entry. A stem also used as a **compound member** in the samāsa /
kāraka lists cannot be deleted — the composer takes ONE `Pratipadika` object per member, so
there is no place to put a second `strI_abs` element. For those, step A is the narrower
"repoint the vibhakti entry, keep the stem" and the stem's deletion waits on step C.

**Step A RESULT (2026-08-05): it is already done, and bucket 1 is much smaller than 12.**

*Repointing:* the only bucket-1 stems with a `vibhaktis_list.py` paradigm entry are
`brAhmaRI`, `kumArI`, `gOrI`, `rohiRI` — and all four are **already** `[base, strI_abs]`
(`:3143`, `:1885`, `:2650`, `:2602`), plus `aja_A`. There is nothing left to repoint.

*Deletion:* of the 12, **eleven are compound members** in `samasa_list.py` /
`samasa_asraya_list.py` / `karaka_list.py` / `manual_list.py`, so the caveat blocks them. The
twelfth, `naKI`, is used only in `vibhaktis_list.py:4173` (शूर्पनखी) — and it must stay too,
for the reason below.

*And the "a base exists, so `[base, strI_abs]` replaces it" premise only holds for 6 of 12.*
Probed each pair directly (nom. sg., live vs stored):

| replaceable | fork (optional rule) | **different lexeme** |
|---|---|---|
| `brAhmaRI` `kumArI` `mAlA` `ajA` `gOrI` `ekA` | `kalyARI` → कल्याणा/कल्याणी · `rohiRI` → रोहिता/रोहिणी (4.1.39 is `optional: true` **by design**) | `kuSA` → *कुशी (कुश is ?jAnapadAdi → ङीष् 4.1.42; the grass कुशा is ṭāp) · `karRI` → *कर्णा · `naKI` → *नखा · `haMsI` → *हंसा (needs 4.1.63 जातेरस्त्रीविषयादयोपधात्, not present) |

The right-hand column is not a tagging gap — those bases are **homographs of a different
word**, so `[base, strI_abs]` is simply the wrong derivation and the stems must stay. The
middle column would need a marker to pick one fork. So bucket 1's real deletable set, once
step C lifts the compound-member block, is **6 stems**, not 12.

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

**STEP B RESULT (2026-08-05) — it is the FIRST branch: a propagation-list gap. Step C is
unblocked.** Instrumented `PaninianObject.join_objects` and logged every merge:

```
1. [brAhmaRa, strI_abs]        JOIN [('brAhmaR',[]), ('I',[NI,strI])]        -> 'brAhmaRI' [NI,strI]
                               JOIN [('brAhmaRI',[NI,strI,nadI]), ('.',[])]  -> 'brAhmaRI.' [strI]
2. [brAhmaRa, strI_abs, su]    JOIN [('brAhmaR',[]), ('I',[NI,strI])]        -> 'brAhmaRI' [NI,strI]
                               JOIN [('brAhmaRI',[NI,strI,nadI]), ('',[])]   -> 'brAhmaRI'  [strI]
3. pre-formed brAhmaRI + su    JOIN [('brAhmaRI',[NI,strI,nadI]), ('',[])]   -> 'brAhmaRI'  [strI]
```

Three things fall out, and they rewrite the §1 diagnosis:

1. **The ṅīp merge is fine.** `(brAhmaR | ī)` produces `?NI` on the merged **aṅga**, live.
   So at bahiranga 2–3 the live-derived feminine *does* carry `?NI` — the earlier "only
   `?strI` survives" probe had read the object *after* its avasāna merge (line 2 above),
   which is what strips it. §1's "the pre-tagging exists because the affix is not yet chosen
   at −1" still holds; the "`?NI` is lost in derivation" worry does not.
2. **`?NI` (and `?nadI`) die at the aṅga+sup merge — identically for the PRE-FORMED stem**
   (case 3). This is not a live-path defect at all; it is symmetric.
3. **Cause, exactly:** `join_objects` builds a blank result and only named tags survive.
   `?NI`/`?Ap` ride solely through the strī-block (`paninian_object.py:371`), which fires
   only when **`last`** carries NI/Ap/UN/strI_abs. A sup carries none, and there is no
   tier-1/2/3 entry for NI/Ap — so nothing carries them from `first`.

**Fix for step C:** add `NI`, `Ap` (and `nadI`) to the **tier-2 aṅga-gated** propagation list
(`if first.hasTag("aNga")`, `paninian_object.py:286`) — which is precisely the right gate:
tier 2 is documented as "stem-identity tags that should not propagate at pada-pada
boundaries", and ṅī-ness is exactly that. One line, no new mechanism.

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

### Step C — SETTLED AND PROVEN ON 6.3.43 (2026-08-05)

The "can a pūrva member be live-derived?" question is answered **yes**, and an earlier note
here claiming the strī affix "breaks the (pūrva | uttara) adjacency every −1 rule depends on"
was **wrong**: `_samasa_prepass_after_reorder` computes its member pairs over member
**indices** (`_is_samasa_member` skips pratyayas), so an intervening `strI_abs` does not
break the pair. The only real obstacle was always §1's: at −1 the ṭāp/ṅīp choice has not been
made, so the member is still the bare base. That is what relocation fixes.

**The destination is the MAIN SCAN, not bahiranga 3** — the (pūrva-pada | uttara-pada) member
window that X6's cross-member ṇatva already uses. Three levers, all now in the tree:

1. **`?sup_luk`** (`pratyaya.py`) — `luk_sup` now carries it. NOT `?luk`: 1.1.63 न
   लुमताङ्गस्य reads `?luk` and would strip every tag off the merge.
2. **ṅī/āp identity across the pūrva's sup-luk** — `join_objects` propagates
   `NI`/`Ap`/`nadI`/`puMvat` when `first` is `?samAsaPurva` **and** `last` is `?sup_luk`.
   The luk gate is the load-bearing part: with an **aluk** pūrva (6.3.1 ff., स्तोकान्मुक्तः,
   आत्मनेपदम्) the retained sup *is* the pada's final, and `?NI` would be a false statement
   about it. This rides the existing `?samAsaPurva` channel (the one `?saMKyA`/`?avyaya`
   already use for 4.1.26) and is consumed at the `samasta_pada` merge, so it never leaks.
3. **`?puMvat` earned, not declared** — a feminine formed by ङी/आप् on a **masculine** stem
   is भाषितपुंस्क by construction, so the strī-block sets `?puMvat` when `first` is `?pum`.
   Without this the live path fails 6.3.43's भाषितपुंस्कात् gate while the pre-formed path
   (lexical `?puMvat`) passes — the asymmetry that would otherwise force the pre-tagging.

Plus item 2 above (content → tag): 6.3.43's uttara list is now the stem-class tag `?GarUpAdi`
on गोत्र/ब्रुव/मत/हत, riding tier 2 exactly as `?vana` does for X6.

**Result:** `[brAhmaRa, strI_abs] + गोत्र → ब्राह्मणिगोत्रम्`, identical to the pre-formed
path, with `?NI` and `?puMvat` both derived. Test
`X2-brAhmaRigotram-live-derived-SK985-6.3.43` (new `purva_strI_abs` hook in the X2 driver)
asserts it. The three pre-formed 6.3.43 cases keep their surfaces; their `fired` lists lost
`6.3.43` because the driver checks the **pre-pass** trace only, and the rule is no longer a
pre-pass rule.

**All five X2 rules are now relocated** (6.3.43, 6.3.61, 6.3.62, 6.3.63, 6.3.65). What each
needed beyond the move:

| rule | extra lever |
|---|---|
| 6.3.43 | `?GarUpAdi` on the uttara stems (tier 2) + `?NI`/`?puMvat` through the luk |
| 6.3.61 | `?gAlava_hrasva` added to the luk channel (a pūrva marker, same lifetime); its `?!NI` अङ्यः guard is what the move most improves — the tag now reaches this window on both paths |
| 6.3.62 | **nothing** — `=ekA` tests the pūrva's own content, which the sup-luk leaves untouched |
| 6.3.63 | `?Candas` added to the tier-1 list (`?saMjYA` was already there) |
| 6.3.65 | three **separate** self-named uttara tags `?cita`/`?tUla`/`?BArin` (tier 2) — a shared class tag would break the sūtra's क्रमात् pairing and license *इष्टकतूलम् |

A correction to an earlier note here: 6.3.65 does **not** get away without a marker. Its
*pūrva* content survives the luk, but its *uttara* content (`=cita` …) does not — only 6.3.62
is a pure move.

**Test-side:** the X2 driver now checks the **main-scan trace as well** as the pre-pass one
(`_main_scan_fired`, walking `p.tree` plus the nested `hier_prakriyas` the samāsa pre-pass
builds). Without it, all five rules would have had to drop their `fired` assertions and —
worse — every `not_fired` guard on them (ब्राह्मणीपुत्रः, गौरीपुत्रः, हरिपुत्रः, श्रीपुत्रः,
अजाक्षीरम्) would have gone vacuously true.

5.4.110 and 5.4.153 read `?NI` on the **uttara** and are samāsānta *selection* rules that must
run in the pre-pass; they are not relocation candidates, and a live-derived **uttara** remains
out of reach for them (its ī does not exist at −1 either). That is the remaining boundary of
the migration.

### Step D — payoff (DONE 2026-08-05)

**1. SK999/6.3.61 is UN-SCOPED.** The standing Skipped row is repaid: `?gAlava_hrasva` is
gone, the rule fires on its own condition, and the full suite is unchanged (8458). All four
damage causes were fixed at the root instead of by suppressing the sūtra:

| damage | fix |
|---|---|
| केशाकेशि / मुष्टीमुष्टि / बाहूबाहवि (6.3.137) | `?vihita_dIrGa` |
| अग्नीवरुणौ (6.3.27 ईदग्नेः) | `?vihita_dIrGa` |
| ऋषीवहम् (6.3.121) | `?vihita_dIrGa` — found by the suite, not in the original list |
| कारीषगन्धीपुत्रः / -पतिः / -बन्धु (6.1.13, 6.1.14 ṣyaṅ saṁprasāraṇa) | `?vihita_dIrGa` — likewise |
| ऊरीकृतम् | `?!avyaya` — the sūtra's **own** vārtika इयङुवङ्भाविनाम्**अव्ययानां** च न |
| सुकेशीभार्यः | already fixed in step 1 (सुकेशी gained its `?NI`) |

`?vihita_dIrGa` generalises the note the status doc asked for — *"a general 'this pūrva's
final vowel was just supplied by another rule' marker"*. Each supplying rule sets it in its
own `update:`; it rides the pūrva's sup-luk with `?NI`; 6.3.61 skips it. Two of the five
sources were **not** in the original damage list and only surfaced when the suite ran, which
is the argument for the marker over an enumerated guard list.

**2. Ten stems deleted in all** (five in the first pass, five more once the tooling blocks came down — see below), **and eleven cases now live-derived.** `gOrI` and `ekA` are gone —
`[gaura, strI_abs]` (ङीष् 4.1.41 गौरादि) and `[eka, strI_abs]` (ṭāp 4.1.4) — and X2's
अजक्षीरम् moved to `[aja, strI_abs]`, which proves **`?Ap` rides the sup-luk exactly as `?NI`
does**. The गौरीपुत्रः negative is now a stronger अङ्यः-किम् than it was: the `?NI` that blocks
6.3.61 is derived at the ṅīṣ merge rather than stored on a stem.

**3. Bucket 2: three more stems deleted — `izwakA`, `izIkA`, `revatI`.** An earlier draft of
this section claimed no bucket-2 base was worth adding because "every candidate has a use a
live derivation cannot serve". **That was wrong, and probing each candidate disproved it:**

| stem | live derivation | uses | outcome |
|---|---|---|---|
| `izwakA` | `[izwaka, strI_abs]` → ṭāp 4.1.4 | 2, both pūrva | **deleted** |
| `izIkA` | `[izIka, strI_abs]` → ṭāp 4.1.4 | 1, pūrva | **deleted** |
| `revatI` | `[revat, strI_abs]` → **ङीप् by 4.1.6 उगितश्च** | 1, pūrva | **deleted** |
| `yUkA` | `[yUka, strI_abs]` → ṭāp ✓ | 1, first member of a dvandva | blocked by TOOLING only — the dvandva driver has no `purva_strI_abs` hook |
| गङ्गा सेना वडवा राक्षसी पञ्चमी नाडी स्थाली नासिका | — | uttara (or uttara + standalone) | blocked, per the boundaries below |
| दुह्यमाना | — | standalone word in a kāraka sentence | blocked by tooling (no multi-element word in `karaka_list`) |

`revatI` is the instructive one: the plan's own inventory said "रेवती ← रेवत", and that is
**wrong** — `[revata, strI_abs]` yields *रेवता (ṭāp). The base is the **ugit** रेवत् (a
मतुप्-formation, and मतुप् is u-it), so it is registered `its=["u"]` — the same device
`nartaka` uses for its ṣ-it — and 4.1.6 उगितश्च then supplies ङीप्. For an ī-stem the base's
*class* is the whole question; for an ā-stem it never is, because 4.1.4 अजाद्यतष्टाप् catches
every a-final prātipadika.

**The remaining blocks, measured (2026-08-05).** They are THREE kinds, not two, and not the
same in severity — probing each is what showed it:

| | probe | pre-formed | live-derived |
|---|---|---|---|
| **A. samāsānta SELECTION** (5.4.153 नद्यृतश्च) | बहुकुमारीकः | `bahukumArIkaH` ✅ 5.4.153 fires | **`bahukumAriH` ❌ WRONG FORM** — no `?NI` at −1 → कप् never added → 1.2.48 then shortens the ī |
| **A′. compound FORMATION naming the feminine** (2.1.26 खट्वा क्षेपे, `lp: =KawvA`) | खट्वारूढः | `KawvArUQaH` ✅ | **no compound at all** — the pūrva never gets `?samAsaPurva`, since at −1 it is still खट्व |
| **B. B1 puṁvadbhāva** (6.3.41 जातेश्च) | ब्राह्मणीभार्यः | `brAhmaRIBAryaH` ✅ 6.3.41 fires | `brAhmaRIBAryaH` ✅ **right form, but 6.3.41 does NOT fire** |

A′ was found by building the tatpuruṣa driver's `strI_abs` hook and trying खट्वा through it —
the hook works, the sūtra does not. It is the sharpest form of the −1 problem: not a rule that
needs a TAG the live member lacks, but one that names the feminine's SURFACE. No propagation
channel can help, because the string itself does not exist yet.

**A is a wrong form; B is a lost attribution.** In B the surface survives only because 6.3.41
is a *prohibition* — it blocks puṁvadbhāva — and puṁvadbhāva (6.3.34) cannot fire on a live
pūrva either, since `?puMvat` is not on the raw base at −1. So the feminine survives by
default and the compound comes out right **for the wrong reason**: the sūtra that ought to be
responsible has dropped out of the derivation. Converting these stems would keep the suite
green on surface and silently gut the `fired` assertions — which is exactly what those
assertions exist to catch.

Why neither can be fixed the way the pūrva-hrasva family was:

- **A cannot be relocated.** 5.4.153 / 5.4.110 do not transform anything — they *select a
  samāsānta affix*, and the affix is inserted in the pre-pass (`_insert_samasanta`) because
  the compound then declines with it. A main-scan version would decide कप् after the
  declension it is supposed to feed. **A′ even less so**: 2.1.26 *is* the compound formation.
- **B's rules read LEXICAL properties of the feminine** — `?jAti`, `?kopaDa`, `?svAnga_I`,
  `?strI_saMjYA`, `?puMvat` — on the raw member at −1. `?puMvat` is now derivable (step C),
  and `?jAti` could sit on the base; but the rules would still be marking a member that has
  not yet become feminine, so the puṁvadbhāva they govern has nothing to act on.

Both need the ṭāp/ṅīp choice moved *before* bahiranga −1, which is a bahiranga-ordering
change, not a tag or a driver hook.

**Census of the 36 stems still carrying `?NI`/`?Ap`** (classified by their actual use, not by
family resemblance):

| why it stays | stems |
|---|---|
| **A. uttara position** — a −1 rule reads `?NI`/`?Ap` on the uttara (samāsānta selection and friends) | `kumArI` `nAqI` `pravARI` `pramARI` `paYcamI` `prajA` `meDA` `jAyA` `rAkzasI` `senA` `BaginI` `gaNgA` `sTAlI` `nAsikA` `mAlA` (pūrva use too, but the uttara one pins it) `vaqavA` `likzA` |
| **A′. formation names the feminine's surface** | `KawvA` (2.1.26) |
| **A″. ekaśeṣa must IDENTIFY the feminine at −1** (1.2.67 पुमान् स्त्रिया, 1.2.73 ग्राम्यपशु) | `haMsI` `ajA` |
| **B. B1 puṁvadbhāva** — surface survives, attribution lost | `brAhmaRI` `kalyARI` `dattA` `pAcikA` `sukeSI` |
| **not a rule at all: the base is a HOMOGRAPH** — `[base, strI_abs]` derives a different word | `kuSA` (कुश → *कुशी, ङीष् 4.1.42 jānapada) `karRI` (→ *कर्णा) `naKI` (→ *नखा) |
| **optional-rule FORK** — 4.1.39 is a वा, so the live form is रोहिणी/रोहिता | `rohiRI` |
| **the ī is not a strī-pratyaya** | `nadI` `strI` `pfTivI` |
| **derivation not modelled** — ṣyaṅ / kṛt / nipātana / taddhita bases | `kArIzaganDyA` `vidyA` `suparRA` |
| **open question** | `dAsI` — which sūtra supplies its ङीष् (गौरादि 4.1.41?) is still unchecked |

Only the last three rows are candidates for further work, and none of them is about `?NI`
propagation. `vidyA` / `suparRA` are the interesting pair: they are taddhita BASES
(`[vidyA, aR_t, strI_abs]` → वैद्यी), so a live version would be a feminine inside a feminine —
untested, and the one place left where a probe might still surprise.

**The tooling block is REMOVED (2026-08-05).** It was the third, smaller boundary — the
dvandva driver and `karaka_list` could not express a multi-element word. Both now can:
`_build_member` / `_build_word` return a LIST of elements and take `strI_abs: True`, the same
shape as the X2 driver's `purva_strI_abs`. Four more stems fell out:

| stem | now | what had held it |
|---|---|---|
| `yUkA` | `[yUka, strI_abs]` | dvandva driver (first member of यूकालिक्षम्) |
| `duhyamAnA` | `[duhyamAna, strI_abs]` | kāraka driver (standalone word, गोषु दुह्यमानासु गतः) |
| `ramA` | `[rama, strI_abs]` | kāraka driver + a `vibhaktis_list` paradigm |
| `jawA` | `[jawa, strI_abs]` | kāraka driver (जटाभिस्तापसः) |
| `niSA` | `[niSa, strI_abs]` | nothing but inertia — a `vibhaktis_list` paradigm, which has taken element lists all along |

Neither of the two REAL boundaries is a tagging gap — both are rules that must run before the
affix is chosen, and no driver change reaches them. Note in particular that **ekaśeṣa is not
a tooling block either**: 1.2.67 पुमान् स्त्रिया / 1.2.73 ग्राम्यपशु have to *identify* the
feminine member at −1, where a live member is still the masculine base — so `haMsI` and `ajA`
stay stored for the same reason the puṁvadbhāva family's stems do.
That is the honest end state of the migration: the **pūrva-hrasva family is fully live**, the
samāsānta-selection and puṁvadbhāva families are not, and the pre-formed stems that remain are
the ones those two families need.

---

## 4. Recommended order

0. ✅ **DONE** — delete `strI_pUrva` (§2), one stem + one test line.
1. ✅ **DONE** — §2's latent bugs, for the stems that keep a lexical form (nine stems; every
   one was a wrong nom sg, not just a missing marker). `haMsI` was fixed even though it is
   nominally bucket 1, because the step-A caveat means it is not going anywhere.
2. ✅ **DONE (was already done)** — step A: all four repointable paradigms were already
   `[base, strI_abs]`; deletion is blocked by the compound-member caveat and, for 4 of the
   12, by the base being a different lexeme.
3. ✅ **DONE** — step B: propagation-list gap, step C unblocked. See the result block above.
4. ✅ **Step C DONE for all five X2 pūrva rules** (6.3.43, 6.3.61, 6.3.62, 6.3.63, 6.3.65) —
   `?sup_luk` + the `?samAsaPurva`+luk propagation + `?puMvat` earned at the ṅī/āp merge +
   per-rule uttara tags. The live-derived pūrva works, and the driver now checks the
   main-scan trace so nothing lost its attribution.
5. ✅ **Step D DONE** — 6.3.61 un-scoped (via the general `?vihita_dIrGa` marker), `gOrI`
   and `ekA` deleted, three X2 cases live-derived. Bucket 2 bases are NOT worth adding, and
   §3 step D records the two boundaries (uttara position; the B1 puṁvadbhāva family) that
   hold the remaining bucket-1 stems in place.

## 5. Verification

```bash
cd sanskrit_parser/generator/test && PYTHONPATH=<repo root> /Users/karthik/venvs/sanskrit/bin/pytest -n 8 --dist worksteal
```

Baseline at `f524e44`: **8422 passed**. Step A should be surface-neutral — any change in a
vibhakti table means the live derivation and the stored form disagree, which is itself the
bug worth finding. Step C must additionally re-check the forms 6.3.61 damaged when
unscoped: केशाकेशि / मुष्टीमुष्टि / बाहूबाहवि (6.3.137), अग्नीवरुणौ (6.3.27), ऊरीकृतम् (avyaya),
सुकेशीभार्यः (ङीष्).

---

## 6. What steps 0–B did to step C's payoff (2026-08-05)

Step C exists to serve step D. Two of D's three items shrank, and the third got cheaper:

- **"Delete `?NI`/`?Ap` from bucket 1"** — down from 12 stems to **6**, and every one of
  those 6 still cannot be deleted while it is a compound member. C lifts that block only if
  the pūrva-member question above resolves favourably.
- **"Add bases for bucket 2"** — unchanged, and independent of C. It can be done any time.
- **"Un-scope 6.3.61"** — the real prize, and it is now **closer than the plan assumed**.
  Of the four forms the un-scoped rule damaged, one (सुकेशीभार्यः) was damaged *because*
  सुकेशी lacked `?NI`, which step 1 has now fixed — the `?!NI` gate is that much more
  trustworthy. Of the remaining three, ऊरीकृतम् is covered by the sūtra's **own** vārtika
  (इयङुवङ्भाविनाम्**अव्ययानां** च न → a `?!avyaya` guard, which the rule should have had
  anyway), and केशाकेशि (6.3.137) / अग्नीवरुणौ (6.3.27) are both cases where **another rule
  deliberately supplied the long vowel** — i.e. a marker set by those two rules and read as
  `?!<marker>` by 6.3.61, the same one-way lever used elsewhere.

  That is a self-contained piece of work that does **not** require the C relocation. Worth
  costing as its own phase before committing to C.
