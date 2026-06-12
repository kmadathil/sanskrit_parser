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
               {"word": <avyaya-module name>}                  (particle, passthrough)
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
            {"word": "antareRa"},
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
            {"word": "antarA"},
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
            {"word": "antareRa"},
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
]
