# -*- coding: utf-8 -*-
"""
Sutra YAML Processor

@author: kmadathil
"""
from sanskrit_parser.generator.sutra import LRSutra
from sanskrit_parser.generator.maheshvara import *  # noqa: F403
from sanskrit_parser.generator.paribhasha import *  # noqa: F403
from sanskrit_parser.generator.pratyaya import *  # noqa: F403
from sanskrit_parser.generator.pratipadika import *  # noqa: F403

import logging
logger = logging.getLogger(__name__)


def process_yaml(y):
    '''
    Process yaml file to return sutras dict

    Inputs:
      y: Sutra Yaml
    Outputs
      sutra_dict: dict of sutras keyed by sutra id
    '''
    logger.debug(f'Processing YAML {y}')
    sutra_dict = {}
    for s in y:
        logger.debug(f"processing {s}")
        if "sutra" not in s:
            logger.error("No sutra name")
            assert False
        if "id" not in s:
            logger.error("No sutra id")
            assert False
        for c in ["condition", "domain", "xform", "update", "insert"]:
            if c not in s:
                s[c] = None
        if "bahiranga" not in s:
            s["bahiranga"] = 9    # Class 9 - other sutras
        # svar = "sutra_"+s["id"].replace(".", "_")
        sname = s["sutra"]
        soverrides = None
        sopt = False
        if "optional" in s:
            sopt = s["optional"]
        # 6.1.85 antādivat: single-substitute (ekādeśa) rules of the 6.1.84
        # adhikāra are flagged so the engine can mark the antādivat boundary
        # (substitute is "like the final of pūrva and the initial of para").
        spurvapara = bool(s.get("purvapara", False))
        if "overrides" in s:
            if isinstance(s["overrides"], str):
                soverrides = [s["overrides"]]
            else:
                soverrides = s["overrides"]
            logger.debug(f"Sutra {s['id']} Overrides {soverrides}")
        scond = None
        if s["condition"] is not None:
            def _exec_cond(s):
                logger.debug(f"Cond dict {s}")
                # FIXME Fix variables after fixing sutra_engine

                def _cond(env):
                    def _c(env):
                        # _s a dict
                        # LHS = variable
                        # RHS = _pratyahara , {variable}, or savarna
                        x = True
                        results = {}
                        for k in _s:
                            def _cond_single(sk, k):
                                if (sk[0] == "_"):
                                    # Pratyahara
                                    _x = isInPratyahara(sk[1:], k)  # noqa: F405
                                elif (sk[0:2] == "$$"):
                                    # function call
                                    _x = eval(f"{sk[2:]}(k)")
                                elif (sk[0] == "$"):
                                    # Variable
                                    _x = isSavarna(env[sk[1:]], k)  # noqa: F405
                                elif (sk[0:2] == "=!"):
                                    # Raw inequality
                                    _x = (sk[2:] != k.canonical())
                                elif (sk[0] == "="):
                                    # Raw equality
                                    _x = (sk[1:] == k.canonical())
                                elif (sk[0:2] == "?!"):  # Tag false check
                                    _x = not k.hasTag(sk[2:])
                                elif (sk[0] == "?"):  # Tag check
                                    _x = k.hasTag(sk[1:])
                                elif (sk[0] == "+"):  # It check
                                    _x = hasattr(k, 'hasIt') and k.hasIt(sk[1:])
                                else:
                                    _x = isSavarna(sk, k)   # noqa: F405
                                return _x
                            if isinstance(_s[k], list):
                                if _s[k][0] == "and":
                                    _x = True
                                    for sk in _s[k][1:]:
                                        _x = _x and _cond_single(sk, env[k])
                                else:
                                    _x = False
                                    for sk in _s[k]:
                                        _x = _x or _cond_single(sk, env[k])
                            else:
                                _x = _cond_single(_s[k], env[k])
                            results[k] = (_s[k], _x)
                            x = x and _x
                        parts = "  ".join(f"{k}:{v[0]}={'✓' if v[1] else '✗'}" for k, v in results.items())
                        logger.debug(f"Cond  {parts}  →  {'match' if x else 'no'}")
                        return x
                    # List implies an or condition
                    if isinstance(s, list):
                        _ret = False
                        for _s in s:
                            _ret = _ret or _c(env)
                        return _ret
                    else:
                        _s = s
                        return _c(env)
                return _cond

            scond = _exec_cond(s["condition"])

        sxform = None
        if s["xform"] is not None:
            def _exec_xform(s):
                logger.debug(f"Xform dict {s}")
                xdict = s
                # FIXME Fix variables after fixing sutra_engine

                def _xform(env):
                    # Don't Remove - keep for debug
                    # logger.debug(f"Env {env}")
                    # for k in env:
                    #    logger.debug(f"{k} {type(env[k])}")
                    _l = l = env["l"].canonical()  # noqa: E741, F841
                    _r = r = env["r"].canonical()  # noqa: E741, F841
                    _lc = lc = env["lc"].canonical()  # noqa: E741, F841
                    _rc = rc = env["rc"].canonical()  # noqa: E741, F841
                    # Execute transforms for predefined variables
                    # FIXME: We assume our code in xform is safe to eval
                    if "l" in xdict:
                        if xdict["l"] is not None:
                            _l = eval(xdict["l"])
                        else:
                            _l = ""
                    if "r" in xdict:
                        if xdict["r"] is not None:
                            _r = eval(xdict["r"])
                        else:
                            _r = ""
                    if "lc" in xdict:
                        if xdict["lc"] is not None:
                            _lc = eval(xdict["lc"])
                        else:
                            _lc = ""
                    if "rc" in xdict:
                        if xdict["rc"] is not None:
                            _rc = eval(xdict["rc"])
                        else:
                            _rc = ""
                    ret = [_lc+_l, _r+_rc]
                    logger.debug(f"Xform: {lc}{l}|{r}{rc} → {ret[0]}|{ret[1]}")
                    return ret
                return _xform
            sxform = _exec_xform(s["xform"])
        sinsert = None
        if s["insert"] is not None:
            def _exec_insert(s):
                logger.debug(f"insert dict {s}")
                idict = s

                def _insert(env):
                    _rv = {}
                    _l = l = env["l"].canonical()  # noqa: E741, F841
                    _r = r = env["r"].canonical()  # noqa: E741, F841
                    _lc = lc = env["lc"].canonical()  # noqa: E741, F841
                    _rc = rc = env["rc"].canonical()  # noqa: E741, F841
                    for i in idict:
                        _rv[i] = eval(idict[i])
                    logger.debug(f"Insert: {_rv}")
                    return _rv
                return _insert
            sinsert = _exec_insert(s["insert"])
        sdom = None
        if s["domain"] is not None:
            def _exec_trig(s):
                logger.debug(f"Domain: {s}")

                def _trig(domains):
                    # list of domains
                    if isinstance(s, list):
                        x = True
                        for t in s:
                            x = x and domains.isdomain(t)
                    else:
                        return domains.isdomain(s)
                return _trig
            sdom = _exec_trig(s["domain"])
        supdate = None
        if s["update"] is not None:

            def _exec_update(s):
                logger.debug(f"Update {s}")

                def _update(env):
                    def _c(env):
                        # _s a dict
                        # LHS = variable
                        # RHS = _pratyahara , {variable}, or savarna
                        x = True
                        for k in _s:
                            if (_s[k][0] == "_"):
                                # Pratyahara
                                _x = isInPratyahara(_s[k][1:], env[k])  # noqa: F405
                            elif (_s[k][0] == "$"):
                                # Variable
                                _x = isSavarna(env[_s[k][1:]], env[k])  # noqa: F405
                            else:
                                _x = isSavarna(_s[k], env[k])  # noqa: F405
                            x = x and _x
                        return x

                    for k in ["olp", "orp", "lp", "rp"]:
                        if k in s.keys():
                            # Set or remove one tag
                            def _tag(k, sk):
                                if sk[0:2] == "++":
                                    logger.debug(f"Setting {k} it {sk[2:]}")
                                    env[k].setIt(sk[2:])
                                elif sk[0:2] == "--":
                                    logger.debug(f"Removing {k} it {sk[1:]}")
                                    env[k].deleteIt(sk[2:])
                                elif sk[0] == "+":
                                    logger.debug(f"Setting {k} tag {sk[1:]}")
                                    env[k].setTag(sk[1:])
                                elif sk[0] == "-":
                                    logger.debug(f"Removing {k} tag {sk[1:]}")
                                    if env[k].hasTag(sk[1:]):
                                        env[k].deleteTag(sk[1:])
                                elif sk == "_lu":
                                    logger.debug("Removing all tags ")
                                    env[k].luTags()
                                elif sk[0] == "=":  # Replace
                                    logger.debug(f"Replacing {k} with {sk[1:]} {eval(sk[1:])}")
                                    env[k] = eval(sk[1:])  # Must be defined!

                            # Possibly set/remove multiple tags
                            if isinstance(s[k], list):
                                for sk in s[k]:
                                    _tag(k, sk)
                            else:
                                _tag(k, s[k])

                return _update
            supdate = _exec_update(s["update"])
        if s["id"] in sutra_dict:
            logger.error(f"Duplicate Sutra {s['id']} - {sutra_dict[s['id']]} and {sname}")
            assert False
        sutra_dict[s["id"]] = LRSutra(sname, s["id"],
                                      cond=scond,
                                      xform=sxform,
                                      insert=sinsert,
                                      domain=sdom,
                                      update=supdate,
                                      optional=sopt,
                                      bahiranga=s["bahiranga"],
                                      overrides=soverrides,
                                      purvapara=spurvapara)
        sutra_dict[s["id"]]._cond_dict     = s["condition"]  # raw YAML for per-subcondition detail
        sutra_dict[s["id"]]._cond_globals   = globals()       # eval namespace (includes all imports)

    return sutra_dict
