"""
Antaranga Prakriya Engine for Panini Sutras

Takes in a list of Sutras, and executes them on a bunch of inputs

Inputs are provided at prakRti + pratyayas level. A list of such combinations
is provided. (ie: this is post karaka assignment and pratyaya selection).
For each future pada (prakRti + pratyayas), rules are executed, and output
padas are generated. Then, further rules are run on the padas themselves to
produce a vakya.

@author: kmadathil
"""

from abc import abstractmethod
from sanskrit_parser.generator.paninian_object import PaninianObject
from sanskrit_parser.generator.prakriya import PrakriyaVakya, PrakriyaBase, PrakriyaNode, PrakriyaTree, _isScalar
from sanskrit_parser.generator.pratyaya import Pratyaya
from sanskrit_parser.generator.sutra import Sutra

from copy import deepcopy, copy
import logging
logger = logging.getLogger(__name__)

    
class AntarangaPrakriya(PrakriyaBase):
    """
    Antaranga Prakriya Class


    Implement Antaranga algorithm based on Patanjali

    Inputs:
       sutra_list: list of Sutra objects
       inputs    : PrakriyaVakya object
    """
    def __init__(self, sutra_list, inputs):
        super().__init__(sutra_list, inputs)
        self.hier_prakriyas = []
        self.need_hier = False
        # List of alternatives
        # Used only in hierarchy is needed
        self.hier_inputs = [self.inputs]
        # Assmeble hierarchical prakriya outputs into a single list
        self.hier_outputs = [[] for x in self.inputs]
        # Scan inputs for hierarchical prakriya needs
        for ix in range(len(self.inputs)):
            if self.inputs.need_hierarchy_at(ix):
                self.need_hier = True
                # hierarchy needed here
                hp = AntarangaPrakriya(sutra_list,
                                       PrakriyaVakya(self.inputs[ix]))
                self.hier_prakriyas.append(hp)
                # This will execute hierarchically as needed
                hp.execute()
                hpo = hp.output()
                self.hier_outputs[ix] = hpo  # accumulate hierarchical outputs
        if self.need_hier:
            for ix, ol in enumerate(self.hier_outputs):
                if ol != []:  # Hierarchy exists here
                    tmpl = []
                    # For each alternate output
                    for o in ol:
                        hobj = PaninianObject.join_objects([o])
                        # Assemble exploded list with each input
                        # replaced by multiple alternates at this
                        # index
                        for i in self.hier_inputs:
                            tmpl.append(i.copy_replace_at(ix, hobj))
                    # Replace input list with exploded list
                    # Explosion at position ix is now dealt with
                    self.hier_inputs = tmpl
                    logger.debug(f"Hier inputs after expl {ix} {self.hier_inputs}")
            logger.debug(f"Hier inputs after full expl {self.hier_inputs} {[[_r.tags for _r in o] for o in self.hier_inputs]}")
            # At the end of the loop above self.hier_inputs has been fully exploded
            for i in self.hier_inputs:
                _n = PrakriyaNode(i, i, "Prakriya Hierarchical Start")
                self.tree.add_node(_n, root=True)
        else:
            _n = PrakriyaNode(self.inputs, self.inputs, "Prakriya Start")
            self.tree.add_node(_n, root=True)

        self.outputs = []
        self.disabled_sutras = []
        # Sliding window counter
        self.windowIdx = 0

    # pUrvaparanityAntaraNgApavAdAnamuttarottaraM balIyaH
    def sutra_priority(self, sutras: list):
        def _winner(s1, s2):
            logger.debug(f"{s1} bahiranga {s1.bahiranga} overrides {s1.overrides}")
            logger.debug(f"{s2} bahiranga {s2.bahiranga} overrides {s2.overrides}")
            # Apavada
            if (s2.overrides is not None) and (s1.aps in s2.overrides):
                logger.debug(f"{s2} overrides {s1}")
                return s2
            elif (s1.overrides is not None) and (s2.aps in s1.overrides):
                logger.debug(f"{s1} overrides {s2}")
                return s1
            # Nitya
            # Antaranga
            elif (s1.bahiranga < s2.bahiranga):
                logger.debug(f"{s1} antaranga {s2}")
                return s1
            elif (s2.bahiranga < s1.bahiranga):
                logger.debug(f"{s2} antaranga {s1}")
                return s2
            # samjYA before 1.4.2 vipratizeDe param kAryam
            elif (s1._aps_num < 14000) or (s2._aps_num < 14000):
                logger.debug(f"SaMjYA, lower of {s1} {s2}")
                if s1._aps_num < s2._aps_num:
                    return s1
                else:
                    return s2
            # Also handles if one sutra is spsp and one tp
            elif (s1._aps_num > 82000) or (s2._aps_num > 82000):
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
        # Wrapper for special "siddha" situations
        def _special_siddha(a1, a2):
            # zqutva is siddha for q lopa
            if (int(a1) == 84041) and (a2 == 83013):   # Int gets both the branches
                return True
            # q, r lopa siddha for purvadirgha
            elif ((a1 == 83013) or (a1 == 83014)) and (a2 == 63111):
                return True
            else:
                return False

        if s is not None:
            aps_num = s._aps_num
        else:
            aps_num = 0
        # Default view
        _l = self.inputs
        if node is None:
            # logger.debug(f"View {l} {node}")
            return _l
            
        if aps_num < 82000:
            # FIXME: Only Sapadasaptapadi implemented.
            # Need to implement asiddhavat, zutvatokorasiddhaH
            # Can see the entire sapadasaptapadi
            _n = node
            while (self.tree.parent[_n] is not None) and \
                  ((_n.sutra._aps_num > 82000)
                   and not _special_siddha(_n.sutra._aps_num, aps_num)):
                _n = self.tree.parent[_n]
            _l = _n.outputs
        else:
            # Asiddha
            # Can see all outputs of sutras less than oneself
            _n = node
            while (self.tree.parent[_n] is not None) and \
                  ((_n.sutra._aps_num > aps_num)
                   and not _special_siddha(_n.sutra._aps_num, aps_num)):
                _n = self.tree.parent[_n]
            _l = _n.outputs
        if ix > (len(_l)-2):
            # Someone has inserted something this sutra can't see
            logger.debug(f"Unseen insertion? {s} {_l} {ix}")
            ix = len(_l) - 2
        return _l[ix:ix+2]

    def _exec(self, node):
        l = self.sutra_list  # noqa: E741
        found_pratyaya = False
        found_samasa   = False
        found_pada     = False
        # Sliding window pass 1
        for ix in range(len(node.outputs)-1):
            if node.outputs[ix+1].hasTag('pratyaya'):
                found_pratyaya = 1
                logger.debug(f"Found pratyaya at {ix+1} {node.outputs[ix+1]}")
                logger.debug(f"Disabled Sutras at window {ix} {[s for s in node.outputs[ix].disabled_sutras]}")
                triggered = [s for s in l if ((s.aps not in node.outputs[ix].disabled_sutras)
                                          and s.isTriggered(*self.view(s, node, ix)))]
                # Break at first index from left where trigger occurs
                _ix = ix
                break
        if not found_pratyaya:
            for ix in range(len(node.outputs)-1):
                if node.outputs[ix].hasTag("samAsa"):
                    found_samasa = 1
                    logger.debug(f"Found samAsa at {ix} {node.outputs[ix+1]}")
                    logger.debug(f"Disabled Sutras at window {ix} {[s for s in node.outputs[ix].disabled_sutras]}")
                    triggered = [s for s in l if ((s.aps not in node.outputs[ix].disabled_sutras)
                                          and s.isTriggered(*self.view(s, node, ix)))]
                    # Break at first index from left where trigger occurs
                    _ix = ix
                    break
        if not (found_pratyaya or found_samasa):
            _ix = 0
            if len(node.outputs) != 1:
                triggered = [s for s in l if ((s.aps not in node.outputs[ix].disabled_sutras)  and s.isTriggered(*self.view(s, node, ix)))]

                #    assert node.outputs[0].hasTag("pada"), f"Expected pada at {0} got {node.outputs[0]}"
                #    assert node.outputs[0].hasTag("pada") or node.outputs[0].hasTag("avasAna"), f"Expected pada at {1} got {node.outputs[0]}"
            else:
                triggered = False
            
        logger.debug(f"I: {node.id} {node.outputs} {[_r.tags for _r in node.outputs]} ")
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
            r = s.update(*v, *r)
            r = s.insert(*v, *r)
            # Insertion - hierarchical prakriya
            for i in [0, 1]:
                if not _isScalar(r[i]):
                    logger.debug(f"Insertion hier prakriya for {r[i]}")
                    # need hierarchy here if we get list back
                    # hierarchy needed here
                    hp = AntarangaPrakriya(self.sutra_list,
                                           PrakriyaVakya(r[i]))
                    # This will execute hierarchically as needed
                    hp.execute()
                    hpo = hp.output()
                    logger.debug(f"Hier output for r[{i}] {hpo}")
                    assert len(hpo)==1, f"Unexpected multiple output {hpo} for insertion hier prakriya"
                    # Don't use join_object, since this is not a promotion but a replacement
                    r[i] = r[i][i]  # Appropriate sub-object for insertion
                    r[i].update("".join([o.canonical() for o in hpo[0]]))
                    
            logger.debug(f"I (post update): Node {node.id} Outputs {node.outputs} {[_r.tags for _r in node.outputs]} ")
            logger.debug(f"I (post update): View {v}")
            logger.debug(f"I (post update): Op/Update/Insert/Hier Result {r}")
            
            
            # Sutras that run disable not only themselves but the utsargas they override  from running again by the
            # pariBAzA "lakzye lakzaRaM sakfdeva pravartate" read with the traditional concept of ekavAkyatvam

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
            # FIXME: disable sutras for AkaqArAdekA saMjYA

            logger.debug(f"O: {r} {[_r.tags for _r in r]} Disabled: {[[s for s in _r.disabled_sutras] for _r in r]}")

                    
            # Update Prakriya Tree
            # Craft inputs and outputs based on viewed inputs
            # And generated outputs
            pnv = node.outputs.copy_replace_at(ix, v[0]).copy_replace_at(ix+1, v[1])
            pnr = node.outputs.copy_replace_at(ix, r[0]).copy_replace_at(ix+1, r[1])
            if len(r) > 2:
                for i in range(len(r)-2):
                    pnr = pnr.copy_insert_at(ix+i+2, r[i+2])
            _ps = PrakriyaNode(pnv, pnr, s, ix, [t for t in triggered if t != s])
            logger.debug(f'O Node: {str(_ps)} {[_r.tags for _r in _ps.outputs]}')
            if node is not None:
                self.tree.add_child(node, _ps, opt=s.optional)
            else:
                self.tree.add_node(_ps, root=True)
            return r
        else:
            logger.debug(f"Nothing triggered")
            if len(node.outputs) == 1:
                return False
            if found_pratyaya:
                logger.debug(f"Merging anga + pratyaya at {ix} {node.outputs[ix]} {node.outputs[ix+1]}")
            elif found_samasa:
                logger.debug(f"Merging samasa at {ix} {node.outputs[ix]} {node.outputs[ix+1]}")
            else:
                logger.debug(f"Merging pada at {ix} {node.outputs[ix]} {node.outputs[ix+1]}")
                         
            # Update Prakriya Tree
            # Craft inputs and outputs based on viewed inputs
            # And generated outputs
            pnv = node.outputs
            # Merge element at index
            mobj = PaninianObject.join_objects([pnv[ix:ix+2]])
            # Replace element at ix with merged element and delete next
            pnr = node.outputs.copy_replace_at(ix, mobj).delete_at(ix+1)
            _ps = PrakriyaNode(pnv, pnr, dummySamhitaSutra, ix, [])
            logger.debug(f'O Node: {str(_ps)} {[_r.tags for _r in _ps.outputs]}')
            self.tree.add_child(node, _ps)
            return True

    def execute(self):
        if self.need_hier:
            logger.debug(f"Input: {self.hier_inputs}")
        else:
            logger.debug(f"Input: {self.inputs}")
        done = []
        act = False
        # Initial run on input
        for r in self.tree.get_root():
            _act = self._exec(r)
            act = act or _act
        if (act):
            # Iterate over leaves if something triggered
            while (act):
                act = False
                for n in self.tree.get_leaves():
                    if n not in done:
                        res = self._exec(n)
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
            for n in self.tree.get_root():
                self.outputs.append(n.outputs)
        r = self.outputs
        logger.debug(f"Final Result: {r} {[[_r.tags for _r in o] for o in r]}\n")
        return r

    def describe(self):
        print("\nPrakriya")
        if self.hier_prakriyas != []:
            print(f"Pre Input {self.pre_inputs}")
        for h in self.hier_prakriyas:
            print("Hierarchical Prakriya")
            h.describe()
        print(f"Input {self.inputs}")
        self.tree.describe()
        print(f"Final Output {self.outputs} = {[''.join([str(x) for x in y]) for y in self.outputs]}\n\n")


    def name(self):
        return "Antaranga Prakriya"


# Dummy Sutra
dummySamhitaSutra = Sutra("samhitA", "0.0.0")
