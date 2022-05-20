from indic_transliteration import sanscript
from sanskrit_parser.generator.paninian_object import PaninianObject


class Pratipadika(PaninianObject):
    """ Sanskrit Object Class: Derived From SanskritString

     Attributes:
    """
    def __init__(self, thing=None, linga="pum",
                 other_tags=[], encoding=sanscript.SLP1,
                 unicode_encoding='utf-8',
                 strict_io=True, replace_ending_visarga='s'):
        super().__init__(thing, encoding, unicode_encoding, strict_io, replace_ending_visarga)
        self.linga = linga
        self.inPrakriya = True
        self.setTag("prAtipadika")
        self.setTag(linga)
        # self.setTag("aNga")
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
SamBu = Pratipadika("SamBu", "pum")
go = Pratipadika("go", "pum")
rE = Pratipadika("rE", "pum")

# f
pitf = Pratipadika("pitf", "pum")
nf = Pratipadika("nf", "pum")
tvazwf = Pratipadika("tvazwf", "pum", other_tags=["naptrAdi"])
naptf = Pratipadika("naptf", "pum", other_tags=["naptrAdi"])
nezwf = Pratipadika("nezwf", "pum", other_tags=["naptrAdi"])
kzatf = Pratipadika("kzatf", "pum", other_tags=["naptrAdi"])
hotf = Pratipadika("hotf", "pum", other_tags=["naptrAdi"])
potf = Pratipadika("potf", "pum", other_tags=["naptrAdi"])
praSAstf = Pratipadika("praSAstf", "pum", other_tags=["naptrAdi"])


# क्विबन्ताः विजन्ताश्च प्रातिपदिकत्वं न. जहति, धातुत्वमपि न मुञ्चन्ति
viSvapA = Pratipadika("viSvapA", "pum", other_tags=["DAtu", "vic"])
senAnI = Pratipadika("senAnI", "pum", other_tags=["DAtu", "kvip"])
nI = Pratipadika("nI", "pum", other_tags=["DAtu", "kvip"])
KalapU = Pratipadika("KalapU", "pum", other_tags=["DAtu", "kvip"])
varzABU = Pratipadika("varzABU", "pum", other_tags=["DAtu", "BU", "kvip"])
svayamBU = Pratipadika("svayamBU", "pum", other_tags=["DAtu", "BU", "kvip"])
suDI = Pratipadika("suDI", "pum", other_tags=["DAtu", "kvip", "purvastrI"])

hAhA = Pratipadika("hAhA", "pum")

rAjan = Pratipadika("rAjan", "pum")
mahat = Pratipadika("mahat", "pum")

# FIXME - remove this, derive from qati

kati = Pratipadika("kati", "pum", other_tags=["qati", "nityabahuvacana"])

# saMKyA
tri = Pratipadika("tri", "pum", other_tags=["saMKyA", "nityabahuvacana"])
dvi = Pratipadika("dvi", "pum", other_tags=["saMKyA", "nityadvivacana",
                                            'tyadAdi'])
catur = Pratipadika("catur", "pum", other_tags=["saMKyA", "nityabahuvacana"])
# tri_s = Pratipadika("tri", "strI", other_tags=["saMKyA", "nityabahuvacana"])
# catur_s = Pratipadika("catur", "strI", other_tags=["saMKyA", "nityabahuvacana"])
dvi_s = Pratipadika("dvi", "strI", other_tags=["saMKyA", "nityadvivacana",
                                               'tyadAdi', "Ap"])

# Stri
ap = Pratipadika("ap", "strI", other_tags=["nityabahuvacana"])
mAtf = Pratipadika("mAtf", "strI", other_tags=["svasrAdi"])
svasf = Pratipadika("svasf", "strI", other_tags=["svasrAdi", "naptrAdi"])
tisf = Pratipadika("tisf", "strI", other_tags=["svasrAdi", "saMKyA",
                                               "nityabahuvacana"])
catasf = Pratipadika("catasf", "strI", other_tags=["svasrAdi""saMKyA",
                                                   "nityabahuvacana"])
nanAndf = Pratipadika("nanAndf", "strI", other_tags=["svasrAdi"])
duhitf = Pratipadika("duhitf", "strI", other_tags=["svasrAdi"])
yAtf = Pratipadika("yAtf", "strI", other_tags=["svasrAdi"])

BrU = Pratipadika("BrU", "strI", other_tags=["BrU"])
ramA = Pratipadika("ramA", "strI", other_tags=["Ap"])
nadI = Pratipadika("nadI", "strI", other_tags=["NI"])
niSA = Pratipadika("niSA", "strI", other_tags=["pAdAdi", "Ap"])
nAsikA = Pratipadika("nAsikA", "strI", other_tags=["pAdAdi", "Ap"])
mati = Pratipadika("mati", "strI")
lakzmI = Pratipadika("lakzmI", "strI")  # No NI
strI = Pratipadika("strI", "strI", other_tags=["NI", "strI_p"])
SrI = Pratipadika("SrI", "strI", other_tags=["DAtu", "kvip"])
# to test
Denu = Pratipadika("Denu", "strI")
suBrU = Pratipadika("suBrU", "strI", other_tags=["BrU"])

# Napum

jYAna = Pratipadika("jYAna", "napum")
anya = Pratipadika("anya", "napum", other_tags=["qatarAdi", "sarvanAma"])
anyatara = Pratipadika("anyatara", "napum", other_tags=["qatarAdi", "sarvanAma"])
itara = Pratipadika("itara", "napum", other_tags=["qatarAdi", "sarvanAma"])
qatara = Pratipadika("qatara", "napum", other_tags=["qatarAdi", "sarvanAma"])
qatama = Pratipadika("qatama", "napum", other_tags=["qatarAdi", "sarvanAma"])
vAri = Pratipadika("vAri", "napum")
mahat_n = Pratipadika("mahat", "napum")
payas = Pratipadika("payas", "napum")
SrIpA = Pratipadika("SrIpA", "napum", other_tags=["DAtu", "kvip"])
asTi = Pratipadika("asTi", "napum")
daDi = Pratipadika("daDi", "napum")
sakTi = Pratipadika("sakTi", "napum")
akzi = Pratipadika("akzi", "napum")
atirE = Pratipadika("atirE", "napum")
atinO = Pratipadika("atinO", "napum")


# halanta pum
lih_kvip = Pratipadika("lih", "pum", other_tags=["DAtu", "kvip"])
duh_kvip = Pratipadika("duh", "pum", other_tags=["DAtu", "kvip"])
druh_kvip = Pratipadika("druh", "pum", other_tags=["DAtu", "kvip"])
muh_kvip = Pratipadika("muh", "pum", other_tags=["DAtu", "kvip"])
