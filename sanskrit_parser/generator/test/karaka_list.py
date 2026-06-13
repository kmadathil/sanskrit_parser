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

    # ════════════════════════════════════════════════════════════════════════
    # Phase K2 — karmapravacanīya + dvitīyā (SK546–558; karaka_plan.md §K2).
    # The particle is an avyaya carrying its per-usage sense tag; Pass A assigns
    # karmapravacanIya + a governance-direction tag (kp_pUrva = governs the noun
    # to its left; kp_para = to its right); 2.3.8 reads it via rrp/llp. Particles
    # take their own su → 2.4.82 luk → bare avyaya form.
    # ════════════════════════════════════════════════════════════════════════

    # ── SK547 (1.4.84) + SK548 (2.3.8): anu lakṣaṇa, noun precedes ───────────
    {
        # जपमनु प्रावर्षत् (reduced: जपम् अनु) — "rained along the japa".
        "label": "SK548-japam-anu",
        "sutras": ["1.4.84", "2.3.8"],
        "sentence": [
            {"stem": "japa", "vacana": 1, "sem": []},
            {"word": "anu_kp", "sem": ["semantic_lakzaRa"]},
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
            {"word": "anu_kp", "sem": ["semantic_tftIyArTa"]},
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
            {"word": "anu_kp", "sem": ["semantic_hIna"]},
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
            {"word": "upa_kp", "sem": ["semantic_hIna"]},
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
            {"word": "prati_kp", "sem": ["semantic_lakzaRa"]},
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
            {"word": "prati_kp", "sem": ["semantic_itTamBUta"]},
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
            {"word": "aBi_kp", "sem": ["semantic_lakzaRa"]},
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
            {"word": "ati_kp", "sem": ["semantic_atikramaRa"]},
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
        # कृष्णम् अनु रामः — anu in lakṣaṇa (kp_pUrva) governs the PRECEDING noun
        # (kṛṣṇa → dvitīyā); rāma follows anu, so 2.3.8 (kp_para arm) does not fire
        # on it → prathamā. Confirms only the intended noun is tagged.
        "label": "SK548-krsnam-anu-ramah-direction",
        "sutras": ["1.4.84", "2.3.8", "2.3.46"],
        "sentence": [
            {"stem": "kfzRa", "vacana": 1, "sem": []},
            {"word": "anu_kp", "sem": ["semantic_lakzaRa"]},
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
            {"word": "saha"},
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
            {"word": "saha"},
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
            {"word": "sAkam"},
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
]
