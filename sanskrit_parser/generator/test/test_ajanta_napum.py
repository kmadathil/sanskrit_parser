# flake8: noqa
from conftest import run_test, sutra_list
from sanskrit_parser.generator.pratipadika import *

from indic_transliteration import sanscript

def test_vibhakti_ajanta_napum(ajanta_napum):
      run_test(ajanta_napum, sutra_list, encoding=sanscript.DEVANAGARI)
