# flake8: noqa
from sanskrit_parser.generator.pratyaya import *
from sanskrit_parser.generator.dhatu import *
from sanskrit_parser.generator.pratipadika import *
from sanskrit_parser.base.sanskrit_base import SLP1, DEVANAGARI
from sanskrit_parser.generator.pratipadika import *
from sanskrit_parser.generator.sutras_yaml import sutra_list

from conftest import run_test

import pytest
import logging


def test_vibhakti_halanta_pum(halanta_pum):
      run_test(halanta_pum, sutra_list, encoding=DEVANAGARI)

def test_vibhakti_halanta_stri(halanta_stri):
      run_test(halanta_stri, sutra_list, encoding=DEVANAGARI)

def test_vibhakti_halanta_napum(halanta_napum):
      run_test(halanta_napum, sutra_list, encoding=DEVANAGARI)
