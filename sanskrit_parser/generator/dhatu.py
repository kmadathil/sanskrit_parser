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
        # Auto-tag monosyllabic dhātus (ekāc) so SK307 and downstream rules can
        # detect a monosyllabic uttara-pada when the dhātu takes a krit suffix.
        _vowels = set("aAiIuUfFxXeEoO")
        if sum(1 for ch in self.canonical() if ch in _vowels) == 1:
            self.setTag("ekac")


iR = Dhatu("i", its=["R"], other_tags=["eti"])
naS = Dhatu("naS")   # √naś "to perish"; SK470 kvarap test: naś+kvarap → नश्वर → नश्वरी
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
han = Dhatu("han", its=[], other_tags=["han"])   # √han "to kill"; ?han → SK359 (8.4.22)
spfS = Dhatu("spfS", its=[], other_tags=["spfS"])  # √spṛś "to touch" (SLP1: spfS = स्पृश्)
vah = Dhatu("vah", its=[])
Sam = Dhatu("Sam", its=[])
Sf = Dhatu("Sf", its=[])   # √śṛ "to break/destroy"; ig-anta — SK2168 guṇa fires before vanip

# FIXME: temporary for testing, samprasarana version of veY. Remove later
veY_smp = Dhatu("u", its=["Y"])

aYc_u = Dhatu("aYc", its=['u'])     # √añc with u-it; anidita → SK415 applies; ?aYc → SK361 nUM


# ── Kāraka layer (karaka_plan.md §2/§6) ──────────────────────────────────────
# Verb meaning-class tags (gatyarTa, rucyarTa, SabdakarmA, akarmaka, …) ride on
# Dhatu(..., other_tags=[...]) as the kāraka phases K1/K4 introduce them; the
# kāraka pre-pass reads them from the sentence dhātu via rp.

def tinanta_pada(form, prayoga, meaning_tags=()):
    """Pre-formed tiṅanta pada (karaka_plan.md §6): surface form + prayoga
    (kartari/karmaRi/BAve) + dhātu meaning-class tags. Until tiṅanta
    derivation exists, the verb enters a sentence as this finished pada; the
    kāraka pre-pass reads only its tags (?tiNanta also stubs the sup-insertion
    tiṅ branch), so real tiṅanta derivation can replace it later without
    touching the rule set."""
    p = PaninianObject(form, encoding=sanscript.SLP1)
    for t in ("pada", "tiNanta", prayoga, *meaning_tags):
        p.setTag(t)
    return p


Bajati  = tinanta_pada("Bajati",  "kartari")   # भजति "worships"
sevyate = tinanta_pada("sevyate", "karmaRi")   # सेव्यते "is served"


# ── Kāraka Phase K1 (karaka_plan.md §5): verb meaning-class membership ────────
# The kāraka pre-pass reads these as rp tags off the sentence dhātu.
#
#  - meaning-classes for 1.4.52 (gati/buddhi/pratyavasāna/śabdakarma/akarmaka):
#       gatyarTa, budDyarTa, pratyavasAnArTa, SabdakarmA, akarmaka
#  - Ryanta            : the verb is a causative (ṇic-anta) — gate for 1.4.52/53
#  - hfkf              : √hṛ / √kṛ (1.4.53 optional kartṛ→karma)
#  - dvikarmaka        : duhādi-12 + nī-ādi-4 (1.4.51 akathita-karma); the gaṇa
#                        membership is the SK539 kārikā
#                          दुह्याच्पच्दण्ड्रुधिप्रच्छिचिब्रूशासुजिमथ्मुषाम् ।
#                          कर्मयुक् स्यादकथितं तथा स्यान्नीहृकृष्वहाम् ॥
#  - aDiSIN/aBiniviS/upAdivas : the upasarga-bound loci-as-karma verbs of
#                        1.4.46 (adhi-śī/sthā/ās), 1.4.47 (abhi-ni-viś),
#                        1.4.48 (upa/anu/adhi/āṅ-vas)

# duhādi-12 (1.4.51): √duh, yāc, pac, daṇḍ, rudh, prach, ci, brū, śās, ji,
# math, muṣ; nī-ādi-4: √nī, hṛ, kṛṣ, vah. These take two karmans; in our scope
# verbs enter as pre-formed padas, so the list is documentation + the gaṇa-head
# Dhatu entries that already exist are tagged dvikarmaka.
DVIKARMAKA_DHATUS = ("duh", "yAc", "pac", "daRq", "ruD", "praC", "ci", "brU",
                     "SAs", "ji", "maT", "muz",       # duhādi-12
                     "nI", "hf", "kfz", "vah")        # nī-ādi-4
for _d in (duh, vah):                                  # the heads present here
    _d.setTag("dvikarmaka")

# Pre-formed tiṅanta padas for the K1 test sentences (tiṅanta derivation TODO,
# §6). meaning_tags ride on the pada and are read via rp by the pre-pass.
spfSati     = tinanta_pada("spfSati",     "kartari")                              # स्पृशति "touches" — 1.4.50 anīpsita
dogDi       = tinanta_pada("dogDi",       "kartari", ["dvikarmaka"])             # दोग्धि "milks" — 1.4.51 (duhādi)
Aste        = tinanta_pada("Aste",        "kartari", ["akarmaka"])              # आस्ते "stays/sits" — 1.4.51 vārttika
agamayat    = tinanta_pada("agamayat",    "kartari", ["Ryanta", "gatyarTa"])    # अगमयत् "made go" — 1.4.52 gati
aDyApayat   = tinanta_pada("aDyApayat",   "kartari", ["Ryanta", "budDyarTa"])   # अध्यापयत् "made study" — 1.4.52 buddhi
kArayati    = tinanta_pada("kArayati",    "kartari", ["Ryanta", "hfkf"])        # कारयति "causes to make" — 1.4.53
aDyAste     = tinanta_pada("aDyAste",     "kartari", ["aDiSIN"])                # अध्यास्ते "occupies" — 1.4.46
aBiniviSate = tinanta_pada("aBiniviSate", "kartari", ["aBiniviS"])             # अभिनिविशते "settles on" — 1.4.47
upavasati   = tinanta_pada("upavasati",   "kartari", ["upAdivas"])             # उपवसति "dwells in" — 1.4.48
pAcayati    = tinanta_pada("pAcayati",    "kartari", ["Ryanta"])               # पाचयति "causes to cook" — 1.4.52 गत्यादि-किम् negative (ṇyanta but not a gati-class verb)
