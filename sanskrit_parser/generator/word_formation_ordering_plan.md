# Running word-formation before the sentence pre-passes — ordering plan

**Status: NOT STARTED.** Written 2026-08-05 against commit `189d679`. Every number below is
measured on that tree (a script over the 773 rules in `sutras_antaranga.yaml`, plus prakriyā
traces); inferences are marked as such.

**The design is ADVISORY TAGGING (§3), not a level move.** W computes which strī affix a member
*would* take and records the verdict as a tag; it does not substitute the affix, move a rule, or
reorder anything. The level-move version is kept as §2/§7's fallback because it is what the
analysis started from — and because त्रिलोकी shows why it fails.

## 1. The problem: the ladder is inverted

| bahiranga | contents |
|---|---|
| **−2** | kāraka pre-pass (112 rules) — *sentence level*, and it inserts the sups |
| **−1** | samāsa pre-pass (211 rules) — *compound level* |
| **0** | 1.4.3 यू स्त्र्याख्यौ नदी (22) |
| **1** | 30 |
| **2** | **ṭāp/ṅīp selection + 2.4.71 sup-luk** (69) — *word level* |
| **3** | 1 |
| default 9 | main scan (328) |

Word-level affixation runs **three levels after** the sentence- and compound-level pre-passes
that depend on it. A compound member written live as `[base, strI_abs]` is therefore still the
bare masculine base when every samāsa rule looks at it.

`pratipadika.py`'s pre-tagged feminines exist to paper over exactly this: `?NI`/`?Ap` on a
stored stem is a bahiranga-2 outcome smuggled into a bahiranga-−1 condition
(`ni_ap_derivation_plan.md` §1). That plan removed ten such stems by relocating the five X2
pūrva-hrasva rules *later* (to the main scan, where the ī exists). The ~26 stems it could not
remove are held by four blocks, all of which are the same inversion seen from different sides:

| block | rule family | symptom on a live member |
|---|---|---|
| **A** | samāsānta SELECTION — SK833/5.4.153 नद्यृतश्च, SK681/5.4.110 | **wrong form** `bahukumAriH` (no `?NI` at −1 → no कप् → 1.2.48 shortens) |
| **A′** | compound FORMATION naming the feminine — SK688/2.1.26 खट्वा क्षेपे (`lp: =KawvA`) | **no compound at all** |
| **A″** | ekaśeṣa identifying the feminine — SK933/1.2.67 पुमान् स्त्रिया, SK939/1.2.73 | rule cannot pick the member to elide |
| **B** | B1 puṁvadbhāva — SK831/6.3.34 ff., reading `?jAti`/`?kopaDa`/`?svAnga_I` | right form, **rule stops firing** (attribution lost) |

None of these can be fixed by relocating the rule *later*, the way the hrasva family was:
5.4.153 selects an affix the compound then declines with, and 2.1.26 **is** the compound
formation. The fix has to come from the other end.

---

## 2. The finding that makes a fix possible

**The strī block is not one block.** Of the 69 rules whose condition mentions `?strI_abs`:

| | count | where they sit now | examples |
|---|---|---|---|
| **compound-INDEPENDENT** | **46** | 38 @ 2, 6 @ 1, 2 @ main | SK454/4.1.4 ṭāp · 4.1.5 · SK/4.1.6 उगितश्च · 4.1.15 · SK478/4.1.20 · SK496/4.1.39 · 4.1.40 · SK498/4.1.41 · 4.1.63 · 4.1.73 |
| **compound-DEPENDENT** | **23** | 19 @ 2, 4 @ 1 | SK479/4.1.21 दिगोः · 4.1.22–24 · 4.1.25–29 · 4.1.12/13 · 4.1.54–58 · 4.1.8 · 4.1.33/34 · 4.1.64 · 4.1.4.1, 4.1.4.2 (ajādi prabalatva) · 5.4.131 |

The split is not arbitrary — it falls exactly along **whose femininity it is**:

- the **46** decide a *member's own* feminine affix (कुमारी as a word);
- the **23** decide the *compound's* feminine affix (बहुकुमारी, पञ्चखट्वी — anyapadārtha and
  dvigu femininity).

They act on **different objects**, so a member's affix can be settled before the compound
exists. There is no circular dependency to break — which is what makes the whole plan viable
rather than a rewrite.

**The 46/23 counts are an upper bound on independence, not the answer.** 7 of the "46" read
`llp` and are compound rules that identify the pūrva **by position rather than by tag** —
SK/4.1.35 (`=sa/=eka/=vIra`, सपत्नी), 4.1.36 (`=pUta`), 4.1.50/51 (`?karaNa`), 4.1.57,
4.1.60 (`?dik`), 4.1.70. The real split is nearer **39 / 30**, and phase W0 exists to settle
it exactly.

### 2a. But moving selection earlier is NOT sufficient on its own

Measured, from a live trace of बहुकुमारी:

```
[4.1.20] ['bahu','kumAra','','s'] -> ['bahu','kumAra','I','s']
```

Selection **substitutes the affix element**; it does not merge it. The merge into `kumArI` is
a saṁhitā operation in the main scan. So even with selection moved before −1, the member at
−1 is still `kumAra`, and `rp: ?NI` still fails.

What changes is the **neighbour**: the element beside the member is now `NIp`, which carries
`?NI`, instead of the undifferentiated `strI_abs` (tags `["strI_abs", "strI"]` only).

### 2b. The peek already exists — half of it

`_samasa_window_fixpoint` (`antaranga_prakriya.py:990`) builds

```python
ctx = (inputs[a - 1] if a - 1 >= 0 else None,
       inputs[b + 1] if b + 1 < len(inputs) else None)
```

and passes it as `context=` to `isTriggered` — the same llp/rrp channel 30+ rules use at −2
and the strī rules use at 1/2. **No bahiranga −1 rule uses it today.**

Because these are physical neighbours by index, for a live **uttara**
`[… bahu(a), kumAra(b), NIp(b+1), sup …]` the affix lands precisely on `rrp`. For a live
**pūrva** `[… Kawva(a), Ap(a+1), … , rUQa(b), sup(b+1)]` it sits **between** the operands and
is visible to neither.

> **early selection + the peek = sufficient. Neither alone is.**

**Superseded by §3.** That conclusion is sound but it describes the *level-move* design. The
advisory design below needs neither: it never touches the placeholder, so the affix keeps its
`?strI_abs` identity for the level-2 rules, and the −1 rules read a tag on the member rather
than peeking at a neighbour. The peek analysis is kept because it is what led here, and
because the between-slot accessor remains the fallback if advisory tagging proves too weak.

---

## 3. Design — ADVISORY tagging, not a level move

Revised 2026-08-05 after checking how the strī rules actually operate. **Nothing inserts a
strī pratyaya.** All 69 expect a composer-supplied `strI_abs` placeholder and either
substitute it (`orp: =NIp` / `=NIz` / `=Ap` / `=DAp`, 16 rules), block a competitor
(`overrides:` + `update: null`, falling through to 4.1.4's ṭāp, 6 rules), or reshape the stem
(`xform`, 5.4.131 ऊधस्→ऊधन्). `strI_abs` is an *input* — the declaration "a feminine is wanted
here".

That kills the naive "move the 46 earlier", because member-level and compound-level femininity
**share one placeholder slot** and are the same object:

- बहुकुमारीकः — the ī is the **uttara's own** (कुमारी is a word);
- **त्रिलोकी** — the ī is the **compound's** (SK479/4.1.21 दिगोः reads `lp: ?dvigu` on the
  *merged* stem त्रिलोक).

Run the 46 early and they consume the placeholder for त्रिलोक's member `loka` by 4.1.4 ṭāp →
लोका, and 4.1.21's ṅīp never gets its turn → ***त्रिलोका**. `vibhaktis_list.py:1903` asserts
त्रिलोकी, so **त्रिलोकी is the case that discriminates the two designs.**

### The design that works: advise, do not consume

**Phase W runs the compound-independent strī rules in a sandbox to decide which affix a member
WOULD take, writes that verdict as a tag on the member, and leaves the `strI_abs` element
untouched.** Nothing is substituted, nothing is reordered, and level 2 proceeds exactly as it
does today.

1. **Distinct tag names — `?NI_adv` / `?Ap_adv`, not `?NI` / `?Ap`.** *Measured, and this is
   what forces it:* no strī-window rule reads `?NI`/`?Ap` on its **lp**, so an advisory tag
   cannot feed back into affix selection — but **15 other rules do** read them on the left
   operand, and they are the declension family that must see the tag only on the *merged*
   stem: SK/6.1.68 हल्ङ्याब्भ्यो, 7.1.18, 7.1.54, 7.3.105/106/113/114/115/116, 7.4.15,
   SK656/1.2.48, and the relocated 6.3.43/61/63/64. Reusing the names would leak a **stale**
   verdict onto the merged stem in exactly the त्रिलोक case (advisory `?Ap`, actual ṅīp), where
   7.3.105/113 would then see a spurious `?Ap` on a nadī stem.
2. **The −1 consumers read both.** `5.4.153` becomes `[or, ?NI, ?NI_adv]`, and likewise
   5.4.110, 6.3.63, 2.1.26 (via content + `?Ap_adv`), 1.2.67/1.2.73. Pre-formed stems keep
   working unchanged — which is what lets the migration proceed stem-by-stem instead of in one
   jump.
3. **The 23 compound-dependent rules do not move**, and the placeholder is still live when
   they run, so त्रिलोकी survives untouched.
4. **`_insert_samasanta` must skip the member's strī affix.** *Measured:* it inserts at
   `ix + 1`, "just after the uttara (before its sup)". With a live member the element at
   `ix + 1` is the `strI_abs`, so कप् would land as कुमार+**क**+ī — wrong; it belongs to the
   compound stem बहुकुमारी, i.e. कुमार+ī+**क**. The fix is to advance past a following
   `?strI_abs` before inserting. (Today the pre-formed कुमारी *is* the member, so `ix+1` is
   already correct — which is why this has never bitten.)

### Does the order work for a PLAIN (non-samāsa) derivation?

Yes, and provably so with distinct tag names — **no rule reads `?NI_adv`/`?Ap_adv` except the
−1 consumers, and a non-samāsa derivation never reaches them.** Walking `[brAhmaRa, strI_abs,
su]`:

| step | state |
|---|---|
| W | `brAhmaRa` gains `?NI_adv`; the placeholder is untouched |
| −2 kāraka | sup already present / inserted **after** the affix → `stem \| strI \| sup` |
| −1 samāsa | skipped (no compound) |
| 0–2 | 4.1.15 substitutes `strI_abs` → `NIp`, exactly as today |
| main | merge → ब्राह्मणी carrying the affix's real `?NI`; the declension family fires on that |

The base never meets a sup while holding the advisory tag (the affix element is always between
them), so 6.1.68 and the 7.3.x family cannot see it early. The one thing to verify by test
rather than by argument is `?TAp_added` vs a pre-baked `?Ap`: 4.1.4's comment records that
SK/7.2.102 must still fire for a stem carrying a *pre-baked* `?Ap` (दवि → दव) but not after a
freshly added ṭāp — advisory tags must not disturb that distinction, which is a second reason
they need their own names.

### Does it work for a SAMĀSA derivation?

Yes, with fix (4). Walking बहु + `[kumAra, strI_abs]`:

| step | state |
|---|---|
| W | `kumAra` gains `?NI_adv` |
| −1 | 2.2.24 forms the bahuvrīhi; **5.4.153 now fires** on `[or ?NI ?NI_adv]` → `?samasanta_kap` |
| −1 post | `_insert_samasanta` skips the `strI_abs` and inserts कप् after it → `[bahu, kumAra, strI_abs, kap, sup]` |
| 2 | 4.1.20 substitutes `strI_abs` → `NIp` (कप् sits beyond it and does not interfere) |
| 1 (re-scan) | 1.2.48 arm 4 needs `rp: ?sup`; at the (कुमारी \| कप्) window rp is कप्, so it does **not** fire — the ī is preserved, which is 7.4.14 न कपि's effect, already folded in as the `?!ka_pratyaya` guard |
| main | कुमारी+कप् → कुमारीक, बहु+कुमारीक → **बहुकुमारीकः** |

The ordering race with 1.2.48 that the `insert:` route had to win **does not arise**: कप् is
already in the list before the affix is even chosen.

## 4. Phases

**W0 — the audit (do this first, it is cheap and it will move the numbers).** A checked-in
script that classifies every strī rule by compound-dependence. *The 46/23 split in §2 is
already known to be wrong*: **7 of the "46" read `llp`** — SK/4.1.35 (`=sa/=eka/=vIra`,
सपत्नी), 4.1.36 (`=pUta`, पूतक्रतु), 4.1.50/51 (`?karaNa`), 4.1.57, 4.1.60 (`?dik`), 4.1.70 —
i.e. they are compound rules that identify the pūrva **by position instead of by tag**. The
real split is nearer **39 / 30**, and only the audit will say exactly.

**W1 — `?NI_adv`/`?Ap_adv` and the sandbox.** Compute the verdict, write the tag, touch
nothing else. Surface-neutral by construction: no rule reads the new tags yet.

**W2 — `_insert_samasanta` skips the strī affix.** Independently testable against a live
`[kumAra, strI_abs]` uttara.

**W3 — teach the −1 consumers `[or ?NI ?NI_adv]`**: 5.4.153, 5.4.110, 6.3.63, 2.1.26,
1.2.67/1.2.73, and the B1 puṁvadbhāva family. Each conversion is provable by a single test —
the live twin of a case that already passes with the pre-formed stem.

**W4 — delete what that frees.** The census in `ni_ap_derivation_plan.md` §3 step D: the 17
uttara-position stems, `KawvA`, `haMsI`/`ajA`, and the five puṁvadbhāva pūrvas.

**W5 — taddhita (SK1072+) inherits the same mechanism.** A taddhita-derived stem feeding the
strī machine (विद्या + अण् + ङीप् = वैद्यी) is the same shape: advise on the derived stem,
leave the placeholder for the real substitution.

**The level move stays available as a fallback** if advisory tagging proves too weak — but it
must then solve त्रिलोकी, which advisory tagging solves for free.

## 5. Risks

1. **The advisory verdict can be WRONG for the compound** — and by design. In त्रिलोक the
   member advice is `?Ap_adv` while the compound actually takes ṅīp. That is tolerable only
   because the advisory tag is consumed exclusively by the −1 rules, which run before the
   compound-level choice is made. It is the same staleness today's pre-tagged `KawvA` carries;
   the distinct tag names keep it from reaching the declension family. **This is the property
   to watch in review** — the moment something outside the −1 pre-pass reads `?NI_adv`, the
   design has a leak.
2. **The sandbox has to be a real evaluation, not a re-implementation.** W must run the actual
   rule objects (priority, `overrides`, optional forks) against a `(member | strI_abs)` window,
   or it becomes a second, drifting copy of the ṭāp/ṅīp machine — the exact failure mode the
   pre-tagged stems are.
3. **Optional rules make the verdict multi-valued.** SK496/4.1.39 वा gives रोहिणी *or* रोहिता.
   The advisory phase then has two verdicts and no basis for choosing; the honest encoding is
   to set *both* `?NI_adv` and `?Ap_adv`, and let the −1 consumer decide whether an ambiguous
   verdict is enough (5.4.153 arguably should not fire on one). `rohiRI` is the test case, and
   it is already flagged in `ni_ap_derivation_plan.md` as fork-blocked.
4. **`?TAp_added` vs a pre-baked `?Ap`.** 4.1.4's own comment records that SK/7.2.102 must
   still fire for a stem carrying a pre-baked `?Ap` (दवि → दव) but not after a freshly added
   ṭāp. A third tag in that space needs its behaviour under 7.2.102/103 pinned by test.
5. **Scope of the sandbox.** Which elements get advised? "Every prātipadika followed by
   `?strI_abs`" is the obvious rule, but a taddhita chain (`[vidyA, aR_t, strI_abs]`) has the
   affix two elements away — W5's problem, and a reason to define the scope now rather than
   discover it later.

## 6. Verification

```bash
cd sanskrit_parser/generator/test && PYTHONPATH=<repo root> /Users/karthik/venvs/sanskrit/bin/pytest -n 8 --dist worksteal
```

Baseline at `189d679`: **8458 passed**. W0–W2 must be **surface-neutral** — W1 writes tags
nothing reads yet, and W2 only changes an insertion index that no current derivation exercises.
W3 changes which rules appear in the `fired` traces (live members should *gain* 5.4.153 /
2.1.26) and nothing else.

Two cases discriminate the whole design and should be asserted at every step:

- **त्रिलोकी** (`vibhaktis_list.py:1903`) — compound-level ṅīp over an a-stem member. Goes to
  *त्रिलोका the moment W consumes a placeholder it should not have.
- **बहुकुमारीकः** with a LIVE `[kumAra, strI_abs]` uttara — the target of the whole exercise.
  Its failure modes are distinct and diagnostic: *बहुकुमारिः = 5.4.153 never fired;
  *बहुकुमारकी = `_insert_samasanta` inserted कप् before the strī affix; *बहुकुमारिकः = कप्
  landed but 1.2.48 shortened anyway.

## 7. What this does not solve

- **`?NI`/`?Ap` on the ~9 stems held for non-ordering reasons** — homograph bases (`kuSA`,
  `karRI`, `naKI` derive a *different word*), the optional-rule fork (`rohiRI`, 4.1.39 वा),
  the ī that is not a strī-pratyaya (`lakzmI`, `tantrI`, `SrI`), and the unmodelled
  derivations (`kArIzaganDyA` ṣyaṅ, `vidyA`/`suparRA` taddhita bases). See
  `ni_ap_derivation_plan.md` §3 step D's census.
- **The `insert:` route for 5.4.153** (deciding कप् late and inserting it mid-scan) becomes
  unnecessary if W lands, but it stays the fallback if W2 proves too costly. Its open
  questions are recorded in the same section.
