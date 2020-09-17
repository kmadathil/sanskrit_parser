"""
Operational Sutras

"""
from sanskrit_parser.base.sanskrit_base import SanskritObject, SanskritImmutableString, SLP1
from .guna_vriddhi import guna, vriddhi
from .maheshvara import ms

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
    return e == "a"

def aadgunah_o(s1: str,  s2: str) -> str:
    # Last letter of first string
    f = s2[0]
    # First letter of second string
    f = guna(f)
    return s1[:-1]+f+s2[1:]

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
    return s1[:-1]+f+s2[1:]
     
    
vriddhirechi = SandhiSutra(SanskritImmutableString("vfdDireci",SLP1),
                           None, vriddhirechi_c, vriddhirechi_o)

