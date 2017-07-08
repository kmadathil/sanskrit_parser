'''
Created on Jul 7, 2017

@author: alvarna
'''
import pytest
import codecs
import os
import inspect
from sandhi import Sandhi
from indic_transliteration import sanscript
import logging

# logging.basicConfig(filename="sandhi.log", filemode = "wb", level=logging.DEBUG)

@pytest.fixture(scope="module")
def sandhiobj():
    return Sandhi()

def test_sandhi_join(sandhiobj, sandhi_reference):
    joins = sandhiobj.join(*(sandhi_reference[0]))
    assert sandhi_reference[1] in joins

def test_sandhi_split(sandhiobj, sandhi_reference):
    splits = sandhiobj.split_at(sandhi_reference[1], len(sandhi_reference[0][0]))
    # In some cases the split may need to happen at len -1
    splits1 = sandhiobj.split_at(sandhi_reference[1], len(sandhi_reference[0][0])-1)
    if splits:
        splits.extend(splits1)
    else:
        splits = splits1
    assert sandhi_reference[0] in splits

def load_reference_data():
    sandhi_references = []
    base_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    filename = os.path.join(base_dir, "sandhi_test_data/refs.txt")
    with codecs.open(filename, "rb", 'utf-8') as f:
        for line in f:
            if "=>" in line:
                ref = sanscript.transliterate(line, sanscript.DEVANAGARI, sanscript.SLP1)
                after, b = map(unicode.strip, ref.split("=>"))
                before = map(unicode.strip, b.split('+'))
                sandhi_references.append((before, after))
            elif "=" in line:
                ref = sanscript.transliterate(line, sanscript.DEVANAGARI, sanscript.SLP1)
                b, after = map(unicode.strip, ref.split("="))
                before = map(unicode.strip, b.split('+'))
                sandhi_references.append((before, after))
#     print sandhi_references
    return sandhi_references

def pytest_generate_tests(metafunc):
    if 'sandhi_reference' in metafunc.fixturenames:
        sandhi_references = load_reference_data()
        metafunc.parametrize("sandhi_reference", sandhi_references)
