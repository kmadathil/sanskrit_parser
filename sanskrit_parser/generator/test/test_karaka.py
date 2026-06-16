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

from sanskrit_parser.generator.paninian_object import PaninianObject, _is_karaka_tag
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
        # Particles (avyaya). A karmapravacanīya particle carries its per-usage
        # sense tag at input (e.g. semantic_lakzaRa on anu) plus a governance-
        # DIRECTION tag — kp_pUrva (governs the preceding noun) or kp_para
        # (governs the following noun) — which is a user choice, NOT derived from
        # the sense. spec["dir"] is "pUrva"/"para" (default "pUrva" when a sense
        # is present, mirroring cmd_line/UI). Plain particles (he, antarA) carry
        # neither and pass through bare.
        p = deepcopy(getattr(_avyaya, spec["word"]))
        sems = spec.get("sem", [])
        for t in sems:
            p.setTag(t)
        # Direction is meaningful only for a karmapravacanīya usage (sense present);
        # plain particles ignore it. The user's choice defaults to "pUrva".
        if sems:
            direction = spec.get("dir") or "pUrva"
            p.setTag("kp_pUrva" if direction == "pUrva" else "kp_para")
        return p
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

    # A vibhāṣā (optional) kāraka rule forks the pre-pass into alternative
    # sentences, so karaka_log holds one entry per (index, branch). Aggregate
    # by index — the union of tags/fired across branches — so saṁjñā/vibhakti
    # expectations can be the SET seen across branches (e.g. 2.3.22 पित्रा /
    # पितरम् → {viBakti_3, viBakti_2}). Single-branch cases (K0–K2) aggregate
    # to a single entry, unchanged.
    agg = {}
    for e in p.karaka_log:
        a = agg.setdefault(e["index"], {"tags": set(), "fired": set()})
        a["tags"].update(e["tags"])
        a["fired"].update(e["fired"])
    fired_all = {aps for a in agg.values() for aps in a["fired"]}

    # Fired-sutra trace
    for aps in case["sutras"]:
        assert aps in fired_all, \
            f"{case['label']}: {aps} missing from fired trace {sorted(fired_all)}"

    # Levels 1–2 per word, plus per-word negative trace
    for spec, exp, ix in zip(case["sentence"], case["expect"], word_ix):
        entry = agg.get(ix)
        tags = entry["tags"] if entry else set()
        fired = entry["fired"] if entry else set()
        if "karaka" in exp:
            karakas = {t for t in tags if t.startswith("kAraka_")}
            k = exp["karaka"]
            expected = set() if k is None else ({k} if isinstance(k, str) else set(k))
            assert karakas == expected, \
                f"{case['label']} word {spec}: kāraka {karakas} != {expected}"
        if "vibhakti" in exp:
            vibhaktis = {t for t in tags
                         if t.startswith("viBakti_") and t[8:].isdigit()}
            assert vibhaktis == set(exp["vibhakti"]), \
                f"{case['label']} word {spec}: vibhakti {vibhaktis} != {exp['vibhakti']}"
        for aps in exp.get("not_fired", []):
            assert aps not in fired, \
                f"{case['label']} word {spec}: {aps} must not fire (fired {sorted(fired)})"

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

    # Issue-2 guard: kāraka-section tags are pre-pass scaffolding and must not
    # leak onto a realized pada / merged sentence. Every output pada must be
    # free of them. (A bare stem that never took a sup — e.g. the skip-guard
    # case — is not a pada and legitimately keeps its input vacana_N tag.)
    for branch in p.output():
        for obj in branch:
            if obj.hasTag("pada"):
                leaked = [t for t in obj.tags if _is_karaka_tag(t)]
                assert not leaked, \
                    f"{case['label']}: kāraka tags leaked onto pada {obj}: {leaked}"
