# समासाश्रयविधिप्रकरणम् (SK 985–1071) — implementation plan

## Context

The generator has finished the entire **samāsa section**: avyayībhāva (SK647–683),
tatpuruṣa (SK684–828), bahuvrīhi (SK829–900), and — as of 2026-07-23 — dvandva,
ekaśeṣa, sarvasamāsānta and aluk (SK188, 901–984, `samasa_completion_plan.md`).
`samasa_completion_plan.md:18` explicitly parked **समासाश्रयविधिप्रकरणम् (SK985–1071)**
as out of scope. This plan picks it up. It is the next prakaraṇa in SK order and the
last one before the taddhita section (SK1072 / 4.1.82 समर्थानां प्रथमाद्वा).

At the time of writing, all 87 sūtras were unimplemented — a grep of `id:` across the
three YAMLs returned zero hits for every Ashtadhyayi id in the range. See the Status
table below for what has landed since.

**What the prakaraṇa is.** Having formed the compound, Pāṇini now mutates its
*members*: the pūrvapada shortens, lengthens, or is replaced outright depending on
what the uttarapada is; the uttarapada's initial `s` becomes `ṣ` and its `n` becomes
`ṇ` under a pūrvapada trigger; and a tail of frozen suṭ-nipātana forms is licensed.
Eight mechanism families, six of which reuse levers that already exist.

**Why now, beyond order.** SK1055 / 8.4.11 प्रातिपदिकान्तनुम्विभक्तिषु च is precisely the
sūtra behind the generator's longest-standing ṇatva deferral — `generator_status.md:838`
("a pūrva-only र/ष trigger reaching the uttara's न-bearing sup (चोरात् भयम् → चोरभयेण)
does not fire") and the त्रिभुवनम् note at `test/samasa_list.py:423`. Phase X6 closes it.

**Decisions taken (user, this session):**
1. **8.4.11 is implemented as nitya**, not as the SK's वा. Modelling the वा literally
   would fork every landed compound whose only r/ṣ sits in the pūrva (राजपुरुषेण →
   also राजपुरुषेन) and would require rewriting the tatpuruṣa/bahuvrīhi/dvandva vibhakti
   sweeps. The unmodelled वा is recorded as a documented deviation + a Skipped row.
2. **Affix depth:** build **त्व** and **मतुप्** as live pratyayas (cheap, reusable, and
   they unlock SK1002/6.3.64 and SK1041–1042/6.3.119–120). Every other affix-only arm
   (घ = तरप्/तमप्, रूपप्, कल्पप्, वलच्, क्विप्-anta) gets an explicit **Skipped row** naming
   the missing affix; the sūtra's uttarapada (compound) arm is still implemented where
   it has one.
3. **Sequential on `generator`**, one phase at a time — as the D/E/S/A phases were done.

**Outcome:** हृल्लेखः, पदाजिः, उदमेघः, सपलाशम्, सज्योतिः, सदृशः, ईदृशः / कीदृशः, अन्यद्रागः,
कदश्वः / काक्षः / कवोष्णम् *(all of the above landed in X1; कापथम् needs 5.4.74 — see the X1
notes)*; ब्राह्मणिगोत्रम्, ग्रामणिपुत्रः, एकक्षीरम्, रेवतिपुत्रः, अजत्वम् / अजात्वम्, इष्टकचितम्,
मालभारि; सत्यङ्कारः, रात्रिञ्चरः *(X2 + X3 landed; ब्राह्मणिचेली would need the चेलट् affix)*;
द्विगुणाकर्णः, कोटरावणम्, अमरावती, ऋषीवहम्, नीकाशः, अष्टापदम्, विश्वानरः, विश्वामित्रः;
अङ्गुलिषङ्गः, भीरुष्ठानम्, ज्योतिष्टोमः, सुषामा, हरिषेणः; प्रवणम्, क्षीरपाणाः, **माषवापेण /
चोरभयेण**; पृषोदरम्, गोष्पदम्, आस्पदम्, आश्चर्यम्, मस्करः, कारस्करः, पारस्करः;
कारीषगन्धीपुत्रः.

---

## Status (last updated 2026-08-03)

| Phase | Sūtras | Status | Landed as |
|---|---|---|---|
| **X1** pūrvapada ādeśa | 30 | **DONE** — 28 implemented, 2 Skipped | `b3847ca`, 45 cases, suite 8363 green |
| **X2** pūrva hrasva (ङी/आप्) + `tva` | 8 | **DONE** — 6 implemented, 2 Skipped | 18 cases; adds `tva_t`, `$$ik_dIrGa_anekAc` |
| **X3** मुम् | 2 | **DONE** — 2 implemented | 5 cases; no new machinery beyond the append xform |
| **X4** pūrva dīrgha + `matup` | 14 | **DONE** — 12 implemented, 2 Skipped | 26 cases; adds `matup` + 8.2.9 |
| **X5** samāsa ṣatva | 6 | **DONE** — 6 implemented | 10 cases; N2 needed no engine work |
| X6 samāsa ṇatva | 9 | pending | — |
| X7 पृषोदरादि + suṭ nipātanas | 15 | pending | — |
| X8 ष्यङ् सम्प्रसारणम् | 3 | pending | — |
| X9 prakaraṇa audit + status | — | pending | — |
| | **87** | **54 done / 33 to go** | |

**Machinery status:** **N2 built in X5 and N3 completed in X4** — N2 needed no engine work,
just `xform: r: str("z")` at the pre-pass junction (`r` is the uttara's first char); N3's
`matup` landed with 8.2.9 मतोर्वः, and the five SK examples of 6.3.119/120 pinned that
sūtra's condition exactly as the plan predicted. **N1 (मुम्) built in X3** — and it needed no engine work at all, just the
append xform `l: l+str("m")`, since 1.1.47 मिदचोऽन्त्यात्परः coincides with appending for a
vowel-final pūrva. **N3's `tva` built in X2** (`tva_t` in `pratyaya.py`), plus one new
paribhāṣā helper the plan did not anticipate, `$$ik_dIrGa_anekAc`. Still to build: N2
(junction ṣatva, X5) and N3's `matup` (X4).

**Recorded deferrals so far** (each also a `generator_status.md` Skipped row): X1 — 6.3.53
(यत् + the तदर्थ/अतदर्थ sense distinction), 6.3.55 (needs the शस् taddhita 5.4.43). X2 —
6.3.44/6.3.45 (every SK example is a तरप् context), and 6.3.61's GENERAL इगन्त form: the
rule is implemented but scoped to an opt-in `?gAlava_hrasva`, because unscoped it undoes
other rules' deliberate dīrghas (6.3.137's केशाकेशि, 6.3.27's अग्नीवरुणौ), breaks its own
अव्ययानाम् vārtika on ऊरीकृतम्, and reaches ङीष्-feminines because `?NI` tagging is
incomplete lexicon-wide. X3 — 6.3.70's vārtika tail (अस्तुङ्कारः, तिमिङ्गिलः, …).

---

## 0. Numbering convention (MANDATORY)

Per the standing dual-numbering rule, **every sūtra reference carries BOTH its SK
number and its Ashtadhyayi id, SK-first** (`SK1055 / 8.4.11`) in all four places: this
doc; the `# <N>:` block comment of each rule in `sutras_antaranga.yaml` (the `id:`
field stays the bare Ashtadhyayi id); every test-case `label`
(e.g. `"X6-mAzavApeRa-SK1055-8.4.11"`); and the `generator_status.md` rows.
`"fired"` lists hold Ashtadhyayi ids — `karaka_log` records those.

---

## 1. Placement: which window does a rule fire at?

This prakaraṇa is almost entirely "change the pūrva, conditioned on the uttara", and
the generator already has **three** placements for that. Choosing wrong is the single
most likely source of lost time, so the rule is:

| Placement | Window seen | Template in repo | Use when |
|---|---|---|---|
| `bahiranga: -1` (samāsa pre-pass) | **(pūrva \| uttara)** | SK926/6.3.29 दिवो द्यावा, `sutras_antaranga.yaml:12823` | The rule reads the **uttara's identity** and must land before sup-luk / declension. **Default for this prakaraṇa.** |
| `bahiranga: 1` (main scan, pre-luk) | (pūrva \| its own sup) | SK849/6.3.82 वोपसर्जनस्य, `:11209` | The rule needs no uttara information (सह → स in a bahuvrīhi). **Cannot be used here** for uttara-keyed rules — the uttara is not in the window. |
| main scan, default bahiranga | (pūrva \| uttara+**sup**) | 6.3.128 विश्वस्य वसुराटोः, `:745` | **Only when the uttara is identified by a TAG.** By the time the main scan reaches this junction the uttara has merged with its sup, so `rp: =X` and `r: <char>` no longer match — 6.3.128 works solely because it keys on `?vasupada`/`?rAj`. X4 and X5 both learned this the hard way; all 17 of their compound rules moved to `bahiranga: -1`. |

The xform vocabulary is already sufficient (`sutra.py:273-311`): `l`/`lc` = last char /
rest of the pūrva, `r`/`rc` = **first** char / rest of the uttara. Whole-stem
substitution is `lc: str("")` + `l: str("newstem")` (SK888/5.4.150 uses the mirror form
on the uttara, `:11778`). Helpers `dirgha`, `hrasva`, `samprasaranam`, `is_ekac`,
`bahvac`, `anekAc_asaMyogapUrva` all live in `paribhasha.py`.

**Known trap** (from the केशाकेशि work): a main-scan rule can find the window is
(pūrva | *sup*) rather than (pūrva | uttara) if 2.4.71 has not yet run — 6.3.137 had to
be moved to the pre-pass for exactly this. When a main-scan placement misfires, move
the rule to `bahiranga: -1` before debugging anything else.

---

## 2. New machinery (only three items)

**(N1) मुम् augment on the pūrva** *(phase X3)* — SK1007/6.3.70 and SK1008/6.3.72 append
`m` to the pūrva (सत्य + कार → सत्यङ्कारः, रात्रि + चर → रात्रिंचरः). Realised as a pre-pass
xform `lc: lc+l`, `l: str("m")`; the ङ्/ं then come free from the landed 8.3.23
मोऽनुस्वारः + 8.4.58 अनुस्वारस्य ययि परसवर्णः. No engine change.

**(N2) Junction ṣatva lever** *(phase X5)* — the uttara's **initial** `s` → `ṣ` under a
named pūrva. This is a plain main-scan rule at the compound junction using
`xform: r: str("z")` — the exact shape of the landed 8.3.59 आदेशप्रत्यययोः
(`sutras_antaranga.yaml:1491`), only with a lexical `lp:` gate instead of the
pratyaya gate. No engine change; ṣṭutva (ज्योतिष्टोमः) then follows from 8.4.41.

**(N3) Two live taddhitas** *(phases X2, X4)* — `tva` (SK1002/6.3.64) and `matup`
(SK1041–1042/6.3.119–120), added to `pratyaya.py`:
- `tva = Pratyaya("tva", other_tags=["svAdi", "tadDita"])` + SK/5.1.119 तस्य भावस्त्वतलौ
  (त्व arm only; तल् deferred). त्व-anta is napuṁsaka.
- `matup = Pratyaya("mat", its=["u~", "p"], other_tags=["svAdi", "tadDita"])` + 5.2.94
  तदस्यास्त्यस्मिन्निति मतुप् + **8.2.9 मादुपधायाश्च मतोर्वोऽयवादिभ्यः** (म् → व् after an
  अवर्ण-final / म्-final stem). The five SK examples pin the condition exactly:
  अमर/शर/अजिर/वलय (a-final) → **व**; व्रीहि (i-final) → **म**. Feminine ङीप् comes free
  from the landed 4.1.6 उगितश्च (मतुप् is u-it) — same route as datṛ in the B4 work.
  The existing pre-formed `DImat`/`gomat`/`himavat` stems stay as they are.

Everything else reuses: the pre-pass pūrva-substitution (6.3.29), the main-scan dīrgha
(6.3.128), the `?samasta_Ratva` → `?samasta_Ratva_pada` → 8.4.1/8.4.2-arm-B ṇatva lever
(SK307/8.4.12, `:1074`), and the single-gated-nipātana-gaṇa rule pattern (SK/5.4.77).

---

## 3. Phases

Sequential on `generator`. Each phase = yaml rules + stems + tests + status rows, green
suite before the next starts.

### X1 — pūrvapada ādeśa keyed on the uttarapada (30 sūtras) — **DONE (2026-08-03)**

28 implemented + 2 Skipped (6.3.53 यत्, 6.3.55 शस् — affix contexts). 45 test cases in
`test/samasa_asraya_list.py`, driver `test/test_samasa_asraya.py`. **No engine change was
needed** — every rule is the SK926/6.3.29 pre-pass shape. Findings that carry into X2–X8:

- **Placement §1 held exactly as predicted.** All 28 rules work at `bahiranga: -1` on the
  (pūrva | uttara) window, first try. Nothing needed a main-scan placement.
- **A pre-pass rule pre-empts a main-scan rule structurally, with no `overrides:`.** The
  nitya सह→स rules (6.3.78/79/80) substitute in the pre-pass, so 6.3.82's main-scan
  `=saha` gate simply fails afterwards — no fork, no priority declaration. Expect to reuse
  this wherever a new nitya rule shadows a landed optional one.
- **Read SK for the substitute's final phoneme.** 6.3.52 supplies the ADANTA पद (SK says
  so: "पद इत्यदन्त आदेशः") but 6.3.54 ff. supply पत् — that one अ is the whole difference
  between पदाजिः and *पदजिः. X4's dīrgha rules have the same exposure.
- **Positional pratyāhāra gates work**: `r: _hal` + `rr: _ac` expresses 6.3.59's एकहलादि
  directly (कुम्भ passes, स्थाली fails). Useful for X4/X5's phonological conditions.
- **A "विवक्षिते" condition in the sūtra is licence for a composer tag.** 6.3.87/88's
  यादौ प्रत्यये विवक्षिते → `?tadDita_ya_para`, alongside the physically present यत्.
- **New driver capabilities** other phases can reuse: `type` selects the formation
  (`zazWI`/`karmaDAraya`/`ku`/`saha_bv`), `uttara_affix` attaches a taddhita after the
  uttara, and a member spec's `linga` overrides the stem's lexical gender (needed where a
  sūtra's example is a derivative — सतीर्थ्यः masc from neuter तीर्थ).
- **CLI parity verified, and it needs three composer inputs the test driver supplies
  implicitly** — worth knowing before debugging an X2+ rule that "does not fire" from the
  CLI: a karmadhāraya needs `?viSezaRa` on the pūrva (`-k samAna 1 ?viSezaRa -k jyotis 1`
  → सज्योतिः); the सह bahuvrīhi needs `--referent-linga`; and a कु/prādi pūrva needs a
  **semantic sense** token (`-k ku 1 kutsita -k aSva 1` → कदश्वः, versus कतश्वः without it —
  the sense is what keeps the pūrva a `?pada` so 8.2.39 jaśtva can apply, the standing
  `semantic_*` → `?pada` gotcha). Note zsh does not word-split unquoted `$args`; use `${=args}`.
- **One landed expectation changed:** `samasa_list.py`'s `T4-kupuruSaH` now expects
  कुपुरुषः / कापुरुषः (SK1032/6.3.106's vibhāṣā). Predicted in the plan; no other regressions.
- **Divergences from SK, each traced to an already-deferred sūtra, not to X1:** कापन्थाः
  for कापथम् (needs 5.4.74's अच्); उदवाहनम् for उदवाहनः (वाहन is lexically neuter and
  2.4.26 takes the uttara's gender); पद्हतिः alongside पद्धतिः and सोदर्य्यः alongside
  सोदर्यः (8.4.62 and 8.4.46 are landed *optional* rules).

Original scope, for reference:


| SK | A | Substitution | Canonical form |
|---|---|---|---|
| 988–989 | 6.3.50, 6.3.51 | हृदय → हृद् (51 optional) | हृल्लेखः; हृच्छोकः / हृदयशोकः |
| 990–994 | 6.3.52–56 | पाद → पद् (56 optional) | पदाजिः, पदातिः, पद्धतिः, पच्छः, पद्घोषः / पादघोषः |
| 995–998 | 6.3.57–60 | उदक → उद (59 optional) | उदमेघः, उदधिः, उदकुम्भः / उदककुम्भः, उदमन्थः |
| 1009–1011 | 6.3.78–80 | सह → स | सपलाशम्, समुहूर्तम्, सराक्षसीका |
| 1012–1016 | 6.3.84–88 | समान → स (88 optional) | सज्योतिः, सब्रह्मचारी, सतीर्थ्यः, सोदर्यः / समानोदर्यः |
| 1017–1018 | 6.3.89, 6.3.90 | समान → स; इदम् → ईश्, किम् → की | सदृक्, सदृशः; ईदृक्, ईदृशः, कीदृक्, कीदृशः |
| 1025–1026 | 6.3.99, 6.3.100 | अन्य + दुक् (आगम) | अन्यदाशीः, अन्यदुत्सुकः; अन्यदर्थः / अन्यार्थः |
| 1027–1033 | 6.3.101–107 | कु → कत्/कद्/का/कव | कदश्वः, कद्रथः, कत्तृणम्, कापथम्, काजलम्, कापुरुषः / कुपुरुषः, कवोष्णम् / कोष्णम् / कदुष्णम् |

**Mechanism:** one `bahiranga: -1` rule per sūtra, `lc: str("")` + `l: str("...")` (or
`l: str("d")`-style augment for दुक्), gated `lp: [and, "?samAsaPurva", "=<stem>"]` and
`rp: [and, "?samAsa", <uttara test>]`. Optional sūtras carry `optional: true` and fork.

**Why this goes first:** the pūrva stems all exist already — `hfdaya` (`pratipadika.py:902`),
`pAda` (`:216`), `udaka` (`:115`), `saha` (`:987`), `samAna` (`:325`), `anya` (`:874`),
`idam` (`:1031`), `kim` (`:1030`), `ku` (`:978`) — and `ku` already forms a working
tatpuruṣa through the landed SK761/2.2.18 कुगतिप्रादयः (कुपुरुषः is a live test case,
`test/samasa_list.py:475`). Cost is dominated by **new uttarapada stems**
(लेख, शोक, रोग, अजि, अति, हति, घोष, मेघ, धि, कुम्भ, मन्थ, पलाश, मुहूर्त, ज्योतिस्, तीर्थ, उदर,
दृश्, अश्व, रथ, तृण, पथिन्, जल, उष्ण, पुरुष, आशिस् …). Add them once, here; later phases
reuse them. **Before adding any stem, grep `pratipadika.py` and `avyaya.py` for both the
surface form and the variable name** — duplicate definitions silently shadow at import
(standing gotcha).

**Skipped rows:** the vārtikas (उत्तरपदस्य च for क्षीरोदः, त्रौ च for कत्त्रयः, दृक्षे च for
सदृक्षः/ईदृक्षः) — implement only where the uttara stem is already cheap.

### X2 — pūrvapada hrasva of ङी/आप् (8 sūtras) + the त्व affix — **DONE (2026-08-03)**

6 implemented + 2 Skipped (6.3.44/6.3.45 — affix contexts). 18 cases. Findings for X4–X8:

- **The `?NI` tagging in `pratipadika.py` is incomplete, and it matters.** ब्राह्मणी was missing
  `?NI` although it is a ङीप् formation (4.1.15); सुकेशी carries only `?svAnga_I`. Any rule
  whose condition is ङ्यन्त or अङ्यन्त therefore cannot trust `?NI` / `?!NI` lexicon-wide. This
  is the same root cause as the standing 5.4.153 नदी-arm note in generator_status.md.
- **A hrasva/dīrgha rule can UNDO another rule's deliberate work, and that is worse than
  noise.** 6.3.61, written to its literal condition, shortened back 6.3.137's criterial dīrgha
  (केशाकेशि, मुष्टीमुष्टि, बाहूबाहवि) and 6.3.27's ई (अग्नीवरुणौ). The engine offers no help here:
  the other rule fires first, is then disabled at the window, and 6.3.61 becomes newly
  triggered on its output — so `overrides:` cannot express the interaction. It was scoped to an
  opt-in `?gAlava_hrasva` marker instead, exactly as 6.3.137 itself was scoped, and the general
  form recorded as the deferral. **X4's 14 dīrgha rules are the mirror image of this — expect
  the same collisions and check against the केशाकेशि / अग्नीवरुणौ / ऊरीकृतम् cases specifically.**
- **A vibhāṣā whose xform is a no-op still forks.** Gating 6.3.61 on the bare `_ik` pratyāhāra
  made it fire on every short-i-final pūrva in the language, doubling outputs with identical
  surfaces. Hence `$$ik_dIrGa_anekAc` (`paribhasha.py`): require a LONG vowel, so hrasva
  actually changes something. The same trap applies to any optional length rule.
- **An affix-context rule is a MAIN-SCAN rule, not a pre-pass rule.** 6.3.64 त्वे च operates on
  stem + त्व with no compound at all; `bahiranga: -1` plus `?samAsaPurva` would have made it
  dead. It is therefore absent from the pre-pass trace (`fired: []`, as 6.3.82 is in X1).
- **Gender belongs on the affix when the affix determines it.** `tva_t` carries `?napum`, so
  अजा f. → अजत्वम् and रोहिणी f. → रोहिणित्वम् both come out right without touching either stem.
- **Ordered lists (क्रमात्) need one arm per pair.** 6.3.65 pairs इष्टका–चित, इषीका–तूल,
  माला–भारिन् respectively; a single `or` over both sides would license *इष्टकतूलम्.
- **New driver hooks:** `type: "affix"` (bare stem + affix, structure assertions skipped) and
  `sup: [N, M]` (an explicit sup — automatic insertion lives in the kāraka pre-pass, which is
  skip-guarded on `semantic_*`/`?samAsa_vivakza`, neither of which a stem+taddhita input has).

Original scope, for reference:

| SK | A | Form |
|---|---|---|
| 985 | 6.3.43 | ब्राह्मणिचेली, ब्राह्मणिगोत्र (uttarapada arms); घ/रूप/कल्प arms → **Skipped** |
| 986 | 6.3.44 | ब्रह्मबन्धुतरा / ब्रह्मबन्धूतरा → **Skipped** (तरप्) |
| 987 | 6.3.45 | विदुषितरा → **Skipped** (तरप्) |
| 999 | 6.3.61 | ग्रामणिपुत्रः / ग्रामणीपुत्रः (optional) |
| 1000 | 6.3.62 | एकक्षीरम् (uttarapada arm); एकरूप्यम् taddhita arm → **Skipped** |
| 1001 | 6.3.63 | रेवतिपुत्रः, अजक्षीरम् (बहुलम् → `optional: true`) |
| 1002 | 6.3.64 | अजत्वम् / अजात्वम्, रोहिणित्वम् / रोहिणीत्वम् — **needs `tva` (N3)** |
| 1006 | 6.3.65 | इष्टकचितम्, इषीकतूलम्, मालभारि |

**Mechanism:** `bahiranga: -1`, `xform: l: hrasva(l)`, gated on the pūrva's `?NI` (the
existing ङी tag on `nadI`, `kumArI`, `brAhmaRI` …) or `?Ap`, plus `$$anekAc_*`/`$$is_ekac`
for the अनेकाच् condition and `?puMvat` for भाषितपुंस्कात्.

**Interaction to watch:** SK985/6.3.43's own SK note says the hrasva **overrides**
puṁvadbhāva by paratva (`घरूप - इति वक्ष्यमाणो ह्रस्वः परत्वात्पुंवद्भावं बाधते`). The
puṁvadbhāva set (6.3.34/37/38/40/41/42/46) is landed at `sutras_antaranga.yaml:10998 ff.`
and gates on `?puMvat` — the same tag `brAhmaRI` carries. Add explicit `overrides:` and a
negative-control test so ब्राह्मणिचेली does not become *ब्राह्मणचेली.

New stems: चेली, ब्रुव, गोत्र, ग्रामणी, एका, रेवती, अजा, रोहिणी, इष्टका, इषीका, माला, चित, तूल,
भारिन्, क्षीर, पुत्र.

### X3 — मुम् (2 sūtras) — **DONE (2026-08-03)**

Both implemented, 5 cases, **no new machinery** — N1 turned out to need nothing beyond the
append xform `l: l+str("m")`, because मुम् is मित् and 1.1.47 मिदचोऽन्त्यात्परः (insert after the
last vowel) coincides with appending for a vowel-final pūrva. A consonant-final pūrva would
need the real after-the-last-vowel insertion; none arises in these two sūtras.

The nasal's surface is entirely landed sandhi's work, and it brings a fork with it: 8.3.23
मोऽनुस्वारः + 8.4.58 परसवर्णः give SK's सत्यङ्कारः / रात्रिञ्चरः, but 8.4.59 वा पदान्तस्य makes that
parasavarṇa optional at a pada boundary, so every form has an anusvāra twin (सत्यंकारः,
रात्रिंचरः). Not a defect — just expect the extra surface when asserting on मुम् forms.

Original scope, for reference:

SK1007/6.3.70 कारे सत्यागदस्य → **सत्यङ्कारः**, अगदङ्कारः; SK1008/6.3.72 रात्रेः कृति विभाषा
(`optional: true`) → **रात्रिंचरः / रात्रिचरः**. Mechanism N1. The long vārtika tail
(अस्तुङ्कारः, धेनुम्भव्या, लोकम्पृणः, तिमिङ्गिलः, उष्णङ्करणम् …) goes in as one Skipped row
unless a stem happens to be free.

### X4 — uttarapada-conditioned pūrva dīrgha (14 sūtras) + the मतुप् affix — **DONE (2026-08-03)**

12 implemented + 2 Skipped (6.3.116 क्विबन्त, 6.3.118 वलच्). 26 cases. Findings:

- **§1's placement table was WRONG in its most load-bearing row, and this phase found out.**
  All nine compound-dīrgha rules were written main-scan per the plan, following 6.3.128 — and
  *none of them fired*. Cause: at the main-scan junction the uttara has already merged with
  its sup, so `rp: =nara` / `r: s` can never match a literal. 6.3.128 works only because it
  keys on a TAG (`?vasupada`). **Rule of thumb: content-keyed → pre-pass; tag-keyed → either.**
  The table is corrected above.
- **X2's 6.3.61 problem did NOT recur, and the reason is worth stating**: every X4 rule is
  pinned to a specific uttarapada (कर्ण, वन, गिरि, मतुप्, वह, काश, नर, मित्र) or a specific pūrva.
  6.3.121 इको वहे can therefore use a bare `l: _ik` gate safely, where 6.3.61 could not.
  A length rule is dangerous only when its condition is a vowel class *and nothing else*.
- **A rule on an n-final pūrva needs the `lc`-form xform.** 6.3.125 अष्टनः: at pre-pass time
  the pūrva is still अष्टन्, so `l: dirgha(l)` lengthens the न् (a no-op). Use
  `lc: lc[:-1]+dirgha(lc[-1])` — 6.4.8's shape — and let 8.2.7's न्-lopa strip the न्.
- **मतुप् came out exactly right**, and the plan's reading of 8.2.9 was confirmed by the data:
  a-final अमर/शर/अजिर/वलय → व, i-final व्रीहि → म. One gotcha: the it-marker is `["u", "p"]`,
  not `["u~", "p"]` — `u~` is the anunāsika marker सु uses, and with it the u-it never
  registered, so 4.1.6 उगितश्च gave no ङीप् and 6.4.14 no upadhā-dīrgha.
- Per-instance tagging is the right tool for a shared pūrva: `?prAdi` goes on the test's परि,
  not on the base stem, which `ui/app.py` and the अक्षपरि avyayībhāva also use.

Original scope, for reference:

| SK | A | Form | Note |
|---|---|---|---|
| 1035 | 6.3.114 | संहितायाम् | adhikāra — a documentation row, no rule |
| 1036 | 6.3.115 | द्विगुणाकर्णः | `?lakzaRa` composer tag; अविष्टाष्ट… exclusion list as negative controls (`karRa` exists, `:773`) |
| 1037 | 6.3.116 | उपानत्, प्रावृट् | **Skipped** — क्विप्-anta derivations |
| 1038 | 6.3.117 | कोटरावणम्, किंशुलुकागिरिः | `?saMjYA`-gated; **feeds X6's 8.4.4** (`vana` `:139`, `giri` `:173` exist) |
| 1040 | 6.3.118 | कृषीवलः | **Skipped** — वलच् |
| 1041–1042 | 6.3.119, 6.3.120 | अमरावती, शरावती | **needs `matup` (N3)**; negative controls अजिरवती / व्रीहिमती / वलयवती |
| 1043 | 6.3.121 | ऋषीवहम् | `$$is_ik`-style गate; negative पिण्डवहम्, पीलुवहम् |
| 1044 | 6.3.122 | परीपाकः / परिपाकः | `GaY` pratyaya exists (`pratyaya.py:40`); बहुलम् → optional; negative निषादः |
| 1045 | 6.3.123 | नीकाशः, वीकाशः | negative प्रकाशः |
| 1046 | 6.3.125 | अष्टापदम् | `azwan` exists (`:742`); `?saMjYA`; negative अष्टपुत्रः |
| 1047 | 6.3.127 | एकचितीकः | कप्-context; reuse `kap` (`pratyaya.py:257`) |
| 1048–1049 | 6.3.129, 6.3.130 | विश्वानरः, विश्वामित्रः | **cheapest in the plan** — literally the landed 6.3.128 rule (`:745`) with `rp: =nara` / `=mitra`; `viSva` (`:1104`), `nara` (`:603`), `mitra` (`:1221`) all exist |

**Mechanism:** main-scan `xform: l: dirgha(l)`, template 6.3.128. Start with X4's
6.3.129/130 pair to validate the placement before the harder members.

### X5 — samāsa ṣatva (6 sūtras) — **DONE (2026-08-03)**

All 6 implemented, 10 cases, no engine work — N2 is just `xform: r: str("z")` at the pre-pass
junction, since `r` is the uttara's FIRST char (`sutra.py:279`). Findings:

- **ṢṬUTVA had to be folded into 8.3.81 and 8.3.83.** The plan assumed 8.4.41 ष्टुना ष्टुः would
  supply it for free; it cannot. 8.4.41 is a JUNCTION rule, and the fresh ष् and the थ्/त् it
  must act on both end up inside the uttara element (स्थान → ष्थान), where there is no
  junction. The xform therefore calls 8.4.41's own `zwutva` helper on the next char — one
  extra call site for the same helper, not duplicated logic. Without it: *भीरुष्थानम्.
  **A general fix would be an element-internal variant of 8.4.41**, worth considering if a
  later phase hits the same wall.
- **A वा that competes with a NITYA needs the nitya carved out.** 8.3.100 नक्षत्राद्वा is optional,
  but 8.3.99 is nitya and re-supplied the ṣatva in 8.3.100's skip branch, so रोहिणीसेना could
  never surface. Fixed by `?!nakzatra` on 8.3.99. `overrides:` alone does not help — it governs
  the case where both are triggered, not the skip branch.
- **ज्योतिष्टोमः is partial and it is not this phase's fault.** The ष्ट is correct; the pūrva's own
  final sibilant survives too (ज्योतिःष्टोमः / ज्योतिष्ष्टोमः) because visarga-LOPA before शर् +
  stop — a vārtika on 8.3.36 — is unimplemented. Adding it would touch every visarga-before-
  श्च/ष्ट/स्त in the suite, so it stays a recorded gap.
- SK's masc हरिषेणः / सुषामा: सुषामा works (n-stem bahuvrīhi, masc referent); हरिषेणः would need
  the ṭāp-lopa a masculine name-compound triggers on an ā-stem uttara, so सेना stays feminine
  and the case asserts हरिषेणा. The ṣatva is what is under test and is unaffected.

Original scope, for reference:

SK1019/8.3.80 **अङ्गुलिषङ्गः** · SK1020/8.3.81 **भीरुष्ठानम्** · SK1021/8.3.83
**ज्योतिष्टोमः, आयुष्टोमः** · SK1022/8.3.98 **सुषामा, सुषन्धिः** · SK1023/8.3.99
**हरिषेणः** (`?saMjYA`, अगात् — negative विष्वक्सेनः, पृथुसेनः, सर्वसेनः) ·
SK1024/8.3.100 **रोहिणीषेणः / रोहिणीसेनः** (`optional: true`).

**Mechanism N2.** Every rule is `lp: <lexical gate>` + `l: [_iR, ku]` (the इण्कोः
condition, still live by anuvṛtti) + `r: s` → `r: str("z")`. Each `असमासे` counter-example
in SK becomes a negative-control test case (अङ्गुलेः सङ्गः, भीरोः स्थानम्, ज्योतिषः स्तोमः).
`aNguli` exists (`:893`), `hari` (`:60`); new: भीरु, सङ्ग, स्थान, ज्योतिस्, आयुस्, स्तोम, सामन्,
सन्धि, सेना.

### X6 — samāsa ṇatva (9 sūtras) — closes the standing gap — PENDING

| SK | A | Form |
|---|---|---|
| 1039 | 8.4.4 | पुरगावणम्, कोटरावणम्, अग्रेवणम् (needs X4's 6.3.117 dīrgha); negative असिपत्रवनम् |
| 1050 | 8.4.5 | प्रवणम्, निर्वणम्, कार्ष्यवणम् (असंज्ञायामपि) |
| 1051 | 8.4.6 | दूर्वावणम् / दूर्वावनम् (`optional: true`); वārtika द्व्यच्त्र्यज्भ्यामेव → negative देवदारुवनम् |
| 1052 | 8.4.8 | इक्षुवाहणम्; negative इन्द्रवाहनम् (`?AhitA` composer tag) |
| 1053 | 8.4.9 | क्षीरपाणाः, सुरापाणाः (देशे) |
| 1054 | 8.4.10 | क्षीरपाणम् / क्षीरपानम् (`optional: true`, भावकरणयोः) |
| **1055** | **8.4.11** | **माषवापिणौ, व्रीहिवापाणि, माषवापेण; क्षीरपेण; and the standing चोरभयेण / त्रिभुवनम् family** |
| 1056 | 8.4.13 | हरिकामिणौ, हरिकामाणि, हरिकामेण (कवर्गवति उत्तरपदे) |
| 1057 | 8.4.38 | माषकुम्भवापेन (prohibition across a pada); वārtika अतद्धित → आर्द्रगोमयेण |

**Mechanism:** each rule sets `+samasta_Ratva` on the uttara — the exact `update:` of the
landed SK307/8.4.12 एकाजुत्तरपदे णः (`sutras_antaranga.yaml:1074`). The propagated
`?samasta_Ratva_pada` then drives **arm B** of 8.4.1 / 8.4.2 (`:1033`, `:1056`); arm A is
blocked by `?merged_pada`, which is exactly why the pūrva-only trigger currently fails.

**8.4.11 is implemented nitya** (decision 1). Its three arms are प्रातिपदिकान्त / नुम् /
विभक्ति; the विभक्ति arm is the one that produces चोरभयेण. Two guards from SK1055 must go
in: the vārtika **उत्तरपदं यत्प्रातिपदिकं तदन्तस्यैव णत्वम्** (negative गर्गभगिनी) and
**युवादेर्न** (negative रम्ययूना, परिपक्वानि). A Skipped row records the unmodelled वा.

**Regression duty for this phase:** re-run the whole suite and diff outputs, not just the
new tests. Flip `test/samasa_list.py:418-431` (त्रिभुवनम्) and the
`generator_status.md:838` deferral row from Deferred to Implemented, and re-check the
existing 8.4.3-marker plumbing (`?nas_AdeSa` / `?saMjYA_nas` in the `join_objects` Tier-1
allowlist) still behaves.

### X7 — पृषोदरादि + the suṭ nipātanas (15 sūtras) — PENDING

SK1034/6.3.109 पृषोदरादीनि यथोपदिष्टम् → पृषोदरम्, बलाहकः, हंसः, सिंहः, दूडाशः, बृसी;
SK1058–1071 / 6.1.143–157 → कुस्तुम्बुरूणि, अपरस्पराः, गोष्पदम्, आस्पदम्, आश्चर्यम्, अवस्करः,
अपस्करः, विष्किरः / विकिरः, प्रतिष्कशः, प्रस्कण्वः, हरिश्चन्द्रः, मस्करः / मस्करी, कास्तीरम्,
अजस्तुन्दम्, कारस्करः, पारस्करः, तस्करः, बृहस्पतिः, प्रायश्चित्तम्.

**Mechanism:** the landed 5.4.77 precedent — **one `?nipAta_<id>`-gated rule per gaṇa**,
not one per member, with the members supplied as tagged stems. Two rules total
(पृषोदरादि; the सुट्-nipātana set), plus the individually-conditioned ones
(6.1.145 सेवितासेवितप्रमाणेषु, 6.1.147 अनित्ये, 6.1.150 वा) as their own rules with their
own `?saMjYA` / sense gates and the SK negative controls (गोपदम्, आपदम्, आचर्यम्, अवकरः,
विकिरः, प्रतिकशः, प्रकण्वः, मकरः, कातीरम्, कारकरः). Cheapest phase per sūtra.

### X8 — ष्यङ् सम्प्रसारणम् (3 sūtras) — PENDING

SK1003/6.1.13 ष्यङः सम्प्रसारणं पुत्रपत्योस्तत्पुरुषे + SK1004/6.3.139 सम्प्रसारणस्य (दीर्घः) +
SK1005/6.1.14 बन्धुनि बहुव्रीहौ → **कारीषगन्धीपुत्रः, कारीषगन्धीपतिः, कारीषगन्धीबन्धु**;
negatives कारीषगन्ध्याबन्धुः, अतिकारीषगन्ध्यापुत्रः.

Needs a ष्यङ्-formed feminine stem (`kArIzaganDyA` / `kaumudaganDyA`) and the existing
`samprasaranam` helper (`paribhasha.py:46`). 6.3.139 is a pre-pass `l: dirgha(l)` on the
`?samprasAraRa` residue. Left last because it is the only phase needing a genuinely new
stem *class*. If the ष्यङ् derivation proves expensive, the fallback is the landed 6.3.42
puṁvadbhāva precedent: composer supplies the stem, the rule fires as a documented saṁjñā.

### X9 — Prakaraṇa audit + status — PENDING

Per the prakaraṇa-audit convention: enumerate SK985–1071, cross-reference every
Ashtadhyayi `id:` present in the YAMLs against the range, and confirm **every one of the
87 is either an Implemented row or an explicit Skipped row** — target 0 unaccounted, as
tatpuruṣa (SK684–828) achieved. Update `generator_status.md` counts, and replace (do not
stack) the Last/Next lines, keeping them to 1–3 sentences.

**No UI phase is expected.** The composer already accepts arbitrary `?tag` tokens through
`cmd_line.py`'s `-k/--karaka` action, which is how `?saMjYA`, `?lakzaRa`, `?AhitA` etc.
will be supplied; `-m`/`-u`/`-B`/`-D` already build the compounds these rules mutate.
Confirm during X9 rather than planning work for it.

---

## 4. Files touched

| File | Change | X1 status |
|---|---|---|
| `sanskrit_parser/generator/sutras_antaranga.yaml` | ~70 new rule blocks, one prakaraṇa banner per phase (mirror the D/E/S/A banners at `:12750`) | 30 rules + the prakaraṇa banner added at the file tail |
| `sanskrit_parser/generator/pratipadika.py` | ~60 new stems, grouped and commented per phase; **grep for dupes first** | 21 stems added in one commented X1 block |
| `sanskrit_parser/generator/pratyaya.py` | `tva`, `matup` (N3) | untouched (arrives with X2/X4) |
| `sanskrit_parser/generator/test/samasa_asraya_list.py` | **new** — `samasa_asraya_tests`, ~100 cases. `samasa_list.py` is already 1997 lines with five lists; a sixth belongs in its own module | created, 45 cases |
| `sanskrit_parser/generator/test/test_samasa_asraya.py` | **new** driver, modelled on `test_samasa_tatpurusha.py` — three assertion levels (member structure / fired-sutra trace / surface), plus negative-control cases via `not_fired` | created |
| `sanskrit_parser/generator/test/samasa_list.py` | flip the त्रिभुवनम् deferral at `:418-431` (phase X6) | not yet; X1 instead updated `T4-kupuruSaH` to its two forms |
| `sanskrit_parser/generator/generator_status.md` | 87 rows + Skipped rows; counts; Last/Next | 10 grouped rows (28 sūtras) + 2 Skipped rows; counts and Last/Next updated |
| `sanskrit_parser/generator/samasa_asraya_plan.md` | **new** — this plan, committed alongside (as `samasa_completion_plan.md` and `bahuvrihi_plan.md` were) | committed with X1 (`b3847ca`) |

The test driver is generic over compound type: unlike the existing per-samāsa-type
drivers, these rules apply to tatpuruṣa, bahuvrīhi and dvandva alike. **As built, the
field is named `type`** (not `samasa_type`), and it selects the formation the case rides
on — `zazWI` / `karmaDAraya` / `ku` / `saha_bv`, each mapped to the intent tags that
formation's saṁjñā rule needs. Two further hooks were added in X1 and are available to
later phases: `uttara_affix` (attach a taddhita after the uttara, in the slot
`_insert_samasanta` uses) and a member spec's `linga` (override the stem's lexical
gender, needed where a sūtra's example is a derivative — सतीर्थ्यः masc from neuter तीर्थ).

---

## 5. Verification

Per phase:

```bash
cd /Users/karthik/personal_projects/sanskrit_parser/sanskrit_parser/generator/test && PYTHONPATH=/Users/karthik/personal_projects/sanskrit_parser /Users/karthik/venvs/sanskrit/bin/pytest -n 8 --dist worksteal
```

Expect ~8,300 items in ≈7.5 min at `-n 8` (8363 after X1; it stretches to ~19 min if you
run CLI probes concurrently — they compete for the same 8 cores). Green before moving to
the next phase; the per-phase slice (`pytest test_samasa_asraya.py`) runs in ~10s.

CLI spot-checks — **use `scripts/sanskrit_generator`**, one per mechanism family, from the
repo root. (`python -m sanskrit_parser.generator.cmd_line` does not invoke the entry
point; and `-k` takes ONE stem per flag, so each member needs its own `-k`.)

```bash
PYTHONPATH=$PWD python scripts/sanskrit_generator -k hfdaya 1 v6 -k leKa 1 --samasa
```

```bash
PYTHONPATH=$PWD python scripts/sanskrit_generator -k ku 1 kutsita -k aSva 1 --samasa
```

Three composer inputs the test driver supplies implicitly and the CLI does not — check
these before concluding a rule is broken:
- a **karmadhāraya** needs `?viSezaRa` on the pūrva (`-k samAna 1 ?viSezaRa -k jyotis 1`
  → सज्योतिः; without it the members merely sandhi → समानोज्योतिः);
- the **saha bahuvrīhi** needs `--referent-linga <pum|strI|napum>`;
- a **कु / prādi pūrva** needs a **semantic sense** token (`-k ku 1 kutsita -k aSva 1`
  → कदश्वः, versus कतश्वः without it — the sense is what keeps the pūrva a `?pada`, so
  8.2.39 jaśtva can apply; the standing `semantic_*` → `?pada` gotcha).

Note zsh does not word-split unquoted `$args` — use `${=args}` when looping.

Extra gates:
- **X6 only:** run the full suite and diff surface outputs against the pre-phase run —
  8.4.11 touches every compound with a pūrva r/ṣ, so a silent extra/changed form
  elsewhere is the failure mode to look for.
- **Placement debugging:** when a rule does not fire, dump the window first
  (`--verbose --tag-display`) before editing the condition — the (pūrva | sup) vs
  (pūrva | uttara) confusion of §1 accounts for most misfires in this family.
- `flake8` (max line length 150, `setup.cfg`) on the touched Python files.
