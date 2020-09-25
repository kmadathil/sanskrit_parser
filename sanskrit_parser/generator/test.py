from sanskrit_parser import enable_console_logger
from sanskrit_parser.base.sanskrit_base import SLP1
from sanskrit_parser.generator.sutra import SutraEngine
from sanskrit_parser.generator.paninian_object import PaninianObject

import logging
enable_console_logger(logging.DEBUG)

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
    ("yAne", "eti", "yAnayeti"),
    ("yAne", "atra", "yAnetra"),
    ("yAne", "AgacCati", "yAnayAgacCati"),
    ("vizRo", "ava", "vizRova"),
    ]


def test_static():
    for s in test_list:
        l = PaninianObject(s[0], SLP1)
        r = PaninianObject(s[1], SLP1)
        r = SutraEngine.sandhi(l, r)
        assert "".join([_r.canonical() for _r in list(r)])==s[2]

#print(SutraEngine.sandhi_sutra_list)
test_static()
