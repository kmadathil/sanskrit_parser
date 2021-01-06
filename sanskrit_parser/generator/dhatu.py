from sanskrit_parser.generator.paninian_object import PaninianObject
from sanskrit_parser.base.sanskrit_base import SLP1


class Dhatu(PaninianObject):
    """ Sanskrit Object Class: Derived From SanskritString

     Attributes:
    """
    def __init__(self, thing=None, its=[], other_tags=[], encoding=SLP1,
                 unicode_encoding='utf-8',
                 strict_io=True, replace_ending_visarga='s'):
        super().__init__(thing, encoding, unicode_encoding, strict_io, replace_ending_visarga)
        self.inPrakriya = True
        self.its = its
        self.setTag("DAtu")
        self.setTag("aNga")
        for t in other_tags:
            self.setTag(t)

    def hasIt(self, it):
        return it in self.its


iR = Dhatu("i", its=["R"], other_tags=["eti"])
eDa = Dhatu("eD", other_tags=["eDati"], its=["a"])
lUY = Dhatu("lU", its=["Y"])
kzI = Dhatu("kzI")
ji = Dhatu("ji")
wukrIY = Dhatu("krI", its=["Y", "wu"])
veY = Dhatu("veY", its=["Y"])
fcCa = Dhatu("fcC", its=["~a"])
Cad = Dhatu("Cad")
mud = Dhatu("mud")
vid = Dhatu("vid")
gfj = Dhatu("gfj")
BU = Dhatu("BU")
as_dhatu = Dhatu("as")
qulaBaz = Dhatu("laB", its=["~a", "z", "qu"])
guhU = Dhatu("guh", its=["~u"])
sTA = Dhatu("sTA", other_tags=["sTA"])

# FIXME: temporary for testing, samprasarana version of veY. Remove later
veY_smp = Dhatu("u", its=["Y"])
