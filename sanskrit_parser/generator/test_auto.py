from sanskrit_parser.generator.pratyaya import *
from sanskrit_parser.generator.dhatu import *
from sanskrit_parser.generator.pratipadika import *
from sanskrit_parser.base.sanskrit_base import SLP1, DEVANAGARI

from sutras_yaml import sutra_list
from conftest import run_test

import pytest
import logging

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
    (ava, (AN, "ihi"), "avehi"), # 6.1.95
    ("SivAya", "om", "SivAyom"), # 6.1.95
    (kavi, O, "kavI"),
    ("catur", "nAm", ['caturRAm', 'catur~RAm', 'caturRRAm']), #8.4.1
    ("BavAn", "liKati", "BavAl~liKati"), #8.4.60 .1
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
    (("अग्नि", su), "रोचते", "अग्नी रोचते"),
    # FIXME: correct when we can do uttizTati, move to utTAna
    (ud, (sTA, tip), ["उत्थाति", "उत्थ्थाति"]),
    ("पुष्*", "ना", "ति", "पुष्णाति"), # 8.4.1
    ("तृंह्*", "अनीय", "तृंहणीय"), # 8.4.2
     ]

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


@pytest.fixture
def sutra_fixture():
    return sutra_list


def generate_vibhakti(pratipadika, vibhaktis):
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
    return t

# Manual test
def check_vibhakti(t, sutra_list):
    for s in t:
        run_test(s, sutra_list, encoding=DEVANAGARI)
            
def test_vibhakti(vibhakti, sutra_fixture, caplog):
    run_test(vibhakti, sutra_fixture, encoding=DEVANAGARI)

def test_manual_d(manual_d, sutra_fixture):
    run_test(manual_d, sutra_fixture, encoding=DEVANAGARI)

def test_manual(manual, sutra_fixture):
    run_test(manual, sutra_fixture, encoding=SLP1)

def pytest_generate_tests(metafunc):
    if 'vibhakti' in metafunc.fixturenames:
         vibhakti_list = generate_vibhakti(rAma, viBakti["rAma"])
         metafunc.parametrize("vibhakti", vibhakti_list)
    if 'manual_d' in metafunc.fixturenames:
         metafunc.parametrize("manual_d", test_list_d)
    if 'manual' in metafunc.fixturenames:
         metafunc.parametrize("manual", test_list)
         

if __name__ == "__main__":
    from sanskrit_parser import enable_console_logger, enable_file_logger
    logging.basicConfig(level=logging.INFO)
    enable_console_logger()
    enable_file_logger(level=logging.DEBUG)

    check_vibhakti(generate_vibhakti(rAma, viBakti["rAma"]), sutra_list)
