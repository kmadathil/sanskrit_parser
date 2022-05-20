# flake8: noqa
from sanskrit_parser.generator.pratyaya import *
from sanskrit_parser.generator.dhatu import *
from sanskrit_parser.generator.pratipadika import *
from sanskrit_parser.generator.pratipadika import *
from sanskrit_parser.generator.sutras_yaml import sutra_list
from indic_transliteration import sanscript
from conftest import run_test

import pytest
import logging


def test_vibhakti_ajanta_pum(ajanta_pum):
      run_test(ajanta_pum, sutra_list, encoding=sanscript.DEVANAGARI)
