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
    # The samāsa pre-pass nests the compound members into a sub-list (so the
    # compound resolves as one samasta_pada — see _nest_samasa_members), so
    # flatten one level before scanning for member objects.
    branch = (getattr(p, "_karaka_branches", None) or [p.inputs])[0]
    flat = []
    for o in branch:
        flat.extend(o if isinstance(o, list) else [o])
    members = [o for o in flat
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


# ── T1 vibhakti sweeps: masc (ṣaṣṭhī + caturthī) + napuṁsaka (ṣaṣṭhī) ──────────
# Each proves the compound declines NORMALLY in the uttara's gender (2.4.26
# परवल्लिङ्गम्): राजपुरुष / धान्यार्थ as masc a-stems (राम paradigm), जीवसुख as a
# napuṁsaka a-stem (nom=acc जीवसुखम्, the hallmark napuṁsaka अम्). राजपुरुष exercises
# ṇatva (राजपुरुषेण, inst) — the compound resolves as one samasta_pada via the
# pre-pass member-nesting (_nest_samasa_members), so the uttara ष triggers 8.4.2
# across एन just as in a plain pada. (A pūrva-only ṇatva trigger reaching the
# uttara's sup — चोरभयेण — is still not applied; a pre-existing engine gap seen on
# the CLI in_compound path too, unrelated to T1. See generator_status.md.)
def _sweep(purva_stem, purva_vib, uttara_stem, vib_n):
    purva = deepcopy(getattr(_pratipadika, purva_stem))
    purva.setTag("vacana_1")
    purva.setTag(f"viBakti_{purva_vib}")   # vigraha vibhakti (luks via 2.4.71)
    purva.setTag("has_viBakti")
    purva.setTag("samAsa_vivakza")
    uttara = deepcopy(getattr(_pratipadika, uttara_stem))
    uttara.setTag("vacana_1")
    uttara.setTag(f"viBakti_{vib_n}")       # external compound case
    uttara.setTag("has_viBakti")
    uttara.setTag("samAsa_vivakza")
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya([Adya, purva, uttara, avasAna]))
    p.execute()
    return {"".join(x.canonical() for x in o).rstrip(avasAna.canonical())
            for o in p.output()}


_DHANYARTHA_VIBHAKTIS = {           # धान्याय अर्थः (caturthī 2.1.36) — masc a-stem
    1: ["धान्यार्थः"],
    2: ["धान्यार्थम्"],
    3: ["धान्यार्थेन"],
    4: ["धान्यार्थाय"],
    5: ["धान्यार्थात्", "धान्यार्थाद्"],
    6: ["धान्यार्थस्य"],
    7: ["धान्यार्थे"],
}


@pytest.mark.parametrize("vib_n", sorted(_DHANYARTHA_VIBHAKTIS))
def test_tatpurusha_caturthi_sweep(vib_n):
    """धान्याय अर्थः (caturthī-tatpuruṣa) declined per vibhakti (sg) — a normal
    masc a-stem, proving the tatpuruṣa is not indeclinable."""
    got = _sweep("DAnya", 4, "arTa", vib_n)
    expected = {_to_slp1(s) for s in _DHANYARTHA_VIBHAKTIS[vib_n]}
    assert got == expected, f"धान्यार्थ viBakti_{vib_n}: {got} != {expected}"


_RAJAPURUSHA_VIBHAKTIS = {           # राज्ञः पुरुषः (ṣaṣṭhī 2.2.8) — masc a-stem, ṇatva
    1: ["राजपुरुषः"],
    2: ["राजपुरुषम्"],
    3: ["राजपुरुषेण"],               # ṇatva: uttara ष → न्→ण् across एन (8.4.2) — the fix
    4: ["राजपुरुषाय"],
    5: ["राजपुरुषात्", "राजपुरुषाद्"],
    6: ["राजपुरुषस्य"],
    7: ["राजपुरुषे"],
}


@pytest.mark.parametrize("vib_n", sorted(_RAJAPURUSHA_VIBHAKTIS))
def test_tatpurusha_sasthi_natva_sweep(vib_n):
    """राज्ञः पुरुषः (ṣaṣṭhī-tatpuruṣa) declined per vibhakti (sg). The an-stem
    pūrva राजन् → राज (8.2.7 न-lopa), and the compound resolves as one
    samasta_pada (pre-pass nesting) so the uttara ष triggers ṇatva → राजपुरुषेण
    (inst) — the previously-missing ṇatva that motivated _nest_samasa_members."""
    got = _sweep("rAjan", 6, "puruza", vib_n)
    expected = {_to_slp1(s) for s in _RAJAPURUSHA_VIBHAKTIS[vib_n]}
    assert got == expected, f"राजपुरुष viBakti_{vib_n}: {got} != {expected}"


_JIVASUKHA_VIBHAKTIS = {            # जीवस्य सुखम् (ṣaṣṭhī 2.2.8) — napuṁsaka a-stem
    1: ["जीवसुखम्"],
    2: ["जीवसुखम्"],                 # napuṁsaka nom=acc अम् (2.4.26 → uttara सुख napuṁsaka)
    3: ["जीवसुखेन"],
    4: ["जीवसुखाय"],
    5: ["जीवसुखात्", "जीवसुखाद्"],
    6: ["जीवसुखस्य"],
    7: ["जीवसुखे"],
}


@pytest.mark.parametrize("vib_n", sorted(_JIVASUKHA_VIBHAKTIS))
def test_tatpurusha_napumsaka_sweep(vib_n):
    """जीवस्य सुखम् (ṣaṣṭhī-tatpuruṣa) declined per vibhakti (sg) — a napuṁsaka
    a-stem (nom=acc जीवसुखम्), proving 2.4.26 inherits the uttara's napuṁsaka."""
    got = _sweep("jIva", 6, "suKa", vib_n)
    expected = {_to_slp1(s) for s in _JIVASUKHA_VIBHAKTIS[vib_n]}
    assert got == expected, f"जीवसुख viBakti_{vib_n}: {got} != {expected}"


# ── T2 real-dvigu ṅīp: त्रिलोकी from a REAL dvigu (2.1.52), not the in_compound shim ─
# The T2 dvigu saṁjñā (2.1.52 संख्यापूर्वो द्विगुः) tags the compound ?dvigu via real
# compound formation in the samāsa pre-pass. That ?dvigu rides to the merged stem
# (join_objects Tier-3) so the existing 4.1.21 (SK479) द्विगोः ṅīप fires at the
# (loka | strI_abs) window → त्रिलोकी. This replaces the vibhaktis_list.py shim
# (in_context(in_compound(loka), "dvigu")) that set ?dvigu by hand — the shim tests
# (त्रिलोकी/त्रिफला/पञ्चाश्वी) still stand, but the tag now also has a real producer.
def test_real_dvigu_ngiip_trilokI():
    """त्रि + लोक (a REAL saṅkhyā-pūrva dvigu, 2.1.52) + strī → त्रिलोकी: the ?dvigu
    the pre-pass assigns drives SK479 (4.1.21) ṅīp, exactly as the hand-tagged
    shim did — proving the dvigu saṁjñā is wired to the feminine-pratyaya path."""
    from sanskrit_parser.generator.pratyaya import strI_abs
    tri = deepcopy(getattr(_pratipadika, "tri"))       # tri: ?saMKyA (intrinsic)
    tri.setTag("samAsa_vivakza")
    loka = deepcopy(getattr(_pratipadika, "loka"))
    loka.setTag("vacana_1")
    loka.setTag("samAsa_vivakza")
    p = AntarangaPrakriya(sutra_list,
                          PrakriyaVakya([Adya, tri, loka, deepcopy(strI_abs), avasAna]))
    # ?dvigu is set by the REAL rule 2.1.52 (not a composer shim).
    fired = {aps for e in p.karaka_log for aps in e["fired"]}
    assert "2.1.52" in fired, f"2.1.52 (dvigu saṁjñā) did not fire: {sorted(fired)}"
    p.execute()
    got = {"".join(x.canonical() for x in o).rstrip(avasAna.canonical())
           for o in p.output()}
    assert got == {_to_slp1("त्रिलोकी")}, f"real-dvigu त्रिलोकी: {got}"
