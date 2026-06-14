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

# ── Kāraka Phase K3 (karaka_plan.md §K3): tṛtīyā-cluster verb tags ───────────
#  - div     : √div (दिवु क्रीडाविजिगीषा…, "play/gamble") — 1.4.43 दिवः कर्म च:
#              its sādhakatama (the dice) is optionally karma else karaṇa.
#  - saMjYAna : sam-pūrva √jñā (saṁjānīte, "recognizes/agrees with") — 2.3.22
#              संज्ञोऽन्यतरस्यां कर्मणि: its karma is optionally tṛtīyā else dvitīyā.
dIvyati   = tinanta_pada("dIvyati",   "kartari", ["div"])       # दीव्यति "gambles" — 1.4.43 (vibhāṣā)
saMjAnIte = tinanta_pada("saMjAnIte", "kartari", ["saMjYAna"])  # संजानीते "agrees with" — 2.3.22 (vibhāṣā)

# ── Kāraka Phase K4 (karaka_plan.md §K4): sampradāna + caturthī verb tags ─────
# Meaning-class tags read via rp by the sampradāna saṁjñā rules 1.4.33–41/1.4.44:
#  - rucyarTa    : ruc-class "please" (rocate)                  — 1.4.33
#  - slAGAdi     : ślāgh/hnu/sthā/śap "inform by …"             — 1.4.34
#  - DAri        : ṇyanta dhṛ "owe" (dhārayati)                 — 1.4.35
#  - spfha       : spṛh "desire" (spṛhayati)                    — 1.4.36
#  - kruDdruh    : krudh/druh "be angry at"                     — 1.4.37 (target → sampradāna)
#  - upasfzwa    : the verb bears an upasarga (abhi-krudh …); with kruDdruh,
#                  the target → karma by 1.4.38 (param beats 1.4.37). Explicit
#                  input tag (verbs are pre-formed padas, §6); real upasarga
#                  scanning is a post-tiṅanta TODO.
#  - rADIkz      : rādh/īkṣ "deliberate/consider for"           — 1.4.39
#  - pratiANSru  : prati/āṅ + śru "promise"                     — 1.4.40
#  - anupratigF  : anu/prati + gṝ "respond/applaud"             — 1.4.41
#  - parikrayaRa : pari-krī "hire" (parikrīṇīte)                — 1.4.44 (vibhāṣā)
#  - manyarTa    : man "consider" (manyate)                     — 2.3.17 (vibhāṣā)
#  - gatyarTa    : motion verbs (gacchati); reused from K1      — 2.3.12 (vibhāṣā)
dadAti       = tinanta_pada("dadAti",       "kartari")                          # ददाति "gives" — 1.4.32 general sampradāna
rocate       = tinanta_pada("rocate",       "kartari", ["rucyarTa"])            # रोचते "pleases" — 1.4.33
slAGate      = tinanta_pada("slAGate",      "kartari", ["slAGAdi"])             # श्लाघते "praises (to inform)" — 1.4.34
DArayati     = tinanta_pada("DArayati",     "kartari", ["DAri"])                # धारयति "owes" — 1.4.35
spfhayati    = tinanta_pada("spfhayati",    "kartari", ["spfha"])               # स्पृहयति "desires" — 1.4.36
kruDyati     = tinanta_pada("kruDyati",     "kartari", ["kruDdruh"])            # क्रुध्यति "is angry at" — 1.4.37
aBikruDyati  = tinanta_pada("aBikruDyati",  "kartari", ["kruDdruh", "upasfzwa"])  # अभिक्रुध्यति "is angry at" (upasṛṣṭa) — 1.4.38 (param)
rADyati      = tinanta_pada("rADyati",      "kartari", ["rADIkz"])              # राध्यति "deliberates for" — 1.4.39
pratiSfRoti  = tinanta_pada("pratiSfRoti",  "kartari", ["pratiANSru"])          # प्रतिशृणोति "promises" — 1.4.40
anugfRAti    = tinanta_pada("anugfRAti",    "kartari", ["anupratigF"])          # अनुगृणाति "responds to" — 1.4.41
parikrIRIte  = tinanta_pada("parikrIRIte",  "kartari", ["parikrayaRa"])         # परिक्रीणीते "hires" — 1.4.44 (vibhāṣā)
manyate      = tinanta_pada("manyate",      "kartari", ["manyarTa"])            # मन्यते "considers" — 2.3.17 (vibhāṣā)
gacCati      = tinanta_pada("gacCati",      "kartari", ["gatyarTa"])            # गच्छति "goes to" — 2.3.12 (vibhāṣā)

# ── Kāraka Phase K5 (karaka_plan.md §K5): apādāna + pañcamī verb tags ─────────
# Meaning-class tags read via rp by the apādāna saṁjñā rules 1.4.25–31:
#  - BItrA       : bhī/trā "fear/protect-from" (bibheti)         — 1.4.25 (bhaya-hetu → apādāna)
#  - parAji      : parā-ji "fail/give up" (parājayate)           — 1.4.26 (asoḍha → apādāna)
#  - vAraRArTa   : vāraṇa "ward off" (vārayati)                  — 1.4.27 (īpsita → apādāna)
#  - antarDi     : "hide from" (nilīyate, in concealment)        — 1.4.28
#  - upayoga     : ākhyātṛ/learn-from (adhīte, in upayoga)       — 1.4.29
#  - jani        : √jan "be born" (prajāyate)                    — 1.4.30 (prakṛti → apādāna)
#  - praBava     : √bhū "originate from" (prabhavati)            — 1.4.31
Ayati        = tinanta_pada("Ayati",        "kartari")                          # आयाति "comes (from)" — 1.4.24 general apādāna
biBeti       = tinanta_pada("biBeti",       "kartari", ["BItrA"])               # बिभेति "fears" — 1.4.25
parAjayate   = tinanta_pada("parAjayate",   "kartari", ["parAji"])              # पराजयते "gives up" — 1.4.26
vArayati     = tinanta_pada("vArayati",     "kartari", ["vAraRArTa"])           # वारयति "wards off" — 1.4.27
nilIyate     = tinanta_pada("nilIyate",     "kartari", ["antarDi"])             # निलीयते "hides" — 1.4.28
aDIte        = tinanta_pada("aDIte",        "kartari", ["upayoga"])             # अधीते "studies" — 1.4.29
prajAyate    = tinanta_pada("prajAyate",    "kartari", ["jani"])                # प्रजायते "is born" — 1.4.30
praBavati    = tinanta_pada("praBavati",    "kartari", ["praBava"])             # प्रभवति "originates" — 1.4.31

# ── Kāraka Phase K6 (karaka_plan.md §K6): ṣaṣṭhī-chapter verb tags ────────────
# Verb-conditioned ṣaṣṭhī rules SK612–619/621 read these meaning-class tags via
# rp off the sentence dhātu. Each marks its karaṇa/karman as a *śeṣa* (the
# kāraka is not abhihita by a finite verb here — the action is named, so the
# participant relates as śeṣa → kāraka-section ṣaṣṭhī), so the test nouns carry
# semantic_Seza and these rules are apavādas to 2.3.50 (śeṣe ṣaṣṭhī) that pin
# the SAME viBakti_6 with the verb-specific scope the sutras describe.
#  - jYAvid    : √jñā NOT in the "know" sense (avid-artha), karaṇa     — 2.3.51
#  - aDIgartha : adhi-i (smṛ-sense) / day / īś, karman                 — 2.3.52
#  - kfYpratiyatna : √kṛ in pratiyatna (guṇādhāna), karman            — 2.3.53
#  - rujArTa   : ruj-sense bhāva-verbs (not jvar), karman              — 2.3.54
#  - nATASis   : √nāth in āśis (blessing) sense, karman                — 2.3.55
#  - hiMsArTa  : jāsi/ni-prahaṇa/nāṭa/krātha/piṣ hiṁsā-verbs, karman  — 2.3.56
#  - vyavahfpaR : vyavahṛ/paṇ in equal (samartha) sense, karman        — 2.3.57
#  - divtadarTa : √div in gambling / buy-sell sense, karman            — 2.3.58
#  - prezyabrU : preṣ/brū in devatā-sampradāna with a havis-word       — 2.3.61
jAnIte       = tinanta_pada("jAnIte",       "kartari", ["jYAvid"])      # जानीते "knows-of/recognizes" (avid-artha) — 2.3.51 सर्पिषो जानीते
smarati      = tinanta_pada("smarati",      "kartari", ["aDIgartha"])   # स्मरति "remembers" (adhi-i) — 2.3.52 मातुः स्मरति
upaskurute   = tinanta_pada("upaskurute",   "kartari", ["kfYpratiyatna"])  # उपस्कुरुते "prepares (guṇādhāna)" — 2.3.53
rujati       = tinanta_pada("rujati",       "kartari", ["rujArTa"])     # रुजति "pains/breaks" — 2.3.54 चौरस्य रुजति
nATate       = tinanta_pada("nATate",       "kartari", ["nATASis"])     # नाथते "blesses/asks" (āśis) — 2.3.55 सर्पिषो नाथते
ujjAsayati   = tinanta_pada("ujjAsayati",   "kartari", ["hiMsArTa"])    # उज्जासयति "destroys" (hiṁsā) — 2.3.56 चौरस्य उज्जासयति
vyavaharati  = tinanta_pada("vyavaharati",  "kartari", ["vyavahfpaR"])  # व्यवहरति "deals/trades" (samartha) — 2.3.57 शतस्य व्यवहरति
prezyati     = tinanta_pada("prezyati",     "kartari", ["prezyabrU"])   # प्रेष्य "directs" (devatā-sampradāna) — 2.3.61 छागस्य हविषः प्रेष्य

# √div in gambling sense for SK619/620 — reuses the K3 "div" tag (1.4.43) PLUS
# the SK619 "divtadarTa" karman-ṣaṣṭhī scope; prati-div is the upasṛṣṭa variant
# for the SK620 vibhāṣā fork (otherwise the SK619 ṣaṣṭhī falls to 2.3.2 dvitīyā).
dIvyatiK6     = tinanta_pada("dIvyati",     "kartari", ["div", "divtadarTa"])              # दीव्यति "gambles for" — 2.3.58 शतस्य दीव्यति
pratidIvyati  = tinanta_pada("pratidIvyati", "kartari", ["div", "divtadarTa", "upasfzwa"])  # प्रतिदीव्यति "gambles against" — 2.3.59 (vibhāṣā)

# ── Kāraka Phase K7 (karaka_plan.md §K7): adhikaraṇa + saptamī verb tags ──────
# The adhikaraṇa saṁjñā (1.4.45) reads only the noun's semantic_ADAra, so most
# K7 verbs need no special tag — they just supply the prayoga + a dhātu for the
# pre-pass rp.  kfYi marks √kṛ for SK646 (विभाषा कृञि: adhi optionally kp before
# √kṛ); pravavarza is the verbless-rain example dhātu for the absolute SK634.
icCAsti      = tinanta_pada("icCAsti",      "kartari", ["akarmaka"])            # इच्छास्ति "desire exists" — 1.4.45 (मोक्षे इच्छास्ति)
pacati       = tinanta_pada("pacati",       "kartari")                          # पचति "cooks" — 1.4.45 (स्थाल्यां पचति)
gataH        = tinanta_pada("gataH",        "kartari", ["gatyarTa"])            # गतः "[he] left/went" — 2.3.37 (गोषु दुह्यमानासु गतः)
prAvrAjIt    = tinanta_pada("prAvrAjIt",    "kartari")                          # प्राव्राजीत् "renounced" — 2.3.38 (रुदति/रुदतो वा)
biBeti       = tinanta_pada("biBeti",       "kartari")                          # बिभेति "fears" — generic adhikaraṇa example verb
aDikarizyati = tinanta_pada("aDikarizyati", "kartari", ["kfYi"])               # अधिकरिष्यति "will appoint" — 1.4.98 (vibhāṣā kṛñi)
