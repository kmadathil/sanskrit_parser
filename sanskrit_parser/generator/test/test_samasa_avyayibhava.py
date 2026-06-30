# -*- coding: utf-8 -*-
"""Avyayībhāva-samāsa test driver (avyayībhāva samāsa plan, S1A).

Three assertion levels per case (samasa_list.py):
  1. structure : pre-pass member tags (samAsaPurva/upasarjana on the pūrva,
                 samAsa/avyayIBAva on the uttara) — sups retained, NOT merged
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
from samasa_list import samasa_tests


def _build_member(spec):
    """A member is either an avyaya (avyaya.py) or a stem (pratipadika.py),
    with an optional semantic sense and/or ?samAsa_vivakza intent tag."""
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
    if spec.get("vibhakti"):   # a pre-supplied external vibhakti (e.g. 2.4.84 saptamī)
        p.setTag(f"viBakti_{spec['vibhakti']}")
        p.setTag("has_viBakti")
    for t in spec.get("tags", []):
        p.setTag(t)
    return p


def _to_slp1(deva):
    return sanscript.transliterate(deva, sanscript.DEVANAGARI, sanscript.SLP1)


@pytest.mark.parametrize("case", samasa_tests, ids=[c["label"] for c in samasa_tests])
def test_samasa_avyayibhava(case):
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
        # Vibhāṣā without ?samAsa_vivakza: NO compound forms (the words stay
        # separate — a different input, not a branch). Neither member is tagged.
        for o in members:
            for t in ("samAsa", "samAsaPurva", "avyayIBAva", "upasarjana"):
                assert not o.hasTag(t), \
                    f"{case['label']}: {o} unexpectedly got ?{t} without vivakṣā"
        return
    for t in ("samAsaPurva", "upasarjana"):
        assert purva_o.hasTag(t), \
            f"{case['label']}: pūrva {purva_o} missing ?{t} ({sorted(purva_o.tags)})"
    for t in ("samAsa", "avyayIBAva"):
        assert uttara_o.hasTag(t), \
            f"{case['label']}: uttara {uttara_o} missing ?{t} ({sorted(uttara_o.tags)})"

    # ── Level 2: fired-sutra trace (pre-pass rules) ──
    fired = {aps for e in p.karaka_log for aps in e["fired"]}
    for aps in case["fired"]:
        assert aps in fired, \
            f"{case['label']}: {aps} missing from pre-pass trace {sorted(fired)}"

    # ── Level 3: surface (full pipeline) ──
    p.execute()
    got = {"".join(x.canonical() for x in o).rstrip(avasAna.canonical())
           for o in p.output()}
    # "surfaces" (a set) for a bahula/optional fork (2.4.84); else single "surface".
    want = case["surfaces"] if "surfaces" in case else [case["surface"]]
    expected = {_to_slp1(s) for s in want}
    assert got == expected, f"{case['label']}: surface {got} != {expected}"


# ── Full vibhakti sweep for an a-stem avyayībhāva (उपकृष्ण) ───────────────────
# The avyayībhāva is avyaya, so it declines invariantly as उपकृष्णम् (अम्, 2.4.83)
# — EXCEPT the ablative उपकृष्णात् (apañcamyāḥ, 2.4.83.1; both pada-final त्/द्
# surface variants) and the OPTIONAL tṛtīyā/saptamī forms उपकृष्णेन/उपकृष्णे
# (2.4.84 bahula, which fork alongside the अम् form).
_AVYAYIBHAVA_VIBHAKTIS = {
    1: ["उपकृष्णम्"],
    2: ["उपकृष्णम्"],
    3: ["उपकृष्णम्", "उपकृष्णेन"],            # 2.4.84 bahula
    4: ["उपकृष्णम्"],
    5: ["उपकृष्णात्", "उपकृष्णाद्"],          # 2.4.83.1 apañcamyāḥ (त्/द् variants)
    6: ["उपकृष्णम्"],
    7: ["उपकृष्णम्", "उपकृष्णे"],            # 2.4.84 bahula
}


@pytest.mark.parametrize("vib_n", sorted(_AVYAYIBHAVA_VIBHAKTIS))
def test_avyayibhava_vibhakti_sweep(vib_n):
    """उप + कृष्ण (samīpa, a-stem) declined in each vibhakti — exercises 2.4.83
    (अम्), 2.4.83.1 (apañcamyāḥ → ablative), and 2.4.84 (bahula tṛtīyā/saptamī)."""
    purva = deepcopy(getattr(_avyaya, "upa_avyaya"))
    purva.setTag("semantic_samIpa")
    uttara = deepcopy(getattr(_pratipadika, "kfzRa"))
    uttara.setTag("vacana_1")
    uttara.setTag(f"viBakti_{vib_n}")
    uttara.setTag("has_viBakti")
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya([Adya, purva, uttara, avasAna]))
    p.execute()
    got = {"".join(x.canonical() for x in o).rstrip(avasAna.canonical())
           for o in p.output()}
    expected = {_to_slp1(s) for s in _AVYAYIBHAVA_VIBHAKTIS[vib_n]}
    assert got == expected, \
        f"avyayībhāva viBakti_{vib_n}: {got} != {expected}"
    # The pañcamī must NOT collapse to the अम् form (the apañcamyāḥ point).
    if vib_n == 5:
        assert _to_slp1("उपकृष्णम्") not in got, "pañcamī wrongly got अम्"
