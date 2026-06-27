# -*- coding: utf-8 -*-
"""
Kāraka test cases (karaka_plan.md §3) — Phase K0: SK 532/533/535/537/559/560/561/606
(2.3.46, 2.3.47, 1.4.49, 2.3.2, 1.4.54, 1.4.42, 2.3.18, 2.3.50; SK534/536 are
adhikāras realized as engine semantics). Examples lifted from the SK commentary
(references/siddhantakaumudi.html anchors SK532–537, 559–561, 606).

Case format:
  label    : pytest id
  sutras   : ids that must appear in the kāraka pre-pass fired trace
  sentence : ordered word specs —
               {"stem": <pratipadika name>, "vacana": 1|2|3, "sem": [semantic_* tags]}
               {"verb": <dhatu-module pre-formed pada name>}   (tiṅanta stub, §6)
               {"word": <avyaya-module name>, "sem": [...], "dir": "pUrva"|"para"}
                   (particle; "sem" carries a karmapravacanīya's per-usage sense,
                    "dir" its governance direction — pūrva governs the preceding
                    noun, para the following — a USER choice, not sense-derived,
                    defaulting to "pUrva" when a sense is present; plain particles
                    pass through bare)
             Words are separated by avasAna in the built vakya, so each word
             derives without inter-word sandhi and the joined output is the
             concatenation of per-word forms + "." separators.
  expect   : per-word dicts, aligned with sentence —
               "karaka"   : exact kAraka_* tag, or None for "no kāraka at all"
               "vibhakti" : exact set of viBakti_N tags ([] = none)
               "not_fired": sutra ids that must NOT have fired for this word
               "forms"    : acceptable surface alternatives (Devanagari); the
                            sentence-level expectation is the cross-product

Input conventions (karaka_plan.md §2):
  - semantic_* tags are the primitives in the sutra wording. A sentence whose
    only content is bare stem-meaning (SK532 कृष्णः, ज्ञानम्) carries
    semantic_prAtipadikArTa — 2.3.46's own primitive — which also arms the
    pre-pass skip-guard; no rule conditions on it (the prathamā default arm
    fires on ?prAtipadika), so untagged co-participants still default to
    prathamā without it (see SK606-ramasya-putrah).
  - the verb is a pre-formed pada carrying its prayoga tag (kartari/karmaRi).
"""

karaka_tests = [
    # ── SK535 + SK537: karma saṁjñā → dvitīyā ───────────────────────────────
    {
        "label": "SK537-harim-bhajati",
        "sutras": ["1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "hari", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "Bajati"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["हरिम्"]},
            {"forms": ["भजति"]},
        ],
    },
    {
        "label": "SK537-hari-dvivacana",
        "sutras": ["1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "hari", "vacana": 2, "sem": ["semantic_Ipsitatama"]},
            {"verb": "Bajati"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["हरी"]},
            {"forms": ["भजति"]},
        ],
    },
    {
        "label": "SK537-hari-bahuvacana",
        "sutras": ["1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "hari", "vacana": 3, "sem": ["semantic_Ipsitatama"]},
            {"verb": "Bajati"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["हरीन्"]},
            {"forms": ["भजति"]},
        ],
    },
    {
        "label": "SK537-jnanam-dvitiya-napum",
        "sutras": ["1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "jYAna", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "Bajati"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["ज्ञानम्"]},
            {"forms": ["भजति"]},
        ],
    },

    # ── SK559 + SK532: kartṛ abhihita (kartari prayoga) → prathamā ──────────
    {
        "label": "SK532-ramo-harim-bhajati",
        "sutras": ["1.4.54", "2.3.46", "1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "rAma", "vacana": 1, "sem": ["semantic_svatantra"]},
            {"stem": "hari", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "Bajati"},
        ],
        "expect": [
            {"karaka": "kAraka_kartA", "vibhakti": ["viBakti_1"],
             "not_fired": ["2.3.18"], "forms": ["रामः"]},
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["हरिम्"]},
            {"forms": ["भजति"]},
        ],
    },

    # ── SK536 + SK532: karma abhihita (karmaṇi prayoga) → prathamā ──────────
    {
        "label": "SK532-harih-sevyate",
        "sutras": ["1.4.49", "2.3.46"],
        "sentence": [
            {"stem": "hari", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "sevyate"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_1"],
             "not_fired": ["2.3.2"], "forms": ["हरिः"]},
            {"forms": ["सेव्यते"]},
        ],
    },

    # ── SK559 + SK561: kartṛ anabhihita (karmaṇi prayoga) → tṛtīyā ──────────
    {
        "label": "SK561-ramena-sevyate",
        "sutras": ["1.4.54", "2.3.18"],
        "sentence": [
            {"stem": "rAma", "vacana": 1, "sem": ["semantic_svatantra"]},
            {"verb": "sevyate"},
        ],
        "expect": [
            {"karaka": "kAraka_kartA", "vibhakti": ["viBakti_3"],
             "not_fired": ["2.3.46"], "forms": ["रामेण"]},
            {"forms": ["सेव्यते"]},
        ],
    },
    {
        "label": "SK561-harih-ramena-sevyate",
        "sutras": ["1.4.49", "2.3.46", "1.4.54", "2.3.18"],
        "sentence": [
            {"stem": "hari", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"stem": "rAma", "vacana": 1, "sem": ["semantic_svatantra"]},
            {"verb": "sevyate"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_1"], "forms": ["हरिः"]},
            {"karaka": "kAraka_kartA", "vibhakti": ["viBakti_3"], "forms": ["रामेण"]},
            {"forms": ["सेव्यते"]},
        ],
    },
    {
        "label": "SK561-kartr-dvivacana",
        "sutras": ["1.4.54", "2.3.18"],
        "sentence": [
            {"stem": "rAma", "vacana": 2, "sem": ["semantic_svatantra"]},
            {"verb": "sevyate"},
        ],
        "expect": [
            {"karaka": "kAraka_kartA", "vibhakti": ["viBakti_3"], "forms": ["रामाभ्याम्"]},
            {"forms": ["सेव्यते"]},
        ],
    },

    # ── SK560 + SK561: karaṇa → tṛtīyā (both prayogas) ──────────────────────
    {
        "label": "SK561-banena-karana-kartari",
        "sutras": ["1.4.42", "2.3.18"],
        "sentence": [
            {"stem": "rAma", "vacana": 1, "sem": ["semantic_svatantra"]},
            {"stem": "bARa", "vacana": 1, "sem": ["semantic_sADakatama"]},
            {"stem": "hari", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "Bajati"},
        ],
        "expect": [
            {"karaka": "kAraka_kartA", "vibhakti": ["viBakti_1"], "forms": ["रामः"]},
            {"karaka": "kAraka_karaRa", "vibhakti": ["viBakti_3"], "forms": ["बाणेन"]},
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["हरिम्"]},
            {"forms": ["भजति"]},
        ],
    },
    {
        "label": "SK561-banena-karana-karmani",
        "sutras": ["1.4.42", "2.3.18", "1.4.49", "2.3.46"],
        "sentence": [
            {"stem": "hari", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"stem": "bARa", "vacana": 1, "sem": ["semantic_sADakatama"]},
            {"verb": "sevyate"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_1"], "forms": ["हरिः"]},
            {"karaka": "kAraka_karaRa", "vibhakti": ["viBakti_3"], "forms": ["बाणेन"]},
            {"forms": ["सेव्यते"]},
        ],
    },
    {
        "label": "SK561-karana-bahuvacana",
        "sutras": ["1.4.42", "2.3.18"],
        "sentence": [
            {"stem": "hari", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"stem": "bARa", "vacana": 3, "sem": ["semantic_sADakatama"]},
            {"verb": "sevyate"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_1"], "forms": ["हरिः"]},
            {"karaka": "kAraka_karaRa", "vibhakti": ["viBakti_3"], "forms": ["बाणैः"]},
            {"forms": ["सेव्यते"]},
        ],
    },

    # ── SK533: sambodhana → viBakti_8 (sup row 8) ───────────────────────────
    {
        "label": "SK533-he-rama",
        "sutras": ["2.3.47"],
        "sentence": [
            {"word": "he"},
            {"stem": "rAma", "vacana": 1, "sem": ["semantic_samboDana"]},
        ],
        "expect": [
            {"forms": ["हे"]},
            {"karaka": None, "vibhakti": ["viBakti_8"], "forms": ["राम"]},
        ],
    },
    {
        "label": "SK533-he-hare",
        "sutras": ["2.3.47"],
        "sentence": [
            {"word": "he"},
            {"stem": "hari", "vacana": 1, "sem": ["semantic_samboDana"]},
        ],
        "expect": [
            {"forms": ["हे"]},
            {"karaka": None, "vibhakti": ["viBakti_8"], "forms": ["हरे"]},
        ],
    },
    {
        "label": "SK533-he-harayah-bahuvacana",
        "sutras": ["2.3.47"],
        "sentence": [
            {"word": "he"},
            {"stem": "hari", "vacana": 3, "sem": ["semantic_samboDana"]},
        ],
        "expect": [
            {"forms": ["हे"]},
            {"karaka": None, "vibhakti": ["viBakti_8"], "forms": ["हरयः"]},
        ],
    },

    # ── SK606: śeṣa → ṣaṣṭhī ────────────────────────────────────────────────
    {
        "label": "SK606-ramasya-putrah",
        "sutras": ["2.3.50", "2.3.46"],
        "sentence": [
            {"stem": "rAma", "vacana": 1, "sem": ["semantic_Seza"]},
            {"stem": "putra", "vacana": 1, "sem": []},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_6"], "forms": ["रामस्य"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["पुत्रः"]},
        ],
    },
    {
        "label": "SK606-sesa-bahuvacana",
        "sutras": ["2.3.50", "2.3.46"],
        "sentence": [
            {"stem": "hari", "vacana": 3, "sem": ["semantic_Seza"]},
            {"stem": "putra", "vacana": 1, "sem": []},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_6"], "forms": ["हरीणाम्"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["पुत्रः"]},
        ],
    },
    {
        "label": "SK606-sesa-in-verb-sentence",
        "sutras": ["2.3.50", "1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "rAma", "vacana": 1, "sem": ["semantic_Seza"]},
            {"stem": "hari", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "Bajati"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_6"], "forms": ["रामस्य"]},
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["हरिम्"]},
            {"forms": ["भजति"]},
        ],
    },

    # ── SK532: prathamā for mere stem-meaning ───────────────────────────────
    {
        "label": "SK532-krsnah",
        "sutras": ["2.3.46"],
        "sentence": [
            {"stem": "kfzRa", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["कृष्णः"]},
        ],
    },
    {
        "label": "SK532-jnanam",
        "sutras": ["2.3.46"],
        "sentence": [
            {"stem": "jYAna", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["ज्ञानम्"]},
        ],
    },
    {
        "label": "SK532-ramau-dvivacana",
        "sutras": ["2.3.46"],
        "sentence": [
            {"stem": "rAma", "vacana": 2, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["रामौ"]},
        ],
    },

    # ── Negative / structural cases ─────────────────────────────────────────
    {
        # SK535 kartuḥ kim: in माषेष्वश्वं बध्नाति only the aśva is the agent's
        # īpsitatama; the māṣa slot must NOT get kAraka_karma (it defaults to
        # prathamā here — its locative awaits 1.4.45 adhikaraṇa in K7).
        "label": "SK535-negative-masa-not-karma",
        "sutras": ["1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "aSva", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"stem": "mAza", "vacana": 1, "sem": []},
            {"verb": "Bajati"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["अश्वम्"]},
            {"karaka": None, "vibhakti": ["viBakti_1"],
             "not_fired": ["1.4.49", "2.3.2"], "forms": ["माषः"]},
            {"forms": ["भजति"]},
        ],
    },
    {
        # 1.4.2 vipratiṣedhe param via the engine carve-out: a noun carrying
        # both sādhakatama and īpsitatama gets karma (1.4.49 > 1.4.42), and
        # ekā-saṁjñā keeps 1.4.42 off afterwards.
        "label": "SK535-param-carveout-1449-beats-1442",
        "sutras": ["1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "bARa", "vacana": 1,
             "sem": ["semantic_sADakatama", "semantic_Ipsitatama"]},
            {"verb": "Bajati"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"],
             "not_fired": ["1.4.42"], "forms": ["बाणम्"]},
            {"forms": ["भजति"]},
        ],
    },
    {
        # Skip-guard: no semantic/prayoga tag anywhere → the pre-pass never
        # runs; no vibhakti is assigned, no sup inserted, the stem passes
        # through underived.
        "label": "negative-skip-guard-no-tags",
        "sutras": [],
        "sentence": [
            {"stem": "kfzRa", "vacana": 1, "sem": []},
        ],
        "expect": [
            {"karaka": None, "vibhakti": [], "forms": ["कृष्ण"]},
        ],
    },
    {
        # Two karma nouns in one sentence: each gets its own saṁjñā (the
        # +kAraka guard is per-object, 1.4.1 ekā saṁjñā is per-kāraka).
        "label": "SK537-two-karma-nouns",
        "sutras": ["1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "hari", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"stem": "kfzRa", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "Bajati"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["हरिम्"]},
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["कृष्णम्"]},
            {"forms": ["भजति"]},
        ],
    },
    {
        # Feminine second noun: the sup-insertion scan must place rAma's su at
        # rAma's own position and NOT scroll past the next word ramA just
        # because ramA carries the strī tag (it is a pratipadika, not a
        # pratyaya). Regression for the strī-stem sup-placement bug.
        "label": "SK537-rama-ramaa-karma-feminine",
        "sutras": ["1.4.54", "2.3.46", "1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "rAma", "vacana": 1, "sem": ["semantic_svatantra"]},
            {"stem": "ramA", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "Bajati"},
        ],
        "expect": [
            {"karaka": "kAraka_kartA", "vibhakti": ["viBakti_1"], "forms": ["रामः"]},
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["रमाम्"]},
            {"forms": ["भजति"]},
        ],
    },
    {
        # Sambodhana + kartari verb: the vocative is not a kāraka; the verb
        # sentence still derives around it.
        "label": "SK533-he-rama-harim-bhajati",
        "sutras": ["2.3.47", "1.4.49", "2.3.2"],
        "sentence": [
            {"word": "he"},
            {"stem": "rAma", "vacana": 1, "sem": ["semantic_samboDana"]},
            {"stem": "hari", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "Bajati"},
        ],
        "expect": [
            {"forms": ["हे"]},
            {"karaka": None, "vibhakti": ["viBakti_8"], "forms": ["राम"]},
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["हरिम्"]},
            {"forms": ["भजति"]},
        ],
    },

    # ════════════════════════════════════════════════════════════════════════
    # Phase K1 — karma extensions (SK538–545; karaka_plan.md §5). Examples from
    # references/siddhantakaumudi.html anchors SK538–545; participle/multi-clause
    # originals reduced to single finite verbs (multi-clause deferred, §6).
    # ════════════════════════════════════════════════════════════════════════

    # ── SK538 (1.4.50): anīpsita-but-connected → karma → dvitīyā ─────────────
    {
        # ग्रामं गच्छन् तृणं स्पृशति — the grass, though not desired, is karma.
        "label": "SK538-trnam-sprsati",
        "sutras": ["1.4.50", "2.3.2"],
        "sentence": [
            {"stem": "tfRa", "vacana": 1, "sem": ["semantic_anIpsita"]},
            {"verb": "spfSati"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["तृणम्"]},
            {"forms": ["स्पृशति"]},
        ],
    },

    # ── SK539 (1.4.51): akathita karma in dvikarmaka, + akarmaka vārttika ────
    {
        # गां दोग्धि पयः — the cow (else apādāna) is akathita karma; payas is the
        # primary (īpsitatama) karma. Both → dvitīyā.
        "label": "SK539-gam-dogdhi-payah",
        "sutras": ["1.4.51", "1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "go", "vacana": 1, "sem": ["semantic_akaTita"]},
            {"stem": "payas", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "dogDi"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["गाम्"]},
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["पयः"]},
            {"forms": ["दोग्धि"]},
        ],
    },
    {
        # मासमास्ते — vārttika: deśa/kāla/bhāva/adhvan with an akarmaka verb → karma.
        "label": "SK539-masam-aste",
        "sutras": ["1.4.51", "2.3.2"],
        "sentence": [
            {"stem": "mAsa", "vacana": 1, "sem": ["semantic_deSakAlAdhvan"]},
            {"verb": "Aste"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["मासम्"]},
            {"forms": ["आस्ते"]},
        ],
    },
    {
        # Negative: akathita noun with a NON-dvikarmaka verb (भजति) — 1.4.51 must
        # not fire; the cow defaults to prathamā.
        "label": "SK539-negative-not-dvikarmaka",
        "sutras": ["2.3.46"],
        "sentence": [
            {"stem": "go", "vacana": 1, "sem": ["semantic_akaTita"]},
            {"verb": "Bajati"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_1"],
             "not_fired": ["1.4.51"], "forms": ["गौः"]},
            {"forms": ["भजति"]},
        ],
    },

    # ── SK540 (1.4.52): ṇyanta kartṛ → karma (gati/buddhi classes) ───────────
    {
        # कृष्णं स्वर्गम् अगमयत् — the prayojya kartṛ (Kṛṣṇa, made to go) → karma by
        # 1.4.52 (overrides 1.4.54); svarga is the gati-goal karma by 1.4.49.
        "label": "SK540-krsnam-svargam-agamayat",
        "sutras": ["1.4.52", "1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "kfzRa", "vacana": 1, "sem": ["semantic_svatantra"]},
            {"stem": "svarga", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "agamayat"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"],
             "not_fired": ["1.4.54"], "forms": ["कृष्णम्"]},
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["स्वर्गम्"]},
            # imperfect at avasāna: 8.2.39 voices the final t → द्, 8.4.56
            # optionally devoices it back → both अगमयत् / अगमयद्.
            {"forms": ["अगमयत्", "अगमयद्"]},
        ],
    },
    {
        # वेदम् अध्यापयद् विधिम् — buddhi (study=cognition) class: vidhi (made to
        # study) → karma; veda the primary karma.
        "label": "SK540-vedam-adhyapayad-vidhim",
        "sutras": ["1.4.52", "1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "viDi", "vacana": 1, "sem": ["semantic_svatantra"]},
            {"stem": "veda", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "aDyApayat"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"],
             "not_fired": ["1.4.54"], "forms": ["विधिम्"]},
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["वेदम्"]},
            {"forms": ["अध्यापयत्", "अध्यापयद्"]},
        ],
    },
    {
        # गत्यादि-किम्: पाचयति देवदत्तः — ṇyanta but pac is NOT a gati-class verb, so
        # 1.4.52 does not fire; Devadatta stays kartṛ, abhihita → prathamā.
        "label": "SK540-negative-gatyadi-kim",
        "sutras": ["1.4.54", "2.3.46"],
        "sentence": [
            {"stem": "devadatta", "vacana": 1, "sem": ["semantic_svatantra"]},
            {"verb": "pAcayati"},
        ],
        "expect": [
            {"karaka": "kAraka_kartA", "vibhakti": ["viBakti_1"],
             "not_fired": ["1.4.52"], "forms": ["देवदत्तः"]},
            {"forms": ["पाचयति"]},
        ],
    },

    # ── SK541 (1.4.53): hṛ/kṛ ṇyanta kartṛ → karma (karma-only; t-branch K3) ──
    {
        # कारयति भृत्यं कटम् — the servant (made to make) → karma by 1.4.53; kaṭa
        # the primary karma. (The anyatarasyām tṛtīyā भृत्येन branch is deferred.)
        "label": "SK541-karayati-bhrtyam-katam",
        "sutras": ["1.4.53", "1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "Bftya", "vacana": 1, "sem": ["semantic_svatantra"]},
            {"stem": "kawa", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "kArayati"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"],
             "not_fired": ["1.4.54"], "forms": ["भृत्यम्"]},
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["कटम्"]},
            {"forms": ["कारयति"]},
        ],
    },

    # ── SK542 (1.4.46): ādhāra of adhi-śī/sthā/ās → karma ────────────────────
    {
        # अध्यास्ते वैकुण्ठं हरिः — the locus Vaikuṇṭha → karma; Hari the (abhihita,
        # kartari) kartṛ → prathamā.
        "label": "SK542-adhyaste-vaikuntham-harih",
        "sutras": ["1.4.46", "2.3.2", "1.4.54", "2.3.46"],
        "sentence": [
            {"stem": "vEkuRWa", "vacana": 1, "sem": ["semantic_aDikaraRa"]},
            {"stem": "hari", "vacana": 1, "sem": ["semantic_svatantra"]},
            {"verb": "aDyAste"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["वैकुण्ठम्"]},
            {"karaka": "kAraka_kartA", "vibhakti": ["viBakti_1"], "forms": ["हरिः"]},
            {"forms": ["अध्यास्ते"]},
        ],
    },

    # ── SK543 (1.4.47): ādhāra of abhi-ni-viś → karma ───────────────────────
    {
        # अभिनिविशते सन्मार्गम् — the locus (the good path) → karma → dvitīyā.
        "label": "SK543-abhinivisate-sanmargam",
        "sutras": ["1.4.47", "2.3.2"],
        "sentence": [
            {"stem": "sanmArga", "vacana": 1, "sem": ["semantic_aDikaraRa"]},
            {"verb": "aBiniviSate"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["सन्मार्गम्"]},
            {"forms": ["अभिनिविशते"]},
        ],
    },

    # ── SK544 (1.4.48): ādhāra of upa/anu/adhi/āṅ-vas → karma ────────────────
    {
        # उपवसति वैकुण्ठं हरिः — the locus Vaikuṇṭha → karma; Hari the kartṛ.
        "label": "SK544-upavasati-vaikuntham-harih",
        "sutras": ["1.4.48", "2.3.2", "1.4.54", "2.3.46"],
        "sentence": [
            {"stem": "vEkuRWa", "vacana": 1, "sem": ["semantic_aDikaraRa"]},
            {"stem": "hari", "vacana": 1, "sem": ["semantic_svatantra"]},
            {"verb": "upavasati"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["वैकुण्ठम्"]},
            {"karaka": "kAraka_kartA", "vibhakti": ["viBakti_1"], "forms": ["हरिः"]},
            {"forms": ["उपवसति"]},
        ],
    },

    # ── SK545 (2.3.4): antarā/antareṇa-yukte dvitīyā ────────────────────────
    {
        # अन्तरेण हरिम् — the noun governed by antareṇa → dvitīyā (no kāraka).
        "label": "SK545-antarena-harim",
        "sutras": ["2.3.4"],
        "sentence": [
            {"word": "antareRa", "dir": "para"},
            {"stem": "hari", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"forms": ["अन्तरेण"]},
            {"karaka": None, "vibhakti": ["viBakti_2"],
             "not_fired": ["2.3.46"], "forms": ["हरिम्"]},
        ],
    },
    {
        # अन्तरा कृष्णम् — likewise with antarā.
        "label": "SK545-antara-krsnam",
        "sutras": ["2.3.4"],
        "sentence": [
            {"word": "antarA", "dir": "para"},
            {"stem": "kfzRa", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"forms": ["अन्तरा"]},
            {"karaka": None, "vibhakti": ["viBakti_2"],
             "not_fired": ["2.3.46"], "forms": ["कृष्णम्"]},
        ],
    },
    {
        # Adjacency: antareṇa governs only the adjacent hari (→ dvitīyā); the
        # non-adjacent kṛṣṇa must NOT get 2.3.4 — it defaults to prathamā.
        "label": "SK545-adjacency-harim-krsnah",
        "sutras": ["2.3.4", "2.3.46"],
        "sentence": [
            {"word": "antareRa", "dir": "para"},
            {"stem": "hari", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
            {"stem": "kfzRa", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"forms": ["अन्तरेण"]},
            {"karaka": None, "vibhakti": ["viBakti_2"], "forms": ["हरिम्"]},
            {"karaka": None, "vibhakti": ["viBakti_1"],
             "not_fired": ["2.3.4"], "forms": ["कृष्णः"]},
        ],
    },

    # ════════════════════════════════════════════════════════════════════════
    # Phase K2 — karmapravacanīya + dvitīyā (SK546–558; karaka_plan.md §K2).
    # The particle is an avyaya carrying its per-usage sense tag; Pass A assigns
    # karmapravacanIya + the case marker kp_dvitIyA. The governance DIRECTION is a
    # separate user input on the particle, given here as "dir": "pUrva" (governs
    # the noun to its left) or "para" (to its right); _build_word maps it to
    # kp_pUrva/kp_para and 2.3.8 reads it via rrp/llp. "dir" defaults to "pUrva"
    # when a sense is present, so pūrva cases may omit it. Particles take their own
    # su → 2.4.82 luk → bare avyaya form.
    # ════════════════════════════════════════════════════════════════════════

    # ── SK547 (1.4.84) + SK548 (2.3.8): anu lakṣaṇa, noun precedes ───────────
    {
        # जपमनु प्रावर्षत् (reduced: जपम् अनु) — "rained along the japa".
        "label": "SK548-japam-anu",
        "sutras": ["1.4.84", "2.3.8"],
        "sentence": [
            {"stem": "japa", "vacana": 1, "sem": []},
            {"word": "anu_kp", "sem": ["semantic_lakzaRa"], "dir": "pUrva"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_2"],
             "not_fired": ["2.3.46"], "forms": ["जपम्"]},
            {"forms": ["अनु"]},
        ],
    },
    # ── SK549 (1.4.85): anu tṛtīyārtha ("along with") ───────────────────────
    {
        # नदीमन्ववसिता सेना (reduced: नदीम् अनु).
        "label": "SK549-nadim-anu",
        "sutras": ["1.4.85", "2.3.8"],
        "sentence": [
            {"stem": "nadI", "vacana": 1, "sem": []},
            {"word": "anu_kp", "sem": ["semantic_tftIyArTa"], "dir": "pUrva"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_2"], "forms": ["नदीम्"]},
            {"forms": ["अनु"]},
        ],
    },
    # ── SK550 (1.4.86): anu hīna, noun FOLLOWS (llp peek) ───────────────────
    {
        # अनु हरिं सुराः (reduced: अनु हरिम्) — "the suras are inferior to Hari".
        "label": "SK550-anu-harim",
        "sutras": ["1.4.86", "2.3.8"],
        "sentence": [
            {"word": "anu_kp", "sem": ["semantic_hIna"], "dir": "para"},
            {"stem": "hari", "vacana": 1, "sem": []},
        ],
        "expect": [
            {"forms": ["अनु"]},
            {"karaka": None, "vibhakti": ["viBakti_2"],
             "not_fired": ["2.3.46"], "forms": ["हरिम्"]},
        ],
    },
    # ── SK551 (1.4.87): upa hīna, noun follows ──────────────────────────────
    {
        # हीने उप हरिं सुराः (reduced: उप हरिम्).
        "label": "SK551-upa-harim",
        "sutras": ["1.4.87", "2.3.8"],
        "sentence": [
            {"word": "upa_kp", "sem": ["semantic_hIna"], "dir": "para"},
            {"stem": "hari", "vacana": 1, "sem": []},
        ],
        "expect": [
            {"forms": ["उप"]},
            {"karaka": None, "vibhakti": ["viBakti_2"], "forms": ["हरिम्"]},
        ],
    },
    # ── SK552 (1.4.90): prati lakṣaṇa / itthaṁbhūta, noun precedes ───────────
    {
        # वृक्षं प्रति विद्योतते विद्युत् (reduced: वृक्षं प्रति).
        "label": "SK552-vrksam-prati",
        "sutras": ["1.4.90", "2.3.8"],
        "sentence": [
            {"stem": "vfkza", "vacana": 1, "sem": []},
            {"word": "prati_kp", "sem": ["semantic_lakzaRa"], "dir": "pUrva"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_2"], "forms": ["वृक्षम्"]},
            {"forms": ["प्रति"]},
        ],
    },
    {
        # भक्तो विष्णुं प्रति (reduced: विष्णुं प्रति) — itthaṁbhūta-ākhyāna.
        "label": "SK552-visnum-prati-itthambhuta",
        "sutras": ["1.4.90", "2.3.8"],
        "sentence": [
            {"stem": "vizRu", "vacana": 1, "sem": []},
            {"word": "prati_kp", "sem": ["semantic_itTamBUta"], "dir": "pUrva"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_2"], "forms": ["विष्णुम्"]},
            {"forms": ["प्रति"]},
        ],
    },
    # ── SK553 (1.4.91): abhi lakṣaṇādi (not bhāga), noun precedes ────────────
    {
        # हरिमभि वर्तते (reduced: हरिम् अभि).
        "label": "SK553-harim-abhi",
        "sutras": ["1.4.91", "2.3.8"],
        "sentence": [
            {"stem": "hari", "vacana": 1, "sem": []},
            {"word": "aBi_kp", "sem": ["semantic_lakzaRa"], "dir": "pUrva"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_2"], "forms": ["हरिम्"]},
            {"forms": ["अभि"]},
        ],
    },
    # ── SK556 (1.4.95): ati atikramaṇa, noun follows ────────────────────────
    {
        # अति देवान् कृष्णः — "Kṛṣṇa surpasses the gods". devān → dvitīyā (llp ati);
        # kṛṣṇa (not adjacent to ati) → prathamā.
        "label": "SK556-ati-devan-krsnah",
        "sutras": ["1.4.95", "2.3.8", "2.3.46"],
        "sentence": [
            {"word": "ati_kp", "sem": ["semantic_atikramaRa"], "dir": "para"},
            {"stem": "deva", "vacana": 3, "sem": []},
            {"stem": "kfzRa", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"forms": ["अति"]},
            {"karaka": None, "vibhakti": ["viBakti_2"], "forms": ["देवान्"]},
            {"karaka": None, "vibhakti": ["viBakti_1"],
             "not_fired": ["2.3.8"], "forms": ["कृष्णः"]},
        ],
    },
    # ── Direction disambiguation: particle between two nouns ─────────────────
    {
        # कृष्णम् अनु रामः — anu in lakṣaṇa with dir=pUrva governs the PRECEDING noun
        # (kṛṣṇa → dvitīyā); rāma follows anu, so 2.3.8's kp_para arm does not fire
        # on it → prathamā. Confirms direction is the user's choice and only the
        # intended noun is tagged.
        "label": "SK548-krsnam-anu-ramah-direction",
        "sutras": ["1.4.84", "2.3.8", "2.3.46"],
        "sentence": [
            {"stem": "kfzRa", "vacana": 1, "sem": []},
            {"word": "anu_kp", "sem": ["semantic_lakzaRa"], "dir": "pUrva"},
            {"stem": "rAma", "vacana": 1, "sem": []},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_2"], "forms": ["कृष्णम्"]},
            {"forms": ["अनु"]},
            {"karaka": None, "vibhakti": ["viBakti_1"],
             "not_fired": ["2.3.8"], "forms": ["रामः"]},
        ],
    },
    # ── SK555 (1.4.94): su pūjā — saṁjñā only, no dvitīyā ────────────────────
    {
        # सुसिक्तम् — su (pūjā) is karmapravacanīya but governs no noun (prefixed to
        # a participle). Lone particle: fired-trace asserts the saṁjñā; su → सु.
        "label": "SK555-su-pujayam",
        "sutras": ["1.4.94"],
        "sentence": [
            {"word": "su_kp", "sem": ["semantic_pUjA"]},
        ],
        "expect": [
            {"forms": ["सु"]},
        ],
    },
    # ── SK557 (1.4.96): api sambhāvanā — saṁjñā only; sarpis ṣaṣṭhī, no dvitīyā ─
    {
        # सर्पिषोऽपि (reduced, avasāna-separated: सर्पिषः अपि) — api is
        # karmapravacanīya (no direction tag), so 2.3.8 does NOT fire; sarpis is
        # ṣaṣṭhī (modelled via śeṣa 2.3.50). द्वितीया तु नेह प्रवर्तते.
        "label": "SK557-sarpisah-api",
        "sutras": ["1.4.96", "2.3.50"],
        "sentence": [
            {"stem": "sarpis", "vacana": 1, "sem": ["semantic_Seza"]},
            {"word": "api_kp", "sem": ["semantic_saMBAvanA"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.8"], "forms": ["सर्पिषः"]},
            {"forms": ["अपि"]},
        ],
    },
    # ── SK558 (2.3.5): kāla/adhvan atyanta-saṁyoga → dvitīyā ─────────────────
    {
        # मासं कल्याणी — "beautiful for a month".
        "label": "SK558-masam-kalyani",
        "sutras": ["2.3.5", "2.3.46"],
        "sentence": [
            {"stem": "mAsa", "vacana": 1,
             "sem": ["semantic_kAlADvan", "semantic_atyantasaMyoga"]},
            {"stem": "kalyARI", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_2"], "forms": ["मासम्"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["कल्याणी"]},
        ],
    },
    {
        # क्रोशं गिरिः — "the hill is a krośa (away/long)".
        "label": "SK558-krosam-girih",
        "sutras": ["2.3.5", "2.3.46"],
        "sentence": [
            {"stem": "kroSa", "vacana": 1,
             "sem": ["semantic_kAlADvan", "semantic_atyantasaMyoga"]},
            {"stem": "giri", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_2"], "forms": ["क्रोशम्"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["गिरिः"]},
        ],
    },
    {
        # अत्यन्तसंयोगे किम् — मासस्य द्विरधीते: not continuous → ṣaṣṭhī, not dvitīyā.
        "label": "SK558-negative-masasya",
        "sutras": ["2.3.50"],
        "sentence": [
            {"stem": "mAsa", "vacana": 1,
             "sem": ["semantic_kAlADvan", "semantic_Seza"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.5"], "forms": ["मासस्य"]},
        ],
    },

    # ════════════════════════════════════════════════════════════════════════
    # Phase K3 — tṛtīyā cluster (SK562–568; karaka_plan.md §K3). Two vibhāṣā
    # rules (1.4.43, 2.3.22) fork the pre-pass; their words carry the SET of
    # tags/forms seen across branches, and p.output() yields both sentences.
    # Examples from references/siddhantakaumudi.html anchors SK562–568.
    # ════════════════════════════════════════════════════════════════════════

    # ── SK562 (1.4.43): दिवः कर्म च — vibhāṣā karma/karaṇa for √div's instrument ─
    {
        # अक्षैरक्षान्वा दीव्यति — the dice are optionally karma (द्वितीया अक्षान्,
        # via 1.4.43→2.3.2) or karaṇa (तृतीया अक्षैः, via 1.4.42→2.3.18).
        "label": "SK562-aksair-aksan-divyati",
        "sutras": ["1.4.43", "1.4.42", "2.3.2", "2.3.18"],
        "sentence": [
            {"stem": "akza", "vacana": 3, "sem": ["semantic_sADakatama"]},
            {"verb": "dIvyati"},
        ],
        "expect": [
            {"karaka": ["kAraka_karma", "kAraka_karaRa"],
             "vibhakti": ["viBakti_2", "viBakti_3"], "forms": ["अक्षान्", "अक्षैः"]},
            {"forms": ["दीव्यति"]},
        ],
    },

    # ── SK563 (2.3.6): अपवर्गे तृतीया — kāla/adhvan + completion → tṛtīyā ────────
    {
        # क्रोशेन (अनुवाकोऽधीतः) — studied [over the course of] a krośa, with
        # completion (apavarga) → tṛtīyā; beats 2.3.5 dvitīyā by para.
        "label": "SK563-krosena-apavarga",
        "sutras": ["2.3.6"],
        "sentence": [
            {"stem": "kroSa", "vacana": 1,
             "sem": ["semantic_kAlADvan", "semantic_atyantasaMyoga",
                     "semantic_apavarga"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_3"],
             "not_fired": ["2.3.5"], "forms": ["क्रोशेन"]},
        ],
    },
    {
        # अपवर्गे किम् — मासमधीतो नायातः: no completion → 2.3.5 dvitīyā, not 2.3.6.
        "label": "SK563-negative-no-apavarga",
        "sutras": ["2.3.5"],
        "sentence": [
            {"stem": "kroSa", "vacana": 1,
             "sem": ["semantic_kAlADvan", "semantic_atyantasaMyoga"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_2"],
             "not_fired": ["2.3.6"], "forms": ["क्रोशम्"]},
        ],
    },

    # ── SK564 (2.3.19): सहयुक्तेऽप्रधाने — saha-yoga subordinate → tṛtīyā ────────
    {
        # पुत्रेण सह (आगतः पिता) — the son (subordinate) → tṛtīyā; saha is putra's
        # rrp. The principal pitṛ defaults to prathamā (पिता).
        "label": "SK564-putrena-saha-pita",
        "sutras": ["2.3.19", "2.3.46"],
        "sentence": [
            {"stem": "putra", "vacana": 1, "sem": ["semantic_apraDAna"]},
            {"word": "saha", "dir": "pUrva"},
            {"stem": "pitf", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_3"],
             "not_fired": ["2.3.46"], "forms": ["पुत्रेण"]},
            {"forms": ["सह"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["पिता"]},
        ],
    },
    {
        # सह पुत्रेण — saha as the noun's llp (saha-first order); same tṛtīyā.
        "label": "SK564-saha-putrena-llp",
        "sutras": ["2.3.19"],
        "sentence": [
            {"word": "saha", "dir": "para"},
            {"stem": "putra", "vacana": 1, "sem": ["semantic_apraDAna"]},
        ],
        "expect": [
            {"forms": ["सह"]},
            {"karaka": None, "vibhakti": ["viBakti_3"],
             "not_fired": ["2.3.46"], "forms": ["पुत्रेण"]},
        ],
    },
    {
        # साकम् variant — एवं साकंसार्धंसमंयोगेऽपि (SK564 commentary).
        "label": "SK564-putrena-sakam",
        "sutras": ["2.3.19"],
        "sentence": [
            {"stem": "putra", "vacana": 1, "sem": ["semantic_apraDAna"]},
            {"word": "sAkam", "dir": "pUrva"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_3"], "forms": ["पुत्रेण"]},
            {"forms": ["साकम्"]},
        ],
    },

    # ── SK565 (2.3.20): येनाङ्गविकारः — limb of deformity → tṛtīyā ──────────────
    {
        # अक्ष्णा काणः — one-eyed by [reason of] the eye; akṣi → tṛtīyā (अक्ष्णा),
        # kāṇa the qualified one → prathamā (काणः).
        "label": "SK565-aksna-kanah",
        "sutras": ["2.3.20", "2.3.46"],
        "sentence": [
            {"stem": "akzi", "vacana": 1, "sem": ["semantic_aNgavikAra"]},
            {"stem": "kARa", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_3"],
             "not_fired": ["2.3.46"], "forms": ["अक्ष्णा"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["काणः"]},
        ],
    },
    {
        # अङ्गविकारः किम् — अक्षि काणमस्य: the eye itself, no aṅga-vikāra → prathamā.
        "label": "SK565-negative-no-angavikara",
        "sutras": ["2.3.46"],
        "sentence": [
            {"stem": "akzi", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_1"],
             "not_fired": ["2.3.20"], "forms": ["अक्षि"]},
        ],
    },

    # ── SK566 (2.3.21): इत्थंभूतलक्षणे — mark of a state → tṛtīyā ───────────────
    {
        # जटाभिस्तापसः — an ascetic [recognized] by his matted hair; jaṭā (inst.
        # pl. जटाभिः) → tṛtīyā, tāpasa → prathamā (तापसः).
        "label": "SK566-jatabhis-tapasah",
        "sutras": ["2.3.21", "2.3.46"],
        "sentence": [
            {"stem": "jawA", "vacana": 3, "sem": ["semantic_itTamBUtalakzaRa"]},
            {"stem": "tApasa", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_3"],
             "not_fired": ["2.3.46"], "forms": ["जटाभिः"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["तापसः"]},
        ],
    },

    # ── SK567 (2.3.22): संज्ञोऽन्यतरस्यां कर्मणि — vibhāṣā tṛtīyā for sam-jñā karma ─
    {
        # पित्रा पितरं वा संजानीते — the karma of saṁjānīte is optionally tṛtīyā
        # (पित्रा, via 2.3.22) or dvitīyā (पितरम्, fall-through to 2.3.2). The noun
        # is kAraka_karma (1.4.49) in both branches.
        "label": "SK567-pitra-pitaram-samjanite",
        "sutras": ["1.4.49", "2.3.22", "2.3.2"],
        "sentence": [
            {"stem": "pitf", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "saMjAnIte"},
        ],
        "expect": [
            {"karaka": "kAraka_karma",
             "vibhakti": ["viBakti_2", "viBakti_3"], "forms": ["पितरम्", "पित्रा"]},
            {"forms": ["संजानीते"]},
        ],
    },
    {
        # Negative: a non-saṁjñā verb (भजति) — 2.3.22 must not fire; the karma is
        # plain dvitīyā (हरिम्) by 2.3.2 with no तृतीया alternative.
        "label": "SK567-negative-not-samjna",
        "sutras": ["1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "hari", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "Bajati"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"],
             "not_fired": ["2.3.22"], "forms": ["हरिम्"]},
            {"forms": ["भजति"]},
        ],
    },

    # ── SK568 (2.3.23): हेतौ — cause → tṛtīyā ──────────────────────────────────
    {
        # धनेन कुलम् — a family [is esteemed] by reason of wealth; dhana (hetu) →
        # tṛtīyā (धनेन), kula → prathamā (कुलम्).
        "label": "SK568-dhanena-kulam",
        "sutras": ["2.3.23", "2.3.46"],
        "sentence": [
            {"stem": "Dana", "vacana": 1, "sem": ["semantic_hetu"]},
            {"stem": "kula", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_3"],
             "not_fired": ["2.3.46"], "forms": ["धनेन"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["कुलम्"]},
        ],
    },

    # ════════════════════════════════════════════════════════════════════════
    # Phase K4 — sampradāna + caturthī (SK569–585; karaka_plan.md §K4). The
    # sampradāna saṁjñā cluster (1.4.32–41) + 2.3.13 caturthī; the param pair
    # 1.4.38 > 1.4.37 (upasṛṣṭa krudh → karma); 2.3.16 namaḥ-yoga; and three
    # vibhāṣā rules (1.4.44, 2.3.17, 2.3.12) that fork the pre-pass (words carry
    # the SET of tags/forms across branches). Examples from
    # references/siddhantakaumudi.html anchors SK569–585.
    # ════════════════════════════════════════════════════════════════════════

    # ── SK571 (1.4.33) + SK570 (2.3.13): rucyartha prīyamāṇa → caturthī ───────
    {
        # हरये रोचते भक्तिः — the pleased one (hari) → sampradāna → caturthī (हरये);
        # the pleasing thing (bhakti) is the kartṛ → prathamā (भक्तिः).
        "label": "SK571-harye-rocate-bhaktih",
        "sutras": ["1.4.33", "2.3.13", "1.4.54", "2.3.46"],
        "sentence": [
            {"stem": "hari", "vacana": 1, "sem": ["semantic_prIyamARa"]},
            {"stem": "Bakti", "vacana": 1, "sem": ["semantic_svatantra"]},
            {"verb": "rocate"},
        ],
        "expect": [
            {"karaka": "kAraka_sampradAna", "vibhakti": ["viBakti_4"], "forms": ["हरये"]},
            {"karaka": "kAraka_kartA", "vibhakti": ["viBakti_1"], "forms": ["भक्तिः"]},
            {"forms": ["रोचते"]},
        ],
    },

    # ── SK573 (1.4.35): dhāreḥ uttamarṇa → caturthī (+ śata karma) ────────────
    {
        # देवदत्ताय शतं धारयति — the creditor Devadatta → sampradāna → caturthī
        # (देवदत्ताय); the debt śata = karma → dvitīyā (शतम्).
        "label": "SK573-devadattaya-satam-dharayati",
        "sutras": ["1.4.35", "2.3.13", "1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "devadatta", "vacana": 1, "sem": ["semantic_uttamarRa"]},
            {"stem": "Sata", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "DArayati"},
        ],
        "expect": [
            {"karaka": "kAraka_sampradAna", "vibhakti": ["viBakti_4"], "forms": ["देवदत्ताय"]},
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["शतम्"]},
            {"forms": ["धारयति"]},
        ],
    },

    # ── SK575 (1.4.37): krudh target → sampradāna → caturthī ──────────────────
    {
        # हरये क्रुध्यति — the one angered-at (hari) → sampradāna → caturthī (हरये).
        "label": "SK575-harye-krudhyati",
        "sutras": ["1.4.37", "2.3.13"],
        "sentence": [
            {"stem": "hari", "vacana": 1, "sem": ["semantic_kopyamAna"]},
            {"verb": "kruDyati"},
        ],
        "expect": [
            {"karaka": "kAraka_sampradAna", "vibhakti": ["viBakti_4"],
             "not_fired": ["1.4.38"], "forms": ["हरये"]},
            {"forms": ["क्रुध्यति"]},
        ],
    },
    # ── SK576 (1.4.38): upasṛṣṭa krudh target → KARMA (param 1.4.38 > 1.4.37) ──
    {
        # अभिक्रुध्यति हरिम् — with the upasṛṣṭa verb abhi-krudh the target → karma
        # → dvitīyā (हरिम्). 1.4.38 beats 1.4.37 by the param carve-out; 1.4.37
        # must not fire. Direct counter to SK575-harye-krudhyati.
        "label": "SK576-abhikrudhyati-harim-param",
        "sutras": ["1.4.38", "2.3.2"],
        "sentence": [
            {"stem": "hari", "vacana": 1, "sem": ["semantic_kopyamAna"]},
            {"verb": "aBikruDyati"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"],
             "not_fired": ["1.4.37", "2.3.13"], "forms": ["हरिम्"]},
            {"forms": ["अभिक्रुध्यति"]},
        ],
    },

    # ── SK569 (1.4.32): general sampradāna (karmaṇā yam abhipraiti) ───────────
    {
        # विप्राय गां ददाति — the recipient vipra → sampradāna → caturthī (विप्राय);
        # the gift go = karma → dvitīyā (गाम्).
        "label": "SK569-vipraya-gam-dadati",
        "sutras": ["1.4.32", "2.3.13", "1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "vipra", "vacana": 1, "sem": ["semantic_aBipreta"]},
            {"stem": "go", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "dadAti"},
        ],
        "expect": [
            {"karaka": "kAraka_sampradAna", "vibhakti": ["viBakti_4"], "forms": ["विप्राय"]},
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["गाम्"]},
            {"forms": ["ददाति"]},
        ],
    },

    # ── SK583 (2.3.16): namaḥ-yoga → caturthī ────────────────────────────────
    {
        # नमो देवेभ्यः — deva governed by namaḥ → caturthī (देवेभ्यः); namas the
        # neuter noun takes its own prathamā नमः. (avasāna-separated, so नमः.)
        "label": "SK583-namo-devebhyah",
        "sutras": ["2.3.16", "2.3.46"],
        "sentence": [
            {"stem": "namas", "vacana": 1, "sem": ["semantic_prAtipadikArTa"], "dir": "para"},
            {"stem": "deva", "vacana": 3, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["नमः"]},
            {"karaka": None, "vibhakti": ["viBakti_4"],
             "not_fired": ["2.3.46"], "forms": ["देवेभ्यः"]},
        ],
    },

    # ── SK585 (2.3.12): gatyartha karma → vibhāṣā dvitīyā / caturthī ──────────
    {
        # ग्रामं ग्रामाय वा गच्छति — the goal grāma is karma (1.4.49) and optionally
        # dvitīyā (ग्रामम्, via 2.3.2) or caturthī (ग्रामाय, via 2.3.12). Fork.
        "label": "SK585-gramam-gramaya-gacchati",
        "sutras": ["1.4.49", "2.3.12", "2.3.2"],
        "sentence": [
            {"stem": "grAma", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "gacCati"},
        ],
        "expect": [
            {"karaka": "kAraka_karma",
             "vibhakti": ["viBakti_2", "viBakti_4"], "forms": ["ग्रामम्", "ग्रामाय"]},
            {"forms": ["गच्छति"]},
        ],
    },
    {
        # गत्यर्थ किम्: a non-gatyartha verb (भजति) — 2.3.12 must not fire; the
        # karma is plain dvitīyā (ग्रामम्) only, no caturthī alternative.
        "label": "SK585-negative-not-gatyartha",
        "sutras": ["1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "grAma", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "Bajati"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"],
             "not_fired": ["2.3.12"], "forms": ["ग्रामम्"]},
            {"forms": ["भजति"]},
        ],
    },

    # ── SK580 (1.4.44): parikrayaṇa → vibhāṣā sampradāna / karaṇa ─────────────
    {
        # शताय शतेन वा परिक्रीणीते — the wage śata is optionally sampradāna (शताय,
        # 1.4.44 → 2.3.13) or karaṇa (शतेन, 1.4.42 → 2.3.18). Fork; the noun also
        # carries semantic_sADakatama for the skip branch.
        "label": "SK580-sataya-satena-parikrinite",
        "sutras": ["1.4.44", "2.3.13", "1.4.42", "2.3.18"],
        "sentence": [
            {"stem": "Sata", "vacana": 1,
             "sem": ["semantic_parikrIta", "semantic_sADakatama"]},
            {"verb": "parikrIRIte"},
        ],
        "expect": [
            {"karaka": ["kAraka_sampradAna", "kAraka_karaRa"],
             "vibhakti": ["viBakti_4", "viBakti_3"], "forms": ["शताय", "शतेन"]},
            {"forms": ["परिक्रीणीते"]},
        ],
    },

    # ── SK584 (2.3.17): manya-karma anādara → vibhāṣā caturthī ───────────────
    {
        # तृणं तृणाय वा मन्यते — the manya-karman tṛṇa, in disrespect (anādara), is
        # optionally dvitīyā (तृणम्, 2.3.2) or caturthī (तृणाय, 2.3.17). Fork.
        "label": "SK584-trnam-trnaya-manyate",
        "sutras": ["1.4.49", "2.3.17", "2.3.2"],
        "sentence": [
            {"stem": "tfRa", "vacana": 1,
             "sem": ["semantic_Ipsitatama", "semantic_anAdara"]},
            {"verb": "manyate"},
        ],
        "expect": [
            {"karaka": "kAraka_karma",
             "vibhakti": ["viBakti_2", "viBakti_4"], "forms": ["तृणम्", "तृणाय"]},
            {"forms": ["मन्यते"]},
        ],
    },

    # ── Negative: rucyartha/krudh saṁjñā off for a plain transitive verb ──────
    {
        # हरिं भजति — bhajati is neither rucyartha nor krudh-class; 1.4.33/1.4.37/
        # 2.3.13 must not fire. hari = īpsitatama karma → dvitīyā (हरिम्).
        "label": "SK571-negative-not-rucyartha-krudh",
        "sutras": ["1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "hari", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "Bajati"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"],
             "not_fired": ["1.4.33", "1.4.37", "2.3.13"], "forms": ["हरिम्"]},
            {"forms": ["भजति"]},
        ],
    },

    # ════════════════════════════════════════════════════════════════════════
    # Phase K5 — apādāna + pañcamī (SK586–605; karaka_plan.md §K5). The apādāna
    # saṁjñā cluster (1.4.24–31) + 2.3.28 pañcamī; the karmapravacanīya
    # apa/āṅ/pari/prati (1.4.88/89/92 → 2.3.10/11); akartari ṛṇe (2.3.24); the
    # yoga-word peeks (2.3.29 anya/ārāt/itara/ṛte/dik); and the vibhāṣā forks —
    # two two-way (2.3.25 guṇa-hetu, 2.3.33 stoka-karaṇa) and two THREE-way
    # (2.3.32 pṛthak/vinā/nānā, 2.3.35 dūra/antika). pañcamī a-stems take both
    # pausa variants (त्/द्) at avasāna. Examples from
    # references/siddhantakaumudi.html anchors SK586–605.
    # ════════════════════════════════════════════════════════════════════════

    # ── SK586 (1.4.24) + SK587 (2.3.28): general dhruva-apāya → pañcamī ───────
    {
        # ग्रामादायाति — the fixed point (grāma) of separation → apādāna →
        # pañcamī (ग्रामात्/ग्रामाद्). General definition, no verb gate.
        "label": "SK586-gramad-ayati",
        "sutras": ["1.4.24", "2.3.28"],
        "sentence": [
            {"stem": "grAma", "vacana": 1, "sem": ["semantic_DruvApAya"]},
            {"verb": "Ayati"},
        ],
        "expect": [
            {"karaka": "kAraka_apAdAna", "vibhakti": ["viBakti_5"],
             "forms": ["ग्रामात्", "ग्रामाद्"]},
            {"forms": ["आयति"]},
        ],
    },

    # ── SK588 (1.4.25): bhī/trā bhaya-hetu → apādāna ──────────────────────────
    {
        # चोराद्बिभेति — the cause of fear (cora) → apādāna → pañcamī (चोराद्/चोरात्).
        "label": "SK588-corad-bibheti",
        "sutras": ["1.4.25", "2.3.28"],
        "sentence": [
            {"stem": "cora", "vacana": 1, "sem": ["semantic_Bayahetu"]},
            {"verb": "biBeti"},
        ],
        "expect": [
            {"karaka": "kAraka_apAdAna", "vibhakti": ["viBakti_5"],
             "forms": ["चोराद्", "चोरात्"]},
            {"forms": ["बिभेति"]},
        ],
    },

    # ── SK589 (1.4.26): parā-ji asoḍha → apādāna (+ negative) ─────────────────
    {
        # अध्ययनात्पराजयते — the unbearable thing (adhyayana) → apādāna → pañcamī
        # (अध्ययनात्/अध्ययनाद्). glāyati-artha "gives up studying".
        "label": "SK589-adhyayanat-parajayate",
        "sutras": ["1.4.26", "2.3.28"],
        "sentence": [
            {"stem": "aDyayana", "vacana": 1, "sem": ["semantic_asoQa"]},
            {"verb": "parAjayate"},
        ],
        "expect": [
            {"karaka": "kAraka_apAdAna", "vibhakti": ["viBakti_5"],
             "forms": ["अध्ययनात्", "अध्ययनाद्"]},
            {"forms": ["पराजयते"]},
        ],
    },
    {
        # सोढः किम् — शत्रून्पराजयते (abhibhava "defeats"): the enemies are soḍha,
        # so 1.4.26 must not fire; śatru = īpsitatama karma → dvitīyā (शत्रून्).
        "label": "SK589-negative-sodha-karma",
        "sutras": ["1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "Satru", "vacana": 3, "sem": ["semantic_Ipsitatama"]},
            {"verb": "parAjayate"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"],
             "not_fired": ["1.4.26", "2.3.28"], "forms": ["शत्रून्"]},
            {"forms": ["पराजयते"]},
        ],
    },

    # ── SK590 (1.4.27): vāraṇa īpsita → apādāna (+ go karma) ──────────────────
    {
        # यवेभ्यो गां वारयति — the desired thing warded off (yava, pl) → apādāna →
        # pañcamī (यवेभ्यः); the protected go = karma → dvitīyā (गाम्).
        "label": "SK590-yavebhyo-gam-varayati",
        "sutras": ["1.4.27", "2.3.28", "1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "yava", "vacana": 3, "sem": ["semantic_Ipsita_vAraRa"]},
            {"stem": "go", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "vArayati"},
        ],
        "expect": [
            {"karaka": "kAraka_apAdAna", "vibhakti": ["viBakti_5"],
             "forms": ["यवेभ्यः"]},
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"], "forms": ["गाम्"]},
            {"forms": ["वारयति"]},
        ],
    },

    # ── SK591 (1.4.28): antardhi → apādāna ────────────────────────────────────
    {
        # मातुर्निलीयते कृष्णः — the one hidden-from (mātṛ) → apādāna → pañcamī
        # (मातुः); Kṛṣṇa the kartṛ → prathamā (कृष्णः).
        "label": "SK591-matur-niliyate-krsnah",
        "sutras": ["1.4.28", "2.3.28", "1.4.54", "2.3.46"],
        "sentence": [
            {"stem": "mAtf", "vacana": 1, "sem": ["semantic_antardhi"]},
            {"stem": "kfzRa", "vacana": 1, "sem": ["semantic_svatantra"]},
            {"verb": "nilIyate"},
        ],
        "expect": [
            {"karaka": "kAraka_apAdAna", "vibhakti": ["viBakti_5"],
             "forms": ["मातुः"]},
            {"karaka": "kAraka_kartA", "vibhakti": ["viBakti_1"], "forms": ["कृष्णः"]},
            {"forms": ["निलीयते"]},
        ],
    },

    # ── SK592 (1.4.29): ākhyātṛ upayoga → apādāna ─────────────────────────────
    {
        # उपाध्यायादधीते — the teacher (upādhyāya), in regulated learning → apādāna
        # → pañcamī (उपाध्यायाद्/उपाध्यायात्).
        "label": "SK592-upadhyayad-adhite",
        "sutras": ["1.4.29", "2.3.28"],
        "sentence": [
            {"stem": "upADyAya", "vacana": 1, "sem": ["semantic_AKyAtf"]},
            {"verb": "aDIte"},
        ],
        "expect": [
            {"karaka": "kAraka_apAdAna", "vibhakti": ["viBakti_5"],
             "forms": ["उपाध्यायाद्", "उपाध्यायात्"]},
            {"forms": ["अधीते"]},
        ],
    },

    # ── SK593 (1.4.30): jani-prakṛti → apādāna ────────────────────────────────
    {
        # ग्रामात्प्रजायते — the source (grāma) of what is born (prakṛti of the
        # √jan agent) → apādāna → pañcamī (ग्रामात्/ग्रामाद्). (a-stem stand-in for
        # the SK's an-stem ब्रह्मणः.)
        "label": "SK593-gramat-prajayate",
        "sutras": ["1.4.30", "2.3.28"],
        "sentence": [
            {"stem": "grAma", "vacana": 1, "sem": ["semantic_janiprakfti"]},
            {"verb": "prajAyate"},
        ],
        "expect": [
            {"karaka": "kAraka_apAdAna", "vibhakti": ["viBakti_5"],
             "forms": ["ग्रामात्", "ग्रामाद्"]},
            {"forms": ["प्रजायते"]},
        ],
    },

    # ── SK594 (1.4.31): bhuvaḥ prabhava → apādāna ─────────────────────────────
    {
        # हिमवतो गङ्गा प्रभवति — the place of origin (himavat) of the √bhū agent →
        # apādāna → pañcamī (हिमवतः); Gaṅgā the kartṛ → prathamā (गङ्गा).
        "label": "SK594-himavato-ganga-prabhavati",
        "sutras": ["1.4.31", "2.3.28", "1.4.54", "2.3.46"],
        "sentence": [
            {"stem": "himavat", "vacana": 1, "sem": ["semantic_praBava"]},
            {"stem": "gaNgA", "vacana": 1, "sem": ["semantic_svatantra"]},
            {"verb": "praBavati"},
        ],
        "expect": [
            {"karaka": "kAraka_apAdAna", "vibhakti": ["viBakti_5"],
             "forms": ["हिमवतः"]},
            {"karaka": "kAraka_kartA", "vibhakti": ["viBakti_1"], "forms": ["गङ्गा"]},
            {"forms": ["प्रभवति"]},
        ],
    },

    # ── SK595 (2.3.29): anya/ārāt/itara/ṛte/dik-yoga → pañcamī ────────────────
    {
        # अन्यो रामात् — rāma in yoga with anya → pañcamī (रामात्/रामाद्); anya itself
        # is its own prathamā (अन्यत्/अन्यद्, neuter sarvanāma). anya is rāma's llp.
        "label": "SK595-anyo-ramat",
        "sutras": ["2.3.29", "2.3.46"],
        "sentence": [
            {"stem": "anya", "vacana": 1, "sem": ["semantic_prAtipadikArTa"], "dir": "para"},
            {"stem": "rAma", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["अन्यत्", "अन्यद्"]},
            {"karaka": None, "vibhakti": ["viBakti_5"],
             "not_fired": ["2.3.46"], "forms": ["रामात्", "रामाद्"]},
        ],
    },
    {
        # Direction (the headline review case): कृष्ण अन्य(para) राम — anya with
        # dir=para governs ONLY the following rāma (→ pañcamī रामात्); the preceding
        # kṛṣṇa is NOT governed and defaults to prathamā (कृष्णः). Pre-fix this gave
        # both kṛṣṇād AND rāmāt (anya fired on both neighbours).
        "label": "SK595-krsna-anya-rama-para",
        "sutras": ["2.3.29", "2.3.46"],
        "sentence": [
            {"stem": "kfzRa", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
            {"stem": "anya", "vacana": 1,
             "sem": ["semantic_prAtipadikArTa"], "dir": "para"},
            {"stem": "rAma", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_1"],
             "not_fired": ["2.3.29"], "forms": ["कृष्णः"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["अन्यत्", "अन्यद्"]},
            {"karaka": None, "vibhakti": ["viBakti_5"],
             "not_fired": ["2.3.46"], "forms": ["रामात्", "रामाद्"]},
        ],
    },
    {
        # Mirror with dir=pUrva: कृष्ण(←anya) — anya governs the PRECEDING kṛṣṇa
        # (→ कृष्णात्); the following rāma defaults to prathamā.
        "label": "SK595-krsna-anya-rama-purva",
        "sutras": ["2.3.29", "2.3.46"],
        "sentence": [
            {"stem": "kfzRa", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
            {"stem": "anya", "vacana": 1,
             "sem": ["semantic_prAtipadikArTa"], "dir": "pUrva"},
            {"stem": "rAma", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_5"],
             "not_fired": ["2.3.46"], "forms": ["कृष्णात्", "कृष्णाद्"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["अन्यत्", "अन्यद्"]},
            {"karaka": None, "vibhakti": ["viBakti_1"],
             "not_fired": ["2.3.29"], "forms": ["रामः"]},
        ],
    },
    {
        # dik-word class via the ?dikSabda tag (not a literal): पूर्वो ग्रामात् —
        # pūrva (a dik-śabda) with dir=pUrva governs the preceding grāma → pañcamī.
        "label": "SK595-grama-purva-diksabda",
        "sutras": ["2.3.29", "2.3.46"],
        "sentence": [
            {"stem": "grAma", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
            {"stem": "pUrva_dik", "vacana": 1,
             "sem": ["semantic_prAtipadikArTa"], "dir": "pUrva"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_5"],
             "not_fired": ["2.3.46"], "forms": ["ग्रामात्", "ग्रामाद्"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["पूर्वः"]},
        ],
    },

    # ── SK596 (1.4.88) + SK598 (2.3.10): apa/pari varjana kp → pañcamī ────────
    {
        # अप हरेः (संसारः) — apa (varjana sense) is karmapravacanīya governing the
        # following hari → pañcamī (हरेः). apa is hari's llp.
        "label": "SK598-apa-hareh",
        "sutras": ["1.4.88", "2.3.10"],
        "sentence": [
            {"word": "apa_kp", "sem": ["semantic_varjana"], "dir": "para"},
            {"stem": "hari", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"forms": ["अप"]},
            {"karaka": None, "vibhakti": ["viBakti_5"],
             "not_fired": ["2.3.46"], "forms": ["हरेः"]},
        ],
    },
    {
        # परि हरेः (संसारः) — pari in varjana → kp; same pañcamī (हरेः).
        "label": "SK598-pari-hareh",
        "sutras": ["1.4.88", "2.3.10"],
        "sentence": [
            {"word": "pari_kp", "sem": ["semantic_varjana"], "dir": "para"},
            {"stem": "hari", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"forms": ["परि"]},
            {"karaka": None, "vibhakti": ["viBakti_5"], "forms": ["हरेः"]},
        ],
    },

    # ── SK597 (1.4.89) + SK598 (2.3.10): āṅ maryādā kp → pañcamī ──────────────
    {
        # आ मुक्तेः (संसारः) — āṅ (maryādā "up to") is kp governing the following
        # noun → pañcamī. Modelled with hari (आ हरेः) → हरेः; āṅ surfaces आ.
        "label": "SK597-a-hareh-maryada",
        "sutras": ["1.4.89", "2.3.10"],
        "sentence": [
            {"word": "AN_kp", "sem": ["semantic_maryAdA"], "dir": "para"},
            {"stem": "hari", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"forms": ["आ"]},
            {"karaka": None, "vibhakti": ["viBakti_5"], "forms": ["हरेः"]},
        ],
    },

    # ── SK599 (1.4.92) + SK600 (2.3.11): prati pratinidhi/pratidāna kp → pañcamī ─
    {
        # कृष्णात्प्रति (प्रद्युम्नः) — prati (pratinidhi "in place of") is kp governing
        # the PRECEDING noun (kṛṣṇa) → pañcamī. Modelled with hari (हरेः प्रति);
        # prati is hari's rrp (dir=pUrva). The kp_pancamI_pratinidhi marker keeps
        # this on 2.3.11, distinct from 2.3.10 (apa/āṅ/pari, kp_pancamI).
        "label": "SK600-hareh-prati-pratinidhi",
        "sutras": ["1.4.92", "2.3.11"],
        "sentence": [
            {"stem": "hari", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
            {"word": "prati_kp", "sem": ["semantic_pratiniDi"], "dir": "pUrva"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_5"],
             "not_fired": ["2.3.46", "2.3.10"], "forms": ["हरेः"]},
            {"forms": ["प्रति"]},
        ],
    },
    {
        # शताद्प्रति (तिलेभ्यः प्रतियच्छति माषान्) — pratidāna "in exchange for" sense;
        # śata governed by prati → pañcamī (शताद्/शतात्).
        "label": "SK600-satat-prati-pratidana",
        "sutras": ["1.4.92", "2.3.11"],
        "sentence": [
            {"stem": "Sata", "vacana": 1, "sem": ["semantic_pratidAna"]},
            {"word": "prati_kp", "sem": ["semantic_pratidAna"], "dir": "pUrva"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_5"], "forms": ["शताद्", "शतात्"]},
            {"forms": ["प्रति"]},
        ],
    },

    # ── SK601 (2.3.24): akartari ṛṇe → pañcamī (+ negative) ───────────────────
    {
        # शताद्बद्धः — the debt (śata, a non-agent cause) → pañcamī (शताद्/शतात्).
        # akartari: the debt is not the karaṇa/kartṛ of binding.
        "label": "SK601-satad-baddhah-rna",
        "sutras": ["2.3.24"],
        "sentence": [
            {"stem": "Sata", "vacana": 1, "sem": ["semantic_fRa"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_5"],
             "not_fired": ["2.3.46"], "forms": ["शताद्", "शतात्"]},
        ],
    },
    {
        # अकर्तरि किम् — शतेन बन्धितः: the debt AS the karaṇa (agent of binding) →
        # tṛtīyā (शतेन), not pañcamī; 2.3.24 must not fire. The śata is sādhakatama
        # → 1.4.42 karaṇa → 2.3.18.
        "label": "SK601-negative-kartari-karana",
        "sutras": ["1.4.42", "2.3.18"],
        "sentence": [
            {"stem": "Sata", "vacana": 1, "sem": ["semantic_sADakatama"]},
        ],
        "expect": [
            {"karaka": "kAraka_karaRa", "vibhakti": ["viBakti_3"],
             "not_fired": ["2.3.24"], "forms": ["शतेन"]},
        ],
    },
    {
        # akartari guard: a debt that IS the agent (semantic_fRa + svatantra kartṛ)
        # must NOT take the 2.3.24 pañcamī. With no abhihita verb the kartā is
        # anabhihita → 2.3.18 tṛtīyā (शतेन); the key point is 2.3.24 does not fire.
        # Confirms the ?!semantic_svatantra guard added to 2.3.24.
        "label": "SK601-negative-rna-svatantra",
        "sutras": ["1.4.54", "2.3.18"],
        "sentence": [
            {"stem": "Sata", "vacana": 1,
             "sem": ["semantic_fRa", "semantic_svatantra"]},
        ],
        "expect": [
            {"karaka": "kAraka_kartA", "vibhakti": ["viBakti_3"],
             "not_fired": ["2.3.24"], "forms": ["शतेन"]},
        ],
    },

    # ── SK602 (2.3.25): vibhāṣā guṇe astriyām → pañcamī / tṛtīyā ──────────────
    {
        # जाड्याज्जाड्येन वा (बद्धः) — the non-feminine guṇa-hetu jāḍya is optionally
        # pañcamī (जाड्यात्/जाड्याद्, via 2.3.25) or tṛtīyā (जाड्येन, fall-through to
        # 2.3.23 hetu). Fork. The noun carries semantic_hetu for the skip branch.
        "label": "SK602-jadyaj-jadyena-guna",
        "sutras": ["2.3.25", "2.3.23"],
        "sentence": [
            {"stem": "jAqya", "vacana": 1,
             "sem": ["semantic_guRahetu", "semantic_hetu"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_5", "viBakti_3"],
             "forms": ["जाड्यात्", "जाड्याद्", "जाड्येन"]},
        ],
    },

    # ── SK604 (2.3.33): karaṇe stoka/alpa/… adravya → pañcamī / tṛtīyā ────────
    {
        # स्तोकेन स्तोकाद्वा (मुक्तः) — stoka as adravya karaṇa is optionally pañcamī
        # (स्तोकात्/स्तोकाद्, via 2.3.33) or tṛtīyā (स्तोकेन, fall-through to 1.4.42
        # karaṇa → 2.3.18). Fork. The noun carries semantic_sADakatama for the
        # skip branch.
        "label": "SK604-stokad-stokena-karana",
        "sutras": ["2.3.33", "1.4.42", "2.3.18"],
        "sentence": [
            {"stem": "stoka", "vacana": 1,
             "sem": ["semantic_stokAdi", "semantic_sADakatama"]},
        ],
        "expect": [
            {"karaka": "kAraka_karaRa",
             "vibhakti": ["viBakti_5", "viBakti_3"],
             "forms": ["स्तोकात्", "स्तोकाद्", "स्तोकेन"]},
        ],
    },

    # ── SK603 (2.3.32): pṛthak/vinā/nānā → THREE-way tṛtīyā/pañcamī/dvitīyā ───
    {
        # पृथग् रामेण रामात् रामं वा — with pṛthak the noun is tṛtīyā (रामेण, 2.3.32.2),
        # pañcamī (रामात्/रामाद्, 2.3.32.1), OR dvitīyā (रामम्, 2.3.32). Three-arm
        # fork. pṛthak is rāma's llp.
        "label": "SK603-prthag-ramena-ramat-ramam",
        "sutras": ["2.3.32.2", "2.3.32.1", "2.3.32"],
        "sentence": [
            {"word": "pfTak", "dir": "para"},
            {"stem": "rAma", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"forms": ["पृथक्"]},
            {"karaka": None,
             "vibhakti": ["viBakti_2", "viBakti_3", "viBakti_5"],
             "not_fired": ["2.3.46"],
             "forms": ["रामेण", "रामात्", "रामाद्", "रामम्"]},
        ],
    },
    {
        # विना रामेण रामात् रामं वा — same three-way fork with vinā.
        "label": "SK603-vina-ramena-ramat-ramam",
        "sutras": ["2.3.32.2", "2.3.32.1", "2.3.32"],
        "sentence": [
            {"word": "vinA", "dir": "para"},
            {"stem": "rAma", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"forms": ["विना"]},
            {"karaka": None,
             "vibhakti": ["viBakti_2", "viBakti_3", "viBakti_5"],
             "forms": ["रामेण", "रामात्", "रामाद्", "रामम्"]},
        ],
    },

    # ── SK605 (2.3.35 + 2.3.36.1 च): dūra/antika → FOUR-way 2/5/3/7 ──────────
    {
        # ग्रामस्य दूरं दूरात् दूरेण वा — dūra (a-stem napuṃsaka, declines itself) is
        # dvitīyā (दूरम्, 2.3.35.2), pañcamī (दूरात्/दूराद्, 2.3.35.1), OR tṛtīyā
        # (दूरेण, 2.3.35). Three-arm fork.
        "label": "SK605-duram-durat-durena",
        "sutras": ["2.3.36.1", "2.3.35.2", "2.3.35.1", "2.3.35"],
        "sentence": [
            {"stem": "dUra", "vacana": 1, "sem": ["semantic_dUrAntika"]},
        ],
        "expect": [
            {"karaka": None,
             "vibhakti": ["viBakti_2", "viBakti_3", "viBakti_5", "viBakti_7"],
             "not_fired": ["2.3.46"],
             "forms": ["दूरम्", "दूरात्", "दूराद्", "दूरेण", "दूरे"]},
        ],
    },
    {
        # अन्तिकम् अन्तिकात् अन्तिकेन वा — same three-way fork with antika.
        "label": "SK605-antikam-antikat-antikena",
        "sutras": ["2.3.36.1", "2.3.35.2", "2.3.35.1", "2.3.35"],
        "sentence": [
            {"stem": "antika", "vacana": 1, "sem": ["semantic_dUrAntika"]},
        ],
        "expect": [
            {"karaka": None,
             "vibhakti": ["viBakti_2", "viBakti_3", "viBakti_5", "viBakti_7"],
             "forms": ["अन्तिकम्", "अन्तिकात्", "अन्तिकाद्", "अन्तिकेन", "अन्तिके"]},
        ],
    },

    # Phase K6 — Ṣaṣṭhī (SK607–631; karaka_plan.md §K6). The ṣaṣṭhī chapter.
    # Three families: (a) yoga-word peeks — a fixed-surface particle (hetoH,
    # dakziRatas, …) read via llp/rrp, like K2/K3 saha/namas; (b) verb-conditioned
    # śeṣa-ṣaṣṭhī (2.3.51–58/61) — the noun carries semantic_Seza, the rule reads
    # the verb's meaning-class tag via rp, apavāda to 2.3.50; (c) kṛd-yoga
    # (2.3.65–71) — the governing kṛdanta noun carries a kṛt-TYPE tag (kft /
    # kta_vartamAna / kta_aDikaraRa / kftya / kft_aSazWI) read via llp/rrp.
    # Deferred: SK624 (2.3.66 ubhaya-prāpti); SK627/628 (2.3.69/70) are realized
    # as the ?!kft_aSazWI guard on 2.3.65 (asserted via the घातुक negative).
    # Examples from references/siddhantakaumudi.html anchors SK607–631; the
    # fixed-surface yoga-words (hetoH/dakziRatas/…) pass through bare (s-final
    # avyaya keep their s, e.g. दक्षिणतस्) — the rule of interest is the cause/
    # kāraka noun's vibhakti, not the particle surface.
    # ════════════════════════════════════════════════════════════════════════

    # ── SK607 (2.3.26): hetu-word → cause ṣaṣṭhī ─────────────────────────────
    {
        # अन्नस्य हेतोर्वसति (reduced: अन्नस्य हेतोः) — anna → ṣaṣṭhī (hetu-word peek).
        "label": "SK607-annasya-hetoh",
        "sutras": ["2.3.26"],
        "sentence": [
            {"stem": "anna", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
            {"word": "hetoH", "dir": "pUrva"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.46"], "forms": ["अन्नस्य"]},
            {"forms": ["हेतोः"]},
        ],
    },

    # ── SK608 (2.3.27): sarvanāman cause + hetu → tṛtīyā / ṣaṣṭhī fork ────────
    {
        # केन हेतुना / कस्य हेतोः — the sarvanāman kim is optionally tṛtīyā (केन, via
        # 2.3.27) or ṣaṣṭhī (कस्य, fall-through to 2.3.26). Fork; the hetu-word is
        # fixed-surface हेतुना here (both branches share it).
        "label": "SK608-kena-kasya-hetuna",
        "sutras": ["2.3.27", "2.3.26"],
        "sentence": [
            {"stem": "kim", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
            {"word": "hetunA", "dir": "pUrva"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_3", "viBakti_6"],
             "not_fired": ["2.3.46"], "forms": ["केन", "कस्य"]},
            {"forms": ["हेतुना"]},
        ],
    },

    # ── SK609 (2.3.30): atasartha-pratyaya word → ṣaṣṭhī ─────────────────────
    {
        # ग्रामस्य दक्षिणतः — grāma → ṣaṣṭhī (dakṣiṇataḥ peek). dakziRatas is s-final
        # avyaya → surfaces दक्षिणतस्.
        "label": "SK609-gramasya-dakshinatah",
        "sutras": ["2.3.30"],
        "sentence": [
            {"stem": "grAma", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
            {"word": "dakziRatas", "dir": "pUrva"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.46"], "forms": ["ग्रामस्य"]},
            {"forms": ["दक्षिणतस्"]},
        ],
    },
    {
        # Generality: a SECOND atasartha word (uttaratas) via the ?atasuCarTa tag,
        # not a literal. ग्रामस्य उत्तरतः → ṣaṣṭhī.
        "label": "SK609-gramasya-uttaratah",
        "sutras": ["2.3.30"],
        "sentence": [
            {"stem": "grAma", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
            {"word": "uttaratas", "dir": "pUrva"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.46"], "forms": ["ग्रामस्य"]},
            {"forms": ["उत्तरतस्"]},
        ],
    },

    # ── SK610 (2.3.31): enap-anta word → dvitīyā / ṣaṣṭhī fork ───────────────
    {
        # दक्षिणेन ग्रामं / ग्रामस्य — grāma is optionally dvitīyā (ग्रामम्, via 2.3.31)
        # or ṣaṣṭhī (ग्रामस्य, via the 2.3.31.1 yoga-vibhāga companion). Fork.
        "label": "SK610-dakshinena-gramam-gramasya",
        "sutras": ["2.3.31", "2.3.31.1"],
        "sentence": [
            {"word": "dakziRena", "dir": "para"},
            {"stem": "grAma", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"forms": ["दक्षिणेन"]},
            {"karaka": None, "vibhakti": ["viBakti_2", "viBakti_6"],
             "not_fired": ["2.3.46"], "forms": ["ग्रामम्", "ग्रामस्य"]},
        ],
    },
    {
        # Generality: a SECOND enap-anta word (uttareṇa) via the ?enap tag.
        # उत्तरेण ग्रामं / ग्रामस्य → same dvitīyā/ṣaṣṭhī fork.
        "label": "SK610-uttarena-gramam-gramasya",
        "sutras": ["2.3.31", "2.3.31.1"],
        "sentence": [
            {"word": "uttareRa", "dir": "para"},
            {"stem": "grAma", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"forms": ["उत्तरेण"]},
            {"karaka": None, "vibhakti": ["viBakti_2", "viBakti_6"],
             "not_fired": ["2.3.46"], "forms": ["ग्रामम्", "ग्रामस्य"]},
        ],
    },

    # ── SK611 (2.3.34): dūra/antika word → ṣaṣṭhī / pañcamī fork ─────────────
    {
        # दूरं ग्रामस्य / ग्रामात् — grāma is optionally ṣaṣṭhī (ग्रामस्य, via 2.3.34)
        # or pañcamī (ग्रामात्, via the 2.3.34.1 companion). Fork.
        "label": "SK611-duram-gramasya-gramat",
        "sutras": ["2.3.34", "2.3.34.1"],
        "sentence": [
            {"word": "dUram", "dir": "para"},
            {"stem": "grAma", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"forms": ["दूरम्"]},
            {"karaka": None, "vibhakti": ["viBakti_6", "viBakti_5"],
             "not_fired": ["2.3.46"], "forms": ["ग्रामस्य", "ग्रामात्", "ग्रामाद्"]},
        ],
    },

    # ── SK612 (2.3.51): jñā-non-know karaṇa → śeṣa ṣaṣṭhī ────────────────────
    {
        # सर्पिषो जानीते — the karaṇa sarpis, named (śeṣa), → ṣaṣṭhī. Apavāda to
        # 2.3.50 (2.3.51 names the jñā-avidartha scope in the trace).
        "label": "SK612-sarpiso-janite",
        "sutras": ["2.3.51"],
        "sentence": [
            {"stem": "sarpis", "vacana": 1, "sem": ["semantic_Seza"]},
            {"verb": "jAnIte"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.50"], "forms": ["सर्पिषः"]},
            {"forms": ["जानीते"]},
        ],
    },

    # ── SK613 (2.3.52): adhi-i/day/īś karman → śeṣa ṣaṣṭhī ───────────────────
    {
        # मातुः स्मरति — the karman mātṛ (remembered), named, → ṣaṣṭhī.
        "label": "SK613-matuh-smarati",
        "sutras": ["2.3.52"],
        "sentence": [
            {"stem": "mAtf", "vacana": 1, "sem": ["semantic_Seza"]},
            {"verb": "smarati"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.50"], "forms": ["मातुः"]},
            {"forms": ["स्मरति"]},
        ],
    },
    {
        # मातुर्दयते — the day-group of 2.3.52 (?daya arm); karman mātṛ → ṣaṣṭhī.
        "label": "SK613-matuh-dayate",
        "sutras": ["2.3.52"],
        "sentence": [
            {"stem": "mAtf", "vacana": 1, "sem": ["semantic_Seza"]},
            {"verb": "dayate"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.50"], "forms": ["मातुः"]},
            {"forms": ["दयते"]},
        ],
    },
    {
        # गवामीष्टे — the īś-group of 2.3.52 (?IS arm); karman go → ṣaṣṭhī.
        "label": "SK613-gavam-iste",
        "sutras": ["2.3.52"],
        "sentence": [
            {"stem": "go", "vacana": 3, "sem": ["semantic_Seza"]},
            {"verb": "ISte"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.50"], "forms": ["गवाम्"]},
            {"forms": ["ईष्टे"]},
        ],
    },

    # ── SK614 (2.3.53): kṛ-pratiyatna karman → śeṣa ṣaṣṭhī ───────────────────
    {
        # ओदनस्योपस्कुरुते — the karman odana (in guṇādhāna), named, → ṣaṣṭhī.
        "label": "SK614-odanasya-upaskurute",
        "sutras": ["2.3.53"],
        "sentence": [
            {"stem": "odana", "vacana": 1, "sem": ["semantic_Seza"]},
            {"verb": "upaskurute"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.50"], "forms": ["ओदनस्य"]},
            {"forms": ["उपस्कुरुते"]},
        ],
    },

    # ── SK615 (2.3.54): ruj-bhāva karman → śeṣa ṣaṣṭhī ───────────────────────
    {
        # चौरस्य रुजति — the karman caura (pained), named, → ṣaṣṭhī.
        "label": "SK615-caurasya-rujati",
        "sutras": ["2.3.54"],
        "sentence": [
            {"stem": "cOra", "vacana": 1, "sem": ["semantic_Seza"]},
            {"verb": "rujati"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.50"], "forms": ["चौरस्य"]},
            {"forms": ["रुजति"]},
        ],
    },

    # ── SK616 (2.3.55): nāth-āśis karman → śeṣa ṣaṣṭhī ───────────────────────
    {
        # सर्पिषो नाथते — the karman sarpis (blessed-for), named, → ṣaṣṭhī.
        "label": "SK616-sarpiso-nathate",
        "sutras": ["2.3.55"],
        "sentence": [
            {"stem": "sarpis", "vacana": 1, "sem": ["semantic_Seza"]},
            {"verb": "nATate"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.50"], "forms": ["सर्पिषः"]},
            {"forms": ["नाथते"]},
        ],
    },

    # ── SK617 (2.3.56): hiṁsā-class karman → śeṣa ṣaṣṭhī ─────────────────────
    {
        # चौरस्योज्जासयति — the karman caura (destroyed), named, → ṣaṣṭhī.
        "label": "SK617-caurasya-ujjasayati",
        "sutras": ["2.3.56"],
        "sentence": [
            {"stem": "cOra", "vacana": 1, "sem": ["semantic_Seza"]},
            {"verb": "ujjAsayati"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.50"], "forms": ["चौरस्य"]},
            {"forms": ["उज्जासयति"]},
        ],
    },
    {
        # चौरस्य पिनष्टि — a second jāsi-class (jasAdi) hiṁsā verb (√piṣ); the
        # named karman caura → ṣaṣṭhī. Confirms 2.3.56 keys on ?jasAdi, not a literal.
        "label": "SK617-caurasya-pinasti",
        "sutras": ["2.3.56"],
        "sentence": [
            {"stem": "cOra", "vacana": 1, "sem": ["semantic_Seza"]},
            {"verb": "pinazwi"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.50"], "forms": ["चौरस्य"]},
            {"forms": ["पिनष्टि"]},
        ],
    },

    # ── SK618 (2.3.57): vyavahṛ/paṇ samartha karman → śeṣa ṣaṣṭhī ────────────
    {
        # शतस्य व्यवहरति — the karman śata (transacted), named, → ṣaṣṭhī.
        "label": "SK618-satasya-vyavaharati",
        "sutras": ["2.3.57"],
        "sentence": [
            {"stem": "Sata", "vacana": 1, "sem": ["semantic_Seza"]},
            {"verb": "vyavaharati"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.50"], "forms": ["शतस्य"]},
            {"forms": ["व्यवहरति"]},
        ],
    },
    {
        # शतस्य पणते — the √paṇ arm of 2.3.57 (?paR); the named karman śata → ṣaṣṭhī.
        "label": "SK618-satasya-panate",
        "sutras": ["2.3.57"],
        "sentence": [
            {"stem": "Sata", "vacana": 1, "sem": ["semantic_Seza"]},
            {"verb": "paRate"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.50"], "forms": ["शतस्य"]},
            {"forms": ["पणते"]},
        ],
    },

    # ── SK619 (2.3.58): div-gamble karman → śeṣa ṣaṣṭhī (non-upasṛṣṭa) ───────
    {
        # शतस्य दीव्यति — the karman śata (gambled-for), named, → ṣaṣṭhī. dīvyati
        # is non-upasṛṣṭa, so 2.3.58 (not the 2.3.59 vibhāṣā) fires.
        "label": "SK619-satasya-divyati",
        "sutras": ["2.3.58"],
        "sentence": [
            {"stem": "Sata", "vacana": 1, "sem": ["semantic_Seza"]},
            {"verb": "dIvyatiK6"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.50", "2.3.59"], "forms": ["शतस्य"]},
            {"forms": ["दीव्यति"]},
        ],
    },

    # ── SK620 (2.3.59): upasṛṣṭa div → ṣaṣṭhī / dvitīyā fork ─────────────────
    {
        # शतस्य / शतं प्रतिदीव्यति — with upasṛṣṭa prati-div the karman śata is
        # optionally ṣaṣṭhī (शतस्य, via 2.3.59) or the plain karma dvitīyā (शतम्,
        # via 2.3.2). Fork. The noun is kAraka_karma (1.4.49) in both branches.
        "label": "SK620-satasya-satam-pratidivyati",
        "sutras": ["2.3.59", "1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "Sata", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "pratidIvyati"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_6", "viBakti_2"],
             "forms": ["शतस्य", "शतम्"]},
            {"forms": ["प्रतिदीव्यति"]},
        ],
    },

    # ── SK621 (2.3.61): preṣ/brū havis devatā-sampradāna → śeṣa ṣaṣṭhī ───────
    {
        # छागस्य प्रेष्यति — the havis-related karman chāga, named, → ṣaṣṭhī.
        "label": "SK621-chagasya-presyati",
        "sutras": ["2.3.61"],
        "sentence": [
            {"stem": "CAga", "vacana": 1, "sem": ["semantic_Seza", "semantic_havis"]},
            {"verb": "prezyati"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.50"], "forms": ["छागस्य"]},
            {"forms": ["प्रेष्यति"]},
        ],
    },
    {
        # छागस्य ब्रूते — same 2.3.61 with √brū (the other listed root); the
        # havis-karman chāga → ṣaṣṭhī. Exercises the ?brU arm + havis guard.
        "label": "SK621-chagasya-brute",
        "sutras": ["2.3.61"],
        "sentence": [
            {"stem": "CAga", "vacana": 1, "sem": ["semantic_Seza", "semantic_havis"]},
            {"verb": "brUte"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.50"], "forms": ["छागस्य"]},
            {"forms": ["ब्रूते"]},
        ],
    },

    # ── SK622 (2.3.64): kṛtvas-word + kāla adhikaraṇa → śeṣa ṣaṣṭhī ──────────
    {
        # पञ्चकृत्वोऽह्नः (reduced: पञ्चकृत्वः अह्नः) — the kāla ahan, named, → ṣaṣṭhī
        # (kṛtvas-word peek). pañcakṛtvas is s-final avyaya → surfaces पञ्चकृत्वस्.
        "label": "SK622-pancakrtvo-ahnah",
        "sutras": ["2.3.64"],
        "sentence": [
            {"word": "paYcakftvas", "dir": "para"},
            {"stem": "ahan", "vacana": 1, "sem": ["semantic_Seza"]},
        ],
        "expect": [
            {"forms": ["पञ्चकृत्वस्"]},
            {"karaka": None, "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.50", "2.3.46"], "forms": ["अह्नः"]},
        ],
    },
    {
        # Generality: a SECOND kṛtvas-artha word (saptakṛtvas) via the ?kftvasuCarTa
        # tag. सप्तकृत्वोऽह्नः → ṣaṣṭhī.
        "label": "SK622-saptakrtvo-ahnah",
        "sutras": ["2.3.64"],
        "sentence": [
            {"word": "saptakftvas", "dir": "para"},
            {"stem": "ahan", "vacana": 1, "sem": ["semantic_Seza"]},
        ],
        "expect": [
            {"forms": ["सप्तकृत्वस्"]},
            {"karaka": None, "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.50", "2.3.46"], "forms": ["अह्नः"]},
        ],
    },

    # ── SK623 (2.3.65): kartṛ/karman in kṛd-yoga → ṣaṣṭhī ────────────────────
    {
        # ओदनस्य पाचकः — the karman odana, governed by the kṛdanta pācaka (?kft),
        # → ṣaṣṭhī. No finite verb (empty-sentinel dhātu).
        "label": "SK623-odanasya-pacakah",
        "sutras": ["2.3.65"],
        "sentence": [
            {"stem": "odana", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"stem": "pAcaka", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.2"], "forms": ["ओदनस्य"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["पाचकः"]},
        ],
    },
    {
        # हरेः कृतिः — the kartṛ hari, governed by the kṛdanta kṛti (?kft), → ṣaṣṭhī.
        "label": "SK623-hareh-krtih",
        "sutras": ["2.3.65"],
        "sentence": [
            {"stem": "hari", "vacana": 1, "sem": ["semantic_svatantra"]},
            {"stem": "kfti", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"karaka": "kAraka_kartA", "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.18"], "forms": ["हरेः"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["कृतिः"]},
        ],
    },

    # ── SK625 (2.3.67): kta-vartamāna governor → ṣaṣṭhī ──────────────────────
    {
        # राज्ञां मतः — the kartṛ rājan (pl.), governed by the present-sense kta
        # mata, → ṣaṣṭhī.
        "label": "SK625-rajnam-matah",
        "sutras": ["2.3.67"],
        "sentence": [
            {"stem": "rAjan", "vacana": 3, "sem": ["semantic_svatantra"]},
            {"stem": "mata", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"karaka": "kAraka_kartA", "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.18"], "forms": ["राज्ञाम्"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["मतः"]},
        ],
    },

    # ── SK626 (2.3.68): kta-adhikaraṇa governor → ṣaṣṭhī ─────────────────────
    {
        # एतेषामासितम् — the kartṛ etad (pl.), governed by the adhikaraṇa-kta āsita,
        # → ṣaṣṭhī.
        "label": "SK626-etesham-asitam",
        "sutras": ["2.3.68"],
        "sentence": [
            {"stem": "etad", "vacana": 3, "sem": ["semantic_svatantra"]},
            {"stem": "Asita", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"karaka": "kAraka_kartA", "vibhakti": ["viBakti_6"],
             "not_fired": ["2.3.18"], "forms": ["एतेषाम्"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["आसितम्"]},
        ],
    },

    # ── SK627/628 (2.3.69/70): prohibition — 2.3.65 must NOT fire ────────────
    {
        # दैत्यान् घातुको हरिः (reduced: हरिं घातुकः) — the kṛt governor ghātuka carries
        # kft_aSazWI (ukañ-bhaviṣyat, a 2.3.70 member), so the ?!kft_aSazWI guard on
        # 2.3.65 keeps it OFF; the karman hari falls to 2.3.2 dvitīyā (हरिम्), NOT
        # ṣaṣṭhī. This realizes the 2.3.69/70 niṣedha (no positive rule).
        "label": "SK628-negative-harim-ghatukah",
        "sutras": ["1.4.49", "2.3.2", "2.3.46"],
        "sentence": [
            {"stem": "hari", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"stem": "GAtuka", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"],
             "not_fired": ["2.3.65"], "forms": ["हरिम्"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["घातुकः"]},
        ],
    },
    {
        # व्रजं गामी (reduced: ग्रामं गामी) — gāmin carries kft_aSazWI (ṇini ādhamarṇya,
        # 2.3.70), so 2.3.65 is blocked; the goal grāma → 2.3.2 dvitīyā (ग्रामम्).
        "label": "SK628-negative-gramam-gami",
        "sutras": ["1.4.49", "2.3.2", "2.3.46"],
        "sentence": [
            {"stem": "grAma", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"stem": "gAmin", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"],
             "not_fired": ["2.3.65"], "forms": ["ग्रामम्"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["गामी"]},
        ],
    },

    # ── SK629 (2.3.71): kṛtya kartṛ → ṣaṣṭhī / tṛtīyā fork ───────────────────
    {
        # मम / मया वा सेव्यः — the kartṛ asmad, governed by the kṛtya sevya, is
        # optionally ṣaṣṭhī (मम/मे, via 2.3.71) or tṛtīyā (मया, fall-through to
        # 2.3.18). Fork. asmad ṣaṣṭhī = मे/मम (form-set), tṛtīyā = मया.
        "label": "SK629-mama-maya-sevyah",
        "sutras": ["2.3.71", "1.4.54", "2.3.18"],
        "sentence": [
            {"stem": "asmad", "vacana": 1, "sem": ["semantic_svatantra"]},
            {"stem": "sevya", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"karaka": "kAraka_kartA", "vibhakti": ["viBakti_6", "viBakti_3"],
             "forms": ["मम", "मे", "मया"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["सेव्यः"]},
        ],
    },

    # ════════════════════════════════════════════════════════════════════════
    # Phase K7 — adhikaraṇa + saptamī (SK632–646; karaka_plan.md §K7). FINAL
    # kāraka phase. 1.4.45 adhikaraṇa saṁjñā → 2.3.36 saptamī; the sati-saptamī
    # absolute construction (2.3.37, both partners semantic_BAvalakzaRa); the
    # ṣaṣṭhī/saptamī forks (2.3.38–41, default ṣaṣṭhī via 2.3.50) and the
    # adhikaraṇa-default forks (2.3.7/44/45, default saptamī via 2.3.36); the
    # pañcamī (2.3.42) and sādhu/nipuṇa-arcā (2.3.43) apavādas; and the adhi/upa
    # īśvara/adhika karmapravacanīya tail (1.4.97/1.4.87.1 → kp_saptamI → 2.3.9
    # saptamī, overriding 2.3.8). Examples from references/siddhantakaumudi.html
    # anchors SK632–646. Vasu (vasu_english.txt) agrees throughout.
    # ════════════════════════════════════════════════════════════════════════

    # ── SK632 (1.4.45) + SK633 (2.3.36): ādhāra → adhikaraṇa → saptamī ────────
    {
        # कटे आस्ते — the seat (kaṭa) is the locus → adhikaraṇa → saptamī (कटे).
        "label": "SK633-kate-aste",
        "sutras": ["1.4.45", "2.3.36"],
        "sentence": [
            {"stem": "kawa", "vacana": 1, "sem": ["semantic_ADAra"]},
            {"verb": "Aste"},
        ],
        "expect": [
            {"karaka": "kAraka_aDikaraRa", "vibhakti": ["viBakti_7"], "forms": ["कटे"]},
            {"forms": ["आस्ते"]},
        ],
    },
    {
        # मोक्षे इच्छास्ति — mokṣa is the vaiṣayika ādhāra → saptamī (मोक्षे).
        "label": "SK633-mokshe-icchasti",
        "sutras": ["1.4.45", "2.3.36"],
        "sentence": [
            {"stem": "mokza", "vacana": 1, "sem": ["semantic_ADAra"]},
            {"verb": "icCAsti"},
        ],
        "expect": [
            {"karaka": "kAraka_aDikaraRa", "vibhakti": ["viBakti_7"], "forms": ["मोक्षे"]},
            {"forms": ["इच्छास्ति"]},
        ],
    },
    {
        # स्थाल्यां पचति — the pot (sthālī, ī-stem) is the aupaśleṣika ādhāra →
        # saptamī (स्थाल्याम्).
        "label": "SK633-sthalyam-pacati",
        "sutras": ["1.4.45", "2.3.36"],
        "sentence": [
            {"stem": "sTAlI", "vacana": 1, "sem": ["semantic_ADAra"]},
            {"verb": "pacati"},
        ],
        "expect": [
            {"karaka": "kAraka_aDikaraRa", "vibhakti": ["viBakti_7"], "forms": ["स्थाल्याम्"]},
            {"forms": ["पचति"]},
        ],
    },
    {
        # चकाराद्दूरान्तिकार्थेभ्यः — दूरे आस्ते: the dūra-sense word → saptamī by
        # the च of 2.3.36 (semantic_dUrAntika, NOT a kāraka). वनस्य दूरे.
        "label": "SK633-dure-durantika",
        "sutras": ["2.3.36.1", "2.3.35.2", "2.3.35.1", "2.3.35"],
        "sentence": [
            {"stem": "dUra", "vacana": 1, "sem": ["semantic_dUrAntika"]},
            {"verb": "Aste"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_2", "viBakti_3", "viBakti_5", "viBakti_7"],
             "forms": ["दूरम्", "दूरात्", "दूराद्", "दूरेण", "दूरे"]},
            {"forms": ["आस्ते"]},
        ],
    },

    # ── SK634 (2.3.37): sati-saptamī (bhāva-lakṣaṇa absolute) ─────────────────
    {
        # गोषु दुह्यमानासु गतः — "he left while the cows were being milked".
        # The absolute pair (go, duhyamānā) both carry semantic_BAvalakzaRa and
        # are adjacent; each sees the other via llp/rrp → both → saptamī
        # (गोषु loc.pl., दुह्यमानासु loc.pl.). 2.3.46 prathamā is overridden.
        "label": "SK634-goshu-duhyamanasu-gatah",
        "sutras": ["2.3.37"],
        "sentence": [
            {"stem": "go", "vacana": 3, "sem": ["semantic_BAvalakzaRa"]},
            {"stem": "duhyamAnA", "vacana": 3, "sem": ["semantic_BAvalakzaRa"]},
            {"verb": "gataH"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_7"],
             "not_fired": ["2.3.46"], "forms": ["गोषु"]},
            {"karaka": None, "vibhakti": ["viBakti_7"], "forms": ["दुह्यमानासु"]},
            {"forms": ["गतः"]},
        ],
    },

    # ── SK635 (2.3.38): षष्ठी चानादरे — anādara bhāva-lakṣaṇa, vibhāṣā 7/6 ──────
    {
        # रुदति रुदतो वा प्राव्राजीत् — "he renounced, disregarding [the kin]
        # weeping". The bhāva-lakṣaṇa locus (rudat, śatṛ) is semantic_Seza +
        # semantic_anAdara → 2.3.50 ṣaṣṭhī by default; 2.3.38 forks the optional
        # saptamī. apply ⇒ रुदति (7); skip ⇒ रुदतः (6, via 2.3.50).
        "label": "SK635-rudati-rudato-pravrajit",
        "sutras": ["2.3.38", "2.3.50"],
        "sentence": [
            {"stem": "rudat", "vacana": 1,
             "sem": ["semantic_Seza", "semantic_anAdara"]},
            {"verb": "prAvrAjIt"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_7", "viBakti_6"],
             "forms": ["रुदति", "रुदतः"]},
            {"forms": ["प्राव्राजीत्", "प्राव्राजीद्"]},
        ],
    },

    # ── SK636 (2.3.39): svāmi-yoga — vibhāṣā 6/7 ─────────────────────────────
    {
        # गवां गोषु वा स्वामी — "the owner of/over the cows". go is semantic_Seza,
        # the yoga-word svāmin is adjacent (rrp peek) → 2.3.50 ṣaṣṭhī default,
        # 2.3.39 forks the optional saptamī. apply ⇒ गोषु (7); skip ⇒ गवाम् (6).
        # svāmin itself → prathamā (स्वामी).
        "label": "SK636-gavam-goshu-svami",
        "sutras": ["2.3.39", "2.3.50"],
        "sentence": [
            {"stem": "go", "vacana": 3, "sem": ["semantic_Seza"]},
            {"stem": "svAmin", "vacana": 1, "sem": ["semantic_prAtipadikArTa"], "dir": "pUrva"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_7", "viBakti_6"],
             "forms": ["गोषु", "गवाम्"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["स्वामी"]},
        ],
    },

    # ── SK637 (2.3.40): āyukta/kuśala āsevā — vibhāṣā 6/7 ─────────────────────
    {
        # पूजने पूजनस्य वा कुशलः — "skilled at (devoted to) worship". pūjana is
        # semantic_Seza + semantic_AsevA, the yoga-word kuśala is adjacent →
        # 2.3.50 ṣaṣṭhī default, 2.3.40 forks the optional saptamī.
        # apply ⇒ पूजने (7); skip ⇒ पूजनस्य (6). kuśala → prathamā (कुशलः).
        "label": "SK637-pujane-pujanasya-kusalah",
        "sutras": ["2.3.40", "2.3.50"],
        "sentence": [
            {"stem": "pUjana", "vacana": 1,
             "sem": ["semantic_Seza", "semantic_AsevA"]},
            {"stem": "kuSala", "vacana": 1, "sem": ["semantic_prAtipadikArTa"], "dir": "pUrva"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_7", "viBakti_6"],
             "forms": ["पूजने", "पूजनस्य"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["कुशलः"]},
        ],
    },

    # ── SK638 (2.3.41): यतश्च निर्धारणम् — nirdhāraṇa whole, vibhāṣā 6/7 ─────────
    {
        # नृणां नृषु वा ब्राह्मणः श्रेष्ठः — "the best AMONG men". The whole (nṛ) is
        # semantic_Seza + semantic_nirDAraRa → 2.3.50 ṣaṣṭhī default; 2.3.41
        # forks the optional saptamī. apply ⇒ नृषु (7); skip ⇒ नृणाम्/नॄणाम् (6).
        # The singled-out brāhmaṇa → prathamā (ब्राह्मणः).
        "label": "SK638-nrnam-nrshu-brahmanah",
        "sutras": ["2.3.41", "2.3.50"],
        "sentence": [
            {"stem": "nf", "vacana": 3,
             "sem": ["semantic_Seza", "semantic_nirDAraRa"]},
            {"stem": "brAhmaRa", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_7", "viBakti_6"],
             "forms": ["नृषु", "नृणाम्", "नॄणाम्"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["ब्राह्मणः"]},
        ],
    },

    # ── SK639 (2.3.42): पञ्चमी विभक्ते — nirdhāraṇa by separation → pañcamī ──────
    {
        # माथुराः पाटलिपुत्रकेभ्य आढ्यतराः — "the Mathurans are wealthier THAN the
        # Pāṭaliputrans". The separated set (pāṭaliputraka) is semantic_viBakta →
        # pañcamī (पाटलिपुत्रकेभ्यः). The Mathurans → prathamā (माथुराः).
        "label": "SK639-mathurah-pataliputrakebhyah",
        "sutras": ["2.3.42"],
        "sentence": [
            {"stem": "mATura", "vacana": 3, "sem": ["semantic_prAtipadikArTa"]},
            {"stem": "pAwaliputraka", "vacana": 3, "sem": ["semantic_viBakta"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["माथुराः"]},
            {"karaka": None, "vibhakti": ["viBakti_5"],
             "not_fired": ["2.3.46"], "forms": ["पाटलिपुत्रकेभ्यः"]},
        ],
    },

    # ── SK640 (2.3.43): sādhu/nipuṇa arcā → saptamī ──────────────────────────
    {
        # मातरि साधुः — "good towards (his) mother" (praise). The object (mātṛ) is
        # semantic_arcA, the yoga-word sādhu adjacent → saptamī (मातरि). sādhu →
        # prathamā (साधुः). Apavāda to 2.3.46.
        "label": "SK640-matari-sadhuh",
        "sutras": ["2.3.43"],
        "sentence": [
            {"stem": "mAtf", "vacana": 1, "sem": ["semantic_arcA"]},
            {"stem": "sADu", "vacana": 1, "sem": ["semantic_prAtipadikArTa"], "dir": "pUrva"},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_7"],
             "not_fired": ["2.3.46"], "forms": ["मातरि"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["साधुः"]},
        ],
    },

    # ── SK641 (2.3.44): प्रसितोत्सुकाभ्यां तृतीया च — vibhāṣā 3/7 ─────────────────
    {
        # हरिणा प्रसितः — "intent on Hari". The object hari is semantic_ADAra
        # (→ kAraka_aDikaraRa → 2.3.36 saptamī default); the adjacent prasita word
        # (yoga_pUrva, governing the preceding hari) forks the 2.3.44 tṛtīyā.
        # apply ⇒ हरिणा (3); skip ⇒ हरौ (7). prasita itself → prathamā (प्रसितः).
        "label": "SK641-harina-harau-prasita",
        "sutras": ["2.3.44", "2.3.36"],
        "sentence": [
            {"stem": "hari", "vacana": 1, "sem": ["semantic_ADAra"]},
            {"stem": "prasita", "vacana": 1,
             "sem": ["semantic_prAtipadikArTa"], "dir": "pUrva"},
        ],
        "expect": [
            {"karaka": "kAraka_aDikaraRa",
             "vibhakti": ["viBakti_3", "viBakti_7"], "forms": ["हरिणा", "हरौ"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["प्रसितः"]},
        ],
    },
    {
        # उत्सुको हरिणा हरौ वा — utsuka FIRST (yoga_para, governs the following
        # hari); same 3/7 fork. Exercises the other root and the para direction.
        "label": "SK641-utsuko-harina-harau",
        "sutras": ["2.3.44", "2.3.36"],
        "sentence": [
            {"stem": "utsuka", "vacana": 1,
             "sem": ["semantic_prAtipadikArTa"], "dir": "para"},
            {"stem": "hari", "vacana": 1, "sem": ["semantic_ADAra"]},
        ],
        "expect": [
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["उत्सुकः"]},
            {"karaka": "kAraka_aDikaraRa",
             "vibhakti": ["viBakti_3", "viBakti_7"], "forms": ["हरिणा", "हरौ"]},
        ],
    },

    # ── SK642 (2.3.45): नक्षत्रे च लुपि — taddhita-lup nakṣatra, vibhāṣā 3/7 ──────
    {
        # मूलेन मूले वा आवाहयेत् — under the (deferred, §6) taddhita-lup the nakṣatra
        # form mūla → tṛtīyā or saptamī (adhikaraṇe). semantic_nakzatralup +
        # semantic_ADAra → 2.3.36 saptamī default; 2.3.45 forks the tṛtīyā.
        # apply ⇒ मूलेन (3); skip ⇒ मूले (7). (modelled on the plain stem मूल.)
        "label": "SK642-mulena-mule-nakshatra",
        "sutras": ["2.3.45", "2.3.36"],
        "sentence": [
            {"stem": "mUla", "vacana": 1,
             "sem": ["semantic_ADAra", "semantic_nakzatralup"]},
            {"verb": "pacati"},
        ],
        "expect": [
            {"karaka": "kAraka_aDikaraRa",
             "vibhakti": ["viBakti_3", "viBakti_7"], "forms": ["मूलेन", "मूले"]},
            {"forms": ["पचति"]},
        ],
    },

    # ── SK643 (2.3.7): सप्तमीपञ्चम्यौ कारकमध्ये — kāla/adhvan between śaktis, 7/5 ──
    {
        # द्व्यहे द्व्यहाद्वा भोक्ता — "he will eat in / after two days". The kāla
        # (dvyaha) lies between kartṛ-karma śaktis: semantic_ADAra +
        # semantic_kArakamaDya → 2.3.36 saptamī default; 2.3.7 forks the pañcamī.
        # apply ⇒ द्व्यहात्/द्व्यहाद् (5); skip ⇒ द्व्यहे (7).
        "label": "SK643-dvyahe-dvyahat-karakamadhya",
        "sutras": ["2.3.7", "2.3.36"],
        "sentence": [
            {"stem": "dvyaha", "vacana": 1,
             "sem": ["semantic_ADAra", "semantic_kArakamaDya"]},
            {"verb": "icCAsti"},
        ],
        "expect": [
            {"karaka": "kAraka_aDikaraRa",
             "vibhakti": ["viBakti_5", "viBakti_7"],
             "forms": ["द्व्यहात्", "द्व्यहाद्", "द्व्यहे"]},
            {"forms": ["इच्छास्ति"]},
        ],
    },
    {
        # क्रोशे क्रोशाद्वा लक्ष्यं विध्येत् — the adhvan (krośa) between kartṛ-karma →
        # saptamī or pañcamī. Same fork on krośa.
        "label": "SK643-krose-krosat-karakamadhya",
        "sutras": ["2.3.7", "2.3.36"],
        "sentence": [
            {"stem": "kroSa", "vacana": 1,
             "sem": ["semantic_ADAra", "semantic_kArakamaDya"]},
            {"verb": "biBeti"},
        ],
        "expect": [
            {"karaka": "kAraka_aDikaraRa",
             "vibhakti": ["viBakti_5", "viBakti_7"],
             "forms": ["क्रोशात्", "क्रोशाद्", "क्रोशे"]},
            {"forms": ["बिभेति"]},
        ],
    },

    # ── SK644 (1.4.97) + SK645 (2.3.9): अधि-ईश्वरे karmapravacanīya → saptamī ──
    {
        # अधि भुवि रामः — "Rama [rules] over the earth" (sva-svāmi-bhāva). adhi in
        # the īśvara sense → karmapravacanīya carrying kp_saptamI; with dir=para
        # (governs the following noun) → 2.3.9 saptamī (भुवि / भुवाम्). 2.3.8 cannot
        # fire (no kp_dvitIyA). The lord (rāma) → prathamā (रामः).
        "label": "SK644-adhi-bhuvi-ramah",
        "sutras": ["1.4.97", "2.3.9"],
        "sentence": [
            {"word": "aDi_kp", "sem": ["semantic_ESvara"], "dir": "para"},
            {"stem": "BU", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
            {"stem": "rAma", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"forms": ["अधि"]},
            {"karaka": None, "vibhakti": ["viBakti_7"],
             "not_fired": ["2.3.8"], "forms": ["भुवि", "भुवाम्"]},
            {"karaka": None, "vibhakti": ["viBakti_1"], "forms": ["रामः"]},
        ],
    },
    {
        # उप परार्धे हरेर्गुणाः — "Hari's qualities are MORE than half the universe".
        # upa in the adhika sense → karmapravacanīya (1.4.87.1, kp_saptamI); with
        # dir=para → 2.3.9 saptamī (परार्धे).
        "label": "SK645-upa-pararhe-adhika",
        "sutras": ["1.4.87.1", "2.3.9"],
        "sentence": [
            {"word": "upa_kp", "sem": ["semantic_aDika"], "dir": "para"},
            {"stem": "parArDa", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"forms": ["उप"]},
            {"karaka": None, "vibhakti": ["viBakti_7"],
             "not_fired": ["2.3.8"], "forms": ["परार्धे"]},
        ],
    },

    # ── SK646 (1.4.98): विभाषा कृञि — adhi optionally kp before √kṛ (saṁjñā fork) ─
    {
        # यदत्र माम् अधिकरिष्यति — before √kṛ, adhi (īśvara sense) is OPTIONALLY a
        # karmapravacanīya, else a gati. Saṁjñā-level fork on the adhi particle:
        # the apply branch fires 1.4.98 (adhi → karmapravacanīya, kp_saptamI),
        # the skip branch leaves adhi a bare gati. No governed-noun vibhakti
        # here (surface deferred, §6) — the adhi avyaya surfaces as अधि either way.
        "label": "SK646-adhi-kr-vibhasha",
        "sutras": ["1.4.98"],
        "sentence": [
            {"word": "aDi_kp", "sem": ["semantic_ESvara"], "dir": "para"},
            {"verb": "aDikarizyati"},
        ],
        "expect": [
            {"forms": ["अधि"]},
            {"forms": ["अधिकरिष्यति"]},
        ],
    },

    # ── Negative: a plain karma noun (not ādhāra) → no adhikaraṇa/saptamī ─────
    {
        # हरिं भजति — hari is īpsitatama karma, NOT an ādhāra; 1.4.45 / 2.3.36
        # must not fire. Counter to SK633.
        "label": "SK633-negative-not-adhara",
        "sutras": ["1.4.49", "2.3.2"],
        "sentence": [
            {"stem": "hari", "vacana": 1, "sem": ["semantic_Ipsitatama"]},
            {"verb": "Bajati"},
        ],
        "expect": [
            {"karaka": "kAraka_karma", "vibhakti": ["viBakti_2"],
             "not_fired": ["1.4.45", "2.3.36"], "forms": ["हरिम्"]},
            {"forms": ["भजति"]},
        ],
    },
    {
        # अधि without the īśvara sense → adhi is NOT a karmapravacanīya here;
        # 1.4.97 / 2.3.9 must not fire. (The bare adhi is a plain gati/passthrough
        # avyaya; the noun falls through to prathamā.) Counter to SK644.
        "label": "SK644-negative-adhi-not-isvara",
        "sutras": ["2.3.46"],
        "sentence": [
            {"word": "aDi_kp"},
            {"stem": "rAma", "vacana": 1, "sem": ["semantic_prAtipadikArTa"]},
        ],
        "expect": [
            {"forms": ["अधि"]},
            {"karaka": None, "vibhakti": ["viBakti_1"],
             "not_fired": ["1.4.97", "2.3.9"], "forms": ["रामः"]},
        ],
    },
]
