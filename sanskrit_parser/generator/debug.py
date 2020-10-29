# -*- coding: utf-8 -*-
from sanskrit_parser import enable_console_logger, enable_file_logger
from sanskrit_parser.base.sanskrit_base import SLP1, DEVANAGARI
import sanskrit_parser.generator.sutra as sutra
from sanskrit_parser.generator.paninian_object import PaninianObject
from sanskrit_parser.generator.prakriya import Prakriya, PrakriyaVakya
from sanskrit_parser.generator.pratyaya import *
from sanskrit_parser.generator.dhatu import *
from sanskrit_parser.generator.pratipadika import *
from conftest import run_test, check_vibhakti, generate_vibhakti, test_prakriya

import logging
#logging.basicConfig(level=logging.INFO)
enable_console_logger()
enable_file_logger(level=logging.DEBUG)

test_list = [
]

test_list_d = [
]


viBakti = {}
prAtipadika = {}

prAtipadika["rAma"] = rAma
viBakti["rAma"] = [
    ["रामः", "रामौ", "रामाः"],
    ["रामम्", "रामौ", "रामान्"],
    ["रामेण", "रामाभ्याम्", "रामैः"],
    ["रामाय", "रामाभ्याम्", "रामेभ्यः"],
    [["रामात्", "रामाद्"], "रामाभ्याम्", "रामेभ्यः"],
    ["रामस्य", "रामयोः", "रामाणाम्"],
    ["रामे", "रामयोः", "रामेषु"],
    ["राम", "रामौ", "रामाः"],
]

prAtipadika["sarva"] = sarva
viBakti["sarva"] = [
    ["सर्वः", "सर्वौ", "सर्वे"],
    ["सर्वम्", "सर्वौ", "सर्वान्"],
    ["सर्वेण", "सर्वाभ्याम्", "सर्वैः"],
    ["सर्वस्मै", "सर्वाभ्याम्", "सर्वेभ्यः"],
    [["सर्वस्मात्", "सर्वस्माद्"], "सर्वाभ्याम्", "सर्वेभ्यः"],
    ["सर्वस्य", "सर्वयोः", "सर्वेषाम्"], 
    ["सर्वस्मिन्", "सर्वयोः", "सर्वेषु "],
]


from sutras_yaml import sutra_list

for v in viBakti:
    check_vibhakti(generate_vibhakti(prAtipadika[v], viBakti[v]), sutra_list)
test_prakriya(sutra_list, test_list, test_list_d)

