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
        "label": "S1A-upakRSNam-samIpa",          # समीप, a-stem → 2.4.83 am
        "purva": {"avyaya": "upa_avyaya", "sem": "semantic_samIpa"},
        "uttara": {"stem": "kfzRa", "vacana": 1},
        "fired": ["2.1.6", "1.2.43"],
        "surface": "उपकृष्णम्",
    },
    {
        "label": "S1A-adhihari-vibhakti",         # विभक्ति, i-stem → 1.1.41 → 2.4.82 luk
        "purva": {"avyaya": "aDi_avyaya", "sem": "semantic_vibhakti"},
        "uttara": {"stem": "hari", "vacana": 1},
        "fired": ["2.1.6", "1.2.43"],
        "surface": "अधिहरि",
    },
    # ── S1B: 2.1.6 further sense (atyaya), 2.1.7 yathā, 2.1.8 yāvat ──
    {
        "label": "S1B-atihimam-atyaya",           # अत्यय, a-stem → am
        "purva": {"avyaya": "ati_avyaya", "sem": "semantic_atyaya"},
        "uttara": {"stem": "hima", "vacana": 1},
        "fired": ["2.1.6", "1.2.43"],
        "surface": "अतिहिमम्",
    },
    {
        "label": "S1B-yathASakti-2.1.7",          # यथा (anatikrama), i-stem fem → luk
        "purva": {"avyaya": "yaTA", "sem": "semantic_yaTArTa"},
        "uttara": {"stem": "Sakti", "vacana": 1},
        "fired": ["2.1.7", "1.2.43"],
        "surface": "यथाशक्ति",
    },
    {
        "label": "S1B-yAvajjIvam-2.1.8",          # यावत् (avadhāraṇa), a-stem → am + t→j sandhi
        "purva": {"avyaya": "yAvat", "sem": "semantic_avaDAraRa"},
        "uttara": {"stem": "jIva", "vacana": 1},
        "fired": ["2.1.8", "1.2.43"],
        "surface": "यावज्जीवम्",
    },
    # ── S1B: 2.1.9 / 2.1.10 (NOUN-pūrva, avyaya is the uttara; needs 2.4.71) ──
    {
        "label": "S1B-SAkaprati-2.1.9",           # śāka (mātrā) + prati; prati i-stem → luk
        "purva": {"stem": "SAka", "vacana": 1, "sem": "semantic_mAtrA"},
        "uttara": {"avyaya": "prati_avyaya"},
        "fired": ["2.1.9", "1.2.43"],
        "surface": "शाकप्रति",
    },
    {
        "label": "S1B-akzapari-2.1.10",           # akṣa + pari (structural nitya → vivakza)
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
        "label": "S2-apagrAmam-2.1.12",
        "purva": {"avyaya": "apa_avyaya", "sem": "semantic_varjana", "dir": "para", "vivakza": True},
        "uttara": {"stem": "grAma", "vacana": 1, "vivakza": True},
        "fired": ["1.4.88", "2.3.10", "2.1.12", "1.2.43"],
        "surface": "अपग्रामम्",
    },
    {
        # ā + samudra: pañcamī via A + semantic_maryAdA → 1.4.89 → 2.3.10.
        "label": "S2-Asamudram-2.1.13",
        "purva": {"avyaya": "AN_avyaya", "sem": "semantic_maryAdA", "dir": "para", "vivakza": True},
        "uttara": {"stem": "samudra", "vacana": 1, "vivakza": True},
        "fired": ["1.4.89", "2.3.10", "2.1.13", "1.2.43"],
        "surface": "आसमुद्रम्",
    },
    {
        "label": "S2-pratyagni-2.1.14",           # prati + agni (ābhimukhya), i-stem → luk + sandhi
        "purva": {"avyaya": "prati_avyaya", "vivakza": True},
        "uttara": {"stem": "agni", "vacana": 1, "vivakza": True},
        "fired": ["2.1.14", "1.2.43"],
        "surface": "प्रत्यग्नि",
    },
    {
        "label": "S2-anuvanam-2.1.15",            # anu (samayā) + vana, a-stem → am
        "purva": {"avyaya": "anu_avyaya", "sem": "semantic_samayA", "vivakza": True},
        "uttara": {"stem": "vana", "vacana": 1, "vivakza": True},
        "fired": ["2.1.15", "1.2.43"],
        "surface": "अनुवनम्",
    },
    {
        "label": "S2-anugaNgam-2.1.16",           # anu (āyāma) + gaṅgā, ā-stem → napum → hrasva → am
        "purva": {"avyaya": "anu_avyaya", "sem": "semantic_AyAma", "vivakza": True},
        "uttara": {"stem": "gaNgA", "vacana": 1, "vivakza": True},
        "fired": ["2.1.16", "1.2.43"],
        "surface": "अनुगङ्गम्",
    },
    {
        "label": "S2-dvimuni-2.1.19",             # dvi + muni (vaṁśya), i-stem → luk
        "purva": {"stem": "dvi", "vivakza": True},   # dvi: nityadvivacana — no forced vacana
        "uttara": {"stem": "muni", "vacana": 1, "vivakza": True, "tags": ["vaMSya"]},
        "fired": ["2.1.19", "1.2.43"],
        "surface": "द्विमुनि",
    },
    {
        "label": "S2-dvigaNgam-2.1.20",           # dvi + gaṅgā (nadī), ā-stem → hrasva → am
        "purva": {"stem": "dvi", "vivakza": True},   # dvi: nityadvivacana — no forced vacana
        "uttara": {"stem": "gaNgA", "vacana": 1, "vivakza": True, "tags": ["nadI_saMjYA"]},
        "fired": ["2.1.20", "1.2.43"],
        "surface": "द्विगङ्गम्",
    },
    # ── S2 negative: विभाषा is "only when intended" — WITHOUT samAsa_vivakza no
    #    compound forms (prati + agni stay as separate words). ──
    {
        "label": "S2-pratyagni-no-vivakza",
        "purva": {"avyaya": "prati_avyaya"},
        "uttara": {"stem": "agni", "vacana": 1},
        "fired": [],
        "no_samasa": True,
    },
    # ── S3/S4: samāsānta — rule-driven ?samasanta_TaC (5.4.107–112) ──
    {
        "label": "S3-upaSaradam-5.4.107",         # upa + śarad → TaC → उपशरदम्
        "purva": {"avyaya": "upa_avyaya", "sem": "semantic_samIpa"},
        "uttara": {"stem": "Sarad", "vacana": 1},
        "fired": ["2.1.6", "1.2.43", "5.4.107"],
        "surface": "उपशरदम्",
    },
    {
        "label": "S4-upamanasam-5.4.107-gana",    # upa + manas (śaradādi s-stem) → TaC → उपमनसम्
        "purva": {"avyaya": "upa_avyaya", "sem": "semantic_samIpa"},
        "uttara": {"stem": "manas", "vacana": 1},
        "fired": ["2.1.6", "1.2.43", "5.4.107"],
        "surface": "उपमनसम्",
    },
    {
        "label": "S4-uparAjam-5.4.108",           # upa + rājan (an-final) → TaC + 6.4.144 → उपराजम्
        "purva": {"avyaya": "upa_avyaya", "sem": "semantic_samIpa"},
        "uttara": {"stem": "rAjan", "vacana": 1},
        "fired": ["2.1.6", "1.2.43", "5.4.108"],
        "surface": "उपराजम्",
    },
    {
        "label": "S4-upanadam-5.4.110",           # upa + nadī (ī-fem) → TaC → उपनदम्
        "purva": {"avyaya": "upa_avyaya", "sem": "semantic_samIpa"},
        "uttara": {"stem": "nadI", "vacana": 1},
        "fired": ["2.1.6", "1.2.43", "5.4.110"],
        "surface": "उपनदम्",
    },
    {
        "label": "S4-upasamiDam-5.4.111",         # upa + samidh (jhay-final) → TaC → उपसमिधम्
        "purva": {"avyaya": "upa_avyaya", "sem": "semantic_samIpa"},
        "uttara": {"stem": "samiD", "vacana": 1},
        "fired": ["2.1.6", "1.2.43", "5.4.111"],
        "surface": "उपसमिधम्",
    },
    {
        "label": "S4-upagiram-5.4.112",           # upa + giri (Senaka) → TaC → उपगिरम्
        "purva": {"avyaya": "upa_avyaya", "sem": "semantic_samIpa"},
        "uttara": {"stem": "giri", "vacana": 1},
        "fired": ["2.1.6", "1.2.43", "5.4.112"],
        "surface": "उपगिरम्",
    },
    {
        # upa + carman (napuṁsaka an-stem): 5.4.109 अन्यतरस्याम् — TaC OPTIONAL →
        # the samāsa pre-pass forks: उपचर्मम् (TaC) / उपचर्म (no TaC).
        "label": "S4-upacarma-5.4.109-fork",
        "purva": {"avyaya": "upa_avyaya", "sem": "semantic_samIpa"},
        "uttara": {"stem": "carman", "vacana": 1},
        "fired": ["2.1.6", "1.2.43", "5.4.109"],
        "surfaces": ["उपचर्म", "उपचर्मम्"],
    },
    # ── S3: 6.3.81 अव्ययीभावे चाकाले — saha → sa (non-kāla) ──
    {
        "label": "S3-sacakram-6.3.81",            # saha (yaugapadya) + cakra → सचक्रम् (saha→sa)
        "purva": {"stem": "saha", "sem": "semantic_yOgapadya", "vivakza": True},
        "uttara": {"stem": "cakra", "vacana": 1, "vivakza": True},
        "fired": ["2.1.6", "1.2.43"],             # 6.3.81 is a main-scan rule (not in pre-pass trace)
        "surface": "सचक्रम्",
    },
    # ── S3: 2.4.84 तृतीयासप्तम्योर्बहुलम् — bahula am for tṛtīyā/saptamī (optional fork) ──
    {
        "label": "S3-upakRSNam-bahula-2.4.84",    # upa + kṛṣṇa (saptamī) → उपकृष्णम् / उपकृष्णे
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
        "label": "T0-kRSNaSritaH-2.1.24",         # कृष्णं श्रितः → कृष्णश्रितः (nom sg)
        "purva": {"stem": "kfzRa", "vacana": 1, "vibhakti": 2, "vivakza": True},
        "uttara": {"stem": "Srita", "vacana": 1, "vivakza": True},
        "fired": ["2.1.24", "1.2.43", "2.4.26"],
        "surface": "कृष्णश्रितः",
    },
    # negative: WITHOUT ?samAsa_vivakza no tatpuruṣa forms (only-when-intended).
    {
        "label": "T0-kRSNaSrita-no-vivakza",
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
        "label": "T0-svayaMkRtam-2.1.25",
        "purva": {"avyaya": "svayam", "sem": "semantic_1", "vivakza": True},
        "uttara": {"stem": "kfta", "vacana": 1, "vivakza": True},
        "fired": ["2.1.25", "1.2.43", "2.4.26"],
        "surfaces": ["स्वयंकृतम्", "स्वयङ्कृतम्"],
    },
    {
        "label": "T0-KawvArUQaH-2.1.26",          # खट्वा (dvitīyā, kṣepa) + रूढ → खट्वारूढः
        "purva": {"stem": "KawvA", "vacana": 1, "vibhakti": 2, "sem": "semantic_kzepa"},
        "uttara": {"stem": "rUQa", "vacana": 1},
        "fired": ["2.1.26", "1.2.43", "2.4.26"],
        "surface": "खट्वारूढः",
    },
    {
        # सामि + कृत → सामिकृतम् (i-final pūrva, no junction sandhi). Same avyaya-pūrva
        # shape as 2.1.25 — carries a semantic sense to mirror the kāraka/CLI path.
        "label": "T0-sAmikRtam-2.1.27",
        "purva": {"avyaya": "sAmi", "sem": "semantic_1", "vivakza": True},
        "uttara": {"stem": "kfta", "vacana": 1, "vivakza": True},
        "fired": ["2.1.27", "1.2.43", "2.4.26"],
        "surface": "सामिकृतम्",
    },
    {
        "label": "T0-mAsapramitaH-2.1.28",        # मास (dvitīyā, kāla, non-atyanta) + प्रमित → मासप्रमितः
        "purva": {"stem": "mAsa", "vacana": 1, "vibhakti": 2, "vivakza": True},
        "uttara": {"stem": "pramita", "vacana": 1, "vivakza": True},
        "fired": ["2.1.28", "1.2.43", "2.4.26"],
        "surface": "मासप्रमितः",
    },
    {
        "label": "T0-muhUrtasuKam-2.1.29",        # मुहूर्त (dvitīyā, kāla, atyantasaṃyoga) + सुख → मुहूर्तसुखम्
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
        "label": "T1-mAsapUrvaH-2.1.31",          # मासेन पूर्वः → मासपूर्वः (tṛtīyā, pūrvasadṛśa)
        "purva": {"stem": "mAsa", "vacana": 1, "vibhakti": 3, "vivakza": True},
        "uttara": {"stem": "pUrva_tp", "vacana": 1, "vivakza": True},
        "fired": ["2.1.31", "1.2.43", "2.4.26"],
        "surface": "मासपूर्वः",
    },
    {
        "label": "T1-DAnyArTaH-2.1.36",           # धान्याय अर्थः → धान्यार्थः (caturthī, tadartha)
        "purva": {"stem": "DAnya", "vacana": 1, "vibhakti": 4, "vivakza": True},
        "uttara": {"stem": "arTa", "vacana": 1, "vivakza": True},
        "fired": ["2.1.36", "1.2.43", "2.4.26"],
        "surface": "धान्यार्थः",
    },
    {
        "label": "T1-coraBayam-2.1.37",           # चोरात् भयम् → चोरभयम् (pañcamī, bhaya; napuṁsaka)
        "purva": {"stem": "cora", "vacana": 1, "vibhakti": 5, "vivakza": True},
        "uttara": {"stem": "Baya", "vacana": 1, "vivakza": True},
        "fired": ["2.1.37", "1.2.43", "2.4.26"],
        "surface": "चोरभयम्",
    },
    {
        "label": "T1-rAjapuruSaH-2.2.8",          # राज्ञः पुरुषः → राजपुरुषः (ṣaṣṭhī — the canonical tatpuruṣa)
        "purva": {"stem": "rAjan", "vacana": 1, "vibhakti": 6, "vivakza": True},
        "uttara": {"stem": "puruza", "vacana": 1, "vivakza": True},
        "fired": ["2.2.8", "1.2.43", "2.4.26"],
        "surface": "राजपुरुषः",
    },
    {
        "label": "T1-pUrvakAyaH-2.2.1",           # पूर्वं कायस्य → पूर्वकायः (ṣaṣṭhī pūrvāpara/ekadeśī)
        "purva": {"stem": "pUrva_dik", "vacana": 1, "vibhakti": 1, "vivakza": True},
        "uttara": {"stem": "kAya_ed", "vacana": 1, "vivakza": True},
        "fired": ["2.2.1", "1.2.43", "2.4.26"],
        "surface": "पूर्वकायः",
    },
    {
        "label": "T1-akzaSORqaH-2.1.40",          # अक्षेषु शौण्डः → अक्षशौण्डः (saptamī, śauṇḍa)
        "purva": {"stem": "akza", "vacana": 1, "vibhakti": 7, "vivakza": True},
        "uttara": {"stem": "SORqa", "vacana": 1, "vivakza": True},
        "fired": ["2.1.40", "1.2.43", "2.4.26"],
        "surface": "अक्षशौण्डः",
    },
    # ── T1 extension rules (one case each, previously untested) ──
    {
        "label": "T1-guqasvAduH-2.1.30",          # गुडेन स्वादुः → गुडस्वादुः (tṛtīyā, guṇavacana; u-stem uttara)
        "purva": {"stem": "guqa", "vacana": 1, "vibhakti": 3, "vivakza": True},
        "uttara": {"stem": "svAdu", "vacana": 1, "vivakza": True},
        "fired": ["2.1.30", "1.2.43", "2.4.26"],
        "surface": "गुडस्वादुः",
    },
    {
        "label": "T1-ahihataH-2.1.32",            # अहिना हतः → अहिहतः (tṛtīyā kartṛ/karaṇa + kṛta)
        "purva": {"stem": "ahi", "vacana": 1, "vibhakti": 3, "vivakza": True},
        "uttara": {"stem": "hata", "vacana": 1, "vivakza": True},
        "fired": ["2.1.32", "1.2.43", "2.4.26"],
        "surface": "अहिहतः",
    },
    {
        "label": "T1-suKApetaH-2.1.38",           # सुखात् अपेतः → सुखापेतः (pañcamī, apeta-gaṇa)
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
        "label": "T1-stokamuktaH-2.1.39",
        "purva": {"stem": "stoka", "vacana": 1, "vibhakti": 5, "vivakza": True},
        "uttara": {"stem": "mukta", "vacana": 1, "vivakza": True},
        "fired": ["2.1.39", "1.2.43", "2.4.26"],
        "surface": "स्तोकमुक्तः",
    },
    {
        "label": "T1-svargasidDaH-2.1.41",        # स्वर्गे सिद्धः → स्वर्गसिद्धः (saptamī, siddha-gaṇa)
        "purva": {"stem": "svarga", "vacana": 1, "vibhakti": 7, "vivakza": True},
        "uttara": {"stem": "sidDa", "vacana": 1, "vivakza": True},
        "fired": ["2.1.41", "1.2.43", "2.4.26"],
        "surface": "स्वर्गसिद्धः",
    },
]
