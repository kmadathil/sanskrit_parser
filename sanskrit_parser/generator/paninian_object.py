"""
Paninian Object Class

Derived from SanskritObject

@author: kmadathil

"""
from sanskrit_parser.base.sanskrit_base import SanskritObject, SLP1
import logging
logger = logging.getLogger(__name__)


class PaninianObject(SanskritObject):
    """ Paninian Object Class: Derived From SanskritObject

    Attributes:
    """
    def __init__(self, thing=None, encoding=None, unicode_encoding='utf-8',
                 strict_io=True, replace_ending_visarga='s'):
        super().__init__(thing, encoding, unicode_encoding, strict_io,
                         replace_ending_visarga)
        self.inPrakriya = True
        # FIXME: I don't like this being here
        self.disabled_sutras = []
        # Prakriya Related Tags are ephemeral

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
        s = "".join([o.canonical() for o in objects[0]])
        so = PaninianObject(s, encoding=SLP1)
        # Tag rules
        # 1.4.14 suptiNantaM padam
        if objects[0][-1].hasTag("sup") or objects[0][-1].hasTag("tiN"):
            so.setTag("pada")
        # 1.4.13 yasmAtpratyayaviDistadAdipratyayeNgam
        elif objects[0][0].hasTag("aNga"):
            so.setTag("aNga")
        # 3.1.32 sannAdyantA dhAtavaH
        if objects[0][-1].hasTag("sannAdi"):
            so.setTag("DAtu")
        # 1.2.46 krttaDitasamAsAsca
        if objects[0][-1].hasTag("krt") or objects[0][-1].hasTag("tadDita"):
            so.setTag("prAtipadika")

        # Custom tag propagation for rule implementation
        for t in ["eti", "eDati", "UW", "sTA", "sTamB"]:
            if objects[0][0].hasTag(t) and objects[0][0].hasTag("DAtu"):
                so.setTag(t)
        for t in ["AN"]:
            if objects[0][0].hasTag(t) and objects[0][0].hasTag("upasarga"):
                so.setTag(t)
        for t in ["trc", "trn"]:
            if objects[0][-1].hasTag(t) and objects[0][0].hasTag("aNga"):
                so.setTag(t)
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
        return so
