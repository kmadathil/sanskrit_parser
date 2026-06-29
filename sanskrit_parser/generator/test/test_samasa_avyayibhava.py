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


def _build_purva(spec):
    p = deepcopy(getattr(_avyaya, spec["avyaya"]))
    p.setTag(spec["sem"])
    return p


def _build_uttara(spec):
    p = deepcopy(getattr(_pratipadika, spec["stem"]))
    p.setTag(f"vacana_{spec['vacana']}")
    return p


def _to_slp1(deva):
    return sanscript.transliterate(deva, sanscript.DEVANAGARI, sanscript.SLP1)


@pytest.mark.parametrize("case", samasa_tests, ids=[c["label"] for c in samasa_tests])
def test_samasa_avyayibhava(case):
    purva = _build_purva(case["purva"])
    uttara = _build_uttara(case["uttara"])
    # Members ADJACENT (no avasAna between) → one compound.
    pl = [Adya, purva, uttara, avasAna]
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya(pl))

    # ── Level 1: structure (pre-pass member tags, before the main-scan merge) ──
    branch = (getattr(p, "_karaka_branches", None) or [p.inputs])[0]
    members = [o for o in branch
               if o.canonical() and o.hasTag("prAtipadika") and not o.hasTag("sup")]
    assert len(members) == 2, f"{case['label']}: expected 2 members, got {members}"
    purva_o, uttara_o = members
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
    expected = {_to_slp1(case["surface"])}
    assert got == expected, f"{case['label']}: surface {got} != {expected}"
