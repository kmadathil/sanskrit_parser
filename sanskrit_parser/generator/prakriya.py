"""
Prakriya Engine for Panini Sutras

Takes in a list of Sutras, and executes them on a bunch of inputs

Inputs are provided at prakRti + pratyayas level. A list of such combinations 
is provided. (ie: this is post karaka assignment and pratyaya selection). 
For each future pada (prakRti + pratyayas), rules are executed, and output 
padas are generated. Then, further rules are run on the padas themselves to
produce a vakya.  

@author: kmadathil

"""

import logging
logger = logging.getLogger(__name__)
from sanskrit_parser.generator.sutra import GlobalTriggers

class Prakriya(object):
    """
    Prakriya Class
    
    Inputs:
       sutra_list: list of Sutra objects
       inputs    : list of PaninianObject objects
    """
    def __init__(self, sutra_list, inputs):
        self.sutra_list = sutra_list
        self.inputs = inputs
        self.stages = []
        self.outputs = []
        self.disabled_sutras = []
        self.triggers = GlobalTriggers()
        
    # pUrvaparanityAntaraNgApavAdAnamuttarottaraM balIyaH
    def sutra_priority(self, sutras: list):
        _s = sutras
        # Apavada
        # Antaranga
        # Nitya
        # Para > purva
        aps_nums = [s._aps_num for s in sutras]
        nmax = aps_nums.index(max(aps_nums))
        smax = sutras[nmax]
        return smax

    def view(self, s):
        """
        Current view as seen by sutra s

        """
        if s is not None:
            aps_num = s._aps_num
        else:
            aps_num = 0
        # Default view
        l = self.inputs
        if aps_num < 82000:
            # FIXME: Only Sapadasaptapadi implemented.
            # Need to implement asiddhavat, zutvatokorasiddhaH
            # Can see the entire sapadasaptapadi
            for s in reversed(self.stages):
                if s.sutra._aps_num < 82000:
                    l = s.outputs
                    break
        else:
            # Asiddha
            # Can see all outputs of sutras less than oneself
            for s in reversed(self.stages):
                if s.sutra._aps_num < aps_num:
                    l = s.outputs
                    break
        return l
    
    def _exec_single(self):
        l = self.sutra_list
        triggered = [s for s in l if ((not s in self.disabled_sutras)
                                      and s.isTriggered(*self.view(s), self.triggers))]
        logger.debug(f"I: {self.view(None)}")
        if triggered:
            logger.debug("Triggered rules")
            for t in triggered:
                logger.debug(t)
            s = self.sutra_priority(triggered)
            v = self.view(s)
            if len(triggered)!=1:
                logger.debug(f"Winner {s} View {v}")
            s.update(*v, self.triggers) # State update
            r = s.operate(*v) # Transformation
            logger.debug(f"I*: {self.view(None)}")
            self.disabled_sutras.append(s)
            # Overridden sutras disabled
            if s.overrides is not None:
                for so in l:
                    if so.aps in s.overrides:
                        self.disabled_sutras.append(so)
                        logger.debug(f"Disabling overriden {so}")
            logger.debug(f"O: {r}")
            # Update Prakriya Stages
            _ps = PrakriyaStage(v, r, s, [t for t in triggered if t != s])
            self.stages.append(_ps)
            return r
        else:
            logger.debug(f"Nothing triggered")
            return False

    def execute(self):
        logger.debug(f"Input: {self.inputs}")
        _r = self._exec_single()
        r = None
        while(_r):
            r = _r
            _r = self._exec_single()
        if r is None: # Nothing got triggered
            self.outputs = self.inputs
        else:
            self.outputs = self.stages[-1].outputs
        r = self.outputs
        logger.debug(f"Final Result: {r}\n")
        return r
            
    def output(self):
        return self.outputs
    
    def describe(self):
        print("\nPrakriya")
        print(f"Input {self.inputs}")
        for s in self.stages:
            s.describe()
        print(f"Final Output {self.outputs}\n\n")
            
class PrakriyaStage(object):
    """ 
    Prakriya History Stage

    Inputs
        inputs : list of Paninian Objects
        outputs: list of Paninian Objects
       sutra_id: id for triggered sutra
   other_sutras: sutras that were triggered, but did not win.    
    """
    def __init__(self, inputs, outputs, sutra, other_sutras=[]):
        self.inputs = inputs
        self.outputs = outputs
        self.sutra = sutra
        self.other_sutras = other_sutras
        
    def __str__(self):
        return f"{self.sutra} {self.inputs} -> {self.outputs}"

    def describe(self):
        print("Prakriya Stage")
        print(str(self))
        if self.other_sutras:
            print("Sutras that were tiggered but did not win")
            for s in self.other_sutras:
                print(str(s))
        print("End")
        
