from sanskrit_parser.base.maheshvara_sutra import MaheshvaraSutras
from sanskrit_parser.base.sanskrit_base import SanskritImmutableString, SLP1

ms = MaheshvaraSutras()


# Utility functions
# Pratyahara check
def isInPratyahara(p, s):
    if s == "":
        return False
    if isinstance(p, str):
        p = SanskritImmutableString(p, SLP1)
    if isinstance(s, str):
        s = SanskritImmutableString(s, SLP1)
    return ms.isInPratyahara(p, s)


# Savarna check
def isSavarna(p, s):
    if ((s == "") and (p != "") or (s != "") and (p == "")):
        return False
    elif ((s == "") and (p == "")):
        return True
    else:
        if isinstance(p, str):
            p = SanskritImmutableString(p, SLP1)
        if isinstance(s, str):
            s = SanskritImmutableString(s, SLP1)
        return ms.isSavarna(p, s)


__all__ = ["isInPratyahara", "isSavarna"]
