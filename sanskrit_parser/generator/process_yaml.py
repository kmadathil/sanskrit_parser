# -*- coding: utf-8 -*-
"""
Sutra YAML Processor

@author: kmadathil
"""
from sanskrit_parser.generator.sutra import SandhiSutra
from sanskrit_parser.generator.maheshvara import * 
from sanskrit_parser.generator.paribhasha import *

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
        if not "sutra" in s:
            logger.error("No sutra name")
            assert False
        if not "id" in s:
            logger.error("No sutra id")
            assert False
        for c in ["condition", "trigger", "xform", "update"]:
            if not c in s:
                s[c] = None
        svar = "sutra_"+s["id"].replace(".","_")
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
                                    _x = isInPratyahara(sk[1:], k)
                                elif (sk[0] == "$"):
                                    # Variable
                                    logger.debug(f"Checking variable {sk[1:]} {k}")
                                    _x = isSavarna(env[sk[1:]], k)
                                elif (sk[0] == "="):
                                    # Raw equality
                                    logger.debug(f"Checking raw {sk[1:]} {k}")
                                    _x = (sk[1:]==k.canonical())
                                else:
                                     logger.debug(f"Checking savarna {sk} {k} ")
                                     _x = isSavarna(sk, k)
                                logger.debug(f"Return {_x}")
                                return _x
                            if isinstance(_s[k], list):
                                logger.debug(f"List")
                                _x = False
                                for sk in _s[k]:
                                    _x = _x or _cond_single(sk, env[k])
                            else:
                                logger.debug(f"Single")
                                _x = _cond_single(_s[k], env[k])
                            logger.debug(f"Got {_x}")
                            x = x and _x
                        return x 
                    # List implies an or in condition
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
                    _l = l = env["l"].canonical()
                    _r = r = env["r"].canonical()
                    _lc = lc = env["lc"].canonical()
                    _rc = rc = env["rc"].canonical()
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
                            _lc =eval(xdict["lc"])
                        else:
                            _lc = ""
                    if "rc" in xdict:
                        if xdict["rc"] is not None:
                            _rc = eval(xdict["rc"])
                        else:
                            _rc = ""
                    logger.debug(f"After {_lc} {_l} {_r} {_rc}")
                    return _lc+_l, _r+_rc
                return _xform
            sxform = _exec_xform(s["xform"])
            logger.debug(f"Xform def {sxform}")
        strig = None
        if s["trigger"] is not None:
            logger.debug("Processing trigger")
            def _exec_trig(s):
                logger.debug(f"Trig {s}")
                def _trig(triggers):
                    # list of triggers
                    logger.debug(f"Trigger checks {s}")
                    if isinstance(s, list):
                        x = True
                        for t in s:
                            x = x and getattr(triggers, t)
                    else:
                        return getattr(triggers, s)
                return _trig
            strig =  _exec_trig(s["trigger"])
        supdate= None
        if s["update"] is not None:
            logger.debug("Processing update")
            def _exec_update(s):
                logger.debug(f"Update {s}")
                # FIXME: Fix variable names after fixing sutra engine
                def _update(env, triggers):
                    # FIXME: Fix variable names after fixing sutra engine
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
                                _x = isInPratyahara(_s[k][1:], env[k])
                            elif (_s[k][0] == "$"):
                                # Variable
                                logger.debug(f"Checking variable {_s[k][1:]} ")
                                _x = isSavarna(env[_s[k][1:]], env[k])
                            else:
                               _x = isSavarna(_s[k], env[k])              
                            logger.debug(f"Got {_x}")
                            x = x and _x
                        return x 
                    for k in s:
                        logger.debug(f"Updating trigger {k} {s[k]}")
                        cond = True
                        if "condition" in s[k]:
                            logger.debug(f"Update condition check {s[k]['condition']}")
                            # List implies an or in condition
                            if isinstance(s[k]['condition'], list):
                                cond = False
                                for _s in s[k]['condition']:
                                    cond = cond or _c(env) 
                            else:
                                _s = s[k]['condition']
                                cond = _c(env) 
                            logger.debug(f"Check got {cond}")
                        if cond:
                            setattr(triggers, k, s[k]["value"])
                return _update
            supdate = _exec_update(s["update"])
        if s["id"] in sutra_dict:
            logger.error(f"Duplicate Sutra {s['id']} - {sutra_dict[s['id']]} and sname")
            assert False
        sutra_dict[s["id"]] = SandhiSutra(sname, s["id"],
                                          cond=scond,
                                          xform=sxform, trig=strig,
                                          update=supdate,
                                          optional=sopt,
                                          overrides=soverrides)
            
    return sutra_dict
