"""
Operational Sutras

"""
from sanskrit_parser.base.sanskrit_base import SanskritObject, SanskritImmutableString, SLP1
from .guna_vriddhi import guna, vriddhi, ikoyan, ayavayav
from .maheshvara import ms

# Global Triggers
class GlobalTriggers(object):
    uran_trigger = False
    
gt = GlobalTriggers()
    
# Base class
class Sutra(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return str(self.name)
    
class SandhiSutra(Sutra):
    def __init__(self, name, adhikara, cond, op):
        super().__init__(name)
        self.adhikara = adhikara
        self.cond = cond
        self.op   = op
    def inAdhikara(self, context):
        return self.adhikara(context)
    def isTriggered(self, s1, s2):
        return self.cond(s1,s2)
    def operate(self, s1, s2):
        return self.op(s1, s2)

#    Sutra: AdguRaH
def aadgunah_c(s1: str,  s2: str) -> str:
    # Last letter of first string
    e = s1[-1].lower()
    # First letter of second string
    f = s2[0]
    return (e == "a") and _isInPratyahara("ik", f)

def aadgunah_o(s1: str,  s2: str) -> str:
    # Last letter of first string
    f = s2[0]
    if f.lower() == "f":
        print("Uran triggered")
        gt.uran_trigger = True
    # First letter of second string
    f = guna(f)
    return s1[:-1], f+s2[1:]

aadgunah = SandhiSutra(SanskritImmutableString("aad guRaH",SLP1),
                       None, aadgunah_c, aadgunah_o)

#     Sutra: vfdDireci
def vriddhirechi_c(s1: str,  s2: str) -> str:
    # Last letter of first string
    e = s1[-1].lower()
    # First letter of second string
    f = s2[0]
    return (e == "a") and \
       ms.isInPratyahara(
           SanskritImmutableString("ec",SLP1),
           SanskritImmutableString(f,SLP1)
                       )

def vriddhirechi_o(s1: str,  s2: str) -> str:
    f = s2[0]
    # First letter of second string
    f = vriddhi(f)
    return s1[:-1], f+s2[1:]
     
    
vriddhirechi = SandhiSutra(SanskritImmutableString("vfdDireci",SLP1),
                           None, vriddhirechi_c, vriddhirechi_o)


# Sutra: uraR raparaH
def uranraparah_c(s1:str, s2: str) -> str:
    return gt.uran_trigger

def uranraparah_o(s1:str, s2: str) -> str:
    gt.uran_trigger = False
    return s1, s2[0]+"r"+s2[1:]

uranraprah = SandhiSutra(SanskritImmutableString("uraRraparaH",SLP1),
                           None, uranraparah_c, uranraparah_o)

# Sutra  ikoyaRaci
def ikoyanaci_c(s1:str, s2: str) -> str:
    # Last letter of first string
    e = s1[-1].lower()
    # first letter of second string
    f = s2[0].lower()
    return _isInPratyahara("ik",e) and _isInPratyahara("ac",f)

def ikoyanaci_o(s1:str, s2: str) -> str:
    # Last letter of first string
    e = s1[-1].lower()
    return s1[:-1]+ikoyan(e), s2

ikoyanaci = SandhiSutra(SanskritImmutableString("ikoyaRaci",SLP1),
                           None, ikoyanaci_c, ikoyanaci_o)


# Sutra ecoyavAyAvaH
def ecoyavayavah_c(s1:str, s2: str) -> str:
    # Last letter of first string
    e = s1[-1].lower()
    # first letter of second string
    f = s2[0].lower()
    return _isInPratyahara("ec",e) and _isInPratyahara("ac",f)

def ecoyavayavah_o(s1:str, s2: str) -> str:
    # Last letter of first string
    e = s1[-1]
    return s1[:-1]+ayavayav(e), s2

ecoyavayavah = SandhiSutra(SanskritImmutableString("ecoyavAyAvaH",SLP1),
                           None, ecoyavayavah_c, ecoyavayavah_o)


# Sutra akaHsavarRedIrGaH
def savarnadirgha_c(s1:str, s2: str) -> str:
    # Last letter of first string
    e = s1[-1].lower()
    # first letter of second string
    f = s2[0].lower()
    return _isInPratyahara("ak",e) and (e == f)

def savarnadirgha_o(s1:str, s2: str) -> str:
    # Last letter of first string
    e = s1[-1]
    return s1[:-1]+e.upper(), s2[1:]

savarnadirgha = SandhiSutra(SanskritImmutableString("akaHsavarRedIrGaH",SLP1),
                           None, savarnadirgha_c, savarnadirgha_o)


# Utility functions

# Pratyahara check
def _isInPratyahara(p, s):
    return ms.isInPratyahara(
        SanskritImmutableString(p,SLP1),
        SanskritImmutableString(s,SLP1)
    )


# Sandhi Sutras
all_sandhi_sutras = [savarnadirgha, vriddhirechi, aadgunah, uranraprah, ikoyanaci,
                     ecoyavayavah]

