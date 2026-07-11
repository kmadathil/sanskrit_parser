# -*- coding: utf-8 -*-
"""Bahuvrīhi-samāsa test driver (bahuvrihi_plan.md, Phase B0).

A bahuvrīhi is EXOCENTRIC: it denotes ANOTHER thing (anyapadārtha, SK830/2.2.24)
not connoted by its members, so it declines in that EXTERNAL referent's gender —
NOT the uttara's (contrast tatpuruṣa SK812/2.4.26 परवल्लिङ्गम्). पीत+अम्बर (n.) →
पीताम्बरः (m.) / पीताम्बरा (f.) / पीताम्बरम् (n.) depending on the referent. Both members
are prathamānta (?viBakti_1) upasarjanas; the pūrva sup luks (2.4.71), the uttara
sup (the referent case) is retained and inflects.

Three assertion levels per case (samasa_list.py :: samasa_bv_tests):
  1. structure : pre-pass member tags (samAsaPurva/upasarjana on the pūrva,
                 samAsa/bahuvrIhi on the uttara)
  2. fired     : listed pre-pass sutras present in the pre-pass trace
  3. surface   : full-pipeline output equals the expected compound form
Plus a gender sweep (proves exocentricity) and a vibhakti sweep (proves the
compound declines normally in the referent gender).
"""
from copy import deepcopy

import pytest
from indic_transliteration import sanscript

from sanskrit_parser.generator.prakriya import PrakriyaVakya
from sanskrit_parser.generator.antaranga_prakriya import AntarangaPrakriya
from sanskrit_parser.generator.pratyaya import Adya, avasAna, strI_abs
from sanskrit_parser.generator import pratipadika as _pratipadika

from conftest import sutra_list
from samasa_list import samasa_bv_tests


_LINGAS = ("pum", "strI", "napum")


def _build_member(spec, *, referent_linga=None):
    """A bahuvrīhi member: a stem (pratipadika.py) in the prathamā (vigraha), with
    the bahuvrīhi intent tags. On the uttara, referent_linga overrides the native
    gender to the referent's liṅga (anyapadārtha) and records ?referent_<linga>."""
    p = deepcopy(getattr(_pratipadika, spec["stem"]))
    if spec.get("vacana"):
        p.setTag(f"vacana_{spec['vacana']}")
    if spec.get("vibhakti"):
        p.setTag(f"viBakti_{spec['vibhakti']}")
        p.setTag("has_viBakti")
    p.setTag("samAsa_vivakza")        # candidate detection (_samasa_prepass_branch)
    p.setTag("bahuvrIhi_vivakza")     # bahuvrīhi intent (SK830/2.2.24 condition)
    if referent_linga is not None:
        for t in _LINGAS:             # override native gender → referent liṅga
            if p.hasTag(t):
                p.deleteTag(t)
        p.setTag(referent_linga)
        p.setTag(f"referent_{referent_linga}")
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


@pytest.mark.parametrize("case", samasa_bv_tests, ids=[c["label"] for c in samasa_bv_tests])
def test_samasa_bahuvrihi(case):
    purva = _build_member(case["purva"])
    uttara = _build_member(case["uttara"], referent_linga=case.get("referent_linga"))
    pl = [Adya, purva, uttara, avasAna]
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya(pl))

    # ── Level 1: structure (pre-pass member tags; flatten the nested sub-list) ──
    branch = (getattr(p, "_karaka_branches", None) or [p.inputs])[0]
    flat = []
    for o in branch:
        flat.extend(o if isinstance(o, list) else [o])
    members = [o for o in flat
               if o.canonical() and o.hasTag("prAtipadika") and not o.hasTag("sup")]
    assert len(members) == 2, f"{case['label']}: expected 2 members, got {members}"
    purva_o, uttara_o = members
    for t in ("samAsaPurva", "upasarjana"):
        assert purva_o.hasTag(t), \
            f"{case['label']}: pūrva {purva_o} missing ?{t} ({sorted(purva_o.tags)})"
    for t in ("samAsa", "bahuvrIhi"):
        assert uttara_o.hasTag(t), \
            f"{case['label']}: uttara {uttara_o} missing ?{t} ({sorted(uttara_o.tags)})"
    # Exocentric: the uttara carries the referent gender, locked (not its native one).
    if case.get("referent_linga"):
        assert uttara_o.hasTag(case["referent_linga"]), \
            f"{case['label']}: uttara missing referent liṅga ?{case['referent_linga']}"
        assert uttara_o.hasTag("samasa_liNga_locked"), \
            f"{case['label']}: uttara gender not locked ({sorted(uttara_o.tags)})"

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
    assert got == {_to_slp1(s) for s in want}, \
        f"{case['label']}: surface {got} != {want}"


# ── Gender sweep: exocentricity (पीत+अम्बर declines in the REFERENT's gender) ──────
# The hallmark of the bahuvrīhi: the SAME stem (अम्बर, natively neuter) declines masc /
# fem / neut purely from the external referent — पीताम्बरः (Viṣṇu) / पीताम्बरा (a woman) /
# पीताम्बरम् (a thing). This is what 2.4.26 (uttara gender) could never produce.
_GENDER_SWEEP = {
    "pum":   ["पीताम्बरः"],
    "strI":  ["पीताम्बरा"],
    "napum": ["पीताम्बरम्"],
}


@pytest.mark.parametrize("linga", sorted(_GENDER_SWEEP))
def test_bahuvrihi_gender_sweep(linga):
    purva = _build_member({"stem": "pIta", "vacana": 1, "vibhakti": 1})
    uttara = _build_member({"stem": "ambara", "vacana": 1, "vibhakti": 1},
                           referent_linga=linga)
    pl = [Adya, purva, uttara, avasAna]
    if linga == "strI":
        # an a-stem feminine takes ṭāp (SK454/4.1.4 अजाद्यतष्टाप्): the strī_abs
        # element at the (uttara | strī) window feminises अम्बर → अम्बरा → पीताम्बरा.
        pl.insert(-1, deepcopy(strI_abs))
    got = _surface(pl)
    expected = {_to_slp1(s) for s in _GENDER_SWEEP[linga]}
    assert got == expected, f"bahuvrīhi referent {linga}: {got} != {expected}"


# ── Vibhakti sweep (masc referent): the compound declines as a normal masc a-stem ──
_VIBHAKTI_SWEEP = {
    1: ["पीताम्बरः"],
    2: ["पीताम्बरम्"],
    3: ["पीताम्बरेण"],
    4: ["पीताम्बराय"],
    5: ["पीताम्बरात्", "पीताम्बराद्"],
    6: ["पीताम्बरस्य"],
    7: ["पीताम्बरे"],
}


@pytest.mark.parametrize("vib_n", sorted(_VIBHAKTI_SWEEP))
def test_bahuvrihi_vibhakti_sweep(vib_n):
    purva = _build_member({"stem": "pIta", "vacana": 1, "vibhakti": 1})
    uttara = _build_member({"stem": "ambara", "vacana": 1, "vibhakti": vib_n},
                           referent_linga="pum")
    got = _surface([Adya, purva, uttara, avasAna])
    expected = {_to_slp1(s) for s in _VIBHAKTI_SWEEP[vib_n]}
    assert got == expected, f"bahuvrīhi viBakti_{vib_n}: {got} != {expected}"
