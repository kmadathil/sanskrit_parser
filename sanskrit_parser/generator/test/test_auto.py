from sanskrit_parser.generator.pratyaya import *
from sanskrit_parser.generator.dhatu import *
from sanskrit_parser.generator.pratipadika import *
from sanskrit_parser.base.sanskrit_base import SLP1, DEVANAGARI

from conftest import run_test, generate_vibhakti

import pytest
import logging

from manual_test1 import viBakti, prAtipadika, test_list_slp1, test_list_devanagari, encoding

            
def test_vibhakti(vibhakti, sutra_fixture):
    run_test(vibhakti, sutra_fixture, encoding=DEVANAGARI)
    
def test_vibhakti_s(vibhakti_s, sutra_fixture):
    run_test(vibhakti, sutra_fixture, encoding=SLP1)

def test_manual_d(manual_d, sutra_fixture):
    run_test(manual_d, sutra_fixture, encoding=DEVANAGARI)

def test_manual(manual, sutra_fixture):
    run_test(manual, sutra_fixture, encoding=SLP1)
