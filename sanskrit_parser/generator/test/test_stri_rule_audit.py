# -*- coding: utf-8 -*-
"""Guards the invariant phase W1 of word_formation_ordering_plan.md will rest on.

The plan's advisory phase evaluates the compound-INDEPENDENT strī rules before the samāsa
pre-pass runs. That is only sound while no such rule reads anything the pre-pass produces —
so this asserts the audit's `DEPENDENT (derived)` bucket stays EMPTY. If a future strī rule
gates on a tag a `bahiranga: -1` rule writes, this fails and the rule needs classifying by
hand before the advisory phase can be trusted with it.

The exact 39/30 split is deliberately NOT asserted: adding strī rules is normal, and pinning
the counts would turn ordinary work into a test failure. What must not drift is the invariant.
"""
from sanskrit_parser.generator.stri_rule_audit import classify, load_rules


def _rules():
    return load_rules()[0]


def test_no_advisable_stri_rule_reads_a_prepass_tag():
    stri, _ = classify(_rules())
    derived = [r["id"] for r in stri if r["bucket"] == "DEPENDENT (derived)"]
    assert derived == [], (
        "strI rules now read tags the samāsa pre-pass writes, so they cannot be advised "
        f"early without classification: {derived}")


def test_every_stri_rule_is_classified():
    stri, _ = classify(_rules())
    assert stri, "audit found no strI-window rules at all — the scan is broken"
    buckets = {"DEPENDENT (tag)", "DEPENDENT (position)", "DEPENDENT (derived)",
               "MIXED (some arms independent)", "INDEPENDENT"}
    assert all(r["bucket"] in buckets for r in stri)
