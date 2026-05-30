import copy
from indic_transliteration import sanscript
from sanskrit_parser.generator.paninian_object import PaninianObject


class Pratipadika(PaninianObject):
    """ Sanskrit Object Class: Derived From SanskritString

     Attributes:
    """
    def __init__(self, thing=None, linga="pum",
                 its=None, other_tags=None, encoding=sanscript.SLP1,
                 unicode_encoding='utf-8',
                 strict_io=True, replace_ending_visarga='s'):
        super().__init__(thing, encoding, unicode_encoding, strict_io, replace_ending_visarga, its=its)
        self.linga = linga
        self.inPrakriya = True
        self.setTag("prAtipadika")
        self.setTag(linga)
        # self.setTag("aNga")
        for t in (other_tags if other_tags is not None else []):
            self.setTag(t)
        # Auto-tag monosyllabic pratipadikas (ekāc) — survives phonological
        # transformations (update() preserves tags) so downstream rules can
        # check ?ekac even after guṇa/vṛddhi strips the vowel from the string.
        _vowels = set("aAiIuUfFxXeEoO")
        if sum(1 for ch in self.canonical() if ch in _vowels) == 1:
            self.setTag("ekac")

    def anta(self):
        return self.canonical()[-1]

# FIXME: Remove this once proper context handling is done
# solution is to let rules look further left and right for context
def in_context(p, tag):
    """Return a deep copy of pratipadika p with ?tag tag set.

    test entries (vibhaktis_list.py) to tag a member being in particular context.

    Must use deepcopy: shallow copy shares the tags list and would mutate the original.
    """
    pc = copy.deepcopy(p)
    pc.setTag(tag)
    return pc

def in_compound(p):
    return in_context(p, "samAsa")

def as_purva_pada(p):
    """Return a deep copy of pratipadika p with samAsaPurva tag set.

    Marks the pūrva-pada in a compound so that join_objects() can detect
    the final compound merge (samAsaPurva+pada + samAsa+pada → samasta_pada).
    """
    return in_context(p, "samAsaPurva")


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
indra = Pratipadika("indra", "pum", other_tags=["indra"])
rE = Pratipadika("rE", "pum")
bahu = Pratipadika("bahu", "pum")  # SK462: pūrva-pada of बहुराजन् bahuvrīhi
# parivrAjaka: ṇvul-derivative (pari+√vraj+ṇvul), an 'aka'-final ka-pratyaya stem.
# SK463 (7.3.44) idādeśa fires standalone (परिव्राजिका) but is blocked by ?!bahuvrIhi
# when it ends a bahuvrīhi (बहुपरिव्राजका — asuwapaH exception).
parivrAjaka = Pratipadika("parivrAjaka", "pum", other_tags=["ka_pratyaya"])
# Raw pieces for deriving (bahu+pari+vrAja+kap) without a pre-formed stem — used to
# test that ?bahuvrIhi propagates (like samAsa) through the vrAja+kap ka-pratyaya merge.
pari  = Pratipadika("pari",  "pum")
vrAja = Pratipadika("vrAja", "pum")
# SK470/471 (4.1.15/16) taddhita-ṅīp test bases: aindra (indra+aṇ), autsa (utsa+añ),
# ūru+dvayasac/daghnac/mātrac, pañca+tayap, gārga (garga+yañ). indra/yad/dfS exist.
utsa  = Pratipadika("utsa",  "pum")
Uru   = Pratipadika("Uru",   "pum")
paYca = Pratipadika("paYca", "pum")
garga = Pratipadika("garga", "pum")
# vidyA: SK472 negative test base — विद्या + अण् → वैद्य (the 'ya' is base-internal,
# NOT a taddhita ya), so ṅīp gives वैद्यी (no ya-lopa), cf. SC Vasu.
vidyA = Pratipadika("vidyA", "strI")
# kuru + car: SK470 ṭiṭ (टित्) test — कुरुचर + ṅīp → कुरुचरी. The ṭit affix is modelled
# with wac (टच्, the available ṭ-it samāsānta affix); strictly कुरुचर is चरेष्टः (3.2.16) ट.
kuru = Pratipadika("kuru", "pum")
car  = Pratipadika("car",  "pum")
# suparRA: SK470 ḍha (ḍhak) test base — सुपर्णा + ढक् → (7.1.2 ḍh→eya) सुपर्णेय → सुपर्णेयी.
# PARTIAL: ādivṛddhi सु→सौ pending (needs 7.2.118 किति च), so not yet साौपर्णेयी.
suparRA = Pratipadika("suparRA", "strI")
# SK470 ṭhak/ṭhañ test bases: akṣa+ṭhak → akṣika → akṣikī (PARTIAL, vṛddhi pending →
# ākṣikī); lavaṇa+ṭhañ → lāvaṇika → लावणिकी (complete, vṛddhi via 7.2.117 ñit).
akza   = Pratipadika("akza",   "pum")
lavaRa = Pratipadika("lavaRa", "pum")
# SK476 (4.1.18) test base: lohita+yaY+sPa → लौहित्यायन → लौहित्यायनी (no ṇatva).
# SK477 (4.1.19) reuses kuru (above) for कौरव्यायणी.
lohita = Pratipadika("lohita", "pum")

# SK478 (4.1.20 वयसि प्रथमे) test bases: a-final stems denoting "early age"
# (prathama vayas) → ङीप् (apavāda to 4.1.4 ṭāp). The ?vayasi_prathama tag
# carries the semantic selection. कुमारी / किशोरी / बर्करी.
kumAra  = Pratipadika("kumAra",  "pum", other_tags=["vayasi_prathama"])
kiSora  = Pratipadika("kiSora",  "pum", other_tags=["vayasi_prathama"])
barkara = Pratipadika("barkara", "pum", other_tags=["vayasi_prathama"])

# SK479 (4.1.21 द्विगोः) Dvigu uttara-pada test stems. The ?dvigu tag is set
# by the test composer via in_context(in_compound(loka), "dvigu") and rides
# through join_objects() (paninian_object.py allowlist) to reach the merged
# stem. त्रिलोकी positive (loka), त्र्यनीका negative (anIka — ?ajAdi so SK454
# ṭāp wins over SK479 ṅīp).
loka  = Pratipadika("loka",  "pum")
anIka = Pratipadika("anIka", "napum", other_tags=["ajAdi"])
# Pala (फल): napum ajādi stem. Drives त्रिफला (Vasu's exact example on SK479)
# via the ajādi-prabalatva apavāda 4.1.4.1.
Pala  = Pratipadika("Pala",  "napum", other_tags=["ajAdi"])

# SK480/481/482 (4.1.22/23/24) tadDita-luk Dvigu test bases.
# Semantic class tags ride from uttara-pada to the compound stem via the
# samāsa-gated propagation in paninian_object.join_objects (alongside ?ajAdi);
# the ?luk_tadDita tag is added on the anga+luk_tadDita merge under the aṅga guard.
#   aSva    — pañca+aśva: aśva ≠ parimāṇa  → SK480 ṭāp → पञ्चाश्वा
#   bista, Acita, kambalya — bistāḍi gaṇa → SK480 ṭāp → द्विबिस्ता, द्व्याचिता, द्विकम्बल्या
#   AQaka  — parimāṇa counter → SK480 blocked → SK479 ṅīp → द्व्याढकी
#   kARqa   — SK481 ṭāp in kzetre sense; SK479 ṅīp otherwise
#   puruza  — SK482 vibhāṣā: ṅīp re-enabled optionally in pramāṇa sense
aSva     = Pratipadika("aSva",     "pum")
bista    = Pratipadika("bista",    "pum",   other_tags=["bistAdi"])
Acita    = Pratipadika("Acita",    "napum", other_tags=["bistAdi"])
kambalya = Pratipadika("kambalya", "pum",   other_tags=["bistAdi"])
AQaka   = Pratipadika("AQaka",   "pum",   other_tags=["parimARa"])
kARqa    = Pratipadika("kARqa",    "pum",   other_tags=["kARqa"])
puruza   = Pratipadika("puruza",   "pum",   other_tags=["puruza"])

# SK483-485 (5.4.131 / 4.1.25 / 4.1.26): ūdhas-bahuvrīhi feminine cluster.
# UDas (long ū) tagged ?uDanta so SK483/484 can fire only on this stem. The
# bahuvrīhi / saMKyAdi / avyayAdi properties are attached by the test composer
# via in_context (matching the trilokI / dvipuruzI pattern) and seen directly
# on UDas at the (UDas | strI_abs) window — no propagation needed.
UDas    = Pratipadika("UDas",    "napum", other_tags=["uDanta"])
kuRqa   = Pratipadika("kuRqa",   "napum")
Gawa    = Pratipadika("Gawa",    "pum")
# ati: avyaya pūrva-pada for atyUDnI (SK485 avyayādi arm)
ati     = Pratipadika("ati",     "pum",   other_tags=["avyaya"])

# SK486 (4.1.27) test bases. ?dAman / ?hAyana let the rule target these stems;
# the test composer also adds ?saMKyAdi and (for hāyana) ?vayasi + ?triCatur
# for the vārttika (n→ṇ for tri/catur+hāyana in age sense).
dAman   = Pratipadika("dAman",   "napum", other_tags=["dAman"])
hAyana  = Pratipadika("hAyana",  "pum",   other_tags=["hAyana"])

# in-stems (iN suffix: possessive adjectives ending in -in)
# 6.4.12 blocks 6.4.8 before O/jas/am/Ow; 6.4.13 re-enables for su (nom sg)
hastin = Pratipadika("hastin", "pum")
yogin = Pratipadika("yogin", "pum")

# paTin-group: SK365 (7.1.85) ā before su; SK366 (7.1.86) i→a before sarvanAmasTAna;
# SK367 (7.1.87) T→nT before sarvanAmasTAna (paTin/maTin only, both have T=th);
# SK368 (7.1.88) ṭi-lopa (delete final i+n) in bha position
paTin = Pratipadika("paTin", "pum", other_tags=["paTin", "paTinTh"])
maTin = Pratipadika("maTin", "pum", other_tags=["paTin", "paTinTh"])
fBukzin = Pratipadika("fBukzin", "pum", other_tags=["paTin"])

# Special an-stems listed in 6.4.12 (treated like in-stems for upadhā dīrgha)
pUzan = Pratipadika("pUzan", "pum")        # Pūṣan (Vedic deity)
aryaman = Pratipadika("aryaman", "pum")    # Aryaman (Vedic deity)

# han-stems (upapada tatpuruṣa compounds ending in √han "killer")
# SK358 (7.3.54): h→G before ñit/ṇit/n-initial suffixes
# SK359 (8.4.22): n→ṇ when preceded by short a
# vftrahan is built dynamically: [as_purva_pada(vftra), luk_sup, in_compound(han), kvip]
vftra = Pratipadika("vftra", "pum")   # pūrva-pada; ṛ provides ratva cause for SK307

# nah-stems (ending in √nah "bind/tie")
# SK440 (8.2.34): h→D (dh) before jhal or at pada-end.
# Nom/voc sg: upAnaD→t (8.4.56 car at avasāna); inst/dat/abl du/pl: upAnaD+Bh.
upAnah = Pratipadika("upAnah", "pum", other_tags=["nah"])

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
# na_pada needs to be set to preserve mo'no DAtoH
dfnBU = Pratipadika("dfnBU", "pum", other_tags=["DAtu", "BU", "kvip", "na_pada"])
karaBU = Pratipadika("karaBU", "pum", other_tags=["DAtu", "BU", "kvip"])
punarBU = Pratipadika("punarBU", "pum", other_tags=["DAtu", "BU", "kvip"])
svayamBU = Pratipadika("svayamBU", "pum", other_tags=["DAtu", "BU", "kvip"])
suDI = Pratipadika("suDI", "pum", other_tags=["DAtu", "kvip", "pUrvastrI"])
praDI = Pratipadika("praDI", "pum", other_tags=["DAtu", "kvip", "pUrvastrI"])

hAhA = Pratipadika("hAhA", "pum")

rAjan = Pratipadika("rAjan", "pum")
mahat = Pratipadika("mahat", "pum", its=['u'])
# SK425 (6.4.14) test pratipadikas — matup (u-it) stems: upadhā dīrgha before su (nom sg)
dhImat = Pratipadika("DImat", "pum", its=['u'])    # dhīmat (dhī + matup): dhīmān nom sg; SLP1 D=dh, I=ī
gomat  = Pratipadika("gomat", "pum", its=['u'])    # gomat (go + matup): gomān nom sg

# SK427+SK428: śatṛ (ṛ-it = f-it) stems.
# śatṛ suffix is ṛ-it → its=["f"]; SK361 (7.1.70) +f block fires → nUM in sarvanamasthana.
# Jakshi-class (SK428/6.1.6): also tagged other_tags=["Satf","abhyasta"] →
#   SK427 (7.1.78) blocks SK361 nUM → no nUM in strong forms.
# Regular śatṛ (non-abhyasta): tagged other_tags=["Satf"] only → SK361 fires normally.
jakzat   = Pratipadika("jakzat",   "pum", its=["f"], other_tags=["Satf", "abhyasta"])  # SLP1: z=ṣ (जक्षत्)
jAgrat   = Pratipadika("jAgrat",   "pum", its=["f"], other_tags=["Satf", "abhyasta"])
daridrat = Pratipadika("daridrat", "pum", its=["f"], other_tags=["Satf", "abhyasta"])
cakAsat  = Pratipadika("cakAsat",  "pum", its=["f"], other_tags=["Satf", "abhyasta"])
SAsat    = Pratipadika("SAsat",    "pum", its=["f"], other_tags=["Satf", "abhyasta"])
dIDyat   = Pratipadika("dIDyat",   "pum", its=["f"], other_tags=["Satf", "abhyasta"])
vevyat   = Pratipadika("vevyat",   "pum", its=["f"], other_tags=["Satf", "abhyasta"])
# SK444 (7.1.79): neuter abhyasta Satf stem → optional nUM before sarvnāmasthāna (plural only)
# dadat = present participle of reduplicated dā (dadāti); used as neuter kliba.
dadat_napum = Pratipadika("dadat", "napum", its=["f"], other_tags=["Satf", "abhyasta"])
# Regular śatṛ stems — nUM fires (no abhyasta tag, so SK427 does not block SK361)
Bavat   = Pratipadika("Bavat", "pum", its=["f"], other_tags=["Satf"])   # bhū+śatṛ f-it → bhavant strong
Bavat_u = Pratipadika("Bavat", "pum", its=["u"])                       # u-it (no Satf) → SK425 fires → bhāvān nom sg
pacat   = Pratipadika("pacat", "pum", its=["f"], other_tags=["Satf", "Sap"])  # pac+śatṛ → pacant strong; Sap: SK446 mandatory nUM

# SK445/SK446 test stems
# Feminine (strī): NIp is passed separately as a right element (rp: ?NI triggers SK445/446).
# xform numAgama(lc+l) receives lp = "pacat" → inserts nUM → "pacant"; joined with NIp → "pacantI".
pacat_strI  = Pratipadika("pacat",  "strI", its=["f"], other_tags=["Satf", "Sap"])   # SK446 mandatory (class 1 śap)
dIvyat_strI = Pratipadika("dIvyat", "strI", its=["f"], other_tags=["Satf", "Syan"])  # SK446 mandatory (class 4 śyan)
tudat_strI  = Pratipadika("tudat",  "strI", its=["f"], other_tags=["Satf", "Sa"])    # SK445 optional  (class 6 śap)
BAt_strI    = Pratipadika("BAt",    "strI", its=["f"], other_tags=["Satf"])           # SK445 optional  (ā-final root)
# Neuter (napum): dual SI (from 7.1.19 O→SI) gets SK445/446; plural uses SK361 mandatory nUM.
pacat_napum  = Pratipadika("pacat",  "napum", its=["f"], other_tags=["Satf", "Sap"])           # SK446 mandatory dual
dIvyat_napum = Pratipadika("dIvyat", "napum", its=["f"], other_tags=["Satf", "Syan"])          # SK446 mandatory dual
tudat_napum  = Pratipadika("tudat",  "napum", its=["f"], other_tags=["Satf", "Sa"])            # SK445 optional dual

atistri = Pratipadika("atistri", "pum", other_tags=["strI_p", "pUrvastrI"])


# FIXME - remove this, derive from qati

kati = Pratipadika("kati", "pum", other_tags=["qati", "nityabahuvacana"])

# saMKyA
tri = Pratipadika("tri", "pum", other_tags=["saMKyA", "nityabahuvacana"])
dvi = Pratipadika("dvi", "pum", other_tags=["saMKyA", "nityadvivacana",
                                            'tyadAdi'])
catur = Pratipadika("catur", "pum", other_tags=["saMKyA", "nityabahuvacana"])
# n-final ṣaṭ-saṃjñā numerals 5-10 (1.1.26 assigns +zaw automatically via saMKyA+n-final)
paYcan = Pratipadika("paYcan", "pum", other_tags=["saMKyA", "nityabahuvacana"])
saptan = Pratipadika("saptan", "pum", other_tags=["saMKyA", "nityabahuvacana"])
navan  = Pratipadika("navan",  "pum", other_tags=["saMKyA", "nityabahuvacana"])
daSan  = Pratipadika("daSan",  "pum", other_tags=["saMKyA", "nityabahuvacana"])
# aṣṭan (8): tagged "azwan" so SK371/SK372 can target it specifically
azwan  = Pratipadika("azwan",  "pum", other_tags=["saMKyA", "nityabahuvacana", "azwan"])
tri_s = Pratipadika("tri", "strI", other_tags=["saMKyA", "nityabahuvacana"])
#catur_s = Pratipadika("catur", "strI", other_tags=["saMKyA", "nityabahuvacana"])
dvi_s = Pratipadika("dvi", "strI", other_tags=["saMKyA", "nityadvivacana",
                                               'tyadAdi', "Ap"])

# Stri
ap = Pratipadika("ap", "strI", other_tags=["nityabahuvacana", "ap"])  # SK442: ?ap tag for p→t before bhi (7.4.48)
mAtf = Pratipadika("mAtf", "strI", other_tags=["svasrAdi"])
svasf = Pratipadika("svasf", "strI", other_tags=["svasrAdi", "naptrAdi"])
tisf = Pratipadika("tisf", "strI", other_tags=["svasrAdi", "saMKyA",
                                               "nityabahuvacana"])
catasf = Pratipadika("catasf", "strI", other_tags=["svasrAdi", "saMKyA",
                                                   "nityabahuvacana"])
nanAndf = Pratipadika("nanAndf", "strI", other_tags=["svasrAdi"])
duhitf = Pratipadika("duhitf", "strI", other_tags=["svasrAdi"])
yAtf = Pratipadika("yAtf", "strI", other_tags=["svasrAdi"])

BrU = Pratipadika("BrU", "strI", other_tags=["BrU"])
ramA = Pratipadika("ramA", "strI", other_tags=["Ap"])
# SK293 (7.3.115): dvitīyā and tṛtīyā optionally get syāw (like sarvanāma āp) before ṅ-marked suffixes.
# Used as [dvitIya, Ap] / [tftIya, Ap] in test fixtures (same pattern as [sarva, Ap] for sarva_A).
dvitIya = Pratipadika("dvitIya", "pum", other_tags=["dvitIyAdi"])
tftIya  = Pratipadika("tftIya",  "pum", other_tags=["dvitIyAdi"])
nadI = Pratipadika("nadI", "strI", other_tags=["NI"])
niSA = Pratipadika("niSA", "strI", other_tags=["pAdAdi", "Ap"])
nAsikA = Pratipadika("nAsikA", "strI", other_tags=["pAdAdi", "Ap"])
mati = Pratipadika("mati", "strI")
lakzmI = Pratipadika("lakzmI", "strI")  # No NI
strI = Pratipadika("strI", "strI", other_tags=["NI", "strI_p"])
SrI = Pratipadika("SrI", "strI", other_tags=["DAtu", "kvip"])
kumArI =  Pratipadika("kumArI", "strI", other_tags=["NI"])

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
mahat_n = Pratipadika("mahat", "napum", other_tags=["mahat"])
payas = Pratipadika("payas", "napum")   # पयस् n. "water, milk" — SK152 test
yaSas = Pratipadika("yaSas", "napum")  # यशस् n. "fame, glory" — SK152 test
namas = Pratipadika("namas", "napum", other_tags=["avyaya", "gati", "svarAdi"])   # नमस् n. "obeisance" — SK154 (gati by 1.4.74); svarAdi per SK447
puras = Pratipadika("puras", "napum", other_tags=["avyaya", "gati"])   # पुरस् adv. "in front" — SK154 (gati by 1.4.67)

agra = Pratipadika("agra", "napum")  # अग्र n. "front, tip" — SK87/SK88 test
odana = Pratipadika("odana", "napum")  # ओदन n. "rice, food" — SK87/SK88 test
Gfta = Pratipadika("Gfta", "napum")  # घृत n. "clarified butter" (ghee)
Danus  = Pratipadika("Danus",  "napum", other_tags=["AdeSa_s"])
sarpis = Pratipadika("sarpis", "napum", other_tags=["AdeSa_s"])  # ghee (i+s-stem); SK153
yajus  = Pratipadika("yajus",  "napum", other_tags=["AdeSa_s"])  # Veda (u+s-stem); SK153
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
vAh_kvip = Pratipadika("vAh", "pum", other_tags=["DAtu", "kvip"])
sraMs_kvip = Pratipadika("sras", "pum", other_tags=["DAtu", "kvip"])
DvaMs_kvip = Pratipadika("Dvas", "pum", other_tags=["DAtu", "kvip"])
div_kvip = Pratipadika("div", "pum", other_tags=["DAtu", "kvip"])
praSAm_kvip = Pratipadika("praSAm", "pum", other_tags=["DAtu", "kvip"])

anaquh = Pratipadika("anaquh", "pum", other_tags=["anaquh"])
turAsAh = Pratipadika("turAsAh", "pum", other_tags=["DAtu", "kvip", "sah", "Ric"])

# kvin-derived consonant-final stems (SK373 / 3.2.59)
# ?kvin tag triggers SK377 (8.2.62 kvinpratyayasya kuH) at pada-end.
# ?yuj tag (additionally on yuj) triggers SK376 (7.1.71 yujerasamAse) num before sarvanamasthAna.
ftvij_kvin  = Pratipadika("ftvij",   "pum",  other_tags=["DAtu", "kvin"])          # ṛtvij m. (the priest)
sraj_kvin   = Pratipadika("sraj",   "strI", other_tags=["DAtu", "kvin"])          # sraj f. (garland)
yuj_kvin    = Pratipadika("yuj",    "pum",  other_tags=["DAtu", "kvin", "yuj"])        # yuj m. non-compound; ?yuj → SK376 num
yuj_kvin_samAsa = Pratipadika("yuj", "pum",  other_tags=["DAtu", "kvin", "yuj", "samAsa"])  # aśvayuk type: ?samAsa blocks SK376 nUM augment
diS_kvin    = Pratipadika("diS",    "strI", other_tags=["DAtu", "kvin"])          # diś f. (direction)
daDfc_kvin   = Pratipadika("daDfc",   "pum",  other_tags=["DAtu", "kvin"])           # dadhṛc m. (bold one); c→j(8.2.39)→g(8.2.62)→k(8.4.56)

# r/v-final kvip stems — SK433 (8.2.76) upadhā-dīrgha at pada-end; SK354 (8.2.77) before hal
gir_kvip     = Pratipadika("gir",     "pum",  other_tags=["DAtu", "kvip"])           # √gṝ+kvip; nom sg gīḥ
pur_kvip     = Pratipadika("pur",     "pum",  other_tags=["DAtu", "kvip"])           # √pū+kvip; nom sg pūḥ


# Generic prefix pratipadikas — reusable with many Dhatus (not tied to añcatir specifically)
# 6.1.77 fires at (prati|ac) → pratyac; 6.1.101 fires at (pra|ac) → prAc
prati = Pratipadika("prati", "pum", other_tags=["nipAta"])
pra   = Pratipadika("pra",   "pum", other_tags=["nipAta"])
tiras = Pratipadika("tiras", "pum", other_tags=["nipAta", "tiras", "svarAdi"])  # svarAdi per SK447
ud    = Pratipadika("ud",    "pum", other_tags=["nipAta"])
sam   = Pratipadika("sam",   "pum", other_tags=["nipAta", "sam"])
saha  = Pratipadika("saha",  "pum", other_tags=["nipAta", "saha"])
nis  = Pratipadika("nis",  "napum", other_tags=["nipAta", "nis"])
dus  = Pratipadika("dus",  "napum", other_tags=["nipAta", "dus"])
bahis  = Pratipadika("bahis",  "napum", other_tags=["nipAta", "tiras"])

# SK160 (8.3.46) — a-final samāsa pūrva + {kāra/kāma/kaṃsa/kumbha/pātra/kuśā/karṇī}
# Bare pratipadikas used by samāsa vibhakti fixture (item 5); tag propagates to _pada via join_objects.
ayas  = Pratipadika("ayas",  "napum")                                           # test pūrva (iron/metal)
kAra  = Pratipadika("kAra",  "pum",   other_tags=["satva_kfkamkaMsAdi"])        # placeholder for √kṛ-form
kAma  = Pratipadika("kAma",  "pum",   other_tags=["satva_kfkamkaMsAdi"])        # placeholder for √kam-form
kaMsa = Pratipadika("kaMsa", "pum",   other_tags=["satva_kfkamkaMsAdi"])
kumBa = Pratipadika("kumBa", "pum",   other_tags=["satva_kfkamkaMsAdi"])
pAtra = Pratipadika("pAtra", "napum", other_tags=["satva_kfkamkaMsAdi"])
kuSA  = Pratipadika("kuSA",  "strI",  other_tags=["satva_kfkamkaMsAdi", "Ap"])
karRI = Pratipadika("karRI", "strI",  other_tags=["satva_kfkamkaMsAdi", "NI"])


# SK161 (8.3.47) — aDas/Siras samāsa pūrva before any viBakti form of pada
aDas  = Pratipadika("aDas",  "pum",   other_tags=["avyaya"])
Siras = Pratipadika("Siras", "napum")
pada  = Pratipadika("pada",  "napum", other_tags=["pada_p"])                    # tag propagates to pada_p_pada

# SK430 (6.3.91) — dṛkṣa stem: दृश् + क्स affix (क् is it, स् remains → क्ष)
# dfS and ksa tags propagate to dfS_pada + ksa_pada on the merged compound form
dfkza = Pratipadika("dfkza", "pum", other_tags=["dfS", "ksa"])

# # SK418 (6.3.92) prātipadikas — viṣvag and deva use specific tags; pronouns use sarvanAma_pada
vizvag = Pratipadika("vizvag", "pum", other_tags=["vizvag"])
deva   = Pratipadika("deva",   "pum", other_tags=["deva"])

# añcatir pre-formed weak stems (used when SK416/417 should NOT fire)
# NO ?DAtu — SK416 requires ?DAtu; its absence blocks SK416/417.
tiryac_kvin = Pratipadika("tiryac", "pum", other_tags=["aYc", "kvin"])
# tiryac = tiras+ac; SK423 (tiry ādeśa when SK416 hasn't run) deferred.
# Bha form tiryacā is correct (SK416/417 don't apply).

udac_kvin   = Pratipadika("udac",   "pum", other_tags=["aYc", "kvin", "udanc"])
# ?udanc → SK420 (6.4.139) fires in bha context (apavāda of SK416).
# SK416 blocked: no ?DAtu and ?udanc guard. SK420 fires → udīcā.

takz_kvip    = Pratipadika("takz",    "pum",  other_tags=["DAtu", "kvip"])          # √takṣ+kvip; nom sg taṭ/taḍ via 8.2.29 k-deletion
naS_kvip     = Pratipadika("naS",     "pum",  other_tags=["DAtu", "kvip", "naS"])   # √naś+kvip; optional kutva 8.2.63

kim = Pratipadika("kim", "pum", other_tags=["kim", "sarvanAma"])
idam = Pratipadika("idam", "pum", other_tags=["idam", "sarvanAma", "tyadAdi"])
idam_strI = Pratipadika("idam", "strI", other_tags=["idam", "sarvanAma", "tyadAdi"])
idam_anu = Pratipadika("idam", "pum", other_tags=["idam", "sarvanAma", "tyadAdi", "anvAdeSa"])

# tyadādi demonstratives (SK381 / 7.2.106): non-final t/d → s before su (nom sg)
# Feminines of tad/etad/yad/kim are formed in tests as [stem, strI_abs] —
# SK441 commentary ("त्यदाद्यत्वं टाप्"): 7.2.102/103 fires first, then SK454 TAp.
tad  = Pratipadika("tad",  "pum", other_tags=["tad",  "sarvanAma", "tyadAdi"])  # "that"
etad = Pratipadika("etad", "pum", other_tags=["etad", "sarvanAma", "tyadAdi"])  # "this (near)"
yad  = Pratipadika("yad",  "pum", other_tags=["yad",  "sarvanAma", "tyadAdi"])  # "which/who" (relative)
tyad = Pratipadika("tyad", "pum", other_tags=["tyad", "sarvanAma", "tyadAdi"])  # "that (yonder)"
adas = Pratipadika("adas", "pum", other_tags=["adas", "sarvanAma", "tyadAdi"])  # "that (far)"

# Personal pronouns — alinga (no gender distinction)
# SK382-395 (7.1.28, 7.2.86-97): nominative sg forms tvam/aham via SK383-385
yuzmad = Pratipadika("yuzmad", "pum", other_tags=["yuzmad", "sarvanAma"])  # yuṣmad "you"
asmad  = Pratipadika("asmad",  "pum", other_tags=["asmad",  "sarvanAma"])  # asmad "I/we"

rAjan = Pratipadika("rAjan", "pum", other_tags=["rAjan"])
parvan_napum = Pratipadika("parvan", "napum")

# SK459 (4.1.11 मनः): man-final stem; ṅīp blocked → halanta feminine सीमा.
sIman = Pratipadika("sIman", "strI")
# SK460/SK461: prebuilt an-final bahuvrīhi. ?van so SK456 (4.1.7) is a live competitor
# that SK460/SK461 must override; ?samasta_pada marks the completed compound.
bahuyajvan = Pratipadika("bahuyajvan", "pum",
                         other_tags=["bahuvrIhi", "samasta_pada", "van"])

# SK443 (8.2.68 ahan n→ru at pada-end): apavāda of 8.2.7 (n-lopa).
# Nom/acc/voc sg: ahan → n→r (ru) → visarga → ahaḥ.
# Bha forms (vowel-initial non-sarvānāmasthāna): existing 6.4.134 a-lopa → ahn-.
# Consonant-initial (bhyAm etc.): ru+voiced → 6.1.114 r-drops, u inserted → aho-.
ahan = Pratipadika("ahan", "napum", other_tags=["ahan"])
yajvan = Pratipadika("yajvan", "pum", other_tags=["yajvan"])

# SvanType: Svan, yuvan, maGavan — -an stems with samprasāraṇa in bha position (SK362 / 6.4.133)
# NOTE: SvanType does NOT propagate through taddhita derivation (paninian_object.py join_objects
# allowlist omits it), so the sutra's "ataddhite" restriction is naturally satisfied —
# śauvana- etc. taddhita derivatives will not carry SvanType and SK362 will not misfire.
svan = Pratipadika("Svan", "pum", other_tags=["SvanType"])
yuvan = Pratipadika("yuvan", "pum", other_tags=["SvanType"])
maGavan = Pratipadika("maGavan", "pum", other_tags=["SvanType", "maGavan"])

# SK364 (6.4.127): arvan — mandatory tṛ-substitute before all suffixes except su.
arvan = Pratipadika("arvan", "pum", other_tags=["arvan"])

# Iyasun (comparative suffix) is u-it → ugit → SK361 nUM fires before sarvanamasthāna.
# pum: its=['u'] → SK361 (7.1.70) fires for all sarvanamasthāna (nom sg śreyān, etc.)
# napum: its=['u'] — ugit; but 7.1.72 (नपुंसकस्य झलचः) overrides 7.1.70 for napum stems,
#   so only 7.1.72 fires for napum pl nUM (no double nUM). See overrides: 7.1.70 in sutras_antaranga.yaml.
Sreyas   = Pratipadika("Sreyas", "pum",   its=['u'], other_tags=["Iyasun"])
Sreyas_n = Pratipadika("Sreyas", "napum", its=['u'], other_tags=["Iyasun"])

# SK435 (6.4.131 vasoḥ samprasāraṇam): kvasu/vas suffix stems — v→u in bha position.
# SK334 (8.2.72): s→d at pada-end before non-sarvānāmasthāna (consonant-initial suffixes).
# SK425 (6.4.14): u-it, ll=a, l=s → upadhā-dīrgha before su (nom sg) → vidvAs.
# its=['u']: u-it → SK361 (7.1.70) nUM fires before sarvānāmasthāna → vidvāṃs strong forms.
# ?vasanta: triggers SK435 in bha position.
# ?vasu: triggers SK334 (8.2.72) s→d at pada-end (consonant-initial non-sarvānāmasthāna).
vidvas = Pratipadika("vidvas", "pum", its=["u"], other_tags=["vasu", "vasanta"])

# SK436 (7.1.89 puṃso'suṅ): before sarvānāmasthāna, the s of puṃs → as (asun suffix, u-it).
# its=['u']: u-it → SK361 nUM fires → pumāṃs strong forms.
# ?pums: triggers SK436 condition.
# SK425 (6.4.14): u-it, ll=a, l=s → upadhā-dīrgha before su → pumAs; SK361 → pumAns → pumān.
pums = Pratipadika("pums", "pum", its=["u"], other_tags=["pums"])

# Compound test pratipadikas (pūrva-pada candidates — used with in_compound() on the uttara-pada)
gaRa        = Pratipadika("gaRa", "pum")                            # gaṇa m. — pūrva-pada for gaṇapati (SK257)
aSva        = Pratipadika("aSva", "pum")                            # aśva m. — pūrva-pada for aśvayuj (SK376)

vizRu      = Pratipadika("vizRu", "pum")              # viṣṇu m. (u-stem) — test target for SK176

# SK379 (6.3.128) pratipadikas — viśva's final a lengthens before vasu/rāṭ in compound
viSva       = Pratipadika("viSva", "pum", other_tags=["viSva"])     # viśva — ?viSva tag triggers 6.3.128
vasu_pum    = Pratipadika("vasu", "pum", other_tags=["vasupada"])   # vasu m. (u-stem) — uttara-pada (?vasupada avoids collision with 8.2.72's ?vasu)
rAj_kvip    = Pratipadika("rAj", "pum", other_tags=["DAtu", "kvip", "rAj", "vraScAdi"])  # √rāj+kvip; nom sg: rāṭ via SK294(j→ṣ)+8.2.39(ṣ→ḍ)+8.4.56(ḍ→ṭ)

# SK414 (6.4.130) test pratipadikas — pādaḥ pat
su_purva    = Pratipadika("su", "pum")                                                    # su — pūrva-pada for supAd compound
pAd_ut      = Pratipadika("pAd", "pum")                                                    # pāda in compound form (terminal a dropped); SK414 shortens pAd→pad when bha

# SK307 (8.4.12) test pratipadikas — एकाजुत्तरपदे णः

# Component pratipadikas for dynamic compound test: Sūrpa (m.) + naKī (f.)
# The compound SūrpanaKī should NOT get Ratva because it is a samasta (compound).
SUrpa = Pratipadika("SUrpa", "pum")   # śūrpa (winnowing basket), m. a-stem
naKI  = Pratipadika("naKI",  "strI", other_tags=["NI"])  # naḳī (basket-maker's wife), f. ī-stem

# Positive test: kṣīra (milk) + monosyllabic uttara-pada with n → ṇatva via SK307
kzIra = Pratipadika("kzIra", "napum")  # kṣīra (milk), neuter a-stem
pa = Pratipadika("pa", "napum", other_tags=["samAsa"])  # monosyllabic uttara-pada (pā = hand)

# ── ajādi gaṇa (SK454 / 4.1.4) — all 34 members ──────────────────────────────────────
# Items 1–27, 31–34 end in short 'a' → TAp via l:at (ajAdi tag redundant but correct).
# Items 28–30 end in consonants → TAp via ?ajAdi condition specifically.
# Source: Vasu commentary on 4.1.4.
aja           = Pratipadika("aja",           "pum", other_tags=["ajAdi"])  #  1 अज   (he-goat)
eqaka         = Pratipadika("eqaka",         "pum", other_tags=["ajAdi"])  #  2 एडक  (sheep)
kokila        = Pratipadika("kokila",        "pum", other_tags=["ajAdi"])  #  3 कोकिल (cuckoo)
cawaka        = Pratipadika("cawaka",        "pum", other_tags=["ajAdi"])  #  4 चटक  (sparrow)
aSva          = Pratipadika("aSva",          "pum", other_tags=["ajAdi"])  #  5 अश्व  (horse)
mUzika        = Pratipadika("mUzika",        "pum", other_tags=["ajAdi"])  #  6 मूषिक (mouse)
bAla          = Pratipadika("bAla",          "pum", other_tags=["ajAdi"])  #  7 बाल  (young/child)
hoqa          = Pratipadika("hoqa",          "pum", other_tags=["ajAdi"])  #  8 होड  (young)
pAka          = Pratipadika("pAka",          "pum", other_tags=["ajAdi"])  #  9 पाक  (young)
vatsa         = Pratipadika("vatsa",         "pum", other_tags=["ajAdi"])  # 10 वत्स (calf)
manda         = Pratipadika("manda",         "pum", other_tags=["ajAdi"])  # 11 मन्द (slow)
vilAta        = Pratipadika("vilAta",        "pum", other_tags=["ajAdi"])  # 12 विलात (foreigner)
pUrvApaharaRa = Pratipadika("pUrvApaharaRa","pum", other_tags=["ajAdi"])  # 13 पूर्वापहरण (lyuT compound)
aparApaharaRa = Pratipadika("aparApaharaRa","pum", other_tags=["ajAdi"])  # 14 अपरापहरण  (lyuT compound)
saMPala       = Pratipadika("saMPala",       "pum", other_tags=["ajAdi"])  # 15 संफल
BastraPala    = Pratipadika("BastraPala",    "pum", other_tags=["ajAdi"])  # 16 भस्त्रफल
ajinaPala     = Pratipadika("ajinaPala",     "pum", other_tags=["ajAdi"])  # 17 अजिनफल
SaRaPala      = Pratipadika("SaRaPala",      "pum", other_tags=["ajAdi"])  # 18 शणफल
piRqaPala     = Pratipadika("piRqaPala",     "pum", other_tags=["ajAdi"])  # 19 पिण्डफल
triPala       = Pratipadika("triPala",       "pum", other_tags=["ajAdi"])  # 20 त्रिफल
satpuzpa      = Pratipadika("satpuzpa",      "pum", other_tags=["ajAdi"])  # 21 सत्पुष्प
prAkpuzpa     = Pratipadika("prAkpuzpa",    "pum", other_tags=["ajAdi"])  # 22 प्राक्पुष्प
kARqapuzpa    = Pratipadika("kARqapuzpa",   "pum", other_tags=["ajAdi"])  # 23 काण्डपुष्प
prAntapuzpa   = Pratipadika("prAntapuzpa",  "pum", other_tags=["ajAdi"])  # 24 प्रान्तपुष्प
Satapuzpa     = Pratipadika("Satapuzpa",    "pum", other_tags=["ajAdi"])  # 25 शतपुष्प
ekapuzpa      = Pratipadika("ekapuzpa",     "pum", other_tags=["ajAdi"])  # 26 एकपुष्प
SUdra         = Pratipadika("SUdra",        "pum", other_tags=["ajAdi"])  # 27 शूद्र
kruYc         = Pratipadika("kruYc",        "pum", other_tags=["ajAdi"])  # 28 क्रुञ्च् (consonant-final)
uzRih         = Pratipadika("uzRih",        "pum", other_tags=["ajAdi"])  # 29 उष्णिह् (consonant-final)
devaviS       = Pratipadika("devaviS",      "pum", other_tags=["ajAdi"])  # 30 देवविश् (consonant-final; iS = i+ś)
jyezWa        = Pratipadika("jyezWa",       "pum", other_tags=["ajAdi"])  # 31 ज्येष्ठ (eldest)
kanizWa       = Pratipadika("kanizWa",      "pum", other_tags=["ajAdi"])  # 32 कनिष्ठ (youngest)
maDyama       = Pratipadika("maDyama",      "pum", other_tags=["ajAdi"])  # 33 मध्यम (middle)
amUla         = Pratipadika("amUla",        "pum", other_tags=["ajAdi"])  # 34 अमूल  (nan+mūla)
# ──────────────────────────────────────────────────────────────────────────────────────
