# -*- coding: utf-8 -*-
"""Avyayībhāva-samāsa test cases (avyayībhāva samāsa plan, S1A + S1B).

Each case builds a two-member sentence [Adya, pūrva, uttara, avasAna] (members
adjacent — no avasAna between, so they form one compound) and asserts three
levels (see test_samasa_avyayibhava.py):

  1. structure : after the samāsa pre-pass the pūrva carries samAsaPurva +
                 upasarjana and the uttara carries samAsa + avyayIBAva
                 (sups retained — combining/luk is the main scan's job)
  2. fired     : the listed pre-pass sutras appear in the pre-pass trace
  3. surface   : the full pipeline (pre-pass → main scan) emits the expected form

Each member spec is either {"avyaya": <name in avyaya.py>} or
{"stem": <name in pratipadika.py>, "vacana": N}; optional "sem" (a semantic_*
sense) and "vivakza" (sets ?samAsa_vivakza). Most avyayībhāva senses double as
the kāraka-pre-pass skip-guard trigger; a purely structural nitya case (2.1.10)
uses vivakza instead.
"""

samasa_tests = [
    # ── S1A: 2.1.6 core (avyaya-pūrva) ──
    {
        "label": "S1A-upakRSNam-samIpa-SK652-2.1.6",          # समीप, a-stem → 2.4.83 am
        "purva": {"avyaya": "upa_avyaya", "sem": "semantic_samIpa"},
        "uttara": {"stem": "kfzRa", "vacana": 1},
        "fired": ["2.1.6", "1.2.43"],
        "surface": "उपकृष्णम्",
    },
    {
        "label": "S1A-adhihari-vibhakti-SK652-2.1.6",         # विभक्ति, i-stem → 1.1.41 → 2.4.82 luk
        "purva": {"avyaya": "aDi_avyaya", "sem": "semantic_vibhakti"},
        "uttara": {"stem": "hari", "vacana": 1},
        "fired": ["2.1.6", "1.2.43"],
        "surface": "अधिहरि",
    },
    # ── S1B: 2.1.6 further sense (atyaya), 2.1.7 yathā, 2.1.8 yāvat ──
    {
        "label": "S1B-atihimam-atyaya-SK652-2.1.6",           # अत्यय, a-stem → am
        "purva": {"avyaya": "ati_avyaya", "sem": "semantic_atyaya"},
        "uttara": {"stem": "hima", "vacana": 1},
        "fired": ["2.1.6", "1.2.43"],
        "surface": "अतिहिमम्",
    },
    {
        "label": "S1B-yathASakti-SK661-2.1.7",          # यथा (anatikrama), i-stem fem → luk
        "purva": {"avyaya": "yaTA", "sem": "semantic_yaTArTa"},
        "uttara": {"stem": "Sakti", "vacana": 1},
        "fired": ["2.1.7", "1.2.43"],
        "surface": "यथाशक्ति",
    },
    {
        "label": "S1B-yAvajjIvam-SK662-2.1.8",          # यावत् (avadhāraṇa), a-stem → am + t→j sandhi
        "purva": {"avyaya": "yAvat", "sem": "semantic_avaDAraRa"},
        "uttara": {"stem": "jIva", "vacana": 1},
        "fired": ["2.1.8", "1.2.43"],
        "surface": "यावज्जीवम्",
    },
    # ── S1B: 2.1.9 / 2.1.10 (NOUN-pūrva, avyaya is the uttara; needs 2.4.71) ──
    {
        "label": "S1B-SAkaprati-SK663-2.1.9",           # śāka (mātrā) + prati; prati i-stem → luk
        "purva": {"stem": "SAka", "vacana": 1, "sem": "semantic_mAtrA"},
        "uttara": {"avyaya": "prati_avyaya"},
        "fired": ["2.1.9", "1.2.43"],
        "surface": "शाकप्रति",
    },
    {
        "label": "S1B-akzapari-SK664-2.1.10",           # akṣa + pari (structural nitya → vivakza)
        "purva": {"stem": "akza", "vacana": 1, "vivakza": True},
        "uttara": {"avyaya": "pari_avyaya", "vivakza": True},
        "fired": ["2.1.10", "1.2.43"],
        "surface": "अक्षपरि",
    },
    # ── S2: vibhāṣā block (≥ SK665) — only-when-intended (gated by samAsa_vivakza) ──
    {
        # apa + grāma: the noun's pañcamī is set by the kāraka layer
        # (apa + semantic_varjana → 1.4.88 → 2.3.10 → viBakti_5), which 2.1.12
        # checks (rp ?viBakti_5) and consumes (swap → prathamā) → अपग्रामम्.
        "label": "S2-apagrAmam-SK666-2.1.12",
        "purva": {"avyaya": "apa_avyaya", "sem": "semantic_varjana", "dir": "para", "vivakza": True},
        "uttara": {"stem": "grAma", "vacana": 1, "vivakza": True},
        "fired": ["1.4.88", "2.3.10", "2.1.12", "1.2.43"],
        "surface": "अपग्रामम्",
    },
    {
        # ā + samudra: pañcamī via A + semantic_maryAdA → 1.4.89 → 2.3.10.
        "label": "S2-Asamudram-SK667-2.1.13",
        "purva": {"avyaya": "AN_avyaya", "sem": "semantic_maryAdA", "dir": "para", "vivakza": True},
        "uttara": {"stem": "samudra", "vacana": 1, "vivakza": True},
        "fired": ["1.4.89", "2.3.10", "2.1.13", "1.2.43"],
        "surface": "आसमुद्रम्",
    },
    {
        "label": "S2-pratyagni-SK668-2.1.14",           # prati + agni (ābhimukhya), i-stem → luk + sandhi
        "purva": {"avyaya": "prati_avyaya", "vivakza": True},
        "uttara": {"stem": "agni", "vacana": 1, "vivakza": True},
        "fired": ["2.1.14", "1.2.43"],
        "surface": "प्रत्यग्नि",
    },
    {
        "label": "S2-anuvanam-SK669-2.1.15",            # anu (samayā) + vana, a-stem → am
        "purva": {"avyaya": "anu_avyaya", "sem": "semantic_samayA", "vivakza": True},
        "uttara": {"stem": "vana", "vacana": 1, "vivakza": True},
        "fired": ["2.1.15", "1.2.43"],
        "surface": "अनुवनम्",
    },
    {
        "label": "S2-anugaNgam-SK670-2.1.16",           # anu (āyāma) + gaṅgā, ā-stem → napum → hrasva → am
        "purva": {"avyaya": "anu_avyaya", "sem": "semantic_AyAma", "vivakza": True},
        "uttara": {"stem": "gaNgA", "vacana": 1, "vivakza": True},
        "fired": ["2.1.16", "1.2.43"],
        "surface": "अनुगङ्गम्",
    },
    {
        "label": "S2-dvimuni-SK673-2.1.19",             # dvi + muni (vaṁśya), i-stem → luk
        "purva": {"stem": "dvi", "vivakza": True},   # dvi: nityadvivacana — no forced vacana
        "uttara": {"stem": "muni", "vacana": 1, "vivakza": True, "tags": ["vaMSya"]},
        "fired": ["2.1.19", "1.2.43"],
        "surface": "द्विमुनि",
    },
    {
        "label": "S2-dvigaNgam-SK674-2.1.20",           # dvi + gaṅgā (nadī), ā-stem → hrasva → am
        "purva": {"stem": "dvi", "vivakza": True},   # dvi: nityadvivacana — no forced vacana
        "uttara": {"stem": "gaNgA", "vacana": 1, "vivakza": True, "tags": ["nadI_saMjYA"]},
        "fired": ["2.1.20", "1.2.43"],
        "surface": "द्विगङ्गम्",
    },
    # ── S2 negative: विभाषा is "only when intended" — WITHOUT samAsa_vivakza no
    #    compound forms (prati + agni stay as separate words). ──
    {
        "label": "S2-pratyagni-no-vivakza-SK668-2.1.14",
        "purva": {"avyaya": "prati_avyaya"},
        "uttara": {"stem": "agni", "vacana": 1},
        "fired": [],
        "no_samasa": True,
    },
    # ── S3/S4: samāsānta — rule-driven ?samasanta_TaC (5.4.107–112) ──
    {
        "label": "S3-upaSaradam-SK677-5.4.107",         # upa + śarad → TaC → उपशरदम्
        "purva": {"avyaya": "upa_avyaya", "sem": "semantic_samIpa"},
        "uttara": {"stem": "Sarad", "vacana": 1},
        "fired": ["2.1.6", "1.2.43", "5.4.107"],
        "surface": "उपशरदम्",
    },
    {
        "label": "S4-upamanasam-SK677-5.4.107-gana",    # upa + manas (śaradādi s-stem) → TaC → उपमनसम्
        "purva": {"avyaya": "upa_avyaya", "sem": "semantic_samIpa"},
        "uttara": {"stem": "manas", "vacana": 1},
        "fired": ["2.1.6", "1.2.43", "5.4.107"],
        "surface": "उपमनसम्",
    },
    {
        "label": "S4-uparAjam-SK678-5.4.108",           # upa + rājan (an-final) → TaC + 6.4.144 → उपराजम्
        "purva": {"avyaya": "upa_avyaya", "sem": "semantic_samIpa"},
        "uttara": {"stem": "rAjan", "vacana": 1},
        "fired": ["2.1.6", "1.2.43", "5.4.108"],
        "surface": "उपराजम्",
    },
    {
        "label": "S4-upanadam-SK681-5.4.110",           # upa + nadī (ī-fem) → TaC → उपनदम्
        "purva": {"avyaya": "upa_avyaya", "sem": "semantic_samIpa"},
        "uttara": {"stem": "nadI", "vacana": 1},
        "fired": ["2.1.6", "1.2.43", "5.4.110"],
        "surface": "उपनदम्",
    },
    {
        "label": "S4-upasamiDam-SK682-5.4.111",         # upa + samidh (jhay-final) → TaC → उपसमिधम्
        "purva": {"avyaya": "upa_avyaya", "sem": "semantic_samIpa"},
        "uttara": {"stem": "samiD", "vacana": 1},
        "fired": ["2.1.6", "1.2.43", "5.4.111"],
        "surface": "उपसमिधम्",
    },
    {
        "label": "S4-upagiram-SK683-5.4.112",           # upa + giri (Senaka) → TaC → उपगिरम्
        "purva": {"avyaya": "upa_avyaya", "sem": "semantic_samIpa"},
        "uttara": {"stem": "giri", "vacana": 1},
        "fired": ["2.1.6", "1.2.43", "5.4.112"],
        "surface": "उपगिरम्",
    },
    {
        # upa + carman (napuṁsaka an-stem): 5.4.109 अन्यतरस्याम् — TaC OPTIONAL →
        # the samāsa pre-pass forks: उपचर्मम् (TaC) / उपचर्म (no TaC).
        "label": "S4-upacarma-SK680-5.4.109-fork",
        "purva": {"avyaya": "upa_avyaya", "sem": "semantic_samIpa"},
        "uttara": {"stem": "carman", "vacana": 1},
        "fired": ["2.1.6", "1.2.43", "5.4.109"],
        "surfaces": ["उपचर्म", "उपचर्मम्"],
    },
    # ── S3: 6.3.81 अव्ययीभावे चाकाले — saha → sa (non-kāla) ──
    {
        "label": "S3-sacakram-SK660-6.3.81",            # saha (yaugapadya) + cakra → सचक्रम् (saha→sa)
        "purva": {"stem": "saha", "sem": "semantic_yOgapadya", "vivakza": True},
        "uttara": {"stem": "cakra", "vacana": 1, "vivakza": True},
        "fired": ["2.1.6", "1.2.43"],             # 6.3.81 is a main-scan rule (not in pre-pass trace)
        "surface": "सचक्रम्",
    },
    # ── S3: 2.4.84 तृतीयासप्तम्योर्बहुलम् — bahula am for tṛtīyā/saptamī (optional fork) ──
    {
        "label": "S3-upakRSNam-bahula-SK658-2.4.84",    # upa + kṛṣṇa (saptamī) → उपकृष्णम् / उपकृष्णे
        "purva": {"avyaya": "upa_avyaya", "sem": "semantic_samIpa"},
        "uttara": {"stem": "kfzRa", "vacana": 1, "vibhakti": 7},
        "fired": ["2.1.6", "1.2.43"],
        "surfaces": ["उपकृष्णम्", "उपकृष्णे"],
    },
]


# ── Tatpuruṣa-samāsa test cases (tatpuruṣa samāsa plan, Phase T0) ──────────────
# Unlike the avyayībhāva, a tatpuruṣa DECLINES NORMALLY in the uttara's gender
# (2.4.26 परवल्लिङ्गम्) — no ?avyaya/?napum, the uttara's sup surfaces. Structure
# assertion: pūrva samAsaPurva + upasarjana, uttara samAsa + tatpuruza (NOT
# avyayIBAva). Driver: test_samasa_tatpurusha.py.
#
# The pūrva carries the vigraha vibhakti directly ("vibhakti": N — decoupled from
# full kṛdanta-kāraka coverage); the uttara's śrita-gaṇa membership (?srita_gaRa)
# is intrinsic to the Srita pratipadika.
samasa_tp_tests = [
    # ── T0: 2.1.24 dvitīyā-tatpuruṣa (śrita-gaṇa uttara), a-stem masc ──
    {
        "label": "T0-kRSNaSritaH-SK686-2.1.24",         # कृष्णं श्रितः → कृष्णश्रितः (nom sg)
        "purva": {"stem": "kfzRa", "vacana": 1, "vibhakti": 2, "vivakza": True},
        "uttara": {"stem": "Srita", "vacana": 1, "vivakza": True},
        "fired": ["2.1.24", "1.2.43", "2.4.26"],
        "surface": "कृष्णश्रितः",
    },
    # negative: WITHOUT ?samAsa_vivakza no tatpuruṣa forms (only-when-intended).
    {
        "label": "T0-kRSNaSrita-no-vivakza-SK686-2.1.24",
        "purva": {"stem": "kfzRa", "vacana": 1, "vibhakti": 2},
        "uttara": {"stem": "Srita", "vacana": 1},
        "fired": [],
        "no_samasa": True,
    },
    # ── T0 dvitīyā extensions (2.1.25–29) ──
    {
        # स्वयम् + कृत → स्वयंकृतम् / स्वयङ्कृतम् (8.3.23 म्→anusvāra at the junction, +
        # 8.4.58 optional parasavarṇa ṅ). The pūrva carries a semantic sense
        # ("sem") exactly as the kāraka/CLI path does (`-w svayam 1` → semantic_1):
        # it rides through the compound merge and keeps the avyaya pūrva ?pada, so
        # 8.3.23 fires. (Without it a degenerate input leaves svayam non-?pada → म्.)
        "label": "T0-svayaMkRtam-SK687-2.1.25",
        "purva": {"avyaya": "svayam", "sem": "semantic_1", "vivakza": True},
        "uttara": {"stem": "kfta", "vacana": 1, "vivakza": True},
        "fired": ["2.1.25", "1.2.43", "2.4.26"],
        "surfaces": ["स्वयंकृतम्", "स्वयङ्कृतम्"],
    },
    {
        "label": "T0-KawvArUQaH-SK688-2.1.26",          # खट्वा (dvitīyā, kṣepa) + रूढ → खट्वारूढः
        "purva": {"stem": "KawvA", "vacana": 1, "vibhakti": 2, "sem": "semantic_kzepa"},
        "uttara": {"stem": "rUQa", "vacana": 1},
        "fired": ["2.1.26", "1.2.43", "2.4.26"],
        "surface": "खट्वारूढः",
    },
    {
        # सामि + कृत → सामिकृतम् (i-final pūrva, no junction sandhi). Same avyaya-pūrva
        # shape as 2.1.25 — carries a semantic sense to mirror the kāraka/CLI path.
        "label": "T0-sAmikRtam-SK689-2.1.27",
        "purva": {"avyaya": "sAmi", "sem": "semantic_1", "vivakza": True},
        "uttara": {"stem": "kfta", "vacana": 1, "vivakza": True},
        "fired": ["2.1.27", "1.2.43", "2.4.26"],
        "surface": "सामिकृतम्",
    },
    {
        "label": "T0-mAsapramitaH-SK690-2.1.28",        # मास (dvitīyā, kāla, non-atyanta) + प्रमित → मासप्रमितः
        "purva": {"stem": "mAsa", "vacana": 1, "vibhakti": 2, "vivakza": True},
        "uttara": {"stem": "pramita", "vacana": 1, "vivakza": True},
        "fired": ["2.1.28", "1.2.43", "2.4.26"],
        "surface": "मासप्रमितः",
    },
    {
        "label": "T0-muhUrtasuKam-SK691-2.1.29",        # मुहूर्त (dvitīyā, kāla, atyantasaṃyoga) + सुख → मुहूर्तसुखम्
        "purva": {"stem": "muhUrta", "vacana": 1, "vibhakti": 2,
                  "sem": "semantic_atyantasaMyoga", "vivakza": True},
        "uttara": {"stem": "suKa", "vacana": 1, "vivakza": True},
        "fired": ["2.1.29", "1.2.43", "2.4.26"],
        "surface": "मुहूर्तसुखम्",
    },
    # ── T1: the remaining five vibhakti-tatpuruṣas (2.1.30–48, 2.2.1–11) ──
    # Each: pūrva carries its vigraha vibhakti (viBakti_N) + vivakṣā; the uttara's
    # class membership (?guRavacana/?pUrvasadfSa_gaRa/?tadarTa_gaRa/?Baya_gaRa/
    # ?SORqa_gaRa/?ekadeSin) is intrinsic to the pratipadika. The compound declines
    # normally in the uttara's gender (masc/napuṁsaka a-stem).
    {
        "label": "T1-mAsapUrvaH-SK693-2.1.31",          # मासेन पूर्वः → मासपूर्वः (tṛtīyā, pūrvasadṛśa)
        "purva": {"stem": "mAsa", "vacana": 1, "vibhakti": 3, "vivakza": True},
        "uttara": {"stem": "pUrva_tp", "vacana": 1, "vivakza": True},
        "fired": ["2.1.31", "1.2.43", "2.4.26"],
        "surface": "मासपूर्वः",
    },
    {
        "label": "T1-DAnyArTaH-SK698-2.1.36",           # धान्याय अर्थः → धान्यार्थः (caturthī, tadartha)
        "purva": {"stem": "DAnya", "vacana": 1, "vibhakti": 4, "vivakza": True},
        "uttara": {"stem": "arTa", "vacana": 1, "vivakza": True},
        "fired": ["2.1.36", "1.2.43", "2.4.26"],
        "surface": "धान्यार्थः",
    },
    {
        "label": "T1-coraBayam-SK699-2.1.37",           # चोरात् भयम् → चोरभयम् (pañcamī, bhaya; napuṁsaka)
        "purva": {"stem": "cora", "vacana": 1, "vibhakti": 5, "vivakza": True},
        "uttara": {"stem": "Baya", "vacana": 1, "vivakza": True},
        "fired": ["2.1.37", "1.2.43", "2.4.26"],
        "surface": "चोरभयम्",
    },
    {
        "label": "T1-rAjapuruSaH-SK702-2.2.8",          # राज्ञः पुरुषः → राजपुरुषः (ṣaṣṭhī — the canonical tatpuruṣa)
        "purva": {"stem": "rAjan", "vacana": 1, "vibhakti": 6, "vivakza": True},
        "uttara": {"stem": "puruza", "vacana": 1, "vivakza": True},
        "fired": ["2.2.8", "1.2.43", "2.4.26"],
        "surface": "राजपुरुषः",
    },
    {
        "label": "T1-pUrvakAyaH-SK712-2.2.1",           # पूर्वं कायस्य → पूर्वकायः (ṣaṣṭhī pūrvāpara/ekadeśī)
        "purva": {"stem": "pUrva_dik", "vacana": 1, "vibhakti": 1, "vivakza": True},
        "uttara": {"stem": "kAya_ed", "vacana": 1, "vivakza": True},
        "fired": ["2.2.1", "1.2.43", "2.4.26"],
        "surface": "पूर्वकायः",
    },
    {
        "label": "T1-akzaSORqaH-SK717-2.1.40",          # अक्षेषु शौण्डः → अक्षशौण्डः (saptamī, śauṇḍa)
        "purva": {"stem": "akza", "vacana": 1, "vibhakti": 7, "vivakza": True},
        "uttara": {"stem": "SORqa", "vacana": 1, "vivakza": True},
        "fired": ["2.1.40", "1.2.43", "2.4.26"],
        "surface": "अक्षशौण्डः",
    },
    # ── T1 extension rules (one case each, previously untested) ──
    {
        "label": "T1-guqasvAduH-SK692-2.1.30",          # गुडेन स्वादुः → गुडस्वादुः (tṛtīyā, guṇavacana; u-stem uttara)
        "purva": {"stem": "guqa", "vacana": 1, "vibhakti": 3, "vivakza": True},
        "uttara": {"stem": "svAdu", "vacana": 1, "vivakza": True},
        "fired": ["2.1.30", "1.2.43", "2.4.26"],
        "surface": "गुडस्वादुः",
    },
    {
        "label": "T1-ahihataH-SK694-2.1.32",            # अहिना हतः → अहिहतः (tṛtīyā kartṛ/karaṇa + kṛta)
        "purva": {"stem": "ahi", "vacana": 1, "vibhakti": 3, "vivakza": True},
        "uttara": {"stem": "hata", "vacana": 1, "vivakza": True},
        "fired": ["2.1.32", "1.2.43", "2.4.26"],
        "surface": "अहिहतः",
    },
    {
        "label": "T1-suKApetaH-SK700-2.1.38",           # सुखात् अपेतः → सुखापेतः (pañcamī, apeta-gaṇa)
        "purva": {"stem": "suKa", "vacana": 1, "vibhakti": 5, "vivakza": True},
        "uttara": {"stem": "apeta", "vacana": 1, "vivakza": True},
        "fired": ["2.1.38", "1.2.43", "2.4.26"],
        "surface": "सुखापेतः",
    },
    {
        # स्तोकात् मुक्तः → स्तोकमुक्तः. NOTE: the classical aluk form स्तोकान्मुक्तः (the
        # pañcamī is RETAINED via 6.3.2 पञ्चम्याः स्तोकादिभ्यः) is not modelled — this
        # rule luks the pūrva sup like the others, so the surface is स्तोकमुक्तः. The
        # aluk exception is deferred (recorded in generator_status.md).
        "label": "T1-stokamuktaH-SK701-2.1.39",
        "purva": {"stem": "stoka", "vacana": 1, "vibhakti": 5, "vivakza": True},
        "uttara": {"stem": "mukta", "vacana": 1, "vivakza": True},
        "fired": ["2.1.39", "1.2.43", "2.4.26"],
        "surface": "स्तोकमुक्तः",
    },
    {
        "label": "T1-svargasidDaH-SK718-2.1.41",        # स्वर्गे सिद्धः → स्वर्गसिद्धः (saptamī, siddha-gaṇa)
        "purva": {"stem": "svarga", "vacana": 1, "vibhakti": 7, "vivakza": True},
        "uttara": {"stem": "sidDa", "vacana": 1, "vivakza": True},
        "fired": ["2.1.41", "1.2.43", "2.4.26"],
        "surface": "स्वर्गसिद्धः",
    },
    # ── T2: karmadhāraya (samānādhikaraṇa) + dvigu (saṅkhyā-pūrva) ──
    # KARMADHĀRAYA — both members the SAME case (samānādhikaraṇa), so the pūrva
    # carries ?viBakti_1 (not a 2–7 case) + the viśeṣaṇa/pūrvakāla role tag. 1.2.42
    # names it karmadhāraya (a ?tatpuruza sub-tag); it still declines paravalliṅga
    # (2.4.26) in the uttara's gender.
    {
        "label": "T2-nIlotpalam-SK736-2.1.57",          # नीलम् उत्पलम् → नीलोत्पलम् (viśeṣaṇa; napuṁsaka)
        "purva": {"stem": "nIla", "vacana": 1, "vibhakti": 1, "vivakza": True,
                  "tags": ["viSezaRa"]},
        "uttara": {"stem": "utpala", "vacana": 1, "vivakza": True},
        "fired": ["2.1.57", "1.2.42", "1.2.43", "2.4.26"],
        "surface": "नीलोत्पलम्",
    },
    {
        "label": "T2-kRSNasarpaH-SK736-2.1.57",         # कृष्णः सर्पः → कृष्णसर्पः (viśeṣaṇa; masc)
        "purva": {"stem": "kfzRa", "vacana": 1, "vibhakti": 1, "vivakza": True,
                  "tags": ["viSezaRa"]},
        "uttara": {"stem": "sarpa", "vacana": 1, "vivakza": True},
        "fired": ["2.1.57", "1.2.42", "1.2.43", "2.4.26"],
        "surface": "कृष्णसर्पः",
    },
    {
        "label": "T2-snAtAnuliptaH-SK726-2.1.49",        # स्नातः अनुलिप्तः → स्नातानुलिप्तः (pūrvakāla)
        "purva": {"stem": "snAta", "vacana": 1, "vibhakti": 1, "vivakza": True,
                  "tags": ["pUrvakAla"]},
        "uttara": {"stem": "anulipta", "vacana": 1, "vivakza": True},
        "fired": ["2.1.49", "1.2.42", "1.2.43", "2.4.26"],
        "surface": "स्नातानुलिप्तः",
    },
    {
        # कल्याणी + प्रियः → कल्याणप्रियः. 6.3.42 puṃvadbhāva: the fem viśeṣaṇa pūrva
        # takes its masc form (कल्याणी → कल्याण). The composer supplies कल्याण (the
        # masc form) + ?puMvat directly; 6.3.42 fires as the puṃvadbhāva saṁjñā
        # (the full ṅīp-strip derivation कल्याणी→कल्याण is deferred — see status).
        "label": "T2-kalyARapriyaH-SK746-6.3.42",
        "purva": {"stem": "kalyARa", "vacana": 1, "vibhakti": 1, "vivakza": True,
                  "tags": ["viSezaRa", "puMvat"]},
        "uttara": {"stem": "priya", "vacana": 1, "vivakza": True},
        "fired": ["2.1.57", "1.2.42", "6.3.42", "1.2.43", "2.4.26"],
        "surface": "कल्याणप्रियः",
    },
    # DVIGU — a saṅkhyā-pūrva tatpuruṣa. 2.1.52 forms + names it ?dvigu; a समाहार
    # (aggregate) dvigu is napuṁsaka singular (2.4.1); a go-final dvigu takes the
    # ṬaC samāsānta (5.4.92). The pūrva carries ?saMKyA (no vigraha vibhakti).
    {
        # पञ्च गावः (समाहारे) → पञ्चगवम्. 5.4.92 गोरतद्धितलुकि: go-final → ṬaC (गो+अ→गव);
        # 2.4.1 द्विगुरेकवचनम्: samāhāra → napuṁsaka sg (nom=acc अम्).
        "label": "T2-paYcagavam-SK731-2.4.1",
        "purva": {"stem": "paYcan", "vacana": 1, "vivakza": True, "tags": ["saMKyA"]},
        "uttara": {"stem": "go", "vacana": 1, "vivakza": True, "tags": ["samAhAra"]},
        "fired": ["2.1.52", "2.4.1", "5.4.92", "1.2.43", "2.4.26"],
        "surface": "पञ्चगवम्",
    },
    {
        # त्रयाणां लोकानां समाहारः → त्रिलोकम् (napuṁsaka sg, 2.4.1). tri carries ?saMKyA
        # intrinsically; a-stem uttara (लोक), no samāsānta. This same dvigu त्रि+लोक
        # declines FEMININE (ṅīप) → त्रिलोकी when strī is intended (see the real-dvigu
        # ṅīp test in test_samasa_tatpurusha.py), proving 2.1.52's ?dvigu drives both.
        # (त्रिभुवनम् — the plan's other example — is DEFERRED: त्रि's र would ṇatva-ise
        # bhuvana's न cross the pūrva/uttara boundary → त्रिभुवण; modelling the 8.4.3
        # पूर्वपदात्संज्ञायाम् restriction that blocks cross-member ṇatva in a non-saṁjñā
        # is a pre-existing ṇatva-engine gap, same family as चोरभयेन. See status.)
        "label": "T2-trilokam-SK731-2.4.1",
        "purva": {"stem": "tri", "vivakza": True},   # tri: ?saMKyA + nityabahuvacana
        "uttara": {"stem": "loka", "vacana": 1, "vivakza": True, "tags": ["samAhAra"]},
        "fired": ["2.1.52", "2.4.1", "1.2.43", "2.4.26"],
        "surface": "त्रिलोकम्",
    },
    # ── T3: nañ-tatpuruṣa (2.2.6 saṁjñā + 6.3.73/74 junction mutation of न) ──
    # The नञ् pūrva (avyaya naY, surface न) has NO vigraha vibhakti; it carries a
    # semantic sense (as the T0 avyaya-pūrvas svayam/sāmi did) so it rides through
    # the merge as a distinct ?pada member. 6.3.73/74 run in the samāsa pre-pass
    # member-window (bahiranga: -1, same window 2.2.6 fires in — the uttara stem's
    # first char is visible as `r`, the un-lukked pūrva sup skipped), so they DO
    # appear in the pre-pass trace and mutate न → अ / अन् before the main scan.
    {
        "label": "T3-abrAhmaNaH-SK757-6.3.73",     # न + ब्राह्मण → अब्राह्मणः (na→a before consonant)
        "purva": {"avyaya": "naY", "sem": "semantic_1", "vivakza": True},
        "uttara": {"stem": "brAhmaRa", "vacana": 1, "vivakza": True},
        "fired": ["2.2.6", "6.3.73", "1.2.43", "2.4.26"],
        "surface": "अब्राह्मणः",
    },
    {
        "label": "T3-anaSvaH-SK758-6.3.74",        # न + अश्व → अनश्वः (na→an before vowel, नुṭ)
        "purva": {"avyaya": "naY", "sem": "semantic_1", "vivakza": True},
        "uttara": {"stem": "aSva", "vacana": 1, "vivakza": True},
        "fired": ["2.2.6", "6.3.74", "1.2.43", "2.4.26"],
        "surface": "अनश्वः",
    },
    {
        "label": "T3-anajaH-SK758-6.3.74",         # न + अज → अनजः
        "purva": {"avyaya": "naY", "sem": "semantic_1", "vivakza": True},
        "uttara": {"stem": "aja", "vacana": 1, "vivakza": True},
        "fired": ["2.2.6", "6.3.74", "1.2.43", "2.4.26"],
        "surface": "अनजः",
    },
    # ── T4: prādi / ku tatpuruṣa (2.2.18 कुगतिप्रादयः) ──
    # The prādi/ku particle is the pūrva (an avyaya ?nipAta → 1.1.37, so its sup
    # luks; no vigraha vibhakti, like the नञ् of T3). It carries a semantic sense
    # ("sem") to ride through the merge as a distinct ?pada member. The compound
    # declines normally in the uttara's masc gender (2.4.26) → the राम paradigm.
    {
        "label": "T4-prAcAryaH-SK761-2.2.18",       # प्र + आचार्य → प्राचार्यः (prādi; a+ā→ā savarṇadīrgha)
        "purva": {"stem": "pra", "sem": "semantic_1", "vivakza": True},
        "uttara": {"stem": "AcArya", "vacana": 1, "vivakza": True},
        "fired": ["2.2.18", "1.2.43", "2.4.26"],
        "surface": "प्राचार्यः",
    },
    {
        "label": "T4-kupuruSaH-SK761-2.2.18",       # कु + पुरुष → कुपुरुषः (ku)
        "purva": {"stem": "ku", "sem": "semantic_1", "vivakza": True},
        "uttara": {"stem": "puruza", "vacana": 1, "vivakza": True},
        "fired": ["2.2.18", "1.2.43", "2.4.26"],
        "surface": "कुपुरुषः",
    },
    {
        "label": "T4-atimAlaH-SK761-2.2.18",  # अति + माल → अतिमालः (prādi)
        "purva": {"stem": "ati", "sem": "semantic_1", "vivakza": True},
        "uttara": {"stem": "mAla", "vacana": 1, "vivakza": True},
        "fired": ["2.2.18", "1.2.43", "2.4.26"],
        "surface": "अतिमालः",
    },
    {
        # NITYA-samāsa proof: 2.2.18 कुगतिप्रादयः is nitya (aswapada-vigraha), so it
        # forms WITHOUT any ?samAsa_vivakza — only the pūrva's semantic sense triggers
        # the pre-pass window. Neither member carries vivakza here (contrast every
        # other case above). प्र + आचार्य → प्राचार्यः.
        "label": "T4-prAcArya-nitya-SK761-2.2.18",
        "purva": {"stem": "pra", "sem": "semantic_1"},   # no vivakza
        "uttara": {"stem": "AcArya", "vacana": 1},       # no vivakza
        "fired": ["2.2.18", "1.2.43", "2.4.26"],
        "surface": "प्राचार्यः",
    },
    {
        # GATI-saṁjñā (SK762/1.4.61 ऊर्यादिच्विडाचश्च): the ūryādi word ऊरी (?UryAdi, NOT
        # intrinsically gati) is given the गति saṁjñā by the real rule 1.4.61, which then
        # feeds the gati arm of 2.2.18 → ऊरी + कृत = ऊरीकृतम् (napuṁsaka, कृत is napum, as
        # स्वयंकृतम्). The fired trace includes 1.4.61 — proving the gati saṁjñā is real,
        # not an intrinsic ?gati tag. Nitya: no vivakza (only the pūrva's semantic sense).
        "label": "T4-UrIkftam-SK762-1.4.61",
        "purva": {"stem": "UrI", "sem": "semantic_1"},   # ?UryAdi, no vivakza
        "uttara": {"stem": "kfta", "vacana": 1},
        "fired": ["1.4.61", "2.2.18", "1.2.43", "2.4.26"],
        "surface": "ऊरीकृतम्",
    },
    # ── T5: tatpuruṣa samāsānta (टच्/ṬaC via ?samasanta_TaC + _insert_samasanta) ──
    # A rājan-final tatpuruṣa (5.4.91) takes टच् → an a-stem: परम + राजन् → परमराजः
    # (न-lopa 6.4.144, exactly as the avyayībhāva उपराजम्). महत् + राजन् → महाराजः via
    # 6.3.46 आन्महतः (महत् → महा) + 5.4.91. Modelled as karmadhārayas (परम/महत्
    # viśeṣaṇa, viBakti_1), so 2.1.57 + 1.2.42 also fire. Decline masc a-stem.
    {
        "label": "T5-paramarAjaH-SK788-5.4.91",     # परम + राजन् → परमराजः (टच्, rājan-arm)
        "purva": {"stem": "parama", "vacana": 1, "vibhakti": 1, "vivakza": True,
                  "tags": ["viSezaRa"]},
        "uttara": {"stem": "rAjan", "vacana": 1, "vivakza": True},
        "fired": ["2.1.57", "1.2.42", "5.4.91", "1.2.43", "2.4.26"],
        "surface": "परमराजः",
    },
    {
        "label": "T5-mahArAjaH-SK807-6.3.46",        # महत् + राजन् → महाराजः (6.3.46 महत्→महा + 5.4.91 टच्)
        "purva": {"stem": "mahat", "vacana": 1, "vibhakti": 1, "vivakza": True,
                  "tags": ["viSezaRa"]},
        "uttara": {"stem": "rAjan", "vacana": 1, "vivakza": True},
        "fired": ["2.1.57", "1.2.42", "6.3.46", "5.4.91", "1.2.43", "2.4.26"],
        "surface": "महाराजः",
    },
    {
        # पुण्या रात्रिः → पुण्यरात्रः (karmadhāraya). SK787/5.4.87 अहस्सर्वैकदेशसंख्यातपुण्याच्च
        # रात्रेः: the रात्रि-final tatpuruṣa after पुण्य takes the samāsānta → रात्र (i-lopa
        # 6.4.148, as giri→उपगिरम्); SK814/2.4.29 रात्राह्नाहाः पुंसि then makes it MASCULINE
        # (overriding रात्रि's native fem + 2.4.26) → पुण्यरात्रः, declining as the राम a-stem.
        # This is the real surface for both 5.4.87 and the रात्रि arm of 2.4.29.
        "label": "T5-puRyarAtraH-SK787-5.4.87",
        "purva": {"stem": "puRya", "vacana": 1, "vibhakti": 1, "vivakza": True,
                  "tags": ["viSezaRa"]},
        "uttara": {"stem": "rAtri", "vacana": 1, "vivakza": True},
        "fired": ["2.1.57", "1.2.42", "5.4.87", "2.4.29", "1.2.43", "2.4.26"],
        "surface": "पुण्यरात्रः",
    },
    {
        # SK751/2.2.38 कडाराः कर्मधारये — a kaḍāra-gaṇa viśeṣaṇa (कडार "brown", ?kaqAra)
        # OPTIONALLY leads a karmadhāraya (an-yatarasyām). Modelled as a saṁjñā tag
        # (+kaqAra_pUrva); the physical reordering (2.2.30) is deferred, so the surface
        # is the input-order karmadhāraya कडारपुरुषः. Proves 2.2.38 fires (was untested).
        "label": "T2-kaqArapuruSaH-SK751-2.2.38",
        "purva": {"stem": "kaqAra", "vacana": 1, "vibhakti": 1, "vivakza": True,
                  "tags": ["viSezaRa"]},
        "uttara": {"stem": "puruza", "vacana": 1, "vivakza": True},
        "fired": ["2.1.57", "1.2.42", "2.2.38", "2.4.26"],
        "surface": "कडारपुरुषः",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# Bahuvrīhi B0 (bahuvrihi_plan.md) — EXOCENTRIC compound: declines in an EXTERNAL
# referent's gender (anyapadārtha, SK830/2.2.24), NOT the uttara's (contrast
# tatpuruṣa SK812/2.4.26). Both members prathamānta (?viBakti_1) + upasarjana. The
# driver (test_samasa_bahuvrihi.py) supplies ?bahuvrIhi_vivakza on both members, the
# referent case/vacana on the uttara, and "referent_linga" → the uttara's gender is
# overridden to the referent liṅga (?referent_pum/strI/napum). Structure/fired levels
# only here; the gender + vibhakti sweeps live in the driver.
# ══════════════════════════════════════════════════════════════════════════════
samasa_bv_tests = [
    {
        # पीत(1) + अम्बर(1, n.) → पीताम्बरः "yellow-garment-having" (m., of Viṣṇu). The
        # referent is masc → the neuter अम्बर declines as a masc a-stem.
        "label": "B0-pItAmbaraH-SK830-2.2.24",
        "purva": {"stem": "pIta", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "ambara", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "1.2.43"],
        "surface": "पीताम्बरः",
    },
    {
        # प्राप्त(1, niṣṭhā) + उदक(1, n.) → प्राप्तोदकः (ग्रामः) "having-obtained-water"
        # (m.). प्राप्त, a niṣṭhā, is already pūrva (SK899/2.2.36); referent ग्राम masc.
        "label": "B0-prAptodakaH-SK830-2.2.24",
        "purva": {"stem": "prApta", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "udaka", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "1.2.43"],
        "surface": "प्राप्तोदकः",
    },

    # ── B1 puṁvadbhāva (SK831/6.3.34 + prohibitions 6.3.37/38/40/41) ──
    # A feminine pūrva → its masculine bhāṣitapuṁska form before a fem uttara. The
    # composer supplies the masc form (दीर्घ) + ?puMvat for the applies-case; 6.3.34
    # fires as the saṁjñā (real ṅīp/ṭāp-strip deferred, as 6.3.42). The prohibitions
    # keep the fem form and OVERRIDE 6.3.34 (fem stem + a blocker-class tag baked into
    # the pratipadika). ?uttara_strI marks the uttara's vigraha femininity (its native
    # ?strI is overridden to the referent liṅga by the B0 anyapadārtha rule).
    {
        # दीर्घे जङ्घे यस्याः → दीर्घजङ्घा (दीर्घा → दीर्घ); fem referent, uttara a-stem base + ṭāp.
        "label": "B1-dIrGajaNGA-SK831-6.3.34",
        "purva": {"stem": "dIrGa", "vacana": 1, "vibhakti": 1, "tags": ["puMvat"]},
        "uttara": {"stem": "jaNGa", "vacana": 1, "vibhakti": 1, "tags": ["uttara_strI"]},
        "referent_linga": "strI",
        "uttara_strI_abs": True,
        "fired": ["2.2.24", "6.3.34", "1.2.43"],
        "surface": "दीर्घजङ्घा",
    },
    {
        # SK842/6.3.41 जातेश्च — ब्राह्मणी (jāti) stays fem: ब्राह्मणीभार्यः (masc referent).
        "label": "B1-brAhmaRIBAryaH-SK842-6.3.41",
        "purva": {"stem": "brAhmaRI", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "BArya", "vacana": 1, "vibhakti": 1, "tags": ["uttara_strI"]},
        "referent_linga": "pum",
        "fired": ["2.2.24", "6.3.41", "1.2.43"],
        "surface": "ब्राह्मणीभार्यः",
    },
    {
        # SK839/6.3.38 संज्ञापूरण्योश्च — दत्ता (name) stays fem: दत्ताभार्यः.
        "label": "B1-dattABAryaH-SK839-6.3.38",
        "purva": {"stem": "dattA", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "BArya", "vacana": 1, "vibhakti": 1, "tags": ["uttara_strI"]},
        "referent_linga": "pum",
        "fired": ["2.2.24", "6.3.38", "1.2.43"],
        "surface": "दत्ताभार्यः",
    },
    {
        # SK838/6.3.37 न कोपधायाः — पाचिका (k-penult) stays fem: पाचिकाभार्यः.
        "label": "B1-pAcikABAryaH-SK838-6.3.37",
        "purva": {"stem": "pAcikA", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "BArya", "vacana": 1, "vibhakti": 1, "tags": ["uttara_strI"]},
        "referent_linga": "pum",
        "fired": ["2.2.24", "6.3.37", "1.2.43"],
        "surface": "पाचिकाभार्यः",
    },
    {
        # SK841/6.3.40 स्वाङ्गाच्चेतः — सुकेशी (svāṅga ī) stays fem: सुकेशीभार्यः.
        "label": "B1-sukeSIBAryaH-SK841-6.3.40",
        "purva": {"stem": "sukeSI", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "BArya", "vacana": 1, "vibhakti": 1, "tags": ["uttara_strI"]},
        "referent_linga": "pum",
        "fired": ["2.2.24", "6.3.40", "1.2.43"],
        "surface": "सुकेशीभार्यः",
    },

    # ── B2 additional formation types (saha 2.2.28 + 6.3.82/6.3.83; diś 2.2.26) ──
    # saha is an indeclinable pūrva (SK830/2.2.24 needs ?viBakti_1, so 2.2.28 forms it);
    # it takes a sup (which luks) so 6.3.82 (main-scan, optional) can see the (saha|sup)
    # window and fork सपुत्रः/सहपुत्रः. In a benediction (?ASis) saha stays (6.3.83).
    {
        # पुत्रेण सह = सपुत्रः / सहपुत्रः (SK849/6.3.82 optional saha→sa).
        "label": "B2-saputraH-SK848-2.2.28",
        "purva": {"stem": "saha", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "putra", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.28", "1.2.43"],
        "surfaces": ["सपुत्रः", "सहपुत्रः"],
    },
    {
        # स्वस्ति राज्ञे सहपुत्राय — āśis (benediction): saha stays (SK850/6.3.83), dative.
        "label": "B2-sahaputrAya-SK850-6.3.83",
        "purva": {"stem": "saha", "vacana": 1, "vibhakti": 1, "tags": ["ASis"]},
        "uttara": {"stem": "putra", "vacana": 1, "vibhakti": 4},
        "referent_linga": "pum",
        "fired": ["2.2.28", "6.3.83", "1.2.43"],
        "surface": "सहपुत्राय",
    },
    {
        # दक्षिणस्याः पूर्वस्याश्च दिशोरन्तरालम् = दक्षिणपूर्वा (SK845/2.2.26; fem diś referent).
        "label": "B2-dakziRapUrvA-SK845-2.2.26",
        "purva": {"stem": "dakziRa_dik", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "pUrva_dik", "vacana": 1, "vibhakti": 1},
        "referent_linga": "strI",
        "uttara_strI_abs": True,
        "fired": ["2.2.26", "1.2.43"],
        "surface": "दक्षिणपूर्वा",
    },

    # ── B3 samāsānta कप् (SK891/5.4.154 optional, SK889/5.4.151 uras, SK893/5.4.155) ──
    # The कप् affix is inserted by the generalized _insert_samasanta (?samasanta_kap →
    # kap). 5.4.154's विभाषा is modelled as a VIVAKṢĀ (not an engine fork): कप् is added
    # exactly when the composer marks the uttara ?kap_vivakzA — बहुयशस्कः WITH the tag,
    # बहुयशाः WITHOUT it (the canonical SK891 pair; the masc s-stem dīrgha now works, see
    # the 6.4.14 `-as` arm relaxation).
    {
        # बहूनि यशांसि यस्य + ?kap_vivakzA = बहुयशस्कः (SK891/5.4.154 कप्).
        "label": "B3-bahuyaSaskaH-SK891-5.4.154",
        "purva": {"stem": "bahu", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "yaSas", "vacana": 1, "vibhakti": 1, "tags": ["kap_vivakzA"]},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.154", "1.2.43"],
        "surface": "बहुयशस्कः",
    },
    {
        # बहूनि यशांसि यस्य, NO ?kap_vivakzA = बहुयशाः (5.4.154 does not fire — no कप्;
        # the 6.4.14 upadhā-dīrgha gives the masc as-stem nom sg).
        "label": "B3-bahuyaSAH-noKap-SK891-5.4.154",
        "purva": {"stem": "bahu", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "yaSas", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "1.2.43"],
        "not_fired": ["5.4.154"],
        "surface": "बहुयशाः",
    },
    {
        # SK893/5.4.155 न संज्ञायाम् — even WITH ?kap_vivakzA a NAME takes no kap: बहुयशाः.
        "label": "B3-bahuyaSAH-saMjYA-SK893-5.4.155",
        "purva": {"stem": "bahu", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "yaSas", "vacana": 1, "vibhakti": 1,
                   "tags": ["kap_vivakzA", "saMjYA"]},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.155", "1.2.43"],
        "not_fired": ["5.4.154"],
        "surface": "बहुयशाः",
    },
    {
        # व्यूढमुरो यस्य = व्यूढोरस्कः (SK889/5.4.151 उरःप्रभृतिभ्यः कप्, nitya — उरस्).
        "label": "B3-vyUQoraskaH-SK889-5.4.151",
        "purva": {"stem": "vyUQa", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "uras", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.151", "1.2.43"],
        "surface": "व्यूढोरस्कः",
    },
    {
        # प्रियं सर्पिर्यस्य = प्रियसर्पिष्कः (SK889/5.4.151 उरःप्रभृति gaṇa member सर्पिस्; स्→ष्).
        "label": "B3-priyasarpizkaH-SK889-5.4.151",
        "purva": {"stem": "priya", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "sarpis", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.151", "1.2.43"],
        "surface": "प्रियसर्पिष्कः",
    },
    {
        # बह्व्यः कुमार्यो यस्य = बहुकुमारीकः (SK833/5.4.153 नद्यृतश्च कप्; nadī ?NI uttara).
        "label": "B3-bahukumArIkaH-SK833-5.4.153",
        "purva": {"stem": "bahu", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "kumArI", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.153", "1.2.43"],
        "surface": "बहुकुमारीकः",
    },
    {
        # बह्व्यो मातरो यस्य = बहुमातृकः (SK833/5.4.153 नद्यृतश्च कप्; ऋ-final uttara).
        "label": "B3-bahumAtfkaH-SK833-5.4.153",
        "purva": {"stem": "bahu", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "mAtf", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.153", "1.2.43"],
        "surface": "बहुमातृकः",
    },

    # ── B3 samāsānta ṣac / ap / ic (SK852/5.4.113, SK854/5.4.115, SK855/5.4.117,
    # SK867/5.4.128). A saṅkhyā pūrva (dvi) carries NO vacana — its ?nityadvivacana
    # conflicts with a forced vacana_1 (→ द्व); the referent's vacana goes on the uttara.
    {
        # दीर्घे सक्थिनी यस्य = दीर्घसक्थः (SK852/5.4.113 ṣac; i-lopa 6.4.148).
        "label": "B3-dIrGasakTaH-SK852-5.4.113",
        "purva": {"stem": "dIrGa", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "sakTi", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.113", "1.2.43"],
        "surface": "दीर्घसक्थः",
    },
    {
        # पञ्चाङ्गुलयो यस्य दारु = पञ्चाङ्गुलम् (SK853/5.4.114 अङ्गुलेर्दारुणि षच्; दारु sense, n.).
        # पञ्चन् (the number stem) → पञ्च: its final न् drops (8.2.7) once the pūrva sup luks.
        "label": "B3-paYcANgulam-SK853-5.4.114",
        "purva": {"stem": "paYcan", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "aNguli", "vacana": 1, "vibhakti": 1, "tags": ["dAru"]},
        "referent_linga": "napum",
        "fired": ["2.2.24", "5.4.114", "1.2.43"],
        "surface": "पञ्चाङ्गुलम्",
    },
    {
        # द्वौ मूर्धानौ यस्य = द्विमूर्धः (SK854/5.4.115 ṣa; न-lopa 6.4.144).
        "label": "B3-dvimUrDaH-SK854-5.4.115",
        "purva": {"stem": "dvi", "vibhakti": 1},
        "uttara": {"stem": "mUrDan", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.115", "1.2.43"],
        "surface": "द्विमूर्धः",
    },
    {
        # बहिर्लोमानि यस्य = बहिर्लोमः (SK855/5.4.117 ap; न-lopa 6.4.144; र्ल doubling optional).
        "label": "B3-bahirlomaH-SK855-5.4.117",
        "purva": {"stem": "bahis", "vibhakti": 1},
        "uttara": {"stem": "loman", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.117", "1.2.43"],
        "surfaces": ["बहिर्लोमः", "बहिर्ल्लोमः"],
    },
    {
        # द्वौ दण्डौ यस्मिन् प्रहरणे = द्विदण्डि (SK867/5.4.128 ic; a-lopa 6.4.148; n. weapon).
        "label": "B3-dvidaRqi-SK867-5.4.128",
        "purva": {"stem": "dvi", "vibhakti": 1},
        "uttara": {"stem": "daRqa", "vacana": 1, "vibhakti": 1},
        "referent_linga": "napum",
        "fired": ["2.2.24", "5.4.128", "1.2.43"],
        "surface": "द्विदण्डि",
    },

    # ── B4 samāsānta ādeśa (SK868/5.4.129 jānu→jñu) — pre-pass uttara-substitution ──
    {
        # प्रगते जानुनी यस्य = प्रज्ञुः (SK868/5.4.129 जानु→ज्ञु; u-stem).
        "label": "B4-prajYuH-SK868-5.4.129",
        "purva": {"stem": "pra", "vibhakti": 1},
        "uttara": {"stem": "jAnu", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.129", "1.2.43"],
        "surface": "प्रज्ञुः",
    },
    {
        # ऊर्ध्वे जानुनी यस्य = ऊर्ध्वज्ञुः / ऊर्ध्वजानुः (SK869/5.4.130 optional जानु→ज्ञु).
        "label": "B4-UrDvajYuH-SK869-5.4.130",
        "purva": {"stem": "UrDva", "vibhakti": 1},
        "uttara": {"stem": "jAnu", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.130", "1.2.43"],
        "surfaces": ["ऊर्ध्वज्ञुः", "ऊर्ध्वजानुः"],
    },
    {
        # सुरभिर्गन्धो यस्य = सुगन्धिः (SK874/5.4.135 गन्ध final → इत्).
        "label": "B4-sugandhiH-SK874-5.4.135",
        "purva": {"stem": "su_pUrva", "vibhakti": 1},
        "uttara": {"stem": "gandha", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.135", "1.2.43"],
        "surface": "सुगन्धिः",
    },
    {
        # शोभनं हृदयं यस्य = सुहृत् / सुहृद् (SK888/5.4.150 हृदय→हृद्; द्→त्/द् वाऽवसाने 8.4.56).
        "label": "B4-suhft-SK888-5.4.150",
        "purva": {"stem": "su_pUrva", "vibhakti": 1},
        "uttara": {"stem": "hfdaya", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.150", "1.2.43"],
        "surfaces": ["सुहृत्", "सुहृद्"],
    },
    {
        # द्वौ पादौ यस्य = द्विपात् / द्विपाद् (SK879/5.4.140 पाद→पाद् consonant stem).
        "label": "B4-dvipAt-SK879-5.4.140",
        "purva": {"stem": "dvi", "vibhakti": 1},
        "uttara": {"stem": "pAda", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.140", "1.2.43"],
        "surfaces": ["द्विपात्", "द्विपाद्"],
    },
    {
        # शोभनं धनुर्यस्य = सुधन्वा (SK870/5.4.132 धनुस्→धन्वन् अनङ्, n-stem → धन्वा).
        "label": "B4-suDanvA-SK870-5.4.132",
        "purva": {"stem": "su_pUrva", "vibhakti": 1},
        "uttara": {"stem": "Danus", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.132", "1.2.43"],
        "surface": "सुधन्वा",
    },
    {
        # कल्याणो धर्मोऽस्य = कल्याणधर्मा (SK863/5.4.124 अनिच्, धर्म→धर्मन् n-stem → धर्मा).
        "label": "B4-kalyARaDarmA-SK863-5.4.124",
        "purva": {"stem": "kalyARa", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "Darma", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.124", "1.2.43"],
        "surface": "कल्याणधर्मा",
    },
    {
        # शोभना प्रजा यस्य = सुप्रजाः (SK862/5.4.122 नित्यमसिच्; प्रजा + असिच् → सुप्रजस् →
        # nom sg masc सुप्रजाः via the widened 6.4.14 `-as` dīrgha). `-Ap` clear as usual.
        "label": "B3-suprajAH-SK862-5.4.122",
        "purva": {"stem": "su_pUrva", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "prajA", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.122", "1.2.43"],
        "surface": "सुप्रजाः",
    },
    {
        # शोभना मेधा यस्य = सुमेधाः (SK862/5.4.122 असिच्, मेधा arm).
        "label": "B3-sumeDAH-SK862-5.4.122",
        "purva": {"stem": "su_pUrva", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "meDA", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.122", "1.2.43"],
        "surface": "सुमेधाः",
    },
    {
        # अविद्यमाना प्रजा यस्य = अप्रजाः — the NAÑ arm of SK862/5.4.122. The nañ pūrva
        # carries an intrinsic ?naY, so 6.3.73 नलोपो नञः turns न→अ before the consonant
        # of प्रजा; 5.4.122 gates on ?naY (NOT "=na") because 6.3.73 rewrites the pūrva first.
        "label": "B3-aprajAH-naY-SK862-5.4.122",
        "purva": {"avyaya": "naY", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "prajA", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.122", "6.3.73", "1.2.43"],
        "surface": "अप्रजाः",
    },
    {
        # अविद्यमाना मेधा यस्य = अमेधाः (nañ arm, मेधा).
        "label": "B3-ameDAH-naY-SK862-5.4.122",
        "purva": {"avyaya": "naY", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "meDA", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.122", "6.3.73", "1.2.43"],
        "surface": "अमेधाः",
    },
    {
        # युवतिर्जाया यस्य = युवजानिः (SK872/5.4.134 जायाया निङ्; जाया→जानि). The rule's
        # `-Ap` clear is what gives the visarga — जाया's ?Ap would else elide the su.
        "label": "B4-yuvajAniH-SK872-5.4.134",
        "purva": {"stem": "yuvan", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "jAyA", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.134", "1.2.43"],
        "surface": "युवजानिः",
    },
    {
        # उन्नता नासिकाऽस्य = उन्नसः (SK858/5.4.119 उपसर्गाच्च अच्; नासिका→नस). उद्नसः is the
        # other fork of 8.4.45 यरोऽनुनासिके (वा). उद् has no ṛ/ṣ/r, so no ṇatva.
        "label": "B3-unnasaH-SK858-5.4.119",
        "purva": {"stem": "ud", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "nAsikA", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.119", "1.2.43"],
        "surfaces": ["उन्नसः", "उद्नसः"],
    },
    {
        # प्रणता नासिकाऽस्य = प्रणसः — SK859/8.4.28 उपसर्गाद्बहुलम् CROSS-COMPOUND ṇatva: प्र's
        # र ṇatva-ises the न of the नस् across the pūrva/uttara boundary. 5.4.119 marks the
        # substitute ?nas_AdeSa (propagated through the (uttara|sup) merge), and 8.4.28 keys
        # on it to set ?samasta_Ratva → ?samasta_Ratva_pada → arm B of 8.4.1/8.4.2.
        "label": "B3-praRasaH-SK859-8.4.28",
        "purva": {"stem": "pra", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "nAsikA", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.119", "1.2.43"],
        "surface": "प्रणसः",
    },
    {
        # द्रुरिव नासिकाऽस्य = द्रुणसः — SK856/5.4.118 (नासिका→नस in a SAṀJÑĀ) + SK857/8.4.3
        # पूर्वपदात्संज्ञायामगः cross-compound ṇatva (द्रु's र → the ण). The saṁjñā path is kept
        # disjoint from the upasarga path via ?saMjYA_nas (vs ?nas_AdeSa for 8.4.28).
        "label": "B3-druRasaH-SK856-5.4.118",
        "purva": {"stem": "dru", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "nAsikA", "vacana": 1, "vibhakti": 1, "tags": ["saMjYA"]},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.118", "1.2.43"],
        "surface": "द्रुणसः",
    },
    {
        # अजातककुत् type = प्राप्तककुत् / प्राप्तककुद् (SK884/5.4.146 ककुद final-lopa; 8.4.56).
        "label": "B4-prAptakakut-SK884-5.4.146",
        "purva": {"stem": "prApta", "vacana": 1, "vibhakti": 1},
        "uttara": {"stem": "kakuda", "vacana": 1, "vibhakti": 1},
        "referent_linga": "pum",
        "fired": ["2.2.24", "5.4.146", "1.2.43"],
        "surfaces": ["प्राप्तककुत्", "प्राप्तककुद्"],
    },
]
