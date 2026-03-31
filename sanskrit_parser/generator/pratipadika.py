import copy
from indic_transliteration import sanscript
from sanskrit_parser.generator.paninian_object import PaninianObject


class Pratipadika(PaninianObject):
    """ Sanskrit Object Class: Derived From SanskritString

     Attributes:
    """
    def __init__(self, thing=None, linga="pum",
                 its=[], other_tags=[], encoding=sanscript.SLP1,
                 unicode_encoding='utf-8',
                 strict_io=True, replace_ending_visarga='s'):
        super().__init__(thing, encoding, unicode_encoding, strict_io, replace_ending_visarga, its=its)
        self.linga = linga
        self.inPrakriya = True
        self.setTag("prAtipadika")
        self.setTag(linga)
        # self.setTag("aNga")
        for t in other_tags:
            self.setTag(t)

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
vftrahan = Pratipadika("vftrahan", "pum", other_tags=["han"])

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
# Regular śatṛ stems — nUM fires (no abhyasta tag, so SK427 does not block SK361)
Bavat   = Pratipadika("Bavat", "pum", its=["f"], other_tags=["Satf"])   # bhū+śatṛ f-it → bhavant strong
Bavat_u = Pratipadika("Bavat", "pum", its=["u"])                       # u-it (no Satf) → SK425 fires → bhāvān nom sg
pacat   = Pratipadika("pacat", "pum", its=["f"], other_tags=["Satf"])  # pac+śatṛ → pacant strong

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
payas = Pratipadika("payas", "napum")
Danus = Pratipadika("Danus", "napum", other_tags=["AdeSa_s"])
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


# Generic prefix pratipadikas — reusable with many Dhatus (not tied to añcatir specifically)
# 6.1.77 fires at (prati|ac) → pratyac; 6.1.101 fires at (pra|ac) → prAc
#prati = Pratipadika("prati", "pum")
#pra   = Pratipadika("pra",   "pum")
#tiras = Pratipadika("tiras", "pum")   # for future SK423 (tiras+ac → tiryac)
#ud = Pratipadika("ud", "pum")   


#Pada versions of above - will be removed later
# FIXME - remove when we implement SK452/2.4.82
prati_pada = Pratipadika("prati", "pum", other_tags=["nipAta", "upasarga", "pada"])
pra_pada   = Pratipadika("pra",   "pum", other_tags=["nipAta", "upasarga", "pada"])
tiras_pada = Pratipadika("tiras", "pum", other_tags=["tiras", "nipAta", "upasarga", "pada"])
ud_pada    = Pratipadika("ud",    "pum", other_tags=["nipAta", "upasarga", "pada"])
sam_pada   = Pratipadika("sam",   "pum", other_tags=["sam",  "nipAta", "upasarga", "pada"])
saha_pada  = Pratipadika("saha",  "pum", other_tags=["saha", "nipAta", "upasarga", "pada"])
# SK418 (6.3.92) prātipadikas — viṣvag and deva use specific tags; pronouns use sarvanAma_pada
vizvag_pada = Pratipadika("vizvag", "pum", other_tags=["vizvag", "pada"])
deva_pada   = Pratipadika("deva",   "pum", other_tags=["deva",   "pada"])
tad_pada    = Pratipadika("tad",    "pum", other_tags=["tad",    "sarvanAma", "sarvanAma_pada", "pada"])
yad_pada    = Pratipadika("yad",    "pum", other_tags=["yad",    "sarvanAma", "sarvanAma_pada", "pada"])
kim_pada    = Pratipadika("kim",    "pum", other_tags=["kim",    "sarvanAma", "sarvanAma_pada", "pada"])
                         


# añcatir pre-formed weak stems (used when SK416/417 should NOT fire)
# NO ?DAtu — SK416 requires ?DAtu; its absence blocks SK416/417.
tiryac_kvin = Pratipadika("tiryac", "pum", other_tags=["aYc", "kvin"])
# tiryac = tiras+ac; SK423 (tiry ādeśa when SK416 hasn't run) deferred.
# Bha form tiryacā is correct (SK416/417 don't apply).

udac_kvin   = Pratipadika("udac",   "pum", other_tags=["aYc", "kvin", "udanc"])
# ?udanc → SK420 (6.4.139) fires in bha context (apavāda of SK416).
# SK416 blocked: no ?DAtu and ?udanc guard. SK420 fires → udīcā.

takz_kvip    = Pratipadika("takz",    "pum",  other_tags=["DAtu", "kvip"])          # √takṣ+kvip; nom sg taṭ/taḍ via 8.2.29 k-deletion

kim = Pratipadika("kim", "pum", other_tags=["kim", "sarvanAma"])
idam = Pratipadika("idam", "pum", other_tags=["idam", "sarvanAma", "tyadAdi"])
idam_strI = Pratipadika("idam", "strI", other_tags=["idam", "sarvanAma", "tyadAdi"])
idam_anu = Pratipadika("idam", "pum", other_tags=["idam", "sarvanAma", "tyadAdi", "anvAdeSa"])

# tyadādi demonstratives (SK381 / 7.2.106): non-final t/d → s before su (nom sg)
tad  = Pratipadika("tad",  "pum", other_tags=["tad",  "sarvanAma", "tyadAdi"])  # "that"
etad = Pratipadika("etad", "pum", other_tags=["etad", "sarvanAma", "tyadAdi"])  # "this (near)"
tyad = Pratipadika("tyad", "pum", other_tags=["tyad", "sarvanAma", "tyadAdi"])  # "that (yonder)"
adas = Pratipadika("adas", "pum", other_tags=["adas", "sarvanAma", "tyadAdi"])  # "that (far)"

# Personal pronouns — alinga (no gender distinction)
# SK382-395 (7.1.28, 7.2.86-97): nominative sg forms tvam/aham via SK383-385
yuzmad = Pratipadika("yuzmad", "pum", other_tags=["yuzmad", "sarvanAma"])  # yuṣmad "you"
asmad  = Pratipadika("asmad",  "pum", other_tags=["asmad",  "sarvanAma"])  # asmad "I/we"

rAjan = Pratipadika("rAjan", "pum", other_tags=["rAjan"])
parvan_napum = Pratipadika("parvan", "napum")

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

# SK379 (6.3.128) pratipadikas — viśva's final a lengthens before vasu/rāṭ in compound
viSva       = Pratipadika("viSva", "pum", other_tags=["viSva"])     # viśva — ?viSva tag triggers 6.3.128
vasu_pum    = Pratipadika("vasu", "pum", other_tags=["vasupada"])   # vasu m. (u-stem) — uttara-pada (?vasupada avoids collision with 8.2.72's ?vasu)
rAj_kvip    = Pratipadika("rAj", "pum", other_tags=["DAtu", "kvip", "rAj", "vraScAdi"])  # √rāj+kvip; nom sg: rāṭ via SK294(j→ṣ)+8.2.39(ṣ→ḍ)+8.4.56(ḍ→ṭ)

# SK414 (6.4.130) test pratipadikas — pādaḥ pat
su_purva    = Pratipadika("su", "pum")                                                    # su — pūrva-pada for supAd compound
pAd_ut      = Pratipadika("pAd", "pum")                                                    # pāda in compound form (terminal a dropped); SK414 shortens pAd→pad when bha
