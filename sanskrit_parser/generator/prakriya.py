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
from sanskrit_parser.generator.paninian_object import PaninianObject
from copy import deepcopy, copy

class PrakriyaVakya(object):
    """
    Prakriya Vakya class

    Start with associated prakriti + pratyayas
    Assemble into padas
    Handle Pratyaya/String Agama / Lopa
    
    Inputs:
        v = list. 
        Elements of v can be PaninianObjects or
            lists thereof
    Internal storage:
       - List of lists of PaninianObject objects
    """
    def __init__(self, v):
        # Deepcopy is required because we add tags to objects
        # during prakriya, and we do not want predefined objects getting
        # tags. 
        self.v = deepcopy(list(v))

    def need_hierarchy_at(self, ix):
        return not _isScalar(self.v[ix])

    def copy_replace_at(self, ix, r):
        vc = PrakriyaVakya(self.v)
        # As above, deepcopy to prevent predefined objects getting tags
        vc.v[ix] = deepcopy(r)
        return vc

    def copy_insert_at(self, ix, r):
        vc = PrakriyaVakya(self.v)
        # As above, deepcopy to prevent predefined objects getting tags
        vc.v.insert(ix, deepcopy(r))
        return vc

    def replace_at(self, ix, r):
        # As above, deepcopy to prevent predefined objects getting tags
        self.v[ix] = deepcopy(r)
        return self

    def insert_at(self, ix, r):
        # As above, deepcopy to prevent predefined objects getting tags
        self.v.insert(ix, deepcopy(r))
        return self

    def __getitem__(self, ix):
        return self.v[ix]

    def __len__(self):
        return len(self.v)

    def __print__(self):
        return [str(x) for x in self.v]

    def __repr__(self):
        return str([str(x) for x in self.v])
        
class Prakriya(object):
    """
    Prakriya Class
    
    Inputs:
       sutra_list: list of Sutra objects
       inputs    : PrakriyaVakya object
    """
    def __init__(self, sutra_list, inputs):
        self.sutra_list = sutra_list
        self.pre_inputs = deepcopy(inputs)
        self.inputs = copy(inputs)
        self.hier_prakriyas = []
        # Scan inputs for hierarchical prakriya needs
        for ix in range(len(self.inputs)):
            if self.inputs.need_hierarchy_at(ix):
                # hierarchy needed here
                hp = Prakriya(sutra_list,
                              PrakriyaVakya(self.inputs[ix]))
                self.hier_prakriyas.append(hp)
                # This will execute hierarchically as needed
                hp.execute()
                hpo = PaninianObject.join_objects(hp.output())
                self.inputs.replace_at(ix, hpo)
        self.tree = PrakriyaTree()
        _n = PrakriyaNode(self.inputs, self.inputs, "Prakriya Start")
        self.tree.add_node(_n, root=True)
        self.outputs = []
        self.triggers = GlobalTriggers() 
        self.disabled_sutras = []
        # Sliding window counter
        self.windowIdx = 0
        
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
        
    def view(self, s, node, ix=0):
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
        if ix > (len(l)-2):
            # Someone has inserted something this sutra can't see
            logger.debug(f"Unseen insertion? {s} {l} {ix}") 
            ix = len(l) - 2
        return l[ix:ix+2]
    
    def _exec_single(self, node):
        l = self.sutra_list
        # Sliding window, check from left
        for ix in range(len(node.outputs)-1):
            logger.debug(f"Disabled Sutras at window {ix} {[s for s in node.outputs[ix].disabled_sutras]}")
            triggered = []
            triggered = [s for s in l if ((s.aps not in node.outputs[ix].disabled_sutras)
                                          and s.isTriggered(*self.view(s, node, ix), self.triggers))]
            # Break at first index from left where trigger occurs
            if triggered:
                _ix = ix
                break
        logger.debug(f"I: {node.outputs}")
        if triggered:
            ix = _ix
            logger.debug(f"Triggered rules at window {ix}")
            for t in triggered:
                logger.debug(t)
            s = self.sutra_priority(triggered)
            v = self.view(s, node, ix)
            logger.debug(f"Sutra {s} View {v} Disabled: {[s for s in v[0].disabled_sutras]}")
            assert s.aps not in v[0].disabled_sutras
            # Transformation
            r = s.operate(*v)
            r0 = r[0]
            v0 = v[0]
            # State update 
            s.update(*v, *r, self.triggers)
            r = s.insert(*r)
            logger.debug(f"I (post update): {v}")
            # Using sutra id in the disabled list to get round paninian object deepcopy
            r0.disabled_sutras.append(s.aps)
            if s.optional:
                # Prevent optional sutra from executing on the same node again
                v0.disabled_sutras.append(s.aps)
            # Overridden sutras disabled
            if s.overrides is not None:
                for so in l:
                    if so.aps in s.overrides:
                        r0.disabled_sutras.append(so.aps)
                        if s.optional:
                            # Prevent optional sutra's overridden sutras from executing on the same node again
                            v0.disabled_sutras.append(so.aps)
                        logger.debug(f"Disabling overriden {so}")
            logger.debug(f"O: {r} {[_r.tags for _r in r]} Disabled: {[[s for s in _r.disabled_sutras] for _r in r]}")
            # Update Prakriya Tree
            # Craft inputs and outputs based on viewed inputs
            # And generated outputs
            pnv = node.outputs.copy_replace_at(ix,v[0]).copy_replace_at(ix+1,v[1])
            pnr = node.outputs.copy_replace_at(ix,r[0]).copy_replace_at(ix+1,r[1])
            if len(r) > 2:
                for i in range(len(r)-2):
                    pnr = pnr.copy_insert_at(ix+i+2, r[i+2])
            _ps = PrakriyaNode(pnv, pnr, s, ix, [t for t in triggered if t != s])
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
        if self.hier_prakriyas != []:
            print(f"Pre Input {self.pre_inputs}")
        for h in self.hier_prakriyas:
            print("Hierarchical Prakriya")
            h.describe()
        print(f"Input {self.inputs}")
        #for s in self.stages:
        #    s.describe()
        self.tree.describe()
        print(f"Final Output {self.outputs}\n\n")

    def dict(self):
        return self.tree.dict()
    
class PrakriyaNode(object):
    """ 
    Prakriya History Node

    Inputs
        inputs : list of Paninian Objects
        outputs: list of Paninian Objects
       sutra_id: id for triggered sutra
   other_sutras: sutras that were triggered, but did not win.    
    """
    def __init__(self, inputs, outputs, sutra, ix=0, other_sutras=[]):
        self.inputs = inputs
        self.outputs = outputs
        self.sutra = sutra
        self.other_sutras = other_sutras
        self.index = ix
        
    def __str__(self):
        return f"{self.sutra} {self.inputs} {self.index}-> {self.outputs}"

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
        
    def dict(self):
        return {
            'sutra': str(self.sutra),
            'inputs': self.inputs,
            'outputs': self.outputs,
            'window': self.index,
            'other_sutras': [str(s) for s in self.other_sutras]
            }
    
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
        assert (c not in self.parent), f"Duplicated {c}, hash{c}"
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

    def dict(self):
        def _dict(n):
            d = n.dict()
            d['children'] = [_dict(c) for c in self.children[n]]
            return d
        return {
            'root': _dict(self.roots[0])
            }
        
            
def _isScalar(x):
    # We do not expect np arrays or other funky nonscalars here
    return not (isinstance(x, list) or isinstance(x, tuple))
