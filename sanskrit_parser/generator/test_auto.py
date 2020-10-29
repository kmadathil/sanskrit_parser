from sanskrit_parser.generator.pratyaya import *
from sanskrit_parser.generator.dhatu import *
from sanskrit_parser.generator.pratipadika import *
from sanskrit_parser.base.sanskrit_base import SLP1, DEVANAGARI

from sutras_yaml import sutra_list
from conftest import run_test

#import pytest

viBakti = {}


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


# @pytest.fixture
# def sutra_fixture():
#     return sutra_list

def check_vibhakti(pratipadika, vibhaktis, sutra_list):
    t = []
    for ix, pv in enumerate(vibhaktis):
        #print(f"test vibakti {ix} {pv}")
        for jx, pvv in enumerate(pv):
            #print(f"test {jx} {pvv}")
            if isinstance(pvv, str):
                _pvv = pvv+avasAna.transcoded(DEVANAGARI)
            else:
                _pvv = [x+avasAna.transcoded(DEVANAGARI) for x in pvv]
            t.append([(pratipadika, sups[ix][jx]), avasAna, _pvv])
    print(t)
    for s in t:
        run_test(s, sutra_list, encoding=DEVANAGARI)
            
    
from sanskrit_parser import enable_console_logger, enable_file_logger
import logging
#logging.basicConfig(level=logging.INFO)
enable_console_logger()
enable_file_logger(level=logging.DEBUG)

check_vibhakti(rAma, viBakti["rAma"], sutra_list)
        
