from sanskrit_parser.generator.pratyaya import *  # noqa: F403, F401
from sanskrit_parser.generator.dhatu import *  # noqa: F403, F401
from sanskrit_parser.generator.pratipadika import *  # noqa: F403, F401
from indic_transliteration import sanscript
from sanskrit_parser.generator.sutras_yaml import SutraFactory
sutra_list = SutraFactory()

from conftest import run_test


def test_vibhakti_ajanta_stri(ajanta_stri):
    run_test(ajanta_stri, sutra_list, encoding=sanscript.DEVANAGARI)
