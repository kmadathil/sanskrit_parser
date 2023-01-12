# -*- coding: utf-8 -*-
# flake8: noqa
from conftest import check_vibhakti, generate_vibhakti, test_prakriya
from manual_list import test_list_slp1, test_list_devanagari
from sanskrit_parser import enable_console_logger, enable_file_logger
from vibhaktis_list import viBakti, prAtipadika, encoding

if __name__ == "__main__":
    import sys
    import codecs
    # Windows doesn't work correctly without this
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    import logging
    #logging.basicConfig(level=logging.INFO)
    # First we disable the root logger handlers
    rootlogger = logging.getLogger()
    for h in rootlogger.handlers:
        rootlogger.removeHandler(h)
    rootlogger.addHandler(logging.NullHandler())
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


