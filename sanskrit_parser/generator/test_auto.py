from sanskrit_parser.generator.pratyaya import *
from sanskrit_parser.generator.dhatu import *
from sanskrit_parser.generator.pratipadika import *
from sanskrit_parser.base.sanskrit_base import SLP1, DEVANAGARI

from sutras_yaml import sutra_list
from conftest import run_test, generate_vibhakti

import pytest
import logging

from manual_test import viBakti, prAtipadika, test_list_slp1, test_list_devanagari, encoding

@pytest.fixture
def sutra_fixture():
    return sutra_list
            
def test_vibhakti(vibhakti, sutra_fixture):
    run_test(vibhakti, sutra_fixture, encoding=DEVANAGARI)
    
def test_vibhakti_s(vibhakti_s, sutra_fixture):
    run_test(vibhakti, sutra_fixture, encoding=SLP1)

def test_manual_d(manual_d, sutra_fixture):
    run_test(manual_d, sutra_fixture, encoding=DEVANAGARI)

def test_manual(manual, sutra_fixture):
    run_test(manual, sutra_fixture, encoding=SLP1)

def pytest_generate_tests(metafunc):
    if 'vibhakti' in metafunc.fixturenames:
        vibhakti_list = []
        for v in viBakti:
            if (v in encoding) and (encoding[v]=="SLP1"):
                pass
            else:
                vibhakti_list.extend(generate_vibhakti(prAtipadika[v],
                                                       viBakti[v]))
        metafunc.parametrize("vibhakti", vibhakti_list)
    if 'vibhakti_s' in metafunc.fixturenames:
        vibhakti_s_list = [] 
        for v in viBakti:
            if (v in encoding) and (encoding[v]=="SLP1"):
                vibhakti_s_list.extend(generate_vibhakti(prAtipadika[v],
                                                         viBakti[v], SLP1))
        metafunc.parametrize("vibhakti_s", vibhakti_s_list)
    if 'manual_d' in metafunc.fixturenames:
         metafunc.parametrize("manual_d", test_list_devanagari)
    if 'manual' in metafunc.fixturenames:
         metafunc.parametrize("manual", test_list_slp1)
         
