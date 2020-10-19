# -*- coding: utf-8 -*-
from sanskrit_parser import enable_console_logger, enable_file_logger
from sanskrit_parser.base.sanskrit_base import SLP1, DEVANAGARI
import sanskrit_parser.generator.sutra as sutra
from sanskrit_parser.generator.paninian_object import PaninianObject
from sanskrit_parser.generator.prakriya import Prakriya, PrakriyaVakya
from sanskrit_parser.generator.pratyaya import *
from sanskrit_parser.generator.dhatu import *

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
    ((mud, Ric), Sap, tip, "modayati"),
    (BU, Sap, tip, "Bavati"),
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
#     ("अज्*", "हलौ", ["अज्झलौ", "अज् हलौ"]),
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
    (("राम", su), (as_dhatu, tip), "रामोस्ति"),
    ("रामस्", "गच्छति", "रामोगच्छति"),
    ('भोस्',  'देवाः', "भोदेवाः"),
    ('भगोस्',  'मनुष्याः', "भगोमनुष्याः"),
    ('अघोस्',  'राक्षसाः', "अघोराक्षसाः"),
    ('देवास्',  'गच्छन्ति', "देवागच्छन्ति"),
    ("रामस्", "आसीत्", "राम आसीत्"),
    ("रामस्", "ईशः", "रामईशः"),
    ("भवान्", "चरति", "भवांश्चरति"),
    ("सन्", "शम्भुः", ["सञ्च्छम्भुः", 'सञ्शम्भुः', 'सञ्च्शम्भुः']),
    ("स्व", "छाया", "स्वच्छाया"),
    (AN, "छाया", "आच्छाया"),
    (AN, ((Cad, Ric), Sap, tip), "आच्छादयति"),
#    (AN, "छादयति", "आच्छादयति"),
    (mAN, "छिदत्", "माच्छिदत्"),
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
    ("दोघ्*", "धुम्", "दोग्धुम्"),
    ("विद्वान्स्", "अपठत्", "विद्वानपठत्"),
    ("अपठन्त्", "बालकाः", "अपठन्बालकाः"), 
    (lUY, Ryat, "लाव्य"),
    (kzI, yat, ["क्षेय", "क्षय्य"]),
    (ji, yat, ["जेय", "जय्य"]),
    (wukrIY, yat, ["क्रेय", "क्रय्य"]),
     # FIXME - can't test this now
    # आ + वेञ् + यक् + त = ओयते
    ("आ", (veY_smp, yak), "ओय"),
    ("प्र", (eDa, Sap, "te"), "प्रैधते"),
    ("उप", (iR,  tip), "उपैति"),
    (pra, (fcCa, Sap, tip), "प्रार्च्छति"),
    ("ब्रह्म", "ऋषि", "ब्रह्मर्षि"),
    (AN, ((Cad, Ric), Sap, tip), "आच्छादयति"),
    (("राम", su), "आसीत्", "राम आसीत्"),
    (gfj, Sap, tip, "गर्जति"),
    (vid, tip, "वेत्ति"),
    (("राम", su), (as_dhatu, tip), "रामोस्ति"),
    (("राम", su), avasAna, "रामः ।"),
    ("वाच्", ByAm, "वाग्भ्याम्"),
    ("त्यज्", ktvA, "त्यक्त्वा"),
    (("वाच्", su), avasAna, ["वाग् ।", "वाक् ।"]),
    (("वाच्", su), (as_dhatu, tip), "वागस्ति"),
    ("मधुलिह्", ByAm, "मधुलिड्भ्याम्"),
    (("लिह्", su) , avasAna, ["लिट् ।", "लिड् ।"]),
    (qulaBaz, kta, "लब्ध"),
    (guhU, kta, "गूढ"),
    ("पुनर्", "रमते", "पुना रमते"),
    (("अग्नि", su), "रोचते", "अग्नी रोचते")
    ]

def test_prakriya(sutra_list):
    def _test(output, s, enc):
        _s = s[-1]
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
        pl = []
        # Assemble list of inputs
        for i in range(len(s)-1):
            def _gen_obj(s, i):
                if isinstance(s[i], str):
                    # Shortcuts for two input tests not using predefined objects
                    # If a string in the first place ends with * it's an anga
                    # Else it's a pada
                    # For everything else, use predefined objects
                    if (i==0) and (s[i][-1] == "*"):
                        s0 =  s[0][:-1]
                        l = PaninianObject(s0, encoding)
                        l.setTag("aNga")
                    else:
                        s0 =  s[i]
                        l = PaninianObject(s[i], encoding)
                        if i==0:
                            l.setTag("pada")
                        return l
                elif isinstance(s[i], tuple) or isinstance(s[i], list):
                    l = [_gen_obj(s[i], ii) for (ii, ss) in enumerate(s[i])]
                else:
                    l = s[i]
                return l
            l = _gen_obj(s, i)
            pl.append(l)
        p = Prakriya(sutra_list,PrakriyaVakya(pl))
        p.execute()
        p.describe()
        #print(p.dict())
        o = p.output()
        assert _test(o, s, encoding)
       
    for s in test_list:
        run_test(s, SLP1)
    for s in test_list_d:
        run_test(s, DEVANAGARI)

from sandhi_yaml import sutra_list
test_prakriya(sutra_list)
