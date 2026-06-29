# -*- coding: utf-8 -*-
"""Avyayībhāva-samāsa test cases (avyayībhāva samāsa plan).

Each case builds a two-member sentence [Adya, pūrva, uttara, avasAna] (members
adjacent — no avasAna between them, so they form one compound) and asserts three
levels (see test_samasa_avyayibhava.py):

  1. structure : after the samāsa pre-pass the pūrva carries samAsaPurva +
                 upasarjana and the uttara carries samAsa + avyayIBAva
                 (sups retained — combining/luk is the main scan's job)
  2. fired     : the listed pre-pass sutras appear in the pre-pass trace
  3. surface   : the full pipeline (pre-pass → main scan) emits the expected form

  pūrva : an avyaya from avyaya.py (?nipAta) carrying an avyayībhāva sense
  uttara: a stem from pratipadika.py (vacana 1)
"""

samasa_tests = [
    {
        # SK651/652 — समीप sense, a-stem uttara → 2.4.83 अम् → उपकृष्णम्
        "label": "S1A-upakRSNam-samIpa",
        "purva": {"avyaya": "upa_avyaya", "sem": "semantic_samIpa"},
        "uttara": {"stem": "kfzRa", "vacana": 1},
        "fired": ["2.1.6", "1.2.43"],
        "surface": "उपकृष्णम्",
    },
    {
        # SK652 — विभक्ति sense, i-stem uttara → 1.1.41 avyaya → 2.4.82 luk → अधिहरि
        "label": "S1A-adhihari-vibhakti",
        "purva": {"avyaya": "aDi_avyaya", "sem": "semantic_vibhakti"},
        "uttara": {"stem": "hari", "vacana": 1},
        "fired": ["2.1.6", "1.2.43"],
        "surface": "अधिहरि",
    },
]
