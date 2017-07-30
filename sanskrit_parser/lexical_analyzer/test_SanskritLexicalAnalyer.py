#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import pytest
import SanskritLexicalAnalyzer
from base.SanskritBase import SanskritObject,SLP1,DEVANAGARI

@pytest.fixture(scope="module")
def lexan():
    return SanskritLexicalAnalyzer.SanskritLexicalAnalyzer()

@pytest.fixture(params=[True, False], ids=["Internal Sandhi splitter", "Sandhi module"])
def use_internal_sandhi_splitter(request):
    return request.param


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
    ts=lexan.getInriaLexicalTags(i)
    assert ts == [('gaReSa', set(['na', 'mas', 'sg', 'nom']))]

def test_simple_split(lexan,use_internal_sandhi_splitter):
    # gaNeshannamAmi
    i=SanskritObject("gaReSannamAmi",encoding=SLP1)
    graph=lexan.getSandhiSplits(i,use_internal_sandhi_splitter)
    splits=graph.findAllPaths()
    assert [u'gaReSam', u'namAmi'] in splits

def test_medium_split(lexan,use_internal_sandhi_splitter):
    i=SanskritObject("budDaMSaraRaNgacCAmi",encoding=SLP1)
    graph=lexan.getSandhiSplits(i,use_internal_sandhi_splitter)
    splits=graph.findAllPaths()
    assert [u'budDam', u'SaraRam', u'gacCAmi'] in splits

def test_file_splits(lexan,use_internal_sandhi_splitter, splittext_refs):
    f = splittext_refs[0]
    s = splittext_refs[1]
    i=SanskritObject(f,encoding=SLP1)
    graph=lexan.getSandhiSplits(i, use_internal_sandhi_splitter)
    assert graph is not None
    splits=graph.findAllPaths(max_paths=1000,sort=False)
    if s not in splits:
        # Currently, this triggers a fallback to all_simple_paths
        splits=graph.findAllPaths(max_paths=10000,sort=False)
    assert s in splits
    
def pytest_generate_tests(metafunc):
    if 'splittext_refs' in metafunc.fixturenames:
        splittext_refs = get_splitstxt()
        metafunc.parametrize("splittext_refs", splittext_refs)

