'''
Created on Jul 7, 2017

@author: alvarna
'''
import pytest
import codecs
import os
import inspect
from sanskrit_parser.lexical_analyzer.sandhi import Sandhi
from sanskrit_parser.base.SanskritBase import SanskritObject, SLP1
import logging
import json

logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def sandhiobj():
    return Sandhi()

def test_sandhi_join(sandhiobj, join_reference):
    objs = map(lambda x:SanskritObject(x, encoding = SLP1), (join_reference[0]))
    joins = sandhiobj.join(*objs)
    assert join_reference[1] in joins, u"Join, {}, {}, {}, {}".format(*join_reference)

def test_sandhi_split(sandhiobj, split_reference):
    obj = SanskritObject(split_reference[1], encoding=SLP1)
    splits = sandhiobj.split_all(obj)
    assert split_reference[0] in splits, u"Split, {}, {}, {}, {}".format(*split_reference)

def load_reference_data(passing, failing):
    references = []
    base_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    directory = os.path.join(base_dir, "sandhi_test_data")
    
    with codecs.open(os.path.join(directory, passing), encoding="utf-8") as f:
        for line in f:
            test = json.loads(line)
            references.append((tuple(test["before"]), test["after"], test["filename"], test["linenum"]))
    
    with codecs.open(os.path.join(directory, failing), encoding="utf-8") as f:
        for line in f:
            test = json.loads(line)
            references.append(
                pytest.mark.xfail(
                    (tuple(test["before"]), test["after"], test["filename"], test["linenum"])
                    )
                )
    return references

def pytest_generate_tests(metafunc):
    if 'join_reference' in metafunc.fixturenames:
        join_references = load_reference_data("sandhi_join_passing.txt", "sandhi_join_failing.txt")
        metafunc.parametrize("join_reference", join_references)
    if 'split_reference' in metafunc.fixturenames:
        split_references = load_reference_data("sandhi_split_passing.txt", "sandhi_split_failing.txt")
        metafunc.parametrize("split_reference", split_references)
