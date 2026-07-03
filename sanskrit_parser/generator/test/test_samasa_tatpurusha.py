# -*- coding: utf-8 -*-
"""Tatpuruṣa-samāsa test driver (tatpuruṣa samāsa plan, Phase T0).

Unlike the avyayībhāva (which becomes an indeclinable → invariant अम्), a
tatpuruṣa DECLINES NORMALLY in the uttara's gender (2.4.26 परवल्लिङ्गम्): the
uttara keeps its own sup and inflects; the pūrva (case-marked upasarjana) sup-luks
via 2.4.71. Three assertion levels per case (samasa_list.py :: samasa_tp_tests):

  1. structure : pre-pass member tags (samAsaPurva/upasarjana on the pūrva,
                 samAsa/tatpuruza on the uttara — NOT avyayIBAva)
  2. fired     : listed pre-pass sutras present in the pre-pass trace
  3. surface   : full-pipeline output equals the expected compound form
"""
from copy import deepcopy

import pytest
from indic_transliteration import sanscript

from sanskrit_parser.generator.prakriya import PrakriyaVakya
from sanskrit_parser.generator.antaranga_prakriya import AntarangaPrakriya
from sanskrit_parser.generator.pratyaya import Adya, avasAna
from sanskrit_parser.generator import pratipadika as _pratipadika
from sanskrit_parser.generator import avyaya as _avyaya

from conftest import sutra_list
from samasa_list import samasa_tp_tests


def _build_member(spec):
    """A member is either an avyaya (avyaya.py) or a stem (pratipadika.py),
    with an optional vibhakti/vacana, a semantic sense, and/or the
    ?samAsa_vivakza intent tag (mirrors the avyayībhāva driver)."""
    if "avyaya" in spec:
        p = deepcopy(getattr(_avyaya, spec["avyaya"]))
    else:
        p = deepcopy(getattr(_pratipadika, spec["stem"]))
        if spec.get("vacana"):
            p.setTag(f"vacana_{spec['vacana']}")
    if spec.get("sem"):
        p.setTag(spec["sem"])
    if spec.get("vivakza"):
        p.setTag("samAsa_vivakza")
    if spec.get("vibhakti"):    # the pūrva's vigraha vibhakti (e.g. dvitīyā = 2)
        p.setTag(f"viBakti_{spec['vibhakti']}")
        p.setTag("has_viBakti")
    for t in spec.get("tags", []):
        p.setTag(t)
    return p


def _to_slp1(deva):
    return sanscript.transliterate(deva, sanscript.DEVANAGARI, sanscript.SLP1)


@pytest.mark.parametrize("case", samasa_tp_tests, ids=[c["label"] for c in samasa_tp_tests])
def test_samasa_tatpurusha(case):
    purva = _build_member(case["purva"])
    uttara = _build_member(case["uttara"])
    # Members ADJACENT (no avasAna between) → one compound.
    pl = [Adya, purva, uttara, avasAna]
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya(pl))

    # ── Level 1: structure (pre-pass member tags, before the main-scan merge) ──
    branch = (getattr(p, "_karaka_branches", None) or [p.inputs])[0]
    members = [o for o in branch
               if o.canonical() and o.hasTag("prAtipadika") and not o.hasTag("sup")]
    assert len(members) == 2, f"{case['label']}: expected 2 members, got {members}"
    purva_o, uttara_o = members
    if case.get("no_samasa"):
        # Only-when-intended: WITHOUT ?samAsa_vivakza no tatpuruṣa forms.
        for o in members:
            for t in ("samAsa", "samAsaPurva", "tatpuruza", "upasarjana"):
                assert not o.hasTag(t), \
                    f"{case['label']}: {o} unexpectedly got ?{t} without vivakṣā"
        return
    for t in ("samAsaPurva", "upasarjana"):
        assert purva_o.hasTag(t), \
            f"{case['label']}: pūrva {purva_o} missing ?{t} ({sorted(purva_o.tags)})"
    for t in ("samAsa", "tatpuruza"):
        assert uttara_o.hasTag(t), \
            f"{case['label']}: uttara {uttara_o} missing ?{t} ({sorted(uttara_o.tags)})"
    # A tatpuruṣa is NOT an avyayībhāva (no avyaya/napum on the uttara).
    for t in ("avyayIBAva", "avyaya"):
        assert not uttara_o.hasTag(t), \
            f"{case['label']}: uttara {uttara_o} wrongly got ?{t} (tatpuruṣa declines)"

    # ── Level 2: fired-sutra trace (pre-pass rules) ──
    fired = {aps for e in p.karaka_log for aps in e["fired"]}
    for aps in case["fired"]:
        assert aps in fired, \
            f"{case['label']}: {aps} missing from pre-pass trace {sorted(fired)}"

    # ── Level 3: surface (full pipeline) ──
    p.execute()
    got = {"".join(x.canonical() for x in o).rstrip(avasAna.canonical())
           for o in p.output()}
    want = case["surfaces"] if "surfaces" in case else [case["surface"]]
    expected = {_to_slp1(s) for s in want}
    assert got == expected, f"{case['label']}: surface {got} != {expected}"


# ── Full vibhakti sweep for an a-stem tatpuruṣa (कृष्णश्रित) ───────────────────
# The tatpuruṣa declines NORMALLY (परवल्लिङ्गम्, the uttara's gender = masc a-stem),
# so कृष्णश्रित follows the plain राम paradigm — proving it is NOT an indeclinable
# (contrast the avyayībhāva's invariant अम्). Singular column only (no न-endings →
# no ṇatva across the र of श्रित).
_TATPURUSHA_VIBHAKTIS = {
    1: ["कृष्णश्रितः"],
    2: ["कृष्णश्रितम्"],
    3: ["कृष्णश्रितेन"],
    4: ["कृष्णश्रिताय"],
    5: ["कृष्णश्रितात्", "कृष्णश्रिताद्"],    # a-stem ablative (त्/द् pada-final variants)
    6: ["कृष्णश्रितस्य"],
    7: ["कृष्णश्रिते"],
}


@pytest.mark.parametrize("vib_n", sorted(_TATPURUSHA_VIBHAKTIS))
def test_tatpurusha_vibhakti_sweep(vib_n):
    """कृष्णं श्रितः (dvitīyā-tatpuruṣa) declined in each vibhakti (singular) —
    proves the compound inflects as a normal a-stem masc (परवल्लिङ्गम्), unlike
    the avyayībhāva's invariant अम्."""
    purva = deepcopy(getattr(_pratipadika, "kfzRa"))
    purva.setTag("vacana_1")
    purva.setTag("viBakti_2")       # vigraha dvitīyā (luks via 2.4.71)
    purva.setTag("has_viBakti")
    purva.setTag("samAsa_vivakza")
    uttara = deepcopy(getattr(_pratipadika, "Srita"))
    uttara.setTag("vacana_1")
    uttara.setTag(f"viBakti_{vib_n}")   # external compound case
    uttara.setTag("has_viBakti")
    uttara.setTag("samAsa_vivakza")
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya([Adya, purva, uttara, avasAna]))
    p.execute()
    got = {"".join(x.canonical() for x in o).rstrip(avasAna.canonical())
           for o in p.output()}
    expected = {_to_slp1(s) for s in _TATPURUSHA_VIBHAKTIS[vib_n]}
    assert got == expected, \
        f"tatpuruṣa viBakti_{vib_n}: {got} != {expected}"
