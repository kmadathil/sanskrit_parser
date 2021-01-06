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
            s["bahiranga"] = 1
        # svar = "sutra_"+s["id"].replace(".", "_")
        sname = s["sutra"]
        soverrides = None
        sopt = False
        if "optional" in s:
            sopt = s["optional"]
        if "overrides" in s:
            if isinstance(s["overrides"], str):
                soverrides = [s["overrides"]]
            else:
                soverrides = s["overrides"]
            logger.debug(f"Sutra {s['id']} Overrides {soverrides}")
        scond = None
        if s["condition"] is not None:
            logger.debug("Processing Condition")

            def _exec_cond(s):
                logger.debug(f"Cond dict {s}")
                # FIXME Fix variables after fixing sutra_engine

                def _cond(env):
                    def _c(env):
                        # _s a dict
                        # LHS = variable
                        # RHS = _pratyahara , {variable}, or savarna
                        x = True
                        for k in _s:
                            logger.debug(f"Checking cond {_s[k]} against {k}")

                            def _cond_single(sk, k):
                                if (sk[0] == "_"):
                                    # Pratyahara
                                    logger.debug(f"Checking pratyahara {sk[1:]} {k}")
                                    _x = isInPratyahara(sk[1:], k)  # noqa: F405
                                elif (sk[0:2] == "$$"):
                                    # function call
                                    logger.debug(f"Checking function {sk[2:]} {k}")
                                    _x = eval(f"{sk[2:]}(k)")
                                elif (sk[0] == "$"):
                                    # Variable
                                    logger.debug(f"Checking variable {sk[1:]} {k}")
                                    _x = isSavarna(env[sk[1:]], k)  # noqa: F405
                                elif (sk[0] == "="):
                                    # Raw equality
                                    logger.debug(f"Checking raw {sk[1:]} {k}")
                                    _x = (sk[1:] == k.canonical())
                                elif (sk[0:2] == "!="):
                                    # Raw inequality
                                    logger.debug(f"Checking raw inequality {sk[2:]} {k}")
                                    _x = (sk[2:] != k.canonical())
                                elif (sk[0:2] == "?!"):  # Tag false check
                                    logger.debug(f"Checking tag false {sk[2:]} {k}")
                                    _x = not k.hasTag(sk[2:])
                                elif (sk[0] == "?"):  # Tag check
                                    logger.debug(f"Checking tag {sk[1:]} {k}")
                                    _x = k.hasTag(sk[1:])
                                elif (sk[0] == "+"):  # It check
                                    logger.debug(f"Checking it {sk[1:]} {k}")
                                    _x = k.hasTag("pratyaya") and k.hasIt(sk[1:])
                                else:
                                    logger.debug(f"Checking savarna {sk} {k} ")
                                    _x = isSavarna(sk, k)   # noqa: F405
                                logger.debug(f"Return {_x}")
                                return _x
                            if isinstance(_s[k], list):
                                logger.debug("List")
                                if _s[k][0] == "and":
                                    logger.debug("Checking and condition")
                                    _x = True
                                    for sk in _s[k][1:]:
                                        _x = _x and _cond_single(sk, env[k])
                                else:
                                    _x = False
                                    for sk in _s[k]:
                                        _x = _x or _cond_single(sk, env[k])
                            else:
                                logger.debug("Single")
                                _x = _cond_single(_s[k], env[k])
                            logger.debug(f"Got {_x}")
                            x = x and _x
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
            logger.debug("Processing Xform")

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
                    logger.debug(f"Xform dict {xdict}")
                    logger.debug(f"Before: {_lc} {_l} {_r} {_rc}")
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
                    logger.debug(f"After {_lc} {_l} {_r} {_rc}")
                    ret = [_lc+_l, _r+_rc]
                    return ret
                return _xform
            sxform = _exec_xform(s["xform"])
            logger.debug(f"Xform def {sxform}")
        sinsert = None
        if s["insert"] is not None:
            logger.debug("Processing insert")

            def _exec_insert(s):
                logger.debug(f"insert dict {s}")
                idict = s

                def _insert(env):
                    _r = {}
                    for i in idict:
                        logger.debug(f"Insert {i} {idict[i]}")
                        _r[i] = eval(idict[i])
                    return _r
                return _insert
            sinsert = _exec_insert(s["insert"])
            logger.debug(f"Insert def {sinsert}")
        sdom = None
        if s["domain"] is not None:
            logger.debug("Processing domain")

            def _exec_trig(s):
                logger.debug(f"Trig {s}")

                def _trig(domains):
                    # list of domains
                    logger.debug(f"Domain checks {s}")
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
            logger.debug("Processing update")

            def _exec_update(s):
                logger.debug(f"Update {s}")

                def _update(env, domains):
                    def _c(env):
                        # _s a dict
                        # LHS = variable
                        # RHS = _pratyahara , {variable}, or savarna
                        x = True
                        for k in _s:
                            logger.debug(f"Checking cond {_s[k]} against {k}")
                            if (_s[k][0] == "_"):
                                # Pratyahara
                                logger.debug(f"Checking pratyahara {_s[k][1:]}")
                                _x = isInPratyahara(_s[k][1:], env[k])  # noqa: F405
                            elif (_s[k][0] == "$"):
                                # Variable
                                logger.debug(f"Checking variable {_s[k][1:]} ")
                                _x = isSavarna(env[_s[k][1:]], env[k])  # noqa: F405
                            else:
                                _x = isSavarna(_s[k], env[k])  # noqa: F405
                            logger.debug(f"Got {_x}")
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

                    if "domain" in s.keys():
                        st = s["domain"]
                        for k in st:
                            logger.debug(f"Updating domain {k} {st[k]}")
                            cond = True
                            if "condition" in st[k]:
                                logger.debug(f"Update condition check {st[k]['condition']}")
                                # List implies an or in condition
                                if isinstance(st[k]['condition'], list):
                                    cond = False
                                    for _s in st[k]['condition']:
                                        cond = cond or _c(env)
                                else:
                                    _s = st[k]['condition']
                                    cond = _c(env)
                                logger.debug(f"Check got {cond}")
                            if cond:
                                setattr(domains, k, st[k]["value"])
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
                                      overrides=soverrides)

    return sutra_dict
