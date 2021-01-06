from sanskrit_parser.generator.paninian_object import PaninianObject
from sanskrit_parser.base.sanskrit_base import SLP1


class Pratyaya(PaninianObject):
    """ Sanskrit Object Class: Derived From SanskritString

     Attributes:
    """
    def __init__(self, thing=None, its=[], other_tags=[], encoding=SLP1,
                 unicode_encoding='utf-8',
                 strict_io=True, replace_ending_visarga='s'):
        super().__init__(thing, encoding, unicode_encoding, strict_io, replace_ending_visarga)
        self.inPrakriya = True
        self.its = its
        self.setTag("pratyaya")
        for t in other_tags:
            self.setTag(t)

    def hasIt(self, it):
        return it in self.its

    def setIt(self, it):
        if it not in self.its:
            self.its.append(it)

    def deleteIt(self, it):
        return self.its.remove(it)

    def luTags(self):
        _l = []
        for t in self.tags:
            if not (t in ["luk", "Slu", "lup"]):
                _l.append(t)
        for t in _l:
            self.tags.remove(t)


tuk = Pratyaya("t", its=["k"])

# Aw (agama)
Aw = Pratyaya("A", its=["w"], other_tags=["Aw"])
yAw = Pratyaya("yA", its=["w"], other_tags=["yAw"])
syAw = Pratyaya("syA", its=["w"], other_tags=["syAw"])

tip = Pratyaya("ti", its=["p"], other_tags=["sArvaDAtuka"])
Sap = Pratyaya("a", its=["S", "p"], other_tags=["sArvaDAtuka"])


Ryat = Pratyaya("ya", its=["t", "R"], other_tags=["ArDaDAtuka"])
GaY = Pratyaya("a", its=["G", "Y"], other_tags=["ArDaDAtuka"])
Ric = Pratyaya("i", its=["R", "c"], other_tags=["ArDaDAtuka"])
tfc = Pratyaya("tf", its=["c"], other_tags=["ArDaDAtuka"])
yat = Pratyaya("ya", its=["t"], other_tags=["ArDaDAtuka"])
yak = Pratyaya("ya", its=["k"], other_tags=["ArDaDAtuka"])
ktvA = Pratyaya("tvA", its=["k"], other_tags=["ArDaDAtuka", "avyaya"])
kta = Pratyaya("ta", its=["k"], other_tags=["ArDaDAtuka"])

# tiN
tip = Pratyaya("ti", its=["p"], other_tags=["tiN", "sArvaDAtuka"])
sip = Pratyaya("si", its=["p"], other_tags=["tiN", "sArvaDAtuka"])


# nIpAtAs
AN = Pratyaya("A", its=["N"], other_tags=["nipAta", "upasarga", "pada"])
mAN = Pratyaya("mA", its=["N"], other_tags=["nipAta", "upasarga", "pada"])
upa = Pratyaya("upa", other_tags=["nipAta", "upasarga", "pada"])
pra = Pratyaya("pra", other_tags=["nipAta", "upasarga", "pada"])
ava = Pratyaya("ava", other_tags=["nipAta", "upasarga", "pada"])
ud = Pratyaya("ud", other_tags=["nipAta", "upasarga", "pada"])


# bha when applied to prAtipadikas only!
# FIXME - maybe have two yats?
yat_t = Pratyaya("ya", its=["t"], other_tags=["svAdi", "tadDita"])
zyaY_t = Pratyaya("ya", its=["z", "Y"], other_tags=["svAdi", "tadDita"])
yaY_t = Pratyaya("ya", its=["Y"], other_tags=["svAdi", "tadDita"])
aR_t = Pratyaya("a", its=["R"], other_tags=["svAdi", "tadDita"])

# sup
# स्वौजसमौट्छष्टाभ्याम्भिस्ङेभ्याम्भ्यस्ङसिभ्याम्भ्यस्ङसोसाम्ङ्योस्सुप्
su = Pratyaya("s", its=["u~"], other_tags=["svAdi", "sup",  "su", "suw"])
O = Pratyaya("O", other_tags=["svAdi", "sup", "O", "suw"])   # noqa 741
jas = Pratyaya("as", its=["j"], other_tags=["svAdi", "sup", "jas",
                                            "suw"])
am = Pratyaya("am", other_tags=["svAdi", "sup", "suw", "am"])
Ow = Pratyaya("O", its=["w"], other_tags=["svAdi", "Ow", "sup", "suw"])
Sas = Pratyaya("as", its=["S"], other_tags=["svAdi", "sup", "Sas"])
wA = Pratyaya("A", its=["w"], other_tags=["svAdi", "wA", "sup"])
ByAm = Pratyaya("ByAm", other_tags=["svAdi", "ByAm", "sup"])
Bis = Pratyaya("Bis", other_tags=["svAdi", "Bis", "sup"])
Ne = Pratyaya("e", its=["N"], other_tags=["svAdi", "Ne", "sup"])
ByAm2 = Pratyaya("ByAm", other_tags=["svAdi", "ByAm", "sup"])
Byas = Pratyaya("Byas", other_tags=["svAdi", "Byas", "sup"])
Nasi = Pratyaya("as", its=["N", "i~"], other_tags=["svAdi", "Nasi", "sup"])
ByAm3 = Pratyaya("ByAm", other_tags=["svAdi", "ByAm", "sup"])
Byas2 = Pratyaya("Byas", other_tags=["svAdi",  "Byas", "sup"])
Nas = Pratyaya("as", its=["N"], other_tags=["svAdi", "Nas", "sup"])
os = Pratyaya("os", other_tags=["svAdi", "os", "sup"])
Am = Pratyaya("Am", other_tags=["svAdi", "Am", "sup"])
Ni = Pratyaya("i", its=["N"], other_tags=["svAdi", "Ni", "sup"])
os2 = Pratyaya("os", other_tags=["svAdi", "os", "sup"])
sup = Pratyaya("su", its=["p"], other_tags=["svAdi", "sup"])
su2 = Pratyaya("s", its=["u~"], other_tags=["svAdi", "sup", "suw", "su",
                                            "sambudDi"])
O2 = Pratyaya("O", other_tags=["svAdi", "O", "sup", "suw"])
jas2 = Pratyaya("as", its=["j"], other_tags=["svAdi", "sup", "suw", "jas"])

sups = [[su, O, jas],
        [am, Ow, Sas],
        [wA, ByAm, Bis],
        [Ne, ByAm2, Byas],
        [Nasi, ByAm3, Byas2],
        [Nas, os, Am],
        [Ni, os, sup],
        [su2, O2, jas2]]

for p in sups:
    for ix, v in enumerate(["ekavacana", "dvivacana", "bahuvacana"]):
        p[ix].setTag(v)

for ix, v in enumerate(["praTamA", "dvitIyA", "tftIyA", "caturTi",
                        "pancamI", "zazWI", "saptamI", "samboDana"]):
    for p in sups[ix][:]:
        p.setTag(v)
        p.setTag("viBakti")

# SI - jasaH SI
SI = Pratyaya("I", its=["S"], other_tags=["svAdi", "sup", "SI"])
# Si - jasSasaH Si
Si = Pratyaya("i", its=["S"], other_tags=["svAdi", "sup", "Si",
                                          "sarvanAmasTAna"])
# adaw - for watarAdi
adaq = Pratyaya("ad", its=["q"], other_tags=["svAdi", "sup", "adaq"])

# StrI
NIp = Pratyaya("I", its=["N", "p"], other_tags=["svAdi", "NI", "strI"])
NIz = Pratyaya("I", its=["N", "z"], other_tags=["svAdi", "NI", "strI"])
Ap = Pratyaya("A", its=["p"], other_tags=["svAdi", "Ap", "strI"])
strI_abs = Pratyaya("", its=[], other_tags=["strI_abs", "strI"])

# Sup Luk
luk_sup = Pratyaya("", its=[], other_tags=["sup"])

# Sambuddhi
sambudDi = PaninianObject("")
sambudDi.setTag("sambudDi")

# Anta
avasAna = PaninianObject(".")
avasAna.setTag("avasAna")
