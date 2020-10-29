# -*- coding: utf-8 -*-
from sanskrit_parser import enable_console_logger, enable_file_logger
from sanskrit_parser.base.sanskrit_base import SLP1, DEVANAGARI
import sanskrit_parser.generator.sutra as sutra
from sanskrit_parser.generator.paninian_object import PaninianObject
from sanskrit_parser.generator.prakriya import Prakriya, PrakriyaVakya
from sanskrit_parser.generator.pratyaya import *
from sanskrit_parser.generator.dhatu import *
from sanskrit_parser.generator.pratipadika import *
from conftest import run_test

import logging
#logging.basicConfig(level=logging.INFO)
enable_console_logger()
enable_file_logger(level=logging.DEBUG)

test_list = [
    (rAma, "ina", "rAmeRa"),
]

test_list_d = [
    ((rAma, su), avasAna, "रामः ।"), 
    (rAma, O, "रामौ"),
    ((rAma, jas), avasAna, "रामाः ।"),
    (rAma, su2, "राम"),
    (rAma, am, "रामम्"),
    (rAma, O2, "रामौ"),
    (rAma, Sas, "रामान्"),
    (rAma, wA, "रामेण"),
    (rAma,  ByAm, "रामाभ्याम्"),
    ((rAma,  Bis), avasAna, "रामैः ।"),
    (rAma,  Ne, "रामाय"),
    (rAma,  ByAm2, " रामाभ्याम्"),
    ((rAma,  Byas), avasAna, "रामेभ्यः ।"),
    ((rAma, Nasi), avasAna, ["रामात् ।", "रामाद् ।"]),
    (rAma,  ByAm3, " रामाभ्याम्"),
    ((rAma,  Byas2), avasAna, "रामेभ्यः ।"),
    (rAma, Nas, "रामस्य"),
    ((rAma,  os), avasAna, "रामयोः ।"),
    (rAma, Am, "रामाणाम्"),
    ((rAma,  os2), avasAna, "रामयोः ।"),
    (rAma, sup, "रामेषु"),
    ]

def test_prakriya(sutra_list):
    for s in test_list:
        run_test(s, sutra_list, SLP1)
    for s in test_list_d:
        run_test(s, sutra_list, DEVANAGARI)
        
from sutras_yaml import sutra_list
test_prakriya(sutra_list)

