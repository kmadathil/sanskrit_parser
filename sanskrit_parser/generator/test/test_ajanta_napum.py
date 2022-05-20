# flake8: noqa
from conftest import run_test
from sanskrit_parser.generator.pratipadika import *
from sanskrit_parser.generator.sutras_yaml import sutra_list
from indic_transliteration import sanscript

def test_vibhakti_ajanta_napum(ajanta_napum):
      run_test(ajanta_napum, sutra_list, encoding=sanscript.DEVANAGARI)
