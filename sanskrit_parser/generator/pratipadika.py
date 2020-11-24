from paninian_object import PaninianObject
from sanskrit_parser.base.sanskrit_base import SLP1

class Pratipadika(PaninianObject):
    """ Sanskrit Object Class: Derived From SanskritString

     Attributes:
        
    """
    def __init__(self, thing=None, linga= "pum",
                 other_tags=[], encoding=SLP1,
                 unicode_encoding='utf-8',
                 strict_io=True, replace_ending_visarga='s'):
            super().__init__(thing, encoding, unicode_encoding, strict_io, replace_ending_visarga)
            self.linga = linga
            self.inPrakriya = True
            self.setTag("prAtipadika")
            self.setTag(linga)
            #self.setTag("aNga")
            for t in other_tags:
                self.setTag(t)

    def anta(self):
        return self.canonical()[-1]


rAma = Pratipadika("rAma", "pum")
kavi = Pratipadika("kavi", "pum")
hari = Pratipadika("hari", "pum")
saKi = Pratipadika("saKi", "pum", other_tags=["saKi"])
pati = Pratipadika("pati", "pum", other_tags=["pati"])
pAda = Pratipadika("pAda", "pum",  other_tags=["pAdAdi"])
yUza = Pratipadika("yUza", "pum",  other_tags=["pAdAdi"])
sarva = Pratipadika("sarva", "pum", other_tags=["sarvAdi"])
krozwu = Pratipadika("krozwu", "pum")

# f
pitf = Pratipadika("pitf", "pum")
tvazwf = Pratipadika("tvazwf", "pum", other_tags=["svasrAdi"])
naptf = Pratipadika("naptf", "pum", other_tags=["svasrAdi"])
nezwf = Pratipadika("nezwf", "pum", other_tags=["svasrAdi"])
kzatf = Pratipadika("kzatf", "pum", other_tags=["svasrAdi"])
hotf = Pratipadika("hotf", "pum", other_tags=["svasrAdi"])
potf = Pratipadika("potf", "pum", other_tags=["svasrAdi"])
praSAstf = Pratipadika("praSAstf", "pum", other_tags=["svasrAdi"])

# क्विबन्ताः विजन्ताश्च प्रातिपदिकत्वं न. जहति, धातुत्वमपि न मुञ्चन्ति 
viSvapA = Pratipadika("viSvapA", "pum", other_tags=["DAtu", "vic"])
hAhA = Pratipadika("hAhA", "pum")

rAjan = Pratipadika("rAjan", "pum")

# FIXME - remove this, derive from qati

kati = Pratipadika("kati", "pum", other_tags=["qati", "nityabahuvacana"])

# saMKyA
tri = Pratipadika("tri", "pum", other_tags=["saMKyA", "nityabahuvacana"])
dvi = Pratipadika("dvi", "pum", other_tags=["saMKyA", "nityadvivacana",
                                            'tyadAdi'])
# Stri
ap = Pratipadika("ap", "strI", other_tags=["nityabahuvacana"])
mAtf = Pratipadika("mAtf", "strI")
svasf = Pratipadika("svasf", "strI", other_tags=["svasrAdi"])

