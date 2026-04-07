"""
Samāsa (compound) inflection tests.

Tests compound prakriyas where the uttara-pada (second member) is tagged with
?samAsa via in_compound(). This tests:
  - SK257 (1.4.8): gaṇapati — pati in compound gets ghī-saṃjñā
  - SK376 (7.1.71): aśvayuj — compound yuj has no nUM augment (?samAsa blocks SK376)
  - SK379 (6.3.128): viśvāvasu / viśvārāṭ — viśva final a→ā before vasu/rāṭ in compound
"""
from indic_transliteration import sanscript
from conftest import sutra_list, run_test


def test_samAsa_pum(samAsa_pum):
    run_test(samAsa_pum, sutra_list, encoding=sanscript.DEVANAGARI)

def test_samAsa_strI(samAsa_strI):
    run_test(samAsa_strI, sutra_list, encoding=sanscript.DEVANAGARI)

def test_samAsa_napum(samAsa_napum):
    run_test(samAsa_napum, sutra_list, encoding=sanscript.DEVANAGARI)
