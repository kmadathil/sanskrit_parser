# -*- coding: utf-8 -*-
"""The strī ADVISORY pre-pass (phase W1 of word_formation_ordering_plan.md).

The pre-pass records which feminine affix a member WOULD take — `?NI_adv` / `?Ap_adv` /
`?UN_adv` on the stem — before the kāraka and samāsa pre-passes run, which is three bahiranga
levels before the affix is actually chosen. Nothing reads those tags yet; W3 will.

The property that matters is that **the advisory verdict agrees with the real derivation**, so
each case here derives `[stem, strI_abs]` for real and checks the advice against the affix that
actually landed, read off the resulting stem's final vowel (ā = ṭāp, ī = ṅī, ū = ūṅ). A
verdict that merely looks plausible is worthless: the whole point is that a −1 rule can trust
it.

अज is the case that earns the file. It advises `?Ap_adv` (अजा) only because the audit
classifies rule arms INDIVIDUALLY — SK454+/4.1.4.1's first arm is the plain-word
ajādi-prabalatva, its second names `?samAsa`. Judging the rule as a whole excluded it from the
advisory set, 4.1.63 जातेः ṅīṣ then won unopposed, and अज was advised `?NI_adv` against its own
derivation अजा.
"""
from copy import deepcopy

import pytest

from sanskrit_parser.generator.prakriya import PrakriyaVakya
from sanskrit_parser.generator.antaranga_prakriya import AntarangaPrakriya
from sanskrit_parser.generator.pratyaya import Adya, avasAna, strI_abs
from sanskrit_parser.generator import pratipadika as _pratipadika

from conftest import sutra_list

# stem → the affix its own derivation must produce. Chosen to cover every path the advisory
# sandbox can take: plain ṭāp, the ajādi-prabalatva apavāda, gaurādi ṅīṣ, ugit ṅīp, ūṅ, a
# jāti ṅīṣ, and a vibhāṣā that is genuinely two-valued.
_CASES = [
    ("brAhmaRa", ["NI"]),        # ङीप्
    ("kumAra",   ["NI"]),        # ङीप् 4.1.20
    ("gaura",    ["NI"]),        # ङीष् 4.1.41 गौरादि
    ("revat",    ["NI"]),        # ङीप् 4.1.6 उगितश्च (ugit रेवत्)
    ("aja",      ["Ap"]),        # ṭāp by the 4.1.4.1 ajādi-prabalatva, NOT 4.1.63 ṅīṣ
    ("loka",     ["Ap"]),        # plain ṭāp 4.1.4 — त्रिलोकी's ṅīp is the COMPOUND's, not this
    ("eka",      ["Ap"]),
    ("kuru",     ["UN"]),        # ऊङ् 4.1.66
    ("rohita",   ["Ap", "NI"]),  # 4.1.39 वा — रोहिणी / रोहिता, genuinely two-valued
]

_VOWEL_TO_AFFIX = {"A": "Ap", "I": "NI", "U": "UN"}


def _advisory_tags(stem):
    """The verdict the pre-pass records on the stem, from a [stem, strI_abs] input."""
    pl = [Adya, deepcopy(stem), deepcopy(strI_abs), avasAna]
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya(pl))
    return sorted(t[:-4] for t in p.inputs[1].tags if t.endswith("_adv"))


def _derived_affixes(stem):
    """The affix the real derivation lands on, per output branch, from its final vowel."""
    pl = [Adya, deepcopy(stem), deepcopy(strI_abs), avasAna]
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya(pl))
    p.execute()
    out = set()
    for branch in p.output():
        surface = "".join(x.canonical() for x in branch).rstrip(avasAna.canonical())
        assert surface, f"{stem} produced an empty derivation"
        out.add(_VOWEL_TO_AFFIX.get(surface[-1], f"?{surface[-1]}"))
    return sorted(out)


@pytest.mark.parametrize("name,want", _CASES, ids=[c[0] for c in _CASES])
def test_advisory_matches_the_real_derivation(name, want):
    stem = getattr(_pratipadika, name)
    advised = _advisory_tags(stem)
    derived = _derived_affixes(stem)
    assert derived == want, f"{name}: derivation gives {derived}, expected {want}"
    assert advised == want, f"{name}: advised {advised}, but derivation gives {derived}"


def test_advisory_is_not_written_without_a_stri_abs():
    """A stem with no feminine affix after it must be left alone — the pre-pass keys on the
    placeholder, not on the stem, so a masculine derivation never acquires a verdict."""
    pl = [Adya, deepcopy(_pratipadika.brAhmaRa), avasAna]
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya(pl))
    assert [t for t in p.inputs[1].tags if t.endswith("_adv")] == []


def test_advisory_does_not_consume_the_placeholder():
    """The verdict is ADVICE. The `strI_abs` element must survive the pre-pass untouched, or
    the compound-level rules (SK479/4.1.21 दिगोः → त्रिलोकी) lose the slot they resolve."""
    pl = [Adya, deepcopy(_pratipadika.loka), deepcopy(strI_abs), avasAna]
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya(pl))
    assert p.inputs[1].hasTag("Ap_adv"), "loka should have been advised ṭāp"
    assert p.inputs[2].hasTag("strI_abs"), "the placeholder was consumed by the advisory pass"
    assert not p.inputs[2].hasTag("Ap"), "the placeholder was resolved, not merely advised"
