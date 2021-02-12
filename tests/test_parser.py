#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os.path
from tests.conftest import get_testcount
from tests.parser.test_conll import conll_tests, parse_test_f
import itertools
import inspect


def test_parse(parse_entry):
    testpadas = [t[1] for t in parse_entry]
    status, parse = parse_test_f(parse_entry, testpadas)
    assert status


def pytest_generate_tests(metafunc):
    test_count = get_testcount(metafunc.config)
    if 'parse_entry' in metafunc.fixturenames:
        base_dir = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))
        data_dir = os.path.join(base_dir, 'parser')
        manual_file = open(os.path.join(data_dir, "golden.conll"), "rt")
        if test_count > 0:
            parse_entries = itertools.islice(conll_tests(manual_file), test_count)
        else:
            parse_entries = conll_tests(manual_file)
        metafunc.parametrize("parse_entry", list(parse_entries))
        manual_file.close()
