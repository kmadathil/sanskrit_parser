"""
Paninian Object Class

Derived from SanskritObject

@author: kmadathil

"""
from indic_transliteration import sanscript
from sanskrit_parser.base.sanskrit_base import SanskritObject

_SLP1_VOWELS = set("aAiIuUfFxXeEoO")
import logging
logger = logging.getLogger(__name__)


class PaninianObject(SanskritObject):
    """ Paninian Object Class: Derived From SanskritObject

    Attributes:
    """
    def __init__(self, thing=None, encoding=None, unicode_encoding='utf-8',
                 strict_io=True, replace_ending_visarga='s', its=None):
        super().__init__(thing, encoding, unicode_encoding, strict_io,
                         replace_ending_visarga)
        self.inPrakriya = True
        # FIXME: I don't like this being here
        self.disabled_sutras = []
        self.disabled_by = {}  # aps -> aps of the sutra that caused disabling
        # Prakriya Related Tags are ephemeral
        # it-markers (anubandha): used by Pratyaya (e.g. śatṛ u-it) and by Pratipadika
        # when an it is added dynamically during prakriyā (e.g. SK360 adds f-it to maghavat).
        self.its = its if its is not None else []

    def hasIt(self, it):
        return it in self.its

    def setIt(self, it):
        if it not in self.its:
            self.its.append(it)

    def deleteIt(self, it):
        if it in self.its:
            self.its.remove(it)

    def hasTag(self, t):
        return t in self.tags

    def deleteTag(self, t):
        return self.tags.remove(t)

    def setTag(self, t):
        if t not in self.tags:
            self.tags.append(t)
        return t

    def fix(self):
        self.inPrakriya = False

    def isPada(self):
        return self.hasTag("pada")

    @classmethod
    def join_objects(cls, objects):
        logger.debug(f"Joining Objects {objects} {type(objects)}")
        for o in objects[0]:
            logger.debug(f"{o} type {type(o)}")
            assert isinstance(o, SanskritObject), f"{o} type {type(o)}"
        # Passthrough
        if len(objects[0]) == 1:
            return objects[0][0]
        parts = objects[0]
        first, last = parts[0], parts[-1]
        s = "".join([o.canonical() for o in parts])
        so = PaninianObject(s, encoding=sanscript.SLP1)

        def _propagate(src, tags, suffix=""):
            """For each t in `tags`: if `src` has it, set `t + suffix` on `so`."""
            for t in tags:
                if src.hasTag(t):
                    so.setTag(t + suffix)

        def _delete_if_present(tags):
            """Bulk-delete any of `tags` that are currently set on `so`."""
            for t in tags:
                if so.hasTag(t):
                    so.deleteTag(t)

        # ── Phase 1: Word-class assignment (pada / aNga / DAtu / prAtipadika / gender) ──

        # --- 1.4.14 suptiNantaM padam: word ending in sup/tiN (or already pada) is a pada ---
        if last.hasTag("sup") or last.hasTag("tiN") or last.hasTag("pada"):
            so.setTag("pada")
            # SK307 (8.4.12): tag the pada if its anga is monosyllabic (ekāc).
            # Use the ?ekac tag (set at Pratipadika init and preserved through
            # phonological transformations) rather than re-counting vowels in
            # the post-guṇa/vṛddhi string (which may have lost its vowel).
            if first.hasTag("ekac"):
                so.setTag("ekac_anga_pada")
        # --- 1.4.13 yasmAtpratyayaviDistadAdipratyayeNgam ---
        elif first.hasTag("aNga"):
            so.setTag("aNga")
            # Propagate ekac to anga results (e.g. kvin forms) so SK307 can
            # fire when the anga later takes a sup/tiN suffix.
            if sum(1 for ch in s if ch in _SLP1_VOWELS) == 1:
                so.setTag("ekac")

        # --- 3.1.32 sannAdyantA dhātavaḥ ---
        if last.hasTag("sannAdi"):
            so.setTag("DAtu")

        # --- kvin/kvip kṛt result is dhātu-like (cf. sannAdi) ---
        # Handles both: (aYc_u | kvin) → ac gets DAtu+aYc+kvin;
        #           and (prati | ac_result) → pratyac gets DAtu+aYc+kvin (ac_result has kvin).
        if last.hasTag("kvin") or last.hasTag("kvip"):
            so.setTag("DAtu")
            _propagate(last, ["aYc", "kvin", "kvip"])
            # Propagate ekac from the anga through kvin/kvip so SK307 can detect
            # a monosyllabic uttara-pada after the kṛt suffix join.
            if first.hasTag("ekac"):
                so.setTag("ekac")

        # --- 1.2.46 kṛttaddhitasamāsāśca ---
        if last.hasTag("krt") or last.hasTag("tadDita"):
            so.setTag("prAtipadika")
            # Propagate it-markers from kṛt/taddhita suffix to merged stem.
            # Needed for SK425 (6.4.14) which checks +u on u-it stems like vatup.
            for it in last.its:
                so.setIt(it)

        # --- Gender: prefer last element's; fall back to first's ---
        for t in ["pum", "strI", "napum"]:
            if last.hasTag(t):
                so.setTag(t)
                break
        else:
            for t in ["pum", "strI", "napum"]:
                if first.hasTag(t):
                    so.setTag(t)
                    break

        # ── Phase 2: Stem identity markers ────────────────────────────────────────

        # --- DAtu-gated semantic tag propagation (custom dhātu identifiers) ---
        if first.hasTag("DAtu"):
            _propagate(first, ["eti", "eDati", "UW", "sTA", "sTamB",
                               "rAj", "rAw", "aYc", "dfS"])

        # --- Stem-class tags for pada-internal sandhi ---
        # 3a: dhātu→kṛt: ?han flows from aNga (dhātu) to derived stem (han+kvip).
        if first.hasTag("han") and first.hasTag("aNga"):
            so.setTag("han")
        # 3b: compound merge: ?han on uttara-pada (samāsa+pada) → samasta_pada.
        if last.hasTag("han") and last.hasTag("pada") and last.hasTag("samAsa"):
            so.setTag("han")
        # AN upasarga propagation.
        if first.hasTag("AN") and first.hasTag("upasarga"):
            so.setTag("AN")

        # --- kṛt suffix classifier tags from last, gated by first being an aNga ---
        # kvin/kvip are omitted here: already propagated by the kvin/kvip DAtu block above.
        if first.hasTag("aNga"):
            # NIp_taddhita (SK470 4.1.15) and yaY (SK471 4.1.16) ride along so the
            # ṅīp-triggering affix class reaches the merged stem (aindra, gārgya …).
            # The ṭiṭ-class needs no entry — the ṭ-it survives via the taddhita setIt
            # loop (line ~128), so SK470's +w condition matches the merged stem.
            _propagate(last, ["trc", "trn", "kaY", "suc", "van", "ka_pratyaya",
                              "NIp_taddhita", "yaY"])

        # --- samasta_Ratva on uttara-pada → samasta_Ratva_pada on compound ---
        if last.hasTag("samasta_Ratva"):
            so.setTag("samasta_Ratva_pada")

        # ── Phase 3: Compound lifecycle ───────────────────────────────────────────

        # --- Compound-context tags (first → result), needed for SK379 pūrva-pada ---
        # bahuvrIhi rides along like samAsa so it survives intermediate merges
        # (e.g. vrAja+kap → vrājaka) and reaches the completed compound stem,
        # letting SK463 (7.3.44) asuwapaH ?!bahuvrIhi guard fire on a derived
        # bahuvrīhi (बहुपरिव्राजका, not बहुपरिव्राजिका).
        _propagate(first, ["samAsa", "samAsaPurva", "vasupada", "udanc", "adas",
                           "bahuvrIhi"])

        # tyadAdi survives ONLY a ka-pratyaya derivation (tad+kan → taka), so
        # 7.2.106 (तदोः सः) still gives nom sg takā → sakā. Gated on ka_pratyaya
        # so ordinary tyadāra compounds (tāvat = tad+vatup, tādṛk = tad+dṛś+kvin)
        # do NOT inherit tyadAdi and keep their normal declension. sarvanAma is
        # intentionally not propagated either: taka declines as a plain a-stem
        # (takāyai, not tasyai).
        if last.hasTag("ka_pratyaya"):
            _propagate(first, ["tyadAdi"])

        # --- pada+pada merge → merged_pada ---
        # Blocks arm-A ṇatva rules (8.4.1/8.4.2/8.4.22) which require ?!merged_pada.
        if first.hasTag("pada") and last.hasTag("pada"):
            so.setTag("merged_pada")

        # --- samasta_pada: compound complete ---
        # L has samAsaPurva+pada and R has samAsa+pada → compound is done:
        # set samasta_pada and consume the in-progress compound tags.
        if (first.hasTag("samAsaPurva") and first.hasTag("pada")
                and last.hasTag("samAsa") and last.hasTag("pada")):
            so.setTag("samasta_pada")
            _delete_if_present(["samAsa", "samAsaPurva"])

        # ── Phase 4: Gender-morphology transformations ────────────────────────────

        # --- samprasāraṇam: inherit all tags from the middle element (parts[1]) ---
        if first.hasTag("samprasAraRam"):
            for tt in parts[1].tags:
                so.setTag(tt)
            if first.hasTag("UW"):
                so.setTag("UW")

        # --- strī forms (NI/Ap/strI_abs on last) ---
        # Set strI, copy all tags from first, drop pum/napum.
        for t in ["NI", "Ap", "strI_abs"]:
            if last.hasTag(t):
                so.setTag("strI")
                so.setTag(t)
                for tt in first.tags:
                    so.setTag(tt)
                _delete_if_present(["pum", "napum"])

        # --- pum_abs on last: restore pum, drop strī-markers, flag pUrvastrI ---
        if last.hasTag("pum_abs"):
            so.setTag("pum")
            for tt in parts[-2].tags:
                so.setTag(tt)
            _delete_if_present(["NI", "Ap", "strI_abs", "strI"])
            so.setTag("pUrvastrI")
            if so.hasTag("napum"):
                so.deleteTag("napum")

        # ── Phase 5: Pada-indexed tags (_pada variants, blocking/sandhi guards) ─────

        # --- Vibhakti case/number from pratyaya (last) → merged pada (_pada suffix) ---
        # Stored as tag+"_pada" to distinguish merged-pada tags from raw suffix tags.
        # Rules firing at (aNga | raw-suffix) still see the original tags on the suffix.
        # Rules checking the merged pada on the left (SK404, 1.1.11) use the _pada variants.
        # This prevents 6.1.102 from firing at (prefix | merged-pada) junctions.
        _propagate(last, ["praTamA", "dvitIyA", "tftIyA", "caturTi", "pancamI",
                          "zazWI", "saptamI", "ekavacana", "dvivacana",
                          "bahuvacana", "viBakti"], suffix="_pada")

        # --- First-element tags that get a "_pada" counterpart when result is a pada ---
        # Mechanics are identical; comments mark each origin group so SK references
        # and rule provenance are preserved.
        if so.hasTag("pada"):
            _propagate(first, [
                # kvin/kvip/kaY/etc. are on the left (prAtipadika), not the suffix
                "kvin", "kvip", "kaY", "dfS", "ksa", "vatup", "suc",
                # sarvanAma/avyaya: pronouns carry sarvanAma_pada on merged form
                "sarvanAma", "avyaya",
                # tad/etad: SK176 su-lopa needs to identify these specifically post-merge
                "tad", "etad",
                # indra/pums: carry *_pada on merged form
                "indra", "pums",
                # aYc_u forms: sam_pada/saha_pada/tiras_pada;
                # satva_kfkamkaMsAdi (SK160) and pada_p (SK161) propagate as _pada
                "sam", "saha", "tiras", "satva_kfkamkaMsAdi", "pada_p",
                "vizvag", "deva",
                "ahan"
            ], suffix="_pada")

        # --- na_pada: vApadAntasya/monoDatoH blocks further naScApadAntasya on pada creation ---
        if first.hasTag("na_pada"):
            so.setTag("na_pada")

        # --- AdeSa_s (skipped when first is already viBakti_pada) ---
        if first.hasTag("AdeSa_s") and not first.hasTag("viBakti_pada"):
            so.setTag("AdeSa_s")

        return so
