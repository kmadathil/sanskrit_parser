from sanskrit_parser.base.sanskrit_base import SanskritImmutableString, SLP1
from .operations import adesha
from .maheshvara import ms, isInPratyahara, isSavarna
from sanskrit_parser.generator.pratipadika import *  # noqa: F403


def dirgha(s: str):
    return adesha(s, "aAiIuUfFxX", "AAIIUUFFXX")


def hrasva(s: str):
    return adesha(s, "aAiIuUfFxXeEoO", "aaiiuuffxxiiuu")


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
                  ms.getPratyahara(SanskritImmutableString("ik", SLP1)),
                  ms.getPratyahara(SanskritImmutableString("yaR", SLP1),
                                   remove_a=True)
                  )


def samprasaranam(s: str):
    return adesha(s,
                  ms.getPratyahara(SanskritImmutableString("yaR", SLP1),
                                   remove_a=True),
                  ms.getPratyahara(SanskritImmutableString("ik", SLP1))
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


def kutva(s: str):
    return adesha(s, "cCjJY", "kKgGN")


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


def pAdAdi_AdeSa(s: str):
    d = {
        "pAda": "pad",
        "danta": "dat",
        "nAsikA": "nas",
        "mAsa": "mAs",
        "hfdaya": "hfd",
        "niSA": "niS",
        "asfj": "asan",
        "yUza": "yUzan",
        "doza": "dozan",
        "yakft": "yakan",
        "Sakft": "Sakan",
        "udaka": "udan",
        "Asya": "Asan",
        }
    if s in d:
        return d[s]
    else:
        return s


# FIXME - this is better. debug in SK228
def pAdAdi_AdeSa_r(s):
    d = {
        "pAda": pad,    # noqa: F405
        "danta": dat,    # noqa: F405
        "nAsikA": nas,    # noqa: F405
        "mAsa": mAs,    # noqa: F405
        "hfdaya": hfd,    # noqa: F405
        "niSA": niS,    # noqa: F405
        "asfj": asan,    # noqa: F405
        "yUza": yUzan,    # noqa: F405
        "doza": dozan,    # noqa: F405
        "yakft": yakan,    # noqa: F405
        "Sakft": Sakan,    # noqa: F405
        "udaka": udan,    # noqa: F405
        "Asya": Asan,    # noqa: F405
        }
    if str(s) in d:
        return d[s]
    else:
        return s


# Fixme - anunasika ZSs yrl
def anunasika(s: str):
    if s in "yrlvSZs":
        return s+"~"
    else:
        return adesha(s, "kKgGcCjJwWqQtTdDpPbB", "NNNNYYYYRRRRnnnnmmmm")


# vyavAya check for razAByAM noRaH samAnapade
def rz_vyavaya_l(s: str):
    i = len(s)-1
    while(i >= 0):
        # ऋवर्णात् नस्य णत्वं वाच्यम्
        if ((s[i] == "r") or (s[i] == "z") or (s[i] == "f")):
            return True
        elif awkupvaNnum(s[i]):
            i = i-1
        else:
            return False
    return False


def rz_vyavaya_r(s: str):
    i = 0
    while(i < len(s)):
        if (s[i] == "n"):
            # Na padAntasya
            if s.hasTag("svAdi"):
                return (i != (len(s) - 1))
            else:
                return True
        elif awkupvaNnum(s[i]):
            i = i+1
        else:
            return False
    return False


# For situations like yUzan + i yUzaRi
def rz_vyavaya_n(s: str):
    if len(s) == 0:
        return False
    if (s[-1] != "n"):
        return False
    i = len(s)-2
    while(i >= 0):
        # ऋवर्णात् नस्य णत्वं वाच्यम्
        if ((s[i] == "r") or (s[i] == "z") or (s[i] == "f")):
            return True
        elif awkupvaNnum(s[i]):
            i = i-1
        else:
            return False
    return False


def awkupvaNnum(s):
    # FIXME handle AN
    return isInPratyahara("aw", s) or isSavarna("ku", s) or isSavarna("pu", s) \
        or (s == "M")


def Ratva(s):
    return s.replace("n", "R", 1)


def iyuvaN(s):
    if isSavarna("i", s):
        return "iy"
    elif isSavarna("u", s):
        return ("uv")
    else:
        return s


def anekAc_asaMyogapUrva(s):
    if ((len(s) > 2) and (isInPratyahara("hal", s[-2]) and isInPratyahara("hal", s[-3]))):
        return False
    ac = 0
    for sc in s:
        if isInPratyahara("ac", sc):
            ac = ac+1
        if ac > 1:
            return True
    return False


def numAgama(s):
    lastac = -1
    lens = len(s)
    for j in range(lens):
        jj = -1*(j+1)
        if isInPratyahara("ac", s[jj]):  # Backwards
            lastac = lens + jj
            break
    if lastac == lens-1:
        r = s + "n"
    elif lastac > -1:
        r = s[:lastac+1] + "n" + s[lastac+1:]
    else:
        r = s
    return r


# aco'ntyAdi wi
def wilopa(s):
    lastac = -1
    lens = len(s)
    for j in range(lens):
        jj = -1*(j+1)
        if isInPratyahara("ac", s[jj]):  # Backwards
            lastac = lens + jj
            break
    if lastac > -1:
        r = s[:lastac]
    else:
        r = s
    return r


def notnull(s):
    return ((s is not None) and (s != ""))


def null(s):
    return ((s is None) or (s == ""))


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
