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
