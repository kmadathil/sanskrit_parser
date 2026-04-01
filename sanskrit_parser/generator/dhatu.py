from indic_transliteration import sanscript
from sanskrit_parser.generator.paninian_object import PaninianObject


class Dhatu(PaninianObject):
    """ Sanskrit Object Class: Derived From SanskritString

     Attributes:
    """
    def __init__(self, thing=None, its=[], other_tags=[], encoding=sanscript.SLP1,
                 unicode_encoding='utf-8',
                 strict_io=True, replace_ending_visarga='s'):
        super().__init__(thing, encoding, unicode_encoding, strict_io, replace_ending_visarga, its=its)
        self.inPrakriya = True
        self.setTag("DAtu")
        self.setTag("aNga")
        self.setTag(self.canonical())
        for t in other_tags:
            self.setTag(t)


iR = Dhatu("i", its=["R"], other_tags=["eti"])
eDa = Dhatu("eD", other_tags=["eDati"], its=["a"])
lUY = Dhatu("lU", its=["Y"])
kzI = Dhatu("kzI")
ji = Dhatu("ji")
qukrIY = Dhatu("krI", its=["Y", "qu"])
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
duh = Dhatu("duh", its=[])
dfS = Dhatu("dfS", its=[], other_tags=["dfS"])
vah = Dhatu("vah", its=[])
Sam = Dhatu("Sam", its=[])

# FIXME: temporary for testing, samprasarana version of veY. Remove later
veY_smp = Dhatu("u", its=["Y"])

aYc_u = Dhatu("aYc", its=['u'])     # √añc with u-it; anidita → SK415 applies; ?aYc → SK361 nUM
