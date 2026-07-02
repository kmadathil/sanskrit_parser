# Tatpuruṣa-samāsa Implementation Plan (SK 684–828)

## Context

The generator has completed the **avyayībhāva** samāsa (SK 647–683) on branch
`claude/samasa-avyayibhava-s0-s1a`. That work built a reusable **samāsa pre-pass**
(`AntarangaPrakriya._samasa_prepass`, `bahiranga: -1`) that runs after the kāraka
pre-pass + sup-insertion, scans adjacent `(pūrva | uttara)` member windows, and
assigns the samāsa saṁjñā / member-role / type tags. The next samāsa type in SK order
is **tatpuruṣa** (SK 684 onwards). This plan covers the full tatpuruṣa prakaraṇa —
the six vibhakti-tatpuruṣas, karmadhāraya, dvigu, nañ, prādi/gati, upapada,
samāsānta, and the gender/vacana rules — as parallel-worktree phases, mirroring the
`karaka_plan.md` (K0–K7) and avyayībhāva (S0–S4) structure.

**Outcome:** a user can compose a tatpuruṣa (e.g. कृष्णश्रितः, राजपुरुषः, नीलोत्पलम्,
पञ्चगवम्, अब्राह्मणः) and the generator derives the surface form — crucially, the
compound **declines normally in the uttara's gender**, not as an indeclinable.

---

## 1. Why tatpuruṣa is architecturally different from avyayībhāva

Avyayībhāva turns the whole compound into an **indeclinable** (1.1.41 avyaya, 2.4.18
napuṁsaka, 2.4.82/83 → invariant अम्). Tatpuruṣa does the opposite: the compound
**retains the uttara's sup and declines normally**, taking the **uttara-pada's
gender** (2.4.26 परवल्लिङ्गम्). So the ONE genuinely new mechanism is gender
inheritance + retaining the uttara sup; almost everything else is reuse.

**Reused as-is (no engine change):**
- The samāsa pre-pass spine: `_samasa_prepass`, `_samasa_prepass_branch`,
  `_samasa_window_fixpoint`, member detection (`_is_samasa_member`), the
  `?samAsa_vivakza` intent gate (`antaranga_prakriya.py`).
- Member-role tagging pattern: pūrva → `?samAsaPurva`, uttara → `?samAsa` + a
  type tag (here `?tatpuruza` instead of `?avyayIBAva`).
- **2.4.71** सुपो धातुप्रातिपदिकयोः — pūrva member's internal sup luks (already used
  for the noun-pūrva avyayībhāva शाकप्रति; fires on `?samAsaPurva`).
- **1.2.43** प्रथमानिर्दिष्टं समास उपसर्जनम् — upasarjana tagging in the pre-pass.
- Vibhakti-consume mechanism: require `?viBakti_N` on a member, set `?swap_viBakti`,
  `_swap_sups` post-pass replaces the sup (as 2.1.12/13 consume pañcamī).
- `?samasanta_TaC` + `_insert_samasanta` post-pass for samāsānta affixes.
- The `join_objects` Tier-3 tag propagation through the pūrva+uttara merge.

**New (this plan):**
- **2.4.26** परवल्लिङ्गं द्वन्द्वतत्पुरुषयोः — a pre-pass rule setting the compound's
  gender = uttara's gender (`orp` inherits uttara liṅga; the compound then declines
  via the retained uttara sup). This replaces the avyaya/napuṁsaka path.
- The `?tatpuruza` type tag + its saṁjñā (2.1.22) and the six vibhakti-vidhi rules.
- Do **not** tag the uttara `?avyaya`/`?napum`; the uttara sup is retained and inflects.

**Explicitly still deferred: 2.2.30 physical pūrva-nipāta.** In every tatpuruṣa the
upasarjana (the case-marked / viśeṣaṇa member, prathamā-nirdiṣṭa in the sūtra) is
already the **pūrva** by input order, so no member reordering is needed — exactly as
in avyayībhāva. 2.2.30 physical reorder lands only when bahuvrīhi/dvandva need it.

---

## 2. Scope map (SK 684–828)

| Block | SK / sūtra | Phase |
|---|---|---|
| tatpuruṣa saṁjñā, dvigu saṁjñā | 684 (2.1.22), 685 (2.1.23) | T0 |
| **dvitīyā** श्रितातीत… | 686–691 (2.1.24–29) | T0 |
| **tṛtīyā** तत्कृतार्थेन… | 692–697 (2.1.30–35) | T1 |
| **caturthī** तदर्थ… | 698 (2.1.36) | T1 |
| **pañcamī** भयेन, अपेत… | 699–701 (2.1.37–39) | T1 |
| **ṣaṣṭhī** (राजपुरुष) + याजकादि | 702–716 (2.2.8–17, 2.2.1–5) | T1 |
| **saptamī** शौण्ड… | 717–725 (2.1.40–48) | T1 |
| **karmadhāraya** (समानाधिकरण) | 726, 736 (2.1.49, 2.1.57), 745 (1.2.42), 746 (6.3.42 puṃvad), 751 (2.2.38 kaḍārāḥ) | T2 |
| **dvigu** (संख्यापूर्व, समाहार) | 727–731 (2.1.50–52, 5.4.92, 2.4.1) | T2 |
| **nañ**-tatpuruṣa | 756 (2.2.6), 757–760 (6.3.73–77) | T3 |
| **prādi / gati / upapada** | 761 (2.2.18), 762–780 (gati 1.4.61–79), 781–785 (upapada 3.1.92, 2.2.19–22) | T4 |
| **samāsānta** (ṬaC/aC/ṭac) | 786–811 (5.4.86–105, 6.3.46–49) | T5 |
| **gender / vacana** | 812–828 (2.4.19–31, incl. 2.4.26 done in T0) | T-liṅga |
| **UI + CLI** | — | T-UI |

karmadhāraya, dvigu, nañ, prādi and samāsānta phases are largely independent and can
run in parallel worktrees once **T0** is merged. T-liṅga and T-UI can run any time
after T0.

**How to run this plan:** each phase below ends with a self-contained *Session
prompt*. Start a fresh worktree session (the usual parallel-session workflow; merge
with `/gen-merge`) and paste the phase prompt. **Phase T0 must complete and merge
first**; T1–T5, T-liṅga and T-UI are then largely independent and can run in parallel
worktrees. When spawning worktree-isolated background agents, pin the base branch
(the T0 tip) and forbid git surgery — merge prerequisites into the base first.

---

## 3. Phases

### Phase T0 — Spine + tatpuruṣa saṁjñā + dvitīyā (proof of concept)

The foundational slice that proves the **normally-declining compound** path.

- **2.1.22 तत्पुरुषः** (SK684): pre-pass saṁjñā. Fused with the first vidhi (2.1.24):
  sets `?samAsaPurva` on the pūrva, `?samAsa` + `?tatpuruza` on the uttara.
- **2.1.24 द्वितीया श्रितातीत…** (SK686): the pūrva carries `?viBakti_2` and the uttara
  is one of {श्रित, अतीत, पतित, गत, अत्यस्त, प्राप्त, आपन्न}. Model the uttara list as a
  `?srita_gaRa`/lexical `=Srita`-style tag (analogous to the avyaya-sense tags in
  2.1.6). The rule consumes the pūrva's dvitīyā (`+swap_viBakti`, `_swap_sups` drops
  it since 2.4.71 luks the pūrva sup anyway).
- **2.4.71** (reuse): pūrva sup luks → कृष्ण (no am).
- **2.4.26 परवल्लिङ्गम्** (NEW, pre-pass `bahiranga: -1`): condition `rp: ?tatpuruza`;
  set the compound gender from the uttara. Do **not** tag `?avyaya`/`?napum`. The
  uttara's own sup is retained → the compound declines like the uttara stem.
- **1.2.43** upasarjana (reuse) → pūrva `?upasarjana`.
- **Test-composer note:** like the avyayībhāva tests supplied the semantic sense
  directly, T0 tests supply `?viBakti_2` on the pūrva and the uttara-class tag
  directly, decoupling from full kṛdanta-kāraka coverage.
- **Surface goal:** `कृष्ण(acc) + श्रित` → **कृष्णश्रितः**, declining masculine a-stem
  (कृष्णश्रितः / कृष्णश्रितौ / कृष्णश्रिताः …). A full vibhakti sweep validates that the
  compound inflects normally (contrast avyayībhāva's invariant अम्).

**Files:** `sutras_antaranga.yaml` (new tatpuruṣa block after the avyayībhāva block,
~line 9793); possibly a small `_samasa_prepass` tweak so a non-avyaya uttara keeps its
sup (verify the current pre-pass does not force luk); `test/samasa_list.py` +
`test/test_samasa_tatpurusha.py` (new, modeled on `test_samasa_avyayibhava.py`'s
three assertion levels: structure / fired-trace / surface).

**T0 must complete and merge before T1–T5.**

**Session prompt:**
```
Read sanskrit_parser/generator/tatpuruza_plan.md (§1–§2, Phase T0) and skim the
avyayībhāva samāsa block already in sutras_antaranga.yaml (~line 9303–9793) plus
_samasa_prepass in antaranga_prakriya.py. Implement the tatpuruṣa foundation — a
compound that DECLINES NORMALLY in the uttara's gender (the opposite of
avyayībhāva's invariant अम्). (1) sutras_antaranga.yaml: add a new tatpuruṣa block
of bahiranga: -1 pre-pass rules after the avyayībhāva block. 2.1.22/2.1.24 (fused):
condition lp = (?viBakti_2, ?!samAsaPurva), rp = (?srita_gaRa uttara-class,
?!samAsa); update olp +samAsaPurva, orp +samAsa +tatpuruza; consume the pūrva
dvitīyā via +swap_viBakti (the pūrva sup luks by 2.4.71 anyway). Add 1.2.43
upasarjana (reuse pattern). NEW rule 2.4.26 परवल्लिङ्गम् (bahiranga: -1, condition
rp ?tatpuruza): set the compound gender from the uttara; do NOT tag ?avyaya/?napum
— the uttara sup is retained and inflects. (2) antaranga_prakriya.py: verify the
samāsa pre-pass leaves a non-avyaya uttara's sup intact (no forced luk); add a
minimal tweak only if it currently luks. (3) A ?srita_gaRa tag (श्रित/अतीत/पतित/गत/
अत्यस्त/प्राप्त/आपन्न) — model like the avyaya-sense tags; the test composer supplies
?viBakti_2 on the pūrva and ?srita_gaRa on the uttara directly (decoupled from
kṛdanta-kāraka coverage). (4) test/test_samasa_tatpurusha.py (new, model on
test_samasa_avyayibhava.py's three levels: structure / fired-trace / surface) +
tatpuruṣa cases in test/samasa_list.py. Surface goal कृष्णश्रितः with a full vibhakti
sweep proving normal masculine a-stem declension (कृष्णश्रितः/कृष्णश्रितौ/कृष्णश्रिताः …).
Full generator suite green (pytest -n 6 from generator/test), no avyayībhāva/kāraka
regressions. Update generator_status.md.
```

### Phase T1 — Remaining vibhakti-tatpuruṣas

Each vibhakti branch is the same shape as T0's dvitīyā: pūrva carries `?viBakti_N`,
uttara matches a semantic/lexical list, → `?samAsaPurva` / `?samAsa` + `?tatpuruza`,
2.4.71 luks the pūrva sup, 2.4.26 sets gender, compound declines.

- **tṛtīyā** 2.1.30–35 (शङ्कुलाखण्डः, मासपूर्वः; guṇavacana / pūrvasadṛśa senses).
- **caturthī** 2.1.36 (यूपदारु, कुण्डलहिरण्यम्; तदर्थ/हित/सुख/रक्षित).
- **pañcamī** 2.1.37–39 (चोरभयम्, स्वर्गपतितः; भय, अपेत/अपोढ…).
- **ṣaṣṭhī** 2.2.8–11 + 2.2.1–5 (**राजपुरुषः** — the canonical tatpuruṣa; पूर्वकाय via
  2.2.1 pūrvāparādharottaram / एकदेशी). This is the highest-value branch.
- **saptamī** 2.1.40–48 (अक्षशौण्डः, सिद्ধसंस्कृतम्; शौण्ड, सिद्ध/शुष्क/पक्व…).

Add per-branch test cases. Each branch is an independent worktree off the T0 tip.

**Session prompt:**
```
Read sanskrit_parser/generator/tatpuruza_plan.md (§1–§2, Phase T1); the T0 tatpuruṣa
foundation (saṁjñā + dvitīyā + 2.4.26 paravalliṅga) is already merged — reuse its
exact shape. Implement the remaining five vibhakti-tatpuruṣa branches as bahiranga:
-1 pre-pass rules in sutras_antaranga.yaml, each: pūrva carries ?viBakti_N +
?!samAsaPurva, uttara matches a semantic/lexical uttara-class, → +samAsaPurva /
+samAsa +tatpuruza, consume the pūrva vibhakti (+swap_viBakti), 2.4.71 luks the
pūrva sup, 2.4.26 sets gender. Branches: tṛtīyā 2.1.30–35, caturthī 2.1.36, pañcamī
2.1.37–39, ṣaṣṭhī 2.2.8–11 (+ 2.2.1–5 pūrvāpara/ekadeśī — राजपुरुषः is the canonical
high-value case), saptamī 2.1.40–48. Add the uttara-class tags (guṇavacana /
भय / शौण्ड / सिद्ध-gaṇa …) as the composer supplies them directly. Test cases into
test/samasa_list.py + test_samasa_tatpurusha.py: राजपुरुषः, धान्यार्थः, चोरभयम्,
अक्षशौण्डः, each with a vibhakti sweep. (These five branches are independent and may
be split into separate parallel worktrees; ṣaṣṭhī is the priority.) Full suite green.
Update generator_status.md.
```

### Phase T2 — Karmadhāraya + dvigu

- **karmadhāraya** (samānādhikaraṇa tatpuruṣa, both members prathamā, one referent):
  - **1.2.42** तत्पुरुषः समानाधिकरणः कर्मधारयः (SK745): saṁjñā — when both members
    share the same case/referent (`?viBakti_1` on both, `?samAsa_vivakza`), tag
    `?karmaDAraya` (a `?tatpuruza` sub-tag). eka-vibhakti 1.2.44 (reuse).
  - **2.1.57** विशेषणं विशेष्येण बहुलम् (SK736): विशेषण-pūrva → नीलोत्पलम्, कृष्णसर्पः.
  - **2.1.49** पूर्वकाल… (SK726): स्नातानुलिप्तः (pūrvakāla kriyā).
  - **6.3.42** पुंवद्भाव (SK746): a feminine viśeṣaṇa pūrva takes its masculine form in
    karmadhāraya (कल्याणीप्रिया → कल्याणप्रियः). Pre-pass tag on the pūrva.
  - **2.2.38** कडाराः कर्मधारये (SK751): the kaḍāra-gaṇa optionally pūrva.
- **dvigu** (numeral-led, saṁjñā via 2.1.23 द्विगुश्च):
  - **2.1.52** संख्यापूर्वो द्विगुः (SK730): saṅkhyā-pūrva tatpuruṣa → `?dvigu` (the tag
    already exists — set by the fake test composer for the SK479 ṅīp path; this phase
    sets it via real compound formation).
  - **2.4.1** द्विगुरेकवचनम् (SK731): a **samāhāra** dvigu is napuṁsaka singular
    (पञ्चगवम्, त्रिभुवनम्). Reuse the `?napum` + ekavacana machinery.
  - **5.4.92** गोरतद्धितलुकि (SK729): go-final dvigu samāsānta (पञ्चगवम्, via TaC path).
  - Connect to the existing 4.1.21 (SK479 ṅīp) so त्रिलोकी etc. derive from a **real**
    dvigu instead of the `in_context(in_compound(...), "dvigu")` test shim.

**Session prompt:**
```
Read sanskrit_parser/generator/tatpuruza_plan.md (§1–§2, Phase T2); the T0 tatpuruṣa
foundation is already merged. Implement karmadhāraya and dvigu as bahiranga: -1
pre-pass rules in sutras_antaranga.yaml. KARMADHĀRAYA (samānādhikaraṇa tatpuruṣa,
both members prathamā, one referent): 1.2.42 saṁjñā — both members ?viBakti_1 +
?samAsa_vivakza → tag ?karmaDAraya (a ?tatpuruza sub-tag), eka-vibhakti 1.2.44
(reuse); 2.1.57 विशेषणं विशेष्येण (विशेषण-pūrva → नीलोत्पलम्, कृष्णसर्पः); 2.1.49
पूर्वकाल (स्नातानुलिप्तः); 6.3.42 puṃvadbhāva (a fem viśeṣaṇa pūrva → masculine form,
कल्याणप्रियः — pre-pass tag on the pūrva); 2.2.38 कडाराः optional-pūrva. DVIGU
(numeral-led, 2.1.23 saṁjñā): 2.1.52 संख्यापूर्वो द्विगुः → set ?dvigu (tag already
exists from the SK479 ṅīp path — here set it via real compound formation); 2.4.1
द्विगुरेकवचनम् (samāhāra dvigu → napuṁsaka singular, पञ्चगवम्/त्रिभुवनम् — reuse ?napum
+ ekavacana); 5.4.92 गोरतद्धितलुकि (go-final samāsānta, via the ?samasanta_TaC path).
Wire the existing 4.1.21 SK479 ṅīp so त्रिलोकी derives from a real dvigu, not the
in_context(in_compound(...),"dvigu") test shim. Cases: नीलोत्पलम्, कृष्णसर्पः,
पञ्चगवम्, त्रिभुवनम् into test/samasa_list.py + test_samasa_tatpurusha.py. Full suite
green (watch the existing dvigu ṅīp tests त्रिलोकी/त्रिफला/पञ्चाश्वी stay green).
Update generator_status.md.
```

### Phase T3 — Nañ-tatpuruṣa

Well-bounded, semi-independent. The nañ (न) is pūrva.
- **2.2.6 नञ्** (SK756): न + noun → tatpuruṣa; pūrva `?samAsaPurva` + `?naY`.
- **6.3.73 नलोपो नञः** (SK757): न → अ before a consonant → अब्राह्मणः.
- **6.3.74 तस्मान्नुडचि** (SK758): न → अन् before a vowel (nuṬ augment) → अनश्वः, अनजः.
- **6.3.75 / 6.3.77** exceptions (नभ्राट्…, नगः) — implement the prakṛtibhāva list; can
  be a stretch goal.

These are char-window rules (`l`/`r`/`lc`/`rc`) on the नञ् pūrva, keyed by `?naY`;
they can live in the main scan, gated on `?samAsa`.

**Session prompt:**
```
Read sanskrit_parser/generator/tatpuruza_plan.md (§1–§2, Phase T3); the T0 tatpuruṣa
foundation is already merged. Implement the nañ-tatpuruṣa (the negative न is pūrva).
(1) A pre-pass rule 2.2.6 नञ् (bahiranga: -1): the नञ् pūrva element (tag ?naY) +
noun → +samAsaPurva +naY on the pūrva, +samAsa +tatpuruza on the uttara; reuse
2.4.26 for gender. (2) Main-scan char-window rules gated on ?samAsa + ?naY:
6.3.73 नलोपो नञः (न → अ before a consonant → अब्राह्मणः) and 6.3.74 तस्मान्नुडचि (न →
अन् before a vowel via nuṬ augment → अनश्वः, अनजः). (3) Stretch: 6.3.75/6.3.77
prakṛtibhāva exceptions (नभ्राट्…, नगः) as a lexical list — defer with a Skipped row
if not reached. Add न as an avyaya/nipāta pūrva element if not present. Cases:
अब्राह्मणः, अनश्वः, अनजः into test/samasa_list.py + test_samasa_tatpurusha.py, with a
vibhakti sweep. Full suite green. Update generator_status.md.
```

### Phase T4 — Prādi / gati / upapada (partial expected)

- **2.2.18 कुगतिप्रादयः** (SK761): pra-ādi / ku / gati + noun → tatpuruṣa (प्राचार्यः,
  कुपुरुषः, अतिमालः). Prādi-pūrva tagging.
- **gati saṁjñā** 1.4.61–79 (SK762–780): ऊर्यादि, अच्छ, अस्तं etc. — the gati class that
  feeds 2.2.18. Implement the core (ऊर्यादि/च्वि, पुरस्, अस्तम्); the long tail is a
  stretch goal.
- **upapada** 2.2.19 उपपदमतिङ् + 3.1.92 (SK781–785): **defer most** — upapada
  compounds need the kṛt-pratyaya machinery (कुम्भकारः = कुम्भ + √कृ + अण्), out of the
  current samāsa scope. Note as a dependency, implement only the trivial cases if any.

**Session prompt:**
```
Read sanskrit_parser/generator/tatpuruza_plan.md (§1–§2, Phase T4); the T0 tatpuruṣa
foundation is already merged. Implement prādi/gati-tatpuruṣa (a partial phase is
expected). (1) 2.2.18 कुगतिप्रादयः as a bahiranga: -1 pre-pass rule: pra-ādi / ku /
gati pūrva + noun → +samAsaPurva +tatpuruza; reuse 2.4.26 for gender. Add the prādi
particles + ku to the pūrva-element vocabulary (avyaya.py / pratipadika as
appropriate). (2) gati saṁjñā 1.4.61–79 — implement the CORE that feeds 2.2.18
(ऊर्यादि/च्वि 1.4.61, पुरस् 1.4.67, अस्तम् 1.4.68); defer the long tail (1.4.66,
1.4.70–79) with a Skipped row. (3) upapada 2.2.19/3.1.92: DEFER — upapada compounds
need kṛt-pratyaya machinery (कुम्भकारः = कुम्भ+√कृ+अण्) not yet in samāsa scope;
record the dependency, implement only trivial cases if any surface without kṛt.
Cases: प्राचार्यः, कुपुरुषः, अतिमालः into test/samasa_list.py +
test_samasa_tatpurusha.py. Full suite green. Update generator_status.md with the
deferrals.
```

### Phase T5 — Samāsānta (tatpuruṣa)

Rule-driven via the proven `?samasanta_TaC` + `_insert_samasanta` path; each rule is a
pre-pass rule setting the marker on the qualifying uttara.
- **5.4.91 राजाहःसखिभ्यष्टच्** (SK788): rājan/ahar/sakhi-final tatpuruṣa → ṬaC
  (परमराजः → परमराज+अ). **5.4.86** अङ्गुलि, **5.4.87** ahar (द्व्यहः), **5.4.94** an-final
  (अक्ष्णः), **5.4.101** khārī, etc.
- **6.3.46 आन्महतः…** (SK807): mahat-pūrva → महा (महाराजः).
- Add cases; each affix is one pre-pass rule + reuse of `_insert_samasanta`.

**Session prompt:**
```
Read sanskrit_parser/generator/tatpuruza_plan.md (§1–§2, Phase T5); the T0 tatpuruṣa
foundation is already merged. Implement tatpuruṣa samāsānta affixes, rule-driven via
the proven ?samasanta_TaC + _insert_samasanta path (same as avyayībhāva 5.4.107–112):
each rule is a bahiranga: -1 pre-pass rule that sets ?samasanta_TaC on the qualifying
uttara, and _insert_samasanta does the structural insertion. Rules: 5.4.91
राजाहःसखिभ्यष्टच् (rājan/ahar/sakhi-final → ṬaC, परमराजः), 5.4.86 अङ्गुलि, 5.4.87 ahar
(द्व्यहः), 5.4.94 an-final (अक्ष्णः), 5.4.101 khārī. Plus 6.3.46 आन्महतः (mahat-pūrva
→ महा, महाराजः) as a pre-pass pūrva-substitution rule. Cases: परमराजः, महाराजः,
द्व्यहः into test/samasa_list.py + test_samasa_tatpurusha.py, with a vibhakti sweep.
Full suite green (watch the avyayībhāva samāsānta tests stay green). Update
generator_status.md.
```

### Phase T-liṅga — Gender / vacana rules

2.4.26 परवल्लिङ्गम् is done in T0; this phase adds the exceptions:
- **2.4.19 तत्पुरुषोऽनञ्कर्मधारयः** (SK822): a non-nañ, non-karmadhāraya tatpuruṣa in
  saṃjñā-domain is napuṁsaka (सुराजन् → सुराजम्-type saṃjñā cases).
- **2.4.29 रात्राह्नाहाः पुंसि** (SK814): rātra/ahna/aha-final → masculine.
- **2.4.30 अपथं नपुंसकम्**, **2.4.31 अर्धर्चाः पुंसि च** (SK815–816).
Each is a pre-pass gender-override rule keyed by the uttara stem-class.

**Session prompt:**
```
Read sanskrit_parser/generator/tatpuruza_plan.md (§1–§2, Phase T-liṅga); the T0
tatpuruṣa foundation (incl. 2.4.26 paravalliṅga) is already merged. Implement the
tatpuruṣa gender/vacana EXCEPTIONS to 2.4.26, as bahiranga: -1 pre-pass
gender-override rules keyed by the uttara stem-class, each overriding 2.4.26:
2.4.19 तत्पुरुषोऽनञ्कर्मधारयः (non-nañ non-karmadhāraya tatpuruṣa in saṃjñā → napuṁsaka),
2.4.29 रात्राह्नाहाः पुंसि (rātra/ahna/aha-final → masculine), 2.4.30 अपथं नपुंसकम्,
2.4.31 अर्धर्चाः पुंसि च. Add uttara stem-class tags as needed. Cases exercising each
override into test/samasa_list.py + test_samasa_tatpurusha.py, confirming the final
declension follows the overridden gender. Full suite green. Update
generator_status.md.
```

### Phase T-UI — Vākya Composer + CLI

- **CLI** (`cmd_line.py`): the `--samasa` flag already tags `?samAsa_vivakza`. For
  tatpuruṣa the members carry a vibhakti (from the kāraka args) rather than an avyaya
  sense; verify the pre-pass summary prints the `?tatpuruza`/`?karmaDAraya`/`?dvigu`
  role tags (the print list already includes some of these).
- **UI** (`ui/app.py`, `_build_word` / compound grouping ~lines 1209–1460): the
  `compounds` response block already carries `type` + `surface`. For tatpuruṣa the
  `surface` is now a **full declension paradigm**, not a fixed अम् — ensure the
  composer requests/render the paradigm. Add tatpuruṣa presets to the gallery.
- No engine changes; this phase is a thin extension.

**Session prompt:**
```
Read sanskrit_parser/generator/tatpuruza_plan.md (§1–§2, Phase T-UI); the T0
tatpuruṣa foundation is already merged. Extend the CLI + Vākya Composer for
tatpuruṣa (NO engine changes). (1) cmd_line.py: the --samasa flag already tags
?samAsa_vivakza; verify the pre-pass summary print list includes the
?tatpuruza/?karmaDAraya/?dvigu role tags, and that members carrying a vibhakti (from
the kāraka args) compose correctly. (2) ui/app.py (_build_word / compound grouping
~lines 1209–1460): the compounds response block already carries type + surface — for
tatpuruṣa the surface is now a FULL DECLENSION PARADIGM, not a fixed अम्; ensure the
composer requests and renders the paradigm. Add tatpuruṣa presets to the
/karaka gallery regression view. Smoke: sanskrit_generator -k kfzRa 2 -k Srita 1
--samasa → कृष्णश्रितः, then a vibhakti sweep. Full suite + gallery green. Update
generator_status.md.
```

---

## 4. Test strategy

Follow the avyayībhāva test pattern (`test/test_samasa_avyayibhava.py` +
`test/samasa_list.py`), three assertion levels per case:
1. **Structure** — pūrva has `?samAsaPurva` + `?upasarjana`; uttara has `?samAsa` +
   `?tatpuruza` (+ `?karmaDAraya`/`?dvigu`); the compound gender = uttara gender.
2. **Fired trace** — the expected pre-pass sūtra ids appear in `karaka_log`.
3. **Surface** — full-pipeline output matches the expected form(s); for tatpuruṣa run a
   **vibhakti sweep** to confirm the compound declines (unlike avyayībhāva's invariant अम्).

New files: `test/test_samasa_tatpurusha.py`, tatpuruṣa cases appended to
`test/samasa_list.py`. Canonical cases: कृष्णश्रितः (T0), राजपुरुषः, धान्यार्थः, चोरभयम्,
अक्षशौण्डः (T1), नीलोत्पलम्, पञ्चगवम्, त्रिभुवनम् (T2), अब्राह्मणः, अनश्वः (T3), प्राचार्यः (T4),
परमराजः, महाराजः (T5).

**How to run** (from memory `MEMORY.md`):
```bash
cd <worktree>/sanskrit_parser/generator/test
PYTHONPATH=<worktree_root> /Users/karthik/venvs/sanskrit/bin/pytest -n 6
```
Quick slice while iterating: `pytest test_samasa_tatpurusha.py`.

---

## 5. Verification (end-to-end)

1. **Per-phase pytest** — the new `test_samasa_tatpurusha.py` cases green, plus the
   full generator suite (`pytest -n 6`, ~7900 items) with **no avyayībhāva/kāraka
   regressions** (2.4.26 and the tatpuruṣa saṁjñā must not perturb the avyayībhāva
   pre-pass — they are gated on `?tatpuruza`).
2. **CLI smoke** — e.g. `sanskrit_generator -k kfzRa 2 -k Srita 1 --samasa` → कृष्णश्रितः,
   then sweep vibhaktis to confirm normal declension.
3. **UI** — the Vākya Composer renders the tatpuruṣa `compounds` block with a declining
   paradigm; gallery regression view stays green.
4. **Status doc** — update `generator/generator_status.md`: move the tatpuruṣa SK rows
   (684–828) from the deferred/map section into the implemented section, and update the
   top "Last implemented" / "Next to be implemented" lines. Add the pratipadika/test
   rows as done for avyayībhāva.

---

## 6. Deliverables

- New tatpuruṣa rule block in `sutras_antaranga.yaml` (T0–T5, keyed `bahiranga: -1`).
- New `2.4.26` gender-inheritance pre-pass rule (the one new mechanism).
- `test/test_samasa_tatpurusha.py` + tatpuruṣa cases in `test/samasa_list.py`.
- This doc, `generator/tatpuruza_plan.md`, with per-phase copy-paste **Session
  prompts** (as in `karaka_plan.md`) so phases T1–T5 can be run in parallel worktrees
  and merged with `/gen-merge`.
- `generator_status.md` updates.

**Known deferrals (record in status):** 2.2.30 physical pūrva-nipāta (not needed for
tatpuruṣa); upapada-kṛt compounds (2.2.19/3.1.92, need kṛt machinery); the gati
long-tail (1.4.66–79); nañ prakṛtibhāva exceptions (6.3.75/77) if not reached.
