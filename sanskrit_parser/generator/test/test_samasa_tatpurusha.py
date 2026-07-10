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


# ── T3 nañ vibhakti sweep: अनश्व (न + अश्व) as a clean masc a-stem ─────────────
# न → अन् before the vowel of अश्व (6.3.74, नुṭ augment) → अनश्व, which then declines
# NORMALLY in the uttara's masc gender (2.4.26 परवल्लिङ्गम्) — the राम paradigm. अश्व
# has no र/ष, so the sweep stays off the ṇatva-blocker corner that अब्राह्मणेन hits
# (there the ण of ब्राह्मण blocks the र from ṇatva-ising the -ena न — an engine detail
# unrelated to the nañ mechanism; अब्राह्मणः is asserted nom-sg only in samasa_list.py).
_ANASHVA_VIBHAKTIS = {
    1: ["अनश्वः"],
    2: ["अनश्वम्"],
    3: ["अनश्वेन"],
    4: ["अनश्वाय"],
    5: ["अनश्वात्", "अनश्वाद्"],    # a-stem ablative (त्/द् pada-final variants)
    6: ["अनश्वस्य"],
    7: ["अनश्वे"],
}


@pytest.mark.parametrize("vib_n", sorted(_ANASHVA_VIBHAKTIS))
def test_tatpurusha_nan_sweep(vib_n):
    """न + अश्व (nañ-tatpuruṣa) declined per vibhakti (sg) — proves the nañ compound
    declines as a normal masc a-stem after न→अन् (6.3.74), unlike the avyayībhāva's
    invariant अम्."""
    purva = deepcopy(getattr(_avyaya, "naY"))
    purva.setTag("semantic_1")       # keeps the avyaya pūrva a distinct ?pada member
    purva.setTag("samAsa_vivakza")
    uttara = deepcopy(getattr(_pratipadika, "aSva"))
    uttara.setTag("vacana_1")
    uttara.setTag(f"viBakti_{vib_n}")   # external compound case
    uttara.setTag("has_viBakti")
    uttara.setTag("samAsa_vivakza")
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya([Adya, purva, uttara, avasAna]))
    p.execute()
    got = {"".join(x.canonical() for x in o).rstrip(avasAna.canonical())
           for o in p.output()}
    expected = {_to_slp1(s) for s in _ANASHVA_VIBHAKTIS[vib_n]}
    assert got == expected, f"अनश्व viBakti_{vib_n}: {got} != {expected}"


# ── T4 prādi vibhakti sweep: प्राचार्य (प्र + आचार्य) as a clean masc a-stem ─────
# The prādi pūrva प्र (avyaya, sup luks) + आचार्य → प्राचार्य (a+ā→ā), which then
# declines NORMALLY in the uttara's masc gender (2.4.26 परवल्लिङ्गम्) — the राम
# paradigm — proving the prādi-tatpuruṣa is not indeclinable.
_PRACARYA_VIBHAKTIS = {
    1: ["प्राचार्यः"],
    2: ["प्राचार्यम्"],
    3: ["प्राचार्येण"],
    4: ["प्राचार्याय"],
    5: ["प्राचार्यात्", "प्राचार्याद्"],
    6: ["प्राचार्यस्य"],
    7: ["प्राचार्ये"],
}


@pytest.mark.parametrize("vib_n", sorted(_PRACARYA_VIBHAKTIS))
def test_tatpurusha_pradi_sweep(vib_n):
    """प्र + आचार्य (prādi-tatpuruṣa, 2.2.18) declined per vibhakti (sg) — a normal
    masc a-stem, proving the prādi compound declines (not an indeclinable)."""
    purva = deepcopy(getattr(_pratipadika, "pra"))
    purva.setTag("semantic_1")       # keeps the avyaya pūrva a distinct ?pada member
    purva.setTag("samAsa_vivakza")
    uttara = deepcopy(getattr(_pratipadika, "AcArya"))
    uttara.setTag("vacana_1")
    uttara.setTag(f"viBakti_{vib_n}")   # external compound case
    uttara.setTag("has_viBakti")
    uttara.setTag("samAsa_vivakza")
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya([Adya, purva, uttara, avasAna]))
    p.execute()
    got = {"".join(x.canonical() for x in o).rstrip(avasAna.canonical())
           for o in p.output()}
    expected = {_to_slp1(s) for s in _PRACARYA_VIBHAKTIS[vib_n]}
    assert got == expected, f"प्राचार्य viBakti_{vib_n}: {got} != {expected}"


# ── SK769/1.4.68 अस्तं च: the gati saṁjñā is a REAL pre-pass rule feeding 2.2.18 ──
# astam is NOT tagged ?gati intrinsically; 1.4.68 (=astam) assigns ?gati in the samāsa
# pre-pass window, which then feeds the gati arm of 2.2.18. (astam has no common
# noun-compound surface; the 1.4.61 ऊरीकृतम् case above covers a gati SURFACE.)
def test_gati_sanjna_astam_SK769_1_4_68():
    astam = deepcopy(getattr(_pratipadika, "astam"))
    assert not astam.hasTag("gati"), "astam must NOT be intrinsically ?gati (1.4.68 assigns it)"
    astam.setTag("semantic_1")       # triggers the pre-pass window (nitya, no vivakza)
    uttara = deepcopy(getattr(_pratipadika, "kfta"))
    uttara.setTag("vacana_1")
    uttara.setTag("viBakti_1")
    uttara.setTag("has_viBakti")
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya([Adya, astam, uttara, avasAna]))
    fired = {aps for e in p.karaka_log for aps in e["fired"]}
    assert "1.4.68" in fired, f"1.4.68 (gati saṁjñā for astam) did not fire: {sorted(fired)}"
    assert "2.2.18" in fired, f"2.2.18 gati arm did not fire for astam: {sorted(fired)}"
    branch = (getattr(p, "_karaka_branches", None) or [p.inputs])[0]
    flat = []
    for o in branch:
        flat.extend(o if isinstance(o, list) else [o])
    members = [o for o in flat
               if o.canonical() and o.hasTag("prAtipadika") and not o.hasTag("sup")]
    assert members[0].hasTag("gati"), "1.4.68 did not assign ?gati to astam"


# ── SK768/1.4.67 पुरोऽव्ययम्: puras is NO LONGER intrinsically ?gati — the real rule
# 1.4.67 (a main-scan saṁjñā, bahiranga: 0) now assigns the गति that the main-scan
# sandhi 8.3.40 नमस्पुरसोर्गत्योः consumes → पुरस्कृतम् (H → s). This proves 1.4.67 does
# real work (the पुरस्कृतम् in test_list.py::SK154 goes through this same path).
def test_gati_sanjna_puras_SK768_1_4_67():
    assert not getattr(_pratipadika, "puras").hasTag("gati"), \
        "puras must NOT be intrinsically ?gati — 1.4.67 पुरोऽव्ययम् assigns it"
    puras = deepcopy(getattr(_pratipadika, "puras"))
    kfta = deepcopy(getattr(_pratipadika, "kfta"))
    kfta.setTag("vacana_1")
    kfta.setTag("viBakti_1")
    kfta.setTag("has_viBakti")
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya([Adya, puras, kfta, avasAna]))
    p.execute()
    got = {"".join(x.canonical() for x in o).rstrip(avasAna.canonical())
           for o in p.output()}
    # 1.4.67 → puras ?gati → 8.3.40 नमस्पुरसोर्गत्योः: the visarga becomes स् before कृत
    # (पुरः → पुरस्कृ…), NOT पुरःकृ / पुरकृ. That s-junction is the proof 1.4.67 fired.
    # (The full पुरस्कृतम् with the sup ending is asserted in test_list.py::SK154.)
    assert any(g.startswith("puraskf") for g in got), \
        f"1.4.67 → 8.3.40 H→s junction (puras+kfta) broken: {got}"


# ── T5 samāsānta vibhakti sweep: परमराज (परम + राजन् + टच्) as a masc a-stem ────


# ── T5 samāsānta vibhakti sweep: परमराज (परम + राजन् + टच्) as a masc a-stem ────
# 5.4.91 राजाहःसखिभ्यष्टच् turns the rājan-final tatpuruṣa into an a-stem (परमराज,
# न-lopa via 6.4.144), so it declines as the राम paradigm — proving the samāsānta
# makes the compound a normally-declining a-stem (not the an-stem राजा).
_PARAMARAJA_VIBHAKTIS = {
    1: ["परमराजः"],
    2: ["परमराजम्"],
    3: ["परमराजेन"],
    4: ["परमराजाय"],
    5: ["परमराजात्", "परमराजाद्"],
    6: ["परमराजस्य"],
    7: ["परमराजे"],
}


@pytest.mark.parametrize("vib_n", sorted(_PARAMARAJA_VIBHAKTIS))
def test_tatpurusha_samasanta_sweep(vib_n):
    """परम + राजन् + टच् (5.4.91) declined per vibhakti (sg) — a masc a-stem
    (परमराज), proving the ṬaC samāsānta yields a normally-declining compound."""
    purva = deepcopy(getattr(_pratipadika, "parama"))
    purva.setTag("vacana_1")
    purva.setTag("viBakti_1")           # karmadhāraya pūrva (prathamā, luks via 2.4.71)
    purva.setTag("has_viBakti")
    purva.setTag("viSezaRa")
    purva.setTag("samAsa_vivakza")
    uttara = deepcopy(getattr(_pratipadika, "rAjan"))
    uttara.setTag("vacana_1")
    uttara.setTag(f"viBakti_{vib_n}")   # external compound case
    uttara.setTag("has_viBakti")
    uttara.setTag("samAsa_vivakza")
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya([Adya, purva, uttara, avasAna]))
    p.execute()
    got = {"".join(x.canonical() for x in o).rstrip(avasAna.canonical())
           for o in p.output()}
    expected = {_to_slp1(s) for s in _PARAMARAJA_VIBHAKTIS[vib_n]}
    assert got == expected, f"परमराज viBakti_{vib_n}: {got} != {expected}"


# ── T-liṅga: 2.4.29 रात्राह्नाहाः पुंसि — the ahan-family gender override ─────────
# An ahan-final (non-samāhāra) tatpuruṣa is MASCULINE (2.4.29), overriding the
# native napuṁsaka of अहन्. This is a pre-pass gender override: the uttara अहन् is
# re-tagged ?pum (dropping ?napum) and locked (?samasa_liNga_locked), so the
# compound declines masculine, NOT napuṁsaka. Asserted at the structure/trace
# level — the full a-stem SURFACE (द्व्यहः) needs the deferred ahar टच् samāsānta
# (5.4.91 ahar-arm; see the T5 Skipped row), so this proves the gender override
# without depending on that surface.
def test_tatpurusha_liNga_ahan_pumsi():
    """द्वि + अहन् (a non-samāhāra dvigu-tatpuruṣa): 2.4.29 रात्राह्नाहाः पुंसि forces
    the natively-napuṁsaka अहन् uttara to MASCULINE (overriding 2.4.26)."""
    dvi = deepcopy(getattr(_pratipadika, "dvi"))     # ?saMKyA
    dvi.setTag("samAsa_vivakza")
    ahan = deepcopy(getattr(_pratipadika, "ahan"))   # natively ?napum
    ahan.setTag("vacana_1")
    ahan.setTag("viBakti_1")
    ahan.setTag("has_viBakti")
    ahan.setTag("samAsa_vivakza")
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya([Adya, dvi, ahan, avasAna]))
    fired = {aps for e in p.karaka_log for aps in e["fired"]}
    assert "2.4.29" in fired, f"2.4.29 did not fire: {sorted(fired)}"
    # Locate the ahan uttara in the (nested) pre-pass branch.
    branch = (getattr(p, "_karaka_branches", None) or [p.inputs])[0]
    flat = []
    for o in branch:
        flat.extend(o if isinstance(o, list) else [o])
    members = [o for o in flat
               if o.canonical() and o.hasTag("prAtipadika") and not o.hasTag("sup")]
    uttara = members[-1]
    assert uttara.hasTag("tatpuruza"), f"uttara {uttara} not a tatpuruṣa"
    assert uttara.hasTag("pum"), f"2.4.29: uttara {uttara} not masc ({sorted(uttara.tags)})"
    assert not uttara.hasTag("napum"), \
        f"2.4.29: uttara {uttara} still napuṁsaka ({sorted(uttara.tags)})"
    assert uttara.hasTag("samasa_liNga_locked"), \
        f"2.4.29: uttara {uttara} gender not locked ({sorted(uttara.tags)})"


# ── SK787/5.4.87 + SK814/2.4.29 rātri arm: पुण्यरात्र declines masc a-stem ──────
# पुण्य + रात्रि → SK787/5.4.87 अहस्सर्वैकदेशसंख्यातपुण्याच्च रात्रेः → रात्र (a-stem, i-lopa
# 6.4.148), then SK814/2.4.29 रात्राह्नाहाः पुंसि makes the compound MASCULINE (overriding
# रात्रि's native feminine + 2.4.26 paravalliṅga). This is the REAL surface that upgrades
# 2.4.29 from the structure-only ahan check above — पुण्यरात्र follows the राम paradigm.
_PUNYARATRA_VIBHAKTIS = {
    1: ["पुण्यरात्रः"],
    2: ["पुण्यरात्रम्"],
    3: ["पुण्यरात्रेण"],          # ṇatva: रात्र's र → न्→ण् across एन (8.4.2)
    4: ["पुण्यरात्राय"],
    5: ["पुण्यरात्रात्", "पुण्यरात्राद्"],
    6: ["पुण्यरात्रस्य"],
    7: ["पुण्यरात्रे"],
}


@pytest.mark.parametrize("vib_n", sorted(_PUNYARATRA_VIBHAKTIS))
def test_tatpurusha_ratri_samasanta_sweep(vib_n):
    """पुण्य + रात्रि (SK787/5.4.87 → रात्र + SK814/2.4.29 → masc) declined per vibhakti
    (sg) — a masc a-stem पुण्यरात्र, proving the रātri samāsānta + the masculine
    gender-override together yield a normally-declining compound."""
    purva = deepcopy(getattr(_pratipadika, "puRya"))
    purva.setTag("vacana_1")
    purva.setTag("viBakti_1")           # karmadhāraya pūrva (prathamā, luks via 2.4.71)
    purva.setTag("has_viBakti")
    purva.setTag("viSezaRa")
    purva.setTag("samAsa_vivakza")
    uttara = deepcopy(getattr(_pratipadika, "rAtri"))
    uttara.setTag("vacana_1")
    uttara.setTag(f"viBakti_{vib_n}")   # external compound case
    uttara.setTag("has_viBakti")
    uttara.setTag("samAsa_vivakza")
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya([Adya, purva, uttara, avasAna]))
    p.execute()
    got = {"".join(x.canonical() for x in o).rstrip(avasAna.canonical())
           for o in p.output()}
    expected = {_to_slp1(s) for s in _PUNYARATRA_VIBHAKTIS[vib_n]}
    assert got == expected, f"पुण्यरात्र viBakti_{vib_n}: {got} != {expected}"
