# -*- coding: utf-8 -*-
"""Ekaśeṣa test driver (samasa_completion_plan.md, Phases E0/E1).

Ekaśeṣa (SK188/1.2.64 सरूपाणामेकशेष एकविभक्तौ): several sarūpa (same-form) padas in ONE
vibhakti collapse to a SINGLE surviving pada, which takes the SUMMED vacana — राम + राम →
रामौ (dual), three → रामाः (plural). It is NOT a compound: one pada survives and declines
alone. The pre-pass tags the elided members ?ekaSeza_lupta and the survivor
?ekaSeza_Sizyate; `_commit_ekasesa` physically deletes the elided members (the M3 step);
the survivor's vacana climbs via the widened 1.4.22/1.4.21.

The E1 vidhis (1.2.65–73) extend this to heterogeneous pairs where a specific member
survives (masc over fem, kinship, pronoun) — modelled with the survivor as the LAST
member (rp), so the same rp-survives machinery applies.

Assertion levels per case (samasa_list.py :: ekasesa_tests):
  1. structure : exactly ONE member remains in the branch after elision
  2. fired     : listed pre-pass sutras present in the trace
  3. surface   : full-pipeline output equals the expected form
"""
from copy import deepcopy

import pytest
from indic_transliteration import sanscript

from sanskrit_parser.generator.prakriya import PrakriyaVakya
from sanskrit_parser.generator.antaranga_prakriya import AntarangaPrakriya
from sanskrit_parser.generator.pratyaya import Adya, avasAna
from sanskrit_parser.generator import pratipadika as _pratipadika

from conftest import sutra_list
from samasa_list import ekasesa_tests


def _build_member(spec):
    """An ekaśeṣa member: a stem in the given vibhakti/vacana, with the ekaśeṣa intent."""
    p = deepcopy(getattr(_pratipadika, spec["stem"]))
    p.setTag(f"vacana_{spec.get('vacana', 1)}")
    p.setTag(f"viBakti_{spec.get('vibhakti', 1)}")
    p.setTag("has_viBakti")
    p.setTag("samAsa_vivakza")
    p.setTag("ekaSeza_vivakza")
    for t in spec.get("tags", []):
        p.setTag(t)
    return p


def _to_slp1(deva):
    return sanscript.transliterate(deva, sanscript.DEVANAGARI, sanscript.SLP1)


def _surface(pl):
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya(pl))
    p.execute()
    return {"".join(x.canonical() for x in o).rstrip(avasAna.canonical())
            for o in p.output()}


@pytest.mark.parametrize("case", ekasesa_tests, ids=[c["label"] for c in ekasesa_tests])
def test_ekasesa(case):
    members = [_build_member(m) for m in case["members"]]
    pl = [Adya, *members, avasAna]
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya(pl))

    # ── Level 1: structure — exactly ONE member survives the elision ──
    branch = (getattr(p, "_karaka_branches", None) or [p.inputs])[0]
    flat = []
    for o in branch:
        flat.extend(o if isinstance(o, list) else [o])
    survivors = [o for o in flat
                 if o.canonical() and o.hasTag("prAtipadika") and not o.hasTag("sup")]
    assert len(survivors) == 1, \
        f"{case['label']}: expected 1 survivor, got {[s.canonical() for s in survivors]}"

    # ── Level 2: fired-sutra trace ──
    fired = {aps for e in p.karaka_log for aps in e["fired"]}
    for aps in case["fired"]:
        assert aps in fired, \
            f"{case['label']}: {aps} missing from pre-pass trace {sorted(fired)}"
    for aps in case.get("not_fired", []):
        assert aps not in fired, \
            f"{case['label']}: {aps} unexpectedly fired (trace {sorted(fired)})"

    # ── Level 3: surface ──
    p.execute()
    got = {"".join(x.canonical() for x in o).rstrip(avasAna.canonical())
           for o in p.output()}
    want = case["surfaces"] if "surfaces" in case else [case["surface"]]
    assert got == {_to_slp1(s) for s in want}, \
        f"{case['label']}: surface {got} != {want}"


# ── Vacana sweep: the survivor's number is DERIVED from the count of elided members ──
_VACANA_SWEEP = [
    (2, ["रामौ"]),
    (3, ["रामाः"]),
    (4, ["रामाः"]),
]


@pytest.mark.parametrize("n,want", _VACANA_SWEEP, ids=[f"rama-x{n}" for n, _ in _VACANA_SWEEP])
def test_ekasesa_vacana_sweep(n, want):
    members = [_build_member({"stem": "rAma"}) for _ in range(n)]
    got = _surface([Adya, *members, avasAna])
    assert got == {_to_slp1(s) for s in want}, \
        f"ekaśeṣa राम×{n}: {got} != {want}"


# ── Vibhakti sweep: the dual survivor declines normally in the supplied vibhakti ──
_VIBHAKTI_SWEEP = {
    1: ["रामौ"],
    3: ["रामाभ्याम्"],
    6: ["रामयोः"],
}


@pytest.mark.parametrize("vib_n", sorted(_VIBHAKTI_SWEEP))
def test_ekasesa_vibhakti_sweep(vib_n):
    members = [_build_member({"stem": "rAma", "vibhakti": vib_n}) for _ in range(2)]
    got = _surface([Adya, *members, avasAna])
    expected = {_to_slp1(s) for s in _VIBHAKTI_SWEEP[vib_n]}
    assert got == expected, f"ekaśeṣa viBakti_{vib_n}: {got} != {expected}"


# ── DE-UI: the CLI --ekasesa path (cmd_line.prepare_ekasesa) ───────────────────────
def test_cli_ekasesa():
    from sanskrit_parser.generator.cmd_line import get_args, prepare_ekasesa
    args = get_args(["-k", "rAma", "1", "-k", "rAma", "1", "--samasa", "--ekasesa"])
    for w in args.karaka_words:      # the --samasa loop
        w.setTag("samAsa_vivakza")
    words = prepare_ekasesa(args.karaka_words)
    got = _surface([Adya, *words, avasAna])
    assert got == {_to_slp1("रामौ")}, f"CLI --ekasesa: {got}"
