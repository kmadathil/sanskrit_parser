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
     ("तत्", "लीनः", "तल्लीनः"),
     ("प्रत्यङ्", "आत्मा", "प्रत्यङ्ङात्मा"),
     ("सुगण्", "ईशः", "सुगण्णीशः"),
     ("अस्मिन्", "एव", "अस्मिन्नेव"),
     ("वाग्", "हरि", "वाग्घरि"),
     ("अज्", "हलौ", "अज्झलौ"),
     ("मधुलिड्", "हसति", "मधुलिड्ढसति"),
     ("तद्", "हितम्", "तद्धितम्"),
     ("त्रिष्टुब्", "हि", "त्रिष्टुब्भि"),
     ("तद्", "शेते", "तच्छेते"),
     ("मधुलिड्", "शेते", "मधुलिट्छेते"),
     ("त्रिष्टुब्", "शेते", "त्रिष्टुप्छेते"),
     ("तद्", "श्लोकेन", "तच्छ्लोकेन"),
     ("तत्", "जयते", "तज्जयते"),
     # Fixme - tugAgama requires two runs - need prakriti pratyaya working
     #("सन्", "शम्भुः", "सञ्छम्भुः"),
]

def test_prakriya(sutra_list):
    def _test_c(o, s):
        return ("".join([_o.canonical() for _o in list(o)])==s[2])
    def _test_d(o, s):
        return ("".join([_o.devanagari() for _o in list(o)])==s[2])
    for s in test_list:
        l = PaninianObject(s[0], SLP1)
        r = PaninianObject(s[1], SLP1)
        p = Prakriya(sutra_list,((l, r)))
        p.execute()
        p.describe()
        o = p.output()
        # One of the outputs
        assert any([_test_c(_o,s) for _o in o])
    for s in test_list_d:
        l = PaninianObject(s[0])
        r = PaninianObject(s[1])
        p = Prakriya(sutra_list,((l, r)))
        p.execute()
        p.describe()
        # Only one output
        o = p.output()
        assert any([_test_d(_o,s) for _o in o])

from sandhi_yaml import sutra_list
test_prakriya(sutra_list)


