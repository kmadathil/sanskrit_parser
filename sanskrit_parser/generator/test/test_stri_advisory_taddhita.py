# -*- coding: utf-8 -*-
"""The advisory pre-pass on a TADDHITA chain — phase W5b of word_formation_ordering_plan.md.

A feminine is often built on a taddhita-derived stem: `[vidyA, aR_t, strI_abs]` → वैद्यी,
`[amara, matup, strI_abs]` → अमरावती. W1's scan keyed on "a prātipadika followed by
`strI_abs`", and in a chain the element before the placeholder is the AFFIX, so these got no
verdict at all. W5b admits a `?tadDita` element there too; the advisable rules then read the
affix's own class tags (`?NIp_taddhita` on aṇ/añ/matup/dvayasac/…), which is how SK470/4.1.15
already decides these forms.

This sweep is data-driven rather than a hand-picked list: it walks every paradigm in
`vibhaktis_list` that ends `[…, <taddhita>, strI_abs]` — 32 of them today — and checks the
verdict against the affix the real derivation lands on.

**Silence is allowed; a wrong verdict is not.** Two groups come out silent, and both should:

  * dvigu chains (द्विबिस्ता, द्विकाण्डी, द्व्याढकी, पञ्चाश्वी …) — their feminine is the
    COMPOUND's, decided by SK479/4.1.21 दिगोः and 4.1.22–24, which are compound-dependent and
    so are not in the advisory set. This is the त्रिलोकी hazard one level deeper, and the
    measured answer is that it does not materialise: the sandbox declines rather than guesses.
  * affixes not yet in their final shape (ढक् → एय by 7.1.2, सुपर्णेयी) — nothing matches yet.

Both are safe, because nothing reads an absent verdict. A WRONG verdict would not be.
"""
from copy import deepcopy

import pytest

from sanskrit_parser.generator.prakriya import PrakriyaVakya
from sanskrit_parser.generator.antaranga_prakriya import AntarangaPrakriya
from sanskrit_parser.generator.pratyaya import Adya, avasAna

from conftest import sutra_list
from vibhaktis_list import prAtipadika

_AFFIX_ADV = ("NI_adv", "Ap_adv", "UN_adv")
_VOWEL_TO_AFFIX = {"A": "Ap", "I": "NI", "U": "UN"}


def _taddhita_chains():
    """Every paradigm shaped [… , <taddhita affix>, strI_abs]."""
    out = []
    for name, elements in sorted(prAtipadika.items()):
        if not isinstance(elements, list) or len(elements) < 2:
            continue
        last, prev = elements[-1], elements[-2]
        if not (hasattr(last, "hasTag") and last.hasTag("strI_abs")):
            continue
        if not (hasattr(prev, "hasTag") and prev.hasTag("tadDita")):
            continue
        out.append((name, elements))
    return out


_CHAINS = _taddhita_chains()


def test_the_corpus_is_not_empty():
    """If this ever finds nothing, the sweep below is passing vacuously."""
    assert len(_CHAINS) >= 30, f"only {len(_CHAINS)} taddhita chains found — scan broken?"


@pytest.mark.parametrize("name,elements", _CHAINS, ids=[c[0] for c in _CHAINS])
def test_taddhita_chain_advice_is_right_or_absent(name, elements):
    pl = [Adya] + [deepcopy(e) for e in elements] + [avasAna]
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya(pl))
    advised = sorted({t[:-4] for o in p.inputs if hasattr(o, "tags")
                      for t in o.tags if t in _AFFIX_ADV})
    p.execute()
    derived = sorted({_VOWEL_TO_AFFIX[s[-1]] for s in
                      ("".join(x.canonical() for x in o).rstrip(avasAna.canonical())
                       for o in p.output())
                      if s and s[-1] in _VOWEL_TO_AFFIX})
    assert not advised or advised == derived, (
        f"{name}: advised {advised} but the derivation gives {derived}")
