# -*- coding: utf-8 -*-
# flake8: noqa
from sanskrit_parser import enable_console_logger, enable_file_logger
from sanskrit_parser.base.sanskrit_base import SLP1, DEVANAGARI
import sanskrit_parser.generator.sutra as sutra
from sanskrit_parser.generator.paninian_object import PaninianObject
from sanskrit_parser.generator.prakriya import Prakriya, PrakriyaVakya
from sanskrit_parser.generator.pratyaya import *
from sanskrit_parser.generator.dhatu import *
from sanskrit_parser.generator.pratipadika import *
from conftest import run_test, check_vibhakti, generate_vibhakti, test_prakriya
from vibhaktis_list import viBakti, prAtipadika, encoding
from manual_list import  test_list_slp1, test_list_devanagari

if __name__ == "__main__":
    import logging
    #logging.basicConfig(level=logging.INFO)
    enable_console_logger()
    enable_file_logger(level=logging.DEBUG)
    from sanskrit_parser.generator.sutras_yaml import sutra_list

    test_prakriya(sutra_list, test_list_slp1, test_list_devanagari)
    for v in viBakti:
        if v in encoding:
            check_vibhakti(generate_vibhakti(prAtipadika[v], viBakti[v],
                                             encoding[v]), sutra_list, encoding[v])
        else:
            check_vibhakti(generate_vibhakti(prAtipadika[v], viBakti[v]),
                           sutra_list)


