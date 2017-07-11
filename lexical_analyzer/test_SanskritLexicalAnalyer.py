#!/usr/bin/env python
# encoding: utf-8

import pytest
import SanskritLexicalAnalyzer
from base.SanskritBase import SanskritObject,SLP1

@pytest.fixture(scope="module")
def lexan():
    return SanskritLexicalAnalyzer.SanskritLexicalAnalyzer()

@pytest.fixture(scope="module")
def filetests():
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

def test_simple_split(lexan):
    # gaNeshannamAmi
    i=SanskritObject("gaReSannamAmi",encoding=SLP1)
    graph=lexan.getSandhiSplits(i)
    splits=graph.findAllPaths()
    assert [u'gaReSam', u'namAmi'] in splits

def test_medium_split(lexan):
    i=SanskritObject("budDaMSaraRaNgacCAmi",encoding=SLP1)
    graph=lexan.getSandhiSplits(i)
    splits=graph.findAllPaths()
    assert [u'budDam', u'SaraRam', u'gacCAmi'] in splits

def test_file_splits(lexan,filetests):
    for t in filetests:
        f = t[0]
        s = t[1]
        i=SanskritObject(f,encoding=SLP1)
        graph=lexan.getSandhiSplits(i)
        assert graph is not None
        splits=graph.findAllPaths(n_paths=1000)
        assert s in splits
       
