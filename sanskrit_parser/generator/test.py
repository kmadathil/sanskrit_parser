# -*- coding: utf-8 -*-
from sanskrit_parser import enable_console_logger, enable_file_logger
from sanskrit_parser.base.sanskrit_base import SLP1, DEVANAGARI
import sanskrit_parser.generator.sutra as sutra
from sanskrit_parser.generator.paninian_object import PaninianObject
from sanskrit_parser.generator.prakriya import Prakriya, PrakriyaVakya
from sanskrit_parser.generator.pratyaya import *

import logging
#logging.basicConfig(level=logging.INFO)
enable_console_logger()
enable_file_logger(level=logging.DEBUG)

test_list = [
    ("kArt*", "tikaH", ["kArtikaH", "kArttikaH"]),
    ("gaRa", "upadeSaH", "gaRopadeSaH"),
    ("rAma", "eti", "rAmEti"),
    ("rAma", "iti", "rAmeti"),
    ("tyaktvA", "uttizWa", "tyaktvottizWa"),
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
    ("haras", "Sete", ['haraHSete', 'haraSSete']),
    ("Bavat", "caraRam", "BavaccaraRam"),
    # Non pada
    ("praS*", "nas", "praSnas"),
    ("rAmas", "zazQa", ["rAmazzazQa", 'rAmaHzazQa']),
    ("rAmas", "wIkate", "rAmazwIkate"),
    ("sarpiz", "tamam", "sarpizwamam"),
    ("marut", "wIkate", "maruwwIkate"),
    ("SuBam", "karoti", ["SuBaNkaroti", "SuBaMkaroti"]),
    ("vAk", "arTO", "vAgarTO"),
    ("goDuk", "awati", "goDugawati"),
    ("goDuk", "girati", "goDuggirati"),
    ("virAw", "vadati", "virAqvadati"),
    ("kavis", "asti", "kavirasti"),
    ("havis", "vartate", ["havirvartate", "havirvvartate"]),
    ("brah*", "mA", ["brahmA", "brahmmA"]),
    ]

test_list_d = [
    ("मरुत्", "टीकते", "मरुट्टीकते"),
    ("मधुलिट्", "तरति", "मधुलिट्तरति"),
    ("मरुत्", "षष्ठः", "मरुत्षष्ठः"),
    ("सन्", "षष्ठः", "सन्षष्ठः"),
    ("षण्", "नाम्", "षण्णाम्"),
    ("वाग्", "मुखम्", ["वाङ्मुखम्", "वाग् मुखम्"]),
     ("षड्", "मुखम्", ["षण्मुखम्", "षड्मुखम्"]),
     ("एतद्", "मुरारि", ["एतद् मुरारि", "एतन्मुरारि"]),
     ("त्रिष्टुब्", "नमति", ["त्रिष्टुम्नमति", "त्रिष्टुब् नमति"]),
     ("वाग्", "चलति", "वाक्चलति"),
     ("त्रिष्टुब्", "छन्दः", "त्रिष्टुप्छन्दः"),
     ("अस्", "ति", "अस्ति"),
     ("तत्", "लीनः", "तल्लीनः"),
     ("प्रत्यङ्", "आत्मा", "प्रत्यङ्ङात्मा"),
     ("सुगण्", "ईशः", "सुगण्णीशः"),
     ("अस्मिन्", "एव", "अस्मिन्नेव"),
     ("वाग्", "हरि", ["वाग्घरि", "वाग् हरि"]),
     ("अज्", "हलौ", ["अज्झलौ", "अज् हलौ"]),
     ("मधुलिड्", "हसति", ["मधुलिड्ढसति", "मधुलिड्हसति"]),
     ("तद्", "हितम्", ["तद्धितम्", "तद्हितम्"]),
     ("त्रिष्टुब्", "हि", ["त्रिष्टुब्हि", "त्रिष्टुब्भि"]),
     ("तद्", "शेते", ["तच्शेते", "तच्छेते"]),
     ("मधुलिड्", "शेते", ['मधुलिट्शेते', "मधुलिट्छेते"]),
     ("त्रिष्टुब्", "शेते", ["त्रिष्टुप्शेते", "त्रिष्टुप्छेते"]),
     ("तद्", "श्लोकेन", ["तच्श्लोकेन", "तच्छ्लोकेन"]),
     ("तत्", "जयते", "तज्जयते"),
     ("रामः", "तरति", "रामस्तरति"),
     ("बालः", "थूकरोति", "बालस्थूकरोति"),
     ("हरिः", "चलति", "हरिश्चलति"),
     ("पयः", "क्षीरम्", "पयःक्षीरम्"),
     ("कः", "त्सरुः", "कःत्सरुः"),
     ("हरिस्", "शेते", ["हरिश्शेते", "हरिःशेते"]),
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
    ("सन्", "शम्भुः", ["सञ्च्छम्भुः", 'सञ्शम्भुः', 'सञ्च्शम्भुः']),
    ("स्व", "छाया", "स्वच्छाया"),
    ("आ", "छाया", "आच्छाया"),
    ("आ", "छादयति", "आच्छादयति"),
    ("मा", "छिदत्", "माच्छिदत्"),
    ("सा", "छाया", ["साच्छाया", "साछाया"]),
    ("कार्*", "यम्", ["कार्य्यम्", "कार्यम्"]),
    ("आदित्य्", "य", ["आदित्य", "आदित्य्य"]),
    ("गो*", yat_t, "गव्य"),  
    ("नौ*", yat_t, "नाव्य"),  
    ("भू*", GaY, "भाव"),
    ("कृ*", Ric, "कारि"),
    ("औपगु*", aR_t, "औपगव"),
    ("बभ्रु*", yaY_t, "बाभ्रव्य"),
    ("नी*", tfc, "नेतृ"),
    ("भू*", Sap, "भव"),
]

def test_prakriya(sutra_list):
    def _test(output, s, enc):
        _s = s[2]
        if not isinstance(_s, list):
            # Single element
            _s = [_s]
        # Remove spaces in reference
        _s = [x.replace(' ',"") for x in _s]
        j = [
            PaninianObject("".join([
                _o.transcoded(SLP1) for _o in list(o)
            ]), encoding=SLP1).transcoded(enc)
            for o in output
        ]
        if not  (set(j) == set(_s)):
            print(set(j), set(_s))
        return (set(j) == set(_s))
    def run_test(s, encoding=SLP1):
        if (isinstance(s[0], str) and (s[0][-1] == "*")):
            _pada = False
            s0 = s[0][:-1]
            s1 = s[1]
        else:
            s0 = s[0]
            s1 = s[1]
            _pada = True
        if isinstance(s0, str):
            l = PaninianObject(s0, encoding)
            if _pada:
                l.setTag("pada")
            else:
                l.setTag("anga")
        else:
            l = s0
        if isinstance(s1, str):
            r = PaninianObject(s1, encoding)
        else:
            r = s1
        p = Prakriya(sutra_list,PrakriyaVakya((l, r)))
        p.execute()
        p.describe()
        o = p.output()
        assert _test(o, s, encoding)
        
    for s in test_list:
        run_test(s, SLP1)
    for s in test_list_d:
        run_test(s, DEVANAGARI)

from sandhi_yaml import sutra_list
test_prakriya(sutra_list)
