from indic_transliteration import sanscript
from sanskrit_parser.generator.paninian_object import PaninianObject


class Pratyaya(PaninianObject):
    """ Sanskrit Object Class: Derived From SanskritString

     Attributes:
    """
    def __init__(self, thing=None, its=None, other_tags=None, encoding=sanscript.SLP1,
                 unicode_encoding='utf-8',
                 strict_io=True, replace_ending_visarga='s'):
        super().__init__(thing, encoding, unicode_encoding, strict_io, replace_ending_visarga, its=its)
        self.inPrakriya = True
        self.setTag("pratyaya")
        for t in (other_tags if other_tags is not None else []):
            self.setTag(t)

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
AN_upasarga = Pratyaya("A", its=["N"], other_tags=["nipAta", "upasarga", "pada"])
mAN_upasarga = Pratyaya("mA", its=["N"], other_tags=["nipAta", "upasarga", "pada"])
upa_upasarga = Pratyaya("upa", other_tags=["nipAta", "upasarga", "pada"])
pra_upasarga = Pratyaya("pra", other_tags=["nipAta", "upasarga", "pada"])
ava_upasarga = Pratyaya("ava", other_tags=["nipAta", "upasarga", "pada"])
ud_upasarga = Pratyaya("ud", other_tags=["nipAta", "upasarga", "pada"])
ati_upasarga = Pratyaya("ati", other_tags=["nipAta", "upasarga", "pada"])


# bha when applied to prAtipadikas only!
# FIXME - maybe have two yats?
# tadDita_ya: shared tag on the taddhita affixes whose content is "ya" (yat/ṣyañ/yañ).
# SK472 (6.4.150 हलस्तद्धितस्य) elides only this taddhita ya-kāra before ṅīp ī — NOT a
# base-internal 'y' (e.g. विद्या+अण् → वैद्य, where the ya is from the base, gives वैद्यी).
yat_t = Pratyaya("ya", its=["t"], other_tags=["svAdi", "tadDita", "tadDita_ya"])
zyaY_t = Pratyaya("ya", its=["z", "Y"], other_tags=["svAdi", "tadDita", "tadDita_ya"])
# yaY_t (yañ): SK471 (4.1.16 यञश्च) → ṅīp (needs the yañ-specific ?yaY tag); SK472
# elides its ya via ?tadDita_ya. Both tags propagate to the merged stem.
yaY_t = Pratyaya("ya", its=["Y"], other_tags=["svAdi", "tadDita", "yaY", "tadDita_ya"])
# aR_t (aṇ): one of the SK470 (4.1.15) ṅīp-triggering taddhita affixes.
aR_t = Pratyaya("a", its=["R"], other_tags=["svAdi", "tadDita", "NIp_taddhita"])

# SK470 (4.1.15 टिड्ढाणञ्द्वयसज्दघ्नञ्मात्रच्तयप्ठक्ठञ्कञ्क्वरपः): a-final stems ending in
# these taddhita affixes take ṅīp (apavāda to 4.1.4 ṭāp). Shared tag NIp_taddhita
# drives one SK470 condition block; ādivṛddhi (7.2.117) fires for the +R/+Y ones.
# (aṇ = aR_t above; kañ = kaY below, reused from SK429; ṭiṭ-class = +w it-marker.)
aY_t     = Pratyaya("a",       its=["Y"],     other_tags=["svAdi", "tadDita", "NIp_taddhita"])  # añ
dvayasac = Pratyaya("dvayasa", its=["c"],     other_tags=["svAdi", "tadDita", "NIp_taddhita"])  # द्वयसच्
daGnac   = Pratyaya("daGna",   its=["c"],     other_tags=["svAdi", "tadDita", "NIp_taddhita"])  # दघ्नच्
mAtrac   = Pratyaya("mAtra",   its=["c"],     other_tags=["svAdi", "tadDita", "NIp_taddhita"])  # मात्रच्
tayap    = Pratyaya("taya",    its=["p"],     other_tags=["svAdi", "tadDita", "NIp_taddhita"])  # तयप्
Wak      = Pratyaya("Wa",      its=["k"],     other_tags=["svAdi", "tadDita", "NIp_taddhita"])  # ठक् → इक (SK1170)
WaY      = Pratyaya("Wa",      its=["Y"],     other_tags=["svAdi", "tadDita", "NIp_taddhita"])  # ठञ् → इक + ādivṛddhi
kvarap   = Pratyaya("vara",    its=["k", "p"], other_tags=["svAdi", "tadDita", "NIp_taddhita"])  # क्वरप् (kit → no guṇa)
Qhak     = Pratyaya("Q",       its=["k"],     other_tags=["svAdi", "tadDita", "NIp_taddhita"])  # ढक्: ढ → एय् (SK475 partial)

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
        [Ni, os2, sup],
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
# Handled in rule - commenting out
#SI = Pratyaya("I", its=["S"], other_tags=["svAdi", "sup", "SI"])

# Si - jasSasaH Si
Si = Pratyaya("i", its=["S"], other_tags=["svAdi", "sup", "Si", "viBakti",
                                          "praTamA",
                                          "sarvanAmasTAna"])

OS = Pratyaya("O", other_tags=["sup"])


# adaq - for qatarAdi - 
adaq = Pratyaya("ad", its=["q"], other_tags=["svAdi", "sup", "adaq"])

# StrI
NIp = Pratyaya("I", its=["N", "p"], other_tags=["svAdi", "NI", "strI"])
NIz = Pratyaya("I", its=["N", "z"], other_tags=["svAdi", "NI", "strI"])
Ap = Pratyaya("A", its=["p"], other_tags=["svAdi", "Ap", "strI"])
# DAp — डाप् (4.1.13): optional feminine affix after man-final / an-bahuvrīhi stems.
# q-it (ḍit) triggers ṭi-lopa via 6.4.143 टेः; "Ap" tag → ramā-type ā-stem declension.
DAp = Pratyaya("A", its=["q", "p"], other_tags=["svAdi", "Ap", "DAp", "strI"])
strI_abs = Pratyaya("", its=[], other_tags=["strI_abs", "strI"])

# Sup Luk
luk_sup = Pratyaya("", its=[], other_tags=["sup"])
luk = Pratyaya("", its=[], other_tags=[""])

# Sambuddhi
sambudDi = PaninianObject("")
sambudDi.setTag("sambudDi")

# Pum / Napum
pum_abs = Pratyaya("", its=[], other_tags=["pum_abs", "pum"])
napum_abs = Pratyaya("", its=[], other_tags=["napum_abs", "napum"])

# kvip
kvip = Pratyaya("", its=["k", "p"], other_tags=["kvip", "krt"])

# kvin — kit krt suffix (phonologically zero); aYc + kvin → SK415 drops Y → ac
# its=['k'] → kit; "krt" → join_objects produces ?prAtipadika; "kvin" → SK377 (8.2.62 ku)
# NOTE: no "aYc" tag here — kvin is generic; aYc propagates from the Dhatu via join_objects
kvin = Pratyaya("", its=['k'], other_tags=["kvin", "krt"])

# kaY — creates vowel-final stems from tyadAdi + dṛś (SK429)
# kaY (कञ्): kṛt used by SK429 (tādṛśa/yādṛśa); also one of the SK470 (4.1.15)
# ṅīp-triggering affixes → NIp_taddhita gives yādṛśī etc.
kaY = Pratyaya("a", its=["k", "Y"], other_tags=["kaY", "krt", "NIp_taddhita"])

# vatup — वतुप् affix (5.2.39): after yad/tad/etad for "measure of volume"
# u, p are it markers; content is "vat" (वत्). krt → join_objects produces prAtipadika.
vatup = Pratyaya("vat", its=["u", "p"], other_tags=["vatup", "krt"])

# van-class kṛt suffixes (3.2.74 vanip, 3.2.103 ṅvanip; kvanip is also van-class).
# All three carry "van" so SK456 (4.1.7 वनो र च) can fire on lp: ?van + rp: ?strI_abs.
# ArDaDAtuka enables SK2168 (7.3.84) guṇa for ig-anta dhātus (e.g. SF + vanip → Sar+van).
# 1.1.5 (k(N)iti ca) blocks guṇa for kvanip (kit) and Dvanip (ṅit); vanip (only p-it)
# admits guṇa. "van" tag is propagated to the merged stem by paninian_object.join_objects.
vanip  = Pratyaya("van", its=["p"],       other_tags=["van", "krt", "ArDaDAtuka"])
kvanip = Pratyaya("van", its=["k", "p"],  other_tags=["van", "krt", "ArDaDAtuka"])
Dvanip = Pratyaya("van", its=["N", "p"],  other_tags=["van", "krt", "ArDaDAtuka"])

# UW
UW = Pratyaya("U", its=["W"], other_tags=["samprasAraRam","UW"])


# wac - for rAjan, ahan and saKi in samAsa
# wac (टच्): samāsānta affix. Tagged tadDita (समासान्त affixes are taddhita) so the
# krt/tadDita-gated setIt loop in join_objects propagates its ṭ-it (w) to the merged
# stem — enabling SK470's ṭiṭ (+w) arm (kurucarī etc.).
wac = Pratyaya("a", its=["w", "c"], other_tags=["svAdi", "tadDita", "wac", "pum"])



#
kanin = Pratyaya("an", its=["k", "i", "n"], other_tags=["kanin"])

# anIYa
anIya= Pratyaya("anIya", its=[], other_tags=["kft", "anIYa"])


# Taddhita pratyayas for SK152/SK153 (8.3.38-39): visarjanīya sandhi before ku/pu
# pāśap, kalpap, kap, kāmyac — share tag "satva_t" used as condition in YAML
pASap  = Pratyaya("pASa",  its=["p"], other_tags=["svAdi", "tadDita", "satva_t"])
kalpap = Pratyaya("kalpa", its=["p"], other_tags=["svAdi", "tadDita", "satva_t"])
kap  = Pratyaya("ka",     its=["p"], other_tags=["svAdi", "tadDita", "satva_t", "ka_pratyaya"])
# kan (5.3.75 saMjJAyAm kan; 5.3.87 etc.) — ka with anubandha n. SK463 (7.3.44)
# idādeśa applies before Ap on ?ka_pratyaya stems (sarva+kan → sarvika+Ap).
kan  = Pratyaya("ka",     its=["n"], other_tags=["svAdi", "tadDita", "ka_pratyaya"])
kAmyac = Pratyaya("kAmya", its=["c"], other_tags=["svAdi", "tadDita", "satva_t"])


# suc - SK2086
suc =  Pratyaya("s", its=["c", "u"], other_tags=["svAdi", "tadDita", "suc"])


# Adya / Anta
avasAna = PaninianObject(".")
avasAna.setTag("avasAna")

Adya = PaninianObject("")
Adya.setTag("Adya")
