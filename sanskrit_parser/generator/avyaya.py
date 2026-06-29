from sanskrit_parser.generator.pratipadika import Pratipadika
# saha is already defined in pratipadika.py (nipāta, tagged "saha" for the
# sadhryac sadhri-ādeśa). Re-export the SAME object here — defining a fresh
# svarādi `saha` would shadow it under `from avyaya import *` (vibhaktis_list)
# and break the saDryac compound. Used as the 2.3.19 saha-yoga particle.
from sanskrit_parser.generator.pratipadika import saha  # noqa: F401
from sanskrit_parser.generator.pratyaya import Pratyaya

# ── Section 1: svarādi gaṇa (1.1.37 / SK447) ─────────────────────────────────
# Tagged ?svarAdi → avyaya saṁjñā via SK447; sup deleted via SK452 (2.4.82).
# All 24 vibhakti forms = avasāna form of the stem.
antar  = Pratipadika("antar",  "pum", other_tags=["svarAdi"])   # अन्तर् "within"
prAtar = Pratipadika("prAtar", "pum", other_tags=["svarAdi"])   # प्रातर् "in the morning"
punar  = Pratipadika("punar",  "pum", other_tags=["svarAdi"])   # पुनर् "again"
bahiS  = Pratipadika("bahis",  "pum", other_tags=["svarAdi"])   # बहिस् "outside"
naktam = Pratipadika("naktam", "pum", other_tags=["svarAdi"])   # नक्तम् "at night"
svayam = Pratipadika("svayam", "pum", other_tags=["svarAdi"])   # स्वयम् "self"

svar      = Pratipadika("svar",      "pum", other_tags=["svarAdi"])  # स्वर् "heaven/sun"
sanutar   = Pratipadika("sanutar",   "pum", other_tags=["svarAdi"])  # सनुतर् "in concealment"
uccEs     = Pratipadika("uccEs",     "pum", other_tags=["svarAdi"])  # उच्चैस् "aloft"
nIcEs     = Pratipadika("nIcEs",     "pum", other_tags=["svarAdi"])  # नीचैस् "low down"
SanEs     = Pratipadika("SanEs",     "pum", other_tags=["svarAdi"])  # शनैस् "slowly"
fDak      = Pratipadika("fDak",      "pum", other_tags=["svarAdi"])  # ऋधक् "separately"
fte       = Pratipadika("fte",       "pum", other_tags=["svarAdi"])  # ऋते "except/without"
yugapat   = Pratipadika("yugapat",   "pum", other_tags=["svarAdi"])  # युगपत् "simultaneously"
ArAt      = Pratipadika("ArAt",      "pum", other_tags=["svarAdi"])  # आरात् "near/far from"
pfTak     = Pratipadika("pfTak",     "pum", other_tags=["svarAdi"])  # पृथक् "separately"
zvas      = Pratipadika("Svas",      "pum", other_tags=["svarAdi"])  # श्वस् "tomorrow" (S=ś=श)
hyas      = Pratipadika("hyas",      "pum", other_tags=["svarAdi"])  # ह्यस् "yesterday" (Vasu)
divA      = Pratipadika("divA",      "pum", other_tags=["svarAdi"])  # दिवा "by day"
rAtrO     = Pratipadika("rAtrO",     "pum", other_tags=["svarAdi"])  # रात्रौ "at night"
sAyam     = Pratipadika("sAyam",     "pum", other_tags=["svarAdi"])  # सायम् "at eve"
ciram     = Pratipadika("ciram",     "pum", other_tags=["svarAdi"])  # चिरम् "long/long since"
manAk     = Pratipadika("manAk",     "pum", other_tags=["svarAdi"])  # मनाक् "a little"
Izat      = Pratipadika("Izat",      "pum", other_tags=["svarAdi"])  # ईषत् "slightly"
jozam     = Pratipadika("jozam",     "pum", other_tags=["svarAdi"])  # जोषम् "gladly"
tUSRIm    = Pratipadika("tUzRIm",    "pum", other_tags=["svarAdi"])  # तूष्णीम् "silently" (z=ṣ, R=ṇ)
avas      = Pratipadika("avas",      "pum", other_tags=["svarAdi"])  # अवस् "below/outside" (SK; Vasu: avis)
samayA    = Pratipadika("samayA",    "pum", other_tags=["svarAdi"])  # समया "near"
nikazA    = Pratipadika("nikazA",    "pum", other_tags=["svarAdi"])  # निकषा "near/close by"
vfTA      = Pratipadika("vfTA",      "pum", other_tags=["svarAdi"])  # वृथा "in vain"
naY       = Pratipadika("naY",       "pum", other_tags=["svarAdi"])  # नञ् "not"
hetO      = Pratipadika("hetO",      "pum", other_tags=["svarAdi"])  # हेतौ "by reason of"
idDA      = Pratipadika("idDA",      "pum", other_tags=["svarAdi"])  # इद्धा "truly"
adDA      = Pratipadika("adDA",      "pum", other_tags=["svarAdi"])  # अद्धा "evidently"
sAmi      = Pratipadika("sAmi",      "pum", other_tags=["svarAdi"])  # सामि "half"
vat       = Pratipadika("vat",       "pum", other_tags=["svarAdi"])  # वत् "like" (particle)
sanA      = Pratipadika("sanA",      "pum", other_tags=["svarAdi"])  # सना "perpetually"
sanat     = Pratipadika("sanat",     "pum", other_tags=["svarAdi"])  # सनत् "perpetually"
sanAt     = Pratipadika("sanAt",     "pum", other_tags=["svarAdi"])  # सनात् "perpetually"
upaDA     = Pratipadika("upaDA",     "pum", other_tags=["svarAdi"])  # उपधा "division"
antarA    = Pratipadika("antarA",    "pum", other_tags=["svarAdi"])  # अन्तरा "except/between"
antareRa  = Pratipadika("antareRa",  "pum", other_tags=["svarAdi"])  # अन्तरेण "except/without"
jyok      = Pratipadika("jyok",      "pum", other_tags=["svarAdi"])  # ज्योक् "long"
kam       = Pratipadika("kam",       "pum", other_tags=["svarAdi"])  # कम् "expletive"
Sam       = Pratipadika("Sam",       "pum", other_tags=["svarAdi"])  # शम् "ease/welfare"
sahasA    = Pratipadika("sahasA",    "pum", other_tags=["svarAdi"])  # सहसा "suddenly"
vinA      = Pratipadika("vinA",      "pum", other_tags=["svarAdi"])  # विना "without"
nAnA      = Pratipadika("nAnA",      "pum", other_tags=["svarAdi"])  # नाना "variously"
svasti    = Pratipadika("svasti",    "pum", other_tags=["svarAdi"])  # स्वस्ति "greeting/peace"
svaDA     = Pratipadika("svaDA",     "pum", other_tags=["svarAdi"])  # स्वधा "oblation to Manes"
alam      = Pratipadika("alam",      "pum", other_tags=["svarAdi"])  # अलम् "enough"
vazaw     = Pratipadika("vazaw",     "pum", other_tags=["svarAdi"])  # वषट् "oblation-cry"
SrOzaw    = Pratipadika("SrOzaw",   "pum", other_tags=["svarAdi"])  # श्रौषट् "oblation-cry"
vOzaw     = Pratipadika("vOzaw",    "pum", other_tags=["svarAdi"])  # वौषट् "oblation-cry"
anyat     = Pratipadika("anyat",     "pum", other_tags=["svarAdi"])  # अन्यत् "otherwise/again"
asti      = Pratipadika("asti",      "pum", other_tags=["svarAdi"])  # अस्ति "being present"
upAMSu    = Pratipadika("upAMSu",   "pum", other_tags=["svarAdi"])  # उपांशु "in a low voice"
kzamA     = Pratipadika("kzamA",     "pum", other_tags=["svarAdi"])  # क्षमा "patience/pardon"
vihAyasA  = Pratipadika("vihAyasA", "pum", other_tags=["svarAdi"])  # विहायसा "aloft in the air"
dozA      = Pratipadika("dozA",      "pum", other_tags=["svarAdi"])  # दोषा "at night/evening"
mfzA      = Pratipadika("mfzA",      "pum", other_tags=["svarAdi"])  # मृषा "falsely"
miTyA     = Pratipadika("miTyA",     "pum", other_tags=["svarAdi"])  # मिथ्या "falsely"
muDA      = Pratipadika("muDA",      "pum", other_tags=["svarAdi"])  # मुधा "in vain"
purA      = Pratipadika("purA",      "pum", other_tags=["svarAdi"])  # पुरा "formerly"
miTo      = Pratipadika("miTo",      "pum", other_tags=["svarAdi"])  # मिथो "mutually"
miTas     = Pratipadika("miTas",     "pum", other_tags=["svarAdi"])  # मिथस् "mutually"
prAyas    = Pratipadika("prAyas",    "pum", other_tags=["svarAdi"])  # प्रायस् "frequently"
muhus     = Pratipadika("muhus",     "pum", other_tags=["svarAdi"])  # मुहुस् "repeatedly"
pravAhukam = Pratipadika("pravAhukam", "pum", other_tags=["svarAdi"])  # प्रवाहुकम् "at the same time"
pravAhikA  = Pratipadika("pravAhikA",  "pum", other_tags=["svarAdi"])  # प्रवाहिका "at the same time"
Aryahalam  = Pratipadika("Aryahalam",  "pum", other_tags=["svarAdi"])  # आर्यहलम् "violently"
aBIkzRam   = Pratipadika("aBIkzRam",  "pum", other_tags=["svarAdi"])  # अभीक्ष्णम् "repeatedly"
sAkam     = Pratipadika("sAkam",     "pum", other_tags=["svarAdi"])  # साकम् "together" (2.3.19 saha-yoga)
sArDam    = Pratipadika("sArDam",    "pum", other_tags=["svarAdi"])  # सार्धम् "together with" (2.3.19)
samam     = Pratipadika("samam",     "pum", other_tags=["svarAdi"])  # समम् "together with" (2.3.19; saha re-exported above)
hiruk     = Pratipadika("hiruk",     "pum", other_tags=["svarAdi"])  # हिरुक् "without"
Dik       = Pratipadika("Dik",       "pum", other_tags=["svarAdi"])  # धिक् "fie!"
aTa       = Pratipadika("aTa",       "pum", other_tags=["svarAdi"])  # अथ "thus/now"
am_avyaya        = Pratipadika("am",        "pum", other_tags=["svarAdi"])  # अम् "particle"
Am_avyaya        = Pratipadika("Am",        "pum", other_tags=["svarAdi"])  # आम् "yes/assent"
pratAm    = Pratipadika("pratAm",    "pum", other_tags=["svarAdi"])  # प्रताम् "with fatigue"
praSAn    = Pratipadika("praSAn",    "pum", other_tags=["svarAdi"])  # प्रशान् "alike"
pratAn    = Pratipadika("pratAn",    "pum", other_tags=["svarAdi"])  # प्रतान् "widely"
mA        = Pratipadika("mA",        "pum", other_tags=["svarAdi"])  # मा "don't" (prohibitive)

# ── Section 2: ākaṛtigaṇa additions (SK447) ──────────────────────────────────
# Tagged ?nipAta → avyaya saṁjñā via SK447 nipAta branch.
ca        = Pratipadika("ca",        "pum", other_tags=["nipAta"])   # च "and"
vA        = Pratipadika("vA",        "pum", other_tags=["nipAta"])   # वा "or"
ha        = Pratipadika("ha",        "pum", other_tags=["nipAta"])   # ह particle
aha       = Pratipadika("aha",       "pum", other_tags=["nipAta"])   # अह particle
eva       = Pratipadika("eva",       "pum", other_tags=["nipAta"])   # एव "only/exactly"
evam      = Pratipadika("evam",      "pum", other_tags=["nipAta"])   # एवम् "thus"
nUnam     = Pratipadika("nUnam",     "pum", other_tags=["nipAta"])   # नूनम् "certainly"
SaSvat    = Pratipadika("SaSvat",    "pum", other_tags=["nipAta"])   # शश्वत् "ever"
BUyas     = Pratipadika("BUyas",     "pum", other_tags=["nipAta"])   # भूयस् "more/again"
kUpat     = Pratipadika("kUpat",     "pum", other_tags=["nipAta"])   # कूपत् particle
kuvit     = Pratipadika("kuvit",     "pum", other_tags=["nipAta"])   # कुवित् "perhaps"
sUpats    = Pratipadika("sUpats",    "pum", other_tags=["nipAta"])   # सूपत्स particle
net       = Pratipadika("net",       "pum", other_tags=["nipAta"])   # नेत् "lest"
cet       = Pratipadika("cet",       "pum", other_tags=["nipAta"])   # चेत् "if"
caR       = Pratipadika("caR",       "pum", other_tags=["nipAta"])   # चण् particle
kaccit    = Pratipadika("kaccit",    "pum", other_tags=["nipAta"])   # कच्चित् "I hope/perhaps"
kiMcit    = Pratipadika("kiMcit",    "pum", other_tags=["nipAta"])   # किंचित् "somewhat"
yatra     = Pratipadika("yatra",     "pum", other_tags=["nipAta"])   # यत्र "where"
naha      = Pratipadika("naha",      "pum", other_tags=["nipAta"])   # नह particle
hanta     = Pratipadika("hanta",     "pum", other_tags=["nipAta"])   # हन्त "alas/come!"
mAkiH     = Pratipadika("mAkiH",    "pum", other_tags=["nipAta"])   # माकिः particle
mAkim     = Pratipadika("mAkim",     "pum", other_tags=["nipAta"])   # माकिम् particle
nakiH     = Pratipadika("nakiH",     "pum", other_tags=["nipAta"])   # नकिः particle
Akim      = Pratipadika("Akim",      "pum", other_tags=["nipAta"])   # आकिम् particle
yAvat     = Pratipadika("yAvat",     "pum", other_tags=["nipAta"])   # यावत् "as long as"
tAvat     = Pratipadika("tAvat",     "pum", other_tags=["nipAta"])   # तावत् "so long/then"
tvE       = Pratipadika("tvE",       "pum", other_tags=["nipAta"])   # त्वै particle
dvE       = Pratipadika("dvE",       "pum", other_tags=["nipAta"])   # द्वै particle
rE_avyaya        = Pratipadika("rE",        "pum", other_tags=["nipAta"])   # रै particle
svAhA     = Pratipadika("svAhA",     "pum", other_tags=["nipAta"])   # स्वाहा "oblation-cry"
tum       = Pratipadika("tum",       "pum", other_tags=["nipAta"])   # तुम् particle
taTAhi    = Pratipadika("taTAhi",    "pum", other_tags=["nipAta"])   # तथाहि "therefore"
Kalu      = Pratipadika("Kalu",      "pum", other_tags=["nipAta"])   # खलु "indeed"
kila      = Pratipadika("kila",      "pum", other_tags=["nipAta"])   # किल "they say"
aTo       = Pratipadika("aTo",       "pum", other_tags=["nipAta"])   # अथो "and so"
suzWu     = Pratipadika("suzWu",     "pum", other_tags=["nipAta"])   # सुष्ठु "well/rightly"
sma       = Pratipadika("sma",       "pum", other_tags=["nipAta"])   # स्म particle (past marker)
Adaha     = Pratipadika("Adaha",     "pum", other_tags=["nipAta"])   # आदह particle

# ── Section 3: third section — vowels and exclamations (SK447) ───────────────
# Tagged ?nipAta → avyaya saṁjñā via SK447 nipAta branch.
# Single-letter variables use _sva suffix to avoid Python name conflicts.
a_sva     = Pratipadika("a",         "pum", other_tags=["nipAta"])   # अ
A_sva     = Pratipadika("A",         "pum", other_tags=["nipAta"])   # आ
i_sva     = Pratipadika("i",         "pum", other_tags=["nipAta"])   # इ
I_sva     = Pratipadika("I",         "pum", other_tags=["nipAta"])   # ई
u_sva     = Pratipadika("u",         "pum", other_tags=["nipAta"])   # उ
U_sva     = Pratipadika("U",         "pum", other_tags=["nipAta"])   # ऊ
e_sva     = Pratipadika("e",         "pum", other_tags=["nipAta"])   # ए
E_sva     = Pratipadika("E",         "pum", other_tags=["nipAta"])   # ऐ
o_sva     = Pratipadika("o",         "pum", other_tags=["nipAta"])   # ओ
O_sva     = Pratipadika("O",         "pum", other_tags=["nipAta"])   # औ
paSu_nipAta  = Pratipadika("paSu",   "pum", other_tags=["nipAta"])   # पशु (avoids conflict with pum paSu)
Sukam_nipAta = Pratipadika("Sukam",  "pum", other_tags=["nipAta"])   # शुकम्
yaTAkaTAca = Pratipadika("yaTAkaTAca", "pum", other_tags=["nipAta"])   # यथाकथाच
pAw       = Pratipadika("pAw",       "pum", other_tags=["nipAta"])   # पाट्
pyAw      = Pratipadika("pyAw",      "pum", other_tags=["nipAta"])   # प्याट्
aNga      = Pratipadika("aNga",      "pum", other_tags=["nipAta"])   # अङ्ग "please/come"
hE        = Pratipadika("hE",        "pum", other_tags=["nipAta"])   # है (vocative)
he        = Pratipadika("he",        "pum", other_tags=["nipAta"])   # हे (vocative)
Bos       = Pratipadika("Bos",       "pum", other_tags=["nipAta"])   # भोस् "sir/hey"
aye       = Pratipadika("aye",       "pum", other_tags=["nipAta"])   # अये (vocative)
dya       = Pratipadika("dya",       "pum", other_tags=["nipAta"])   # द्य
vizu      = Pratipadika("vizu",      "pum", other_tags=["nipAta"])   # विषु
ekapade   = Pratipadika("ekapade",   "pum", other_tags=["nipAta"])   # एकपदे
yut       = Pratipadika("yut",       "pum", other_tags=["nipAta"])   # युत्
Atas      = Pratipadika("Atas",      "pum", other_tags=["nipAta"])   # आतस् → आतः

# ── Kāraka Phase K2: karmapravacanīya particle words (karaka_plan.md §K2) ─────
# Standalone avyaya words (passthrough like he/antarA): nipāta → SK447 avyaya →
# 2.4.82 sup-luk. They carry their per-usage sense tag at input (semantic_lakzaRa
# etc.); the pre-pass Pass A then assigns karmapravacanIya. Distinct from the
# nipāta upasarga Pratyaya objects below (upa_upasarga/ati_upasarga).
anu_kp   = Pratipadika("anu",   "pum", other_tags=["nipAta"])   # अनु (1.4.84/85/86, 1.4.90)
upa_kp   = Pratipadika("upa",   "pum", other_tags=["nipAta"])   # उप (1.4.87)
prati_kp = Pratipadika("prati", "pum", other_tags=["nipAta"])   # प्रति (1.4.90)
pari_kp  = Pratipadika("pari",  "pum", other_tags=["nipAta"])   # परि (1.4.90)
aBi_kp   = Pratipadika("aBi",   "pum", other_tags=["nipAta"])   # अभि (1.4.91)
apa_kp   = Pratipadika("apa",   "pum", other_tags=["nipAta"])   # अप (1.4.88 varjana)
AN_kp    = Pratipadika("A",     "pum", other_tags=["nipAta"])   # आङ् (1.4.89 maryādā; surfaces आ)
aDi_kp   = Pratipadika("aDi",   "pum", other_tags=["nipAta"])   # अधि (1.4.93, deferred)
su_kp    = Pratipadika("su",    "pum", other_tags=["nipAta"])   # सु (1.4.94)
ati_kp   = Pratipadika("ati",   "pum", other_tags=["nipAta"])   # अति (1.4.95)
api_kp   = Pratipadika("api",   "pum", other_tags=["nipAta"])   # अपि (1.4.96)

# ── Avyayībhāva-samāsa pūrva-pada avyayas (avyayībhāva samāsa plan, S1A) ──────
# Prādi avyayas that head an avyayībhāva (2.1.6). nipāta → avyaya saṁjñā via
# SK447 (1.1.37). They carry their per-usage avyayībhāva sense at input
# (semantic_samIpa, semantic_vibhakti, …); the samāsa pre-pass 2.1.6 then forms
# the compound and tags the uttara ?avyayIBAva.
upa_avyaya = Pratipadika("upa", "pum", other_tags=["nipAta"])   # उप (समीपम् — उपकृष्णम्)
aDi_avyaya = Pratipadika("aDi", "pum", other_tags=["nipAta"])   # अधि (विभक्ति — अधिहरि)

# ── Kāraka Phase K6: ṣaṣṭhī-chapter yoga-words (karaka_plan.md §K6) ───────────
# Fixed-surface "peek" words read by the K6 ṣaṣṭhī rules via llp/rrp (literal
# =word match), exactly like the K2/K3/K4 yoga particles (saha, namas, antarā).
# Each enters pre-inflected to its SK surface (kṛt/taddhita inflection of these
# is out of scope); they pass through bare (nipāta → SK447 avyaya → 2.4.82 luk).
# Class tags let the K6 rules match by artha/pratyaya rather than a single literal:
#   hetu        — the hetu-word (2.3.26/27)
#   atasuCarTa  — an atasartha-pratyaya word (atasuc/tasil… : dakṣiṇataḥ, puras…) (2.3.30)
#   enap        — an enap-anta word (dakṣiṇena, uttareṇa…) (2.3.31)
#   kftvasuCarTa — a kṛtvasuc-artha word (pañcakṛtvaḥ, saptakṛtvaḥ…) (2.3.64)
hetoH       = Pratipadika("hetoH",      "pum", other_tags=["nipAta", "hetu"])  # हेतोः (2.3.26/27 hetu-word, ṣaṣṭhī surface)
hetunA      = Pratipadika("hetunA",     "pum", other_tags=["nipAta", "hetu"])  # हेतुना (2.3.27 hetu-word, tṛtīyā surface)
dakziRatas  = Pratipadika("dakziRatas", "pum", other_tags=["nipAta", "atasuCarTa"])  # दक्षिणतः (2.3.30 atasartha-pratyaya word)
uttaratas   = Pratipadika("uttaratas",  "pum", other_tags=["nipAta", "atasuCarTa"])  # उत्तरतः (2.3.30 atasartha-pratyaya word)
dakziRena   = Pratipadika("dakziRena",  "pum", other_tags=["nipAta", "enap"])  # दक्षिणेन (2.3.31 enap-anta word)
uttareRa    = Pratipadika("uttareRa",   "pum", other_tags=["nipAta", "enap"])  # उत्तरेण (2.3.31 enap-anta word)
dUram       = Pratipadika("dUram",      "pum", other_tags=["nipAta"])  # दूरम् (2.3.34 dūrārtha word)
nikawam     = Pratipadika("nikawam",    "pum", other_tags=["nipAta"])  # निकटम् (2.3.34 antikārtha word)
paYcakftvas = Pratipadika("paYcakftvas","pum", other_tags=["nipAta", "kftvasuCarTa"])  # पञ्चकृत्वः (2.3.64 kṛtvas-artha word)
saptakftvas = Pratipadika("saptakftvas","pum", other_tags=["nipAta", "kftvasuCarTa"])  # सप्तकृत्वः (2.3.64 kṛtvas-artha word)

# ── nipāta upasargas ──────────────────────────────────────────────────────────
AN_upasarga  = Pratyaya("A",   its=["N"], other_tags=["nipAta", "upasarga", "pada"])
mAN_upasarga = Pratyaya("mA",  its=["N"], other_tags=["nipAta", "upasarga", "pada", "svarAdi"])
upa_upasarga = Pratyaya("upa", other_tags=["nipAta", "upasarga", "pada"])
pra_upasarga = Pratyaya("pra", other_tags=["nipAta", "upasarga", "pada"])
ava_upasarga = Pratyaya("ava", other_tags=["nipAta", "upasarga", "pada"])
ud_upasarga  = Pratyaya("ud",  other_tags=["nipAta", "upasarga", "pada"])
ati_upasarga = Pratyaya("ati", other_tags=["nipAta", "upasarga", "pada"])
