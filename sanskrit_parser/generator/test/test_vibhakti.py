from sanskrit_parser.generator.pratyaya import *
from sanskrit_parser.generator.dhatu import *
from sanskrit_parser.generator.pratipadika import *
from sanskrit_parser.base.sanskrit_base import SLP1, DEVANAGARI
from sanskrit_parser.generator.sutras_yaml import sutra_list

from conftest import run_test

import pytest
import logging


#def test_vibhakti(vibhakti, sutra_fixture):
#     run_test(vibhakti, sutra_fixture, encoding=DEVANAGARI)
    
def test_vibhakti_s(vibhakti_s):
     run_test(vibhakti_s, sutra_list, encoding=SLP1)

