"""
Operational Sutras

"""
from indic_transliteration import sanscript
from sanskrit_parser.base.sanskrit_base import SanskritImmutableString
from decimal import Decimal
from copy import deepcopy
from sanskrit_parser.generator.paninian_object import PaninianObject

import inspect
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
        logger.debug(f"Initialized {self}:  {self._aps_num} Optional:{self.optional}")

    def __str__(self):
        if self.optional:
            _o = "*"
        else:
            _o = ""
        return f"{self.aps:7}: {str(self.name)} {_o}"


class LRSutra(Sutra):
    def __init__(self, name, aps, cond, xform, insert=None, domain=None,
                 update=None, optional=False, bahiranga=99, overrides=None,
                 purvapara=False, purvanipata=False):
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
        # 6.1.85 antādivat: True for the single-substitute (ekādeśa) rules of
        # the 6.1.84 (ekaḥ pūrvaparayoḥ) adhikāra. See AntarangaPrakriya._exec.
        self.purvapara = purvapara
        # 2.2.30 pūrva-nipāta: True for the member-ORDERING samāsa rules (2.2.31–37).
        # These run in the samāsa pre-pass's SWEEP 1 (before the saṁjñā rules), tag the
        # member that must go first ?pUrvanipAta, and _commit_purvanipata physically
        # reorders. Carved out of _samasa_sutras by _split_sutras.
        self.purvanipata = purvanipata

    def inAdhikara(self, context):
        return self.adhikara(context)

    def isInDomain(self, domains):
        if self.domain is not None:
            t = self.domain(domains)
        else:
            t = domains.isdomain("standard")
        return t

    def isTriggered(self, s1, s2, nitya_check=False, context=None):
        llp, rrp = context if context is not None else (None, None)
        env = _env(s1, s2, llp, rrp)
        if self.cond is not None:
            c = self.cond(env)
        else:
            c = True
        if logger.isEnabledFor(logging.DEBUG):
            n = "Nitya " if nitya_check else ""
            logger.debug(f"{'✓' if c else '·'} {n}{self}   {s1} | {s2}")
        return c

    def evalConditionDetail(self, s1, s2, context=None):
        """Re-evaluates condition with per-subcondition detail. Short-circuit preserved.
        Returns (passed: bool, detail: list[dict])
        where detail entries are {"var": str, "check": str, "result": bool}.
        """
        llp, rrp = context if context is not None else (None, None)
        _cond_dict    = getattr(self, '_cond_dict',    None)
        _cond_globals = getattr(self, '_cond_globals', {})
        if _cond_dict is None:
            result = self.cond(_env(s1, s2, llp, rrp)) if self.cond else True
            return result, []
        env = _env(s1, s2, llp, rrp)
        detail = []
        _isInPratyahara = _cond_globals.get('isInPratyahara')
        _isSavarna      = _cond_globals.get('isSavarna')

        def _single(sk, var_name):
            k = env[var_name]
            if sk[0] == "_":       r = _isInPratyahara(sk[1:], k)
            elif sk[:2] == "$$":
                # Parity with process_yaml._exec_cond: an env-aware helper (declaring a
                # 2nd parameter) is called (k, env) so it can read neighbour padas /
                # the other window slot (env['lp']/env['rp']); 1-arg helpers get (k).
                _fn = _cond_globals.get(sk[2:])
                if _fn is not None and len(inspect.signature(_fn).parameters) >= 2:
                    r = _fn(k, env)
                else:
                    r = eval(f"{sk[2:]}(k)", _cond_globals, {"k": k})
            elif sk[0] == "$":     r = _isSavarna(env[sk[1:]], k)
            elif sk[:2] == "=!":   r = (sk[2:] != k.canonical())
            elif sk[0] == "=":     r = (sk[1:] == k.canonical())
            elif sk[:2] == "?!":   r = not k.hasTag(sk[2:])
            elif sk[0] == "?":     r = k.hasTag(sk[1:])
            elif sk[0] == "+":     r = hasattr(k, 'hasIt') and k.hasIt(sk[1:])
            else:                  r = _isSavarna(sk, k)
            detail.append({"var": var_name, "check": sk, "result": r})
            return r

        # Mirror process_yaml._exec_cond: a value is a string leaf check or a list
        # group ("and"/"or"-led, or a bare list = OR); elements may be nested groups.
        def _eval_group(v, var_name):
            if isinstance(v, list):
                if v and v[0] == "and":
                    res = True
                    for e in v[1:]:
                        res = res and _eval_group(e, var_name)
                        if not res:
                            break
                    return res
                elif v and v[0] == "or":
                    res = False
                    for e in v[1:]:
                        res = res or _eval_group(e, var_name)
                        if res:
                            break
                    return res
                else:
                    res = False
                    for e in v:
                        res = res or _eval_group(e, var_name)
                        if res:
                            break
                    return res
            return _single(v, var_name)

        def _eval_one(_s):
            x = True
            for kv in _s:
                _x = _eval_group(_s[kv], kv)
                x = x and _x
            return x

        _cd = _cond_dict
        if isinstance(_cd, list):
            passed = any(_eval_one(_s) for _s in _cd)
        else:
            passed = _eval_one(_cd)
        return passed, detail

    def update(self, s1, s2, o1, o2, context=None):
        llp, rrp = context if context is not None else (None, None)
        env = _env(s1, s2, llp, rrp)
        env["olp"] = o1
        env["orp"] = o2
        if self.update_f is not None:
            self.update_f(env)
        return env["olp"], env["orp"]

    def operate(self, s1, s2, context=None):
        # We take the string tuple returned, and update s1, s2
        llp, rrp = context if context is not None else (None, None)
        rs1 = deepcopy(s1)
        rs2 = deepcopy(s2)
        if self.xform is not None:
            env = _env(s1, s2, llp, rrp, for_xform=True)
            ret = self.xform(env)
            rs1.update(ret[0], sanscript.SLP1)
            rs2.update(ret[1], sanscript.SLP1)
        return rs1, rs2

    def insert(self, s1, s2, o1, o2, context=None):
        if self.insertx is not None:
            llp, rrp = context if context is not None else (None, None)
            env = _env(s1, s2, llp, rrp)
            itx = self.insertx(env)
            r = [o1, o2]
            for i in itx:
                if not isinstance(itx[i], PaninianObject):
                    assert isinstance(itx[i], str)
                    itx[i] = PaninianObject(itx[i], encoding=sanscript.SLP1)

                # A "middle" insert is handled based on it
                # kit => append to left context
                # wit => prepend to right context
                # A list being returned in one of the contexts
                # will trigger a hier prakriya
                # left and right inserts are hierarchically merged
                # with the correct operand
                if ((i=="m") and itx[i].hasIt("k")) or i=="l":
                    r[0] = [r[0], itx[i]]
                elif ((i=="m") and itx[i].hasIt("w")) or i=="r":
                    r[1] = [itx[i], r[1]]
                else:
                    r[i] = [itx[i], r[i]]
            logger.debug(f"After insertion {r}")
            return r
        else:
            return(o1, o2)


def _env(s1, s2, llp=None, rrp=None, for_xform=False):
    # Helper function to define execution environment.
    # llp/rrp: read-only neighbour-pada context (generator branch).
    # for_xform=True (called from operate) skips the antādivat l/lc/ll synthesis
    # so xform reconstruction (ret = _lc+_l | _r+_rc) uses the PHYSICAL strings —
    # the synth is scoped to condition evaluation only, which avoids re-appending
    # the substitute onto the left on every firing (see the 6.1.85 block below).
    env = {}
    env["lp"] = s1
    env["rp"] = s2
    # Neighbour padas (read-only context): the pada before lp (ix-1) and after
    # rp (ix+2), when the engine supplies them. An empty PaninianObject sentinel
    # is used when a neighbour is absent so condition operators stay safe
    # (=x -> False, =!x -> True, ?tag -> False, ?!tag -> True).
    env["llp"] = llp if llp is not None else PaninianObject("")
    env["rrp"] = rrp if rrp is not None else PaninianObject("")
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
    # 6.1.85 antādivat: when an ekādeśa rule lumps the single substitute on the
    # RIGHT object (rp[0]), the left (pūrva) is truncated to a consonant even
    # though, by antādivat, its real final is now that substitute. The
    # ?antAdivat saṁjñā (set by the engine only in that case) makes the antavat
    # view explicit: 'l' = the substitute (rp[0]), 'lc' = the truncated stem,
    # 'll' = its real last char. This blocks consonant-keyed aṅga rules
    # (e.g. 6.4.8 l:n) on the truncated stem WITHOUT stripping its aṅga/Ba/pada
    # saṁjñās. 'r'/'rr'/'rc' are left natural: rp[0] IS the substitute, so the
    # ādivat reading (suffix-initial = substitute) is already correct, and
    # rule conditions on the suffix shape (e.g. 7.2.86 r:_hal) see the true
    # initial. Fresh vowel-sandhi at this resolved junction (6.1.77/6.1.78 and
    # the ekādeśa rules themselves) is instead suppressed via disabled_sutras.
    # Condition-scoped: skipped for xform so reconstruction uses physical strings.
    if (not for_xform) and getattr(s1, "hasTag", None) and s1.hasTag("antAdivat") \
            and s2.canonical() != "":
        rpc = s2.canonical()
        lpc = s1.canonical()
        env["l"] = SanskritImmutableString(rpc[0], sanscript.SLP1)
        env["lc"] = SanskritImmutableString(lpc, sanscript.SLP1)
        env["ll"] = SanskritImmutableString(lpc[-1] if lpc != "" else "", sanscript.SLP1)
    return env
