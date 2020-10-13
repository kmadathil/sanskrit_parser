from sanskrit_parser.base.sanskrit_base import SanskritImmutableString, SLP1
from .operations import adesha
from .maheshvara import ms, isInPratyahara


def dirgha(s: str):
    return adesha(s, "aAiIuUfFxX", "AAIIUUFFXX")

def guna(s: str):
    if s in "fF":
        # Uran raparaH
        r = "ar"
    elif s in "xX":
        r = "al"
    else:
        r = adesha(s, "iIuU", "eeoo")
    return r

def vriddhi(s: str):
    if s in "fF":
        # Uran raparaH
        r = "Ar"
    elif s in "xX":
        r = "Al"
    else:
        r = adesha(guna(s), "aeo", "AEO")
    return r

def ikoyan(s: str):
    return adesha(s.lower(),
                  ms.getPratyahara(SanskritImmutableString("ik",SLP1)),
                  ms.getPratyahara(SanskritImmutableString("yaR",SLP1),
                                   remove_a=True)
                  )

def samprasaranam(s: str):
    return adesha(s,
                  ms.getPratyahara(SanskritImmutableString("yaR",SLP1),
                                   remove_a=True),
                  ms.getPratyahara(SanskritImmutableString("ik",SLP1))
                  )


def ayavayav(s: str):
    if s == "e":
        return "ay"
    elif s == "o":
        return "av"
    elif s == "E":
        return "Ay"
    elif s == "O":
        return "Av"
    else:
        return s

def shcutva(s: str):
    return adesha(s, "stTdDn", "ScCjJY")

def zwutva(s: str):
    return adesha(s, "stTdDn", "zwWqQR")

def jashtva(s: str):
    return adesha(s, "JBGQDjbgqdKPCWTcwtkpSzsh", "jbgqdjbgqdgbjqdjqdgbjqdg")

def chartva(s: str):
    return adesha(s, "kKgGcCjJwWqQtTdDpPbB", "kkkkccccwwwwttttpppp")

def vargatritiya(s: str):
    return adesha(s, "kKgGcCjJwWqQtTdDpPbB", "GGGGJJJJQQQQDDDDBBBB")

def adivriddhi(s: str):
    r = ""
    av = False
    for _s in s:
        if (not av) and isInPratyahara("ac", SanskritImmutableString(_s, encoding=SLP1)):
            r = r + vriddhi(_s)
            av = True
        else:
            r = r + _s
    return r

# Fixme - anunasika ZSs yrl
def anunasika(s: str):
    return adesha(s, "kKgGcCjJwWqQtTdDpPbB", "NNNNYYYYRRRRnnnnmmmm")

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
