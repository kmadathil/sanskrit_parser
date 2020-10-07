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
        self.tree = PrakriyaTree()
        _n = PrakriyaNode(self.inputs, self.inputs, "Prakriya Start")
        self.tree.add_node(_n, root=True)
        self.outputs = []
        # FIXME- will optional sutras cause an issue for global triggers / disabled sutras?
        # Move triggers/disable into Prakriya Stage?
        self.triggers = GlobalTriggers() 
        self.disabled_sutras = []
        
    # pUrvaparanityAntaraNgApavAdAnamuttarottaraM balIyaH
    def sutra_priority(self, sutras: list):
        def _winner(s1, s2):
            logger.debug(f"{s1} overrides {s1.overrides}")
            logger.debug(f"{s2} overrides {s2.overrides}")
            # Apavada
            # Antaranga
            # Nitya
            if (s2.overrides is not None) and (s1.aps in s2.overrides):
                logger.debug(f"{s2} overrides {s1}")
                return s2
            elif (s1.overrides is not None) and (s2.aps in s1.overrides):
                logger.debug(f"{s1} overrides {s2}")
                return s1
            elif (s1._aps_num > 82000) and (s2._aps_num > 82000):
                logger.debug(f"Tripadi, lower of {s1} {s2}")
                if s1._aps_num < s2._aps_num:
                    return s1
                else:
                    return s2
            else:
                # Para > purva
                logger.debug(f"Sapadasaptapadi, higher of {s1} {s2}")
                if s1._aps_num > s2._aps_num:
                    return s1
                else:
                    return s2
        _s = sutras
        w = _s[0]
        for s in _s[1:]:
            w = _winner(w, s)
        return w
        
    def view(self, s, node):
        """
        Current view as seen by sutra s

        """
        if s is not None:
            aps_num = s._aps_num
        else:
            aps_num = 0
        # Default view
        l = self.inputs
        if node is None:
            #logger.debug(f"View {l} {node}")
            return l
        if aps_num < 82000:
            # FIXME: Only Sapadasaptapadi implemented.
            # Need to implement asiddhavat, zutvatokorasiddhaH
            # Can see the entire sapadasaptapadi
            _n = node
            while (self.tree.parent[_n] is not None) and (_n.sutra._aps_num > 82000):
                _n = self.tree.parent[_n]
            l = _n.outputs
        else:
            # Asiddha
            # Can see all outputs of sutras less than oneself
            _n = node
            while (self.tree.parent[_n] is not None) and (_n.sutra._aps_num > aps_num):
                _n = self.tree.parent[_n]
            l = _n.outputs
        #logger.debug(f"View {l} {node} {_n}")
        return l
    
    def _exec_single(self, node):
        l = self.sutra_list
        triggered = [s for s in l if ((not s in self.disabled_sutras)
                                      and s.isTriggered(*self.view(s, node), self.triggers))]
        logger.debug(f"I: {self.view(None, node)}")
        if triggered:
            logger.debug("Triggered rules")
            for t in triggered:
                logger.debug(t)
            s = self.sutra_priority(triggered)
            v = self.view(s, node)
            if len(triggered)!=1:
                logger.debug(f"Winner {s} View {v}")
            # Transformation
            r = s.operate(*v)
            # State update 
            s.update(*v, *r, self.triggers) 
            logger.debug(f"I*: {self.view(None, node)}")
            self.disabled_sutras.append(s)
            # Overridden sutras disabled
            if s.overrides is not None:
                for so in l:
                    if so.aps in s.overrides:
                        self.disabled_sutras.append(so)
                        logger.debug(f"Disabling overriden {so}")
            logger.debug(f"O: {r} {[_r.tags for _r in r]}")
            # Update Prakriya Tree
            _ps = PrakriyaNode(v, r, s, [t for t in triggered if t != s])
            if node is not None:
                self.tree.add_child(node, _ps, opt=s.optional)
            else:
                self.tree.add_node(_ps, root=True)
            #self.stages.append(_ps)
            
            return r
        else:
            logger.debug(f"Nothing triggered")
            return False

    def execute(self):
        logger.debug(f"Input: {self.inputs}")
        done = []
        # Initial run on input
        act = self._exec_single(self.tree.get_root())
        if (act):
            # Iterate over leaves if something triggered
            while (act):
                act = False
                for n in self.tree.get_leaves():
                    if n not in done:
                        res = self._exec_single(n)
                        if not res:
                            done.append(n)
                        else:
                            act = True
            for n in self.tree.get_leaves():
                assert n in done
                self.outputs.append(n.outputs)
        else:
            # Nothing triggered
            logger.debug("Nothing Triggered - Passthrough")
            self.outputs.append(self.inputs)
        r = self.outputs
        logger.debug(f"Final Result: {r}\n")
        return r
        # _r = self._exec_single()
        # r = None
        # while(_r):
        #     r = _r
        #     _r = self._exec_single()
        # if r is None: # Nothing got triggered
        #     self.outputs = self.inputs
        # else:
        #     self.outputs = self.stages[-1].outputs
        # r = self.outputs
        # logger.debug(f"Final Result: {r}\n")
        # return r
            
    def output(self):
        return self.outputs
    
    def describe(self):
        print("\nPrakriya")
        print(f"Input {self.inputs}")
        #for s in self.stages:
        #    s.describe()
        self.tree.describe()
        print(f"Final Output {self.outputs}\n\n")
            
class PrakriyaNode(object):
    """ 
    Prakriya History Node

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

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return str(self) != str(other)


    def describe(self):
        print("Prakriya Node")
        print(str(self))
        if self.other_sutras:
            print("Sutras that were tiggered but did not win")
            for s in self.other_sutras:
                print(str(s))
        print("End")
        

class PrakriyaTree(object):
    """ 
    Prakriya Tree: Tree of PrakriyaNodes
    """
    def __init__(self, node=None):
        self.children = {}
        self.parent = {}
        self.leaves = []
        self.roots = []
        if node is not None:
            self.add_node(node)

    def add_node(self, node, root=False):
        self.children[node] = []
        self.leaves.append(node)
        if root:
            self.parent[node] = None
            self.roots.append(node)

    def get_leaves(self):
        return self.leaves

    def get_root(self):
        return self.roots[0]

    def add_child(self, node, c, opt=False):
        self.children[node].append(c)
        assert (c not in self.parent)
        self.parent[c] = node
        if not c in self.children:
            self.add_node(c)
        if (not opt) and (node in self.leaves):
                self.leaves.remove(node)
            
    def describe(self):
        def _desc(n):
            n.describe()
            if n in self.leaves:
                print("Leaf Node")
            for c in self.children[n]:
                print("Child")
                _desc(c)
        for r in self.roots:
            print("Root")
            _desc(r)
            
