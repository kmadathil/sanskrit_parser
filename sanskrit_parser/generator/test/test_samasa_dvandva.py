# -*- coding: utf-8 -*-
"""Dvandva-samāsa test driver (samasa_completion_plan.md, Phase D0).

A dvandva coordinates two-or-more prathamānta padas in the "and" sense (SK901/2.2.29
चार्थे द्वन्द्वः). Its distinguishing feature is a DERIVED vacana: the itaretara dvandva
denotes all its members together, so its number is their SUM — धव + खदिर → dvivacana
धवखदिरौ; a three-member chain → bahuvacana धवखदिरपलाशाः. It declines paravalliṅga
(SK812/2.4.26, widened for द्वन्द्व) in the LAST member's gender. Both members are
upasarjana (1.2.43); the pūrva sup luks (2.4.71), the uttara sup carries the derived
vacana (via the ?swap_viBakti + _swap_sups lever).

Three assertion levels per case (samasa_list.py :: samasa_dv_tests):
  1. structure : member tags (samAsaPurva/upasarjana on the pūrva-most, samAsa/dvandva
                 on the uttara)
  2. fired     : listed pre-pass sutras present in the pre-pass trace
  3. surface   : full-pipeline output equals the expected compound form
Plus a vacana sweep (2 members → dual, 3 → plural) proving the number is derived, and a
vibhakti sweep proving the compound declines normally in the uttara gender.
"""
from copy import deepcopy

import pytest
from indic_transliteration import sanscript

from sanskrit_parser.generator.prakriya import PrakriyaVakya
from sanskrit_parser.generator.antaranga_prakriya import AntarangaPrakriya
from sanskrit_parser.generator.pratyaya import Adya, avasAna
from sanskrit_parser.generator import pratipadika as _pratipadika

from conftest import sutra_list
from samasa_list import samasa_dv_tests


def _build_member(spec):
    """A dvandva member: a stem (pratipadika.py) in the prathamā (vigraha), with the
    dvandva intent tags. Each member defaults to viBakti_1 / vacana_1 unless overridden
    (the uttara's viBakti carries the compound's external case for the vibhakti sweep)."""
    p = deepcopy(getattr(_pratipadika, spec["stem"]))
    p.setTag(f"vacana_{spec.get('vacana', 1)}")
    p.setTag(f"viBakti_{spec.get('vibhakti', 1)}")
    p.setTag("has_viBakti")
    p.setTag("samAsa_vivakza")        # candidate detection (_samasa_prepass_branch)
    p.setTag("dvandva_vivakza")       # dvandva intent (SK901/2.2.29 condition)
    if spec.get("samahara"):          # composer-declared समाहार (2.4.17 → वाक्त्वचम्)
        p.setTag("samAhAra")
    for t in spec.get("tags", []):    # samāhāra CLASS tag (prāṇyaṅga / vṛkṣādi / …)
        p.setTag(t)
    return p


def _to_slp1(deva):
    return sanscript.transliterate(deva, sanscript.DEVANAGARI, sanscript.SLP1)


def _surface(pl):
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya(pl))
    p.execute()
    return {"".join(x.canonical() for x in o).rstrip(avasAna.canonical())
            for o in p.output()}


@pytest.mark.parametrize("case", samasa_dv_tests, ids=[c["label"] for c in samasa_dv_tests])
def test_samasa_dvandva(case):
    members = [_build_member(m) for m in case["members"]]
    pl = [Adya, *members, avasAna]
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya(pl))

    # ── Level 1: structure (pre-pass member tags; flatten the nested sub-list) ──
    branch = (getattr(p, "_karaka_branches", None) or [p.inputs])[0]
    flat = []
    for o in branch:
        flat.extend(o if isinstance(o, list) else [o])
    mem = [o for o in flat
           if o.canonical() and o.hasTag("prAtipadika") and not o.hasTag("sup")]
    assert len(mem) == len(case["members"]), \
        f"{case['label']}: expected {len(case['members'])} members, got {mem}"
    # The pūrva-most is samAsaPurva + upasarjana; the last is samAsa + dvandva.
    for t in ("samAsaPurva", "upasarjana"):
        assert mem[0].hasTag(t), \
            f"{case['label']}: pūrva {mem[0]} missing ?{t} ({sorted(mem[0].tags)})"
    for t in ("samAsa", "dvandva"):
        assert mem[-1].hasTag(t), \
            f"{case['label']}: uttara {mem[-1]} missing ?{t} ({sorted(mem[-1].tags)})"

    # ── Level 2: fired-sutra trace (pre-pass rules) ──
    fired = {aps for e in p.karaka_log for aps in e["fired"]}
    for aps in case["fired"]:
        assert aps in fired, \
            f"{case['label']}: {aps} missing from pre-pass trace {sorted(fired)}"
    for aps in case.get("not_fired", []):
        assert aps not in fired, \
            f"{case['label']}: {aps} unexpectedly fired (trace {sorted(fired)})"

    # ── Level 3: surface (full pipeline) ──
    p.execute()
    got = {"".join(x.canonical() for x in o).rstrip(avasAna.canonical())
           for o in p.output()}
    want = case["surfaces"] if "surfaces" in case else [case["surface"]]
    assert got == {_to_slp1(s) for s in want}, \
        f"{case['label']}: surface {got} != {want}"


# ── Vacana sweep: the number is DERIVED (the sum of the members) ───────────────────
# The hallmark of the itaretara dvandva: 2 members → dual, 3 → plural, purely from the
# member count — no composer-supplied vacana. This is what makes dvandva unlike every
# earlier samāsa (whose vacana was supplied directly).
_VACANA_SWEEP = [
    (("Dava", "Kadira"),           ["धवखदिरौ"]),
    (("Dava", "Kadira", "palASa"), ["धवखदिरपलाशाः"]),
]


@pytest.mark.parametrize("stems,want", _VACANA_SWEEP,
                         ids=[f"{'-'.join(s)}" for s, _ in _VACANA_SWEEP])
def test_dvandva_vacana_sweep(stems, want):
    members = [_build_member({"stem": s}) for s in stems]
    got = _surface([Adya, *members, avasAna])
    assert got == {_to_slp1(s) for s in want}, \
        f"dvandva vacana ({len(stems)} members): {got} != {want}"


# ── Vibhakti sweep: the dual dvandva declines as a normal masc a-stem in the dual ──
# The uttara carries the compound's external case; धवखदिर + <dual sup> declines like any
# a-stem dual. (The dvandva vacana is dual regardless — the vibhakti varies.)
_VIBHAKTI_SWEEP = {
    1: ["धवखदिरौ"],
    2: ["धवखदिरौ"],
    3: ["धवखदिराभ्याम्"],
    4: ["धवखदिराभ्याम्"],
    5: ["धवखदिराभ्याम्"],
    6: ["धवखदिरयोः"],
    7: ["धवखदिरयोः"],
}


@pytest.mark.parametrize("vib_n", sorted(_VIBHAKTI_SWEEP))
def test_dvandva_vibhakti_sweep(vib_n):
    m1 = _build_member({"stem": "Dava"})
    m2 = _build_member({"stem": "Kadira", "vibhakti": vib_n})
    got = _surface([Adya, m1, m2, avasAna])
    expected = {_to_slp1(s) for s in _VIBHAKTI_SWEEP[vib_n]}
    assert got == expected, f"dvandva viBakti_{vib_n}: {got} != {expected}"


# ── DE-UI: the CLI --dvandva / --samahara path (cmd_line.prepare_dvandva) ──────────
_CLI_CASES = [
    (["-k", "Dava", "1", "-k", "Kadira", "1", "--samasa", "--dvandva"], False, ["धवखदिरौ"]),
    (["-k", "pARi", "1", "-k", "pAda", "1", "--samasa", "--dvandva", "--samahara"],
     True, ["पाणिपादम्"]),
]


@pytest.mark.parametrize("argv,samahara,want", _CLI_CASES,
                         ids=["dvandva-DavaKadira", "samahara-pARipAda"])
def test_cli_dvandva(argv, samahara, want):
    from sanskrit_parser.generator.cmd_line import get_args, prepare_dvandva
    args = get_args(argv)
    for w in args.karaka_words:      # the --samasa loop
        w.setTag("samAsa_vivakza")
    words = prepare_dvandva(args.karaka_words, samahara)
    got = _surface([Adya, *words, avasAna])
    assert got == {_to_slp1(s) for s in want}, f"CLI {argv}: {got} != {want}"
