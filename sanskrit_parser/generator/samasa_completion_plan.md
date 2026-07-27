# Samāsa completion: Dvandva, Ekaśeṣa, Sarvasamāsānta, Aluk (SK 188, 901–984)

## Context

The generator has completed **avyayībhāva** (SK 647–683), **tatpuruṣa** (SK 684–828)
and **bahuvrīhi** (SK 829–900) on the `generator` branch, all built on the reusable
**samāsa pre-pass** (`AntarangaPrakriya._samasa_prepass`, `antaranga_prakriya.py:563`,
all rules keyed `bahiranga: -1`). This plan takes the samāsa section to its end, over
**four consecutive prakaraṇas**:

| Prakaraṇa | SK range | Sūtras |
|---|---|---|
| द्वन्द्वसमासप्रकरणम् | SK 901–930 | 30 |
| एकशेषप्रकरणम् | SK 931–939 (+ its base rule SK 188 / 1.2.64) | 10 |
| सर्वसमासान्तप्रकरणम् | SK 940–957 | 18 |
| अलुक्समासप्रकरणम् | SK 958–984 | 27 |

(सर्वसमासशेषप्रकरणम्, between ekaśeṣa and sarvasamāsānta, contains **no sūtras** — it is a
one-line heading in SK. समासाश्रयविधिप्रकरणम्, SK 985–1071, is **out of scope**.)

They belong in one plan because they are not independent:
- SK939's own note — *"इह सर्वत्रैकशेषे कृतेऽनेकसुबन्ताभावाद् द्वन्द्वो न"* — makes ekaśeṣa a
  competitor of dvandva for the same window; they must be modelled against each other.
- **5.4.77**'s 25-item nipātana list (sarvasamāsānta) is largely **dvandvas**
  (स्त्रीपुंसौ, धेन्वनडुहौ, ऋक्सामे, वाङ्मनसे, अक्षिभ्रुवम्, दारगावम्, ऋग्यजुषम्) — it needs the D
  phases to exist first.
- **5.4.69–72** are prohibitions on samāsāntas *in general*, so they regress-test the
  already-landed 5.4.86–112 set; they can only be written once, at the end.
- **6.3.1 अलुगुत्तरपदे**'s adhikāra runs *प्राग् आनङः* — it terminates exactly at
  **6.3.25 आनङ्**, the dvandva rule in phase D3. The two share one region of 6.3.

**Standing deferrals this plan clears** (each already recorded with its blocker):
`generator_status.md:774` 6.3.2 aluk ("needs an aluk carve-out on 2.4.71 for the
stokādi pūrva"); `:778` 2.4.30 अपथं नपुंसकम् ("needs the pathin अच् samāsānta 5.4.74")
and 2.4.31 अर्धर्चाः पुंसि ("needs the अर्धर्चादि stems" — 5.4.74 supplies अर्धर्चः);
`:770` 2.2.30 उपसर्जनं पूर्वम्; plus the bahuvrīhi 2.2.27 / 5.4.127 / 2.2.35–37 group.

**Decisions taken (user, this session):** implement the physical pūrva-nipāta reorder
rather than defer it again; build **sequentially on `generator`**; add a closing phase
spending the new mechanisms on the standing deferrals; and fold in the sarvasamāsānta
and aluk prakaraṇas (this rewrite).

**Outcome:** धवखदिरौ, होतापोतृनेष्टोद्गातारः, हरिहरौ (from reversed input), पाणिपादम्,
वाक्त्वचम्, मातापितरौ, अग्नीषोमौ; रामौ / रामाः, हंसौ, भ्रातरौ, पितरौ, तौ; अर्धर्चः, गवाक्षः,
ब्रह्मवर्चसम्, द्वीपम्, सुराजा, अपथम्/अपन्थाः; स्तोकान्मुक्तः, ओजसाकृतम्, आत्मनेपदम्,
परस्मैपदम्, युधिष्ठिरः, स्तम्बेरमः, चौरस्यकुलम्, मातृष्वसा/मातुःष्वसा.

---

## 0. Numbering convention (MANDATORY — applies to every phase)

Per the dual-sutra-numbering convention, **every sūtra reference carries BOTH its SK
number and its Ashtadhyayi id, SK-first** (e.g. `SK901 / 2.2.29`), in all four places:
this doc; the `# <N>:` block comment of every rule in `sutras_antaranga.yaml` (the
`id:` field stays the bare Ashtadhyayi id); every test-case `label` in
`test/samasa_list.py` (e.g. `"D0-DavaKadirO-SK901-2.2.29"`); and the
`generator_status.md` rows. The `"fired"` lists hold Ashtadhyayi ids (that is what
`karaka_log` records) — the SK number lives in the label.

---

## 1. The four new mechanisms

Everything else in this plan reuses machinery that already exists.

**(M1) Derived vacana** *(dvandva, ekaśeṣa)* — the itaretara dvandva's number is the
*sum* of its members' (राम + कृष्ण → द्विवचन रामकृष्णौ; three members → बहुवचन); every
prakaraṇa so far took vacana straight from the composer. The lever already exists:
`?swap_viBakti` + **`_swap_sups`** (`antaranga_prakriya.py:699`) replaces a member's
already-inserted sup with the one for its current `viBakti_N`/`vacana_M` tags, so a
rule sets `orp: [-vacana_1, +vacana_2, +swap_viBakti]` and `su` becomes `au`.
Attribute it to **1.4.22 द्व्येकयोर्द्विवचनैकवचने + 1.4.21 बहुषु बहुवचनम्** (neither is
implemented — vacana has always been composer-supplied); implement them **scoped to the
dvandva/ekaśeṣa windows**, and say so in the YAML comment. n-ary falls out free:
`_samasa_prepass_branch` already walks adjacent pairs (`zip(members, members[1:])`,
line 616), so (1,1)→2 then (2,1)→3 gives होतापोतृनेष्टोद्गातारः.

**(M2) Physical pūrva-nipāta — the 2.2.30 deferral, finally paid** *(dvandva, phase X)*
— SK902–905 / 2.2.31–34 exist *only* to decide which member comes first, so tagging
alone would leave them surface-invisible. Design, mirroring the `_insert_samasanta`
split (rule decides, Python performs):
- Mark the ordering rules in YAML with a new flag (`purvanipata: true`, alongside
  `bahiranga: -1`); `_split_sutras` (`antaranga_prakriya.py:191`) grows a
  `_purvanipata_sutras` bucket carved out of `_samasa_sutras`.
- `_samasa_prepass_branch` becomes **two sweeps**: *sweep 1* runs only the ordering
  rules over the member windows and tags the winner `?pUrvanipAta`; then
  **`_commit_purvanipata`** physically moves that member (with its sup) ahead of its
  window-mate via `PrakriyaVakya.delete_at`/`insert_at` (`prakriya.py:64,69`) and
  recomputes the member index list; then *sweep 2* is the existing
  `_samasa_window_fixpoint` over the now-correctly-ordered windows.
- Two disjoint rule sets with the reorder strictly between them means no rule fires
  twice or on a stale order — which matters because the D3 ādeśas (6.3.25 ānaṅ, 8.3.82)
  key on `?samAsaPurva` and must see the *final* pūrva.
- **Deliberate deviation, document it:** in sweep 1 the samāsa saṁjñā does not exist
  yet, so 2.2.32's "in a dvandva" is gated on the composer's intent `?dvandva_vivakza`,
  not the formed `?dvandva`. The intent *is* the vivakṣā 2.2.29 keys on — faithful, but
  it must be stated in the YAML comment.
- Tests must feed **reversed input** (हर + हरि → हरिहरौ); every SK example is cited in
  its already-correct order, so canonical input makes the step a silent no-op.

**(M3) Ekaśeṣa member elision** — 1.2.64–73 retain one pada and delete the other(s),
the survivor taking the summed vacana. A post-fixpoint **`_commit_ekasesa`** step
deletes the member tagged `?ekaSeza_lupta` **and its sup**, then leaves the survivor
(`?ekaSeza_Sizyate`) to M1's `_swap_sups`. Must run *before* `_swap_sups` and before
`_nest_samasa_members` (inert here — ekaśeṣa members never carry
`?samAsaPurva`/`?samAsa`). `_samasa_prepass_branch`'s `_flagged()` (line 602) gains
`ekaSeza_vivakza` so ekaśeṣa windows are scanned.

**(M4) Aluk — suppressing the pūrva sup-luk** *(SK958–984)* — the engine luks every
pūrva member's sup via **2.4.71** (`sutras_antaranga.yaml:9844`). The whole aluk
prakaraṇa is one carve-out: an aluk rule tags the pūrva `?aluk`, and **2.4.71 gains a
`?!aluk` guard on its lp**, so the vigraha sup survives into the surface
(स्तोकान्मुक्तः, ओजसाकृतम्, आत्मनेपदम्). Two consequences to handle deliberately:
- The retained sup must be the **vigraha** one, so an `?aluk` pūrva must never also
  carry `?swap_viBakti` (2.1.12/2.1.13 set it) — add the mutual guard.
- With its sup retained the pūrva is a **full pada inside the compound**, so the
  junction becomes pada-boundary sandhi (स्तोकान् + मुक्तः, आत्मने + पदम्, परस्मै + पदम्,
  मातुः + स्वसा → मातुःष्वसा). This is the phase's real risk: see
  `project_samasa_semantic_pada_gotcha` (`?pada` at a compound junction depends on the
  member carrying a semantic sense) and `project_samasa_nesting_natva`
  (`_nest_samasa_members` must still resolve the whole thing as one `samasta_pada`).
  Prove the junction on a **visarga case, an n-final case and an e-final case** early
  in A0 before writing the long tail.

### Reused as-is (no engine change)

- The pre-pass spine: `_samasa_prepass`, `_samasa_prepass_branch`,
  `_samasa_window_fixpoint`, `_is_samasa_member`, and vibhāṣā forking (`optional: true`
  clones the skip branch — 2.4.12/13/16, 1.2.69/70/71, 5.4.72, 6.3.13/16/17/18/22/24,
  8.3.85 all need it, for free).
- **`_commit_samasa_napum`** (line 678) — already generic and already sets
  `?samasa_liNga_locked`; the samāhāra dvandva's napuṁsaka is the dvigu 2.4.1 /
  avyayībhāva 2.4.18 path exactly. `?samAhAra` is already composer-supplied (precedent:
  `test/samasa_list.py:414,429`).
- **`?samasanta_TaC` + `_insert_samasanta`** (line 747) and the
  `_SAMASANTA_AFFIXES` map — SK930 / 5.4.106 and the whole sarvasamāsānta अच् set are
  the `wac` already in the map (its comment already reads "aC/ṬaC"); अप् (`ap_s`) also
  already exists. **5.4.68 समासान्ताः is already realized** as this path
  (`generator_status.md:789`).
- **2.4.71** (pūrva sup-luk — now `?!aluk`-guarded), **1.2.43** (upasarjana),
  **`_nest_samasa_members`** (already spans >2 members and their sups).
- **Env-aware `$$` condition helpers already exist** — `process_yaml.py:79-86` calls a
  2-parameter helper as `fn(k, env)`, so cross-member conditions (2.2.34 अल्पाच्तर's
  vowel-count comparison, 1.2.64's सरूप lp==rp check) need **no DSL change**. One parity
  fix: `Sutra.evalConditionDetail` (`sutra.py:139`) still calls only the 1-arg form —
  add the same `inspect.signature` branch so the UI condition-detail view survives.

### Known trap (found during exploration — do not re-derive it the hard way)

**`?Gi` is not readable in the pre-pass.** 1.4.7 शेषो घ्यसखि is a *main-scan* saṁjñā
(`sutras_antaranga.yaml:7001`, `bahiranga: 0`) firing at the (stem | sup) window, so no
member carries `?Gi` at pre-pass time. SK903 / 2.2.32 द्वन्द्वे घि must **re-derive** ghi
with a `$$is_Gi_stem` helper in `paribhasha.py` mirroring 1.4.7's three arms (i/u-final,
not sakhi, not the nadī/feminine path), commented with the reason. Same class as the
5.4.153 `?NI` gap already recorded in the status doc.

---

## 2. Scope map

### द्वन्द्वसमासप्रकरणम् (SK 901–930)

| Block | SK / sūtra | Phase |
|---|---|---|
| core saṁjñā चार्थे द्वन्द्वः | SK901 / 2.2.29 | D0 |
| derived vacana (itaretara) | (1.4.21/1.4.22, scoped) | D0 |
| paravalliṅga — **widen the existing rule** | SK812 / 2.4.26 | D0 |
| pūrva-nipāta: राजदन्तादि, घि, अजाद्यदन्त, अल्पाच्तर | SK902–905 / 2.2.31–34 | D2 |
| ekavadbhāva (samāhāra) — prāṇyaṅga … समीपे | SK906–920 / 2.4.2–16 | D1 |
| पूर्ववदश्ववडवौ (dvandva gender exception) | SK813 / 2.4.27 | D1 |
| samāsānta ṭac on samāhāra | SK930 / 5.4.106 | D1 |
| ādeśas: ānaṅ, devatā-dvandva, अग्नि/दिव्/उषस्/मातर् | SK921–929 / 6.3.25–32, 8.3.82 | D3 |

### एकशेषप्रकरणम् (SK 188 + 931–939)

| Block | SK / sūtra | Phase |
|---|---|---|
| base rule सरूपाणामेकशेष एकविभक्तौ | SK188 / 1.2.64 | E0 |
| वृद्धो यूना / स्त्री पुंवच्च / पुमान् स्त्रिया | SK931–933 / 1.2.65–67 | E1 |
| भ्रातृपुत्रौ स्वसृदुहितृभ्याम् | SK934 / 1.2.68 | E1 |
| नपुंसकमनपुंसकेन (vibhāṣā + ekavat) | SK935 / 1.2.69 | E1 |
| पिता मात्रा / श्वशुरः श्वश्वा (both vibhāṣā) | SK936–937 / 1.2.70–71 | E1 |
| त्यदादीनि सर्वैर्नित्यम् | SK938 / 1.2.72 | E1 |
| ग्राम्यपशुसङ्घेष्वतरुणेषु स्त्री | SK939 / 1.2.73 | E1 |

### सर्वसमासान्तप्रकरणम् (SK 940–957)

| Block | SK / sūtra | Phase |
|---|---|---|
| ऋक्/पुर्/अप्/धुर्/पथिन् → अ + its ईत्/ऊत् ādeśas | SK940–942 / 5.4.74, 6.3.97, 6.3.98 | S0 |
| सामन्/लोमन्, अक्षि, वर्चस्, तमस्, श्रेयस्, रहस्, उरस्, गो, वेदि, अध्वन् | SK943–944, 946–953 / 5.4.75–76, 78–85 | S0 |
| the 25-item nipātana list | SK945 / 5.4.77 | S1 |
| **prohibitions** न पूजनात् / किमः क्षेपे / नञस्तत्पुरुषात् / पथो विभाषा | SK954–957 / 5.4.69–72 | S2 |

### अलुक्समासप्रकरणम् (SK 958–984)

| Block | SK / sūtra | Phase |
|---|---|---|
| अलुगुत्तरपदे adhikāra + the `?!aluk` guard on 2.4.71 | SK958 / 6.3.1 | A0 |
| pañcamī (स्तोकादि), tṛtīyā (ओजस्/सहस्/अम्भस्/तमस्, मनस्, आत्मन्) | SK959–963 / 6.3.2–6 | A0 |
| caturthī (आत्मने-/परस्मै-पदम्) | SK964–965 / 6.3.7–8 | A0 |
| saptamī: संज्ञा, कारनामन्, मध्य, स्वाङ्ग, बन्ध, कृत्, ज, काल, शय/वास | SK966, 968–976 / 6.3.9–18 | A1 |
| 8.3.95 गवियुधिभ्यां स्थिरः (गविष्ठिरः, युधिष्ठिरः) | SK967 / 8.3.95 | A1 |
| saptamī **prohibitions** नेन्सिद्धबध्नातिषु / स्थे च भाषायाम् | SK977–978 / 6.3.19–20 | A1 |
| ṣaṣṭhī: आक्रोश, पुत्र, ऋदन्त विद्या/योनि, स्वसृ/पति | SK979–982 / 6.3.21–24 | A2 |
| ṣatva: मातुः/पितुः ष्वसा, मातृ/पितृष्वसा | SK983–984 / 8.3.85, 8.3.84 | A2 |

**Scoped out by policy (explicit Skipped rows, per `project_prakarana_audit`):** the
vārttika long tail — 2.2.31 धर्मादिष्वनियमः, 2.2.34's
ऋतुनक्षत्र/लघ्वक्षर/अभ्यर्हित/वर्णानुपूर्व्य/भ्रातुर्ज्यायस् orderings, 6.3.26's वायुशब्दप्रयोगे
प्रतिषेधः, 1.2.72's four vārttikas, 6.3.21's आमुष्यायण/देवानांप्रिय/शुनःशेप/दिवोदास set
(unless a stem happens to exist). Also **SK925 / 6.3.28 इद्वृद्धौ** (आग्निमारुतम् needs
SK1239's उभयपदवृद्धि, a taddhita rule outside this range) and **SK928 / 6.3.31
उषासोषसः** (Vedic-only citation) unless they land cheaply.

---

## 2a. Implementation status (as-built)

Built sequentially on `generator`. This section is the authoritative as-built account
(the §3 phases keep the forward-looking design); update it per phase.

### Phase D0 — ✅ DONE (dvandva saṁjñā + derived vacana)

- **SK901 / 2.2.29 चार्थे द्वन्द्वः** landed as a `bahiranga: -1` rule, gated on the
  composer intent `?dvandva_vivakza` (mirroring `?bahuvrIhi_vivakza`). lp guard is
  `?!samAsaPurva` (**not** `?!samAsa`) so a chain's middle member — already `?samAsa` as
  the previous window's uttara — still becomes the next window's pūrva. → pūrva
  `+samAsaPurva` (+`?upasarjana` via 1.2.43), uttara `+samAsa +dvandva`.
- **Derived vacana (M1) landed** as the plan specified, riding the existing
  `?swap_viBakti` + `_swap_sups` lever with **no engine change**. Two arms:
  **1.4.22 द्व्येकयोर्द्विवचनैकवचने** (`lp ?vacana_1`, `rp [?dvandva ?vacana_1 ?!samAhAra]`
  → uttara `-vacana_1 +vacana_2 +swap_viBakti`) gives the DUAL; **1.4.21 बहुषु बहुवचनम्**
  (`lp ?!vacana_1`, same rp → `+vacana_3`) gives the PLURAL once the pūrva side has
  climbed past dual. n-ary is free via the existing adjacent-pair window walk: राम|कृष्ण
  → dual at window 1, then कृष्ण(now dual)|गोविन्द → plural at window 2. Trace confirms
  window 1 fires `[2.2.29, 1.2.43, 2.4.26, 1.4.22]` and window 2 `[…, 1.4.21]`.
- **SK812 / 2.4.26 परवल्लिङ्गम् widened** — rp condition is now
  `[and, [or, ?tatpuruza, ?dvandva], ?!paravalliNga]`; the sūtra names both. Documenting
  marker only (`join_objects` already prefers the last member's gender); it gives the
  D1 SK813/2.4.27 पूर्ववदश्ववडवौ override a clean saṁjñā, as the T-liṅga exceptions do.
- **Stems** धव/खदिर/पलाश added to `pratipadika.py` (plain masc a-stem trees).
- **Tests:** `test/test_samasa_dvandva.py` (a **members-list** driver, not a
  purva/uttara pair) + `samasa_dv_tests` in `test/samasa_list.py`; three assertion
  levels + a **vacana sweep** (धवखदिरौ dual / धवखदिरपलाशाः plural — proves derivation) + a
  vibhakti sweep. 11 cases green.
- **No deviations from the plan.** The one thing worth recording: the vacana rules fire
  *within the same window fixpoint* as 2.2.29 (they require the `?dvandva` 2.2.29 sets),
  so ordering is automatic — no priority/`overrides:` needed.

### Phase D1 — ✅ DONE (samāhāra ekavadbhāva + 2.4.17 + 5.4.106 ṭac + 2.4.27)

- **Ekavadbhāva rules landed:** SK906/2.4.2 प्राणितूर्यसेनाङ्ग (पाणिपादम्), SK912/2.4.8
  क्षुद्रजन्तवः (यूकालिक्षम्), SK913/2.4.9 शाश्वतिकविरोध (अहिनकुलम्), SK916/2.4.12 vibhāṣā
  वृक्षादि (प्लक्षन्यग्रोधम् / प्लक्षन्यग्रोधाः). Each is a `domain: saMjYA` rule on a class tag
  the composer supplies (`?prANyaNga` / `?kzudrajantu` / `?nityaviroDa` / `?vfkzAdi`);
  each sets `+samAhAra` and forces ekavacana (`-vacana_2 -vacana_3 +vacana_1 +swap_viBakti`)
  and carries **`overrides: [1.4.21, 1.4.22]`** so the itaretara-vacana rules never fire.
- **Deviation from the plan (a good one): split napuṁsaka into its own rule.** The plan had
  each ekavadbhāva rule set `+samasa_napum` directly. Instead **SK821/2.4.17 स नपुंसकम्** —
  a real, previously-unimplemented sūtra in this range — landed as a separate
  `bahiranga: -1` rule (`rp [?dvandva ?samAhAra ?!samasa_napum]` → `+samasa_napum`). This
  (a) is more faithful (2.4.2 = *ekavat*, 2.4.17 = *napuṁsaka*), and (b) lets a
  **composer-declared समाहार** — the समाहार sense of चार्थ, for a heterogeneous pair with no
  lexical class — reach napuṁsaka. It is gated `?dvandva`, so the dvigu (2.4.1) and
  avyayībhāva (2.4.18) napum paths are untouched.
- **SK930/5.4.106 द्वन्द्वाच्चुदषहान्तात्समाहारे** — `+samasanta_TaC` via the existing
  `_insert_samasanta`; **वाक्त्वचम्** (वाच्+त्वच्, both `?cudazaha_anta`, composer-declared
  samāhāra). The चु/द/ष/ह-final condition is a stem tag (the DSL `r` slot is the FIRST char).
- **SK813/2.4.27 पूर्ववदश्ववडवौ moved here from the tatpuruṣa deferred group** — a
  dvandva-side gender override (pūrva gender, not paravalliṅga): **अश्ववडवौ** (masc dual,
  not the fem अश्ववडवे). Same shape as tatpuruṣa 2.4.29; **hit the `?Ap` trap** — the uttara
  वडवा's ṭāp ā-stem markers survive the pum-lock and drive the fem declension, so the rule
  also clears `orp: [-Ap, -strI]` (exactly the bahuvrīhi B4 ā-stem fix).
- **दधिपयसी** added as a D0-style itaretara case: SK918/2.4.14 न दधिपयआदीनि's prohibition of
  ekavat is **vacuous until 2.4.6 जातिरप्राणिनाम् is implemented** (nothing makes दधि+पयस्
  samāhāra), so the pair falls out as a plain itaretara dual. Recorded as a Skipped row.
- **Deferred (Skipped rows):** the lexical/context-heavy ekavadbhāva sūtras 2.4.3/4/5/6/7/
  10/11/15/16 and the 2.4.13 vipratiṣiddha option — each needs domain-specific tagging
  (anuvāda / yajurveda-kratu / adhyayana / jāti-aprāṇin / nadī-deśa / śūdra / gaṇa /
  adhikaraṇa-number) with no new engine capability; the D1 mechanism covers them all when a
  class tag is added. 18 dvandva cases green.

### Phase D2 — ✅ DONE (physical pūrva-nipāta — the M2 engine step, 2.2.30 realized)

- **The reorder engine landed as designed.** A new `purvanipata: true` YAML flag (threaded
  `process_yaml` → `Sutra.purvanipata`) marks the ordering rules; `_split_sutras` carves a
  `_purvanipata_sutras` bucket out of `_samasa_sutras`. `_samasa_prepass_branch` now runs
  **SWEEP 1** (`_purvanipata_sweep`) *before* the window-fixpoint SWEEP 2: a left-to-right
  bubble pass tries the ordering rules per window in **aps-order** (lower id = stronger:
  2.2.32 > 2.2.33 > 2.2.34), the first triggered rule tags the uttara `?pUrvanipAta`, and
  **`_commit_purvanipata`** swaps the two member-units (member + trailing sups) so it lands
  first. Two disjoint rule sets with the reorder strictly between → SWEEP 2 always sees a
  clean order. **This is the deferred SK654/2.2.30 उपसर्जनं पूर्वम्, finally realized.**
- **Rules landed:** SK903/2.2.32 द्वन्द्वे घि (हरिहरौ), SK904/2.2.33 अजाद्यदन्तम् (ईशकृष्णौ),
  SK905/2.2.34 अल्पाच्तरम् (शिवकेशवौ) — each gated on `?dvandva_vivakza` (the intent, since
  the `?dvandva` saṁjñā does not exist yet in SWEEP 1) and a `$$rp_is_purva_*` env-aware
  helper comparing the two members. **Every test feeds REVERSED input** (हर+हरि, कृष्ण+ईश,
  केशव+शिव) to prove the move; a control case (हरि+हर, already correct) asserts 2.2.32 does
  *not* fire.
- **The `?Gi` trap the plan flagged was real** — 2.2.32 needed `$$rp_is_purva_ghi`, which
  re-derives the ghi saṁjñā (short-i/u-final, not sakhi/strī) because 1.4.7 is a
  `bahiranga:0` main-scan rule and no member carries `?Gi` in the pre-pass.
- **Parity fix applied:** `Sutra.evalConditionDetail` now calls a 2-arg `$$` helper as
  `fn(k, env)` (it previously only ever passed `(k)`), matching `process_yaml`. So the UI
  condition-detail view survives the new env-aware helpers.
- **SK902/2.2.31 राजदन्तादिषु परम् deferred** (Skipped row): a lexical ākṛtigaṇa that spans
  compound types (राजदन्त is a ṣaṣṭhī tatpuruṣa, not a dvandva), so it is not dvandva-scoped
  and needs the gaṇa data; the M2 mechanism will carry it when the gaṇa is added.
- **n-ary reorder is approximate** (a bubble pass, not a full topological sort) — exact for
  the 2-member compounds these examples use; noted in `_purvanipata_sweep`. 22 dvandva
  cases green.

### Phase D3 — ✅ DONE (dvandva ādeśas 6.3.25–29)

- **Pre-pass pūrva-substitution rules** (the bahuvrīhi B4 / tatpuruṣa 6.3.46 shape — an
  `xform` on the pūrva `l`/`lc`), all `bahiranga: -1`:
  - **SK921/6.3.25 आनङ् ऋतो द्वन्द्वे** — a `?vidyAyoni` ऋ-final pūrva's ऋ → आ
    (`xform l: A`, gated `$$is_ftanta`) → **मातापितरौ, होतापोतारौ, पितापुत्रौ**. The uttara
    keeps its own ऋ-/a-stem declension (होतृ→होतारौ vṛddhi, पितृ→पितरौ guṇa).
  - **SK922/6.3.26 देवताद्वन्द्वे च** — a `?devatA` dvandva's pūrva final → आ (not just
    ऋ-final: मित्र a-stem → मित्रा) → **मित्रावरुणौ**. Guarded `=!agni =!div` so its two
    apavādas win.
  - **SK923/6.3.27 ईदग्नेः सोमवरुणयोः** — अग्नि's इ → ई before सोम/वरुण (`overrides: 6.3.26`)
    → **अग्नीवरुणौ**.
  - **SK926/6.3.29 दिवो द्यावा** — whole-stem दिव् → द्यावा (`overrides: 6.3.26`) → the uttara
    पृथिवी (nadī) declines → **द्यावापृथिव्यौ**.
- **Deferred (Skipped rows):** **SK924/8.3.82** (अग्नीषोमौ — सोम's स→ष after अग्नी is a
  cross-compound ṣatva, the same class as the general cross-member ṇatva gap; अग्नीवरुणौ
  covers 6.3.27 without it); **SK929/6.3.32** (मातरपितरौ — the substitution मातृ→मातर् leaves
  an r-final pūrva whose junction with पितृ mis-fires to a visarga मातःपितरौ; the माता form
  from 6.3.25 is the one that surfaces); **SK925/6.3.28** (इद्वृद्धौ — taddhita उभयपदवृद्धि,
  out of range) and **SK928/6.3.31** (उषास्, Vedic-only). 28 dvandva cases green.

### Phase E0 — ✅ DONE (ekaśeṣa spine: SK188/1.2.64 + the M3 elision step)

- **M3 landed.** `$$sarUpa(k, env)` (lp≡rp content) in `paribhasha.py` — the same helper the
  bahuvrīhi 2.2.27 needs. **SK188/1.2.64 सरूपाणामेकशेष** tags the pūrva `?ekaSeza_lupta` and
  the uttara `?ekaSeza_Sizyate`; **`_commit_ekasesa`** (a new post-fixpoint step, before
  `_swap_sups`) physically deletes the लुप्त members + their sups. `_flagged()` gained
  `ekaSeza_vivakza` so ekaśeṣa windows are scanned. → **रामौ** (राम+राम), **रामाः** (×3).
- **Vacana reuse, no new rule.** The survivor's number is DERIVED by the **widened
  1.4.22/1.4.21** — their rp gate is now `[or, ?dvandva, ?ekaSeza_Sizyate]`, so the same
  dual/plural climb serves both dvandva and the ekaśeṣa survivor. The survivor declines in
  the supplied vibhakti (रामाभ्याम् for the instrumental dual) — proven by a vibhakti sweep.
- **Ekaśeṣa ≠ compound:** the survivor is a single pada, so `_nest_samasa_members` (keyed on
  `?samAsaPurva`/`?samAsa`) correctly leaves it flat. Intents are disjoint
  (`?ekaSeza_vivakza` vs `?dvandva_vivakza`), so no override vs 2.2.29 was needed.

### Phase E1 — ✅ DONE (ekaśeṣa vidhis 1.2.67/68/70/72/73)

- All E1 rules **reuse 1.2.64's update** (olp `+ekaSeza_lupta`, orp `+ekaSeza_Sizyate`) with
  the **survivor as the uttara (rp)**, so the widened 1.4.22 derives the dual — they differ
  only in the "which survives" condition:
  - **SK933/1.2.67 पुमान् स्त्रिया** — masc survives over its same-base feminine → **हंसौ**
    (हंसी+हंस). Gated **`?tallakzaRa`** (composer-supplied): the tallakṣaṇa/bhāṣitapuṁska
    same-base requirement — WITHOUT it 1.2.67 wrongly collapsed भ्रातृ+स्वसृ / मातृ+पितृ
    (different lexemes) and masked 1.2.68/1.2.70. (Bug found and fixed during iteration.)
  - **SK934/1.2.68 भ्रातृपुत्रौ स्वसृदुहितृभ्याम्** → **भ्रातरौ, पुत्रौ**.
  - **SK936/1.2.70 पिता मात्रा** → **पितरौ** (the ekaśeṣa arm; the dvandva मातापितरौ is D3).
  - **SK938/1.2.72 त्यदादीनि सर्वैः** → **तौ** (the `?tyadAdi` pronoun survives).
  - **SK939/1.2.73 ग्राम्यपशुसङ्घेषु स्त्री** → **अजे** (fem survives, `overrides: 1.2.67` —
    exercised even with both tags present).
- **Deferred (Skipped rows):** **SK931/1.2.65 वृद्धो यूना** + **SK932/1.2.66 स्त्री पुंवच्च**
  (gotra/yuvan — need the gotra derivation, गार्ग्यौ/गर्गाः); **SK937/1.2.71 श्वशुरः श्वश्वा**
  (needs श्वशुर→श्वाशुर vṛddhi); **SK935/1.2.69 नपुंसकम्** (needs the optional-ekavat vacana
  mode शुक्लम्/शुक्लानि, outside the itaretara-sum model). 14 ekaśeṣa cases green.

---

## 3. Phases (sequential on `generator`; each ends full-suite green + a status update)

### Phase D0 — Spine: dvandva saṁjñā + derived vacana — ✅ DONE (see §2a)

- **SK901 / 2.2.29 चार्थे द्वन्द्वः** — condition: both members `?viBakti_1` +
  `?dvandva_vivakza` (intent gate — a dvandva has no lexical discriminator, exactly
  like `?bahuvrIhi_vivakza`); update `olp: [+samAsaPurva]`, `orp: [+samAsa, +dvandva]`.
  The lp guard must **not** exclude `?samAsa`, so a chain राम|कृष्ण|गोविन्द keeps forming
  at each window.
- **Derived vacana (M1)** — a `bahiranga: -1` rule (id `1.4.22`, with `1.4.21` as its
  bahutva arm) on a `?dvandva` window: `(vacana_1, vacana_1) → orp vacana_2`, anything
  else → `orp vacana_3`; both set `+swap_viBakti`. Guard `?!samAhAra`.
- **SK812 / 2.4.26 परवल्लिङ्गम्** — implemented but gated `rp: ?tatpuruza`
  (`sutras_antaranga.yaml:9909`); **widen to `[or, ?tatpuruza, ?dvandva]`** — the sūtra
  reads द्वन्द्वतत्पुरुषयोः. `join_objects` already prefers the last member's liṅga.
- Surface goals: **धवखदिरौ** (dual), a 3-member chain (plural), a vibhakti sweep.
- Files: `sutras_antaranga.yaml` (dvandva block after the bahuvrīhi block);
  `pratipadika.py` (धव, खदिर … — **grep surface form and var name first**, per
  `feedback_check_pratipadika_dupes`); new `test/test_samasa_dvandva.py` +
  `samasa_dv_tests` in `test/samasa_list.py` — the driver needs a **`members: [...]`
  list** (the bahuvrīhi driver hard-codes exactly two).

**D0 must land before D1–D3.**

### Phase D1 — Samāhāra: ekavadbhāva + ṭac — ✅ DONE (see §2a)

- **SK906–920 / 2.4.2–16** — each sets `orp: [+samAhAra, +samasa_napum, -vacana_*,
  +vacana_1, +swap_viBakti]`; `_commit_samasa_napum` turns the marker into real
  `?napum` + the gender lock. Class membership (प्राण्यङ्ग, तूर्य, सेनाङ्ग, चरण,
  जाति/अप्राणिन्, क्षुद्रजन्तु, शूद्र-अनिरवसित, विरोध-शाश्वतिक, वृक्ष/मृग/तृण/धान्य/…) is
  composer-supplied pratipadika tags, as `?samAhAra` is for the dvigu today.
- **Vibhāṣā arms** 2.4.12/13/16 → `optional: true` fork: प्लक्षन्यग्रोधम् /
  प्लक्षन्यग्रोधाः, शीतोष्णम् / शीतोष्णे.
- **Prohibition SK918 / 2.4.14 न दधिपयआदीनि** → दधिपयसी (`overrides:` apavāda).
- **SK930 / 5.4.106** → `orp: [+samasanta_TaC]` on a च/द/ष/ह-final samāhāra dvandva →
  **वाक्त्वचम्**.
- **SK813 / 2.4.27 पूर्ववदश्ववडवौ** — currently in the *tatpuruṣa* deferred group
  (`generator_status.md:783`) though it is a dvandva rule: अश्ववडवौ takes the **pūrva's**
  gender. Move it here (pūrva-gender override + `?samasa_liNga_locked`, same shape as
  2.4.29).

### Phase D2 — Pūrva-nipāta (the M2 engine step) — ✅ DONE (see §2a)

- `_split_sutras` + the two-sweep `_samasa_prepass_branch` + `_commit_purvanipata`,
  per §1 M2.
- **SK903 / 2.2.32 द्वन्द्वे घि** (with `$$is_Gi_stem` — see §1's trap) → हरिहरौ from
  `हर हरि`. **SK904 / 2.2.33 अजाद्यदन्तम्** (`$$is_ajady_adanta`: vowel-initial *and*
  a-final — the member's initial char is not reachable via the `l` window slot, hence a
  helper) → ईशकृष्णौ. **SK905 / 2.2.34 अल्पाच्तरम्** (`$$alpActara(k, env)`, the 2-arg
  env-aware form, counting vowels in `env["lp"]` vs `env["rp"]`) → शिवकेशवौ.
  **SK902 / 2.2.31 राजदन्तादिषु परम्** (lexical ākṛtigaṇa; the *later* member first) →
  राजदन्तः.
- Priority 2.2.31 > 2.2.32 > 2.2.33 > 2.2.34, plus the vārttika घ्यन्तादजाद्यदन्तं
  विप्रतिषेधेन (इन्द्राग्नी) as an `overrides:` on 2.2.33 (or an explicit skip).
- Every D2 test feeds **reversed input** and asserts fired trace + reordered surface.
- Regression watch: the reorder must be a strict no-op for every existing avyayībhāva /
  tatpuruṣa / bahuvrīhi case.

### Phase D3 — Dvandva ādeśas (SK921–929 / 6.3.25–32, 8.3.82) — ✅ DONE (see §2a)

Pre-pass **pūrva-substitution** rules, the shape bahuvrīhi B4 used (char-window
`rc`/`r` or whole-stem replace, mirroring tatpuruṣa SK807 / 6.3.46 महत्→महा):
- **SK921 / 6.3.25 आनङ् ऋतो द्वन्द्वे** → होतापोतारौ, मातापितरौ, पितापुत्रौ.
- **SK922 / 6.3.26 देवताद्वन्द्वे च** → मित्रावरुणौ; **SK923 / 6.3.27 ईदग्नेः सोमवरुणयोः**
  + **SK924 / 8.3.82 अग्नेः स्तुत्स्तोमसोमाः** → **अग्नीषोमौ**, अग्नीवरुणौ. Check whether
  8.3.82 fires at the merged junction or needs the `?samasta_Ratva`-style lever the
  bahuvrīhi ṇatva work built.
- **SK926 / 6.3.29 दिवो द्यावा**, **SK927 / 6.3.30 दिवसश्च पृथिव्याम्** → द्यावापृथिव्यौ /
  दिवस्पृथिव्यौ (the `div` stem exists, `pratipadika.py:150`).
- **SK929 / 6.3.32 मातरपितरावुदीचाम्** → मातरपितरौ beside 6.3.25's मातापितरौ (a fork).
- **Watch the `?Ap` trap** bahuvrīhi B4 documented: a substitution rewrites the stem
  *string* but leaves the source's class tags; from an ā-stem add
  `update: orp: [-Ap, -strI]`.

### Phase E0 — Ekaśeṣa spine: SK188 / 1.2.64 + the M3 elision step — ✅ DONE (see §2a)

- **`$$sarUpa(k, env)`** in `paribhasha.py` (lp content == rp content) — the same check
  bahuvrīhi 2.2.27 has been blocked on; write once, use twice.
- **SK188 / 1.2.64 सरूपाणामेकशेष एकविभक्तौ** — identical members in the same vibhakti
  (`?ekaSeza_vivakza` intent) → pūrva `+ekaSeza_lupta`, uttara `+ekaSeza_Sizyate` + the
  M1 vacana bump.
- **`_commit_ekasesa`** (§1 M3) + `ekaSeza_vivakza` added to `_flagged()`.
- **Ekaśeṣa must beat dvandva** at a window (SK939's note): `overrides: 2.2.29`, or gate
  2.2.29 on `?!ekaSeza_vivakza`.
- Surface: राम + राम → **रामौ**; three → **रामाः**; a vibhakti sweep.
- New `test/test_ekasesa.py` + `ekasesa_tests` in `test/samasa_list.py`.

### Phase E1 — Ekaśeṣa vidhis (SK931–939 / 1.2.65–73) — ✅ DONE (see §2a)

One rule + one lexical pair per sūtra on the E0 spine:
- **SK931 / 1.2.65 वृद्धो यूना** → गार्ग्यौ; **SK932 / 1.2.66 स्त्री पुंवच्च** → गर्गाः,
  दाक्षी; **SK933 / 1.2.67 पुमान् स्त्रिया** → हंसौ.
- **SK934 / 1.2.68 भ्रातृपुत्रौ स्वसृदुहितृभ्याम्** → भ्रातरौ, पुत्रौ (all four stems exist:
  `pratipadika.py:810,751,62,757`).
- **SK935 / 1.2.69 नपुंसकमनपुंसकेन** — neuter survives, ekavadbhāva `optional: true` →
  शुक्लम् / शुक्लानि.
- **SK936 / 1.2.70 पिता मात्रा** (vibhāṣā) → पितरौ / मातापितरौ — the second fork is D3's
  dvandva, a cross-check that the prakaraṇas compose.
- **SK937 / 1.2.71 श्वशुरः श्वश्वा** (vibhāṣā) → श्वाशुरौ / श्वश्रूश्वाशुरौ.
- **SK938 / 1.2.72 त्यदादीनि सर्वैर्नित्यम्** — nitya; `?tyadAdi` already exists
  (`pratipadika.py:1015-1017`) → स च देवदत्तश्च = **तौ**.
- **SK939 / 1.2.73 ग्राम्यपशुसङ्घेषु** — apavāda to 1.2.67 (`overrides: 1.2.67`) → गाव इमाः.

### Phase S0 — ✅ DONE (sarvasamāsānta — the s-stem अच् family + the napum-lock fix)

- **Landed the s-stem अच् family** (all `?samasanta_TaC` + the existing `_insert_samasanta`,
  as tatpuruṣas): **SK946/5.4.78 ब्रह्महस्तिभ्यां वर्चसः → ब्रह्मवर्चसम्** (ṣaṣṭhī),
  **SK947/5.4.79 अवसमन्धेभ्यस्तमसः → अन्धतमसम्** (karmadhāraya, अन्ध arm),
  **SK949/5.4.81 अन्ववतप्ताद्रहसः → तप्तरहसम्** (karmadhāraya, तप्त arm).
- **The load-bearing discovery — a latent `wac` bug, now fixed at the root.** `wac` carried
  an intrinsic **`?pum`** (`pratyaya.py`), so an s-stem *napuṁsaka* uttara + अच् came out
  **masc** (ब्रह्मवर्चस**ः**). Investigating *why* wac had pum: it was a **pre-2.4.29
  shortcut** (commit 8b16b8a, Apr 2026) for the `dvyahna` manual test stem
  `[dvi, luk_sup, in_compound(ahan), wac]`, which is built by hand and **bypasses the
  samāsa pre-pass** where SK814/2.4.29 रात्राह्नाहाः पुंसि (an ahan-final compound is puṁs)
  would make it masc. The pum was hung on the *affix* instead — wrong as a general property,
  since it mis-genders every napum wac samāsānta (avyayībhāva उपराजम्, dvigu पञ्चगवम्,
  dvandva वाक्त्वचम्, and these s-stems), which only survived because each had a
  `?samasa_liNga_locked` overriding it. **Fix:** removed `?pum` from `wac` (now
  gender-neutral); `dvyahna` sets pum on its *local* wac copy (`in_context(wac, "pum")`,
  representing 2.4.29); and the S0 rules need **no lock** — napum falls out of paravalliṅga.
  Verified: पुण्यरात्रः (2.4.29) stays masc, पञ्चगवम्/उपराजम्/वाक्त्वचम् stay napum, द्व्यह्नः
  stays masc.
- **Deferred (Skipped rows), honestly:** **SK944/5.4.76 गवाक्षः** — गो+अक्षि+अच् *does* yield
  गवाक्षः, but the go-stem optional-sandhi rules (6.1.122–124) over-generate गोक्षः/गोऽक्षः at
  the same junction (a pre-existing go artifact, not this affix). **SK940/5.4.74** (ऋच्/पुर्/
  अप्/धुर्/पथिन् → अर्धर्चः/सुपथः, and its 2.4.30/2.4.31 clearing), **SK941–942/6.3.97–98**
  (द्वीपम् — the ईत्/ऊत् ādeśa on 5.4.74's अप्), **SK943/5.4.75** (सामन्/लोमन्), **SK948/5.4.80,
  SK950–953/5.4.82–85** (श्वस्/उरस्/गो/वेदि/अध्वन् — several are avyayībhāva-pūrva). Each is the
  **same अच् insertion** on a different uttara-class/compound-type; the mechanism (incl. the
  napum lock) is proven, so each needs only its stem + compound formation. 3 S0 cases green.
- **SK945/5.4.77** (the 25-item nipātana list) is **S1**; **SK954–957/5.4.69–72** the
  prohibitions are **S2**.

### Phase S0 (original plan) — Sarvasamāsānta: the affix set (SK940–944, 946–953)

All are `?samasanta_*` markers + the existing `_insert_samasanta`; the affix is the अ
(`wac`, whose map comment already covers aC/ṬaC) unless noted:
- **SK940 / 5.4.74 ऋक्पूरब्धूःपथामानक्षे** → **अर्धर्चः**, विष्णुपुरम्, विमलापं सरः, सुपथः —
  with the अनक्षे carve-out (अक्षधूः). This single rule **clears two standing tatpuruṣa
  deferrals**: 2.4.30 अपथं नपुंसकम् (needed the pathin अच्) and 2.4.31 अर्धर्चाः पुंसि
  (needed अर्धर्च) — land them here or in phase X.
- **SK941–942 / 6.3.97 द्व्यन्तरुपसर्गेभ्योऽप ईत्, 6.3.98 ऊदनोर्देशे** — ādeśas on the
  *result* of that अ → **द्वीपम्**, अन्तरीपम्, प्रतीपम्, समीपम्, अनूपो देशः. Char-window
  rules on the samāsānta output; note they must fire *after* the affix insert.
- **SK943 / 5.4.75 सामलोम्नः** → प्रतिलोमम्, अनुलोमम्; **SK944 / 5.4.76 अक्ष्णोऽदर्शनात्**
  → **गवाक्षः**.
- **SK946–953 / 5.4.78–85** — ब्रह्मवर्चसम्/हस्तिवर्चसम्, अवतमसम्/संतमसम्/अन्धतमसम्,
  श्वोवसीयसम्, अनुरहसम्, प्रत्युरसम्, अनुगवम्, द्विस्तावा/त्रिस्तावा वेदिः, प्राध्वो रथः. Highly
  lexical: one stem + one case each (उरस्, पयस् etc. already exist).

### Phase S1 — ✅ DONE (the 5.4.77 nipātana gaṇa — representative set)

- **SK945/5.4.77** (the 25-item nipātana list) landed as **one rule** gated on a composer
  gaṇa tag **`?nipAta_5477`** on the qualifying uttara → `?samasanta_TaC` →
  `_insert_samasanta` inserts wac (अ). The compound TYPE varies across the 25 members, so a
  single tag-gated rule serves them all.
- **Representative members implemented** (the SK groups them, so they share machinery):
  the उक्षन् **karmadhāraya trio** — **जातोक्षः, महोक्षः** (महत्→महा by 6.3.46), **वृद्धोक्षः**
  (उक्षन्+अच् → उक्ष, then a+u → o) — and a **dvandva** — **वाङ्मनसे** (वाच्+मनस्, the nipātana
  अच् on the dvandva; वाग्मनसे is the valid optional-anunāsika variant, 8.4.45). Now that the
  wac fix landed, no gender lock is needed (paravalliṅga / the उक्षन् masc carry through).
- **Deferred (Skipped row):** the other ~21 nipātanas (अचतुर/विचतुर/सुचतुर, स्त्रीपुंसौ,
  धेन्वनडुहौ, ऋक्सामे, अक्षिभ्रुवम्, दारगवम्, ऊर्वष्ठीवम्, पदष्ठीवम्, नक्तन्दिवम्, रात्रिन्दिवम्,
  अहर्दिवम्, सरजसम्, निःश्रेयसम्, पुरुषायुषम्, द्व्यायुषम्/त्र्यायुषम्, ऋग्यजुषम्, उपशुनम्, गोष्ठश्वः).
  Each is the **same nipātana अच्** on its own stem-pair + compound; a few carry additional
  nipātita changes (ṭi-lopa पदष्ठीवम्, samprasāraṇa उपशुनम्, पाद→पद्) or need irregular stems
  (अनडुह्, श्वन्, अष्ठीवत्). 5 S1 cases green.

### Phase S1 (original plan) — Sarvasamāsānta: the 5.4.77 nipātana list (SK945)

Twenty-five nipātita forms. Purely lexical; each is a fixed stem-pair + fixed surface,
so implement as a gaṇa-tagged rule plus one test case each. Grouped as SK itself groups
them: 3 bahuvrīhis (अचतुरः, विचतुरः, सुचतुरः), then the **dvandvas** — स्त्रीपुंसौ,
धेन्वनडुहौ, ऋक्सामे, वाङ्मनसे, अक्षिभ्रुवम्, दारगावम्, ऊर्वष्ठीवम्, पदष्ठीवम्, नक्तन्दिवम्,
रात्रिन्दिवम्, अहर्दिवम्, ऋग्यजुषम् (these need the D phases) — then सरजसम् (avyayībhāva),
निःश्रेयसम् (tatpuruṣa), पुरुषायुषम्, द्व्यायुषम्/त्र्यायुषम् (dvigu), and the three
karmadhārayas जातोक्षः/महोक्षः/वृद्धोक्षः, plus उपशुनम्, गोष्ठश्वः. May be split in half if
it runs long; the ṭi-lopa / samprasāraṇa nipātanas (पदष्ठीवम्, उपशुनम्) are the only
non-mechanical ones.

### Phase S2 — ✅ DONE (samāsānta prohibitions 5.4.71/72; clears the standing 2.4.30)

- Implemented via the **shared `?samasanta_niziDDa` guard** (the one the bahuvrīhi
  5.4.153/155/159/160 already honour) — chose it over per-rule `overrides:` because it
  keeps the existing affix set untouched; the prohibition rule sets the guard, the affix
  rule checks `?!samasanta_niziDDa`.
- **SK956/5.4.71 नञस्तत्पुरुषात्** → **अराजा**: a नञ्-tatpuruṣa takes NO samāsānta, so राजन्
  keeps its declension. **This fixed a real bug** — न+राजन् was giving *अराजः (5.4.91's ṭac
  wrongly firing → अराज a-stem); now 5.4.71 sets `?samasanta_niziDDa` (+ `overrides: 5.4.91`),
  and 5.4.91 gained the `?!samasanta_niziDDa` guard. **Positive control:** the landed
  परमराजः still takes ṭac (5.4.71 gates on `?naY`, which परम lacks).
- **SK957/5.4.72 पथो विभाषा** → **अपथम् / अपन्थाः** (`optional: true` fork): a नञ्पूर्व पथिन्
  optionally takes अच् — अपथम् (with अच् → अपथ) OR अपन्थाः (without → पथिन् declension, पन्थाः).
  **This lands SK815/2.4.30 अपथं नपुंसकम्** (a standing tatpuruṣa T-liṅga deferral): the
  अच्-fork is napuṁsaka (`?samasanta_TaC`-gated `+samasa_napum`), the no-अच् fork stays masc.
  पथिन् is excluded from 5.4.71's blanket block (`?!paTin`) precisely because it is 5.4.72's
  domain.
- **Deferred (Skipped row):** **SK954/5.4.69 न पूजनात्** (सुराजा — needs the सु/अति pūjana
  prefix compound) and **SK955/5.4.70 किमः क्षेपे** (किंराजा — needs the किम् compound + a
  `?kzepa` sense). Both are the same `?samasanta_niziDDa` block on a different pūrva-class;
  the mechanism is proven. 2 S2 cases green.

### Phase S2 (original plan, superseded by §2a) — Samāsānta prohibitions (SK954–957 / 5.4.69–72)

Cross-cutting and **regression-critical**: these block samāsāntas *in general*, so they
must be tested against the already-landed 5.4.86–112 (avyayībhāva/tatpuruṣa) and
5.4.113–160 (bahuvrīhi) sets, not only against S0/S1.
- **SK954 / 5.4.69 न पूजनात्** → सुराजा, अतिराजा (with the वार्त्तिक स्वतिभ्यामेव, so
  परमराजः is untouched; and the scope note that the prohibition stops before 5.4.113 —
  सुसक्थः, स्वक्षः still take their affix).
- **SK955 / 5.4.70 किमः क्षेपे** → किंराजा / किंराजः (a `?kzepa` sense tag).
- **SK956 / 5.4.71 नञस्तत्पुरुषात्** → अराजा, असखा (reuses the T3 `?naY` tag).
- **SK957 / 5.4.72 पथो विभाषा** → अपथम् / अपन्थाः (`optional: true`).
Implement as `overrides:` entries on the samāsānta rules, or as a shared
`?samasanta_nizedDa` guard the marker-setting rules honour — pick whichever keeps the
existing set untouched, and say which and why.

### Phases A0 / A1 / A2 — ✅ DONE (the M4 aluk mechanism + one clean case per vibhakti)

- **M4 landed exactly as designed.** The whole aluk prakaraṇa (6.3.1 अलुगुत्तरपदे adhikāra,
  folded in) is **one engine carve-out**: an aluk rule tags the pūrva **`?aluk`**, and
  **2.4.71 gained a `?!aluk` guard** on its lp, so the pūrva's vigraha sup is NOT luk'd and
  survives into the compound. No `?swap_viBakti` collides here (none of these pūrvas take
  it), so the retained sup is the vigraha one.
- **A0 — the three "spine" junction types** (the plan's junction proof), all clean:
  - **SK959/6.3.2 पञ्चम्याः स्तोकादिभ्यः** → **स्तोकान्मुक्तः** (n-final junction; स्तोकात्+मुक्त,
    त्→न् before म by 8.4.45; स्तोकाद्मुक्तः the jaśtva variant). **This flips the old
    स्तोकमुक्तः deferral** — the T1 test case was updated.
  - **SK960/6.3.3 ओजःसहोऽम्भस्तमसस्तृतीयायाः** → **ओजसाकृतम्** (tṛtīyā, s-stem).
  - **SK964/6.3.7 वैयाकरणाख्यायां चतुर्थ्याः** → **आत्मनेपदम्** (caturthī, e-final — the
    generator derives its own metalanguage).
- **A1 — saptamī:** **SK971/6.3.13 बन्धे च विभाषा** → **हस्तेबन्धः / हस्तबन्धः** (optional aluk
  fork; the saptamī-tp forms via 2.1.41's बन्ध arm).
- **A2 — ṣaṣṭhī:** **SK979/6.3.21 षष्ठ्या आक्रोशе** → **चौरस्यकुलम्** (ākrośa sense), with a
  **negative control चौरकुलम्** (non-ākrośa → the ṣaṣṭhī luks as usual).
- **Deferred (Skipped rows):** the **ṣatva** aluk rules **SK967/8.3.95** (युधिष्ठिरः,
  गविष्ठिरः) and **SK983–984/8.3.84–85** (मातृष्वसा/मातुःष्वसा) — cross-junction ṣatva, the
  same class as the deferred D3 8.3.82 (अग्नीषोमौ); the **vyadhikaraṇa-bahuvrīhi** saptamī
  aluks (6.3.9/10/12 त्वचिसारः/कण्ठेकालः — need 2.2.35 word-order, phase X); the **kṛd-anta**
  ones (6.3.14/15/16 स्तम्बेरमः/दिविजः — need upapada machinery); and the sense-gaṇa tail
  (6.3.4/5/6/17/18/22/23/24). The **prohibitions 6.3.19/20** (सांकाश्यसिद्धः, समस्थः) are
  **vacuous by default** — 2.4.71 already luks, so no rule is needed. 6 aluk cases green.

### Phase A0 (original plan) — Aluk spine (M4) + pañcamī/tṛtīyā/caturthī (SK958–965)

- **SK958 / 6.3.1 अलुगुत्तरपदे** — the adhikāra; folded into the first rule as the
  `?aluk` tag (the engine's `sutra_dict` forbids a rule with no vidhi, exactly as
  2.2.23 was folded into 2.2.24). Note in the comment that the adhikāra runs
  *प्राग् आनङः*, i.e. up to D3's 6.3.25.
- **The `?!aluk` guard on 2.4.71** + the `?swap_viBakti` mutual guard (§1 M4).
- **SK959 / 6.3.2 पञ्चम्याः स्तोकादिभ्यः** → **स्तोकान्मुक्तः**, अन्तिकादागतः, दूरादागतः —
  this is the exact form `generator_status.md:774` records as deferred; flip that row.
- **SK960 / 6.3.3 ओजःसहोऽम्भस्तमसस्तृतीयायाः** → ओजसाकृतम्; **SK961–962 / 6.3.4–5
  मनसः संज्ञायाम् / आज्ञायिनि च** → मनसागुप्ता, मनसाज्ञायी; **SK963 / 6.3.6 आत्मनश्च**
  (पूरण vārttika) → आत्मनापञ्चमः.
- **SK964–965 / 6.3.7–8 वैयाकरणाख्यायां चतुर्थ्याः / परस्य च** → **आत्मनेपदम्**,
  **परस्मैपदम्** (a satisfying pair: the generator will finally derive its own
  metalanguage).
- **Do the junction proof first** (§1 M4): a visarga case, an n-final case
  (स्तोकान्मुक्तः) and an e-final case (आत्मनेपदम्) before writing the rest.

### Phase A1 — Saptamī aluk + ṣatva + prohibitions (SK966–978)

- **SK966 / 6.3.9 हलदन्तात्सप्तम्याः संज्ञायाम्** → त्वचिसारः; **SK967 / 8.3.95
  गवियुधिभ्यां स्थिरः** → **गविष्ठिरः, युधिष्ठिरः** (a main-scan ṣatva at the junction,
  like D3's 8.3.82 — share the diagnosis).
- **SK968–971 / 6.3.10–13** → मुकुटेकार्षापणम्, मध्येगुरुः, **कण्ठेकालः** (6.3.12
  स्वाङ्ग — the same form phase X's 2.2.35 produces, a useful cross-check),
  हस्तेबन्धः/हस्तबन्धः (vibhāṣā).
- **SK972 / 6.3.14 तत्पुरुषे कृति बहुलम्** → स्तम्बेरमः, कर्णेजपः (बहुलम् — fire on a
  lexical list, do not generalize; कुरुचरः is the counter-example).
- **SK973–976 / 6.3.15–18** → प्रावृषिजः, दिविजः; वर्षेजः/वर्षजः, पूर्वाह्णेतरे/पूर्वाह्णतरे,
  खेशयः/खशयः, ग्रामेवासी/ग्रामवासी (three vibhāṣās).
- **Prohibitions SK977–978 / 6.3.19–20** → स्थण्डिलशायी, चक्रबद्धः, समस्थः.

### Phase A2 — Ṣaṣṭhī aluk + मातृ/पितृ ṣatva (SK979–984)

- **SK979 / 6.3.21 षष्ठ्या आक्रोशे** → **चौरस्यकुलम्** (vs ब्राह्मणकुलम् without the
  आक्रोश sense — a `?AkroSa` tag, the negative case is the test).
- **SK980 / 6.3.22 पुत्रेऽन्यतरस्याम्** (vibhāṣā, निन्दायाम्) → दास्याः पुत्रः / दासीपुत्रः.
- **SK981 / 6.3.23 ऋतो विद्यायोनिसम्बन्धेभ्यः** → होतुःपुत्रः, पितुरन्तेवासी (reuses the
  same विद्या/योनि-सम्बन्ध class D3's 6.3.25 ānaṅ needs — define the tag once, in D3).
- **SK982 / 6.3.24 विभाषा स्वसृपत्योः** + **SK983–984 / 8.3.85, 8.3.84** →
  **मातुःस्वसा / मातुःष्वसा / मातृष्वसा** (the three-way paradigm: aluk × ṣatva, both
  optional — a good end-to-end fork test).

### Phase X — ✅ AUDITED (2.2.30 realized; the rest blocked *beyond* the four mechanisms)

Phase X was meant to spend M1–M4 on the standing deferrals. The audit outcome:
- **SK654/2.2.30 उपसर्जनं पूर्वम् — DONE** (in D2): the generic pūrva-nipāta is realized by the
  M2 `_purvanipata_sweep` / `_commit_purvanipata` step; its status row was flipped to
  Implemented. There is no standalone 2.2.30 rule (it is an adhikāra; 2.2.32–34 are its
  applications).
- **The remaining items need machinery OUTSIDE the four mechanisms, so they stay deferred**
  (honestly, with precise blockers): **SK846/2.2.27 सरूपे** + **SK866/5.4.127 केशाकेशि** need
  **6.3.137 अन्येषामपि दृश्यते** (the केश→केशा dīrgha, unimplemented) + तिष्ठद्गु-gaṇa avyaya
  tagging — `$$sarUpa` and `ic_s` exist, but they are not the blocker. **SK898–900/2.2.35–37**
  (bahuvrīhi word-order) *could* use the M2 step, but the reorder must run **before** the B0
  referent-gender assignment (the `?referent_*` tag follows the *final* uttara, not the input
  uttara) — a sequencing refinement, not new mechanism. Recorded in `generator_status.md`.

### Phase X (original plan) — Spend the new mechanisms on the standing deferrals

- **SK846 / 2.2.27 तत्र तेनेदमिति सरूपे** — needs exactly E0's `$$sarUpa`.
- **SK866 / 5.4.127 इच् कर्मव्यतिहारे → केशाकेशि** — 2.2.27 + the existing `ic_s` affix +
  **6.3.137 अन्येषामपि दृश्यते** (unimplemented — supplies the केश→केशा dīrgha) + avyaya
  tagging. (The old "needs reduplication" framing is wrong: SK's vigraha केशेषु केशेषु
  supplies the word twice.) Also unlocks 6.4.146 ओर्गुणः / बाहूबाहवि.
- **SK898–900 / 2.2.35–37** — currently tagging + input-order validation; convert to
  real `?pUrvanipAta` rules on the M2 step → कण्ठेकालः, कृतकृत्यः from reversed input.
- **SK654 / 2.2.30 उपसर्जनं पूर्वम्** — the generic rule M2 realizes; flip the row from
  Partial to Implemented and re-point every Skipped row citing it as its blocker.
- **SK815–816 / 2.4.30–31** (अपथम्, अर्धर्चः) if not already landed in S0.

### Phase DE-UI — ✅ AS-BUILT

- **CLI** (`cmd_line.py`): `prepare_dvandva(words, samahara)` + `prepare_ekasesa(words)`
  (mirroring `prepare_bahuvrihi`) + the flags **`--dvandva` / `--samahara` / `--ekasesa`**,
  wired in the `--samasa` block. `-k Dava 1 -k Kadira 1 --samasa --dvandva` → धवखदिरौ;
  `--dvandva --samahara` → पाणिपादम्; `-k rAma 1 -k rAma 1 --samasa --ekasesa` → रामौ.
- **Composer API** (`ui/app.py`): `_apply_dvandva` / `_apply_ekasesa`; `run_karaka` +
  `/api/karaka` gained `samasa_type` (`"dvandva"`/`"ekasesa"`) + `samahara`; the compound-view
  `type` annotation now recognises `dvandva` / `ekaSeza_Sizyate`. Verified via the Flask test
  client (धवखदिरौ / पाणिपादम् / रामौ; bad `samasa_type` → 400; bahuvrīhi/tatpuruṣa unregressed).
- **Frontend** (`ui/templates/karaka.html`): a **dvandva / ekaśeṣa `<select>`** + a **samāhāra
  checkbox**, sent in the `/api/karaka` body.
- **Smoke tests:** `test_cli_dvandva` (2 cases) in `test_samasa_dvandva.py`, `test_cli_ekasesa`
  in `test_ekasesa.py`.

#### Original plan (as-built above supersedes)

- `cmd_line.py`: `--dvandva` (sets `?dvandva_vivakza` on the `--samasa` members, reusing
  the `sandhi = True` adjacency the samāsa path already forces, `cmd_line.py:543`) with
  an optional `--samahara`; `--ekasesa` (sets `?ekaSeza_vivakza`); `--aluk` is **not** a
  user flag — aluk is rule-decided from the pūrva's vibhakti + lexical class, so nothing
  is needed beyond the existing `-k <stem> <vibhakti>` path. Mirror `prepare_bahuvrihi`
  (`cmd_line.py:57`) with `prepare_dvandva` / `prepare_ekasesa`.
- `ui/app.py` `/api/karaka` + `ui/templates/karaka.html`: samāsa-type values for dvandva
  (+ samāhāra) and ekaśeṣa, following `_apply_bahuvrihi`; the compound `surface` block
  must show the **derived** vacana. Add presets for the marquee forms (धवखदिरौ,
  पाणिपादम्, आत्मनेपदम्, युधिष्ठिरः).
- Smoke: `-k Dava 1 -k Kadira 1 --samasa --dvandva` → धवखदिरौ;
  `-k stoka 1 v5 -k mukta 1 --samasa` → स्तोकान्मुक्तः.

---

## 4. Test strategy

Follow the bahuvrīhi pattern (`test/test_samasa_bahuvrihi.py` + `test/samasa_list.py`),
three assertion levels per case — **structure** (member tags; for ekaśeṣa, that the
elided member is *gone* from the branch; for aluk, that the pūrva still **has** its
sup), **fired trace** (expected ids in `karaka_log`), **surface** (full pipeline).
Per phase:
- D0: a **vacana sweep** — 2 members → dual, 3 → plural — plus a vibhakti sweep.
- D1: samāhāra cases assert napuṁsaka **singular** regardless of member genders.
- D2: **reversed input** in every case (the whole point of the phase).
- E0/E1: assert the branch has exactly **one** pada left, in the summed vacana.
- S2: assert the prohibition against a **positive control** from the already-landed
  samāsānta sets (i.e. that उपशरदम् etc. still take their affix).
- A0–A2: assert the retained sup in the surface, and keep a **negative case** per rule
  (निस्तोकः, ब्राह्मणकुलम्, समस्थः, मूर्धशिखः) proving the aluk does *not* over-fire.

New files `test/test_samasa_dvandva.py`, `test/test_ekasesa.py`,
`test/test_samasanta.py`, `test/test_samasa_aluk.py`; cases in `test/samasa_list.py`.
The dvandva driver takes a **`members` list**, not a purva/uttara pair. Hand-built cases
need a `semantic_*` sense on the pūrva where junction sandhi matters (see
`project_samasa_semantic_pada_gotcha`) — this is **mandatory** for every aluk case.

**How to run** (per `MEMORY.md`):
```bash
cd /Users/karthik/personal_projects/sanskrit_parser/sanskrit_parser/generator/test
PYTHONPATH=/Users/karthik/personal_projects/sanskrit_parser \
  /Users/karthik/venvs/sanskrit/bin/pytest -n 8 --dist worksteal
```

---

## 5. Verification (end-to-end)

1. **Per-phase pytest** — the new files green, then the **full generator suite**
   (~8,200 items, ~7.5 min at `-n 8`) with zero regressions. The four highest-risk
   changes each get a full-suite run **immediately**, not at phase end: the two-sweep
   restructuring of `_samasa_prepass_branch` (D2), the **2.4.71 `?!aluk` guard** (A0 —
   every samāsa test in the repo goes through 2.4.71), the 2.4.26 widening (D0), and the
   S2 prohibitions (which target rules that are already landed and green).
2. **CLI smoke** — `--samasa --dvandva` on धव/खदिर → धवखदिरौ; `हर हरि` → हरिहरौ;
   `--samahara` on पाणि/पाद → पाणिपादम्; `--ekasesa` on राम/राम → रामौ;
   `-k stoka 1 v5 -k mukta 1 --samasa` → स्तोकान्मुक्तः; `-k Atman 1 v4 -k pada 1
   --samasa` → आत्मनेपदम्.
3. **UI** — `/api/karaka` renders the dvandva / ekaśeṣa / aluk `compounds` block;
   verify via the Flask test client and confirm उपकृष्णम् / राजपुरुषः / पीताम्बरः are
   unregressed.
4. **Status doc** — after each phase update `generator_status.md`: Implemented rows for
   every landed sūtra (dual-numbered), Skipped rows carrying the *precise* blocker,
   Summary counts, and a 1–3 sentence Last/Next header that **replaces** (does not stack
   on) the previous one — per `feedback_status_doc_concise`. Flip the four deferral rows
   this plan clears (`:770` 2.2.30, `:774` 6.3.2, `:778` 2.4.30/2.4.31) rather than
   adding new rows beside them.
5. **Prakaraṇa audit** (per `project_prakarana_audit`) — at the end, enumerate SK901–984
   and confirm every skn is implemented or in an explicit Skipped row. Target: 0
   unaccounted across all four prakaraṇas.
6. The plan doc itself lands as
   `sanskrit_parser/generator/samasa_completion_plan.md` at phase D0, with an as-built
   §2a section (the bahuvrīhi doc's most useful part) updated each phase.

---

## 6. Deliverables

- Dvandva, ekaśeṣa, sarvasamāsānta and aluk rule blocks in `sutras_antaranga.yaml`.
- **M1** derived vacana (1.4.21/1.4.22 scoped to these windows, riding `_swap_sups`).
- **M2** `_commit_purvanipata` + two-sweep `_samasa_prepass_branch` + the
  `purvanipata: true` rule class — i.e. **2.2.30 implemented**.
- **M3** `_commit_ekasesa` member elision.
- **M4** the `?!aluk` carve-out on 2.4.71 (+ the `?swap_viBakti` mutual guard).
- `$$is_Gi_stem`, `$$is_ajady_adanta`, `$$alpActara`, `$$sarUpa` in `paribhasha.py`;
  the 2-arg parity fix in `Sutra.evalConditionDetail`.
- Four new test files + cases in `test/samasa_list.py`; new stems in `pratipadika.py`.
- CLI `--dvandva` / `--samahara` / `--ekasesa` + composer + `karaka.html` presets.
- `generator/samasa_completion_plan.md` + `generator_status.md` rows.

**Methodological note carried over from bahuvrīhi:** five of its six deferrals rested on
a *plausible but wrong* diagnosis. When something here looks blocked on deep machinery,
**verify the blocker by minimal reproduction before recording it** — a stale tag mimics
a missing engine capability very convincingly. (Two of this plan's four target
deferrals, 6.3.2 and 2.4.30, come with a stated blocker; check each is real before
building to it.)
