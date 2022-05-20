"""
Operational Sutras

"""
from indic_transliteration import sanscript
from sanskrit_parser.base.sanskrit_base import SanskritImmutableString
from decimal import Decimal
from copy import deepcopy
from sanskrit_parser.generator.paninian_object import PaninianObject

import logging
logger = logging.getLogger(__name__)


# Global Domains
class GlobalDomains(object):
    def __init__(self):
        self.domains = {
            "saMjYA": True,
            "upadeSa": False,
            "prakfti": False,
            "pratyaya": False,
            "aNga": False,
            "pada": False,
            "saMhitA": False,
            "standard": False
        }

    def isdomain(self, d):
        return self.domains[d]

    def set_domain(self, d):
        for k in self.domains:
            if k == d:
                self.domains[k] = True
            else:
                self.domains[k] = False

    def active_domain(self):
        r = []
        for k in self.domains:
            if self.domains[k]:
                r.append(k)
        return r


# Base class
class Sutra(object):
    def __init__(self, name, aps, optional=False, overrides=None):
        if isinstance(name, str):
            self.name = SanskritImmutableString(name)
        else:
            self.name = name
        if isinstance(aps, str):
            self.aps = aps   # Adhaya.pada.sutra
            aps_l = aps.split(".")
            aps_t = [int(_x) for _x in aps_l]
            if len(aps_l) > 3:  # Subsutra/Vartikam
                aps_sub = Decimal("0."+str(aps_t[-1]))
            else:
                aps_sub = 0
            self._aps_tuple = aps_t
        elif isinstance(aps, tuple):
            aps_t = aps
            self._aps_tuple = aps_t
            self.aps = '.'.join([str(x) for x in list(aps_t)])
        self._aps_num = aps_t[2]+aps_t[1]*1000+aps_t[0]*10000 + aps_sub
        self.overrides = overrides
        self.optional = optional
        logger.info(f"Initialized {self}:  {self._aps_num} Optional:{self.optional}")

    def __str__(self):
        if self.optional:
            _o = "*"
        else:
            _o = ""
        return f"{self.aps:7}: {str(self.name)} {_o}"


class LRSutra(Sutra):
    def __init__(self, name, aps, cond, xform, insert=None, domain=None,
                 update=None, optional=False, bahiranga=1, overrides=None):
        '''
        Sutra Class that expects a left and right input
        '''
        super().__init__(name, aps, optional, overrides)
        self.domain = domain
        self.cond = cond
        self.xform = xform
        self.update_f = update
        self.insertx = insert
        self.bahiranga = bahiranga  # Bahiranga score. Smaller wins

    def inAdhikara(self, context):
        return self.adhikara(context)

    def isTriggered(self, s1, s2, domains):
        logger.debug(f"Checking {self} View: {s1} {s2}")
        env = _env(s1, s2)
        if self.domain is not None:
            t = self.domain(domains)
        else:
            t = domains.isdomain("standard")
        if self.cond is not None:
            c = self.cond(env)
        else:
            c = True
        logger.debug(f"Check Result {c and t} for {self}")
        return c and t

    def update(self, s1, s2, o1, o2, domains):
        env = _env(s1, s2)
        env["olp"] = o1
        env["orp"] = o2
        if self.update_f is not None:
            self.update_f(env, domains)
        return env["olp"], env["orp"]

    def operate(self, s1, s2):
        # We take the string tuple returned, and update s1, s2
        rs1 = deepcopy(s1)
        rs2 = deepcopy(s2)
        if self.xform is not None:
            env = _env(s1, s2)
            ret = self.xform(env)
            rs1.update(ret[0], sanscript.SLP1)
            rs2.update(ret[1], sanscript.SLP1)
        return rs1, rs2

    def insert(self, s1, s2):
        if self.insertx is not None:
            env = _env(s1, s2)
            itx = self.insertx(env)
            r = [s1, s2]
            for i in itx:
                if not isinstance(itx[i], PaninianObject):
                    assert isinstance(itx[i], str)
                    itx[i] = PaninianObject(itx[i])
                r.insert(i, itx[i])
            logger.debug(f"After insertion {r}")
            return r
        else:
            return(s1, s2)


def _env(s1, s2):
    # Helper function to define execution environment
    env = {}
    env["lp"] = s1
    env["rp"] = s2
    if s1.canonical() == "":
        env["l"] = SanskritImmutableString("")
    else:
        env["l"] = SanskritImmutableString(s1.canonical()[-1], sanscript.SLP1)
    if s2.canonical() == "":
        env["r"] = SanskritImmutableString("")
    else:
        env["r"] = SanskritImmutableString(s2.canonical()[0], sanscript.SLP1)
    if len(s1.canonical()) > 1:
        env["ll"] = SanskritImmutableString(s1.canonical()[-2], sanscript.SLP1)
        env["lc"] = SanskritImmutableString(s1.canonical()[:-1], sanscript.SLP1)
    else:
        env["ll"] = SanskritImmutableString("")
        env["lc"] = SanskritImmutableString("")
    if len(s2.canonical()) > 1:
        env["rr"] = SanskritImmutableString(s2.canonical()[1], sanscript.SLP1)
        env["rc"] = SanskritImmutableString(s2.canonical()[1:], sanscript.SLP1)
    else:
        env["rr"] = SanskritImmutableString("", sanscript.SLP1)
        env["rc"] = SanskritImmutableString("", sanscript.SLP1)
    return env
