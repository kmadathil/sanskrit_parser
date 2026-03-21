from indic_transliteration import sanscript
from sanskrit_parser.base.sanskrit_base import SanskritImmutableString
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
                  ms.getPratyahara(SanskritImmutableString("ik", sanscript.SLP1)),
                  ms.getPratyahara(SanskritImmutableString("yaR", sanscript.SLP1),
                                   remove_a=True)
                  )


def samprasaranam(s: str):
    return adesha(s,
                  ms.getPratyahara(SanskritImmutableString("yaR", sanscript.SLP1),
                                   remove_a=True),
                  ms.getPratyahara(SanskritImmutableString("ik", sanscript.SLP1))
                  )


def samprasArana_van(lc: str):
    """samprasāraṇa for -v-a-n stems (Svan, yuvan, maGavan) in bha position (SK362 / 6.4.133).
    lc ends in -v-a (the 'n' is held in l by the YAML rule).
    Converts v→u (samprasāraṇa via samprasaranam), then merges with the preceding character:
      - consonant + u  →  consonant + u        (Sva  → Su)
      - u + u          →  ū  (savarna dīrgha)  (yuva → yU)
      - a + u          →  o  (guṇa sandhi)      (maGava → maGo)
    """
    s = samprasaranam(lc[-2])    # v → u
    pred = lc[-3]                # character just before the v
    if isInPratyahara("ac", pred):
        if isSavarna("u", pred):         # u + u → ū  (yuvan)
            return lc[:-3] + dirgha(s)
        else:                            # a + u → o  (maGavan)
            return lc[:-3] + guna(s)
    else:                                # consonant + u  (śvan: S + u)
        return lc[:-2] + s


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
    return adesha(s, "cCjJYh", "kKgGNG")


def kvinKutva(s: str):
    """ku-substitution for kvin-derived stems (8.2.62): kutva extended with:
    - S (ś) → k, q (ḍ) → g: ś-final path (8.2.36 S→ṣ + 8.2.39 ṣ→ḍ, then ḍ→g here)
    - n (dental) → N (velar ṅ): dental n left at pada-end after 8.2.23 deletes c from añc-stems
      (numAgama inserts n; 8.2.23 fires before 8.3.24+8.4.58 can convert n→M→Y)"""
    return adesha(s, "cCjJYhSqn", "kKgGNGkgN")


def vargatritiya(s: str):
    return adesha(s, "kKgGcCjJwWqQtTdDpPbB", "GGGGJJJJQQQQDDDDBBBB")


def adivriddhi(s: str):
    r = ""
    av = False
    for _s in s:
        if (not av) and isInPratyahara("ac", SanskritImmutableString(_s, encoding=sanscript.SLP1)):
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

#kutva for h in han
def han_kutva(lc: str):
    return lc.replace("h","G")

# for Ratva override in han
def anat(s):
    return s != "a"
    
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


def ratva_string(s, awkupnumvyavaya=False, apply=True):
    """Unified ṇatva helper for both condition check and xform.

    Scans s for every 'n' at position i. A 'n' qualifies if scanning backward
    from i-1 through permissible vyavāya characters we find ṛ/ṣ/r (r, z, f).

    awkupnumvyavaya=False (8.4.1): no intervening characters allowed
    awkupnumvyavaya=True  (8.4.2): aṭkupvāṅnum chars (vowels, ku/pu-class,
                                    anusvara) may intervene

    apply=True  (xform use):       return modified string (n→R where qualifying)
    apply=False (condition check): return bool — True if any 'n' would be changed
    """
    result = list(s)
    changed = False
    for i in range(len(s)):
        if s[i] == 'n':
            # 8.3.24 (naścāpadāntasya jali): n before Jal becomes anusvāra M.
            # That rule has priority; ṇatva must not target such n.
            if i + 1 < len(s) and isInPratyahara('Jal', s[i + 1]):
                continue
            j = i - 1
            while j >= 0:
                if s[j] in ('r', 'z', 'f', 'F'):
                    result[i] = 'R'
                    changed = True
                    break
                elif awkupnumvyavaya and awkupvaNnum(s[j]):
                    j -= 1
                else:
                    break
    if apply:
        return "".join(result)
    else:
        return changed


def has_ratva_simple(s):
    """Return True if s has ṛ/ṣ/r directly before 'n' (8.4.1, no vyavāya)."""
    return ratva_string(s, awkupnumvyavaya=False, apply=False)


def has_ratva_vyavaya(s):
    """Return True if s has ṛ/ṣ/r before 'n' with aṭkupvāṅnum vyavāya (8.4.2)."""
    return ratva_string(s, awkupnumvyavaya=True, apply=False)


def has_ratva_non_at(s):
    """For han-stems (8.4.22): True if s has ṛ/ṣ/r→(aṭkup vyavāya)→n where 'a' does NOT
    directly precede 'n'. Returns True to block ṇatva (non-at-pūrva case);
    returns False when 'a' immediately precedes 'n' (allowing ṇatva in that case)."""
    for i in range(1, len(s)):
        if s[i] == 'n' and s[i-1] != 'a':
            if i + 1 < len(s) and isInPratyahara('Jal', s[i + 1]):
                continue
            j = i - 1
            while j >= 0:
                if s[j] in ('r', 'z', 'f', 'F'):
                    return True
                elif awkupvaNnum(s[j]):
                    j -= 1
                else:
                    break
    return False


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


def saMyogapUrvaVamanta(lp):
    """True if lp ends in hal+[v,m]+a+n — saMyoga ending in v or m immediately precedes 'an'."""
    if len(lp) < 4:
        return False
    return (lp[-1] == 'n' and lp[-2] == 'a' and
            lp[-3] in ['v', 'm'] and isInPratyahara('hal', lp[-4]))


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


def adi(s, x):
    return s[0] == x


def dAdi(s):
    return adi(s, "d")


def ekAcDAtu(s):
    ac_count = len([x for x in s if isInPratyahara("ac", x)])
    return ac_count == 1


def baSoBaz(s):
    for j in range(len(s)):
        if isInPratyahara("baS", s[j]):  # Backwards
            break
    return s[0:j]+adesha(s[j], "bgwd", "BGWD")+s[j+1:]


def druhAdi(ss):
    s = str(ss)
    return ((s == "druh") or (s == "muh") or (s == "snih") or (s == "snuh"))


def notnull(s):
    if hasattr(s, 'canonical'):      # Suggested by Claude Code
        return s.canonical() != ""
    return ((s is not None) and (s != ""))


def null(s):
    if hasattr(s, 'canonical'):
        return s.canonical() == ""
    return (s is None) or (s == "")


# sUtra: adeN guRaH
def is_guna(s: str):
    so = SanskritImmutableString(s, encoding=sanscript.SLP1)
    at = "a"
    eng = SanskritImmutableString("eN", encoding=sanscript.SLP1)
    return (s == at) or ms.isInPratyahara(eng, so)


# sUtra: vRdDirAdEc
def is_vriddhi(s: str):
    so = SanskritImmutableString(s, encoding=sanscript.SLP1)
    aat = "A"
    aich = SanskritImmutableString("Ec", encoding=sanscript.SLP1)
    return (s == aat) or ms.isInPratyahara(aich, so)

# daSca d check
def idam_d_p(s):
    return ("d" in s)
