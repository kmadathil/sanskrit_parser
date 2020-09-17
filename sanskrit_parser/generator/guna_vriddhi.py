from sanskrit_parser.base.sanskrit_base import SanskritImmutableString, SLP1
from .operations import adesha
from .maheshvara import ms

def guna(s: str):
    return adesha(s, "iIuUfFxX", "eeooaaaa")

def vriddhi(s: str):
    return adesha(guna(s), "eo", "EO")

# sUtra: adeN guRaH
def is_guna(s: str):
    so = SanskritImmutableString(s, encoding=SLP1)
    at = "a"
    eng = SanskritImmutableString("eN", encoding=SLP1)
    return (s == at) or ms.isInPratyahara(eng, so)

# sUtra: vRdDirAdEc
def is_vriddhi(s: str):
    so = SanskritImmutableString(s, encoding=SLP1)
    aat = "A"
    aich = SanskritImmutableString("Ec", encoding=SLP1)
    return (s == aat) or ms.isInPratyahara(aich, so)
