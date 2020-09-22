from sanskrit_parser.generator.sutra import *
from sanskrit_parser import enable_console_logger
import logging

enable_console_logger(logging.DEBUG)

test_list = [
    ("rAma", "eti", "rAmEti"),
    ("gaRa", "upadeSaH", "gaRopadeSaH"),
    ("rAma", "iti", "rAmeti"),
    ("tyaktvA", "uttizTa", "tyaktvottizTa"),
    ("tava", "ozTaH", "tavOzTaH"),
    ("deva", "fzi", "devarzi"),
    ("kavO", "asmAkam", "kavAvasmAkam"),
    ("gavi", "asmAkam", "gavyasmAkam"),
    ("gavi", "iha", "gavIha"),
    ("AgacCa", "atra", "AgacCAtra"),
    ("yAne", "eti", "yAnayeti"),
    ]


def test_static():
    for s in test_list:
        r = SutraEngine.sandhi(s[0],s[1])
        assert "".join(list(r))==s[2]

test_static()
