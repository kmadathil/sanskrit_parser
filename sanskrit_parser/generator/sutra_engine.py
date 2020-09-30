"""
Operational Sutras

"""
from sanskrit_parser.base.sanskrit_base import SanskritImmutableString, SLP1

import logging
logger = logging.getLogger(__name__)

# Global Triggers
class GlobalTriggers(object):
    uran_trigger = False

# Sutra execution engine
class SutraEngine(object):

    @classmethod
    # pUrvaparanityAntaraNgApavAdAnamuttarottaraM balIyaH
    def sutra_priority(cls, sutras: list):
        _s = sutras
        # Apavada
        # Antaranga
        # Nitya
        # Para > purva
        aps_nums = [s._aps_num for s in sutras]
        nmax = aps_nums.index(max(aps_nums))
        smax = sutras[nmax]
        return smax
    
    @classmethod
    def _exec_single(cls,l,*args):
        triggered = [s for s in l if s.isTriggered(*args)]
        logger.info(f"I: {args}")
        if triggered:
            logger.info("Triggered rules")
            for t in triggered:
                logger.info(t)
            s = cls.sutra_priority(triggered)
            if len(triggered)!=1:
                logger.info(f"Winner {s}")
            s.update(*args) # State update
            r = s.operate(*args) # Transformation
            logger.info(f"O: {r}")
            return r
        else:
            logger.info(f"Nothing triggered")
            return False

    @classmethod
    def _exec(cls, l, *args):
        logger.info(f"Input: {args}")
        _r = cls._exec_single(l, *args)
        r = None
        while(_r):
            r = _r
            _r = cls._exec_single(l, *_r)
        if r is None: # Nothing got triggered
            r = args
        logger.info(f"Final Result: {str(r[0])+str(r[1])}\n\n")
        return r
    
    @classmethod
    def sandhi(cls, s1, s2, sandhi_sutra_list):
        r = cls._exec(sandhi_sutra_list, s1, s2)
        return r


    
# Base class
class Sutra(object):
    def __init__(self, name, aps):
        if isinstance(name, str):
            self.name = SanskritImmutableString(name, SLP1)
        else:
            self.name = name
        if isinstance(aps, str):
            self.aps = aps  # Adhaya.pada.sutra
            aps_t = [int(_x) for _x in aps.split(".")]
            self._aps_tuple = aps_t
        elif isinstance(aps, tuple):
            aps_t = aps
            self._aps_tuple = aps_t
            self.aps = '.'.join([str(x) for x in list(aps_t)])
        self._aps_num = aps_t[2]+aps_t[1]*1000+aps_t[0]*10000
        logger.info(f"Initialized {self}:  {self._aps_num}")
    def __str__(self):
        return f"{self.aps:7}: {str(self.name)}"
    
class SandhiSutra(Sutra):
    def __init__(self, name, aps, cond, xform, adhikara=None,
                 trig=None, update=None):
        super().__init__(name, aps)
        self.adhikara = adhikara
        self.cond = cond
        self.xform   = xform
        self.update_f = update
        self.trig = trig
    def inAdhikara(self, context):
        return self.adhikara(context)
    
    def isTriggered(self, s1, s2):
        # To check triggering, we define the following
        # l -> object to the left (s1)
        # r -> object to the right (s2)
        # e -> left tadanta (s1)[-1]
        # f -> s2[0]
        l = s1
        r = s2
        e = SanskritImmutableString(l.canonical()[-1], SLP1)
        f = SanskritImmutableString(r.canonical()[0], SLP1)
        if self.trig is not None:
            t = self.trig()
        else:
            t = True
        if self.cond is not None:
            c = self.cond(l, r, e, f)
        else:
            c = True
        return c and t

    def update(self, s1, s2):
        # To check triggering, we define the following
        # l -> object to the left (s1)
        # r -> object to the right (s2)
        # e -> left tadanta (s1)[-1]
        # f -> s2[0]
        l = s1
        r = s2
        e = SanskritImmutableString(l.canonical()[-1], SLP1)
        f = SanskritImmutableString(r.canonical()[0], SLP1)
        if self.update_f is not None:
            self.update_f(l, r, e, f)

    def operate(self, s1, s2):
        # To operate, we define the following
        # e -> left tadanta str(s1)[-1]
        # f -> str(s2)[0]
        # lne -> s1.canonical()[:-1]
        # rnf -> s2.canonical()[1:]
        # We take the string tuple returned, and update s1, s2
        l = s1.canonical()
        r = s2.canonical()
        e = l[-1]
        f = r[0]
        lne = l[:-1]
        rnf = r[1:]
        ret = self.xform(e, f, lne, rnf)
        s1.update(ret[0], SLP1)
        s2.update(ret[1], SLP1)
        return (s1, s2)
