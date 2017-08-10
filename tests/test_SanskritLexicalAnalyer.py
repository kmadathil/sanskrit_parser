#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import pytest
from sanskrit_parser.lexical_analyzer.SanskritLexicalAnalyzer import SanskritLexicalAnalyzer
from sanskrit_parser.base.SanskritBase import SanskritObject,SLP1,DEVANAGARI

@pytest.fixture(scope="module")
def lexan():
    return SanskritLexicalAnalyzer()

def get_splitstxt():
    fs = []
    with open("test_data_SanskritLexicalAnalyzer/splits.txt") as f:
        for l in f:
            l = l.strip()
            if l and l[0] != '#':
                full,split=l.split('=')
                full=unicode(full.strip(),'utf-8')
                split=split.strip()
                splits=map(lambda x: unicode(x,'utf-8'),split.split(' '))
                fs.append((full,splits))
    return fs


def test_simple_tag(lexan):
    # gaNeshaH
    i=SanskritObject("gaReSas",encoding=SLP1)
    ts=lexan.getLexicalTags(i)
    assert [(ts[0][0],set(map(str,ts[0][1])))] == [('gaReSa', set(['puMlliNgam', 'praTamAviBaktiH', 'ekavacanam']))]


def test_simple_split(lexan):
    # gaNeshannamAmi
    i=SanskritObject("gaReSannamAmi",encoding=SLP1)
    graph=lexan.getSandhiSplits(i)
    splits=graph.findAllPaths()
    assert [u'gaReSam', u'namAmi'] in [map(str,ss) for ss in splits]

def test_medium_split(lexan):
    i=SanskritObject("budDaMSaraRaNgacCAmi",encoding=SLP1)
    graph=lexan.getSandhiSplits(i)
    splits=graph.findAllPaths()
    assert [u'budDam', u'SaraRam', u'gacCAmi'] in [map(str,ss) for ss in splits]

def test_file_splits(lexan, splittext_refs):
    f = splittext_refs[0]
    s = splittext_refs[1]
    i=SanskritObject(f,encoding=SLP1)
    graph=lexan.getSandhiSplits(i)
    assert graph is not None
    splits=graph.findAllPaths(max_paths=1000,sort=False)
    if s not in splits:
        # Currently, this triggers a fallback to all_simple_paths
        splits=graph.findAllPaths(max_paths=10000,sort=False)
    assert s in [map(str,ss) for ss in splits]
    
def pytest_generate_tests(metafunc):
    if 'splittext_refs' in metafunc.fixturenames:
        splittext_refs = get_splitstxt()
        metafunc.parametrize("splittext_refs", splittext_refs)

