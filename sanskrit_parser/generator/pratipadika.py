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
# Plain a-stems for the kāraka test sentences (test/karaka_list.py)
putra = Pratipadika("putra", "pum")   # पुत्र — रामस्य पुत्रः (SK606)
mAza = Pratipadika("mAza", "pum")     # माष — माषेष्वश्वं बध्नाति counterexample (SK535)
bARa = Pratipadika("bARa", "pum")     # बाण — बाणेन (SK561 karaṇa)
kfzRa = Pratipadika("kfzRa", "pum")   # कृष्ण — कृष्णः (SK532 prathamā)
# Avyayībhāva-samāsa S1B uttara/pūrva nouns (avyayībhāva samāsa plan)
jIva = Pratipadika("jIva", "pum")     # जीव — यावज्जीवम् (2.1.8, a-stem → am)
SAka = Pratipadika("SAka", "pum")     # शाक — शाकप्रति (2.1.9 mātrārtha, noun pūrva)
Sakti = Pratipadika("Sakti", "strI")  # शक्ति — यथाशक्ति (2.1.7, i-stem fem → luk)
# S2 vibhāṣā-block uttara nouns
samudra = Pratipadika("samudra", "pum")  # समुद्र — आसमुद्रम् (2.1.13, a-stem → am)
vana = Pratipadika("vana", "napum")      # वन — अनुवनम् (2.1.15, a-stem → am)
muni = Pratipadika("muni", "pum")        # मुनि — द्विमुनि (2.1.19 vaṁśya, i-stem → luk)
cakra = Pratipadika("cakra", "napum")    # चक्र — सचक्रम् (6.3.81 saha→sa, a-stem → am)
Sarad = Pratipadika("Sarad", "strI", other_tags=["SaratpraBfti"])  # शरद् — उपशरदम् (5.4.107 TaC)
# Kāraka Phase K1 sentence stems (test/karaka_list.py; a-/i-stems reuse the
# rAma/hari paradigms).
mAsa = Pratipadika("mAsa", "pum")     # मास — मासमास्ते (SK539 akarmaka vārttika)
svarga = Pratipadika("svarga", "pum")  # स्वर्ग — शत्रूनगमयत्स्वर्गम् (SK540)
veda = Pratipadika("veda", "pum")     # वेद — वेदमध्यापयद्विधिम् (SK540 buddhi)
viDi = Pratipadika("viDi", "pum")     # विधि — the prayojya kartṛ→karma (SK540)
vEkuRWa = Pratipadika("vEkuRWa", "pum")  # वैकुण्ठ — अध्यास्ते/उपवसति वैकुण्ठम् (SK542/544)
sanmArga = Pratipadika("sanmArga", "pum")  # सन्मार्ग — अभिनिविशते सन्मार्गम् (SK543)
Bftya = Pratipadika("Bftya", "pum")   # भृत्य — कारयति भृत्यम् (SK541)
kawa = Pratipadika("kawa", "pum")     # कट — कारयति भृत्यं कटम् (SK541)
devadatta = Pratipadika("devadatta", "pum")  # देवदत्त — पाचयति देवदत्तेन (SK540 negative)
# Kāraka Phase K2 sentence stems (karmapravacanīya + atyanta-saṁyoga; SK546–558).
japa = Pratipadika("japa", "pum")     # जप — जपमनु प्रावर्षत् (SK547/548)
vfkza = Pratipadika("vfkza", "pum")   # वृक्ष — वृक्षं प्रति (SK552)
kroSa = Pratipadika("kroSa", "pum")   # क्रोश — क्रोशं गिरिः (SK558)
giri = Pratipadika("giri", "pum")     # गिरि — क्रोशं गिरिः (i-stem like hari) (SK558)
# Kāraka Phase K3 sentence stems (tṛtīyā cluster; SK562–568).
tApasa = Pratipadika("tApasa", "pum")   # तापस — जटाभिस्तापसः (SK566 itthambhūta-lakṣaṇa)
kARa   = Pratipadika("kARa",   "pum")   # काण — अक्ष्णा काणः (SK565 aṅga-vikāra; the one-eyed one)
# Kāraka Phase K7 sentence stems (adhikaraṇa + saptamī; SK632–646). Most reuse
# existing a-/i-/ṛ-/o-stem paradigms; the new ones below cover the SK examples.
#  - mokza  : मोक्ष — मोक्षे इच्छास्ति (SK633 vaiṣayika ādhāra → saptamī)
#  - BU     : भू "earth" (ū-stem strī) — अधि भुवि रामः / अधि रामे भूः (SK644/645)
#  - parArDa: परार्ध — उप परार्धे हरेर्गुणाः (SK645 upa adhika → kp_saptamī)
#  - sTAlI  : स्थाली (ī-stem strī, NI) — स्थाल्यां पचति (SK633 aupaśleṣika ādhāra)
#  - pAwaliputraka / mATura : SK639 पञ्चमी विभक्ते — माथुराः पाटलिपुत्रकेभ्यः
#  - duhyamAnA : दुह्यमाना (passive participle, ā-stem strī) — गोषु दुह्यमानासु गतः
#                (SK634 sati-saptamī partner; loc. pl. दुह्यमानासु)
#  - rudat  : रुदत् (śatṛ pum, √rud class 2, no vikaraṇa) — रुदति/रुदतो (SK635 anādara)
mokza   = Pratipadika("mokza",   "pum")
parArDa = Pratipadika("parArDa", "pum")
dUra    = Pratipadika("dUra",    "napum")  # दूर — वनस्य दूरे (SK633 dūrāntika → saptamī)
pUjana  = Pratipadika("pUjana",  "napum")  # पूजन — पूजने/पूजनस्य कुशलः (SK637 āsevā)
BU      = Pratipadika("BU",      "strI", other_tags=["BrU"])  # monosyllabic ū-stem strī: iyuvaṅ + optional nadī (भुवि/भ्वाम्), like bhrū
sTAlI   = Pratipadika("sTAlI",   "strI", other_tags=["NI"])
pAwaliputraka = Pratipadika("pAwaliputraka", "pum")
mATura  = Pratipadika("mATura",  "pum")
dvyaha  = Pratipadika("dvyaha",  "pum")   # द्व्यह — द्व्यहे/द्व्यहात् (SK643 kāraka-madhya)
# Yoga-words peeked by literal (=svAmin …) via llp/rrp during the pre-pass
# (matched on the bare stem, before any sup is inserted); each also takes its
# own prathamā as a sentence word. SK636/637/640 (svāmi-yoga, āyukta/kuśala,
# sādhu/nipuṇa). The other six members of 2.3.39 are documented in the rule.
svAmin  = Pratipadika("svAmin",  "pum")   # स्वामिन् — गवां/गोषु वा स्वामी (SK636)
Ayukta  = Pratipadika("Ayukta",  "pum")   # आयुक्त — आयुक्तः … (SK637)
kuSala  = Pratipadika("kuSala",  "pum")   # कुशल — कुशलः … (SK637/640)
sADu    = Pratipadika("sADu",    "pum")   # साधु — मातरि साधुः (SK640)
nipuRa  = Pratipadika("nipuRa",  "pum")   # निपुण — निपुणो वा (SK640)
duhyamAnA = Pratipadika("duhyamAnA", "strI", other_tags=["Ap"])
rudat   = Pratipadika("rudat",   "pum", its=["f"], other_tags=["Satf"])
# Kāraka Phase K4 sentence stems (sampradāna + caturthī; SK569–585).
grAma = Pratipadika("grAma", "pum")   # ग्राम — ग्रामं/ग्रामाय गच्छति (SK585 2.3.12 vibhāṣā)
vipra = Pratipadika("vipra", "pum")   # विप्र — विप्राय गां ददाति (SK569 1.4.32 general sampradāna)
# Kāraka Phase K5 sentence stems (apādāna + pañcamī; SK586–605).
cora    = Pratipadika("cora",    "pum")   # चोर — चोराद्बिभेति (SK588 1.4.25 bhaya-hetu → apādāna)
upADyAya = Pratipadika("upADyAya", "pum")  # उपाध्याय — उपाध्यायादधीते (SK592 1.4.29 ākhyātṛ)
Satru   = Pratipadika("Satru",   "pum")   # शत्रु — शत्रून्पराजयते (SK589 negative: defeats → karma)
saKi = Pratipadika("saKi", "pum", other_tags=["saKi", "sakhyAdi"])  # ?sakhyAdi: SK517 (4.1.62)
pati = Pratipadika("pati", "pum", other_tags=["pati"])
pAda = Pratipadika("pAda", "pum",  other_tags=["pAdAdi"])
yUza = Pratipadika("yUza", "pum",  other_tags=["pAdAdi", "gaurAdi"])  # gaurādi #44 (SK498); also 6.1.63 pādādi (yūṣan alt) → यूषी / यूष्णी
sarva = Pratipadika("sarva", "pum", other_tags=["sarvAdi"])
krozwu = Pratipadika("krozwu", "pum")
SamBu = Pratipadika("SamBu", "pum")
go = Pratipadika("go", "pum")
indra = Pratipadika("indra", "pum", other_tags=["indra", "indrAnuk"])  # indrAnuk: SK505 (4.1.49)
rE = Pratipadika("rE", "pum")
bahu = Pratipadika("bahu", "pum", other_tags=["bahvAdi"])  # SK462 pūrva-pada of बहुराजन्; ?bahvAdi: SK503 (4.1.45)
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
Uru   = Pratipadika("Uru",   "pum", other_tags=["Uru_uttara"])  # SK525 ūru uttara-pada (read in-window by 4.1.70)
paYca = Pratipadika("paYca", "pum")
garga = Pratipadika("garga", "pum")
# vidyA: SK472 negative test base — विद्या + अण् → वैद्य (the 'ya' is base-internal,
# NOT a taddhita ya), so ṅīp gives वैद्यी (no ya-lopa), cf. SC Vasu.
vidyA = Pratipadika("vidyA", "strI")
# kuru + car: SK470 ṭiṭ (टित्) test — कुरुचर + ṅīp → कुरुचरी. The ṭit affix is modelled
# with wac (टच्, the available ṭ-it samāsānta affix); strictly कुरुचर is चरेष्टः (3.2.16) ट.
kuru = Pratipadika("kuru", "pum", other_tags=["manuzya_jAti_u"])  # ?manuzya_jAti_u: SK521 (4.1.66) → kurūḥ
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
anIka = Pratipadika("anIka", "napum", other_tags=["ajAdi", "ajAdi_in_Dvigu"])
# Pala (फल): the phala uttara-pada — clean base tagged ?pAkAdi (SK519 4.1.64).
# Whether a phala-compound is ajādi (→ ṭāp: संफला/त्रिफला) or jāti (→ ṅīṣ: दासीफली)
# is decided by $$ajAdi_samasta / $$ajAdi_in_Dvigu on the (pūrva,uttara) pair —
# not baked here. See paribhasha.py and sutras_antaranga.yaml 4.1.4.1/4.1.4.2.
Pala  = Pratipadika("Pala",  "napum", other_tags=["pAkAdi"])

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
# UDas (long ū) tagged ?uDanta so SK483/484 can fire only on this stem. ?bahuvrIhi
# is attached to the uttara-pada (UDas) by the test composer via in_context; the
# saṃkhyā/avyaya nature of the *pūrva-pada* is read by SK485 peeking the left
# neighbour (llp: ?saMKyA / llp: ?avyaya — propagated to the neighbour in
# join_objects when ?samAsaPurva is set) — no fake ?saMKyAdi/?avyayAdi.
UDas    = Pratipadika("UDas",    "napum", other_tags=["uDanta"])
kuRqa   = Pratipadika("kuRqa",   "napum", other_tags=["jAnapadAdi"])  # ?jAnapadAdi: SK500 (4.1.42)
Gawa    = Pratipadika("Gawa",    "pum")
# ati: avyaya pūrva-pada for atyUDnI (SK485 avyayādi arm)
ati     = Pratipadika("ati",     "pum",   other_tags=["avyaya"])

# SK486 (4.1.27) test bases. ?dAman / ?hAyana let the rule target these stems;
# the saṃkhyā pūrva-pada is read via llp: ?saMKyA (and the 4.1.27.1 vārttika n→ṇ
# via llp: [=tri, =catur]). The composer still adds ?vayasi for the hāyana
# age-sense restriction.
dAman   = Pratipadika("dAman",   "napum", other_tags=["dAman"])
hAyana  = Pratipadika("hAyana",  "pum",   other_tags=["hAyana"])

# SK488 (4.1.30) केवलमामक…भेषजाच्च — nine a-final stems that take mandatory
# NIp in saṃjñā or chandas (?saMjYA / ?Candas attached via test composer). The
# class tag ?keval_Adi gates SK488. ?mAmaka separately gates the niyama-blocker
# (4.1.30.1) which suppresses SK470 (4.1.15) NIp on mAmaka outside saMjñā/chandas.
# ?ka_pratyaya on mAmaka allows the laukika ṭāp path to flow through SK463
# (7.3.44 idādeśa) giving मामिका, matching Vasu's लोकेऽसंज्ञायां मामिका.
kevala    = Pratipadika("kevala",    "pum",   other_tags=["keval_Adi"])
mAmaka    = Pratipadika("mAmaka",    "pum",   other_tags=["keval_Adi", "mAmaka",
                                                          "ka_pratyaya"])
BAgaDeya  = Pratipadika("BAgaDeya",  "pum",   other_tags=["keval_Adi"])
pApa      = Pratipadika("pApa",      "pum",   other_tags=["keval_Adi"])
apara_488 = Pratipadika("apara",     "pum",   other_tags=["keval_Adi"])
samAna    = Pratipadika("samAna",    "pum",   other_tags=["keval_Adi"])
AryakRta  = Pratipadika("AryakRta",  "pum",   other_tags=["keval_Adi"])
sumaNgala = Pratipadika("sumaNgala", "pum",   other_tags=["keval_Adi"])
Bezaja    = Pratipadika("Bezaja",    "napum", other_tags=["keval_Adi"])

# SK491 (4.1.34 विभाषा सपूर्वस्य) test base: gṛha + pati compound. pati already
# tagged ?pati (line 62); in_compound(pati) adds ?samAsa, gating SK491. Python
# var named gRha for readability; SLP1 content is "gfha" (f = ṛ) = गृह.
gRha = Pratipadika("gfha", "napum")

# SK492 (4.1.35 नित्यं सपत्न्यादिषु) sapatnyAdi gaṇa (sapati/ekapati/vīrapati) is now
# built live as pūrva + pati compounds in the test (vibhaktis_list sapatnI/ekapatnI/
# vIrapatnI); SK492 peeks the pūrva-pada identity (llp: [=sa, =eka, =vIra]) instead of
# pre-substituted ?sapatnyAdi stems. The समान→स niyama is realised by registering the
# reduced pūrva-pada `sa` (sa_pUrva, defined below). The uttara-pada `pati` supplies
# ?pati in-window so 1.4.8.1 blocks Ghi-saṃjña and 1.4.3 nadī-saṃjña applies (सपत्न्यै,
# exactly like gṛhapatnī, the compound-pati 4.1.34 case).

# SK489 (4.1.32 अन्तर्वत्पतिवतोर्नुक्) — irregular feminine stems. Treated as
# single pratipadikas (not live antar+matup / pati+matup compounds) per plan's
# Q2/engine-limitation deferral: the engine cannot peek into a samāsa's left
# context from a pratyaya-window rule. The ?antarvat_pativat class tag gates
# SK489 (adds nuk = 'n' at end of stem at bahiranga 1); SK453 (4.1.5) at
# bahiranga 2 then sees the n-final stem and supplies NIp → अन्तर्वत्नी,
# पतिवत्नी.
antarvat = Pratipadika("antarvat", "pum", other_tags=["antarvat_pativat"])
pativat  = Pratipadika("pativat",  "pum", other_tags=["antarvat_pativat"])

# ── SK493–499: feminine-affix substitution cluster (4.1.36–41 + 6.4.149) ──────
# SK493 (4.1.36 पूतक्रतोरै च): final u → ai (= SLP1 'E', udātta) + NIp. Built live
# as the compound pūta + kratu; 4.1.36 peeks the pūrva-pada (llp: =pUta) + reads the
# kratu uttara in-window (lp: =kratu). → पूतक्रतायी (E+ī → āy+ī via 6.1.78).
pUta  = Pratipadika("pUta",  "pum")   # SK493 pūrva-pada (pūtakratu)
kratu = Pratipadika("kratu", "pum")   # SK493 uttara-pada (kratu)

# SK494 (4.1.37 वृषाकप्यग्निकुसितकुसिदानामुदात्तः): same ai-substitute + NIp for these
# four. वृषाकपि is kept as a single irregular pratipadika (NOT a live compound): a live
# vṛṣā+kapi exposes (a) the ?bahvAdi optional ṅīṣ on kapi and (b) gen-pl ṇatva across the
# compound boundary (वृषाकपायीणाम्) which the single-pada stem handles for free.
# Per SK (कुसिदशब्दो ह्रस्वमध्यः), kusita/kusida have a SHORT middle i (not Vasu's कुसीद).
vfzAkapi = Pratipadika("vfzAkapi", "pum", other_tags=["vfzAkapyAdi"])
agni     = Pratipadika("agni",     "pum", other_tags=["vfzAkapyAdi"])
kusita   = Pratipadika("kusita",   "pum", other_tags=["vfzAkapyAdi"])
kusida   = Pratipadika("kusida",   "pum", other_tags=["vfzAkapyAdi"])

# SK495 (4.1.38 मनोरौ वा): final u → au (= SLP1 'O', udātta) optionally + NIp →
# मनावी (O+ī → āv+ī). The ai-variant (मनायी) and the no-substitute manuḥ branch
# are deferred.
manu = Pratipadika("manu", "pum", other_tags=["manu"])

# SK496 (4.1.39 वर्णादनुदात्तात्तोपधात्तो नः): colour words with t-upadhā →
# optional NIp + t→n. → एनी/एता, रोहिणी/रोहिता (ṇatva from r). Accent is not
# modelled; the ?varNa_topaDa tag marks the t-upadhā colour class.
eta    = Pratipadika("eta",    "pum", other_tags=["varNa_topaDa"])
rohita = Pratipadika("rohita", "pum", other_tags=["varNa_topaDa"])
Syeta  = Pratipadika("Syeta",  "pum", other_tags=["varNa_topaDa"])
harita = Pratipadika("harita", "pum", other_tags=["varNa_topaDa"])

# SK497 (4.1.40 अन्यतो ङीष्): other colour words (non-t-upadhā) → NIz (surface ī,
# same shape as NIp — accent only). → सारङ्गी, कल्माषी, शबली.
kalmAza = Pratipadika("kalmAza", "pum", other_tags=["varNa_anyatas"])
sAraNga = Pratipadika("sAraNga", "pum", other_tags=["varNa_anyatas"])
Sabala  = Pratipadika("Sabala",  "pum", other_tags=["varNa_anyatas"])

# SK498 (4.1.41 षिद्गौरादिभ्यश्च): ṣit-affixed stems and gaurādi-gaṇa stems → NIz.
# nartaka (√nṛt + ṣvun, 3.1.145) is ṣit by virtue of the ṣvun affix's ṣ it-marker.
# Rather than an ad-hoc ?zit tag, the stem carries the actual ṣ it (its=["z"]) —
# faithful, and forward-compatible: any properly ṣvun/ṣit-derived stem propagates
# its ṣ it through join_objects (1.2.46) and is picked up by SK498's `lp: +z` arm.
# gaura (SLP1 gOra) and matsya are gaurādi. → नर्तकी, गौरी, मत्सी.
nartaka = Pratipadika("nartaka", "pum", its=["z"])
gaura   = Pratipadika("gOra",    "pum",   other_tags=["gaurAdi"])
# SK499 (6.4.149): matsya additionally carries ?sUryAdi so its upadhā 'y' is
# elided before the feminine ī (ābhīya, asiddha to 6.4.148) → मत्सी.
matsya  = Pratipadika("matsya",  "pum",   other_tags=["gaurAdi", "sUryAdi"])
# sUrya and tizya: bha-aṅgas named in SK499 (6.4.149). Their upadhā 'y' is also
# elided before a taddhita affix when ?sUryAdi propagates through the taddhita
# merge (tier-3 propagation in paninian_object.join_objects). The aṇ-derivation
# (7.2.115 ādivṛddhi + affix) gives saurya/taiṣya, then 6.4.149 y-lopa gives
# saur/taiṣ, then 6.4.148 a-lopa + ī → सौरी / तैषी.
# āgastī (agastya + 4.1.114 taddhita) is deferred — it uses a different affix.
sUrya = Pratipadika("sUrya", "pum", other_tags=["sUryAdi"])
tizya = Pratipadika("tizya", "pum", other_tags=["sUryAdi"])

# gaurādi gaṇa (SK498 / 4.1.41) — the named simple members from SC Vasu's list,
# registered so the gaṇa is (largely) complete rather than representative-only.
# Excluded: the samasta/derivation-special items — matsya (above, +sūryAdi),
# gaura (above), sūrya (above, taddhita path), śvan/takṣan (n-stems registered
# elsewhere), anaḍuhī/anaḍvāhī (special feminines), āḍhaka (registered for Dvigu).
# Members already defined above in other gaṇas get ?gaurAdi added in place (śūrpa,
# yūṣa ?pādādi → शूर्पी, यूषी/यूष्णी) rather than re-registered here, to avoid
# clobbering. Each simple member → NIz → ी (nadī). Bound to module globals.
_gaurAdi_members = [
    "manuzya", "SfNga", "piNgala", "haya", "gavaya", "mukaya", "fzya", "puwa",
    "tURa", "druRa", "droRa", "hariRa", "kokaRa", "pawara", "ukaRa", "Amalaka",
    "kuvala", "bimba", "badara", "Parkaraka", "tarkAra", "SarkAra", "puzkara",
    "SiKaRqa", "salada", "SazkaRqa", "sananda", "suzama", "suzava", "alinda",
    "gaquja", "pARqaSa", "Ananda", "ASvatTa", "sfpAwa", "AKaka", "Sazkula",
    "sUca", "yUTa", "sUpa", "meTa", "vallaka", "GAtaka",
    "sallaka", "mAlaka", "mAlata", "sAlvaka", "vetasa", "vfkza", "atasa",
    "BfNga", "maha", "maWa", "Ceda", "peSa", "meda",
]
for _m in _gaurAdi_members:
    globals()[_m] = Pratipadika(_m, "pum", other_tags=["gaurAdi"])

# bahvādi gaṇa (SK503 / 4.1.45) — named simple members from SC Vasu's list,
# optional NIz (both forks). Excluded: the gaṇasūtra entries (इतः प्राप्यंगात्,
# कृदिकारादक्तिनः, सर्वतोऽक्तिन्नर्थात्), candrabhāgā (river-name, special), and the
# members that overlap ajādi / svāṅga gaṇas with different treatment (bāla, ahan,
# kroḍa, nakha, khura, śikhā, śapha, guda). bahu and vāri (?napum 'water') are
# registered above — vāri gets ?bahvAdi added in place → वारिः/वारी.
_bahvAdi_members = [
    "padDati", "aYcati", "aNkati", "aMhati", "Sakawi", "Sakti", "SAri",
    "rAti", "rADi", "SADi", "ahi", "kapi", "yazwi", "muni", "caRqa", "arAla",
    "kfpaRa", "kamala", "vikawa", "viSAla", "viSaNkawa", "Baruja", "Dvaja",
    "kalyARa", "udAra", "purARa",
]
for _m in _bahvAdi_members:
    globals()[_m] = Pratipadika(_m, "pum", other_tags=["bahvAdi"])

# ── SK500–505: ṅīṣ-selection continuation (4.1.42–45, 48, 49) ────────────────
# All select NIz (ṅīṣ — surface ī, accent not modelled) via lexical tags.

# SK500 (4.1.42 जानपदकुण्ड…कबरात्): 11 sense-restricted stems → ṅīṣ. The 11
# distinct senses (vṛtti/amatra/…) are NOT modelled — the rule fires on the tag.
# Full list registered; representative members get test tables.
jAnapada = Pratipadika("jAnapada", "pum", other_tags=["jAnapadAdi"])
# kuRqa already defined above (napum) — ?jAnapadAdi added there to avoid a
# shadowing redefinition that would break kuRqoDnI (kuṇḍodhan bahuvrīhi).
goRa     = Pratipadika("goRa",     "pum", other_tags=["jAnapadAdi"])
sTala    = Pratipadika("sTala",    "pum", other_tags=["jAnapadAdi"])
BAja     = Pratipadika("BAja",     "pum", other_tags=["jAnapadAdi"])
nAga     = Pratipadika("nAga",     "pum", other_tags=["jAnapadAdi"])
kAla     = Pratipadika("kAla",     "pum", other_tags=["jAnapadAdi"])
nIla     = Pratipadika("nIla",     "pum", other_tags=["jAnapadAdi"])
kuSa     = Pratipadika("kuSa",     "pum", other_tags=["jAnapadAdi"])
kAmuka   = Pratipadika("kAmuka",   "pum", other_tags=["jAnapadAdi"])
kabara   = Pratipadika("kabara",   "pum", other_tags=["jAnapadAdi"])

# SK501 (4.1.43 शोणात्प्राचाम्): śoṇa → optional ṅīṣ (Eastern grammarians).
SoRa = Pratipadika("SoRa", "pum", other_tags=["SoRa"])

# SK502 (4.1.44 वोतो गुणवचनात्): u-final quality word → optional ṅīṣ. skip-fork =
# plain u-stem (मृदुः). The kharu/saṃyoga-upadhā exception (पाण्डु) is deferred —
# simply not tagged. guṇavacana is an open class; representative members below.
mfdu  = Pratipadika("mfdu",  "pum", other_tags=["guRavacana"])
laGu  = Pratipadika("laGu",  "pum", other_tags=["guRavacana"])
svAdu = Pratipadika("svAdu", "pum", other_tags=["guRavacana"])

# SK503 (4.1.45 बह्वादिभ्यश्च): bahvādi gaṇa → optional ṅīṣ. skip-fork = u-stem
# (बहुः). bahu already defined above (SK462 pūrva-pada); ?bahvAdi added there.

# SK504 (4.1.48 पुंयोगादाख्यायाम्): a male-designation used of his wife → ṅīṣ.
# The puṃyoga ('wife-of') semantics are not modelled — fires on the tag.
# Vārttikas (pālakānta गोपालिका; सूर्या devatā-cāp) deferred.
gopa = Pratipadika("gopa", "pum", other_tags=["puMyoga"])

# SK505 (4.1.49 इन्द्रवरुण…आनुक्): ānuk augment (आन्) + ṅīṣ. The six proper nouns
# indra/varuṇa/bhava/śarva/rudra/mṛḍa take it in puṃyoga; hima/araṇya/yava/yavana/
# mātula/ācārya in given senses (senses deferred — fires on the tag). ṇatva then
# gives इन्द्राणी/रुद्राणी (r-stems) vs वरुणानी/हिमानी/अरण्यानी (n stays — no r/ṣ,
# or ṇ/y blocks 8.4.2). मातुल/उपाध्याय optional ānuk vārttika → मातुली deferred.
# indra already defined above (?indra for 6.1.124) — ?indrAnuk added there.
varuRa  = Pratipadika("varuRa",  "pum", other_tags=["indrAnuk"])
Bava    = Pratipadika("Bava",    "pum", other_tags=["indrAnuk"])
Sarva   = Pratipadika("Sarva",   "pum", other_tags=["indrAnuk"])
rudra   = Pratipadika("rudra",   "pum", other_tags=["indrAnuk"])
mfqa    = Pratipadika("mfqa",    "pum", other_tags=["indrAnuk"])
hima    = Pratipadika("hima",    "pum", other_tags=["indrAnuk"])
araRya  = Pratipadika("araRya",  "pum", other_tags=["indrAnuk"])
yava    = Pratipadika("yava",    "pum", other_tags=["indrAnuk"])
yavana  = Pratipadika("yavana",  "pum", other_tags=["indrAnuk"])
mAtula  = Pratipadika("mAtula",  "pum", other_tags=["indrAnuk"])
AcArya  = Pratipadika("AcArya",  "pum", other_tags=["indrAnuk"])

# ── SK517–531: remainder of 4.1.x strī-pratyaya chapter ────────────────────

# SK517 (4.1.62 सख्यशिश्वीति भाषायाम्): sakhi + aśiśvī → ṅīṣ in bhāṣā.
# saKi already defined above with ?saKi and (new) ?sakhyAdi tag. aśiśvī is
# an obscure term; only sakhi is given a test table. Semantic bhāṣā restriction
# not modelled — fires unconditionally on ?sakhyAdi.
# aziSvI stem registered for completeness (test coverage TBD):
aziSvI = Pratipadika("aziSvI", "pum", other_tags=["sakhyAdi"])

# SK518 (4.1.63 जातेरस्त्रीविषयादयोपधात्): jāti words (genus/species) that are
# (a) not exclusively stree-only and (b) not y-upadhā → ṅīṣ. Restrictions are
# encoded by NOT tagging ineligible stems. Representative a-final jāti pum stems:
brAhmaRa = Pratipadika("brAhmaRa", "pum", other_tags=["jAti_ayopaDa"])
kukkuwa   = Pratipadika("kukkuwa",  "pum", other_tags=["jAti_ayopaDa"])   # kukkuṭa (hen/cock)
sUkara    = Pratipadika("sUkara",   "pum", other_tags=["jAti_ayopaDa"])   # sūkara (pig)

# SK519 (4.1.64 पाककर्णपर्णपुष्पफलमूलवालोत्तरपदाच्च): a samāsa whose uttara is one of the
# seven pākādi words → ṅīṣ (4.1.64: lp: [and, ?samAsa, ?pAkAdi]). The seven uttara words
# carry ?pAkAdi intrinsically: pAka/parRa/puzpa/Pala/mUla/vAla, plus karRa (defined later).
# karRa is shared with the SK511 svāṅga case, so ?pAkAdi is added PER-INSTANCE on
# śaṅkukarṇa (not on the karRa base) — else tuṅgakarṇā loses its ṭāp fork. The ajādi/dvigu
# phala/puṣpa compounds (संफला/त्रिफला) are detected by $$ajAdi_samasta and take ṭāp
# (4.1.4.1/4.1.4.2 override 4.1.64).
pAka  = Pratipadika("pAka",  "napum", other_tags=["pAkAdi"])  # pāka uttara (SK519, "cooking" sense)
# pūrva-pada pieces for the SK519 jāti compounds (odana/go/sam/tri exist elsewhere):
dAsI  = Pratipadika("dAsI",  "strI")   # dāsī- pūrva (dāsīphalī)
SaNku = Pratipadika("SaNku", "pum")    # śaṅku- pūrva (śaṅkukarṇī)
SAla  = Pratipadika("SAla",  "pum")    # śāla- pūrva (śālaparṇī)
SaNKa = Pratipadika("SaNKa", "pum")    # śaṅkha- pūrva (śaṅkhapuṣpī)
darBa = Pratipadika("darBa", "pum")    # darbha- pūrva (darbhamūlī)
Bastra = Pratipadika("Bastra", "napum")  # bhastra- pūrva (bhastraphalā, a non-dvigu samāsa-ajādi)
parRa = Pratipadika("parRa", "napum", other_tags=["pAkAdi"])  # parṇa uttara (SK519)
puzpa = Pratipadika("puzpa", "napum", other_tags=["pAkAdi"])  # puṣpa uttara (SK519)
mUla  = Pratipadika("mUla",  "napum", other_tags=["pAkAdi"])  # mūla uttara (SK519)
vAla  = Pratipadika("vAla",  "napum", other_tags=["pAkAdi"])  # vāla uttara (SK519)

# SK520 (4.1.65 इतो मनुष्यजातेः): i-final manuṣya-jāti (racial/regional words for
# human groups) → ṅīṣ. Vasu examples: avantī (women of Avanti), kuntī, plākṣī.
# The anuvrṛtti of ayopadhā also applies: not y-upadhā (avanti has 't' penult,
# kunti has 't' penult — safe). Semantic "human jāti" restriction deferred; fires
# on ?mAnuzya_jAti_i tag.
avanti = Pratipadika("avanti", "pum", other_tags=["mAnuzya_jAti_i"])  # → avantī
kunti  = Pratipadika("kunti",  "pum", other_tags=["mAnuzya_jAti_i"])  # → kuntī
# plākṣī: plākṣa + iñ taddhita (ādivṛddhi: a→ā) → plākṣi (i-final). SK520 fires
# on the i-final form. SLP1 "plAkzi" = p+l+A+k+z+i (z=ṣ).
plAkzi = Pratipadika("plAkzi", "pum", other_tags=["mAnuzya_jAti_i"])  # → plākṣī

# SK521 (4.1.66 ऊङुतः): u-final, non-y-upadhā manuṣya-jāti → ūṅ (UN suffix).
# Condition: l: ut (short u, not ū — isSavarna('ut','U')=False). Vasu examples:
# kurūḥ (women of Kuru), brahmabandhūḥ. kuru already defined above (line ~91)
# without manuṣya-jāti tag; add ?manuzya_jAti_u tag there.
# (kuru at line ~91 will be patched to add ?manuzya_jAti_u)
brahmabanDU = Pratipadika("brahmabanDU", "pum", other_tags=["manuzya_jAti_u"])  # → brahmabandhūḥ (D=dh)

# SK522 (4.1.67 बाह्वन्तात्संज्ञायाम्): bāhu-final prātipadika + saṃjñā → ūṅ.
# Example: bhadrabāhūḥ. Register bhadrabAhu directly; saṃjñā restriction deferred.
BadrabAhu = Pratipadika("BadrabAhu", "pum", other_tags=["bAhvanta_saMjYA"])

# SK523 (4.1.68 पङ्गोश्च): paṅgu (lame) → ūṅ; also śvaśrūḥ (mother-in-law)
# from vārttika (श्वशुरस्योकाराकारलोपश्च — drops u/ā of śvaśura, adds ūṅ).
# paṅgu itself takes ūṅ via SK523. śvaśrū is pre-registered (the phonological
# derivation is irregular and needs a separate vārttika mechanism).
paNgu  = Pratipadika("paNgu",  "pum", other_tags=["paNgu_class"])  # → pāṅgūḥ
SvaSrU = Pratipadika("SvaSrU", "strI")                             # → श्वश्रूः (pre-registered; S=ś, not z=ṣ)

# SK524 (4.1.69 ऊरूत्तरपदादौपम्ये): upamāna-first compound ending in ūru → ūṅ.
# Example: karaBoru = karabha (camel foreleg) + ūru → "she with carabha-like thighs".
karaBoru = Pratipadika("karaBoru", "pum", other_tags=["Uru_upamAna"])  # → karaBorUḥ

# SK525 (4.1.70 संहितशफलक्षणवामादेश्च): saṃhita/śapha/lakṣaṇa/vāma + ūru → ūṅ. Built
# live as [as_purva_pada(<pūrva>), luk_sup, in_compound(Uru), strI_abs]; 4.1.70 peeks
# the pūrva-pada identity (llp: [=saMhita, =SaPa, =lakzaRa, =vAma]) and reads the ūru
# uttara-pada in-window (lp: ?Uru_uttara). a+ū → o at the junction (6.1.87 AdguṇaH).
saMhita = Pratipadika("saMhita", "pum")   # SK525 pūrva-pada (saṃhitorū)
SaPa    = Pratipadika("SaPa",    "pum")   # SK525 pūrva-pada (śaphorū)
lakzaRa = Pratipadika("lakzaRa", "pum")   # SK525 pūrva-pada (lakṣaṇorū)
vAma    = Pratipadika("vAma",    "pum")   # SK525 pūrva-pada (vāmorū)

# SK526 (4.1.72 संज्ञायाम्): kadrū + kamaṇḍalu in proper-name (saṃjñā) use → ūṅ.
# Pre-registered as strI (they are the canonical ū-final feminine forms).
# saṃjñā restriction deferred — fires unconditionally on ?kadrU_saMjYA.
kadrU     = Pratipadika("kadrU",     "strI", other_tags=["kadrU_saMjYA"])
kamaRqalU = Pratipadika("kamaRqalU", "strI", other_tags=["kadrU_saMjYA"])  # R=ṇ, q=ḍ

# SK527 (4.1.73 शार्ङ्गरवाद्यञो ङीन्): śārṅgaravādi gaṇa + añ-derived stems → ṅīn
# (NIn). Full named gaṇa registered with ?zANgaravAdi (the post-aṇ/añ forms; the
# taddhita derivation itself is pre-applied). Per Vasu the 6 members are:
# 1 śārṅgarava, 2 kāpaṭava, 3 gauggulava, 4 brāhmaṇa, 5 baida, 6 gautama
# (+ the gaṇasūtra नृनरयोर्वृद्धिश्च for nṛ/nara → nārī, modelled separately below).
# brāhmaṇa is already registered above (line ~263) tagged ?jAti_ayopaDa for SK518;
# it surfaces as ब्राह्मणी either way (ṅīṣ vs ṅīn differ only in accent), so it is
# not re-tagged here. The 2nd arm of 4.1.73 (any añ-ending jāti word → ṅīn) is
# covered for these tagged stems but not as a general structural rule.
SArNgarava = Pratipadika("SArNgarava", "pum", other_tags=["zANgaravAdi"])  # → śārṅgaravī
kApawava   = Pratipadika("kApawava",   "pum", other_tags=["zANgaravAdi"])  # → kāpaṭavī
gOggulava  = Pratipadika("gOggulava",  "pum", other_tags=["zANgaravAdi"])  # → gauggulavī
bEda       = Pratipadika("bEda",       "pum", other_tags=["zANgaravAdi"])  # → baidī (añ-derived; SLP1 E=ai)
gOtama     = Pratipadika("gOtama",     "pum", other_tags=["zANgaravAdi"])  # → gautamī (4.1.114 aṇ)
# nārī (gaṇasūtra नृनरयोर्वृद्धिश्च: nṛ/nara, a śārṅgaravādi member, gets vṛddhi +
# ṅīn). Modelled accurately as the live derivation [nara, aR_t, strI_abs]: aṇ
# supplies the ādivṛddhi (7.2.117: nara → nāra) that the gaṇasūtra calls for, and
# the feminine ī comes via the taddhita-ṅīp path (aR_t is ?NIp_taddhita → SK470),
# which is surface-identical to the gaṇasūtra ṅīn → नारी (nadī decl, नारीणाम् ṇatva).
nara = Pratipadika("nara", "pum")  # → नारी via [nara, aR_t, strI_abs] (see test table)

# SK528 (4.1.74 यङश्चाप्): yañ/ṣyañ-derived a-final stems → cAp. Pre-registered as
# POST-ṣyañ forms (ādivṛddhi + ya already applied; ṣyañ derivation not yet modelled).
# ?yaNzdavya tag triggers SK528 cAp selection. Surface = ā-final (same as ṭāp now).
# SLP1: āmbaṣṭhya = "AmbazWya" (ā+m+b+a+ṣ(z)+ṭh(W)+y+a, z=ṣ, W=ṭh).
# kārīṣagandhya = "kArIzaganDya" (k+ā+r+ī+ṣ(z)+a+g+a+n+dh(D)+y+a, D=dh).
AmbazWya     = Pratipadika("AmbazWya",     "pum", other_tags=["yaNzdavya"])  # → āmbaṣṭhyā
kArIzaganDya = Pratipadika("kArIzaganDya", "pum", other_tags=["yaNzdavya"])  # → kārīṣagandhyā

# SK529 (4.1.75 आवट्याच्च): āvaṭya (from avata, gargādi; ñyaṅ-derived) → cAp.
# SLP1: āvaṭya = "Avawya" (ā+v+a+ṭ(w)+y+a, w=ṭ). ?AvawI tag for SK529 YAML.
Avawya = Pratipadika("Avawya", "pum", other_tags=["AvawI"])  # → āvaṭyā

# SK531 (4.1.77 यूनस्तिः): yuvan + ti (taddhita) → yuvatī. yuvan already defined.
# The derived prātipadika "yuvati" is also registered directly for test coverage;
# see implementation notes in the plan.

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
himavat = Pratipadika("himavat", "pum", its=['u'])  # himavat (hima + matup): pañcamī sg हिमवतः — हिमवतो गङ्गा प्रभवति (SK594 1.4.31)

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
jawA = Pratipadika("jawA", "strI", other_tags=["Ap"])   # जटा — जटाभिस्तापसः (SK566; inst. pl. जटाभिः)
gaNgA = Pratipadika("gaNgA", "strI", other_tags=["Ap"])   # गङ्गा — हिमवतो गङ्गा प्रभवति (SK594 1.4.31; प्रथमा गङ्गा)
# SK293 (7.3.115): dvitīyā and tṛtīyā optionally get syāw (like sarvanāma āp) before ṅ-marked suffixes.
# Used as [dvitIya, Ap] / [tftIya, Ap] in test fixtures (same pattern as [sarva, Ap] for sarva_A).
dvitIya = Pratipadika("dvitIya", "pum", other_tags=["dvitIyAdi"])
tftIya  = Pratipadika("tftIya",  "pum", other_tags=["dvitIyAdi"])
nadI = Pratipadika("nadI", "strI", other_tags=["NI"])
kalyARI = Pratipadika("kalyARI", "strI", other_tags=["NI"])  # कल्याणी — मासं कल्याणी (SK558; ī-stem like nadI)
niSA = Pratipadika("niSA", "strI", other_tags=["pAdAdi", "Ap"])
nAsikA = Pratipadika("nAsikA", "strI", other_tags=["pAdAdi", "Ap"])
tuNga = Pratipadika("tuNga", "pum")   # adj. "prominent/high"; pūrva-pada for SK511 tuNgakarRA
karRa = Pratipadika("karRa", "napum")  # "ear" (svāṅga a-stem); SK511 uttara-pada

# ── SK506–515: svāṅga / compound strī cluster (4.1.50–60), via llp/lp peeking ──
# svāṅga (body-part) uttara-padas — ?svAnga tags the 4-part-definition members.
# Used as in_compound(...) uttara-padas (carry ?samAsa at the strī window).
keSa  = Pratipadika("keSa",  "napum", other_tags=["svAnga"])   # hair (SK510 अतिकेशी; SK513 सकेशा)
muKa  = Pratipadika("muKa",  "napum", other_tags=["svAnga"])   # face (SK510 चन्द्रमुखी; SK514 गौरमुखा; SK515 प्राङ्मुखी)
jaGana = Pratipadika("jaGana", "napum", other_tags=["svAnga"])  # hip (SK512 सुजघना — bahvac svāṅga)
kroqa = Pratipadika("kroqa", "pum",   other_tags=["svAnga", "kroqAdi"])  # chest (SK512 कल्याणक्रोडा — kroḍādi)
gulPa = Pratipadika("gulPa", "pum",   other_tags=["svAnga"])   # ankle (SK510 counter सुगुल्फा — saṃyoga-upadhā)
naKa  = Pratipadika("naKa",  "pum")   # nail (SK514 शूर्पणखा — saṃjñā niṣedha; not ?svAnga-needed)
# kta-final (niṣṭhā) uttara-padas (SK506/507):
krIta = Pratipadika("krIta", "pum", other_tags=["ktAnta"])     # bought (SK506 वस्त्रक्रीती)
lipta = Pratipadika("lipta", "pum", other_tags=["ktAnta"])     # smeared (SK507 अभ्रलिप्ती)
# karaṇa pūrva-padas (name the means) (SK506/507):
vastra = Pratipadika("vastra", "napum", other_tags=["karaNa"])  # cloth
aBra   = Pratipadika("aBra",   "napum", other_tags=["karaNa"])  # cloud
# misc pūrva-padas: candra (SK510), su/saha (SK512/513), ati (exists), Sūrpa (exists),
# gOra (exists), tAmra (SK514 counter), vidyamAna (SK513). The SK515 dik pūrva-pada
# प्राच् is NOT pre-formed — derived live in the test as
# [pra, luk_sup, in_context(aYc_u,"dik"), kvin, luk_sup] (the prAc añc-paradigm).
candra = Pratipadika("candra", "pum")    # moon (SK510 चन्द्रमुखी pūrva)
sa_pUrva = Pratipadika("sa", "pum")      # saha→sa (SK513 सकेशा pūrva; SK492 सपत्नी pūrva)
eka_pUrva = Pratipadika("eka", "pum")    # SK492 एकपत्नी pūrva (eka+pati)
vIra_pUrva = Pratipadika("vIra", "pum")  # SK492 वीरपत्नी pūrva (vīra+pati)
su_pUrva = Pratipadika("su", "pum")      # su- (SK510 ctr सुगुल्फा; SK512 सुजघना)
tAmra  = Pratipadika("tAmra", "pum")     # copper (SK514 counter ताम्रमुखी — non-saṃjñā)
vidyamAna = Pratipadika("vidyamAna", "pum")  # existing (SK513 विद्यमाननासिका pūrva)
mati = Pratipadika("mati", "strI")
Bakti = Pratipadika("Bakti", "strI")   # भक्ति f. (short-i, like mati) — हरये रोचते भक्तिः (SK571; bhakti = kartṛ → prathamā भक्तिः)
lakzmI = Pratipadika("lakzmI", "strI")  # No NI
strI = Pratipadika("strI", "strI", other_tags=["NI", "strI_p"])
SrI = Pratipadika("SrI", "strI", other_tags=["DAtu", "kvip"])
kumArI =  Pratipadika("kumArI", "strI", other_tags=["NI"])

# to test
Denu = Pratipadika("Denu", "strI")
suBrU = Pratipadika("suBrU", "strI", other_tags=["BrU"])


# Napum

jYAna = Pratipadika("jYAna", "napum")
tfRa = Pratipadika("tfRa", "napum")   # तृण — तृणं स्पृशति (SK538 anīpsita-karma)
Dana = Pratipadika("Dana", "napum")   # धन — धनेन कुलम् (SK568 hetu; धनेन तृतीया)
kula = Pratipadika("kula", "napum")   # कुल — धनेन कुलम् (SK568; कुलम् prathamā)
Sata = Pratipadika("Sata", "napum")   # शत — देवदत्ताय शतं धारयति (SK573; शतम् the debt = karma)
# Kāraka Phase K5 napuṃsaka a-stems (apādāna + pañcamī; SK586–605).
aDyayana = Pratipadika("aDyayana", "napum")  # अध्ययन — अध्ययनात्पराजयते (SK589 1.4.26 asoḍha → apādāna)
jAqya    = Pratipadika("jAqya",    "napum")  # जाड्य — जाड्याज्जाड्येन वा (SK602 2.3.25 guṇa-hetu vibhāṣā)
stoka    = Pratipadika("stoka",    "napum")  # स्तोक — स्तोकात्/स्तोकेन मुक्तः (SK604 2.3.33 karaṇa vibhāṣā)
dUra     = Pratipadika("dUra",     "napum")  # दूर — दूरं दूरात् दूरेण वा (SK605 2.3.35 three-way fork)
antika   = Pratipadika("antika",   "napum")  # अन्तिक — अन्तिकम् अन्तिकात् अन्तिकेन वा (SK605)
# नमस् n. — नमो देवेभ्यः (SK583 2.3.16). Modelled as the neuter s-stem noun (its
# true category) so it surfaces नमः via normal nom-sg s-stem declension; 2.3.16
# reads it as the yoga-word by the literal =namas. (Not an avyaya: the bare
# avyaya would surface नमस् with no visarga.)
namas = Pratipadika("namas", "napum")
anya = Pratipadika("anya", "napum", other_tags=["qatarAdi", "sarvanAma"])
anyatara = Pratipadika("anyatara", "napum", other_tags=["qatarAdi", "sarvanAma"])
itara = Pratipadika("itara", "napum", other_tags=["qatarAdi", "sarvanAma"])
# dik-śabdas (पूर्व/उत्तर… — pūrvādi sarvanāma, 1.1.34) used as 2.3.29 yoga-words
# (अन्यारादितरर्ते-दिक्शब्द…): पूर्वो ग्रामात्. Tagged dikSabda so the rule matches the
# whole dik-word class rather than a single literal.
pUrva_dik = Pratipadika("pUrva", "pum", other_tags=["dikSabda", "sarvanAma"])
uttara_dik = Pratipadika("uttara", "pum", other_tags=["dikSabda", "sarvanAma"])
# prasita / utsuka ("intent on / eager for") — the 2.3.44 yoga-adjectives. The
# object they govern → tṛtīyā (vibhāṣā, च saptamī). Tagged prasitotsuka so the
# rule peeks them via llp/rrp; they themselves take their own (prathamā) form.
prasita = Pratipadika("prasita", "pum", other_tags=["prasitotsuka"])
utsuka = Pratipadika("utsuka", "pum", other_tags=["prasitotsuka"])
qatara = Pratipadika("qatara", "napum", other_tags=["qatarAdi", "sarvanAma"])
qatama = Pratipadika("qatama", "napum", other_tags=["qatarAdi", "sarvanAma"])
vAri = Pratipadika("vAri", "napum", other_tags=["bahvAdi"])  # bahvādi #9 (SK503) → वारिः / वारी
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
# yuj_kvin_samAsa (preformed compound-yuj) retired: the proper-samāsa aSvayuj
# [aSva, in_compound(yuj_kvin)] covers SK376's ?samAsa nUM-block path live.
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

# udañc (m.) is derived as a compound [ud, su, aYc_u, kvin] — see test/vibhaktis_list.py
# and ui/app.py (_udac_cpd). SK420 (6.4.139) reads the ud prefix via the llp neighbour,
# so no monolithic udac_kvin pratipadika / udanc tag is needed.

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
# SK460/SK461 an-final bahuvrīhi: built live as a compound (bahu + yajvan) in the test
# (vibhaktis_list bahuyajvan_strI). The preformed bahuyajvan stem is retired; yajvan
# carries ?van so SK456 (4.1.7) competes and SK460 overrides it.

# SK443 (8.2.68 ahan n→ru at pada-end): apavāda of 8.2.7 (n-lopa).
# Nom/acc/voc sg: ahan → n→r (ru) → visarga → ahaḥ.
# Bha forms (vowel-initial non-sarvānāmasthāna): existing 6.4.134 a-lopa → ahn-.
# Consonant-initial (bhyAm etc.): ru+voiced → 6.1.114 r-drops, u inserted → aho-.
ahan = Pratipadika("ahan", "napum", other_tags=["ahan"])
yajvan = Pratipadika("yajvan", "pum", other_tags=["yajvan", "van"])  # ?van → SK456 (4.1.7) competitor in bahuyajvan, overridden by SK460

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
SUrpa = Pratipadika("SUrpa", "pum", other_tags=["gaurAdi"])   # śūrpa (winnowing basket), m. a-stem; gaurādi #42 (SK498) → शूर्पी
naKI  = Pratipadika("naKI",  "strI", other_tags=["NI"])  # naḳī (basket-maker's wife), f. ī-stem

# Positive test: kṣīra (milk) + monosyllabic uttara-pada with n → ṇatva via SK307
kzIra = Pratipadika("kzIra", "napum")  # kṣīra (milk), neuter a-stem
pa = Pratipadika("pa", "napum")  # monosyllabic uttara-pada (pā = hand); ?samAsa comes via in_compound

# ── ajādi gaṇa (SK454 / 4.1.4) — all 34 members ──────────────────────────────────────
# Items 1–27, 31–34 end in short 'a' → TAp via l:at (ajAdi tag redundant but correct).
# Items 28–30 end in consonants → TAp via ?ajAdi condition specifically.
# Source: Vasu commentary on 4.1.4.
# Items 1–6 are jāti (kind/species) words, non-y-upadhā → they would take ṅīṣ by
# 4.1.63 (SK518) but for ajādi. Tagged ?jAti_ayopaDa (faithful), so 4.1.4.1's
# prabalatva (which now overrides 4.1.63) gives ṭāp — कोकिला, not कोकिली.
aja           = Pratipadika("aja",           "pum", other_tags=["ajAdi", "jAti_ayopaDa"])  #  1 अज   (he-goat)
eqaka         = Pratipadika("eqaka",         "pum", other_tags=["ajAdi", "jAti_ayopaDa"])  #  2 एडक  (sheep)
kokila        = Pratipadika("kokila",        "pum", other_tags=["ajAdi", "jAti_ayopaDa"])  #  3 कोकिल (cuckoo)
cawaka        = Pratipadika("cawaka",        "pum", other_tags=["ajAdi", "jAti_ayopaDa"])  #  4 चटक  (sparrow)
aSva          = Pratipadika("aSva",          "pum", other_tags=["ajAdi", "jAti_ayopaDa"])  #  5 अश्व  (horse)
mUzika        = Pratipadika("mUzika",        "pum", other_tags=["ajAdi", "jAti_ayopaDa"])  #  6 मूषिक (mouse)
bAla          = Pratipadika("bAla",          "pum", other_tags=["ajAdi"])  #  7 बाल  (young/child)
hoqa          = Pratipadika("hoqa",          "pum", other_tags=["ajAdi"])  #  8 होड  (young)
pAka_young    = Pratipadika("pAka",          "pum", other_tags=["ajAdi"])  #  9 पाक  (young; simple ajādi word — distinct from the SK519 pāka uttara above)
vatsa         = Pratipadika("vatsa",         "pum", other_tags=["ajAdi"])  # 10 वत्स (calf)
manda         = Pratipadika("manda",         "pum", other_tags=["ajAdi"])  # 11 मन्द (slow)
vilAta        = Pratipadika("vilAta",        "pum", other_tags=["ajAdi"])  # 12 विलात (foreigner)
# The COMPOUND ajādi-gaṇa members (items 13–14 lyuṬ pūrvāpaharaṇa/aparāpaharaṇa,
# 15–26 phala/puṣpa, 30 देवविश्, 34 अमूल) are no longer baked as preformed stems:
# they are detected structurally by $$ajAdi_samasta on the (pūrva, uttara) canonical
# pair (paribhasha._AJADI_SAMASTA), and the uttara reuses the clean ?pAkAdi base above
# (Pala/puzpa/mUla). 4.1.4.1/4.1.4.2 gain a samāsa arm that fires on the helper → संफला,
# त्रिफला. Only the simple-word ajādi members keep the ?ajAdi tag here.
SUdra         = Pratipadika("SUdra",        "pum", other_tags=["ajAdi"])  # 27 शूद्र
kruYc         = Pratipadika("kruYc",        "pum", other_tags=["ajAdi"])  # 28 क्रुञ्च् (consonant-final)
uzRih         = Pratipadika("uzRih",        "pum", other_tags=["ajAdi"])  # 29 उष्णिह् (consonant-final)
jyezWa        = Pratipadika("jyezWa",       "pum", other_tags=["ajAdi"])  # 31 ज्येष्ठ (eldest)
kanizWa       = Pratipadika("kanizWa",      "pum", other_tags=["ajAdi"])  # 32 कनिष्ठ (youngest)
maDyama       = Pratipadika("maDyama",      "pum", other_tags=["ajAdi"])  # 33 मध्यम (middle)
# ──────────────────────────────────────────────────────────────────────────────────────

# ── Kāraka Phase K6 (karaka_plan.md §K6): ṣaṣṭhī-chapter stems ────────────────
# Plain participant stems for the ṣaṣṭhī test sentences (decline through the
# existing ajanta/halanta phonology — verified). The kṛd-yoga governors carry
# a kṛt-TYPE tag which the kṛd-yoga rules (SK623/625/626/629 + the SK627/628
# pratiṣedha guards) read off the *physical neighbour* via llp/rrp. Distinct
# names so they never collide with the real pratyaya tags kta/tfn:
#   - kft          : generic kṛt (2.3.65 kartṛ-karmaṇoḥ kṛti)
#   - kta_vartamAna: kta in the present sense (2.3.67)
#   - kta_aDikaraRa: kta naming the adhikaraṇa/bhāva (2.3.68)
#   - kftya        : a kṛtya pratyaya (2.3.71)
#   - kft_aSazWI   : prohibition marker (2.3.69/70 members — laT-ādeśa/avyaya/
#                    niṣṭhā/khalartha/tṛn, future-aka, ādhamarṇya-in). A
#                    prohibited governor IS a kṛt (carries kft too) but the
#                    ?!kft_aSazWI guard on 2.3.65 keeps the ṣaṣṭhī off.
# The kṛt DERIVATION itself is deferred (karaka_plan.md §6): these enter as
# pre-formed kṛdanta nouns the way the verb enters as a pre-formed tiṅanta pada.
anna   = Pratipadika("anna",   "napum")            # अन्न n. "food" — SK607 अन्नस्य हेतोर्वसति
cOra   = Pratipadika("cOra",   "pum")              # चौर m. "thief" — SK615/617 रुज/हिंसा karman
CAga   = Pratipadika("CAga",   "pum")              # छाग m. "goat" — SK621 छागस्य हविषः
havis  = Pratipadika("havis",  "napum", other_tags=["AdeSa_s"])  # हविस् n. "oblation" — SK621 हविषः
tulya  = Pratipadika("tulya",  "pum")              # तुल्य "equal" — SK630 tulyārtha peek-word
Ayuzya = Pratipadika("Ayuzya", "napum")            # आयुष्य n. "long-life (blessing)" — SK631 āśis peek-word

# kṛd-yoga governor nouns (pre-formed kṛdantas, kṛt derivation deferred):
kfti   = Pratipadika("kfti",   "strI", other_tags=["kft"])              # कृति f. (ktin) "the doing" — SK623 हरेः कृतिः
pAcaka = Pratipadika("pAcaka", "pum",  other_tags=["kft"])              # पाचक m. (ṇvul, aka) "cook" — SK623 ओदनस्य पाचकः
kartf  = Pratipadika("kartf",  "pum",  other_tags=["kft"])              # कर्तृ m. (tṛc) "doer" — SK623 हरेः कर्ता (tṛc ≠ tṛn → ṣaṣṭhī allowed)
mata   = Pratipadika("mata",   "pum",  other_tags=["kta_vartamAna"])   # मत m. (kta, vartamāna) "esteemed" — SK625 राज्ञां मतः (kta is niṣṭhā → NOT kft; 2.3.67 re-permits the present-sense ṣaṣṭhī)
Asita  = Pratipadika("Asita",  "napum", other_tags=["kta_aDikaraRa"])  # आसित n. (kta, adhikaraṇa/bhāva) "sitting" — SK626 एतेषामासितम् (2.3.68 owns it, not 2.3.65)
GAtuka = Pratipadika("GAtuka", "pum",  other_tags=["kft", "kft_aSazWI"])  # घातुक m. (ukañ, bhaviṣyat) "slayer" — SK627/628 prohibition
gAmin  = Pratipadika("gAmin",  "pum",  other_tags=["kft", "kft_aSazWI"])  # गामिन् m. (ṇini, future/ādhamarṇya) "goer" — SK628 prohibition व्रजं गामी
sevya  = Pratipadika("sevya",  "pum",  other_tags=["kftya"])           # सेव्य m. (yat/kṛtya) "to-be-served" — SK629 मया/मम वा सेव्यो हरिः (kftya only, NOT kft — 2.3.71 owns it, not 2.3.65)
# ──────────────────────────────────────────────────────────────────────────────────────
