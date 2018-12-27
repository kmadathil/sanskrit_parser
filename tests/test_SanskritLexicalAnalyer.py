#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import inspect
import os
import pytest
import six
import json
from sanskrit_parser.lexical_analyzer.sanskrit_lexical_analyzer import SanskritLexicalAnalyzer
from sanskrit_parser.base.sanskrit_base import SanskritObject, SLP1
from tests.conftest import get_testcount


@pytest.fixture(scope="module")
def lexan():
    return SanskritLexicalAnalyzer()


def get_splitstxt(test_count):
    fs = []
    base_dir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
    data_dir = os.path.join(base_dir, "test_data_SanskritLexicalAnalyzer")
    with open(os.path.join(data_dir, "splits.txt")) as f:
        for l in f:
            line = l.strip()
            if line and line[0] != '#':
                full, split = line.split('=')
                full = six.u(full.strip())
                split = split.strip()
                splits = list(map(lambda x: six.u(x), split.split(' ')))
                fs.append((full, splits))
    with open(os.path.join(data_dir, "uohd_passing.txt")) as f:
        for l in f:
            test = json.loads(l)
            fs.append((test["full"], test["split"]))
    with open(os.path.join(data_dir, "uohd_split_passing.txt")) as f:
        for l in f:
            test = json.loads(l)
            fs.append((test["full"], test["split"]))
    with open(os.path.join(data_dir, "uohd_failing.txt")) as f:
        for l in f:
            test = json.loads(l)
            fs.append(pytest.mark.xfail((test["full"], test["split"])))
    return fs[:test_count] if test_count > 0 else fs


def test_simple_tag(lexan):
    def _mapt(t):
        return (t[0], set(map(str, t[1])))

    # gaNeshaH
    i = SanskritObject("gaReSas", encoding=SLP1)
    ts = lexan.getLexicalTags(i)
    assert [_mapt(tss) for tss in ts][0] == \
        ('gaReSa', set(['puMlliNgam', 'praTamAviBaktiH', 'ekavacanam']))


def test_simple_split(lexan):
    # gaNeshannamAmi
    i = SanskritObject("gaReSannamAmi", encoding=SLP1)
    graph = lexan.getSandhiSplits(i)
    splits = graph.findAllPaths()
    assert [u'gaReSam', u'namAmi'] in [list(map(str, ss)) for ss in splits]


def test_medium_split(lexan):
    i = SanskritObject("budDaMSaraRaNgacCAmi", encoding=SLP1)
    graph = lexan.getSandhiSplits(i)
    splits = graph.findAllPaths()
    assert [u'budDam', u'SaraRam', u'gacCAmi'] in \
           [list(map(str, ss)) for ss in splits]


def test_file_splits(lexan, splittext_refs):
    f = splittext_refs[0]
    s = splittext_refs[1]
    i = SanskritObject(f, encoding=SLP1)
    graph = lexan.getSandhiSplits(i)
    assert graph is not None
    splits = graph.findAllPaths(max_paths=300, sort=False)
#     if s not in [list(map(str, ss)) for ss in splits]:
#         # Currently, this triggers a fallback to all_simple_paths
#         splits = graph.findAllPaths(max_paths=10000, sort=False)
    assert s in [list(map(str, ss)) for ss in splits]


def pytest_generate_tests(metafunc):
    test_count = get_testcount(metafunc.config)
    if 'splittext_refs' in metafunc.fixturenames:
        splittext_refs = get_splitstxt(test_count)
        metafunc.parametrize("splittext_refs", splittext_refs)
