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
    (ava, (AN, "ihi"), "avehi"),
    # [rAjan, wA, "rAjYA"], # 6.4.134
    # [yUza, wA, ["yUzRA", "yUzeRa"]], # 6.1.63, 6.4.134
    # [rAjan, ByAm, "rAjaByAm"], # 6.2.7
    # [yUza, ByAm, ["yUzaByAm", "yUzAByAm"]], # 6.2.7
    # [rAjan, Ni, ["rAjani", "rAjYi"]], # 6.4.136
    # [yUza, Ni, ["yUzaRi", "yUzRi", "yUze"]], # 6.1.63, 6.4.136
]

test_list_d = [
]


viBakti = {}
prAtipadika = {}

# prAtipadika["rAma"] = rAma
# viBakti["rAma"] = [
#     ["रामः", "रामौ", "रामाः"],
#     ["रामम्", "रामौ", "रामान्"],
#     ["रामेण", "रामाभ्याम्", "रामैः"],
#     ["रामाय", "रामाभ्याम्", "रामेभ्यः"],
#     [["रामात्", "रामाद्"], "रामाभ्याम्", "रामेभ्यः"],
#     ["रामस्य", "रामयोः", "रामाणाम्"],
#     ["रामे", "रामयोः", "रामेषु"],
#     ["राम", "रामौ", "रामाः"],
# ]

# prAtipadika["sarva"] = sarva
# viBakti["sarva"] = [
#     ["सर्वः", "सर्वौ", "सर्वे"],
#     ["सर्वम्", "सर्वौ", "सर्वान्"],
#     ["सर्वेण", "सर्वाभ्याम्", "सर्वैः"],
#     ["सर्वस्मै", "सर्वाभ्याम्", "सर्वेभ्यः"],
#     [["सर्वस्मात्", "सर्वस्माद्"], "सर्वाभ्याम्", "सर्वेभ्यः"],
#     ["सर्वस्य", "सर्वयोः", "सर्वेषाम्"], 
#     ["सर्वस्मिन्", "सर्वयोः", "सर्वेषु "],
# ]

# prAtipadika["pAda"] = pAda
# viBakti["pAda"] = [
#     ["पादः", "पादौ", "पादाः"],
#     ["पादम्", "पादौ", ["पादान्", "पदः"]],
#     [["पादेन", "पदा"], ["पादाभ्याम्", "पद्भ्याम्"], ["पादैः", "पद्भिः"]],
#     [["पादाय", "पदे"], ["पादाभ्याम्", "पद्भ्याम्"], ["पादेभ्यः", "पद्भ्यः"]],
#     [["पादात्", "पादाद्", "पदः"], ["पादाभ्याम्", "पद्भ्याम्"], ["पादेभ्यः", "पद्भ्यः"]],
#     [["पादस्य", "पदः"], ["पादयोः", "पदोः"], ["पादानाम्", "पदाम्"]],
#     [["पादे", "पदि"], ["पादयोः", "पदोः"], ["पादेषु", "पत्सु"]],
#     ["पादः", "पादौ", "पादाः"],
# ]

# prAtipadika["yUza"] = yUza
# viBakti["yUza"] = [
#     ["यूषः", "यूषौ", "यूषाः"],
#     ["यूषम्", "यूषौ", ["यूषान्", "यूष्णः"]],
#     [["यूषेण", "यूष्णा"], ["यूषाभ्याम्", "यूषभ्याम्"], ["यूषैः", "यूषभिः"]],
#     [["यूषाय", "यूष्णे"], ["यूषाभ्याम्", "यूषभ्याम्"], ["यूषेभ्यः", "यूषभ्यः"]],
#     [["यूषात्", "यूषाद्", "यूष्णः"], ["यूषाभ्याम्", "यूषभ्याम्"], ["यूषेभ्यः", "यूषभ्यः"]],
#     [["यूषस्य", "यूष्णः"], ["यूषयोः", "यूष्णोः"], ["यूषाणाम्", "यूष्णाम्"]],
#     [["यूषे", "यूषणि", "यूष्णि"], ["यूषयोः", "यूष्णोः"], ["यूषेषु", "यूषसु"]],
#     ["यूष", "यूषौ", "यूषाः"],
# ]

prAtipadika["hari"] = hari
viBakti["hari"] = [
    ["हरिः", "हरी", "हरयः"],
    ["हरिम्", "हरी", "हरीन्"],
    ["हरिणा", "हरिभ्याम्", "हरिभिः"],
    ["हरये", "हरिभ्याम्", "हरिभ्यः"],
    ["हरेः", "हरिभ्याम्", "हरिभ्यः"],
    ["हरेः", "हर्योः", "हरीणाम्"],
    ["हरौ", "हर्योः", "हरिषु"],
    ["हरे", "हरी", "हरयः"],
]

from sutras_yaml import sutra_list

test_prakriya(sutra_list, test_list, test_list_d)
for v in viBakti:
    check_vibhakti(generate_vibhakti(prAtipadika[v], viBakti[v]), sutra_list)


