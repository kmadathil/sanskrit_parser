# -*- coding: utf-8 -*-
"""
Kāraka layer test driver (karaka_plan.md §3) — three assertion levels:
  1. saṁjñā   : the noun carries exactly the expected kAraka_* tag after the
                pre-pass (tests pass-1 + ekā-saṁjñā + the param carve-out)
  2. vibhakti : exactly the expected viBakti_N tag set
  3. surface  : the derived sentence equals the cross-product of per-word
                forms (words avasAna-separated, so no inter-word sandhi)
plus the fired-sutra trace check that makes negative cases meaningful.
"""
from copy import deepcopy
from itertools import product

import pytest
from indic_transliteration import sanscript

from sanskrit_parser.generator.paninian_object import PaninianObject
from sanskrit_parser.generator.prakriya import PrakriyaVakya
from sanskrit_parser.generator.antaranga_prakriya import AntarangaPrakriya
from sanskrit_parser.generator.pratyaya import Adya, avasAna
from sanskrit_parser.generator import pratipadika as _pratipadika
from sanskrit_parser.generator import dhatu as _dhatu
from sanskrit_parser.generator import avyaya as _avyaya

from conftest import sutra_list
from karaka_list import karaka_tests


def _build_word(spec):
    if "stem" in spec:
        p = deepcopy(getattr(_pratipadika, spec["stem"]))
        p.setTag(f"vacana_{spec['vacana']}")
        for t in spec.get("sem", []):
            p.setTag(t)
        return p
    if "verb" in spec:
        return deepcopy(getattr(_dhatu, spec["verb"]))
    if "word" in spec:
        return deepcopy(getattr(_avyaya, spec["word"]))
    raise ValueError(f"Unknown word spec {spec}")


@pytest.mark.parametrize("case", karaka_tests,
                         ids=[c["label"] for c in karaka_tests])
def test_karaka(case):
    pl = [Adya]
    word_ix = []
    for spec in case["sentence"]:
        word_ix.append(len(pl))
        pl.append(_build_word(spec))
        pl.append(avasAna)
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya(pl))
    p.execute()

    log_by_ix = {e["index"]: e for e in p.karaka_log}
    fired_all = [aps for e in p.karaka_log for aps in e["fired"]]

    # Fired-sutra trace
    for aps in case["sutras"]:
        assert aps in fired_all, \
            f"{case['label']}: {aps} missing from fired trace {fired_all}"

    # Levels 1–2 per word, plus per-word negative trace
    for spec, exp, ix in zip(case["sentence"], case["expect"], word_ix):
        entry = log_by_ix.get(ix)
        tags = set(entry["tags"]) if entry else set()
        if "karaka" in exp:
            karakas = {t for t in tags if t.startswith("kAraka_")}
            expected = set() if exp["karaka"] is None else {exp["karaka"]}
            assert karakas == expected, \
                f"{case['label']} word {spec}: kāraka {karakas} != {expected}"
        if "vibhakti" in exp:
            vibhaktis = {t for t in tags
                         if t.startswith("viBakti_") and t[8:].isdigit()}
            assert vibhaktis == set(exp["vibhakti"]), \
                f"{case['label']} word {spec}: vibhakti {vibhaktis} != {exp['vibhakti']}"
        for aps in exp.get("not_fired", []):
            assert entry is None or aps not in entry["fired"], \
                f"{case['label']} word {spec}: {aps} must not fire (fired {entry['fired']})"

    # Level 3: surface — joined sentence set vs cross-product of word forms
    sep = avasAna.canonical()
    expected_sentences = set()
    for combo in product(*(exp["forms"] for exp in case["expect"])):
        slp = "".join(
            sanscript.transliterate(w.replace(" ", ""),
                                    sanscript.DEVANAGARI, sanscript.SLP1) + sep
            for w in combo)
        expected_sentences.add(slp)
    got = {
        PaninianObject("".join(x.transcoded(sanscript.SLP1) for x in o),
                       encoding=sanscript.SLP1).canonical()
        for o in p.output()
    }
    if got != expected_sentences:
        print(f"Got {got} expected {expected_sentences}")
    assert got == expected_sentences
