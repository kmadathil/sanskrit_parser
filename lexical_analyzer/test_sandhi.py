'''
Created on Jul 7, 2017

@author: alvarna
'''
import pytest
import codecs
import os
import inspect
from sandhi import Sandhi
from base.SanskritBase import SanskritObject, DEVANAGARI, SLP1
import logging
import re

# logging.basicConfig(filename="sandhi.log", filemode = "wb", level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def sandhiobj():
    return Sandhi()

def test_sandhi_join(sandhiobj, sandhi_reference):
    objs = map(lambda x:SanskritObject(x, encoding = SLP1), (sandhi_reference[0]))
    joins = sandhiobj.join(*objs)
    assert sandhi_reference[1] in joins

def test_sandhi_split(sandhiobj, sandhi_reference):
    obj = SanskritObject(sandhi_reference[1], encoding=SLP1)
#     splits = set()
#     start = len(sandhi_reference[0][0]) - 2
#     stop = min(len(sandhi_reference[0][0])+1, len(sandhi_reference[1]))
#     for i in range(start, stop):
#     for i in range(len(sandhi_reference[1])):
#         split = sandhiobj.split_at(obj, i)
#         if split:
#             assert splits.isdisjoint(split)
#             splits |= split
    splits = sandhiobj.split_all(obj)
    assert sandhi_reference[0] in splits

def load_reference_data():
    sandhi_references = []
    base_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    directory = os.path.join(base_dir, "sandhi_test_data")
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            sandhi_references.extend(load_reference_data_from_file(os.path.join(directory, filename)))
    return sandhi_references

def load_reference_data_from_file(filename):
    sandhi_references = []
    basename = os.path.basename(filename)
    logger.debug("Processing tests from file %s", basename)
    with codecs.open(filename, "rb", 'utf-8') as f:
        for linenum, line in enumerate(f):
            line = line.strip()
            if line.startswith('#') or line == '':
                continue
            ref = SanskritObject(line).transcoded(SLP1)
            if "=>" in line:
                after, b = map(unicode.strip, ref.split("=>"))
            elif "=" in line:
                b, after = map(unicode.strip, ref.split("="))
            else:
                continue
            before = map(unicode.strip, b.split('+'))
            #before = map(lambda x: re.sub("\W+", "", x), b.split('+'))
            if len(before) == 2:
                before[0] = re.sub("\W+", "", before[0])
                before[1] = re.sub("\W+", "", before[1])
                after = re.sub("\W+", "", after)
                sandhi_references.append((tuple(before), after, basename, linenum+1))
#     print sandhi_references
    return sandhi_references

def pytest_generate_tests(metafunc):
    if 'sandhi_reference' in metafunc.fixturenames:
        sandhi_references = load_reference_data()
        metafunc.parametrize("sandhi_reference", sandhi_references)
