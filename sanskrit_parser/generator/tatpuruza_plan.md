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

> **STATUS (as-built, last updated 2026-07-21): the tatpuruṣa prakaraṇa is COMPLETE —
> every phase T0–T5 + T-liṅga + T-UI has landed, and the SK 684–828 completeness audit
> (`a548213`) leaves 0 sūtras unaccounted** (each is either implemented or carries an
> explicit Skipped row in `generator_status.md`). Built sequentially on `generator`
> across `8e3dfeb`→`fff452d`; `test/test_samasa_tatpurusha.py` = 96 collected tests over
> 36 cases in `test/samasa_list.py`; full generator suite green (8149 at audit time,
> 8182+ since, with no tatpuruṣa regressions from the bahuvrīhi work).
>
> The Phases (§3) keep their original forward-looking **Session prompts** as a historical
> record — **§2a is the authoritative as-built account** (real mechanisms, deviations,
> engine changes, deferrals). §7 is the T-UI as-built detail.

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

> **AS BUILT — this section's one prediction was wrong.** 2.4.26 turned out **not** to
> need a gender-inheriting mechanism at all: `join_objects` already prefers the LAST
> member's liṅga at the merge (`paninian_object.py` ~L154), so the compound was already
> paravalliṅga. The landed 2.4.26 is therefore a **documenting `?paravalliNga` marker**
> that the T-liṅga exceptions override. The genuinely new engine work turned out to be
> elsewhere: **`_nest_samasa_members`** (a declining compound must be nested into one
> `samasta_pada` or ṇatva never fires — `e3cf09f`), the **2.4.71 stale-`?Ba` clear** (an-stem
> pūrvas: राजन्→राज, `59a66da`), and the **`?samasa_liNga_locked` flag** honoured by
> `join_objects` (`e7c7ece`, then reused by 2.4.29 and by the whole bahuvrīhi prakaraṇa).
> See §2a.

**Explicitly still deferred: 2.2.30 physical pūrva-nipāta.** In every tatpuruṣa the
upasarjana (the case-marked / viśeṣaṇa member, prathamā-nirdiṣṭa in the sūtra) is
already the **pūrva** by input order, so no member reordering is needed — exactly as
in avyayībhāva. 2.2.30 physical reorder lands only when bahuvrīhi/dvandva need it.

---

## 2. Scope map (SK 684–828)

| Block | SK / sūtra | Phase | As-built status |
|---|---|---|---|
| tatpuruṣa saṁjñā | 684 (2.1.22) | T0 | ✅ **fused into 2.1.24** (no standalone rule) |
| dvigu saṁjñā | 685 (2.1.23) | T2 | ✅ **fused into 2.1.52** |
| **dvitīyā** श्रितातीत… | 686–691 (2.1.24–29) | T0 | ✅ all six |
| **tṛtīyā** तत्कृतार्थेन… | 692–697 (2.1.30–35) | T1 | ✅ 2.1.30/31/32; 2.1.33–35 deferred |
| **caturthī** तदर्थ… | 698 (2.1.36) | T1 | ✅ |
| **pañcamī** भयेन, अपेत… | 699–701 (2.1.37–39) | T1 | ✅ all three (2.1.39 luk-form only; 6.3.2 aluk deferred) |
| **ṣaṣṭhī** (राजपुरुष) + याजकादि | 702–716 (2.2.8–17, 2.2.1–5) | T1 | ✅ 2.2.8 + 2.2.1; 2.2.2–5/9–17 deferred (kṛt/aluk) |
| **saptamī** शौण्ड… | 717–725 (2.1.40–48) | T1 | ✅ 2.1.40/41; 2.1.42–48 deferred |
| **karmadhāraya** (समानाधिकरण) | 726, 736 (2.1.49, 2.1.57), 745 (1.2.42), 746 (6.3.42 puṃvad), 751 (2.2.38 kaḍārāḥ) | T2 | ✅ all five; lexical-gaṇa block 2.1.53–72 deferred |
| **dvigu** (संख्यापूर्व, समाहार) | 727–731 (2.1.50–52, 5.4.92, 2.4.1) | T2 | ✅ 2.1.52 (fusing 23/51) + 2.4.1 + 5.4.92; 2.1.50 dik-arm deferred |
| **nañ**-tatpuruṣa | 756 (2.2.6), 757–760 (6.3.73–77) | T3 | ✅ 2.2.6 + 6.3.73/74; 6.3.75/77 prakṛtibhāva deferred |
| **prādi / gati / upapada** | 761 (2.2.18), 762–780 (gati 1.4.61–79), 781–785 (upapada 3.1.92, 2.2.19–22) | T4 | ✅ 2.2.18 (**nitya**) + gati core 1.4.61/67/68; gati tail + upapada deferred |
| **samāsānta** (ṬaC/aC/ṭac) | 786–811 (5.4.86–105, 6.3.46–49) | T5 | ✅ 5.4.91 rājan-arm + 5.4.87 rātri + 6.3.46 महा; per-stem tail deferred |
| **gender / vacana** | 812–828 (2.4.19–31, incl. 2.4.26 done in T0) | T-liṅga | ✅ 2.4.26 (T0) + 2.4.29; 2.4.19/30/31 + saṃjñā-domain 2.4.20–27 deferred |
| **UI + CLI** | — | T-UI | ✅ (see §7) |

**As built, the phases were NOT run in parallel worktrees** — T0→T-UI landed
sequentially on `generator`, each phase building on the previous one's engine fixes
(T1's 2.4.71 `?Ba` clear and `_nest_samasa_members` were prerequisites for T2's dvigu
ṇatva, and T2's `?samasa_liNga_locked` was a prerequisite for T-liṅga's 2.4.29). The
parallel-worktree framing below is historical.

**How to run this plan (historical):** each phase below ends with a self-contained
*Session prompt*. Start a fresh worktree session (the usual parallel-session workflow;
merge with `/gen-merge`) and paste the phase prompt. **Phase T0 must complete and merge
first**; T1–T5, T-liṅga and T-UI are then largely independent and can run in parallel
worktrees. When spawning worktree-isolated background agents, pin the base branch
(the T0 tip) and forbid git surgery — merge prerequisites into the base first.

---

## 2a. Implementation status (as-built, last updated 2026-07-21)

Commits on `generator`, in order: T0 `8e3dfeb` + `26c56b3` (2.1.25–29) + `e34e9bd`
(un-defer स्वयंकृतम्), T1 `59a66da` + `e3cf09f` (nesting fix) + `2b26ac1` (test the
untested T1 rules), T2 `e7c7ece`, T3 `c32a1ee`, T4/T5/T-liṅga/T-UI `229d209`, T4/T5
corrections `24d433d`, completeness audit + SK-numbered labels `a548213`, T-UI as-built
notes `fff452d`.

### Files touched (the whole prakaraṇa)
- `sutras_antaranga.yaml` — the tatpuruṣa rule block (~L9884–10800), appended after the
  avyayībhāva block; **37 rule blocks** (`2.1.24`…`2.4.29`, L9884–10785), nearly all
  `bahiranga: -1` pre-pass rules — the one exception is the gati saṁjñā **1.4.67**, a
  main-scan rule (`bahiranga: 0`) so its `?gati` is live for 8.3.40 पुरस्कृतम् off the
  pre-pass path. The bahuvrīhi blocks were later appended after this one.
- `antaranga_prakriya.py` — `_nest_samasa_members` (new), `_commit_samasa_napum`
  (gender lock), reuse of `_insert_samasanta` / `_swap_sups`.
- `paninian_object.py` — `join_objects` honours `?samasa_liNga_locked`.
- `pratipadika.py` — the uttara-class/gaṇa-tagged stems (śrita-gaṇa, guṇavacana,
  pūrvasadṛśa, tadartha, bhaya, apeta, stoka, śauṇḍa, siddha, dikśabda/ekadeśin,
  kaḍāra, ku/māla, rājan/rātri reuse …).
- `avyaya.py` — the `naY` surface corrected नञ् → **न** (ञ् is an इत्).
- `cmd_line.py`, `ui/app.py`, `ui/templates/karaka.html` — T-UI (§7).
- `test/samasa_list.py` (36 tatpuruṣa cases, labels `T0-…`→`T5-…`),
  `test/test_samasa_tatpurusha.py` (96 collected tests: the case sweep + 12
  vibhakti/gender/ṇatva/gati sweeps).

### Per-phase as-built + deviations from the original plan
| Phase | Done | Real detail / deviation |
|---|---|---|
| **T0** ✅ `8e3dfeb`,`26c56b3`,`e34e9bd` | 2.1.22 (fused) + 2.1.24–29 + 2.4.26 | **No `+swap_viBakti`** — the plan called for consuming the pūrva's dvitīyā via the swap mechanism, but 2.4.71 luks the pūrva sup anyway and the pūrva never surfaces, so the swap was dropped. 2.4.26 landed as a documenting marker (§1 AS BUILT). 2.1.25/27 (svayam/sāmi) are avyaya-pūrvas with **no** vigraha vibhakti; they need a **semantic sense** on the pūrva to stay `?pada` so 8.3.23 म्→anusvāra fires (स्वयंकृतम्/स्वयङ्कृतम्) — first diagnosed here as an "engine gap", then correctly re-diagnosed as a degenerate test input (`e34e9bd`) |
| **T1** ✅ `59a66da`,`e3cf09f`,`2b26ac1` | 2.1.30/31/32, 2.1.36, 2.1.37/38/39, 2.2.8, 2.2.1, 2.1.40/41 | Two **unplanned engine fixes** were required. (a) **2.4.71 stale-`?Ba` clear** (1.1.63 न लुमताङ्गस्य): the vigraha sup had set `?Ba` via 1.4.18, so an an-stem pūrva took 6.4.134 अल्लोपोऽनः (राजन्→राज्ञ्→राक्…) instead of 8.2.7 न-lopa — राजपुरुषः needs the clear. (b) **`_nest_samasa_members`**: the pre-pass only TAGGED members in place, so a flat declining compound never coalesced into one `samasta_pada` and the samānapada ṇatva rules (8.4.1/2, gated `?!merged_pada`) never fired → राजपुरुषेन. Nesting each member span into a sub-list fixed it (राजपुरुषेण, कृष्णपुरुषेण, मासपूर्वेण) — **and retracted an earlier, wrong "fundamental limitation" note**. 2.1.38/39/41 shipped *inert* (no stem carried their class tag) until `2b26ac1` added stems + cases |
| **T2** ✅ `e7c7ece` | 2.1.57, 2.1.49, 1.2.42, 6.3.42, 2.2.38, 2.1.52 (fusing 2.1.23 + 2.1.51's समाहार arm), 2.4.1, 5.4.92 | The plan's "wire 4.1.21 to a real dvigu" **worked** — त्रिलोकी now derives from त्रि+लोक via 2.1.52's `?dvigu` (the `in_context(in_compound(...),"dvigu")` shim stays green alongside). **Unplanned engine fix:** `_commit_samasa_napum` now also sets `?samasa_liNga_locked`, which `join_objects` honours, so the samāsānta `wac`'s hard-coded `?pum` (needed for 2.4.29 द्व्यह्नः) cannot masculinise a समाहार dvigu — पञ्चगवम्, not पञ्चगवः. 6.3.42 puṃvadbhāva is a **saṁjñā marker** (composer supplies the masc कल्याण; the real ṅīp-strip is deferred) — the same model bahuvrīhi B1's 6.3.34 later reused. 1.2.42 correctly skips the ekadeśī पूर्वकायः (`?viBakti_1` pūrva but not samānādhikaraṇa) |
| **T3** ✅ `c32a1ee` | 2.2.6, 6.3.73, 6.3.74 | The plan put 6.3.73/74 in the **main scan**; as built they are **pre-pass member-window xforms** (`bahiranga: -1`, the same (pūrva\|uttara) window 2.2.6 fires in). Doing the नलोप before the main scan means "a"\|ब्राह्मण never meets vowel sandhi, so **no 6.1.101 override is needed**. The नुṭ न् is prepended to the **uttara** (अश्व→नश्व), not left as an "an"-final pūrva — otherwise 8.2.7 re-deletes it (→ आश्वः). अब्राह्मणेन hits the pūrva-only ṇatva gap, so the sweep uses अनश्व |
| **T4** ✅ `229d209`,`24d433d` | 2.2.18 + gati saṁjñā 1.4.61/67/68 | Two corrections after the first cut. (a) **2.2.18 is NITYA, not vibhāṣā** — the initial rule wrongly carried a `?samAsa_vivakza` gate; prādi/gati/ku compounds are aswapada-vigraha, so the gate was dropped and `?nitya` marks the class (प्राचार्यः forms with no vivakṣā), firing off the semantic-sense window trigger like the nitya avyayībhāvas. (b) the gati saṁjñā was initially **faked** by an intrinsic `?gati` tag; `24d433d` made 1.4.61/67/68 **real rules** and removed puras's intrinsic `?gati`, so 1.4.67 is now the genuine source feeding 8.3.40 पुरस्कृतम् |
| **T5** ✅ `229d209`,`24d433d` | 5.4.91 (rājan-arm), 6.3.46, 5.4.87 | 5.4.91 + 6.3.46 landed as planned via `?samasanta_TaC` + `_insert_samasanta`. **5.4.87 रात्रि (not in the original plan's list) was added** in `24d433d` and is what upgraded 2.4.29 from a structure-only rule to a real surface (पुण्यरात्रः, full vibhakti sweep). 6.3.46 is a pre-pass **pūrva-substitution** gated on the *uttara*'s `?samAnADikaraRa` (pinning a genuine karmadhāraya). The plan's 5.4.86/94/101 and the ahar/sakhi arms are **deferred** — see below |
| **T-liṅga** ✅ `229d209`,`24d433d` | 2.4.29 only | Implemented with **no engine change**, by reusing T2's `?samasa_liNga_locked`; gated `?!samAhAra` + `?!samasa_napum` so it cannot clobber a समाहार dvigu (द्व्यहम्/द्विरात्रम्). 2.4.19/30/31 deferred with reasons (below) |
| **T-UI** ✅ `229d209` (notes `fff452d`) | CLI + composer + gallery | The plan's "no engine changes" held, but it **missed two real gaps**: the CLI had no way to set a member's *vigraha* case (→ the new `-k <stem> … vN` token) and the composer's compound-type readout came back empty for every tatpuruṣa until the nested `samasta_pada` was flattened one level. Full detail in §7 |

### Deferrals as built (all carry Skipped rows in `generator_status.md`)
- **2.2.30 physical pūrva-nipāta** — the plan predicted tatpuruṣa would not need it, and
  that **held**: the upasarjana is always the pūrva by input order. It remains the
  blocker for 2.2.38's optional kaḍāra reordering and for the bahuvrīhi word-order rules.
- **T1 long tails** — 2.1.33–35 (kṛtya/anna/bhakṣya), 2.2.2–5 / 2.2.9–11 (ṣaṣṭhī
  extensions), 2.1.42–48 (saptamī), and **6.3.2 पञ्चम्याः स्तोकादिभ्यः** (the aluk form
  स्तोकान्मुक्तः; 2.1.39 currently luks like every other branch → स्तोकमुक्तः).
- **ṣaṣṭhī + kṛt / aluk block** 2.2.12–17, 2.2.7, 2.2.20–22 and **upapada** 2.2.19 /
  3.1.92 — one shared dependency: **kṛt-pratyaya machinery** (कुम्भकारः = कुम्भ+√कृ+अण्).
- **Lexical-gaṇa karmadhāraya** 2.1.53–72 (kutsita/upamāna-vyāghrādi/śreṇyādi/
  mayūravyaṁsakādi …) — per-sūtra gaṇas, low generation value.
- **Gati long tail** 1.4.62–79 — only ऊर्यādi/पुरस्/अस्तम् feed 2.2.18; cvi/ḍāc denominals too.
- **Specialized samāsāntas** 5.4.88–105 (minus 92), 6.3.47–49, 6.3.76, 8.4.7/39 — incl.
  the **5.4.91 ahar/sakhi arms**, which collide with the deliberate `dvyahna`
  न्-retention (6.4.145, SK238/SK789 — द्व्यह्न, not द्व्यह).
- **Gender/vacana** 2.4.19 (inert without saṃjñā tagging — would wrongly neuter ordinary
  masculines like राजपुरुषः), 2.4.30 (needs the pathin अच् 5.4.74), 2.4.31 (अर्धर्चादि stems),
  and the saṃjñā-domain 2.4.20–27 / 1.2.58–63.
- **Nañ prakṛtibhāva** 6.3.75/6.3.77 (नभ्राट्…, नगः) — needs a tagged exception list.
- **Pūrva-only cross-member ṇatva** (चोरात् भयम् → चोरभयेण, त्रिभुवनम्) — **pre-existing**, not
  a tatpuruṣa gap: the CLI `in_compound` path shows the same. Uttara-side / same-segment
  ṇatva works since `e3cf09f`. The bahuvrīhi work later landed a *scoped* cross-compound
  ṇatva (8.4.3 `?saMjYA` gate / 8.4.28 via markers); the general case is still open.

---

## 3. Phases

### Phase T0 — Spine + tatpuruṣa saṁjñā + full dvitīyā block — ✅ DONE (`8e3dfeb`,`26c56b3`,`e34e9bd`; see §2a)

The foundational slice that proves the **normally-declining compound** path.
**Status: implemented** — the whole dvitīyā-tatpuruṣa block SK 684–691 (2.1.22
saṁjñā fused + 2.1.24–29) plus 2.4.26, reusing 1.2.43 / 2.4.71. Derives कृष्णश्रितः
(+ full vibhakti sweep), स्वयंकृतम्/स्वयङ्कृतम्, खट्वारूढः, सामिकृतम्, मासप्रमितः,
मुहूर्तसुखम्. 14 cases in `test/test_samasa_tatpurusha.py`; full suite green. **Test-infra
note:** an avyaya pūrva (svayam/sāmi) needs a **semantic sense** on it — as every
kāraka/CLI-composed word carries (`-w svayam 1` → `semantic_1`) — for the junction
sandhi to fire (it keeps the pūrva `?pada`, so 8.3.23 म्→anusvāra applies →
स्वयंकृतम्/स्वयङ्कृतम्). Hand-built test inputs must include it. The bullets below
describe the 2.1.24 core; 2.1.25–29 follow the same shape (see `generator_status.md`).

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

### Phase T1 — Remaining vibhakti-tatpuruṣas — ✅ DONE (`59a66da`,`e3cf09f`,`2b26ac1`; long tails deferred; see §2a)

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

### Phase T2 — Karmadhāraya + dvigu — ✅ DONE (`e7c7ece`; see §2a)

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

### Phase T3 — Nañ-tatpuruṣa — ✅ DONE (`c32a1ee`; 6.3.75/77 deferred; see §2a)

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

### Phase T4 — Prādi / gati / upapada (partial expected) — ✅ DONE as scoped (`229d209`,`24d433d`; gati tail + upapada deferred; see §2a)

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

### Phase T5 — Samāsānta (tatpuruṣa) — ✅ DONE for 5.4.91 rājan + 5.4.87 + 6.3.46 (`229d209`,`24d433d`); per-stem tail deferred (see §2a)

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

### Phase T-liṅga — Gender / vacana rules — ✅ DONE for 2.4.29 (`229d209`,`24d433d`); 2.4.19/30/31 deferred (see §2a)

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

### Phase T-UI — Vākya Composer + CLI — ✅ DONE (`229d209`; as-built detail in §7)

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

**AS BUILT:** 36 cases in `test/samasa_list.py` (labels `T0-…`→`T5-…`) + 96 collected
tests in `test_samasa_tatpurusha.py` — the case sweep plus 12 dedicated tests: masc /
caturthī / napuṁsaka / ṣaṣṭhī-ṇatva / nañ / prādi / samāsānta / rātri-samāsānta vibhakti
sweeps, the real-dvigu ṅīp त्रिलोकी check, the two gati-saṁjñā checks (1.4.67/1.4.68), and
the 2.4.29 liṅga override. Every case label carries **both** numbers
(`<phase>-<form>-SK<n>-<a.p.n>`, `a548213`) per the dual-numbering convention. Two plan
cases moved: **त्रिभुवनम्** is deferred (cross-member ṇatva → त्रिभुवण) and covered by
त्रिलोकम् instead; **पुण्यरात्रः** was added for 5.4.87/2.4.29. Sweeps deliberately use
ṇatva-safe stems (धान्यार्थ, अनश्व) where the pūrva-only ṇatva gap would otherwise bite.

**How to run** (from memory `MEMORY.md`):
```bash
cd <worktree>/sanskrit_parser/generator/test
PYTHONPATH=<worktree_root> /Users/karthik/venvs/sanskrit/bin/pytest -n 8 --dist worksteal
```
Quick slice while iterating: `pytest test_samasa_tatpurusha.py`.

---

## 5. Verification (end-to-end) — ✅ all four done

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

## 6. Deliverables — ✅ delivered (see §2a for the full as-built account)

- New tatpuruṣa rule block in `sutras_antaranga.yaml` (T0–T5, keyed `bahiranga: -1`)
  — ✅ 36 rule ids, `sutras_antaranga.yaml` ~L9884–10800.
- New `2.4.26` gender-inheritance pre-pass rule (the one new mechanism) — ✅ landed, but
  **as a documenting marker**: `join_objects` was already paravalliṅga (§1 AS BUILT).
  The mechanisms that actually had to be built were `_nest_samasa_members`, the 2.4.71
  `?Ba` clear, and `?samasa_liNga_locked`.
- `test/test_samasa_tatpurusha.py` + tatpuruṣa cases in `test/samasa_list.py` — ✅ 96
  tests / 36 cases.
- This doc, `generator/tatpuruza_plan.md` — ✅; it keeps the per-phase **Session
  prompts** as a historical record (**§2a is the authoritative as-built account**).
  The phases were in the end run **sequentially on `generator`**, not in parallel
  worktrees, because each phase depended on the previous one's engine fixes.
- `generator_status.md` updates — ✅ implemented rows for every landed sūtra + explicit
  grouped Skipped rows; the SK 684–828 completeness audit (`a548213`) leaves **0
  unaccounted**.

**Known deferrals — as built.** The plan's four predicted deferrals all held (2.2.30
physical pūrva-nipāta, still not needed for tatpuruṣa; upapada-kṛt 2.2.19/3.1.92; the
gati long tail; nañ prakṛtibhāva 6.3.75/77). The audit added five more groups —
ṣaṣṭhī+kṛt/aluk (2.2.12–17 etc., same kṛt dependency as upapada), the lexical-gaṇa
karmadhāraya block (2.1.53–72), the per-stem samāsāntas (5.4.88–105 etc., incl. the
5.4.91 ahar/sakhi arms), the saṃjñā-domain gender/vacana rules (2.4.19/30/31,
2.4.20–27, 1.2.58–63), and 6.3.2 aluk. Full list with reasons in §2a; the Skipped rows
in `generator_status.md` are canonical.

---

## 7. Phase T-UI — implementation notes (AS BUILT)

Implemented in commit `229d209` (no engine changes). File:line references are current.

### CLI (`cmd_line.py`)
- **Role-tag display** — the pre-pass summary tag list now prints the tatpuruṣa
  saṁjñās: `"tatpuruza", "karmaDAraya", "naY"` were added alongside
  `avyayIBAva`/`bahuvrIhi`/`dvigu` ([`cmd_line.py:95`](cmd_line.py)).
- **Pūrva vigraha vibhakti (the real gap)** — the original plan assumed "members carry
  a vibhakti from the kāraka args", but the `-k`/`--karaka` action only took
  `<stem> [vacana] [sem…] [pUrva|para]` — no way to set the pūrva's *vigraha* case.
  `CustomActionKaraka` now accepts a **`vN`** token (e.g. `v6`) — or the explicit
  `viBakti_N` — which sets `viBakti_<N>` + `has_viBakti` on that member
  ([`cmd_line.py:321`](cmd_line.py); docstring at `:283–290`, `-k` help at `:461`,
  `--samasa` help at `:471–478`).
- **Dispatch** — `--samasa` still just tags every member `?samAsa_vivakza`; the comment
  at [`cmd_line.py:505`](cmd_line.py) now notes the tatpuruṣa pūrva carries its vigraha
  `viBakti_N` (via `-k … vN`).
- **Smoke (verified):** `-k rAjan 1 v6 -k puruza 1 --samasa` → **राजपुरुषः**;
  `-k kfzRa 1 v2 -k Srita 1 --samasa` → **कृष्णश्रितः**; pre-pass summary shows
  `samAsa, tatpuruza`.

### Composer UI (`ui/app.py`, `ui/templates/karaka.html`)
- **Compound-type readout** — `"tatpuruza"`/`"karmaDAraya"` added to `_SAMASA_ROLE`
  ([`ui/app.py:1407`](ui/app.py)) and to the compound-`type` filter (`:1462`).
- **Nested-member flatten (unplanned fix)** — a *declining* compound nests its members
  into a sub-list (`_nest_samasa_members` → one `samasta_pada`), so the member scan for
  the role tags had to flatten one level ([`ui/app.py:1420–1424`](ui/app.py)); without
  it, `type` came back empty (`[]`) for every tatpuruṣa (avyayībhāva stays flat, so it
  was unaffected). This was NOT in the original T-UI plan — found during verification.
- **Surface** — unchanged: `surface` already collects the full per-group form set by
  splitting the output on the avasāna marker, so the **full declension paradigm renders
  with no surface-computation change** (contrast avyayībhāva's fixed अम्).
- **Preset → spec plumbing** — `toSpec()` now forwards the pūrva's `vibhakti`
  ([`karaka.html:314`](ui/templates/karaka.html)); `_build_word` (`app.py`) already
  consumed a spec `vibhakti`.
- **Gallery presets** — three tatpuruṣa presets added with the pūrva `vibhakti` set
  ([`karaka.html:495–504`](ui/templates/karaka.html)): कृष्णश्रितः (SK686/2.1.24, dvitīyā),
  राजपुरुषः (SK702/2.2.8, ṣaṣṭhī), नीलोत्पलम् (SK736/2.1.57, viśeṣaṇa karmadhāraya).
- **Verified in-browser:** the gallery renders "समासः — TATPURUZA" with the member
  roles (pūrva `samAsaPurva/upasarjana`, uttara `samAsa/tatpuruza`); no console errors.

**Net:** the plan's "thin extension, no engine changes" held — the only real work beyond
tag-list edits was (a) exposing the pūrva vigraha vibhakti on the CLI (`vN`) and in the
composer (`toSpec`), and (b) the nested-member flatten fix for the compound-type readout.
