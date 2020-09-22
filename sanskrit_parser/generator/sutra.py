"""
Operational Sutras

"""
from sanskrit_parser.base.sanskrit_base import SanskritObject, SanskritImmutableString, SLP1
from .guna_vriddhi import guna, vriddhi, ikoyan, ayavayav
from .maheshvara import ms

import logging
logger = logging.getLogger(__name__)

# Global Triggers
class GlobalTriggers(object):
    uran_trigger = False


# Sutra execution engine
class SutraEngine(object):
    all_sutra_list = []
    sandhi_sutra_list = []

    @classmethod
    # pUrvaparanityAntaraNgApavAdAnamuttarottaraM balIyaH
    def sutra_priority(cls, sutras: list):
        _s = sutras
        # Para > purva
        aps_nums = [s._aps_num for s in sutras]
        nmax = aps_nums.index(max(aps_nums))
        smax = sutras[nmax]
        return smax
    
    @classmethod
    def _exec_single(cls,l,*args):
        triggered = [s for s in l if s.isTriggered(*args)]
        logger.debug(f"I: {args}")
        if triggered:
            logger.debug("Triggered rules")
            for t in triggered:
                logger.debug(t)
            r = cls.sutra_priority(triggered).operate(*args)
            logger.debug(f"O: {r}")
            return r
        else:
            logger.debug(f"Nothing triggered")
            return False

    @classmethod
    def _exec(cls, l, *args):
        logger.debug(f"Input: {args}")
        _r = cls._exec_single(l, *args)
        while(_r):
            r = _r
            _r = cls._exec_single(l, *_r)
        logger.debug(f"Final Result: {r[0]+r[1]}\n\n")
        return r
    
    @classmethod
    def sandhi(cls, s1, s2):
        r = cls._exec(cls.sandhi_sutra_list, s1, s2)
        return r
    
# Base class
class Sutra(object):
    def __init__(self, name: str, aps:tuple):
        self.a_p_s = aps  # Tuple: (Adhaya, pada, sutra)
        self.name = name
        self._aps_str = '.'.join([str(x) for x in list(self.a_p_s)])
        self._aps_num = aps[2]+aps[1]*1000+aps[0]*10000
        SutraEngine.all_sutra_list.append(self)
    def __str__(self):
        return f"{self._aps_str:7}: {str(self.name)}"
    
class SandhiSutra(Sutra):
    def __init__(self, name, aps, adhikara, cond, op):
        super().__init__(name, aps)
        self.adhikara = adhikara
        self.cond = cond
        self.op   = op
        SutraEngine.sandhi_sutra_list.append(self)
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
        GlobalTriggers.uran_trigger = True
    # First letter of second string
    f = guna(f)
    return s1[:-1], f+s2[1:]

aadgunah = SandhiSutra(SanskritImmutableString("aad guRaH",SLP1),(6,1,87),
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
     
    
vriddhirechi = SandhiSutra(SanskritImmutableString("vfdDireci",SLP1),(6,1,88),
                           None, vriddhirechi_c, vriddhirechi_o)


# Sutra: uraR raparaH
def uranraparah_c(s1:str, s2: str) -> str:
    return GlobalTriggers.uran_trigger

def uranraparah_o(s1:str, s2: str) -> str:
    GlobalTriggers.uran_trigger = False
    return s1, s2[0]+"r"+s2[1:]

uranraprah = SandhiSutra(SanskritImmutableString("uraRraparaH",SLP1),(1,1,51),
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

ikoyanaci = SandhiSutra(SanskritImmutableString("ikoyaRaci",SLP1),(6,1,77),
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

ecoyavayavah = SandhiSutra(SanskritImmutableString("ecoyavAyAvaH",SLP1),(6,1,78),
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
                            (6,1,101),
                           None, savarnadirgha_c, savarnadirgha_o)



# Utility functions

# Pratyahara check
def _isInPratyahara(p, s):
    return ms.isInPratyahara(
        SanskritImmutableString(p,SLP1),
        SanskritImmutableString(s,SLP1)
    )

