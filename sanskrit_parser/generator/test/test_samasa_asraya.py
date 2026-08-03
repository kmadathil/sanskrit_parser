# -*- coding: utf-8 -*-
"""समासाश्रयविधिप्रकरणम् test driver (samasa_asraya_plan.md, SK 985–1071).

Unlike the four per-samāsa-type drivers (avyayībhāva / tatpuruṣa / bahuvrīhi / dvandva),
the samāsāśrayavidhi rules are TYPE-AGNOSTIC: they mutate the members of an
already-formed compound, whichever kind it is. So each case names the formation it
rides on via a "type" field, and `_build_members` supplies exactly the intent tags that
formation's saṁjñā rule needs:

  "zazWI"       — ṣaṣṭhī-tatpuruṣa (SK702/2.2.8): pūrva viBakti_6 + ?samAsa_vivakza
  "karmaDAraya" — karmadhāraya  (SK/2.1.57):      pūrva viBakti_1 + ?viSezaRa + vivakṣā
  "ku"          — prādi/ku-tatpuruṣa (SK761/2.2.18, NITYA): pūrva carries only a
                  semantic sense — no vivakṣā (that is what makes it nitya)
  "saha_bv"     — saha-bahuvrīhi (SK848/2.2.28): both members ?bahuvrIhi_vivakza,
                  pūrva viBakti_1, referent liṅga on the uttara

Three assertion levels per case (samasa_asraya_list.py :: samasa_asraya_tests):
  1. structure : the pre-pass gave the members their roles (?samAsaPurva / ?samAsa)
  2. fired     : listed pre-pass sutras present in the pre-pass trace, and any
                 "not_fired" ids absent (this is where the negative controls live —
                 the substitution must NOT happen outside the sūtra's condition)
  3. surface   : full-pipeline output equals the expected form(s)
"""
from copy import deepcopy

import pytest
from indic_transliteration import sanscript

from sanskrit_parser.generator.prakriya import PrakriyaVakya
from sanskrit_parser.generator.antaranga_prakriya import AntarangaPrakriya
from sanskrit_parser.generator.pratyaya import Adya, avasAna
from sanskrit_parser.generator import pratipadika as _pratipadika
from sanskrit_parser.generator import pratyaya as _pratyaya
from sanskrit_parser.generator import avyaya as _avyaya

from conftest import sutra_list
from samasa_asraya_list import samasa_asraya_tests


_LINGAS = ("pum", "strI", "napum")

# type → (extra pūrva tags, extra uttara tags). The vibhakti/vacana a member needs
# beyond this comes from its own spec.
_FORMATION = {
    "zazWI":       (["samAsa_vivakza"], ["samAsa_vivakza"]),
    "karmaDAraya": (["samAsa_vivakza", "viSezaRa"], ["samAsa_vivakza"]),
    "ku":          ([], []),
    "saha_bv":     (["samAsa_vivakza", "bahuvrIhi_vivakza"],
                    ["samAsa_vivakza", "bahuvrIhi_vivakza"]),
    # NOT a compound: a bare stem + a taddhita affix. SK1002/6.3.64 त्वे च is an
    # affix rule, not an uttarapada rule (अजा + त्व = अजत्वम्), so there is no second
    # member and no samāsa — the structure assertions are skipped for this type.
    "affix":       ([], []),
}
# type → default vigraha vibhakti of the pūrva (a spec's own "vibhakti" wins)
_PURVA_VIBHAKTI = {"zazWI": 6, "karmaDAraya": 1, "ku": None, "saha_bv": 1,
                   "affix": None}


def _set_linga(p, linga):
    """Replace the member's native liṅga (a stem carries exactly one)."""
    for t in _LINGAS:
        if p.hasTag(t):
            p.deleteTag(t)
    p.setTag(linga)


def _build_one(spec, extra_tags, *, vibhakti=None, referent_linga=None):
    if "avyaya" in spec:
        p = deepcopy(getattr(_avyaya, spec["avyaya"]))
    else:
        p = deepcopy(getattr(_pratipadika, spec["stem"]))
    p.setTag(f"vacana_{spec.get('vacana', 1)}")
    vib = spec.get("vibhakti", vibhakti)
    if vib is not None:
        p.setTag(f"viBakti_{vib}")
        p.setTag("has_viBakti")
    if spec.get("sem"):
        p.setTag(spec["sem"])
    # "linga" overrides the stem's lexical gender. Needed where a sūtra's own example is a
    # DERIVATIVE whose gender differs from its base — सतीर्थ्यः / सोदर्यः (SK1015/6.3.87,
    # SK1016/6.3.88) denote persons (masc) though तीर्थ / उदर are both neuter, and the
    # compound takes the uttara's gender by 2.4.26 परवल्लिङ्गम्.
    if spec.get("linga"):
        _set_linga(p, spec["linga"])
    if referent_linga is not None:
        if p.hasTag("strI"):
            p.setTag("uttara_strI")     # preserve the vigraha femininity (as prepare_bahuvrihi does)
        _set_linga(p, referent_linga)
        p.setTag(f"referent_{referent_linga}")
    for t in extra_tags:
        p.setTag(t)
    for t in spec.get("tags", []):
        p.setTag(t)
    return p


def _build_members(case):
    """Returns the input list between Adya and avasAna: [pūrva, uttara] plus, if the case
    asks for one, a taddhita affix placed just after the uttara (before its sup) — the
    same slot _insert_samasanta uses. SK1015/6.3.87 तीर्थे ये and SK1016/6.3.88 विभाषोदरे
    condition on a य-initial affix being INTENDED (यादौ प्रत्यये विवक्षिते), so those cases
    need the यत् physically present to surface सतीर्थ्यः / सोदर्यः."""
    ptags, utags = _FORMATION[case["type"]]
    ref = case.get("referent_linga")
    purva = _build_one(case["purva"], ptags,
                       vibhakti=_PURVA_VIBHAKTI[case["type"]])
    out = [purva]
    if "uttara" in case:
        out.append(_build_one(case["uttara"], utags, referent_linga=ref))
    if case.get("uttara_affix"):
        out.append(deepcopy(getattr(_pratyaya, case["uttara_affix"])))
    if case.get("sup"):
        # An explicit sup, as the plain vibhakti drivers supply (conftest.py:164). Needed by
        # type "affix": AntarangaPrakriya's automatic sup insertion lives inside the kāraka
        # pre-pass, which is skip-guarded on semantic_*/?samAsa_vivakza — neither of which a
        # bare stem+taddhita derivation has. `sup: [N, M]` = vibhakti N, vacana M.
        n, m = case["sup"]
        out.append(deepcopy(_pratyaya.sups[n - 1][m - 1]))
    if ref == "strI":
        # A strī referent needs the ṭāp so an a-stem uttara feminises — the same
        # strI_abs element cmd_line.prepare_bahuvrihi appends (सराक्षसीक → सराक्षसीका).
        out.append(deepcopy(_pratyaya.strI_abs))
    return out


def _to_slp1(deva):
    return sanscript.transliterate(deva, sanscript.DEVANAGARI, sanscript.SLP1)


@pytest.mark.parametrize("case", samasa_asraya_tests,
                         ids=[c["label"] for c in samasa_asraya_tests])
def test_samasa_asraya(case):
    pl = [Adya, *_build_members(case), avasAna]
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya(pl))

    # ── Level 1: structure (pre-pass member roles; flatten the nested sub-list) ──
    # Skipped for type "affix" — there is no compound, so no roles to check.
    if case["type"] != "affix":
        branch = (getattr(p, "_karaka_branches", None) or [p.inputs])[0]
        flat = []
        for o in branch:
            flat.extend(o if isinstance(o, list) else [o])
        members = [o for o in flat
                   if o.canonical() and o.hasTag("prAtipadika") and not o.hasTag("sup")]
        assert len(members) == 2, f"{case['label']}: expected 2 members, got {members}"
        assert members[0].hasTag("samAsaPurva"), \
            f"{case['label']}: pūrva {members[0]} missing ?samAsaPurva ({sorted(members[0].tags)})"
        assert members[1].hasTag("samAsa"), \
            f"{case['label']}: uttara {members[1]} missing ?samAsa ({sorted(members[1].tags)})"

    # ── Level 2: fired-sutra trace (pre-pass rules) ──
    fired = {aps for e in p.karaka_log for aps in e["fired"]}
    for aps in case["fired"]:
        assert aps in fired, \
            f"{case['label']}: {aps} missing from pre-pass trace {sorted(fired)}"
    for aps in case.get("not_fired", []):
        assert aps not in fired, \
            f"{case['label']}: {aps} wrongly fired (trace {sorted(fired)})"

    # ── Level 3: surface (full pipeline) ──
    p.execute()
    got = {"".join(x.canonical() for x in o).rstrip(avasAna.canonical())
           for o in p.output()}
    want = case["surfaces"] if "surfaces" in case else [case["surface"]]
    expected = {_to_slp1(s) for s in want}
    assert got == expected, f"{case['label']}: surface {got} != {expected}"
