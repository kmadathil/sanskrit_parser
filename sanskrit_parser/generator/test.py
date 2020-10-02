# -*- coding: utf-8 -*-
from sanskrit_parser import enable_console_logger, enable_file_logger
from sanskrit_parser.base.sanskrit_base import SLP1
import sanskrit_parser.generator.sutra as sutra
from sanskrit_parser.generator.paninian_object import PaninianObject
from sanskrit_parser.generator.prakriya import Prakriya

import logging
#logging.basicConfig(level=logging.INFO)
enable_console_logger()
enable_file_logger(level=logging.DEBUG)

test_list = [
    ("gaRa", "upadeSaH", "gaRopadeSaH"),
    ("rAma", "eti", "rAmEti"),
    ("rAma", "iti", "rAmeti"),
    ("tyaktvA", "uttizTa", "tyaktvottizTa"),
    ("tava", "ozTaH", "tavOzTaH"),
    ("deva", "fzi", "devarzi"),
    ("gavi", "asmAkam", "gavyasmAkam"),
    ("kavI", "etau", "kavyetau"),
    ("gavi", "iha", "gavIha"),
    ("kavI", "iha", "kavIha"),
    ("kavO", "asmAkam", "kavAvasmAkam"),
    ("AgacCa", "atra", "AgacCAtra"),
    ("yAne", "eti", "yAnaeti"),
    ("yAne", "atra", "yAnetra"),
    ("yAne", "AgacCati", "yAnaAgacCati"),
    ("vizRo", "ava", "vizRova"),
    ("haras", "Sete", "haraSSete"),
    ("Bavat", "caraRam", "BavaccaraRam"),
    # Fixme: Non pada
    #("praS", "nas", "praSnas"),
    ("rAmas", "zazQa", "rAmazzazQa"),
    ("rAmas", "wIkate", "rAmazwIkate"),
    ("sarpiz", "tamam", "sarpizwamam"),
    ("marut", "wIkate", "maruwwIkate"),
    ("SuBam", "karoti", "SuBaNkaroti"),
    ("vAk", "arTO", "vAgarTO"),
    ("goDuk", "awati", "goDugawati"),
    ("goDuk", "girati", "goDuggirati"),
    ("virAw", "vadati", "virAqvadati"),
    ]

test_list_d = [
    ("मरुत्", "टीकते", "मरुट्टीकते"),
    ("मधुलिट्", "तरति", "मधुलिट्तरति"),
    ("मरुत्", "षष्ठः", "मरुत्षष्ठः"),
    ("सन्", "षष्ठः", "सन्षष्ठः"),
    ("षण्", "नाम्", "षण्णाम्"),
    ("वाग्", "मुखम्", "वाङ्मुखम्"),
     ("षड्", "मुखम्", "षण्मुखम्"),
     ("एतद्", "मुरारि", "एतन्मुरारि"),
     ("त्रिष्टुब्", "नमति", "त्रिष्टुम्नमति"),
     ("वाग्", "चलति", "वाक्चलति"),
     ("त्रिष्टुब्", "छन्दः", "त्रिष्टुप्छन्दः"),
     ("अस्", "ति", "अस्ति"),
]

def test_prakriya(sutra_list):
    for s in test_list:
        l = PaninianObject(s[0], SLP1)
        r = PaninianObject(s[1], SLP1)
        p = Prakriya(sutra_list,((l, r)))
        p.execute()
        p.describe()
        # Only one output
        o = p.output()
        assert ("".join([_o.canonical() for _o in list(o)])==s[2])
    for s in test_list_d:
        l = PaninianObject(s[0])
        r = PaninianObject(s[1])
        p = Prakriya(sutra_list,((l, r)))
        p.execute()
        p.describe()
        # Only one output
        o = p.output()
        assert ("".join([_o.devanagari() for _o in list(o)])==s[2]), \
        f"{''.join([_o.devanagari() for _o in list(o)])}, {s[2]}"

from sandhi_yaml import sutra_list
test_prakriya(sutra_list)


