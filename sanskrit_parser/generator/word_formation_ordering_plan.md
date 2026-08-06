# Running word-formation before the sentence pre-passes — ordering plan

**Status: NOT STARTED.** Written 2026-08-05 against commit `189d679`. Every number below is
measured on that tree (a script over the 773 rules in `sutras_antaranga.yaml`, plus prakriyā
traces); inferences are marked as such.

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

They act on **different objects**, so they can sit at different levels. There is no circular
dependency to break — which is what makes the whole plan viable rather than a rewrite.

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

---

## 3. Design

1. **A word-formation phase (W) before the sentence pre-passes.** Run kṛt / taddhita / strī
   selection to fixpoint at a level below −2. *Inferred, not yet proven:* a single phase run
   to fixpoint is sounder than three ordered levels, because 4.1.22–24 read `?tadDita` **and**
   `?dvigu` together, and a taddhita-derived stem must exist before strī selection runs on it
   (विद्या + अण् + ङीप् = वैद्यी).
2. **The 23 compound-dependent strī rules stay where they are** (bahiranga 1/2). They need the
   samāsa saṁjñā, which is still assigned at −1.
3. **SK650/2.4.71 सुपो धातुप्रातिपदिकयोः stays at 2.** It lives at the same level as the strī
   block but is not part of it — it needs `?samAsaPurva` from −1. This is why the move is a
   per-rule reclassification, not a level shift.
4. **New context slot** on the −1 window: the element immediately after `lp` (the between-slot).
   Contained change — `ctx` tuple + the condition env.
5. **Convert the four blocked families** to read the affix through context instead of through a
   tag on the member.

| block | conversion |
|---|---|
| A (5.4.153, 5.4.110) | `rrp: ?NI` — uttara side, reachable **today** |
| A′ (2.1.26) | `lp: =Kawva` + between-slot `?Ap` |
| A″ (1.2.67, 1.2.73) | between-slot `?strI` — reachable **today**, even before W |
| B (6.3.34 ff.) | `?jAti`/`?kopaDa`/`?svAnga_I` already sit on the base; `?puMvat` is derived at the merge (`ni_ap_derivation_plan.md` step C) |

---

## 4. Phases

**W0 — the between-slot accessor.** Add the third context element and expose it in conditions.
Independently testable and independently useful: it unblocks **A″ (ekaśeṣa) with no reordering
at all**, since `?strI` is on `strI_abs` from the start. Ship this first and convert
1.2.67/1.2.73 as its proof.

**W1 — classify the 69 (audit only, no move).** Turn §2's script into a checked-in audit that
prints each strī rule's compound-dependence, so the classification is reproducible and the
next person can see why a rule is where it is. Expect surprises: the 46/23 split was computed
by tag-name matching, and a rule could depend on the compound *implicitly* (via a tag another
rule sets at −1) without naming a compound tag.

**W2 — move the 46.** The risky step. Do it in sub-batches by gaṇa/family, running the full
suite between batches; the ~8,000 vibhakti tests are both the safety net and the blast radius.

**W3 — convert A and A′, then delete what that frees.** With W0+W2 in place, take the census in
`ni_ap_derivation_plan.md` §3 step D and delete the uttara-position stems (17) plus `KawvA`.

**W4 — taddhita (SK1072+) enters the W phase by construction**, instead of arriving after the
pre-passes and generating a second generation of pre-tagged stems for the same reason `?NI`
was pre-tagged. Today taddhita conditions sit at 15 main-scan / 3 at −1 / 3 at 2.

---

## 5. Risks

1. **It is a 69-rule reclassification, not a level move** — the 46 are spread across bahiranga
   1, 2 and the main scan.
2. **Fork and priority interactions.** Several of the 46 are optional (SK496/4.1.39 वा) and
   interact by para-kāryam with the compound-dependent set (4.1.4.1's prabalatva reads
   `?samAsa`). Moving one set changes which fires first, and the engine re-scans lower levels
   when new tags appear — *measured*: 1.2.48 (level 1) fires **after** 4.1.20 (level 2).
3. **Sup insertion order.** The kāraka pre-pass inserts sups at −2. With W before −2 the list
   is `[stem, affix]` when the sup arrives, so the order comes out `stem | strī | sup` —
   *inferred from the existing live-derivation traces, which already produce that order.*
4. **1.4.3 nadī (bahiranga 0) assigns the saṁjñā post-merge** (*measured* — it fires on
   `kumArI` inside the nest), so it is unaffected by W. Do not "helpfully" move it.

## 6. Verification

```bash
cd sanskrit_parser/generator/test && PYTHONPATH=<repo root> /Users/karthik/venvs/sanskrit/bin/pytest -n 8 --dist worksteal
```

Baseline at `189d679`: **8458 passed**. W0 and W1 must be surface-neutral. W2 must be
surface-neutral too — any changed vibhakti table means a rule's level was load-bearing in a way
the audit missed, and that is the finding worth having. W3 changes only which rules appear in
the `fired` traces (they should *gain* 5.4.153 / 2.1.26 on live-derived members).

## 7. What this does not solve

- **`?NI`/`?Ap` on the ~9 stems held for non-ordering reasons** — homograph bases (`kuSA`,
  `karRI`, `naKI` derive a *different word*), the optional-rule fork (`rohiRI`, 4.1.39 वा),
  the ī that is not a strī-pratyaya (`lakzmI`, `tantrI`, `SrI`), and the unmodelled
  derivations (`kArIzaganDyA` ṣyaṅ, `vidyA`/`suparRA` taddhita bases). See
  `ni_ap_derivation_plan.md` §3 step D's census.
- **The `insert:` route for 5.4.153** (deciding कप् late and inserting it mid-scan) becomes
  unnecessary if W lands, but it stays the fallback if W2 proves too costly. Its open
  questions are recorded in the same section.
