# -*- coding: utf-8 -*-
from sanskrit_parser import enable_console_logger, enable_file_logger
from sanskrit_parser.base.sanskrit_base import SLP1
import sanskrit_parser.generator.sutra as sutra
from sanskrit_parser.generator.paninian_object import PaninianObject
from sanskrit_parser.generator.prakriya import Prakriya, PrakriyaVakya

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
    ("camU", "ASraya", "camvASraya"),
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
    # Non pada
    ("praS*", "nas", "praSnas"),
    ("rAmas", "zazQa", "rAmazzazQa"),
    ("rAmas", "wIkate", "rAmazwIkate"),
    ("sarpiz", "tamam", "sarpizwamam"),
    ("marut", "wIkate", "maruwwIkate"),
    ("SuBam", "karoti", "SuBaNkaroti"),
    ("vAk", "arTO", "vAgarTO"),
    ("goDuk", "awati", "goDugawati"),
    ("goDuk", "girati", "goDuggirati"),
    ("virAw", "vadati", "virAqvadati"),
    ("kavis", "asti", "kavirasti"),
    ("havis", "vartate", "havirvartate"),
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
     ("रामः", "तरति", "रामस्तरति"),
     ("बालः", "थूकरोति", "बालस्थूकरोति"),
     ("हरिः", "चलति", "हरिश्चलति"),
     ("पयः", "क्षीरम्", "पयःक्षीरम्"),
     ("कः", "त्सरुः", "कःत्सरुः"),
     ("हरिस्", "शेते", "हरिःशेते"),
     ("हरिस्", "शेते", "हरिश्शेते"),
     ("रामस्", "कः", "रामःकः"),
     ("रामस्", "खनति", "रामःखनति"),
     ("रामस्", "पातुः", "रामःपातुः"),
     ("वृक्षस्", "फलतु", "वृक्षःफलतु"),
     ("रामस्", "अस्ति", "रामोस्ति"),
    ("रामस्", "गच्छति", "रामोगच्छति"),
    ('भोस्',  'देवाः', "भोदेवाः"),
    ('भगोस्',  'मनुष्याः', "भगोमनुष्याः"),
    ('अघोस्',  'राक्षसाः', "अघोराक्षसाः"),
    ('देवास्',  'गच्छन्ति', "देवागच्छन्ति"),
    ("रामस्", "आसीत्", "रामआसीत्"),
    ("रामस्", "ईशः", "रामईशः"),
    ("भवान्", "चरति", "भवांश्चरति"),
    ("सन्", "शम्भुः", "सञ्छम्भुः"),
]

def test_prakriya(sutra_list):
    def _test_c(o, s):
        return ("".join([_o.canonical() for _o in list(o)])==s[2])
    def _test_d(o, s):
        return ("".join([_o.devanagari() for _o in list(o)])==s[2])
    for s in test_list:
        if s[0][-1] == "*":
            _pada = False
            s0 = s[0][:-1]
            s1 = s[1]
        else:
            s0 = s[0]
            s1 = s[1]
            _pada = True
        l = PaninianObject(s0, SLP1)
        if _pada:
            l.setTag("pada")
        r = PaninianObject(s1, SLP1)
        p = Prakriya(sutra_list,PrakriyaVakya((l, r)))
        p.execute()
        p.describe()
        o = p.output()
        # One of the outputs
        assert any([_test_c(_o,s) for _o in o])
    for s in test_list_d:
        if s[0][-1] == "*":
            _pada = False
            s0 = s[0][:-1]
            s1 = s[1]
        else:
            s0 = s[0]
            s1 = s[1]
            _pada = True
        l = PaninianObject(s0)
        if _pada:
            l.setTag("pada")
        r = PaninianObject(s1)
        p = Prakriya(sutra_list,PrakriyaVakya((l, r)))
        p.execute()
        p.describe()
        # Only one output
        o = p.output()
        assert any([_test_d(_o,s) for _o in o])

from sandhi_yaml import sutra_list
test_prakriya(sutra_list)


