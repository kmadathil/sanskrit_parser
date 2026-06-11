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
]
