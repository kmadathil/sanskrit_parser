# Running word-formation before the sentence pre-passes — ordering plan

**Status: W0, W1, W2 DONE; W3 done for A/A′/A″/B; W4 partial (14 stems gone, the rest gated on more W3);
W5b DONE, the rest of W5 deliberately open (it is an architecture question, see §4).** Written 2026-08-05 against commit `189d679`. Every number below is
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

**The strī block is not one block.** Of the 69 rules whose condition mentions `?strI_abs`
(**measured per ARM by `stri_rule_audit.py` — phase W0, DONE 2026-08-05**):

| bucket | count | where they sit | why |
|---|---|---|---|
| **DEPENDENT (tag)** | **21** | 17 @ 2, 4 @ 1 | names a compound saṁjñā — SK479/4.1.21 दिगोः · 4.1.22–24 · 4.1.25–29 · 4.1.12/13 · 4.1.54–58 · 4.1.8 · 4.1.33/34 · 4.1.64 · 4.1.4.1/4.1.4.2 · 5.4.131 |
| **DEPENDENT (position)** | **7** | 6 @ 2, 1 @ 1 | reads `llp` — SK/4.1.35 (सपत्नी) · 4.1.36 (पूतक्रतु) · 4.1.50/51 · 4.1.57 · 4.1.60 (`?dik`) · 4.1.70 |
| **DEPENDENT (derived)** | **0** | — | reads a tag the −1 pre-pass writes. **Zero — the load-bearing number** |
| **MIXED (some arms independent)** | **2** | 2 @ 2 | 4.1.4.1, 4.1.13 — some arms independent, some not; **advisable**, since a dependent arm cannot match in the sandbox |
| **INDEPENDENT** | **39** | 32 @ 2, 5 @ 1, 2 @ main | SK454/4.1.4 ṭāp · 4.1.5 · 4.1.6 उगितश्च · 4.1.15 · SK478/4.1.20 · SK496/4.1.39 · 4.1.40 · SK498/4.1.41 · 4.1.63 · 4.1.73 |

**41 advisable early / 28 compound-dependent** (per-ARM classification; a per-rule count gives 39/30 and is wrong — see W1). The derived bucket is the check no hand count
can do: it cross-references each advisable rule against the 46 tags the samāsa pre-pass
actually emits, so it does not rely on a tag *looking* like a compound tag. It is empty — no
advisable rule reads anything the pre-pass produces, which is precisely the licence the
advisory phase needs. `test/test_stri_rule_audit.py` guards that it stays empty.

The split is not arbitrary — it falls exactly along **whose femininity it is**:

- the **41** decide a *member's own* feminine affix (कुमारी as a word);
- the **28** decide the *compound's* feminine affix (बहुकुमारी, त्रिलोकी — anyapadārtha and
  dvigu femininity).

They act on **different objects**, so a member's affix can be settled before the compound
exists. There is no circular dependency to break — which is what makes the whole plan viable
rather than a rewrite.

**The first hand count (46/23) was wrong**, which is why W0 is a script and not a grep: it
missed the 7 positional rules entirely, because they name no compound tag at all. Any future
hand count will make the same mistake.

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

**W0 — the audit. DONE 2026-08-05.** `stri_rule_audit.py`
(`python -m sanskrit_parser.generator.stri_rule_audit [--verbose]`) classifies every strī rule
into §2's four buckets and additionally reports what each does to the placeholder (45
substitute / 9 xform / 8 tag-only / 7 block / **0 insert**) and the 15 rules reading
`?NI`/`?Ap` on their left operand. Result **39 / 30**, derived bucket **0**.
`test/test_stri_rule_audit.py` guards the invariant; it deliberately does not pin 39/30.

**W1 — the advisory pre-pass. DONE 2026-08-05.** `_stri_advisory_prepass` in
`antaranga_prakriya.py`, running before the kāraka pre-pass. For each `(stem | strI_abs)` pair
it runs the advisable rules in a SANDBOX (deep copies; the real elements are never touched) and
tags the stem `?NI_adv` / `?Ap_adv` / `?UN_adv`. Surface-neutral by construction — nothing
reads the tags yet.

* The advisable set is selected at runtime by the SAME predicate the W0 audit uses
  (`stri_rule_audit.is_advisable`, applied to each rule's retained `_cond_dict`), so the two
  cannot drift.
* The sandbox runs the real rule objects through the real `sutra_priority`, never a
  re-implementation — risk 2 below.
* An optional rule forks the sandbox and BOTH verdicts are recorded (रोहित → `?NI_adv` **and**
  `?Ap_adv`), which is risk 3's honest encoding.
* `test/test_stri_advisory.py` checks the property that matters: for nine stems covering every
  path — plain ṭāp, ajādi-prabalatva, gaurādi ṅīṣ, ugit ṅīp, ūṅ, and the 4.1.39 vibhāṣā — the
  advice **matches the affix the real derivation lands on**, read off its final vowel. Plus:
  no verdict without a placeholder, and the placeholder survives unconsumed.

**W1 corrected W0's granularity.** The first run advised अज `?NI_adv` while its derivation
gives अजा. Cause: SK454+/4.1.4.1 अजाद्यतष्टाप् has TWO arms — `lp: ?ajAdi` (the plain-word
ajādi-prabalatva) and `lp: [?samAsa, $$ajAdi_samasta]`. Classifying per RULE let arm 2's
`?samAsa` disqualify arm 1, the sandbox dropped the rule, and 4.1.63 जातेः ṅīṣ won unopposed.
The audit now classifies **per arm**, with a `MIXED (some arms independent)` bucket that counts
as advisable — the dependent arms cannot match in the sandbox anyway, since they need a
compound tag the bare member lacks or an `llp` the sandbox does not supply. Split is now
**41 advisable / 28 dependent** (2 mixed: 4.1.4.1, 4.1.13). *Caveat worth re-checking if it
ever changes: no strī arm reads a NEGATED `llp`, which is the one shape that could match
against an absent neighbour.*

**W2 — `_insert_samasanta` skips the member's strī affix. DONE 2026-08-05.** A samāsānta
belongs to the compound STEM, so with a live member it must land after that member's own affix:
कुमार+ī+**क** → बहुकुमारीकः, not कुमार+**क**+ī. **But the skip is conditional**, which the
first attempt got wrong and बहुदण्डिका caught: when the composer declared the COMPOUND feminine
(`?referent_strI`), the trailing placeholder is the anyapadārtha ṭāp and the samāsānta belongs
*inside* it — दण्डिन्+**क**+ā → बहुदण्डिका. Same slot, same object, opposite meanings; the
declared referent gender is what separates them.

**W3 — the −1 consumers read the advisory verdict. DONE for A, A′, A″ 2026-08-05.**

| block | rule | conversion | live case now passing |
|---|---|---|---|
| **A** | SK833/5.4.153 नद्यृतश्च | arm A → `[or, ?NI, ?NI_adv]` | **बहुकुमारीकः** from `[कुमार, strI_abs]` |
| **A′** | SK688/2.1.26 खट्वा क्षेपे | `=KawvA` → `[or, =KawvA, [and, =Kawva, ?Ap_adv]]` | **खट्वारूढः** from `[खट्व, strI_abs]` |
| **A″** | SK933/1.2.67, SK939/1.2.73 | `?strI` → `[or, ?strI, ?strI_adv]`, plus `?!strI_adv` on the opposite arm | **हंसौ**, **अजे** from `[हंस\|अज, strI_abs]` |

Three things W3 forced, each found by a failing case rather than by reading:

1. **`?strI_adv`** — a companion tag recording the verdict's GENDER. A″ and B need "this member
   will be feminine", not which affix does it.
2. **W1 must not advise a `?referent_strI` member.** दण्डिन् in बहुदण्डिका was advised `?NI_adv`
   (दण्डिनी is a word), and 5.4.153 then outranked SK890/5.4.152 इनः स्त्रियाम्. The placeholder
   there is the compound's, so there is no member verdict to give. Fixed at the source, in W1,
   rather than with a `?!referent_strI` guard on each consumer.
3. **The strī merge must drop `?Ba`.** With a live uttara, बहुकुमारीकः came out **\*बहुकुमास्कः**:
   1.4.18 यचि भम् had set bha for the strī affix, `join_objects` copied it onto the merged stem,
   and 6.4.148 यस्येति च then re-fired before कप् and ate the fresh ī — though कप् is
   consonant-initial and never licensed bha at all. Same hygiene 2.4.71 already applies to the
   luk'd sup (`olp: [-Ba]`); 1.4.18 re-derives the saṁjñā per window, so nothing is lost.
4. **1.2.67/1.2.73 now `overrides: 1.2.64`.** With a live feminine member the two ekaśeṣa
   members are the SAME STRING at −1 (हंस + हंस), so the general सरूपाणामेकशेषः grabbed the pair
   first and हंसौ came out right for the wrong reason. The specific rule, which also names the
   survivor, must win.

**Block B — the puṁvadbhāva family (6.3.34–41). DONE for 6.3.41 2026-08-05.** Two pieces:
`?puMvat_adv` (W1 derives bhāṣitapuṁska-ness — a feminine formed by ङी/आप् on a MASCULINE stem
has a masculine counterpart by construction, that stem), and the lexical property moved to
where it belongs: **`?jAti` now sits on `brAhmaRa`**, not only on the pre-formed ब्राह्मणी —
ब्राह्मण *is* the jāti. All seven `?puMvat` arms in the family read
`[or, ?puMvat, ?puMvat_adv]`. Live case: **ब्राह्मणीभार्यः** from `[ब्राह्मण, strI_abs]`, with
6.3.41 जातेश्च firing — the attribution the pre-tagged stem used to buy.

The other three prohibitions (6.3.37 पाचिका, 6.3.38 दत्ता, 6.3.40 सुकेशी) are not blocked by
the mechanism but by their STEMS: no base exists, and सुकेशी's would need 4.1.54, which is
itself compound-dependent (सुकेश is a bahuvrīhi). 6.3.34's own positive case needs no
conversion — it is the marker model, where the composer supplies the masculine form outright.

**W4 — delete what W3 freed. PARTIAL, and the limit is now measured 2026-08-05.**
`KawvA` (A′), `haMsI` and `ajA` (A″) are gone; with `yUka`/`duhyamAna`/`rama`/`jawa`/`niSa`
and the earlier five that is **fourteen** stored feminines removed (`likzA` is the newest).

Kept deliberately: `kumArI` and `brAhmaRI`, as the pre-formed twins of the live बहुकुमारीकः and
ब्राह्मणीभार्यः cases — they are what keeps proving the `[or ?NI ?NI_adv]` /
`[or ?puMvat ?puMvat_adv]` disjunctions still serve stored stems.

**Pushing further found a THIRD limit, and it is the real one.** Probing every candidate base
splits them cleanly:

* **ā-stems derive perfectly** — `[सेन|गङ्ग|प्रज|मेध|जाय|नासिक|वडव|लिक्ष|माल, strI_abs]` all give
  their feminine by 4.1.4 ṭāp. §2's "the base needs no independent attestation" is settled.
* **ī-stems do not**, from a plain a-stem base: `paYcamI` `rAkzasI` `sTAlI` `BaginI` `nAqI` come
  out *पञ्चमा, *राक्षसा, *स्थाला, *भगिना, *नाडा — for an ī-stem the base's CLASS is the whole
  question, as `revat` needed its ugit. `kalyARI` forks on an optional rule.

But a derivable stem is not a convertible one. Converting the ā-stems anyway, and reading each
failure, separates three cases — and only the first is a missing W3 conversion:

| case | what happens live | verdict |
|---|---|---|
| यूकालिक्षम् (2.4.8 + 2.4.17) | ṭāp re-feminised a compound the pre-pass had locked NEUTER → *यूकालिक्षा | **FIXED** — `join_objects`' strī block now honours `?samasa_liNga_locked`. `likzA` deleted |
| अश्ववडवौ (2.4.27 पूर्ववत्) | *अश्ववडवे | **BLOCKED, third mechanism.** The rule's job is `orp: [-Ap, -strI]` — it CANCELS the member's ṭāp. A live member has not applied it yet, and locking the gender does not help: 7.1.18 औङ आपः reads `?Ap`, not the gender. Affix *suppression* is not something the advisory design has |
| हरिषेणः (8.3.99 ṣatva) | 8.3.99 never fires | **BLOCKED, and not worth converting**: the rule reads `=senA` at the member junction, so it needs the same treatment 2.1.26 got — but the compound is masculine, so सेना's trailing placeholder would then feminise it, i.e. the अश्ववडवौ problem again |

**The general limit, stated properly:** a live member works when its own affix and the
compound's are *separable* — because the member is non-final (a pūrva), or because a samāsānta
sits between them (बहुकुमारीकः), or because the compound's gender is locked and the member's
ṭāp merely has to not override it (यूकालिक्षम्). It does NOT work when the compound needs the
member's affix **cancelled** or needs to read its **surface** before it exists. That is a
sharper statement than "uttara position" and it is what W5 should design against.

**W5 — taddhita. W5b DONE 2026-08-05; the rest deliberately NOT done.**

The plan used to say "taddhita inherits the same mechanism". **Measuring it says otherwise, and
the difference matters:**

* Taddhita affixes are composer-supplied **and already resolved** — 39 affix objects in
  `pratyaya.py`, named individually in the input (`[vidyA, aR_t, strI_abs]`), and **no rule
  inserts one** (`update:` never mentions `tadDita` in any of the 773 rules). Unlike
  `strI_abs`, which is an *abstract* placeholder resolved by 41 selection rules, a taddhita
  arrives already chosen. **There is no selection step today, so there is nothing to advise.**
* The exception is the model to copy if selection is ever wanted: **samāsānta taddhitas already
  work marker-first** — a −1 rule sets `?samasanta_*` and the ENGINE inserts the affix
  (`_insert_samasanta`). "Decide by rule, insert structurally" sidesteps the
  placeholder-ownership problem that cost W2 and W3 most of their effort.
* 21 rules read `?tadDita` in a condition; **3 sit at −1** (5.4.92, 6.3.87 सतीर्थ्ये,
  6.3.88 विभाषोदरे), all on `rp`. They work because the affix is *physically present but
  unresolved* at −1 — which is how 6.3.87/88's यादौ प्रत्यये विवक्षिते is modelled, and a third
  solution style already in the tree.

**Whether SK1072+ models taddhita SELECTION is an open architecture question, not a coding
task**, and it decides whether any of this is needed. It is deliberately left open here.

### W5b — the chain gap (the part that WAS worth doing)

W1 scanned for "a prātipadika followed by `strI_abs`". In a chain the element before the
placeholder is the AFFIX, so `[vidyA, aR_t, strI_abs]` got **no verdict at all** (measured).
The scan now admits a `?tadDita` element there too; the advisable rules read the affix's own
class tags (`?NIp_taddhita` on aṇ/añ/matup/dvayasac/…), which is how SK470/4.1.15 already
decides these forms.

`test/test_stri_advisory_taddhita.py` sweeps **every** paradigm in `vibhaktis_list` shaped
`[…, <taddhita>, strI_abs]` — 32 today, found by walking the dict rather than by a hand-picked
list — and asserts the verdict is **right or absent**. Result: **17 advised correctly, 15
silent, 0 wrong.**

The 15 silences are the interesting half, and both groups should be silent:

* **dvigu chains** (द्विबिस्ता, द्विकाण्डी, द्व्याढकी, पञ्चाश्वी …) — their feminine is the
  COMPOUND's, decided by 4.1.21–24, which are compound-dependent and excluded from the
  advisory set. **This is the त्रिलोकी hazard one level deeper, and it does not materialise:
  the sandbox declines rather than guesses.**
* **affixes not yet in final shape** — ढक् becomes एय by 7.1.2 (सुपर्णेयी), so nothing matches
  yet.

Silence is safe because nothing reads an absent verdict; a wrong verdict would not be, which
is why the sweep asserts that property rather than a fixed expected list.

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

---

## 8. Final stem status — derived vs pre-formed, and why (2026-08-05)

The scoreboard for `ni_ap_derivation_plan.md` + all W phases. The population reconciles like
this: **38** stems carried a strī-affix tag when the migration started, **+9** gained one in
step 1 (they were feminines all along, just untagged — the missing tag was a wrong nom sg),
**−14** deleted, = **33 today**. `atistri` is in that count but is not a feminine derivation at
all: it is the compound अतिस्त्रि, carrying `?strI_p` for 6.4.79's iyaṅ.

### DERIVED — the stem is gone, `[base, strI_abs]` is the only form (14)

| stem | base | affix | what unblocked it |
|---|---|---|---|
| `gOrI` | `gaura` | ङीष् 4.1.41 गौरादि | base already existed |
| `ekA` | `eka` | ṭāp 4.1.4 | base already existed |
| `haMsI` | `haMsa` | ṅīp | W3 A″ — 1.2.67 reads `?strI_adv` |
| `ajA` | `aja` | ṭāp (ajādi) | W3 A″ — 1.2.73 reads `?strI_adv` |
| `KawvA` | `Kawva` **(new)** | ṭāp 4.1.4 | W3 A′ — 2.1.26 reads `?Ap_adv` beside its `=KawvA` |
| `likzA` | `likza` **(new)** | ṭāp 4.1.4 | W3 — the strī merge honours `?samasa_liNga_locked` |
| `izwakA` | `izwaka` **(new)** | ṭāp 4.1.4 | pūrva-position; nothing blocked it |
| `izIkA` | `izIka` **(new)** | ṭāp 4.1.4 | pūrva-position |
| `revatI` | `revat` **(new, ugit)** | ङीप् 4.1.6 उगितश्च | pūrva-position. NOT an a-stem base — `revata` gives *रेवता |
| `yUkA` | `yUka` **(new)** | ṭāp 4.1.4 | dvandva driver hook |
| `duhyamAnA` | `duhyamAna` **(new)** | ṭāp 4.1.4 | kāraka driver hook |
| `ramA` | `rama` **(new)** | ṭāp 4.1.4 | kāraka driver hook |
| `jawA` | `jawa` **(new)** | ṭāp 4.1.4 | kāraka driver hook |
| `niSA` | `niSa` **(new)** | ṭāp 4.1.4 | nothing — a vibhakti paradigm, which has taken element lists all along |

Also deleted: **`strI_pUrva`**, a tag-stripped clone of `strI` that guarded nothing.

### PRE-FORMED — and the reason, one per stem (33)

**Kept ON PURPOSE as controls (2).** Their live twins pass beside them; deleting them would
stop proving that the disjunctions still serve stored stems.

| `brAhmaRI` | live twin: ब्राह्मणिगोत्रम् (6.3.43), ब्राह्मणीभार्यः (6.3.41) |
| `kumArI` | live twin: बहुकुमारीकः (5.4.153) |
|---|---|

**Lexical — the ī is not a ṅī on a base (4).** Absence or presence of the tag is correct here;
see `ni_ap_derivation_plan.md` §2.

`nadI` · `strI` (ī IS ङीष्, hence 1.4.4's अस्त्री) · `pfTivI` (ङीष् by the vārtika
पृथिव्यां ङीष्, not modelled) · `kArIzaganDyA` (ī is ष्यङ् + saṁprasāraṇa, 6.1.13)

**Base is a HOMOGRAPH — `[base, strI_abs]` derives a DIFFERENT word (3).**

`kuSA` (कुश is ?jAnapadAdi → *कुशी) · `karRI` (→ *कर्णा) · `naKI` (→ *नखा)

**ī-stem whose base CLASS is not modelled — a plain a-stem base gives ṭāp (6).**

`paYcamI` *पञ्चमा · `rAkzasI` *राक्षसा · `sTAlI` *स्थाला · `BaginI` *भगिना · `nAqI` *नाडा ·
`dAsI` (surface says ङीष्, but WHICH sūtra — गौरादि? — is still unchecked)

**Optional-rule fork — the verdict is genuinely two-valued (2).**

`rohiRI` (4.1.39 वा → रोहिणी/रोहिता) · `kalyARI` (→ कल्याणा/कल्याणी)

**UTTARA position, consumer rule not yet converted (7).** These are the W3 backlog: the base
derives fine, but the rule that reads the member at −1 still needs its own `?…_adv` arm, the
way 5.4.153 got one.

`senA` (8.3.99 ṣatva reads `=senA`) · `gaNgA` · `nAsikA` · `prajA` · `meDA` (5.4.122 असिच्) ·
`jAyA` (5.4.134 निङ्) · `mAlA` (pūrva use convertible; the बहुमालाकः uttara use pins it)

**Affix CANCELLATION needed — a mechanism the design does not have (1).**

`vaqavA` — 2.4.27 पूर्ववत् must *cancel* the ṭāp (`orp: [-Ap, -strI]`). Locking the gender is
not enough: 7.1.18 औङ आपः reads `?Ap`, so a live member still gives *अश्ववडवे.

**puṁvadbhāva prohibition with no base stem (3).**

`dattA` (6.3.38) · `pAcikA` (6.3.37) · `sukeSI` (6.3.40 — and its base would need 4.1.54,
itself compound-dependent, since सुकेश is a bahuvrīhi)

**kṛt / nipātana formation — not base + ङी at all (2).**

`pravARI` (प्र+वे+ल्युट्, cf. 5.4.160 निष्प्रवाणिः) · `pramARI`

**TADDHITA base — converting them means a double chain (2).**

`vidyA` (`[vidyA, aR_t, strI_abs]` → वैद्यी) · `suparRA` (`[suparRA, Qhak, strI_abs]`). A live
version is `[vidya, strI_abs, aR_t, strI_abs]` — two placeholders in one chain, untested.

**Not a feminine derivation (1).** `atistri` — the compound अतिस्त्रि; `?strI_p` is the
word-identity tag 6.4.79 iyaṅ and 1.4.4 read.

### What the table says about where to go next

The only group whose blocker is *bookkeeping rather than grammar* is the **7 uttara-position
stems**. Each needs one rule taught one `?…_adv` arm — the W3 recipe, already applied five
times. Everything else is blocked by a real property of the word (homograph, lexical ī,
optional rule) or by a missing mechanism (affix cancellation, surface-before-it-exists).
