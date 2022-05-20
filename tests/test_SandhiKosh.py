#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os.path
import pytest

from indic_transliteration import sanscript
from sanskrit_parser.parser.sandhi_analyzer import LexicalSandhiAnalyzer
from sanskrit_parser.base.sanskrit_base import SanskritObject, outputctx
from tests.conftest import get_testcount
import pandas as pd
import inspect


@pytest.fixture(scope="module")
def lexan():
    return LexicalSandhiAnalyzer()


def get_kosh_entries(test_count):
    kosh_entries = []
    base_dir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
    data_dir = os.path.join(base_dir, 'SandhiKosh')
    kosh = pd.read_excel(os.path.join(data_dir, "Result.xls"))[['S. No.', 'Word', 'Split', 'Status']]
    kosh_entries.extend(kosh[kosh['Status'] == "Pass"].to_dict(orient='records'))
    return kosh_entries[:test_count] if test_count > 0 else kosh_entries


def test_file_splits(lexan, kosh_entry):
    clean_input = False
    f = kosh_entry['Word']
    s = kosh_entry['Split']
    clean_input = True
    with outputctx(False):
        i = SanskritObject(f, encoding=sanscript.DEVANAGARI, strict_io=True, replace_ending_visarga=None)
        if clean_input:
            sl = [SanskritObject(x, encoding=sanscript.DEVANAGARI, strict_io=True,
                                 replace_ending_visarga=None).canonical()
                  for x in s.strip().replace(" ", "+").split('+')]
        else:
            sl = [SanskritObject(x, encoding=sanscript.DEVANAGARI, strict_io=True, replace_ending_visarga=None).canonical() for x in s.split('+')]
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
