from sanskrit_parser.generator.pratyaya import *
from sanskrit_parser.generator.dhatu import *
from sanskrit_parser.generator.pratipadika import *
from sanskrit_parser.base.sanskrit_base import SLP1, DEVANAGARI

from conftest import run_test, generate_vibhakti

import pytest
import logging

from manual_test import  test_list_slp1, test_list_devanagari, encoding

@pytest.mark.parametrize("tlst_d", test_list_devanagari)
def test_list_d(tlst_d, sutra_fixture):
    run_test(tlst_d, sutra_fixture, encoding=DEVANAGARI)

@pytest.mark.parametrize("tlst", test_list_slp1)
def test_list(tlst, sutra_fixture):
    run_test(tlst, sutra_fixture, encoding=SLP1)
