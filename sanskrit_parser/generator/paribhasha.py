from sanskrit_parser.base.sanskrit_base import SanskritImmutableString, SLP1
from .operations import adesha
from .maheshvara import ms


def dirgha(s: str):
    return adesha(s, "aAiIuUfFxX", "AAIIUUFFXX")

def guna(s: str):
    return adesha(s, "iIuUfFxX", "eeooaaaa")

def vriddhi(s: str):
    return adesha(guna(s), "aeo", "AEO")

def ikoyan(s: str):
    return adesha(s.lower(),
                  ms.getPratyahara(SanskritImmutableString("ik",SLP1)),
                  ms.getPratyahara(SanskritImmutableString("yaR",SLP1))
                  )

def samprasaranam(s: str):
    return adesha(s,
                  ms.getPratyahara(SanskritImmutableString("yaR",SLP1)),
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
