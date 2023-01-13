# flake8: noqa
from sanskrit_parser.generator.pratyaya import *
from sanskrit_parser.generator.dhatu import *
from sanskrit_parser.generator.pratipadika import *
from indic_transliteration import sanscript
from sanskrit_parser.generator.pratipadika import *
from sanskrit_parser.generator.sutras_yaml import SutraFactory
sutra_list = SutraFactory()

from conftest import run_test

import pytest
import logging


def test_vibhakti_halanta_pum(halanta_pum):
      run_test(halanta_pum, sutra_list, encoding=sanscript.DEVANAGARI)

def test_vibhakti_halanta_stri(halanta_stri):
      run_test(halanta_stri, sutra_list, encoding=sanscript.DEVANAGARI)

def test_vibhakti_halanta_napum(halanta_napum):
      run_test(halanta_napum, sutra_list, encoding=sanscript.DEVANAGARI)
