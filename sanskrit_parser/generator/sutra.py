"""
Operational Sutras

"""
from sanskrit_parser.base.sanskrit_base import SanskritImmutableString, SLP1
from decimal import Decimal
from copy import deepcopy

import logging
logger = logging.getLogger(__name__)

# Global Triggers
class GlobalTriggers(object):
    uran_trigger = False
    
# Base class
class Sutra(object):
    def __init__(self, name, aps, optional=False, overrides=None):
        if isinstance(name, str):
            self.name = SanskritImmutableString(name)
        else:
            self.name = name
        if isinstance(aps, str):
            self.aps = aps  # Adhaya.pada.sutra
            aps_l = aps.split(".")
            aps_t = [int(_x) for _x in aps_l]
            if len(aps_l) > 3: # Subsutra/Vartikam
                aps_sub = Decimal("0."+str(aps_t[-1]))
            else:
                aps_sub = 0
            self._aps_tuple = aps_t
        elif isinstance(aps, tuple):
            aps_t = aps
            self._aps_tuple = aps_t
            self.aps = '.'.join([str(x) for x in list(aps_t)])
        self._aps_num = aps_t[2]+aps_t[1]*1000+aps_t[0]*10000 + aps_sub
        self.enable()
        self.overrides = overrides
        self.optional = optional
        logger.info(f"Initialized {self}:  {self._aps_num} Optional:{self.optional}")

    def enable(self):
        self._enable = True

    def disable(self):
        self._enable = False

    def isEnabled(self):
        return self._enable

    def __str__(self):
        if self.optional:
            _o = "*"
        else:
            _o = ""
        return f"{self.aps:7}: {str(self.name)} {_o}"
    
class SandhiSutra(Sutra):
    def __init__(self, name, aps, cond, xform, adhikara=None,
                 trig=None, update=None, optional=False, overrides=None):
        super().__init__(name, aps, optional, overrides)
        self.adhikara = adhikara
        self.cond = cond
        self.xform   = xform
        self.update_f = update
        self.trig = trig
    
    def inAdhikara(self, context):
        return self.adhikara(context)
    
    def isTriggered(self, s1, s2, triggers):
        # To check triggering, we define the following
        env = {}
        env["lp"] = s1
        env["rp"] = s2
        env["l"] = SanskritImmutableString(s1.canonical()[-1], SLP1)
        env["r"] = SanskritImmutableString(s2.canonical()[0], SLP1)
        env["ll"] = SanskritImmutableString(s1.canonical()[-2], SLP1)
        env["rr"] = SanskritImmutableString(s2.canonical()[1], SLP1)
        env["lc"] = SanskritImmutableString(s1.canonical()[:-1], SLP1)
        env["rc"] = SanskritImmutableString(s2.canonical()[1:], SLP1)
        if self.trig is not None:
            t = self.trig(triggers)
        else:
            t = True
        if self.cond is not None:
            c = self.cond(env)
        else:
            c = True
        return c and t

    def update(self, s1, s2, triggers):
        # To check triggering, we define the following
        env = {}
        env["lp"] = s1
        env["rp"] = s2
        env["l"] = SanskritImmutableString(s1.canonical()[-1], SLP1)
        env["r"] = SanskritImmutableString(s2.canonical()[0], SLP1)
        env["ll"] = SanskritImmutableString(s1.canonical()[-2], SLP1)
        env["rr"] = SanskritImmutableString(s2.canonical()[1], SLP1)
        env["lc"] = SanskritImmutableString(s1.canonical()[:-1], SLP1)
        env["rc"] = SanskritImmutableString(s2.canonical()[1:], SLP1)
        if self.update_f is not None:
            self.update_f(env, triggers)

    def operate(self, s1, s2):
        if self.xform is not None:
            # To operate, we define the following
            env = {}
            env["lp"] = s1
            env["rp"] = s2
            env["l"] = SanskritImmutableString(s1.canonical()[-1], SLP1)
            env["r"] = SanskritImmutableString(s2.canonical()[0], SLP1)
            env["ll"] = SanskritImmutableString(s1.canonical()[-2], SLP1)
            env["rr"] = SanskritImmutableString(s2.canonical()[1], SLP1)
            env["lc"] = SanskritImmutableString(s1.canonical()[:-1], SLP1)
            env["rc"] = SanskritImmutableString(s2.canonical()[1:], SLP1)
            ret = self.xform(env)
            # We take the string tuple returned, and update s1, s2
            rs1 = deepcopy(s1)
            rs1.update(ret[0], SLP1)
            rs2 = deepcopy(s2)
            rs2.update(ret[1], SLP1)
            return (rs1, rs2)
        else:
            return (s1, s2)


