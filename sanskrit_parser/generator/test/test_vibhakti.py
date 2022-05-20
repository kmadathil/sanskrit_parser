from sanskrit_parser.generator.pratyaya import *  # noqa: F403, F401
from sanskrit_parser.generator.dhatu import *  # noqa: F403, F401
from sanskrit_parser.generator.pratipadika import *  # noqa: F403, F401
from indic_transliteration import sanscript
from sanskrit_parser.generator.sutras_yaml import sutra_list
from conftest import run_test


def test_vibhakti_s(vibhakti_s):
    run_test(vibhakti_s, sutra_list, encoding=sanscript.SLP1)
