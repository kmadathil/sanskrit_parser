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
from decimal import Decimal
from indic_transliteration import sanscript
from sanskrit_parser.generator.paninian_object import PaninianObject
from sanskrit_parser.generator.prakriya import PrakriyaVakya, PrakriyaBase, PrakriyaNode, PrakriyaTree, _isScalar
from sanskrit_parser.generator.pratyaya import Pratyaya
from sanskrit_parser.generator.sutra import Sutra

from copy import deepcopy, copy
import logging
logger = logging.getLogger(__name__)


def _deduplicate_hier_outputs(outputs):
    """If all PrakriyaVakya outputs produce the same canonical string,
    return a single-element list. Otherwise return the original list."""
    if len(outputs) <= 1:
        return outputs
    canonicals = ["".join(str(x) for x in y) for y in outputs]
    if all(c == canonicals[0] for c in canonicals):
        return [outputs[0]]
    return outputs

    
class AntarangaPrakriya(PrakriyaBase):
    """
    Antaranga Prakriya Class


    Implement Antaranga algorithm based on Patanjali

    Inputs:
       sutra_list: list of Sutra objects
       inputs    : PrakriyaVakya object
    """
    def __init__(self, sutra_list, inputs, initially_disabled=None, capture_eval=False):
        super().__init__(sutra_list, inputs)
        # Set to True to capture per-step evaluation data (opt-in; slower)
        # Must be set before the inner prakriya loop so inner prakriyas inherit it.
        self._capture_eval = capture_eval
        # Apply initially-disabled sutras AFTER PrakriyaVakya's deepcopy so they
        # are visible inside this prakriya.  Used by insert hier prakriyas to honour
        # the triggering sutra's `overrides:` list (the outer disabled_sutras update
        # only runs after the hier prakriya completes, so we must seed it here).
        if initially_disabled is not None:
            for aps in initially_disabled:
                self.inputs[0].disabled_sutras.append(aps)
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
                                       PrakriyaVakya(self.inputs[ix]),
                                       capture_eval=self._capture_eval)
                self.hier_prakriyas.append(hp)
                # This will execute hierarchically as needed
                hp.execute()
                hpo = _deduplicate_hier_outputs(hp.output())
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
                    logger.debug(f"Hier inputs after expl {ix}: {self.hier_inputs}")
            logger.debug(f"Hier inputs after full expl: {self.hier_inputs}")
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
    def sutra_priority(self, sutras: list, v):
        def _nitya(s1, s):     # S1 is still triggered after S applied
            if s not in _o:
                # New copy of prev node outputs
                # We assume both sutras can see it, since that's the only case
                # which matters for nitya test.
                # FIXME - check if this holds for asiddhavat and zutvatokorasiddhaH
                # Transformation
                logger.debug(f"Nitya check: Hypothetical execution of {s}")
                r = s.operate(*v)
                r0 = r[0]
                v0 = v[0]
                # State update
                vc = deepcopy(v)
                r = s.update(*vc, *r)
                r = s.insert(*v, *r)
                # Insertion - hierarchical prakriya
                for i in [0, 1]:
                    if not _isScalar(r[i]):
                        logger.debug(f"Nitya check: Hypothetical insertion hier prakriya for {r[i]}")
                        # need hierarchy here if we get list back
                        # hierarchy needed here
                        hp = AntarangaPrakriya(self.sutra_list,
                                               PrakriyaVakya(r[i]),
                                               initially_disabled=s.overrides)
                        # This will execute hierarchically as needed
                        hp.execute()
                        hpo = _deduplicate_hier_outputs(hp.output())
                        logger.debug(f"Nitya check: Hypothetical Hier output for r[{i}] {hpo}")
                        assert len(hpo)==1, f"Unexpected multiple output {hpo} for insertion hier prakriya"
                        # Don't use join_object, since this is not a promotion but a replacement
                        r[i] = r[i][i]  # Appropriate sub-object for insertion
                        r[i].update("".join([o.canonical() for o in hpo[0]]))
                        logger.debug(f"Nitya Check: Hypothetical  Result {r}")
                _o[s] = r    # Cache output
            # We have the output of s in cache _o[s]
            # Check if s1 is still triggered
            nit = (s1.aps not in v[0].disabled_sutras) and \
                s1.isTriggered(*_o[s])
            logger.debug(f"Nitya check {s1} against {s}: {nit}")
            return nit 
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
                n1 = _nitya(s1, s2)
                n2 = _nitya(s2, s1)
                assert ((s1._aps_num < 82000) and (s2._aps_num < 82000)), \
                    "Unexpected Nitya Check, not in SPSP {s1} {s2}"
                if n1 and not n2:
                    logger.debug(f"{s1} nitya against {s2}")
                    return s1
                if n2 and not n1:
                    logger.debug(f"{s2} nitya against {s1}")
                    return s2
                # Para > purva
                logger.debug(f"Sapadasaptapadi, higher of {s1} {s2}")
                if s1._aps_num > s2._aps_num:
                    return s1
                else:
                    return s2
        _s = sutras
        # First level, strip out apavada-overriden sutras to avoid 3-way problems
        overrides = []
        for s in _s:
            if s.overrides is not None:
                overrides.extend(s.overrides)
        logger.debug(f"Apavada overridden sutras {overrides}")
        for so in _s:
            if so.aps in overrides:
                logger.debug(f"Removing {so} as it is overriden")
                _s.remove(so)
        logger.debug(f"After apavada deletion: {[str(s) for s in _s]}")
        _o = {}    # Will be filled in if needed
        w = _s[0]
        for s in _s[1:]:
            w = _winner(w, s)
        return w

    def sutra_priority_detail(self, sutras: list, v):
        """Like sutra_priority but returns (winner, trace) for display.
        trace entries: {"s1": aps, "s2": aps, "winner": aps, "reason": str}
        """
        if len(sutras) <= 1:
            return (sutras[0] if sutras else None), []
        trace = []
        _o = {}

        def _nitya(s1, s):
            if s not in _o:
                r = s.operate(*v)
                vc = deepcopy(v)
                r = s.update(*vc, *r)
                r = s.insert(*v, *r)
                for i in [0, 1]:
                    if not _isScalar(r[i]):
                        hp = AntarangaPrakriya(self.sutra_list, PrakriyaVakya(r[i]),
                                               initially_disabled=s.overrides)
                        hp.execute()
                        hpo = _deduplicate_hier_outputs(hp.output())
                        r[i] = r[i][i]
                        r[i].update("".join([o.canonical() for o in hpo[0]]))
                _o[s] = r
            return (s1.aps not in v[0].disabled_sutras) and s1.isTriggered(*_o[s])

        def _winner_reason(s1, s2):
            if (s2.overrides is not None) and (s1.aps in s2.overrides):
                return s2, f"apavāda: {s2.aps} overrides {s1.aps}"
            elif (s1.overrides is not None) and (s2.aps in s1.overrides):
                return s1, f"apavāda: {s1.aps} overrides {s2.aps}"
            elif s1.bahiranga < s2.bahiranga:
                return s1, f"antaraṅga: {s1.aps} (score {s1.bahiranga}) beats {s2.aps}"
            elif s2.bahiranga < s1.bahiranga:
                return s2, f"antaraṅga: {s2.aps} (score {s2.bahiranga}) beats {s1.aps}"
            elif (s1._aps_num < 14000) or (s2._aps_num < 14000):
                w = s1 if s1._aps_num < s2._aps_num else s2
                return w, f"saṃjñā: lower APS wins ({w.aps})"
            elif (s1._aps_num > 82000) or (s2._aps_num > 82000):
                w = s1 if s1._aps_num < s2._aps_num else s2
                return w, f"tripadī: lower APS wins ({w.aps})"
            else:
                n1 = _nitya(s1, s2)
                n2 = _nitya(s2, s1)
                if n1 and not n2:
                    return s1, f"nitya: {s1.aps} still triggered after {s2.aps} applied"
                elif n2 and not n1:
                    return s2, f"nitya: {s2.aps} still triggered after {s1.aps} applied"
                else:
                    w = s1 if s1._aps_num > s2._aps_num else s2
                    return w, f"para-pūrva: higher APS wins ({w.aps})"

        # Strip apavāda-overridden sutras first (mirrors sutra_priority)
        _s = list(sutras)
        override_by = {}  # removed_aps -> overrider_aps
        for s in _s:
            if s.overrides is not None:
                for o in s.overrides:
                    override_by[o] = s.aps
        for so in list(_s):
            if so.aps in override_by:
                overrider = override_by[so.aps]
                trace.append({"s1": so.aps, "s2": "—", "winner": "—",
                              "reason": f"Removed: {overrider} is an apavāda of {so.aps}"})
                _s.remove(so)
        if not _s:
            return sutras[0], trace
        w = _s[0]
        for s in _s[1:]:
            winner, reason = _winner_reason(w, s)
            trace.append({"s1": w.aps, "s2": s.aps, "winner": winner.aps, "reason": reason})
            w = winner
        return w, trace

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
            # n lopa siddha for inter pada (happens naturally)
            # also for 7.4.33, 7.4.25 rAjIyati, rAjAyate
            elif ((a1 == 82007) or (a1 == 74033)) and (a2 == 74025):
                return True
            # maGavan upaDA dIrGa (see Siddhanta Kaumudi on 7.1.70)
            elif ((a1 == 82023) and (a2 == Decimal("64008.1"))):
                return True
            # SK439 (8.2.3 न मु ने) marks ada as pada before wA (inst sg), enabling
            # SK419 (8.2.80 adaso'ser) to convert ada→amu at the aNga+pratyaya boundary.
            # The downstream rules 1.4.7 (ghyasakhī) and 7.3.120 (āṅo nā) must see
            # SK419's output (amu) to complete the derivation amu+A → amunā.
            # These two siddha entries give effect to that intent:
            #   1.4.7 sees amu (sets Gi); 7.3.120 sees amu+Gi (replaces A→nā).
            elif (a1 == 82080) and (a2 == 14007):
                return True
            elif (a1 == 82080) and (a2 == 73120):
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

    def _eval_sutras_at_window(self, node, ix):
        """Non-mutating evaluation pass. Returns {"sutras": [...], "priority_trace": [...]}."""
        records = []
        triggered = []
        for s in self.sutra_list:
            disabled = s.aps in node.outputs[ix].disabled_sutras
            disabled_by = node.outputs[ix].disabled_by.get(s.aps) if disabled else None
            domain_pass = None  # AntarangaPrakriya does not use domain filtering
            if not disabled:
                cond_pass, cond_detail = s.evalConditionDetail(*self.view(s, node, ix))
            else:
                cond_pass, cond_detail = None, []
            dev = s.name.devanagari() if not isinstance(s.name, str) else s.name
            records.append({
                "aps": s.aps, "dev": dev, "disabled": disabled,
                "disabled_by": disabled_by, "domain_pass": domain_pass,
                "condition_pass": cond_pass, "condition_detail": cond_detail,
            })
            if cond_pass:
                triggered.append(s)
        v = self.view(triggered[0], node, ix) if triggered else None
        _, priority_trace = self.sutra_priority_detail(triggered, v) if len(triggered) > 1 else (None, [])
        return {"sutras": records, "priority_trace": priority_trace}

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
            ix = _ix
            logger.debug(f"No pratyaya or samAsa. Checking for rule triggers at window 0")
            if len(node.outputs) != 1:
                triggered = [s for s in l if ((s.aps not in node.outputs[ix].disabled_sutras)  and s.isTriggered(*self.view(s, node, ix)))]

                #    assert node.outputs[0].hasTag("pada"), f"Expected pada at {0} got {node.outputs[0]}"
                #    assert node.outputs[0].hasTag("pada") or node.outputs[0].hasTag("avasAna"), f"Expected pada at {1} got {node.outputs[0]}"
            else:
                triggered = False
            
        logger.debug(f"I [{node.id}]: {node.outputs}  tags: {[set(_r.tags) for _r in node.outputs]}")
        if triggered:
            ix = _ix
            logger.debug(f"Triggered at window {ix}: {[str(t) for t in triggered]}")
            s = self.sutra_priority(triggered, node.outputs[ix:ix+2])
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
                    logger.debug(f"Insertion hier prakriya for {r[i]} {[_r.tags for _r in r[i]]}")
                    pada_p = False
                    ru_p = False
                    # Temporarily remove pada tag (not relevant here)
                    if r[i][0].isPada():
                        pada_p = True
                        r[i][0].deleteTag("pada")
                        logger.debug(f"Temporary pada deletion {r[i]} {[_r.tags for _r in r[i]]}")
                    # Temporarily remove ru tag: ru marks a pada-boundary s→r substitution
                    # and must not trigger 6.1.113/114 inside an insert hier prakriya
                    if r[i][0].hasTag("ru"):
                        ru_p = True
                        r[i][0].deleteTag("ru")
                        logger.debug(f"Temporary ru deletion {r[i]} {[_r.tags for _r in r[i]]}")
                    # Pass the triggering sutra's overrides as initially_disabled so
                    # they take effect inside the insert hier prakriya.  We cannot
                    # pre-modify r[i][0].disabled_sutras because PrakriyaVakya deepcopies
                    # its inputs, so any such modification would be lost.
                    hp = AntarangaPrakriya(self.sutra_list,
                                           PrakriyaVakya(r[i]),
                                           initially_disabled=s.overrides,
                                           capture_eval=self._capture_eval)
                    # This will execute hierarchically as needed
                    hp.execute()
                    hpo = _deduplicate_hier_outputs(hp.output())
                    hp.triggering_sutra_aps = s.aps
                    self.hier_prakriyas.append(hp)
                    logger.debug(f"Hier output for r[{i}] {hpo}")
                    assert len(hpo)==1, f"Unexpected multiple output {hpo} for insertion hier prakriya"
                    # Don't use join_object, since this is not a promotion but a replacement
                    if (i==0) and r[0][0].hasTag("samprasAraRam"):
                        r[0] = hpo[0][0]  # Appropriate sub-object for replacement
                    else:
                        r[i] = r[i][i]  # Appropriate sub-object for replacement
                    r[i].update("".
                                join([o.canonical() for o in hpo[0]]))
                    # Restore pada
                    if pada_p:
                        r[i].setTag("pada")
                        logger.debug(f"Restored pada {r[i]} {r[i].tags}")
                    # Restore ru
                    if ru_p:
                        r[i].setTag("ru")
                        logger.debug(f"Restored ru {r[i]} {r[i].tags}")

            logger.debug(f"Op result [{s.aps}]: {r}  tags: {[sorted(_r.tags) for _r in r]}")
            
            
            # Sutras that run disable not only themselves but the utsargas they override  from running again by the
            # pariBAzA "lakzye lakzaRaM sakfdeva pravartate" read with the traditional concept of ekavAkyatvam

            # Using sutra id in the disabled list to get round paninian object deepcopy
            r0.disabled_sutras.append(s.aps)
            r0.disabled_by[s.aps] = s.aps  # fired — disabled itself
            if s.optional:
                # Prevent optional sutra from executing on the same node again
                v0.disabled_sutras.append(s.aps)
                v0.disabled_by[s.aps] = s.aps
            # Overridden sutras disabled
            if s.overrides is not None:
                for so in l:
                    if so.aps in s.overrides:
                        r0.disabled_sutras.append(so.aps)
                        r0.disabled_by[so.aps] = s.aps  # disabled by overriding sutra
                        if s.optional:
                            # Prevent optional sutra's overridden sutras from executing on the same node again
                            v0.disabled_sutras.append(so.aps)
                            v0.disabled_by[so.aps] = s.aps
                        logger.debug(f"Disabling overriden {so}")
            # FIXME: disable sutras for AkaqArAdekA saMjYA

            logger.debug(f"O [{s.aps}]: {r}  tags: {[set(_r.tags) for _r in r]}  disabled: {[list(_r.disabled_sutras) for _r in r]}")

                    
            # Update Prakriya Tree
            # Craft inputs and outputs based on viewed inputs
            # And generated outputs
            pnv = node.outputs.copy_replace_at(ix, v[0]).copy_replace_at(ix+1, v[1])
            pnr = node.outputs.copy_replace_at(ix, r[0]).copy_replace_at(ix+1, r[1])
            if len(r) > 2:
                for i in range(len(r)-2):
                    pnr = pnr.copy_insert_at(ix+i+2, r[i+2])
            eval_log = self._eval_sutras_at_window(node, ix) if self._capture_eval else None
            _ps = PrakriyaNode(pnv, pnr, s, ix, [t for t in triggered if t != s], eval_log=eval_log)
            logger.debug(f'O Node: {_ps.id} [{s.aps}]')
            if node is not None:
                self.tree.add_child(node, _ps, opt=s.optional)
            else:
                self.tree.add_node(_ps, root=True)
            return r
        else:
            ix = _ix
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
            if pnv[ix].hasTag("Adya"):
                # When the Adya object is merged, simply replace by the successor object
                mobj = pnv[ix+1]
            else:
                # Merge element at index
                mobj = PaninianObject.join_objects([pnv[ix:ix+2]])
            # Replace element at ix with merged element and delete next
            pnr = node.outputs.copy_replace_at(ix, mobj).delete_at(ix+1)
            _ps = PrakriyaNode(pnv, pnr, dummySamhitaSutra, ix, [])
            logger.debug(f'O Node: {_ps.id} [merge@{ix}]')
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
        logger.debug(f"Final Result: {r}\n")
        return r

    def describe(self, indent="  ", tag_display=False):
        slp1 = "".join(str(x) for x in self.inputs.v)
        dev = sanscript.transliterate(slp1, sanscript.SLP1, sanscript.DEVANAGARI)
        bar = indent + "\u2500" * 62
        print(f"\n{bar}")
        print(f"{indent}Prakriya: {slp1}  ({dev})")
        # 1. Show init-time hierarchical prakriyas (inner compound derivations)
        for hp in self.hier_prakriyas:
            if not getattr(hp, 'triggering_sutra_aps', None):
                print(f"{indent}  \u250c Inner prakriya (hierarchical):")
                hp.describe(indent=indent + "  \u2502 ", tag_display=tag_display)
                print(f"{indent}  \u2514\u2500")
        # 2. Build hier_map for inline (execution-time) hierarchical prakriyas
        from collections import defaultdict
        hier_map = defaultdict(list)
        for hp in self.hier_prakriyas:
            aps = getattr(hp, 'triggering_sutra_aps', None)
            if aps:
                hier_map[aps].append(hp)
        self.tree.describe(indent=indent, hier_map=hier_map, tag_display=tag_display)
        outputs = ["".join(str(x) for x in y) for y in self.outputs]
        out_devs = [
            sanscript.transliterate(o, sanscript.SLP1, sanscript.DEVANAGARI)
            for o in outputs
        ]
        out_strs = "  |  ".join(f"{o}  ({d})" for o, d in zip(outputs, out_devs))
        print(f"{indent}Output: {out_strs}")
        print(f"{bar}\n")


    def name(self):
        return "Antaranga Prakriya"


# Dummy Sutra
dummySamhitaSutra = Sutra("samhitA", "0.0.0")
