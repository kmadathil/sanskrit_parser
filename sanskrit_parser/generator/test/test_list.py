# flake8: noqa
from sanskrit_parser.generator.pratyaya import *
from sanskrit_parser.generator.dhatu import *
from sanskrit_parser.generator.pratipadika import *
from indic_transliteration import sanscript
from sanskrit_parser.generator.sutras_yaml import sutra_list

from conftest import run_test, generate_vibhakti

import pytest
import logging

from manual_list import  test_list_slp1, test_list_devanagari

@pytest.mark.parametrize("tlst_d", test_list_devanagari)
def test_list_d(tlst_d):
    run_test(tlst_d, sutra_list, encoding=sanscript.DEVANAGARI)

@pytest.mark.parametrize("tlst", test_list_slp1)
def test_list(tlst):
    run_test(tlst, sutra_list, encoding=sanscript.SLP1)
