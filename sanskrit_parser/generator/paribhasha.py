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

def kuk_Tuk(s: str):
    """8.3.28: kuk augment for ṅ (N→k), ṭuk augment for ṇ (R→w/ṭ) before śar."""
    return adesha(s, "NR", "kw")


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


def has_satva_vyavaya(s):
    """Return True if s ends in iṇ/ku with intervening num(M/n)/visarga(H)/śar(S/z/s) (8.3.58)."""
    if not s:
        return False
    i = len(s) - 1
    # Must have at least one vyavāya char (num=M/n, visarga=H, or śar sibilant=S/z/s)
    if s[i] not in ('n', 'H', 'S', 'z', 's'):
        return False
    # Skip all vyavāya chars backward
    while i >= 0 and s[i] in ('n', 'H', 'S', 'z', 's'):
        i -= 1
    # Preceding char must be iṇ or ku-class
    if i >= 0 and (isInPratyahara('iR', s[i]) or isSavarna('ku', s[i])):
        return True
    return False


def anusvara_jhal_string(s, apply=True):
    """8.3.24 naścāpadāntasya jhali: m or n (not at string-final position) → M before Jal.

    Scans s for every m or n at position i (i < len(s)-1). Qualifies when s[i+1] is in
    the Jal pratyahara. Replaces qualifying m/n with M (anusvāra).

    apply=True  (xform use):       return modified string
    apply=False (condition check): return True if any m/n would be changed
    """
    result = list(s)
    changed = False
    k = 0
    for i in range(len(s) - 1):    # āpadāntasya: exclude final position
        if s[i] in ('m', 'n') and isInPratyahara('Jal', s[i + 1]):
            result[i] = 'M'
            changed = True
            k = i
    if apply:
        return "".join(result[0:k+1]), "".join(result[k+1:])
    else:
        return changed


def has_anusvara_jhal(s):
    """Condition check: True if s contains m or n (non-final) before Jal (8.3.24)."""
    return anusvara_jhal_string(s, apply=False)


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


def is_ekac(s):
    """Return True if s contains exactly one vowel (ekāc = monosyllabic stem)."""
    if not s:
        return False
    vowel_count = 0
    vowels = set("aAiIuUfFxXeEoO")
    for ch in s:
        if ch in vowels:
            vowel_count += 1
            if vowel_count > 1:
                return False
    return vowel_count == 1


def lp_has_ratva_cause(lp):
    """Return True if lp contains a ratva cause (r, ṛ=f, ṣ=z) with ONLY vyavāya
    characters (aṭkupvāṅnum) to its right.
    
    Scans left-to-right for r/z/f/F. If found, checks that all characters to its
    right are vyavāya (vowels, ku/pu-class, anusvara). Returns False if any
    non-vyavāya character appears after the ratva cause."""
    if not lp:
        return False
    # Scan right-to-left: find the rightmost ratva cause first.
    # If it fails the vyavāya check, no cause further left can succeed either
    # (the same blocking char would be in its right-hand range too).
    for i in range(len(lp) - 1, -1, -1):
        if lp[i] in ('r', 'f', 'F', 'z'):
            return all(awkupvaNnum(lp[j]) for j in range(i + 1, len(lp)))
    return False


def rp_has_ratva_effect(rp):
    """Return True if rp contains 'n' with ONLY vyavāya characters to its left.
    
    Scans left-to-right for n. If found, checks that all characters to its left
    are vyavāya (vowels, ku/pu-class, anusvara). Returns False if any
    non-vyavāya character appears before the n."""
    if not rp:
        return False
    # Scan left-to-right for n
    for i, ch in enumerate(rp):
        if ch == 'n':
            # Found n at position i
            # Check that all characters to the left are vyavāya
            for j in range(0, i):
                if not awkupvaNnum(rp[j]):
                    return False
            return True
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


def ticAdesha_adri(s):
    """SK418: replace ṭi (final portion from last vowel onwards) of s with 'adri'."""
    for i in range(len(s)-1, -1, -1):
        if isInPratyahara('ac', SanskritImmutableString(s[i], encoding=sanscript.SLP1)):
            return s[:i] + "adri"
    return s  # fallback: no vowel found


def endsWith_pAd(lp):
    """True if lp ends in the compound-form of pāda (pAd = pād without terminal a).
    Used in SK414 (6.4.130): pāda → pad when anga is bha."""
    return len(lp) >= 3 and lp[-3:] == "pAd"


def ns_upadha_hrasva(lp):
    """True if lp ends in hrasva-vowel + n + s (upadhā is short before -ns cluster).
    Used in SK317 (6.4.10) block 1 to prevent firing when upadhā is already dīrgha
    (e.g. after SK425 has lengthened śreyas → śreyās before nUM → śreyāns)."""
    return (len(lp) >= 3 and lp[-1] == 's' and lp[-2] == 'n' and
            lp[-3] in ['a', 'i', 'u', 'f', 'x'])


def tyadAdiHasTorD(lp):
    """True if lp (tyadAdi after 7.2.102, so ending in 'a') has a t or d in non-final position.
    Used in 7.2.106 condition to confirm a t/d exists for s-substitution."""
    return any(c in ('t', 'd') for c in lp[:-1])


def replaceTorDwithS(lc):
    """Replace the rightmost t or d in lc with s (7.2.106 tadoḥ saḥ sāvanantyyayoḥ).
    Handles all tyadAdi stems after 7.2.102 has applied (final d/s → a).
    When the preceding vowel is in iR (includes e, o, i, u, …), the substitute is z (ṣ)
    per 8.3.59 (ādeśapratyayayoḥ) applied eagerly — the 's' ādeśa is embedded in lp
    content after this xform and cannot be reached by the outer 8.3.59 rule."""
    for i in range(len(lc) - 1, -1, -1):
        if lc[i] in ('t', 'd'):
            sub = 'z' if (i > 0 and isInPratyahara('iR', lc[i - 1])) else 's'
            return lc[:i] + sub + lc[i + 1:]
    return lc


def has_adas_amu(s):
    """SK419 (8.2.80) condition check: True if pada contains 'ad'+vowel (excluding 'ade').
    Accepts both str and PaninianObject (calls .canonical() if needed)."""
    if hasattr(s, 'canonical'):
        s = s.canonical()
    long_vowels = set('AIUFXeEoO')
    short_vowels = set('aiufx')
    all_vowels = long_vowels | short_vowels
    for i in range(len(s) - 2):
        if s[i] == 'a' and s[i+1] == 'd' and s[i+2] in all_vowels and s[i+2] != 'e':
            return True
    return False


def adas_amu_stem(s):
    """SK419 (8.2.80) xform helper: return replacement stem 'amu' (short) or 'amU' (long).
    Finds 'ad'+non-e vowel in s and returns the amu/amU stem only (no suffix)."""
    long_vowels = set('AIUFXeEoO')
    short_vowels = set('aiufx')
    all_vowels = long_vowels | short_vowels
    for i in range(len(s) - 2):
        if s[i] == 'a' and s[i+1] == 'd' and s[i+2] in all_vowels and s[i+2] != 'e':
            return 'amU' if s[i+2] in long_vowels else 'amu'
    return s


def adas_suffix(s):
    """SK419 (8.2.80) insert helper: return the suffix portion after 'ad'+non-e vowel.
    Used with insert: l to re-expose the suffix for downstream sandhi rules."""
    long_vowels = set('AIUFXeEoO')
    short_vowels = set('aiufx')
    all_vowels = long_vowels | short_vowels
    for i in range(len(s) - 2):
        if s[i] == 'a' and s[i+1] == 'd' and s[i+2] in all_vowels and s[i+2] != 'e':
            return s[i+3:]
    return ''


def adas_suffix_tagged(s):
    """SK419 (8.2.80) insert helper: return the suffix as a PaninianObject tagged ?pratyaya.
    This allows 8.3.59 (ṣatva: ādeśapratyayayoḥ) to fire at the amu|suffix junction,
    converting s→ṣ in smE/smAt/sya/smin after u."""
    from indic_transliteration import sanscript
    suffix = adas_suffix(s)
    po = PaninianObject(suffix, encoding=sanscript.SLP1)
    po.setTag("pratyaya")
    return po


def has_adas_ami(s):
    """SK438 (8.2.81) condition check: True if pada contains 'ade'.
    Accepts both str and PaninianObject (calls .canonical() if needed)."""
    if hasattr(s, 'canonical'):
        s = s.canonical()
    return 'ade' in s


def adas_ami(s):
    """SK438 (8.2.81) xform: within an adas pada, replace 'ade' → 'amI' (= amī, nom/acc/voc pl)."""
    idx = s.find('ade')
    if idx >= 0:
        return s[:idx] + 'amI' + s[idx+3:]
    return s


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
