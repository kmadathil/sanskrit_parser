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


def test_vibhakti_ajanta_pum(ajanta_pum):
      run_test(ajanta_pum, sutra_list, encoding=DEVANAGARI)
