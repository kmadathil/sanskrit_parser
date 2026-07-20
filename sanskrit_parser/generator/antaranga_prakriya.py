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
from sanskrit_parser.generator.paninian_object import PaninianObject, _SLP1_VOWELS
from sanskrit_parser.generator.prakriya import PrakriyaVakya, PrakriyaBase, PrakriyaNode, PrakriyaTree, _isScalar
from sanskrit_parser.generator.pratyaya import Pratyaya, sups, wac, kap, Sac, ap_s, ic_s, asic, qac
from sanskrit_parser.generator.sutra import Sutra

from copy import deepcopy, copy
import logging
logger = logging.getLogger(__name__)


def _cond_has_both_l_and_r(cond):
    """True if any single condition block references both `l` and `r` keys.
    Such rules are saṁhitā vowel-junction rules (6.1.78 eco'yavāyāvaḥ etc.) and
    must be suppressed at a resolved ekādeśa junction (6.1.85 antādivat), where
    `l` and `r` are the same single substitute phoneme."""
    if cond is None:
        return False
    blocks = cond if isinstance(cond, list) else [cond]
    for b in blocks:
        if isinstance(b, dict) and ("l" in b) and ("r" in b):
            return True
    return False


def _in_abhiya(aps_num):
    """6.4.22 असिद्धवदत्राभात् — outputs of rules in the ābhīya section
    (Pāṇini 6.4.22 .. end of 6.4) are asiddha (invisible) to each other.
    Our scope: aps_num in (64022, 64176). Specific carve-outs (e.g. the
    वुग्युटावुवङ्यणोः vārttika) are deferred."""
    try:
        return 64022 < float(aps_num) < 64176
    except (TypeError, ValueError):
        return False


# Static samanāśraya pairs for 6.4.22 ābhīya asiddhavat.
# Each entry: rule_aps -> set of peer rule_aps that this rule does NOT see.
# (Equivalent: an edge between two rules iff each is asiddha to the other.)
# Kept narrow on purpose: we only enable asiddhavat for pairs we've
# explicitly designed around, since broad-scope walking can over-fire
# in derivations like maGavan (optional vs samprasāraṇa) or BAt_strI
# (inner hier-prakriya branching). Add new pairs as the ābhīya cluster
# is extended.
_ASIDDHA_PEERS = {
    # 6.4.148 (यस्येति च) drops the final 'a' of gārgya before ī.
    # 6.4.150 (हलस्तद्धितस्य) drops the taddhita 'य' in upadhā after hal.
    # Both fire on gārgya|ī simultaneously and must compose:
    # 148 deletes the 'a', 150 deletes the 'y' → gArg → गार्गी.
    # 6.4.149 (सूर्य…य उपधायाः) drops the upadhā 'य' of matsya/sūrya etc.;
    # like 6.4.150 it must fire on the pre-yasyeti snapshot (matsya, not matsy)
    # so the two compose into mats → मत्सी.
    "6.4.148": frozenset({"6.4.150", "6.4.149", "6.4.134"}),
    # 6.4.134 (अल्लोपोऽनः) must NOT see 6.4.148's output — otherwise
    # गार्ग्यायन (post-148) leaks an spurious 'an'-class trigger that
    # mis-fires on the आयन्-substitute (gives गार्ग्याय्णी instead of
    # गार्ग्यायणी).
    "6.4.134": frozenset({"6.4.148"}),
    "6.4.150": frozenset({"6.4.148"}),
    "6.4.149": frozenset({"6.4.148"}),
    # 6.4.144 (नस्तद्धिते) drops the ṭi (final अन्) of a नकारान्त stem before a
    # taddhita (rājan + TaC → rāj → उपराजम्). It must NOT see 6.4.148's a-lopa:
    # for an a-stem uttara like vana, 6.4.148 (यस्येति च) elides the final 'a'
    # → the TRANSIENT 'van', which is not a genuine नकारान्त stem. Reading the
    # pre-148 snapshot ('vana', a-final), 6.4.144 correctly does not fire, and
    # vana + wac → vana → उपवनम्. For a real an-stem (rājan, carman) 6.4.148
    # never fires (न्-final, not a/ī-final), so 6.4.144 applies unchanged.
    #
    # ASYMMETRIC on purpose (single edge, not a mutual pair): the reverse
    # (6.4.148 blind to 6.4.144's output) must NOT be added. yuvatī derives
    # yuvan + ti → 6.4.144 → yuva → yuvatī, where 6.4.148 correctly does *not*
    # elide the 'a' of the yuva that 6.4.144 produced; making 6.4.148 read the
    # pre-144 'yuvan' snapshot breaks that (→ yuvtiḥ). Only the 144→148 edge is
    # grammatically needed here.
    "6.4.144": frozenset({"6.4.148"}),
}


def _is_asiddha_peer(self_aps, peer_aps):
    return peer_aps in _ASIDDHA_PEERS.get(self_aps, frozenset())


def _compose_abhiya(snapshot_str, current_str, target_str):
    """Compose two ābhīya rule edits against a shared snapshot.

    current_str = snapshot_str - prior peer edits.
    target_str  = snapshot_str - this rule's edits (operate on snapshot).
    Returns snapshot_str - (prior ∪ this) edits, position-merged.

    Uses difflib's SequenceMatcher to derive a per-snapshot-position edit
    dictionary for each diff, then merges. Same-position incompatible
    edits raise AssertionError (Pāṇinian samanāśraya pairs in our YAML
    don't overlap on character positions; if a real conflict surfaces,
    surface it rather than silently picking)."""
    if current_str == snapshot_str and target_str == snapshot_str:
        return snapshot_str
    if current_str == snapshot_str:
        return target_str
    if target_str == snapshot_str:
        return current_str

    from difflib import SequenceMatcher

    def _edit_dict(src, dst):
        ed = {}
        sm = SequenceMatcher(a=src, b=dst, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == 'equal':
                for d in range(i2 - i1):
                    ed[i1 + d] = ('keep',)
            elif tag == 'delete':
                for d in range(i2 - i1):
                    ed[i1 + d] = ('delete',)
            elif tag == 'replace':
                # Attribute the new content to the first src position;
                # other src positions in this block are deletions.
                ed[i1] = ('replace', dst[j1:j2])
                for d in range(1, i2 - i1):
                    ed[i1 + d] = ('delete',)
            elif tag == 'insert':
                ed[('before', i1)] = ('insert', dst[j1:j2])
        return ed

    e_curr = _edit_dict(snapshot_str, current_str)
    e_new  = _edit_dict(snapshot_str, target_str)
    keys = set(e_curr.keys()) | set(e_new.keys())
    combined = {}
    for k in keys:
        ec = e_curr.get(k)
        en = e_new.get(k)
        if ec is None:
            combined[k] = en
        elif en is None:
            combined[k] = ec
        elif ec == en:
            combined[k] = ec
        elif ec[0] == 'keep':
            combined[k] = en
        elif en[0] == 'keep':
            combined[k] = ec
        else:
            raise AssertionError(
                f"Ābhīya composition conflict at position {k}: "
                f"current={ec!r} vs new={en!r} "
                f"(snapshot={snapshot_str!r}, current={current_str!r}, target={target_str!r})"
            )

    out = []
    for i, c in enumerate(snapshot_str):
        # 'before' insert first
        ins_key = ('before', i)
        if ins_key in combined:
            out.append(combined[ins_key][1])
        e = combined.get(i, ('keep',))
        if e[0] == 'keep':
            out.append(c)
        elif e[0] == 'delete':
            pass
        elif e[0] == 'replace':
            out.append(e[1])
    # Trailing insert (after last char)
    end_key = ('before', len(snapshot_str))
    if end_key in combined:
        out.append(combined[end_key][1])
    return ''.join(out)


# The bahiranga split and the antādivat aps sets depend only on the (shared,
# effectively immutable) sutra_list, so compute them once per list instead of
# in every AntarangaPrakriya (incl. every inner hierarchical prakriya). The
# cache keeps a strong reference to the list so an id() can't be reused.
_sutra_split_cache = {}


def _split_sutras(sutra_list):
    cached = _sutra_split_cache.get(id(sutra_list))
    if cached is not None and cached[0] is sutra_list:
        return cached[1]
    karaka_sutras = [s for s in sutra_list
                     if getattr(s, "bahiranga", 9) == -2]
    samasa_sutras = [s for s in sutra_list
                     if getattr(s, "bahiranga", 9) == -1]
    main_sutras = [s for s in sutra_list
                   if getattr(s, "bahiranga", 9) > -1]
    purvapara_aps = [s.aps for s in sutra_list
                     if getattr(s, "purvapara", False)]
    ekadesha_block_aps = list(purvapara_aps)
    _seen = set(ekadesha_block_aps)
    for s in sutra_list:
        if (s.aps not in _seen
                and _cond_has_both_l_and_r(getattr(s, "_cond_dict", None))):
            ekadesha_block_aps.append(s.aps)
            _seen.add(s.aps)
    split = (karaka_sutras, samasa_sutras, main_sutras,
             purvapara_aps, ekadesha_block_aps)
    _sutra_split_cache[id(sutra_list)] = (sutra_list, split)
    return split


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
    def __init__(self, sutra_list, inputs, initially_disabled=None, capture_eval=False,
                 karaka=True):
        super().__init__(sutra_list, inputs)
        # Set to True to capture per-step evaluation data (opt-in; slower)
        # Must be set before the inner prakriya loop so inner prakriyas inherit it.
        self._capture_eval = capture_eval
        # Pre-pass rule split (karaka_plan.md §2 + avyayībhāva samāsa plan):
        #   bahiranga == -2 → kāraka pre-pass (sentence-level kāraka-saṁjñā +
        #     vibhakti-vidhi tagging; runs first, fixes vibhakti).
        #   bahiranga == -1 → samāsa pre-pass (compound formation; runs AFTER
        #     the kāraka pass + sup-insertion, since सह सुपा 2.1.4 compounds
        #     padas-with-sup). Lower = more antaraṅga = earlier.
        #   bahiranga  > -1 → main window scan (phonological rules), unchanged
        #     (already excludes both -2 and -1).
        # 6.1.85 antādivat (_purvapara_aps): aps ids of every ekādeśa
        # (pūrvaparayoḥ) rule. When one fires, this whole set PLUS the saṁhitā
        # ac-sandhi junction rules 6.1.77 (iko yaṇaci) and 6.1.78
        # (eco'yavāyāvaḥ) is disabled at that boundary — the two vowels have
        # coalesced into one phoneme, so no further ac-sandhi applies at the
        # resolved junction (see _exec).
        # The set disabled at an antādivat boundary (_ekadesha_block_aps) =
        # the ekādeśa rules themselves PLUS every rule whose condition
        # references both `l` and `r` in one block (the saṁhitā vowel-junction
        # rules — 6.1.77/78 and the tripādī sandhi mass). At a resolved
        # ekādeśa junction l == r == the single substitute, so such a rule
        # would mis-fire (the antādivat simultaneity caveat: one phoneme
        # cannot fill both slots). This is pre-merge-scoped (join_objects
        # resets disabled_sutras) and safe for the consonant-`r` members,
        # which cannot match the vowel substitute anyway.
        (self._karaka_sutras, self._samasa_sutras, self._main_sutras,
         self._purvapara_aps, self._ekadesha_block_aps) = _split_sutras(sutra_list)
        # Apply initially-disabled sutras AFTER PrakriyaVakya's deepcopy so they
        # are visible inside this prakriya.  Used by insert hier prakriyas to honour
        # the triggering sutra's `overrides:` list (the outer disabled_sutras update
        # only runs after the hier prakriya completes, so we must seed it here).
        if initially_disabled is not None:
            for aps in initially_disabled:
                self.inputs[0].disabled_sutras.append(aps)
        # Kāraka pre-pass + sup insertion (karaka_plan.md §2): only for
        # top-level sentence prakriyas (karaka=True — inner/hypothetical
        # prakriyas pass False so mid-phonology fragments carrying propagated
        # semantic_* tags can never re-enter), and only when some element
        # carries semantic_*/prayoga tags (skip-guard inside). MUST precede
        # the hierarchical scan below so it sees the post-insertion inputs.
        self.karaka_log = []
        if karaka and self._karaka_sutras:
            self._karaka_prepass()
        # Samāsa pre-pass (avyayībhāva samāsa plan): runs AFTER the kāraka
        # pre-pass + sup-insertion (सह सुपा 2.1.4 — compounding needs the sups),
        # on each kāraka branch. No-op until -1 samāsa rules exist / a compound
        # candidate is present (skip-guard inside).
        if karaka and self._samasa_sutras:
            self._samasa_prepass()
        self.hier_prakriyas = []
        self.need_hier = False
        # Kāraka pre-pass branches (karaka_plan.md §2 point 3): a vibhāṣā
        # (optional) kāraka rule forks the pre-pass into alternative sentences
        # (e.g. 2.3.22 saṁjño'nyatarasyāṁ → tṛtīyā else 2.3.2 dvitīyā). Each
        # branch becomes its own root below, so each derives independently and
        # output() returns one sentence per branch. Single-branch (the common
        # case, all of K0–K2) is unchanged.
        branches = getattr(self, "_karaka_branches", None) or [self.inputs]
        # Each branch is independently scanned for hierarchical (compound)
        # explosion, then contributes one or more tree roots.
        root_inputs = []
        for binputs in branches:
            branch_hier_inputs = [binputs]
            branch_hier_outputs = [[] for _ in binputs]
            branch_need_hier = False
            # Scan inputs for hierarchical prakriya needs
            for ix in range(len(binputs)):
                if binputs.need_hierarchy_at(ix):
                    branch_need_hier = True
                    self.need_hier = True
                    # hierarchy needed here
                    hp = AntarangaPrakriya(sutra_list,
                                           PrakriyaVakya(binputs[ix]),
                                           capture_eval=self._capture_eval,
                                           karaka=False)
                    self.hier_prakriyas.append(hp)
                    # This will execute hierarchically as needed
                    hp.execute()
                    hpo = _deduplicate_hier_outputs(hp.output())
                    branch_hier_outputs[ix] = hpo  # accumulate hierarchical outputs
            if branch_need_hier:
                for ix, ol in enumerate(branch_hier_outputs):
                    if ol != []:  # Hierarchy exists here
                        tmpl = []
                        # For each alternate output
                        for o in ol:
                            hobj = PaninianObject.join_objects([o])
                            # Assemble exploded list with each input
                            # replaced by multiple alternates at this
                            # index
                            for i in branch_hier_inputs:
                                tmpl.append(i.copy_replace_at(ix, hobj))
                        # Replace input list with exploded list
                        # Explosion at position ix is now dealt with
                        branch_hier_inputs = tmpl
                        logger.debug(f"Hier inputs after expl {ix}: {branch_hier_inputs}")
            root_inputs.extend(branch_hier_inputs)
        # List of alternatives (kept for describe()/logging compatibility)
        self.hier_inputs = root_inputs
        logger.debug(f"Hier inputs after full expl: {self.hier_inputs}")
        if self.need_hier:
            for i in root_inputs:
                _n = PrakriyaNode(i, i, "Prakriya Hierarchical Start")
                self.tree.add_node(_n, root=True)
        else:
            for i in root_inputs:
                _n = PrakriyaNode(i, i, "Prakriya Start")
                self.tree.add_node(_n, root=True)

        self.outputs = []
        self.disabled_sutras = []
        # Sliding window counter
        self.windowIdx = 0

    # ── Kāraka layer (karaka_plan.md §2) ────────────────────────────────────
    _PRAYOGA_TAGS = ("kartari", "karmaRi", "BAve")

    def _karaka_prepass(self):
        """Sentence-level kāraka/vibhakti tagging pre-pass + sup insertion.

        For each participant element (scalar, ?prAtipadika + a vacana_N tag),
        run exactly the bahiranga == -2 rules on the synthetic window
        (element | sentence-dhātu) to fixpoint — 1.4.x rules write kAraka_*,
        2.3.x rules write viBakti_N (naturally sequenced: the latter condition
        on the former). disabled_sutras bookkeeping mirrors _exec. Then insert
        the sup pratyayas the viBakti_N/vacana_M tags select. Skipped entirely
        when no element carries semantic_*/prayoga tags, so non-kāraka
        prakriyas never pay for it. SK534 (kārake) = this pass's scope;
        SK536 (anabhihite) = the rp prayoga gate the 2.3.x rules read.
        """
        def _scalars(inputs):
            for ix in range(len(inputs)):
                o = inputs[ix]
                if _isScalar(o):
                    yield ix, o

        def _is_semantic(o):
            return any(t.startswith("semantic_") or t in self._PRAYOGA_TAGS
                       for t in o.tags)

        # Skip-guard: zero impact on prakriyas without kāraka-layer inputs.
        # ?samAsa_vivakza (samāsa intent) also trips it: a compound needs its
        # members' sups inserted (सह सुपा 2.1.4) before the samāsa pre-pass, even
        # when no kāraka sense is present (e.g. the structural nitya 2.1.10
        # akṣa+pari). Default prathamā (2.3.46) then supplies su to each member.
        if not any(_is_semantic(o) or o.hasTag("samAsa_vivakza")
                   for _, o in _scalars(self.inputs)):
            self._karaka_branches = [self.inputs]
            return

        def _dhatu_of(inputs):
            # Sentence dhātu = first element with a prayoga tag (the pre-formed
            # tiṅanta pada); empty sentinel if none (śeṣa-only sentences).
            for _, o in _scalars(inputs):
                if any(o.hasTag(t) for t in self._PRAYOGA_TAGS):
                    return o
            return PaninianObject("")

        def _neighbours(inputs, ix):
            # Physical neighbour words for llp/rrp (particle-yoga rules),
            # skipping the Adya/avasAna separator elements.
            llp = rrp = None
            for j in range(ix - 1, -1, -1):
                o = inputs[j]
                if _isScalar(o) and (o.hasTag("Adya") or o.hasTag("avasAna")):
                    continue
                llp = o if _isScalar(o) else o[0]
                break
            for j in range(ix + 1, len(inputs)):
                o = inputs[j]
                if _isScalar(o) and (o.hasTag("Adya") or o.hasTag("avasAna")):
                    continue
                rrp = o if _isScalar(o) else o[0]
                break
            return (llp, rrp)

        def _apply(inputs, ix, s, fired):
            # Apply rule s to element ix of inputs in place, mirroring _exec's
            # disabled_sutras bookkeeping. Returns the new element object.
            elem = inputs[ix]
            dhatu = _dhatu_of(inputs)
            r = s.operate(elem, dhatu)
            r = s.update(elem, dhatu, *r)
            r0 = r[0]
            r0.disabled_sutras.append(s.aps)
            r0.disabled_by[s.aps] = s.aps
            if s.overrides is not None:
                for so_aps in s.overrides:
                    r0.disabled_sutras.append(so_aps)
                    r0.disabled_by[so_aps] = s.aps
            fired.append(s.aps)
            logger.debug(f"Kāraka pre-pass [{s.aps}] @{ix}: {r0} tags {sorted(r0.tags)}")
            inputs.replace_at(ix, r0)
            return inputs[ix]

        def _run_fixpoint(inputs, ix, fired_prefix=None):
            # Run the bahiranga == -2 rules on element ix (window = elem | dhātu)
            # to fixpoint, mirroring _exec's bookkeeping. A vibhāṣā (optional)
            # winner FORKS: one branch (a deep clone with the rule disabled on the
            # element) re-runs the fixpoint — falling through to the general rule
            # (e.g. 2.3.22 not applied → 2.3.2 dvitīyā) — while this branch applies
            # the rule. Returns a list of (inputs, log_entry); the common
            # non-optional path returns exactly one.
            fired = list(fired_prefix or [])
            forked = []
            dhatu = _dhatu_of(inputs)
            elem = inputs[ix]
            while True:
                ctx = _neighbours(inputs, ix)
                triggered = [s for s in self._karaka_sutras
                             if (s.aps not in elem.disabled_sutras)
                             and s.isTriggered(elem, dhatu, context=ctx)]
                if not triggered:
                    break
                s = self.sutra_priority(triggered, [elem, dhatu])
                if s.optional:
                    # Vibhāṣā fork: the not-applied branch is a clone with s
                    # disabled, run to its own fixpoint (and possibly forking
                    # again). This branch falls through and applies s below.
                    skip_inputs = PrakriyaVakya(inputs.v)
                    se = skip_inputs[ix]
                    se.disabled_sutras.append(s.aps)
                    se.disabled_by[s.aps] = s.aps
                    forked.extend(_run_fixpoint(skip_inputs, ix, fired))
                elem = _apply(inputs, ix, s, fired)
            log_entry = {"index": ix, "fired": fired, "tags": sorted(elem.tags)}
            return [(inputs, log_entry)] + forked

        def _is_avyaya_particle(o):
            # A karmapravacanīya particle: an avyaya word (nipAta/svarAdi) carrying
            # a per-usage semantic sense tag (e.g. semantic_lakzaRa on anu).
            return (o.hasTag("prAtipadika")
                    and (o.hasTag("nipAta") or o.hasTag("svarAdi"))
                    and _is_semantic(o))

        def _is_noun(o):
            return (o.hasTag("prAtipadika")
                    and any(t.startswith("vacana_") for t in o.tags)
                    and not (o.hasTag("nipAta") or o.hasTag("svarAdi")))

        # Processing order (stable across branches — the partition keys
        # ?prAtipadika/vacana_/nipAta are never written by kāraka rules, and the
        # fixpoint replaces in place without changing indices until sup
        # insertion). Pass A (karaka_plan.md §K2): particle karmapravacanīya
        # saṁjñā FIRST, so 2.3.8 can read it via llp/rrp regardless of word
        # order. Pass B: noun kāraka/vibhakti.
        passA = [ix for ix, o in _scalars(self.inputs) if _is_avyaya_particle(o)]
        passB = [ix for ix, o in _scalars(self.inputs) if _is_noun(o)]
        # Branch states carried across elements; a vibhāṣā rule multiplies them.
        branch_states = [self.inputs]
        branch_logs = [[]]
        for ix in passA + passB:
            new_states, new_logs = [], []
            for st, lg in zip(branch_states, branch_logs):
                for rst, rlog in _run_fixpoint(st, ix):
                    new_states.append(rst)
                    new_logs.append(lg + [rlog])
            branch_states, branch_logs = new_states, new_logs
        for st in branch_states:
            self._insert_sups(st)
        for lg in branch_logs:
            self.karaka_log.extend(lg)
        self._karaka_branches = branch_states

    def _insert_sups(self, inputs):
        """Insert sup pratyayas after elements tagged viBakti_N + vacana_M
        (karaka_plan.md §2 step 1), scrolling right past kṛt/taddhita/strī
        pratyaya elements of the same word. Idempotent: skips when a sup is
        already in place. The tiṅ branch is stubbed until tiṅanta derivation
        exists — pre-formed verb padas (?tiNanta) are left untouched.

        Operates on the given branch's `inputs` (a vibhāṣā kāraka rule may have
        forked the pre-pass into several alternative sentences)."""
        insertions = []
        for ix in range(len(inputs)):
            o = inputs[ix]
            if not _isScalar(o):
                continue
            if o.hasTag("tiNanta"):
                logger.debug(f"Sup insertion: tiṅ stub, skipping {o}")
                continue
            vib = next((t for t in o.tags
                        if t.startswith("viBakti_") and t[8:].isdigit()), None)
            vac = next((t for t in o.tags
                        if t.startswith("vacana_") and t[7:].isdigit()), None)
            if vib is None:
                continue
            n = int(vib[8:])
            if vac is not None:
                m = int(vac[7:])
            elif o.hasTag("nipAta") or o.hasTag("svarAdi"):
                # An avyaya is avibhaktika: it still takes a sup (eka-vacana su),
                # which 2.4.82 (avyayādāpsupaḥ) luks later in the main scan. So a
                # karmapravacanīya particle that took viBakti_1 (2.3.46) gets su →
                # luk → the bare avyaya surface, faithfully (karaka_plan.md §K2).
                m = 1
            else:
                continue
            jx = ix + 1
            while jx < len(inputs):
                nxt = inputs[jx]
                # Only scroll past a kṛt/taddhita/strī *pratyaya* of the same
                # word — never a following pratipadika that merely carries a
                # strI (or other) tag, e.g. a feminine stem ramA, which is the
                # next word and must get its own sup at its own position.
                if (_isScalar(nxt) and nxt.hasTag("pratyaya")
                        and (nxt.hasTag("krt") or nxt.hasTag("tadDita")
                             or nxt.hasTag("strI"))):
                    jx += 1
                else:
                    break
            if (jx < len(inputs) and _isScalar(inputs[jx])
                    and inputs[jx].hasTag("sup")):
                continue  # sup already present (re-entry safety)
            logger.debug(f"Sup insertion: {o} {vib}/{vac} -> sups[{n-1}][{m-1}] at {jx}")
            insertions.append((jx, sups[n-1][m-1]))
        # Apply right-to-left so collected indices stay valid.
        for jx, supobj in reversed(insertions):
            inputs.insert_at(jx, supobj)

    # ── Samāsa layer (avyayībhāva samāsa plan) ───────────────────────────────
    def _samasa_prepass(self):
        """Samāsa formation pre-pass — runs AFTER the kāraka pre-pass +
        _insert_sups, on padas-with-sup (सह सुपा 2.1.4).

        Runs exactly the bahiranga == -1 rules on each adjacent compound-member
        window (pūrva | uttara) to fixpoint. The rules assign the samāsa saṁjñā
        (?avyayIBAva …), the member roles (?samAsaPurva on the pūrva, ?samAsa on
        the uttara) and ?upasarjana (1.2.43). It does NOT delete internal
        vibhakti (sup-luk is a main-scan job, 2.4.71) and does NOT physically
        reorder (2.2.30 deferred — in avyayībhāva the avyaya is already pūrva).

        A compound candidate is a maximal run of adjacent member prātipadikas
        (their inserted sups skipped) NOT separated by an avasAna, flagged for
        samāsa — either ?samAsa_vivakza (user intent; the vibhāṣā block ≥ SK665)
        or a samāsa sense a nitya rule keys on (≤ SK664). Skip-guard: no-op
        unless some -1 rule exists AND a candidate run is present. Operates on
        each kāraka branch in place; mirrors _karaka_prepass's bookkeeping."""
        if not self._samasa_sutras:
            return
        # A vibhāṣā samāsa rule (5.4.109) forks a kāraka branch into several, so
        # collect the expanded set and REPLACE _karaka_branches — the __init__
        # root-building loop (which runs after this) then makes one derivation
        # per branch (उपचर्म / उपचर्मम् surface as two outputs). Non-forking
        # branches return a 1-element list, identical to before.
        new_branches = []
        for inputs in (getattr(self, "_karaka_branches", None) or [self.inputs]):
            new_branches.extend(self._samasa_prepass_branch(inputs))
        self._karaka_branches = new_branches

    @staticmethod
    def _is_samasa_member(o):
        # A compound member: a prātipadika that is not its own inserted sup /
        # pratyaya, not a separator (Adya/avasAna), not the verb pada.
        return (_isScalar(o) and o.hasTag("prAtipadika")
                and not o.hasTag("sup") and not o.hasTag("pratyaya")
                and not o.hasTag("avasAna") and not o.hasTag("Adya")
                and not o.hasTag("tiNanta"))

    def _samasa_prepass_branch(self, inputs):
        def _flagged(o):
            return (o.hasTag("samAsa_vivakza")
                    or any(t.startswith("semantic_") for t in o.tags))

        def _avasana_between(i, j):
            return any(_isScalar(inputs[k]) and inputs[k].hasTag("avasAna")
                       for k in range(i + 1, j))

        members = [ix for ix in range(len(inputs))
                   if self._is_samasa_member(inputs[ix])]
        # Apply -1 rules to each adjacent (pūrva | uttara) member pair that is a
        # compound candidate (no avasAna between; flagged for samāsa). A vibhāṣā
        # rule forks, so thread a list of branches through the member-pair loop.
        branches = [inputs]
        for a, b in zip(members, members[1:]):
            if _avasana_between(a, b):
                continue
            if not (_flagged(inputs[a]) or _flagged(inputs[b])):
                continue
            nxt = []
            for br in branches:
                nxt.extend(self._samasa_window_fixpoint(br, a, b))
            branches = nxt
        # Per-branch post-fixpoint steps: commit the deferred napuṁsaka
        # (samasa_napum → napum) BEFORE the main scan, swap any consumed internal
        # vibhakti, insert the samāsānta affix, then group the members into a
        # hierarchical sub-prakriya so the compound resolves as one samasta_pada.
        for br in branches:
            self._commit_samasa_napum(br)
            self._swap_sups(br)
            self._insert_samasanta(br)
            self._nest_samasa_members(br)
        return branches

    def _nest_samasa_members(self, inputs):
        """Wrap each contiguous compound-member span (the members + their inserted
        sups) into a NESTED sub-list so the __init__ hierarchical scan
        (need_hierarchy_at) processes it as one sub-prakriya.

        The samāsa pre-pass otherwise only TAGS members in place, leaving them
        flat at the top level. A flat compound never coalesces into a single
        `samasta_pada` before the trailing avasāna (or a neighbour word) merges
        into the uttara — so the samānapada ṇatva rules (8.4.1/8.4.2, gated on
        ?!merged_pada) never fire (राजपुरुषेन instead of राजपुरुषेण). Nesting makes
        the compound resolve fully — pūrva sup-luk (2.4.71), 8.2.7 न-lopa, the
        uttara declension, ṇatva, and the samasta_pada merge — as one unit,
        exactly as the CLI in_compound / -m path already does, before it meets
        the sentence context. (No physical reorder — 2.2.30 stays deferred.)

        A span starts at a member (?samAsaPurva / ?samAsa) and greedily extends
        over following sups and further members; it is wrapped only if it holds
        >1 element (a lone member with no sup is left as-is). Non-member padas,
        Adya and avasAna stay at the top level and bound the spans."""
        def _is_member(o):
            return (_isScalar(o) and self._is_samasa_member(o)
                    and (o.hasTag("samAsaPurva") or o.hasTag("samAsa")))

        i = 0
        while i < len(inputs):
            if _is_member(inputs[i]):
                j = i + 1
                # Extend over the members' pratyayas — their inserted sups AND a
                # samāsānta affix (the wac tadDita inserted by _insert_samasanta,
                # e.g. उपराज+अ → उपराजम्) — so the whole compound is one sub-list.
                while j < len(inputs) and _isScalar(inputs[j]) and (
                        inputs[j].hasTag("pratyaya") or _is_member(inputs[j])):
                    j += 1
                if j - i > 1:
                    span = [inputs[k] for k in range(i, j)]
                    inputs.v[i:j] = [span]
                    i += 1
                    continue
                i = j
            else:
                i += 1

    def _commit_samasa_napum(self, inputs):
        """Commit the samāsa-assigned napuṁsaka to the real ?napum at end-of-sweep.
        2.4.18 sets a DEFERRED marker ?samasa_napum (not ?napum) so 5.4.108/5.4.109
        can read the uttara's NATIVE gender during the sweep; here — after the
        sweep, before the main scan — it becomes the real ?napum (removing the
        member's native pum/strI) so 1.2.47 / 7.1.24 / the am path see the compound
        as napuṁsaka. Generic (bahuvrīhi, which also assigns gender, will reuse it)."""
        for o in inputs:
            if _isScalar(o) and o.hasTag("samasa_napum"):
                o.deleteTag("samasa_napum")
                o.setTag("napum")
                # Lock the samāsa-assigned gender so a later samāsānta affix
                # (wac, which hard-codes ?pum for the 2.4.29 rātrāhnāhāḥ puṃsi
                # ahar-case) cannot override it at the (uttara | wac) merge —
                # a samāhāra dvigu (2.4.1) or avyayībhāva (2.4.18) stays napuṁsaka
                # (पञ्चगवम्, not पञ्चगवः). join_objects honours ?samasa_liNga_locked.
                o.setTag("samasa_liNga_locked")
                for g in ("pum", "strI"):
                    if o.hasTag(g):
                        o.deleteTag(g)

    def _swap_sups(self, inputs):
        """For each member a samāsa rule tagged ?swap_viBakti — i.e. it swapped
        the member's internal (kāraka-assigned, vigraha) vibhakti to the
        compound's external one (e.g. 2.1.12/2.1.13 consume the kāraka pañcamī,
        resetting to prathamā) — REPLACE its already-inserted sup with the sup
        for the new viBakti_N/vacana_M (exactly the _insert_sups lookup) and
        clear the tag. The internal sup (e.g. ṅasi) is thus physically replaced
        by the external one (su), so the compound declines as am (2.4.83), not
        the ablative. Generic: reads the target vibhakti/vacana off the member
        (reusable for bahuvrīhi)."""
        for ix in range(len(inputs)):
            o = inputs[ix]
            if not (_isScalar(o) and o.hasTag("swap_viBakti")):
                continue
            o.deleteTag("swap_viBakti")
            vib = next((t for t in o.tags
                        if t.startswith("viBakti_") and t[8:].isdigit()), None)
            vac = next((t for t in o.tags
                        if t.startswith("vacana_") and t[7:].isdigit()), None)
            if vib is None or vac is None:
                continue
            n, m = int(vib[8:]), int(vac[7:])
            # Scroll past this word's kṛt/taddhita/strī pratyayas to its sup
            # (mirrors _insert_sups), then replace it with the new vibhakti's sup.
            jx = ix + 1
            while jx < len(inputs):
                nxt = inputs[jx]
                if (_isScalar(nxt) and nxt.hasTag("pratyaya")
                        and (nxt.hasTag("krt") or nxt.hasTag("tadDita")
                             or nxt.hasTag("strI"))):
                    jx += 1
                else:
                    break
            if (jx < len(inputs) and _isScalar(inputs[jx])
                    and inputs[jx].hasTag("sup")):
                logger.debug(f"Samāsa sup-swap @{jx}: -> sups[{n-1}][{m-1}]")
                inputs.replace_at(jx, sups[n-1][m-1])

    # Samāsānta affix markers → the affix (?tadDita) that _insert_samasanta inserts
    # after the qualifying uttara. ?samasanta_TaC → wac (aC/ṬaC, avyayībhāva + tatpuruṣa
    # samāsāntas 5.4.86–112); ?samasanta_kap → kap (the bahuvrīhi कप्, 5.4.151/154 etc.).
    # Adding a new affix family (ap/ac/ṣac/ḍac/ic…) is one entry here + a Pratyaya.
    _SAMASANTA_AFFIXES = {"samasanta_TaC": wac, "samasanta_kap": kap,
                          "samasanta_Sac": Sac, "samasanta_ap": ap_s,
                          "samasanta_ic": ic_s,
                          "samasanta_asic": asic,
                          "samasanta_qac": qac}

    def _insert_samasanta(self, inputs):
        """Insert the samāsānta affix after any uttara tagged with a ?samasanta_*
        marker (5.4.68 समासान्ताः adhikāra). The DECISION is rule-driven: the samāsānta
        rules set the marker on the qualifying uttara (śarat-prabhṛti, an-final, nadī,
        a bahuvrīhi taking कप्, …); this step just performs the structural insertion
        (like _insert_sups). The affix (?tadDita) is placed just after the uttara
        (before its sup); the main scan merges stem+affix, and join_objects carries the
        compound-type tags through that tadDita merge (उप+शरद्+अ → उपशरदम्; बहु+यशस्+क →
        बहुयशस्कः)."""
        for ix in range(len(inputs)):
            o = inputs[ix]
            if not self._is_samasa_member(o):
                continue
            marker = next((m for m in self._SAMASANTA_AFFIXES if o.hasTag(m)), None)
            if marker is None:
                continue
            o.deleteTag(marker)
            # Insert the affix just after this uttara (before its sup, if present).
            inputs.insert_at(ix + 1, deepcopy(self._SAMASANTA_AFFIXES[marker]))
            # Re-scan from scratch: indices shifted; another member may qualify.
            return self._insert_samasanta(inputs)

    def _samasa_window_fixpoint(self, inputs, a, b, fired_prefix=None):
        """Run the bahiranga == -1 rules on the (pūrva | uttara) member window
        (indices a, b) to fixpoint, writing tags back to both members. llp/rrp
        context = the physical neighbours just outside the window.

        A vibhāṣā (optional) winner FORKS (mirrors the kāraka `_run_fixpoint`):
        the not-applied branch is a deep clone with the rule disabled at the
        window, run to its own fixpoint; this branch applies the rule. Returns
        the list of branch inputs — one element for the common non-optional case,
        two (or more) when an optional rule such as 5.4.109 forks (उपचर्म/उपचर्मम्).
        The a,b indices are stable across the clone (rules only write tags)."""
        fired = list(fired_prefix or [])
        forked = []
        lp, rp = inputs[a], inputs[b]
        while True:
            ctx = (inputs[a - 1] if a - 1 >= 0 else None,
                   inputs[b + 1] if b + 1 < len(inputs) else None)
            triggered = [s for s in self._samasa_sutras
                         if (s.aps not in lp.disabled_sutras)
                         and s.isTriggered(lp, rp, context=ctx)]
            if not triggered:
                break
            s = self.sutra_priority(triggered, [lp, rp])
            if s.optional:
                # Vibhāṣā fork: clone with s disabled at the window, run its own
                # fixpoint; this branch falls through and applies s below.
                skip = PrakriyaVakya(inputs.v)
                se = skip[a]
                se.disabled_sutras.append(s.aps)
                se.disabled_by[s.aps] = s.aps
                forked.extend(self._samasa_window_fixpoint(skip, a, b, fired))
            r = s.operate(lp, rp)
            r = s.update(lp, rp, *r)
            nlp, nrp = r[0], r[1]
            nlp.disabled_sutras.append(s.aps)
            nlp.disabled_by[s.aps] = s.aps
            if s.overrides is not None:
                for so_aps in s.overrides:
                    nlp.disabled_sutras.append(so_aps)
                    nlp.disabled_by[so_aps] = s.aps
            fired.append(s.aps)
            logger.debug(f"Samāsa pre-pass [{s.aps}] @({a},{b}): "
                         f"{nlp}|{nrp} tags {sorted(nlp.tags)}/{sorted(nrp.tags)}")
            inputs.replace_at(a, nlp)
            inputs.replace_at(b, nrp)
            lp, rp = inputs[a], inputs[b]
        if fired:
            # Log BOTH members: the uttara (b) carries the saṁjñā + the fired
            # trace; the pūrva (a) carries samAsaPurva/upasarjana — so the CLI
            # and UI can show the full compound structure.
            self.karaka_log.append({"index": b, "fired": fired,
                                    "tags": sorted(rp.tags), "samasa": True})
            self.karaka_log.append({"index": a, "fired": [],
                                    "tags": sorted(lp.tags), "samasa": True})
        return [inputs] + forked

    def _apply_antadivat(self, s, r):
        """6.1.85 antādivat boundary marking. Called from _exec AND from the
        _nitya priority simulation, so that the hypothetical output a nitya
        check inspects carries the same ?antAdivat view as a real firing (the
        engine's _exec block runs after operate/update/insert, which the nitya
        simulation otherwise would not see — leaving l mis-read as the physical
        residue consonant and flipping the sutra-priority winner).

        Every ekādeśa (purvapara) rule lumps the substitute on the RIGHT (rp[0]),
        truncating the left to a consonant; this guard (left ends in a non-vowel,
        right non-empty) detects that. Sets ?antAdivat and disables the ekādeśa +
        both-l-and-r set (see _cond_has_both_l_and_r). Tag-keyed bha/aṅga rules
        that read the migrated anta are blocked rule-locally instead (e.g. 6.4.130
        carries `l: d`, so the antavat synth l = the substitute vowel fails it on
        a guṇa residue). The vowel-ending guard is defensive — if a rule ever left
        the substitute on a vowel-final left, antavat would already be automatic
        and no marker is needed."""
        if not getattr(s, "purvapara", False):
            return
        lcanon = r[0].canonical()
        if (r[1].canonical() != "" and lcanon != ""
                and lcanon[-1] not in _SLP1_VOWELS):
            r[0].setTag("antAdivat")
            for paps in self._ekadesha_block_aps:
                if paps not in r[0].disabled_sutras:
                    r[0].disabled_sutras.append(paps)
                    r[0].disabled_by[paps] = s.aps

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
                                               initially_disabled=s.overrides,
                                               karaka=False)
                        # This will execute hierarchically as needed
                        hp.execute()
                        hpo = _deduplicate_hier_outputs(hp.output())
                        logger.debug(f"Nitya check: Hypothetical Hier output for r[{i}] {hpo}")
                        assert len(hpo)==1, f"Unexpected multiple output {hpo} for insertion hier prakriya"
                        # Don't use join_object, since this is not a promotion but a replacement
                        r[i] = r[i][i]  # Appropriate sub-object for insertion
                        r[i].update("".join([o.canonical() for o in hpo[0]]))
                        logger.debug(f"Nitya Check: Hypothetical  Result {r}")
                # Replay the 6.1.85 antādivat tagging the real _exec applies, so
                # the nitya test below sees the antavat l (not the physical
                # residue consonant) — otherwise the priority winner flips.
                self._apply_antadivat(s, r)
                _o[s] = r    # Cache output
            # We have the output of s in cache _o[s]
            # Check if s1 is still triggered AFTER s applied. Consult the
            # *hypothetical output's* disabled_sutras (_o[s][0]), not the pre-s
            # state v[0]: if s disabled s1 (e.g. an ekādeśa's antādivat block
            # disables the both-l-and-r set), then s1 is not nitya wrt s. Reading
            # v[0] missed this, letting a both-l-r rule look "still triggered" via
            # the synthesised l==r==substitute phantom junction (e.g. 6.1.77 vs
            # 6.1.101 at sakhi|ṅi, which flipped औत् 7.3.118 out of the fold).
            nit = (s1.aps not in _o[s][0].disabled_sutras) and \
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
            # 1.4.2 vipratiṣedhe paraṁ kāryam — within the kāraka adhikāra
            # (1.4.23 kārake .. 1.4.98) the LATER rule wins on an ekā-saṁjñā
            # conflict (e.g. 1.4.38 karma beats 1.4.37 sampradāna on an
            # upasṛṣṭa krudh-target). Must precede the saṁjñā branch below
            # and skip the nitya simulation (tag rules block each other via
            # the ?!kAraka guard, so nitya would never decide these anyway).
            elif (14023 <= s1._aps_num < 14099) and (14023 <= s2._aps_num < 14099):
                logger.debug(f"Kāraka adhikāra param, higher of {s1} {s2}")
                if s1._aps_num > s2._aps_num:
                    return s1
                else:
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
                                               initially_disabled=s.overrides,
                                               karaka=False)
                        hp.execute()
                        hpo = _deduplicate_hier_outputs(hp.output())
                        r[i] = r[i][i]
                        r[i].update("".join([o.canonical() for o in hpo[0]]))
                self._apply_antadivat(s, r)
                _o[s] = r
            return (s1.aps not in _o[s][0].disabled_sutras) and s1.isTriggered(*_o[s])

        def _winner_reason(s1, s2):
            if (s2.overrides is not None) and (s1.aps in s2.overrides):
                return s2, f"apavāda: {s2.aps} overrides {s1.aps}"
            elif (s1.overrides is not None) and (s2.aps in s1.overrides):
                return s1, f"apavāda: {s1.aps} overrides {s2.aps}"
            elif s1.bahiranga < s2.bahiranga:
                return s1, f"antaraṅga: {s1.aps} (score {s1.bahiranga}) beats {s2.aps}"
            elif s2.bahiranga < s1.bahiranga:
                return s2, f"antaraṅga: {s2.aps} (score {s2.bahiranga}) beats {s1.aps}"
            elif (14023 <= s1._aps_num < 14099) and (14023 <= s2._aps_num < 14099):
                w = s1 if s1._aps_num > s2._aps_num else s2
                return w, f"kāraka adhikāra (1.4.2 vipratiṣedhe param): higher APS wins ({w.aps})"
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
        """Operand pair (lp, rp) = the 2-object window seen by sutra s."""
        if node is None:
            return self.inputs
        _l, ix = self._visible_list(s, node, ix)
        return _l[ix:ix+2]

    def view_context(self, s, node, ix=0):
        """Neighbour padas (llp, rrp) around the window, read from the same
        visible list view() uses — so they respect s's asiddha/ābhīya snapshot.
        llp = pada before lp (ix-1); rrp = pada after rp (ix+2); None if absent.
        """
        if node is None:
            return (None, None)
        _l, ix = self._visible_list(s, node, ix)
        llp = _l[ix-1] if ix > 0 else None
        rrp = _l[ix+2] if ix + 2 < len(_l) else None
        return (llp, rrp)

    def _visible_list(self, s, node, ix=0):
        """Snapshot-correct visible output list (and clamped ix) for sutra s at
        window ix. Both view() and view_context() read from this so they agree
        on the asiddha/ābhīya snapshot. Assumes node is not None.

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


        #FIXME Need to implement zutvatokorasiddhaH
        #FIXME Implement vukyuw... vArttikam on asidDavadatrABAt       
        if _in_abhiya(aps_num) and s is not None and getattr(s, 'aps', None) in _ASIDDHA_PEERS:
            # 6.4.22 ābhīya asiddhavat — static-samanāśraya pairs only.
            # Walk past parent firings of explicit asiddha-peer rules at
            # the same window AND tripādī parents (8.2+), to match the
            # default sapādasaptādhyāyī skip below (aps_num < 82000 path).
            # The engine composes the diff (snapshot → operate(snapshot))
            # with the current state's accumulated peer diffs before
            # writing the new node, so both peer effects and this rule's
            # effect end up in the composed output. Only the rule-pairs
            # in _ASIDDHA_PEERS get this treatment; everything else uses
            # the normal view.
            self_aps = s.aps
            _n = node
            while self.tree.parent[_n] is not None and not isinstance(_n.sutra, str):
                parent_aps_num = getattr(_n.sutra, '_aps_num', None)
                parent_aps     = getattr(_n.sutra, 'aps',      None)
                # Skip tripādī parents (matches default <82000 view).
                if (parent_aps_num is not None and parent_aps_num > 82000
                        and not _special_siddha(parent_aps_num, aps_num)):
                    _n = self.tree.parent[_n]
                    continue
                # Skip ābhīya-peer parents at the same window.
                if (_n.index == ix
                        and _is_asiddha_peer(self_aps, parent_aps)):
                    _n = self.tree.parent[_n]
                    continue
                break
            _l = _n.outputs
        elif aps_num < 82000:
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
        return _l, ix

    def _eval_sutras_at_window(self, node, ix):
        """Non-mutating evaluation pass. Returns {"sutras": [...], "priority_trace": [...]}."""
        records = []
        triggered = []
        for s in self.sutra_list:
            disabled = s.aps in node.outputs[ix].disabled_sutras
            disabled_by = node.outputs[ix].disabled_by.get(s.aps) if disabled else None
            domain_pass = None  # AntarangaPrakriya does not use domain filtering
            if not disabled:
                cond_pass, cond_detail = s.evalConditionDetail(*self.view(s, node, ix), context=self.view_context(s, node, ix))
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
        # Window scan runs only the phonological (bahiranga > -1) rules; the
        # bahiranga == -2 kāraka and == -1 samāsa classes belong to the
        # pre-passes (karaka_plan.md §2 + avyayībhāva samāsa plan).
        l = self._main_sutras  # noqa: E741
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
                                          and s.isTriggered(*self.view(s, node, ix), context=self.view_context(s, node, ix)))]
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
                                          and s.isTriggered(*self.view(s, node, ix), context=self.view_context(s, node, ix)))]
                    # Break at first index from left where trigger occurs
                    _ix = ix
                    break
        if not (found_pratyaya or found_samasa):
            _ix = 0
            ix = _ix
            logger.debug(f"No pratyaya or samAsa. Checking for rule triggers at window 0")
            if len(node.outputs) != 1:
                triggered = [s for s in l if ((s.aps not in node.outputs[ix].disabled_sutras)  and s.isTriggered(*self.view(s, node, ix), context=self.view_context(s, node, ix)))]

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
            ctx = self.view_context(s, node, ix)
            logger.debug(f"Sutra {s} View {v} Disabled: {[s for s in v[0].disabled_sutras]}")
            assert s.aps not in v[0].disabled_sutras
            # Transformation
            r = s.operate(*v, context=ctx)
            r0 = r[0]
            v0 = v[0]
            # State update
            r = s.update(*v, *r, context=ctx)
            r = s.insert(*v, *r, context=ctx)
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
                                           capture_eval=self._capture_eval,
                                           karaka=False)
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

            # 6.4.22 ābhīya asiddhavat composition.
            # If v (the view used by operate) is a snapshot of a *prior*
            # ābhīya state (i.e. peers have already fired and the current
            # node.outputs differs from v at this window), compose this
            # rule's snapshot-relative diff with the prior peer edits
            # so both effects survive in the new node. For the very
            # first ābhīya fire at a window, v IS the current state and
            # no composition is needed — the standard path applies.
            if (_in_abhiya(getattr(s, '_aps_num', None))
                    and getattr(s, 'aps', None) in _ASIDDHA_PEERS
                    and (v[0] is not node.outputs[ix]
                         or v[1] is not node.outputs[ix+1])):
                snap_lp = v[0].canonical()
                snap_rp = v[1].canonical()
                curr_lp = node.outputs[ix].canonical()
                curr_rp = node.outputs[ix+1].canonical()
                tgt_lp  = r[0].canonical()
                tgt_rp  = r[1].canonical()
                composed_lp = _compose_abhiya(snap_lp, curr_lp, tgt_lp)
                composed_rp = _compose_abhiya(snap_rp, curr_rp, tgt_rp)
                if composed_lp != tgt_lp:
                    r[0].update(composed_lp, sanscript.SLP1)
                if composed_rp != tgt_rp:
                    r[1].update(composed_rp, sanscript.SLP1)
                # Compose tags/its/disabled_sutras: keep current's, add this
                # rule's contributions (delta vs snapshot).
                for side, v_obj, c_obj in ((0, v[0], node.outputs[ix]),
                                           (1, v[1], node.outputs[ix+1])):
                    snap_tags = set(v_obj.tags); snap_its = set(v_obj.its)
                    snap_dis  = set(v_obj.disabled_sutras)
                    tgt_tags  = set(r[side].tags); tgt_its = set(r[side].its)
                    tgt_dis   = set(r[side].disabled_sutras)
                    merged_tags = set(c_obj.tags) | (tgt_tags - snap_tags)
                    merged_its  = set(c_obj.its)  | (tgt_its  - snap_its)
                    merged_dis  = set(c_obj.disabled_sutras) | (tgt_dis - snap_dis)
                    # Removed-by-target tags get cleared too (rare; e.g.
                    # a rule that drops a tag from snapshot).
                    merged_tags -= (snap_tags - tgt_tags)
                    merged_its  -= (snap_its  - tgt_its)
                    r[side].tags = list(merged_tags)
                    r[side].its  = list(merged_its)
                    r[side].disabled_sutras = list(merged_dis)
                    # Preserve disabled_by from current
                    for aps, by in c_obj.disabled_by.items():
                        if aps not in r[side].disabled_by:
                            r[side].disabled_by[aps] = by
                logger.debug(f"Ābhīya composed [{s.aps}]: "
                             f"snap={snap_lp}|{snap_rp} curr={curr_lp}|{curr_rp} "
                             f"tgt={tgt_lp}|{tgt_rp} -> {r[0].canonical()}|{r[1].canonical()}")
                # r0 still references the (mutated) post-operate object;
                # downstream disabled_sutras append uses r0, which is r[0].

            # 6.1.85 antādivat boundary marking (see _apply_antadivat): an
            # ekādeśa rule has written the single substitute onto rp[0], leaving a
            # consonant-final residue. The marker drives the condition-scoped
            # antavat synthesis in sutra._env and the at-junction disable. It is
            # dropped when the two objects later coalesce (join_objects).
            self._apply_antadivat(s, r)
            # No clear-on-consume: with condition-scoped synthesis (sutra._env
            # for_xform=True) a later rule's xform uses the physical strings, so
            # the substitute is never re-appended onto the left and the marker
            # can persist harmlessly until the merge clears it (join_objects).

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
        # 0. Kāraka pre-pass summary (sentence-level tagging, karaka_plan.md §2)
        for e in self.karaka_log:
            kv = [t for t in e["tags"]
                  if t.startswith(("kAraka_", "viBakti_")) and t != "viBakti_pada"]
            print(f"{indent}  kāraka pre-pass @{e['index']}: "
                  f"fired {e['fired'] or '—'}  →  {', '.join(kv) or 'no tags'}")
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
