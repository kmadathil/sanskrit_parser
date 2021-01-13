#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os.path
import pytest
from sanskrit_parser.parser.sandhi_analyzer import LexicalSandhiAnalyzer
from sanskrit_parser.base.sanskrit_base import SanskritObject, DEVANAGARI, outputctx
from tests.conftest import get_testcount
import pandas as pd


@pytest.fixture(scope="module")
def lexan():
    return LexicalSandhiAnalyzer()


def get_kosh_entries(test_count):
    kosh_entries = []
    bg_kosh = pd.read_excel(os.path.join('SandhiKosh', "Bhagvad_Gita Corpus.xls"))[['S. No.', 'Word', 'Split']]
    bg_kosh['File'] = "Bhagvad_Gita Corpus.xls"
    uoh_kosh = pd.read_excel(os.path.join('SandhiKosh', "UoH_Corpus.xls"))[['S. No.', 'Word', 'Split']]
    uoh_kosh['File'] = "UoH_Corpus.xls"
    lit_kosh_dict = pd.read_excel(os.path.join('SandhiKosh', "Rule-based Corpus and Literature Corpus.xls"), sheet_name=None)
    for k in lit_kosh_dict:
        t_kosh = lit_kosh_dict[k][['S. No.', 'Word', 'Split']]
        t_kosh['File'] = f"Rule-based Corpus and Literature Corpus.xls:{k}"
        # kosh_entries.extend(t_kosh.to_dict(orient='records'))
    kosh_entries.extend(bg_kosh.to_dict(orient='records'))
    # kosh_entries.extend(uoh_kosh.to_dict(orient='records'))
    return kosh_entries[:test_count] if test_count > 0 else kosh_entries


def test_file_splits(lexan, kosh_entry):
    clean_input = False
    f = kosh_entry['Word']
    s = kosh_entry['Split']
    clean_input = True
    with outputctx(False):
        i = SanskritObject(f, encoding=DEVANAGARI, strict_io=True, replace_ending_visarga=None)
        if clean_input:
            sl = [SanskritObject(x, encoding=DEVANAGARI, strict_io=True,
                                 replace_ending_visarga=None).canonical()
                  for x in s.strip().replace(" ", "+").split('+')]
        else:
            sl = [SanskritObject(x, encoding=DEVANAGARI, strict_io=True, replace_ending_visarga=None).canonical() for x in s.split('+')]
        graph = lexan.getSandhiSplits(i)
        assert graph is not None
        splits = graph.find_all_paths(max_paths=300, sort=False)
        assert sl in [list(map(str, ss)) for ss in splits]


def pytest_generate_tests(metafunc):
    # global clean_input
    # clean_input = get_clean_input(metafunc.config)
    test_count = get_testcount(metafunc.config)
    if 'kosh_entry' in metafunc.fixturenames:
        kosh_entries = get_kosh_entries(test_count)
        metafunc.parametrize("kosh_entry", kosh_entries)
