# Kāraka-prakaraṇam Implementation Plan (SK 532–646)

**Status:** **COMPLETE** — rule phases **K0–K7 + Phase K-UI done** (2026-06-14). The
full kāraka-prakaraṇam SK 532–646 derives as `bahiranga: -1` tag rules on the
integrated engine (tagging pre-pass + sup insertion + 1.4.23–1.4.98 param carve-out +
the optional-fork). K0–K4 landed sequentially; **K5 (apādāna/pañcamī, SK586–605), K6
(ṣaṣṭhī, SK607–631) and K7 (adhikaraṇa/saptamī, SK632–646) were built in parallel
worktrees and merged into `claude/cranky-bhabha-1df4d6`**, resolving two cross-phase
collisions (the `biBeti` duplicate, and the dūra/antika `semantic_dUrAntika` four-way
fork split out as 2.3.36.1). 144 cases in test/karaka_list.py green. **Phase K-UI
(Vākya Composer, §4) is now implemented** — `/karaka` composer + `/karaka/gallery`
regression view + `POST /api/karaka` / `GET /api/karaka/cases` in
`generator/ui/app.py`, no engine changes. Architecture v2 (2026-06-10): integrated
into the existing engine after review — see §2 *Design evolution*.
**Scope:** 115 sutras — SK 532 (प्रातिपदिकार्थलिङ्गपरिमाणवचनमात्रे प्रथमा, 2.3.46) through
SK 646 (विभाषा कृञि, 1.4.98). The section ends right before SK 647 (समर्थः पदविधिः),
which opens the samāsa-prakaraṇam and is **out of scope** here.

**How to run this plan:** each phase below ends with a self-contained *Session prompt*.
Start a fresh worktree session (the usual parallel-session workflow; merge with
`/gen-merge`) and paste the phase prompt. Phase K0 must complete and merge first;
phases K1–K7 are then largely independent and can run in parallel worktrees.
Phase K-UI can run any time after K0.

---

## 1. Why this section is architecturally different

Everything implemented so far (SK 1–515 range) is **phonological/morphological**: the
engine takes a `(prātipadika, sup)` pair and derives the surface form through
char-window rules (`l`/`r`/`lc`/`rc` conditions in `sutras_antaranga.yaml`).

The kāraka-prakaraṇam answers a different question: *given a sentence (verb +
participants + intent), which vibhakti does each participant take?* Its rules
condition on:

- semantic primitives (īpsitatama, dhruva-apāya, sādhakatama, svatantra …)
- verb meaning-classes (gatyartha, rucyartha, krudha-druha-īrṣyā-asūyā-artha …)
- co-occurring particles/upapadas (saha, antarā, namaḥ, dūram, kṛtvaḥ-suffixes …)
- whether the kāraka is already expressed elsewhere (anabhihite, 2.3.1)

None of this is computable from a phonological window's *strings* — but all of it IS
expressible in the existing *tag* DSL, provided the engine gives the rules the right
view. The design: kāraka/vibhakti rules live in **`sutras_antaranga.yaml`** as
ordinary tag rules in a new priority class **`bahiranga: -1`** (extending the existing
bahiranga ladder below the saṁjñā class 0), conditioned on `lp:` (the noun) and `rp:`
(the sentence's dhātu), writing `kAraka_*`/`viBakti_*` tags via `update: olp:`. The engine gains a **tagging pre-pass** and a **sup-insertion step**
before the existing window scan, so a whole sentence derives in ONE prakriyā:
tag → insert sup → existing phonology, unchanged.

### Structure of the section (two interleaved rule families + two adhikāras)

| Family | Count | What they do | Engine analog |
|---|---|---|---|
| Adhikāra | 2 | SK534 कारके (1.4.23), SK536 अनभिहिते (2.3.1) | engine semantics (pre-pass scope; prayoga gate), not YAML rules |
| Kāraka-saṁjñā (1.4.x) | ~45 | assign `kAraka_*` tags to nouns | `bahiranga: -1` tag rules (new pre-pass class) |
| Vibhakti-vidhi (2.3.x) | ~68 | map saṁjñā + context → `viBakti_1..8` tags; many vibhāṣā | same; vibhāṣā via the engine's existing `optional:` branch forking |

Key Paninian mechanics and how each is realized:

1. **ā kaḍārād ekā saṁjñā (1.4.1–2):** one kāraka per noun; on conflict the **later**
   rule wins (vipratiṣedhe param). Realized two ways: (a) a *convention* — every
   kāraka rule sets `[+kAraka_x, +kAraka]` and conditions on `"?!kAraka"`, so a second
   saṁjñā can never attach in a later iteration (this addresses the existing
   `FIXME: disable sutras for AkaqArAdekA saMjYA` at antaranga_prakriya.py:823 for
   the kāraka rule class); (b) a *priority carve-out* — `sutra_priority`'s saṁjñā-zone branch
   (`_aps_num < 14000` → lower wins, antaranga_prakriya.py:371) is backwards for the
   kāraka adhikāra; for two competing rules both in 1.4.23–1.4.98, **higher**
   `_aps_num` must win (e.g. upasṛṣṭa krudh-target: 1.4.38 karma must beat 1.4.37
   sampradāna). 2.3.x rules sit at `_aps_num ≈ 23000`, already in the para-wins SPSP
   zone — correct as-is. Explicit `overrides:` stays available for apavādas that are
   not plain param.
2. **anabhihite (2.3.1):** prayoga tags on the verb (`kartari`/`karmaRi`/`BAve`),
   readable because the pre-pass sets `rp` = the sentence's dhātu. 2.3.2 karma-
   dvitīyā carries `rp: ?!karmaRi`; the abhihita kāraka falls through to 2.3.46
   prathamā. Full abhidhāna detection from kṛt/taddhita/samāsa is deferred (§6).
3. **Optionality (vibhāṣā/anyatarasyām):** reuse the engine's existing
   `optional: true` branch forking (tree-level, antaranga_prakriya.py:840). The
   not-applied branch falls through to the general rule on the next iteration
   (e.g. 2.3.22 optional tṛtīyā, else 2.3.2 dvitīyā) → alternative complete
   sentences as separate prakriyā outputs. Tests assert output *sets*.
4. **Defaults:** unexpressed kartṛ/karaṇa → tṛtīyā (2.3.18); non-kāraka relation
   (śeṣa) → ṣaṣṭhī (2.3.50); mere stem-meaning / abhihita → prathamā (2.3.46).

---

## 2. Architecture (v2 — integrated into the existing engine)

### Where things go

| File | Change |
|---|---|
| `generator/sutras_antaranga.yaml` | New kāraka-prakaraṇam section: all 1.4.x/2.3.x rules as `bahiranga: -1` tag rules in the existing DSL (`lp:`/`rp:`/`llp:`/`rrp:` conditions, `update: olp:` writes). **No new YAML file, no loader change** — `bahiranga` is already a first-class parsed attribute on every sutra. |
| `generator/antaranga_prakriya.py` | (1) kāraka tagging pre-pass before the pratyaya window search, running exactly the `bahiranga == -1` rules; (2) sup-insertion step after it; (3) param-wins carve-out in `sutra_priority` for 1.4.23–1.4.98; (4) the main window scan takes `bahiranga > -1` only (split predicate pinned: pre-pass `== -1`, main scan `> -1`). |
| `generator/dhatu.py` | prayoga tags (kartari/karmaRi/BAve) and meaning-class tags (gatyarTa, rucyarTa, …) on dhātus. Dhātus may carry `semantic_*` tags when kṛt pratyayas are in play (the kṛdanta noun inherits them). |
| `generator/avyaya.py` | particles per phase: saha/sAkam/sArDam/samam, antarA/antareNa, namaH-cluster, vinA/pfTak/nAnA, dUram/antikam, … |
| `generator/paninian_object.py` | whitelist the `semantic_*`/`kAraka_*`/`viBakti_*` families plus the bare guards `kAraka` and `has_viBakti` in `join_objects` tier-1 propagation (same mechanism as the recent ?karaNa/?dik additions) so kṛt/strī/taddhita-derived nouns keep them. |
| `generator/test/karaka_list.py`, `test_karaka.py` | new test data + driver (§3). |

### Engine flow (one prakriyā per sentence)

```
input: ordered PaninianObjects — nouns (semantic_* + vacana_* tags), the verb
       (a pre-formed pada object carrying prayoga + meaning-class tags, §6),
       particles, optional kṛt/taddhita/strī pratyaya elements
  │
  ├─ 0. kāraka pre-pass (NEW): for each prakṛti element, window = (element | dhātu);
  │     run only bahiranga: -1 rules, to fixpoint. 1.4.x rules write kAraka_*;
  │     2.3.x rules write viBakti_* (naturally sequenced: 2.3.x conditions need
  │     kAraka_* tags that only exist after 1.4.x fire). disabled_sutras
  │     bookkeeping mirrors the main loop. SKIPPED ENTIRELY when no element
  │     carries semantic_*/prayoga tags → zero impact on existing tests.
  │
  ├─ 1. sup insertion (NEW): l→r, for each element tagged viBakti_N, scroll right
  │     past kṛt/taddhita/strī pratyaya elements, insert sup[N][vacana].
  │     (tiṅ branch stubbed until tiṅanta derivation exists.)
  │
  └─ 2. existing window-scan loop, unchanged: each pada derives phonologically.
```

**Pre-pass env convention:** `lp` = the noun under consideration; `rp` = the
sentence's dhātu (NOT the physical neighbour) — this is what lets verb-conditioned
saṁjñā rules (≈40 of the 115: 1.4.33–41, 1.4.46–48, 1.4.52–53, 2.3.12, 2.3.51–61 …)
read `rp: ?rucyarTa` etc., and what makes anabhihite expressible. `llp`/`rrp` remain
the physical neighbours, for particle-yoga rules (2.3.19 saha, 2.3.4 antarā) —
input convention: a particle sits adjacent to the noun it governs.

### Tag vocabulary

| Family | Set by | Examples |
|---|---|---|
| `semantic_*` | input (sentence construction) | semantic_Ipsitatama, semantic_Druva_apAya, semantic_prIyamARa, semantic_svatantra, semantic_Seza, semantic_samboDana, semantic_apraDAna |
| prayoga | input, on the verb | kartari, karmaRi, BAve |
| verb class | dhatu.py lexicon | gatyarTa, budDyarTa, rucyarTa, SabdakarmA, akarmaka, … |
| `vacana_*` | input | vacana_1 / vacana_2 / vacana_3 |
| `kAraka_*` + guard `kAraka` | 1.4.x rules | kAraka_karma, kAraka_kartA, kAraka_karaRa, kAraka_sampradAna, kAraka_apAdAna, kAraka_aDikaraRa |
| `viBakti_*` + guard `has_viBakti` | 2.3.x rules | viBakti_1 … viBakti_7, viBakti_8 (sambodhana) |

**Conventions:**
- `semantic_*` tags are the *primitives in the sutra wording* (īpsitatama,
  dhruva-apāya, bhayahetu, prīyamāṇa …), **never kāraka names** — otherwise the
  1.4.x rules would be vacuous relabeling and the apavāda/verb-class structure
  untested.
- Every kAraka-assigning rule sets `[+kAraka_x, +kAraka]` and conditions on
  `"?!kAraka"`; every viBakti rule sets `[+viBakti_N, +has_viBakti]` and conditions
  on `"?!has_viBakti"` (structural ekā-saṁjñā; also prevents tag rules re-firing,
  since a tag update — unlike a string rewrite — does not destroy its own trigger).
  The viBakti guard is `has_viBakti`, NOT bare `viBakti`: every sup pratyaya already
  carries the `viBakti` tag (pratyaya.py:141), so a bare guard would be polluted the
  moment the sup merges into the pada. The kAraka guard stays bare — no existing
  object carries a `kAraka` tag, so there is no clash (asymmetry is deliberate).
- Flow-YAML gotcha (from the SK506–515 work): `?tag` inside `[and, …]` must be
  quoted.
- **`bahiranga: -1` is both the routing marker and the priority class.** It extends
  the existing ladder (0 = saṁjñā, 1 = left-substitution, 2 = pratyaya-substitution,
  9 = YAML default) downward: sentence-level tagging precedes everything, and
  lower-wins means a -1 rule would beat any phonological rule even in a mixed
  competition — the correct outcome, so the convention fails safe. Class -1 is
  RESERVED for pre-pass kāraka rules; never assign it merely as a priority boost.
  Within the pre-pass all rules share -1, so the bahiranga branch never decides
  among them — the 1.4.23–1.4.98 param carve-out does. (Terminology note: vākya
  operations are textbook *bahiranga*; the field is the engine's pragmatic priority
  ladder, and loop placement — not the score — is what sequences the passes.)

### Rule sketch

```yaml
# 535: कर्तुरीप्सिततमं कर्म (1.4.49)
- sutra: कर्तुरीप्सिततमं कर्म
  id: 1.4.49
  bahiranga: -1
  condition:
    lp: ["and", "?semantic_Ipsitatama", "?!kAraka"]
  update:
    olp: [+kAraka_karma, +kAraka]

# 571: रुच्यर्थानां प्रीयमाणः (1.4.33) — verb-conditioned: rp = the sentence's dhātu
- sutra: रुच्यर्थानां प्रीयमाणः
  id: 1.4.33
  bahiranga: -1
  condition:
    lp: ["and", "?semantic_prIyamARa", "?!kAraka"]
    rp: ?rucyarTa
  update:
    olp: [+kAraka_sampradAna, +kAraka]

# 537: कर्मणि द्वितीया (2.3.2) — anabhihite via the verb's prayoga tag
- sutra: कर्मणि द्वितीया
  id: 2.3.2
  bahiranga: -1
  condition:
    lp: ["and", "?kAraka_karma", "?!has_viBakti"]
    rp: ?!karmaRi
  update:
    olp: [+viBakti_2, +has_viBakti]

# 564: सहयुक्तेऽप्रधाने (2.3.19) — particle co-occurrence via physical neighbour peek
- sutra: सहयुक्तेऽप्रधाने
  id: 2.3.19
  bahiranga: -1
  condition:
    lp: ["and", "?semantic_apraDAna", "?!has_viBakti"]
    rrp: [=saha, =sAkam, =sArDam, =samam]
  update:
    olp: [+viBakti_3, +has_viBakti]
```

### Design evolution (v1 rejected)

v1 of this plan proposed a separate `sutras_karaka.yaml` + a standalone
`karaka_prakriya.py` frame evaluator with a new condition vocabulary. Review favored
full integration because: (a) once the pre-pass supplies the right env
(lp = noun, rp = dhātu), the existing DSL expresses every rule — no parallel DSL,
no `FrameSutra`; (b) one engine and one rule file mean priority, `overrides:`,
optional-forking, tracing, the UI eval-capture, and /gen-debug all work on kāraka
rules for free; (c) the whole sentence derives in a single prakriyā — the more
faithful Paninian picture, and the path that later absorbs tiṅanta and real
abhidhāna detection without restructuring. The cost is engine surgery in
`antaranga_prakriya.py` (pre-pass, insertion, priority carve-out, main-scan
exclusion) — mitigated by the skip-guard (the pre-pass no-ops unless semantic tags
are present, so the existing ~1693 tests never enter it) and the mandatory
full-suite-green gate on every phase.

Routing-marker evolution: an earlier v2 draft used `domain: kAraka` plus a
raw-domain stash in `process_yaml.py`; replaced by `bahiranga: -1` (user direction)
— no loader change (bahiranga is already parsed onto every sutra; verified that the
only consumers are `<` comparisons, so negative values are safe), it follows the
engine's existing bahiranga-class convention, and it avoids inventing a domain name
outside `GlobalDomains`' fixed key set.

---

## 3. Test infrastructure (new — required)

The 8×3 vibhakti-table infra (`vibhaktis_list.py` + `test_ajanta_*.py`) tests *forms
given a vibhakti*. It cannot test *vibhakti selection*. New infra:

### `karaka_list.py` case format

```python
karaka_tests = [
    {
        "label": "SK537-harim-bhajati",
        "sutras": ["1.4.49", "2.3.2"],        # must appear in the fired trace
        # ordered sentence; particles adjacent to the noun they govern
        "sentence": [
            {"stem": "hari", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "Bajati", "tags": ["kartari"]},   # pre-formed pada (§6)
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"],
             "forms": [["हरिम्"]]},
            {"forms": [["भजति"]]},
        ],
    },
]
```

### Three assertion levels in `test_karaka.py`

1. **saṁjñā level** — the noun carries exactly the expected `kAraka_*` tag after the
   pre-pass (tests pass-1 + ekā-saṁjñā + param carve-out).
2. **vibhakti level** — expected `viBakti_*` tag(s); vibhāṣā rules fork the prakriyā,
   so the expectation is a *set across output branches* (catches over/under-generation).
3. **surface level** — the final derived sentence words match, per branch. This runs
   the full pipeline (pre-pass → sup insertion → phonology) and reuses stems already
   covered by the vibhakti tables, so failures here indicate wiring bugs, not new
   phonology.

Also assert the **fired-sutra trace** contains the listed `sutras` — this is what
makes counterexamples meaningful (e.g. माषेष्वश्वं बध्नाति: the māṣa slot must *not*
get kAraka_karma). Negative cases use `"karaka": None` / absent sutra ids.

**Test data source:** every example sentence in the SK commentary for SK532–646
(हरिं भजति, ग्रामं गच्छन् तृणं स्पृशति, गां दोग्धि पयः, पयसा ओदनं भुङ्क्ते,
माणवकं पन्थानं पृच्छति …). Each phase lifts its cases directly from
`references/siddhantakaumudi.html` (anchors `id="SK<N>"`) with Vasu
(`references/vasu_english.txt`; dot-free `A0B0C` ids, each component zero-padded to two
digits — `2.3.46` → `20346`, `1.4.49` → `10449`) for cross-checking scope.
If Vasu and SK disagree, stop and ask.

### Wiring

`test_karaka.py` lives in `generator/test/`, runs under the existing
`PYTHONPATH=<root> pytest -n 6` invocation with no conftest changes expected. Target:
~3–6 cases per vibhakti rule, ~1–3 per saṁjñā rule → roughly 350–500 new test items at
completion. **Gate on every phase:** the pre-existing suite (~1693 items, ~37s) stays
green with no measurable slowdown (the pre-pass skip-guard is what protects this).

---

## 4. UI: Vākya Composer (new paradigm — recommended) — ✅ IMPLEMENTED

> **Done (2026-06-14).** Implemented in `generator/ui/app.py` (routes `/karaka`,
> `/karaka/gallery`, `POST /api/karaka`, `GET /api/karaka/cases`) + templates
> `ui/templates/karaka.html` and `karaka_gallery.html`. The composer drops the
> separate prayoga radio — verbs enter as pre-formed tiṅanta padas that already carry
> their prayoga tag (§6), so selecting `sevyate` is karmaṇi. Dropdown inventories
> (stems/verbs/particles/semantic primitives) are derived from `test/karaka_list.py`
> so they stay in sync with the rule set. The per-case status in the gallery mirrors
> `test_karaka.py` (saṁjñā + vibhakti + fired-trace). The cases endpoint is cached
> per-encoding (one engine run per case ≈ 2–3 min on first hit, instant after). No engine
> changes. Run: `PYTHONPATH=. python sanskrit_parser/generator/ui/app.py` → port 5001.
>
> **Update — directional yoga-words (post kāraka-review round, 157 cases):** every
> yoga-word now carries a user-chosen **governance direction** (pūrva = follows its
> noun / governs the preceding; para = precedes / governs the following). `_build_word`
> in `ui/app.py` is a 1:1 mirror of `test_karaka.py`: a karmapravacanīya particle (sense
> present) → `kp_pUrva/kp_para` (default pūrva); a sense-less yoga-word particle
> (saha/dakṣiṇataḥ/hetoḥ…) or a nominal yoga-word stem (anya/namas/svāmin/dik/prasita/
> utsuka…) → `yoga_pUrva/yoga_para` (only when a direction is given). The composer
> exposes the direction on **both** particle cards (none/pūrva/para) and noun cards
> ("yoga-word governs", default off); `toSpec` sends `dir` only when set.


The existing Flask UI (`generator/ui/app.py`, port 5001) is table-oriented: pick a stem,
see 8×3 declensions. Kāraka work needs a **sentence-oriented** view. Extend the same app
(no new server):

**Page `/karaka` — Vākya Composer**
- Pick a verb (dropdown from `dhatu.py` / pre-formed verb padas, meaning-class tags
  shown), prayoga radio (kartari/karmaṇi/bhāve), optional particles (from `avyaya.py`).
- Add participant words: stem dropdown (existing prātipadikas), vacana, and
  semantic-primitive checkboxes (īpsitatama, apāya, sādhakatama, prīyamāṇa …).
- The backend builds the tagged `PrakriyaVakya` and runs the engine once.
- Output per word: assigned kāraka saṁjñā → vibhakti(s) → derived surface form(s),
  with the **fired-sutra trace** (sutra text + SK number) — the same capture-eval
  mechanism `api_generate` already uses.
- Vibhāṣā branches render *all* alternative sentences side by side — this is the main
  debugging payoff over CLI output.

**Page `/karaka/gallery`** — render every `karaka_list.py` case as a readable sentence
with per-word vibhakti coloring and expected-vs-actual status. Doubles as a visual
regression dashboard and as review material when deciding scope questions.

API: `POST /api/karaka` (sentence spec in → per-word tags/vibhakti/forms + fired
sutras out), `GET /api/karaka/cases`. Implementation effort is modest because app.py
already has transliteration helpers, object resolution (`_resolve_token`), and
eval-capture.

---

## 5. Phases

> Counts are sutra counts from the SK→Aṣṭādhyāyī table in §7, which is the
> authoritative list per phase.

### Phase K0 — Engine pre-pass + core spine (gating phase)

Build the §2 machinery: kāraka pre-pass (window = (prakṛti | dhātu),
`bahiranga == -1` filter, fixpoint, skip-guard), sup-insertion step, param-wins
carve-out in `sutra_priority` (1.4.23–1.4.98), main-scan split (`> -1` only),
tag-propagation whitelist in
`paninian_object.py`, and the §3 test infra. Implement the two adhikāras as engine
semantics (SK534 = pre-pass scope; SK536 = the prayoga-tag gate) and the minimal
rule spine:

| SK | id | rule |
|---|---|---|
| 532 | 2.3.46 | prātipadikārtha-mātre prathamā (default 1st; also covers abhihita) |
| 533 | 2.3.47 | sambodhane ca (→ viBakti_8) |
| 535 | 1.4.49 | karma saṁjñā (īpsitatama) |
| 537 | 2.3.2 | karmaṇi dvitīyā (anabhihite via `rp: ?!karmaRi`) |
| 559 | 1.4.54 | svatantraḥ kartā |
| 560 | 1.4.42 | sādhakatamaṁ karaṇam |
| 561 | 2.3.18 | kartṛ-karaṇayos tṛtīyā |
| 606 | 2.3.50 | ṣaṣṭhī śeṣe (pulled forward as the non-kāraka fallback) |

Exit criteria: हरिं भजति (kartari) / हरिः सेव्यते + रामेण (karmaṇi: abhihita karma →
prathamā, kartṛ → tṛtīyā) / हे राम (sambodhana) / रामस्य पुत्रः (śeṣa) all pass at all
three assertion levels; ~25 test cases green; the pre-existing ~1693-item suite green
with no measurable slowdown.

**Session prompt:**
```
Read sanskrit_parser/generator/karaka_plan.md (§1–§3, Phase K0). Implement the
kāraka layer inside the existing engine. (1) antaranga_prakriya.py: add the kāraka
tagging pre-pass before the pratyaya window search — for each prakṛti element the
window is (element | sentence-dhātu), only bahiranga == -1 rules run, to
fixpoint, with disabled_sutras bookkeeping mirroring the main loop; skip the
pre-pass entirely when no element carries semantic_*/prayoga tags. Add the
sup-insertion step after it (viBakti_N + vacana_M → sup object, scrolling right
past kṛt/taddhita/strī pratyaya elements; tiṅ branch stubbed). Add the param-wins
carve-out in sutra_priority: both rules in 1.4.23–1.4.98 → higher _aps_num wins
(the saṁjñā-zone lower-wins branch at ~line 371 is wrong for the kāraka adhikāra).
The main window scan takes bahiranga > -1 rules only (split predicate: pre-pass
== -1, main scan > -1; no process_yaml change needed — bahiranga is already
parsed, and negative values are safe since the only consumers are < comparisons).
(2) paninian_object.py: whitelist the semantic_*/kAraka_*/viBakti_* families plus
the bare guards kAraka and has_viBakti in join_objects tier-1 propagation.
(3) sutras_antaranga.yaml:
new kāraka-prakaraṇam section with bahiranga: -1 rules for SK532,
533, 535, 537, 559, 560, 561, 606 per the §2 tag conventions (+kAraka/+has_viBakti
guard tags, "?!kAraka"/"?!has_viBakti" conditions — the viBakti guard is
has_viBakti because sup pratyayas already carry the bare viBakti tag; quoted ?tags
inside [and,…]; class -1 is reserved for kāraka pre-pass rules). SK534/536
are adhikāras realized by the engine. (4) dhatu.py: prayoga + meaning-class tags;
verbs enter as pre-formed pada objects (e.g. "Bajati" with tags) until tiṅanta
exists. (5) Build test/karaka_list.py + test/test_karaka.py per §3 with ~25 cases
from references/siddhantakaumudi.html anchors SK532–537/559–561/606 (हरिं भजति,
हरिः सेव्यते + रामेण, हे राम, रामस्य पुत्रः, plus negative cases). The pre-existing
generator suite (pytest -n 6 from generator/test, ~1693 items, ~37s) must stay
green with no measurable slowdown. Update generator_status.md.
```

### Phase K1 — Karma extensions (SK 538–545, 8 sutras)

1.4.50 anīpsita; 1.4.51 akathita (dvikarmaka: the duh-ādi 12 + nī-ādi 4 gaṇa from the
kārikā, plus the akarmaka deśa/kāla/bhāva/adhvan vārttika); 1.4.52–53 ṇyanta kartṛ →
karma (gati/buddhi/pratyavasāna/śabdakarma/akarmaka classes; hṛ-kṛ optional); 1.4.46–48
adhi-śīṅ/sthā/ās, abhiniviś, upa-anu-adhi-āṅ + vas locus → karma; 2.3.4
antarā-antareṇa-yukte dvitīyā. Needs: two karma nouns in one sentence (the per-object
`+kAraka` guard handles this naturally — each noun gets its own saṁjñā), a `Ryanta`
tag on the verb, verb gaṇa tags in dhatu.py, antarA/antareNa in avyaya.py. The ṇyanta
vārttika exceptions (nī-vah, ad-khād, bhakṣ ahiṁsā …) — implement the listed ones as
tags, defer the rest with a Skipped/Deferred row.

**Session prompt:**
```
Read sanskrit_parser/generator/karaka_plan.md (§2 conventions, Phase K1); the K0
kāraka pre-pass is already merged. Implement SK538–545 (1.4.50, 1.4.51 + dvikarmaka
gaṇas, 1.4.52, 1.4.53, 1.4.46, 1.4.47, 1.4.48, 2.3.4) as bahiranga: -1 kāraka rules in
sutras_antaranga.yaml. Add verb meaning-class tags to dhatu.py (gatyarTa,
budDyarTa, pratyavasAnArTa, SabdakarmA, akarmaka; duhādi 12, nī/hṛ/kṛṣ/vah 4;
Ryanta) and antarA/antareNa to avyaya.py. Add SK-commentary examples (गां दोग्धि
पयः, ग्रामं गच्छन् तृणं स्पृशति, शत्रूनगमयत्स्वर्गम् …) to test/karaka_list.py incl.
negative cases. Full suite green. Update generator_status.md; defer unlisted
ṇyanta vārttikas with a Skipped row.
```

### Phase K2 — Karmapravacanīya + dvitīyā (SK 546–558, 13 sutras)

1.4.83–87, 1.4.90–96 saṁjñā (anu/upa/prati/pari/abhi/su/ati/api/adhi as
karmapravacanīya in stated senses) + 2.3.8 (karmapravacanīya-yukte dvitīyā) + 2.3.5
(kālādhvanor atyanta-saṁyoge). The karmapravacanīya is a particle element adjacent to
its noun; its sense is an input tag on the particle (semantic_lakzaRa, semantic_hIna,
semantic_aDika, semantic_vIpsA …); the saṁjñā rules tag the particle, and 2.3.8 reads
it from the noun's window via `llp`/`rrp`. SK554 (adhi-parī anarthakau) is a
saṁjñā-denial — model as a blocking rule (`overrides:` + no update).

**Session prompt:**
```
Read sanskrit_parser/generator/karaka_plan.md (§2 conventions, Phase K2); the K0
kāraka pre-pass is already merged. Implement SK546–558 (1.4.83, 1.4.84, 1.4.85,
1.4.86, 1.4.87, 1.4.90, 1.4.91, 1.4.93, 1.4.94, 1.4.95, 1.4.96, 2.3.8, 2.3.5) as
bahiranga: -1 kāraka rules: karmapravacanīya saṁjñā on particle elements with input
sense tags, dvitīyā under karmapravacanīya-yoga via llp/rrp peeking, and
kāla/adhvan atyanta-saṁyoga dvitīyā. Add the particles to avyaya.py. Examples from
SK anchors (जपमनु प्रावर्षत्, मासं कल्याणी …) into test/karaka_list.py. Full suite
green. Update generator_status.md.
```

### Phase K3 — Tṛtīyā cluster (SK 562–568, 7 sutras)

1.4.43 divaḥ karma ca (optional karaṇa/karma for div's instrument); 2.3.6 apavarge
tṛtīyā; 2.3.19 sahayukte 'pradhāne; 2.3.20 yenāṅga-vikāraḥ; 2.3.21 itthambhūta-lakṣaṇe;
2.3.22 saṁjño 'nyatarasyāṁ karmaṇi; 2.3.23 hetau. Mostly straightforward
semantic-tag + particle rules; several vibhāṣā (exercise the optional-fork mechanism).

**Session prompt:**
```
Read sanskrit_parser/generator/karaka_plan.md (§2 conventions, Phase K3); the K0
kāraka pre-pass is already merged. Implement SK562–568 (1.4.43, 2.3.6, 2.3.19,
2.3.20, 2.3.21, 2.3.22, 2.3.23) as bahiranga: -1 kāraka rules: tṛtīyā extensions —
saha-yoga apradhāna (rrp/llp particle peek), aṅga-vikāra, itthambhūta-lakṣaṇa,
hetu, apavarga, div. Add saha/sAkam/sArDam/samam to avyaya.py. Examples: पुत्रेण
सहागतः, अक्ष्णा काणः, जटाभिस्तापसः, धनेन कुलम् … into test/karaka_list.py; assert
both branches of the optional rules. Full suite green. Update generator_status.md.
```

### Phase K4 — Sampradāna + caturthī (SK 569–585, 17 sutras)

Saṁjñā: 1.4.32–41, 1.4.44 (rucyartha prīyamāṇa, ślāgh-hnu-sthā-śap jñīpsyamāna, dhāreḥ
uttamarṇa, spṛheḥ īpsita, krudha-druha-īrṣyā-asūyā target, upasṛṣṭa krudha/druha →
karma, rādh-īkṣ, prati-āṅ-śru, anu-prati-gṝ, parikrayaṇa optional). Vidhi: 2.3.13
caturthī sampradāne, 2.3.14–15 kriyārthopapada/tumartha sthānin, 2.3.16
namaḥ-svasti-svāhā-svadhā-alaṁ-vaṣaṭ-yoga, 2.3.17 manyakarmaṇi anādara vibhāṣā, 2.3.12
gatyarthakarmaṇi dvitīyā-caturthyau. This phase is the param-carve-out stress test:
1.4.38 must beat 1.4.37 on upasṛṣṭa krudh/druh targets. Needs verb gaṇa tags and the
namaḥ-cluster avyayas.

**Session prompt:**
```
Read sanskrit_parser/generator/karaka_plan.md (§2 conventions, Phase K4); the K0
kāraka pre-pass is already merged. Implement SK569–585 (1.4.32–41, 1.4.44; 2.3.13,
2.3.14, 2.3.15, 2.3.16, 2.3.17, 2.3.12) as bahiranga: -1 kāraka rules: sampradāna saṁjñā
cluster and caturthī rules. Add the required verb meaning-class tags to dhatu.py
and namaH/svasti/svAhA/svaDA/alam/vazaw to avyaya.py. Examples: हरये रोचते भक्तिः,
देवदत्ताय शतं धारयति, हरये क्रुध्यति vs उपसृष्ट हरिं अभिक्रुध्यति (param test:
1.4.38 > 1.4.37), नमो देवेभ्यः, ग्रामं ग्रामाय वा गच्छति … into
test/karaka_list.py. Full suite green. Update generator_status.md; defer
2.3.14/15 if tumartha modeling needs kṛt support not yet present (Skipped row
with reason).
```

### Phase K5 — Apādāna + pañcamī (SK 586–605, 20 sutras)

Saṁjñā: 1.4.24–31 (dhruvam apāye, bhī-trā bhaya-hetu, parājeḥ asoḍha, vāraṇārtha
īpsita, antardhi adarśana, ākhyātṛ upayoge, jani-prakṛti, bhū-prabhava) + the
karmapravacanīya members 1.4.88 apa-pari varjane, 1.4.89 āṅ maryādā, 1.4.92 prati
pratinidhi/pratidāna. Vidhi: 2.3.28 apādāne pañcamī, 2.3.29 anya-ārāt-itara-ṛte-dik-
śabda-yoga, 2.3.10 pañcamy apāṅ-paribhiḥ, 2.3.11 pratinidhi-pratidāne, 2.3.24 akartari
ṛṇe, 2.3.25 vibhāṣā guṇe 'striyām, 2.3.32 pṛthak-vinā-nānā (tṛtīyā/pañcamī option),
2.3.33 karaṇe stoka-alpa-kṛcchra-katipaya, 2.3.35 dūrāntikārthebhyo dvitīyā ca.

**Session prompt:**
```
Read sanskrit_parser/generator/karaka_plan.md (§2 conventions, Phase K5); the K0
kāraka pre-pass is already merged. Implement SK586–605 (1.4.24–31, 1.4.88, 1.4.89,
1.4.92; 2.3.28, 2.3.29, 2.3.10, 2.3.11, 2.3.24, 2.3.25, 2.3.32, 2.3.33, 2.3.35)
as bahiranga: -1 kāraka rules: apādāna saṁjñā cluster and pañcamī rules, incl. the
apa/pari/āṅ/prati karmapravacanīya members (reuse the K2 particle-sense mechanism
if merged; otherwise build the minimal version locally). Add
vinA/pfTak/nAnA/fte/ArAt/dUram/antikam etc. to avyaya.py. Examples: ग्रामादायाति,
चोराद्बिभेति, अध्ययनात्पराजयते, उपाध्यायादधीते, हिमवतो गङ्गा प्रभवति, अन्यो रामात्
… into test/karaka_list.py. Full suite green. Update generator_status.md.
```

### Phase K6 — Ṣaṣṭhī (SK 606–631, 26 sutras; 606 done in K0)

2.3.50 śeṣe (K0); 2.3.26–27 hetu-prayoge + sarvanāmnas tṛtīyā ca; 2.3.30–31
ṣaṣṭhy-atasartha / enapā dvitīyā; 2.3.34 dūrāntikārthaiḥ ṣaṣṭhī vā; 2.3.51–59 verb-
specific ṣaṣṭhīs (jñaḥ karaṇe, adhīgartha-daya-īśām karmaṇi, kṛñaḥ pratiyatne,
rujārtha, nāthaḥ āśiṣi, jāsi-ni-prahaṇa-nāṭa-krātha-piṣ hiṁsāyām, vyavahṛ-paṇ, divaḥ
+ vibhāṣā upasarge); 2.3.61 preṣya-bruvoḥ haviṣaḥ; 2.3.64 kṛtvo'rtha kāla; **2.3.65–71
kṛd-yoga block** (kartṛ-karmaṇoḥ kṛti, ubhaya-prāpti, ktasya vartamāne,
adhikaraṇa-vāci, na lokāvyaya-niṣṭhā-khalartha-tṛn pratiṣedha, aka-in bhaviṣyat,
kṛtyānāṁ kartari vā). The kṛd-yoga rules condition on the *governing word being a
kṛdanta of a given type* — the governor is a physical neighbour, so read its tags
(?kta, ?tfn, ?Kalartha, ?kftya …) via `llp`/`rrp`; per §2 point 3, dhātus under kṛt
carry the semantic tags and the kṛdanta noun inherits them through the propagation
whitelist. Defer any member that would require real kṛt derivation machinery, with
Skipped rows. 2.3.72–73 tulyārtha, caturthī cāśiṣi.

**Session prompt:**
```
Read sanskrit_parser/generator/karaka_plan.md (§2 conventions, Phase K6); the K0
kāraka pre-pass is already merged. Implement SK607–631 (2.3.26, 2.3.27, 2.3.30,
2.3.31, 2.3.34, 2.3.51–59, 2.3.61, 2.3.64–73) as bahiranga: -1 kāraka rules: the ṣaṣṭhī
chapter. Model kṛd-yoga rules (2.3.65–71) by reading the governing kṛdanta's tags
(?kta, ?tfn, ?Kalartha, ?kftya, ?aka/?in) via llp/rrp; defer members that need
real kṛt derivation (Skipped rows with reason). Examples: सर्पिषो जानीते, मातुः
स्मरति, भजे शम्भोश्चरणयोः, हरेः कृतिः भक्तिः, ओदनस्य पाचकः … into
test/karaka_list.py. Full suite green. Update generator_status.md.
```

### Phase K7 — Adhikaraṇa + saptamī (SK 632–646, 15 sutras)

1.4.45 ādhāro 'dhikaraṇam; 2.3.36 saptamy adhikaraṇe ca (incl. dūra/antika); 2.3.37
sati-saptamī (bhāva-lakṣaṇa); 2.3.38 ṣaṣṭhī cānādare; 2.3.39 svāmī-īśvara-adhipati-
dāyāda-sākṣi-pratibhū-prasūta ṣaṣṭhī/saptamī; 2.3.40 āyukta-kuśala; 2.3.41 yataś ca
nirdhāraṇam; 2.3.42 pañcamī vibhakte; 2.3.43 sādhu-nipuṇa arcāyām; 2.3.44
prasita-utsuka; 2.3.45 nakṣatre ca lupi; 2.3.7 saptamī-pañcamyau kāraka-madhye; 1.4.97
adhir īśvare; 2.3.9 yasmād adhikam; 1.4.98 vibhāṣā kṛñi. Sati-saptamī/anādara need a
paired-element (absolute construction) input convention — the pair are adjacent
elements with semantic_BAvalakzaRa tags.

**Session prompt:**
```
Read sanskrit_parser/generator/karaka_plan.md (§2 conventions, Phase K7); the K0
kāraka pre-pass is already merged. Implement SK632–646 (1.4.45, 2.3.36, 2.3.37,
2.3.38, 2.3.39, 2.3.40, 2.3.41, 2.3.42, 2.3.43, 2.3.44, 2.3.45, 2.3.7, 1.4.97,
2.3.9, 1.4.98) as bahiranga: -1 kāraka rules: adhikaraṇa saṁjñā and the saptamī chapter,
incl. sati-saptamī/anādara via adjacent paired elements with semantic_BAvalakzaRa
tags, nirdhāraṇa ṣaṣṭhī/saptamī, and the adhi-īśvara karmapravacanīya tail.
Examples: कटे आस्ते, मोक्षे इच्छास्ति, गोषु कृष्णा बहुक्षीरा, रुदति प्रावाजीत् …
into test/karaka_list.py. Full suite green. Update generator_status.md. After
this phase, update karaka_plan.md status to complete.
```

### Phase K-UI — Vākya Composer (any time after K0, parallel-safe)

**Session prompt:**
```
Read sanskrit_parser/generator/karaka_plan.md (§4); the K0 kāraka pre-pass is
already merged. Extend sanskrit_parser/generator/ui/app.py with: (1) /karaka
Vākya Composer page — compose a sentence (verb with meaning-class display, prayoga,
particles, participant words with semantic-primitive checkboxes and vacana), build
the tagged PrakriyaVakya, run the engine, and show per-word kāraka saṁjñā →
vibhakti(s) → derived form(s) with the fired-sutra trace, rendering all vibhāṣā
branch alternatives side by side; (2) /karaka/gallery — render every
test/karaka_list.py case as a sentence with expected-vs-actual status. Add POST
/api/karaka and GET /api/karaka/cases. Follow the existing app.py patterns
(transliteration helpers, capture_eval). No engine changes.
```

---

## 6. Explicitly deferred (record as Skipped/Deferred rows when reached)

- **Verb surface derivation (tiṅanta)** — no lakāra/vikaraṇa machinery exists, so
  `gam + tiṅ` cannot derive गच्छति. Until it does, the verb enters the sentence as a
  **pre-formed pada object** (e.g. `PaninianObject("Bajati")` carrying the dhātu's
  meaning-class + prayoga tags), and the sup-insertion loop's tiṅ branch is a stub.
  The kāraka rules only ever read the verb's *tags*, so dropping in real tiṅanta
  derivation later changes nothing in the rule set.
- **Real abhidhāna detection** — the prayoga tag is given as input. Detecting
  expression by kṛt (लक्ष्म्या सेवितः), taddhita (शत्यः), samāsa (प्राप्तानन्दः), or
  nipāta awaits kṛdanta/taddhita integration; the tag is forward-compatible (it can
  later be *computed* instead of given).
- **Multi-verb / multi-clause sentences** — the pre-pass assumes one dhātu per
  sentence (`rp` pairing). Subordinate clauses, śatṛ/śānac phrases with their own
  kāraka fields, and yat-tat correlatives are out of scope.
- **Vārttika long tails** — e.g. the ṇyanta exception list under SK540, jalpati-
  prabhṛti upasaṅkhyāna: implement the ones SK itself exemplifies; defer the rest.
- **SK 558/642 luk/lup interactions** with taddhita elision — implement the vibhakti
  behavior on plain stems; the taddhita-lup machinery itself is deferred.
- **Accent and Vedic** options, as usual.

## 7. Full SK → Aṣṭādhyāyī map for the section

| Phase | SK | id | | Phase | SK | id |
|---|---|---|---|---|---|---|
| K0 | 532 | 2.3.46 | | K4 | 578 | 1.4.40 |
| K0 | 533 | 2.3.47 | | K4 | 579 | 1.4.41 |
| K0 | 534 | 1.4.23 | | K4 | 580 | 1.4.44 |
| K0 | 535 | 1.4.49 | | K4 | 581 | 2.3.14 |
| K0 | 536 | 2.3.1 | | K4 | 582 | 2.3.15 |
| K0 | 537 | 2.3.2 | | K4 | 583 | 2.3.16 |
| K1 | 538 | 1.4.50 | | K4 | 584 | 2.3.17 |
| K1 | 539 | 1.4.51 | | K4 | 585 | 2.3.12 |
| K1 | 540 | 1.4.52 | | K5 | 586 | 1.4.24 |
| K1 | 541 | 1.4.53 | | K5 | 587 | 2.3.28 |
| K1 | 542 | 1.4.46 | | K5 | 588 | 1.4.25 |
| K1 | 543 | 1.4.47 | | K5 | 589 | 1.4.26 |
| K1 | 544 | 1.4.48 | | K5 | 590 | 1.4.27 |
| K1 | 545 | 2.3.4 | | K5 | 591 | 1.4.28 |
| K2 | 546 | 1.4.83 | | K5 | 592 | 1.4.29 |
| K2 | 547 | 1.4.84 | | K5 | 593 | 1.4.30 |
| K2 | 548 | 2.3.8 | | K5 | 594 | 1.4.31 |
| K2 | 549 | 1.4.85 | | K5 | 595 | 2.3.29 |
| K2 | 550 | 1.4.86 | | K5 | 596 | 1.4.88 |
| K2 | 551 | 1.4.87 | | K5 | 597 | 1.4.89 |
| K2 | 552 | 1.4.90 | | K5 | 598 | 2.3.10 |
| K2 | 553 | 1.4.91 | | K5 | 599 | 1.4.92 |
| K2 | 554 | 1.4.93 | | K5 | 600 | 2.3.11 |
| K2 | 555 | 1.4.94 | | K5 | 601 | 2.3.24 |
| K2 | 556 | 1.4.95 | | K5 | 602 | 2.3.25 |
| K2 | 557 | 1.4.96 | | K5 | 603 | 2.3.32 |
| K2 | 558 | 2.3.5 | | K5 | 604 | 2.3.33 |
| K0 | 559 | 1.4.54 | | K5 | 605 | 2.3.35 |
| K0 | 560 | 1.4.42 | | K0 | 606 | 2.3.50 |
| K0 | 561 | 2.3.18 | | K6 | 607 | 2.3.26 |
| K3 | 562 | 1.4.43 | | K6 | 608 | 2.3.27 |
| K3 | 563 | 2.3.6 | | K6 | 609 | 2.3.30 |
| K3 | 564 | 2.3.19 | | K6 | 610 | 2.3.31 |
| K3 | 565 | 2.3.20 | | K6 | 611 | 2.3.34 |
| K3 | 566 | 2.3.21 | | K6 | 612 | 2.3.51 |
| K3 | 567 | 2.3.22 | | K6 | 613 | 2.3.52 |
| K3 | 568 | 2.3.23 | | K6 | 614 | 2.3.53 |
| K4 | 569 | 1.4.32 | | K6 | 615 | 2.3.54 |
| K4 | 570 | 2.3.13 | | K6 | 616 | 2.3.55 |
| K4 | 571 | 1.4.33 | | K6 | 617 | 2.3.56 |
| K4 | 572 | 1.4.34 | | K6 | 618 | 2.3.57 |
| K4 | 573 | 1.4.35 | | K6 | 619 | 2.3.58 |
| K4 | 574 | 1.4.36 | | K6 | 620 | 2.3.59 |
| K4 | 575 | 1.4.37 | | K6 | 621 | 2.3.61 |
| K4 | 576 | 1.4.38 | | K6 | 622 | 2.3.64 |
| K4 | 577 | 1.4.39 | | K6 | 623 | 2.3.65 |
| | | | | K6 | 624 | 2.3.66 |
| | | | | K6 | 625 | 2.3.67 |
| | | | | K6 | 626 | 2.3.68 |
| | | | | K6 | 627 | 2.3.69 |
| | | | | K6 | 628 | 2.3.70 |
| | | | | K6 | 629 | 2.3.71 |
| | | | | K6 | 630 | 2.3.72 |
| | | | | K6 | 631 | 2.3.73 |
| | | | | K7 | 632 | 1.4.45 |
| | | | | K7 | 633 | 2.3.36 |
| | | | | K7 | 634 | 2.3.37 |
| | | | | K7 | 635 | 2.3.38 |
| | | | | K7 | 636 | 2.3.39 |
| | | | | K7 | 637 | 2.3.40 |
| | | | | K7 | 638 | 2.3.41 |
| | | | | K7 | 639 | 2.3.42 |
| | | | | K7 | 640 | 2.3.43 |
| | | | | K7 | 641 | 2.3.44 |
| | | | | K7 | 642 | 2.3.45 |
| | | | | K7 | 643 | 2.3.7 |
| | | | | K7 | 644 | 1.4.97 |
| | | | | K7 | 645 | 2.3.9 |
| | | | | K7 | 646 | 1.4.98 |
