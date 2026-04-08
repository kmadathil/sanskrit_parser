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
        s = "".join([o.canonical() for o in objects[0]])
        so = PaninianObject(s, encoding=sanscript.SLP1)
        # Tag rules
        # 1.4.14 suptiNantaM padam
        if objects[0][-1].hasTag("sup") or objects[0][-1].hasTag("tiN") or objects[0][-1].hasTag("pada"):
            so.setTag("pada")
            # SK307 (8.4.12): tag the pada if its anga is monosyllabic (ekāc).
            # Use the ?ekac tag (set at Pratipadika init and preserved through
            # phonological transformations) rather than re-counting vowels in
            # the post-guṇa/vṛddhi string (which may have lost its vowel).
            if objects[0][0].hasTag("ekac"):
                so.setTag("ekac_anga_pada")
        # 1.4.13 yasmAtpratyayaviDistadAdipratyayeNgam
        elif objects[0][0].hasTag("aNga"):
            so.setTag("aNga")
            # Propagate ekac to anga results (e.g. kvin forms) so SK307 can
            # fire when the anga later takes a sup/tiN suffix.
            if sum(1 for ch in s if ch in _SLP1_VOWELS) == 1:
                so.setTag("ekac")
        # 3.1.32 sannAdyantA dhAtavaH
        if objects[0][-1].hasTag("sannAdi"):
            so.setTag("DAtu")
        # kvin/kvip krit result is dhatu-like (cf. sannAdi); set DAtu and propagate semantic tags.
        # Handles both: (aYc_u | kvin) → ac gets DAtu+aYc+kvin;
        #           and (prati | ac_result) → pratyac gets DAtu+aYc+kvin (ac_result has kvin).
        if objects[0][-1].hasTag("kvin") or objects[0][-1].hasTag("kvip"):
            so.setTag("DAtu")
            for t in ["aYc", "kvin", "kvip"]:
                if objects[0][-1].hasTag(t):
                    so.setTag(t)
            # Propagate ekac from the anga through kvin/kvip so SK307 can detect
            # a monosyllabic uttara-pada after the krit suffix join.
            if objects[0][0].hasTag("ekac"):
                so.setTag("ekac")
        # 1.2.46 krttaDitasamAsAsca
        if objects[0][-1].hasTag("krt") or objects[0][-1].hasTag("tadDita"):
            so.setTag("prAtipadika")
            # Propagate it-markers from kṛt/taddhita suffix to merged stem
            # Needed for SK425 (6.4.14) which checks +u on u-it stems like vatup
            for it in objects[0][-1].its:
                so.setIt(it)

        # Propagate gender tags (pum/strI/napum) for pratipadika + kft situations
        # 1. If kft (last element) has pum/strI/napum, use that
        # 2. Else, if pratipadika (first element) has pum/strI/napum, propagate that
        for t in ["pum", "strI", "napum"]:
            if objects[0][-1].hasTag(t):
                so.setTag(t)
                break
        else:
            for t in ["pum", "strI", "napum"]:
                if objects[0][0].hasTag(t):
                    so.setTag(t)
                    break

        if objects[0][0].hasTag("samprasAraRam"):
            for tt in objects[0][1].tags:
                    so.setTag(tt)
            if objects[0][0].hasTag("UW"):
                 so.setTag("UW")
            
        
        # Custom tag propagation for rule implementation
        for t in ["eti", "eDati", "UW", "sTA", "sTamB", "rAj", "rAw", "aYc", "dfS"]:
            if objects[0][0].hasTag(t) and objects[0][0].hasTag("DAtu"):
                so.setTag(t)
        # Propagate compound-context tags (needed for SK379 pūrva-pada rule)
        for t in ["samAsa", "samAsaPurva", "vasupada", "udanc", "adas"]:
            if objects[0][0].hasTag(t):
                so.setTag(t)
        # Any pada+pada merge produces merged_pada, blocking arm-A ṇatva rules
        # (8.4.1/8.4.2/8.4.22) which require ?!merged_pada.
        if objects[0][0].hasTag("pada") and objects[0][-1].hasTag("pada"):
            so.setTag("merged_pada")
        # Final compound merge: when L has samAsaPurva+pada and R has samAsa+pada,
        # the compound is complete — set samasta_pada and consume the compound tags.
        if (objects[0][0].hasTag("samAsaPurva") and objects[0][0].hasTag("pada")
                and objects[0][-1].hasTag("samAsa") and objects[0][-1].hasTag("pada")):
            so.setTag("samasta_pada")
            if so.hasTag("samAsa"):
                so.deleteTag("samAsa")
            if so.hasTag("samAsaPurva"):
                so.deleteTag("samAsaPurva")
        # Propagate stem-class tags needed for pada-internal sandhi rules
        # 3a: dhātu→kṛt: ?han flows from aNga (dhātu) to derived stem (han+kvip)
        for t in ["han"]:
            if objects[0][0].hasTag(t) and objects[0][0].hasTag("aNga"):
                so.setTag(t)
        # 3b: compound merge: ?han on uttara-pada (samAsa+pada) propagates to samasta_pada
        for t in ["han"]:
            if objects[0][-1].hasTag(t) and objects[0][-1].hasTag("pada") and objects[0][-1].hasTag("samAsa"):
                so.setTag(t)
        for t in ["AN"]:
            if objects[0][0].hasTag(t) and objects[0][0].hasTag("upasarga"):
                so.setTag(t)
        for t in ["trc", "trn", "kvin", "kvip", "kaY"]:
            if objects[0][-1].hasTag(t) and objects[0][0].hasTag("aNga"):
                so.setTag(t)
        # Propagate samasta_Ratva from uttara-pada to merged compound as samasta_Ratva_pada
        for t in ["samasta_Ratva"]:
            if objects[0][-1].hasTag(t):
                so.setTag(t + "_pada")
        for t in ["NI", "Ap", 'strI_abs']:
            if objects[0][-1].hasTag(t):
                so.setTag("strI")
                so.setTag(t)
                for tt in objects[0][0].tags:
                    so.setTag(tt)
                if so.hasTag("pum"):
                    so.deleteTag("pum")
                if so.hasTag("napum"):
                    so.deleteTag("napum")
        for t in ['pum_abs']:
            if objects[0][-1].hasTag(t):
                so.setTag("pum")
                for tt in objects[0][-2].tags:
                    so.setTag(tt)
                for tt in ["NI", "Ap", 'strI_abs', "strI"]:
                    if so.hasTag(tt):
                        so.deleteTag(tt)
                    so.setTag("pUrvastrI")
                if so.hasTag("napum"):
                    so.deleteTag("napum")

        # Propagate vibhakti case/number tags from last element (pratyaya) onto merged pada.
        # Stored as tag+"_pada" to distinguish merged-pada tags from raw suffix tags.
        # Rules firing at (aNga | raw-suffix) still see the original tags on the suffix.
        # Rules checking the merged pada on the left (SK404, 1.1.11) use the _pada variants.
        # This prevents 6.1.102 from firing at (prefix | merged-pada) junctions.
        for t in ["praTamA", "dvitIyA", "tftIyA", "caturTi", "pancamI",
                  "zazWI", "saptamI", "ekavacana", "dvivacana", "bahuvacana", "viBakti"]:
            if objects[0][-1].hasTag(t):
                so.setTag(t + "_pada")
        # kvin/kvip/kaY are on the left (prAtipadika), not the suffix — same _pada pattern
        for t in ["kvin", "kvip", "kaY", "dfS", "ksa", "vatup"]:
            if objects[0][0].hasTag(t):
                so.setTag(t + "_pada")
        # sarvanAma propagation: pronouns carry sarvanAma_pada on the merged form
        for t in ["sarvanAma"]:
            if objects[0][0].hasTag(t):
                so.setTag(t + "_pada")

        # Propagate sam_pada/saha_pada/tiras_pada for aYc_u forms
        for t in ["sam", "saha", "tiras"]:
            if objects[0][0].hasTag(t):
                so.setTag(t+"_pada")


        # vApadAntasya / monoDatoH must block further naScApadAntasya on pada creation
        for t in ["na_pada"]:
            if objects[0][0].hasTag(t):
                so.setTag("na_pada")
      
                
        return so
