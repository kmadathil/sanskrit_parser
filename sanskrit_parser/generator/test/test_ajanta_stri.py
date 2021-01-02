from sanskrit_parser.generator.pratyaya import *
from sanskrit_parser.generator.dhatu import *
from sanskrit_parser.generator.pratipadika import *
from sanskrit_parser.base.sanskrit_base import SLP1, DEVANAGARI

from conftest import run_test

import pytest
import logging


def test_vibhakti_ajanta_stri(ajanta_stri, sutra_fixture):
      run_test(ajanta_stri, sutra_fixture, encoding=DEVANAGARI)
