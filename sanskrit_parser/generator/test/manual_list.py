# flake8: noqa
from sanskrit_parser.generator.pratyaya import *
from sanskrit_parser.generator.dhatu import *
from sanskrit_parser.generator.pratipadika import *
from sanskrit_parser.generator.avyaya import *

test_list_slp1 = [
    ("kArt*", "tikaH", ["kArtikaH", "kArttikaH"]),
    ("gaRa", "upadeSaH", "gaRopadeSaH"),
    ("rAma", "eti", "rAmEti"),
    ("rAma", "iti", "rAmeti"),
    ("tyaktvA", "uttizWa", "tyaktvottizWa"),
    ("tava", "ozTaH", ["tavOzTaH", "taozTaH"]),  # SK406 optional te: tava→te, e+o→taozTaH (6.1.78+8.3.19)
    ("deva", "fzi", "devarzi"),
    ("gavi", "asmAkam", "gavyasmAkam"),
    ("kavI", "etau", "kavyetau"),
    ("camU", "ASraya", "camvASraya"),
    ("gavi", "iha", "gavIha"),
    ("kavI", "iha", "kavIha"),
    ("kavO", "asmAkam", "kavAvasmAkam"),
    ("AgacCa", "atra", "AgacCAtra"),
    ("yAne", "eti", "yAnaeti"),
    ("yAne", "atra", "yAnetra"),
    ("yAne", "AgacCati", "yAnaAgacCati"),
    ("vizRo", "ava", "vizRova"),
    ("haras", "Sete", ['haraHSete', 'haraSSete']),
    ("Bavat", "caraRam", "BavaccaraRam"),
    # Non pada
    ("praS*", "nas", "praSnas"),
    ("rAmas", "zazQa", ["rAmazzazQa", 'rAmaHzazQa']),
    ("rAmas", "wIkate", "rAmazwIkate"),
    ("sarpiz*", "tamam", "sarpizwamam"),
    ("marut", "wIkate", "maruwwIkate"),
    ("SuBam", "karoti", ["SuBaNkaroti", "SuBaMkaroti"]),
    ("vAk", "arTO", "vAgarTO"),
    ("goDuk", "awati", "goDugawati"),
    ("goDuk", "girati", "goDuggirati"),
    ("virAw", "vadati", "virAqvadati"),
    ("kavis", "asti", "kavirasti"),
    ("havis", "vartate", ["havirvartate", "havirvvartate"]),
    ("brah*", "mA", ["brahmA", "brahmmA"]),
    ((mud, Ric), Sap, tip, "modayati"),
    (BU, Sap, tip, "Bavati"),
    (ava_upasarga, (AN_upasarga, "ihi"), "avehi"), # 6.1.95
    ("SivAya", "om", "SivAyom"), # 6.1.95
    (kavi, O, "kavI"),
    (catur, Am, avasAna, ['caturRAm .', 'caturRnAm .']), #8.4.1
    ("BavAn", "liKati", "BavAl~liKati"), #8.4.60 .1
    ("dviz*", sip, "dvekzi"), #8.2.41
    ("Dvas*", kta, "Dvasta"),
    ("sras*", kta, "srasta"),
    (duh, kta, "dugDa"),
    # SK87/SK88/SK89 — go-stem sandhi
    (go, luk_sup, "agram", ["gavAgram", "gogram", "goagram"]),  # SK87 optional: gav+agra vs go+agra
    (go, luk_sup, "odanam", ["gavOdanam", "gavodanam"]),  # SK87/SK88 optional: o+o→O or av+o→av
    (go, luk_sup, indra, su, "gavendras"),  # SK89 mandatory: avaN before indra
    ]

test_list_devanagari = [
    ("मरुत्", "टीकते", "मरुट्टीकते"),
    ("मधुलिट्", "तरति", "मधुलिट्तरति"),
    ("मरुत्", "षष्ठः", "मरुत्षष्ठः"),
    ("सन्", "षष्ठः", "सन्षष्ठः"),
    ("षण्", "नाम्", "षण्णाम्"),
    ("वाग्", "मुखम्", ["वाङ्मुखम्", "वाग् मुखम्"]),
     ("षड्", "मुखम्", ["षण्मुखम्", "षड्मुखम्"]),
     ("एतद्", "मुरारि", ["एतद् मुरारि", "एतन्मुरारि"]),
     ("त्रिष्टुब्", "नमति", ["त्रिष्टुम्नमति", "त्रिष्टुब् नमति"]),
     ("वाग्", "चलति", "वाक्चलति"),
     ("त्रिष्टुब्", "छन्दः", "त्रिष्टुप्छन्दः"),
     ("अस्", "ति", "अस्ति"),
     ("तत्", "लीनः", "तल्लीनः"),
     ("प्रत्यङ्", "आत्मा", "प्रत्यङ्ङात्मा"),
     ("सुगण्", "ईशः", "सुगण्णीशः"),
     ("अस्मिन्", "एव", "अस्मिन्नेव"),
     ("वाग्", "हरि", ["वाग्घरि", "वाग् हरि"]),
#     ("अज्*", "हलौ", ["अज्झलौ", "अज् हलौ"]),
     ("मधुलिड्", "हसति", ["मधुलिड्ढसति", "मधुलिड्हसति"]),
     ("तद्", "हितम्", ["तद्धितम्", "तद्हितम्"]),
     ("त्रिष्टुब्", "हि", ["त्रिष्टुब्हि", "त्रिष्टुब्भि"]),
     ("तद्", "शेते", ["तच्शेते", "तच्छेते"]),
     ("मधुलिड्", "शेते", ['मधुलिट्शेते', "मधुलिट्छेते"]),
     ("त्रिष्टुब्", "शेते", ["त्रिष्टुप्शेते", "त्रिष्टुप्छेते"]),
     ("तद्", "श्लोकेन", ["तच्श्लोकेन", "तच्छ्लोकेन"]),
     ("तत्", "जयते", "तज्जयते"),
     ("रामः", "तरति", "रामस्तरति"),
     ("बालः", "थूकरोति", "बालस्थूकरोति"),
     ("हरिः", "चलति", "हरिश्चलति"),
     ("पयः", "क्षीरम्", "पयःक्षीरम्"),
     ("कः", "त्सरुः", "कःत्सरुः"),
     ("हरिस्", "शेते", ["हरिश्शेते", "हरिःशेते"]),
     ("रामस्", "कः", "रामःकः"),
     ("रामस्", "खनति", "रामःखनति"),
     ("रामस्", "पातुः", "रामःपातुः"),
     ("वृक्षस्", "फलतु", "वृक्षःफलतु"),
     ("रामस्", "अस्ति", "रामोस्ति"),
    (("राम", su), (as_dhatu, tip), "रामोस्ति"),
    ("रामस्", "गच्छति", "रामोगच्छति"),
    ('भोस्',  'देवाः', "भोदेवाः"),
    ('भगोस्',  'मनुष्याः', "भगोमनुष्याः"),
    ('अघोस्',  'राक्षसाः', "अघोराक्षसाः"),
    ('देवास्',  'गच्छन्ति', "देवागच्छन्ति"),
    ("रामस्", "आसीत्", "राम आसीत्"),
    ("रामस्", "ईशः", "रामईशः"),
    ("भवान्", "चरति", ["भवांश्चरति", "भवाँश्चरति"]),
    ("सन्", "शम्भुः", ["सञ्च्छम्भुः", 'सञ्शम्भुः', 'सञ्च्शम्भुः']),
    ("स्व", "छाया", "स्वच्छाया"),
    (AN_upasarga, "छाया", "आच्छाया"),
    (AN_upasarga, ((Cad, Ric), Sap, tip), "आच्छादयति"),
#    (AN, "छादयति", "आच्छादयति"),
    (mAN_upasarga, "छिदत्", "माच्छिदत्"),
    ("सा", "छाया", ["साच्छाया", "साछाया"]),
    ("कार्*", "यम्", ["कार्य्यम्", "कार्यम्"]),
    ("आदित्य्", "य", ["आदित्य", "आदित्य्य"]),
    ("गो*", yat_t, "गव्य"),  
    ("नौ*", yat_t, "नाव्य"),  
    ("भू*", GaY, "भाव"),
    ("कृ*", Ric, "कारि"),
    ("औपगु*", aR_t, "औपगव"),
    ("बभ्रु*", yaY_t, "बाभ्रव्य"),
    ("नी*", tfc, "नेतृ"),
    ("भू*", Sap, "भव"),
    ("दोघ्*", "धुम्", "दोग्धुम्"),
    ("विद्वान्स्", "अपठत्", "विद्वानपठत्"),
    ("अपठन्त्", "बालकाः", "अपठन्बालकाः"), 
    (lUY, Ryat, "लाव्य"),
    (kzI, yat, ["क्षेय", "क्षय्य"]),
    (ji, yat, ["जेय", "जय्य"]),
    (qukrIY, yat, ["क्रेय", "क्रय्य"]),
     # FIXME - can't test this now
    # आ + वेञ् + यक् + त = ओयते
    ("आ", (veY_smp, yak), "ओय"),
    ("प्र", (eDa, Sap, "te"), "प्रैधते"),
    ("उप", (iR,  tip), "उपैति"),
    (pra_upasarga, (fcCa, Sap, tip), "प्रार्च्छति"),
    ("ब्रह्म", "ऋषि", "ब्रह्मर्षि"),
    (AN_upasarga, ((Cad, Ric), Sap, tip), "आच्छादयति"),
    (("राम", su), "आसीत्", "राम आसीत्"),
    (gfj, Sap, tip, "गर्जति"),
    (vid, tip, "वेत्ति"),
    (("राम", su), (as_dhatu, tip), "रामोस्ति"),
    (("राम", su), avasAna, "रामः ।"),
    ("वाच्", ByAm, "वाग्भ्याम्"),
    ("त्यज्", ktvA, "त्यक्त्वा"),
    (("वाच्", su), avasAna, ["वाग् ।", "वाक् ।"]),
    (("वाच्", su), (as_dhatu, tip), "वागस्ति"),
    ("मधुलिह्", ByAm, "मधुलिड्भ्याम्"),
    (("लिह्", su) , avasAna, ["लिट् ।", "लिड् ।"]),
    (qulaBaz, kta, "लब्ध"),
    (guhU, kta, "गूढ"),
    ("पुनर्", "रमते", "पुना रमते"),
    (("अग्नि", su), "रोचते", "अग्नी रोचते"),
    # FIXME: correct when we can do uttizTati, move to utTAna
    (ud_upasarga, (sTA, tip), ["उत्थाति", "उत्थ्थाति"]),
    ("पुष्*", "ना", "ति", "पुष्णाति"), # 8.4.1
    ("तृंह्*", anIya, su, avasAna, "तृंहणीयः ।"), # 8.4.2
    # SK382-395: yuṣmad/asmad full declension
    # Nom sg (SK384+SK382+SK385)
    (yuzmad, su, "त्वम्"),         # SK384 (tv) + SK382 (su→am) + SK385 (d-lopa) → tvam
    (asmad, su, "अहम्"),          # SK384 (ah) + SK382 (su→am) + SK385 (d-lopa) → aham
    # Nom/voc du (SK386+SK387)
    (yuzmad, O, "युवाम्"),        # SK386 (yuva) + SK387 (O→ām) → yuvām
    (asmad, O, "आवाम्"),         # SK386 (Āva) + SK387 → āvām
    # Nom pl (SK388+SK382+SK385)
    (yuzmad, jas, "यूयम्"),       # SK388 (yūy) + SK382 (jas→am) + SK385 → yūyam
    (asmad, jas, "वयम्"),        # SK388 (vay) + SK382 → vayam
    # Acc sg (SK389+SK390+SK385)
    (yuzmad, am, "त्वाम्"),       # SK389 (tva) + SK390 (am→ām) + SK385 → tvām
    (asmad, am, "माम्"),         # SK389 (ma) + SK390 → mām
    # Acc pl (SK391+SK393+SK385)
    ((yuzmad, Sas), avasAna, ["युष्मान् ।", "वः ।"]),    # SK391 (śas→n) + SK393 (ā) + SK385 + 8.2.23 → yuṣmān; SK405 optional enclitic vaḥ
    ((asmad, Sas), avasAna, ["अस्मान् ।", "नः ।"]),     # SK391 + SK393 + 8.2.23 → asmān; SK405 optional enclitic naḥ
    # Inst sg (SK389+SK392+SK385)
    (yuzmad, wA, "त्वया"),        # SK389 (tva) + SK392 (a→ay) + SK385 → tvayā
    (asmad, wA, "मया"),          # SK389 (ma) + SK392 → mayā
    # Dat sg (SK394+SK382+SK385)
    (yuzmad, Ne, "तुभ्यम्"),      # SK394 (tuBhy+am) + SK385 → tubhyam
    (asmad, Ne, "मह्यम्"),       # SK394 (mahy+am) → mahyam
    # Inst/dat/abl du (SK386+SK393+SK385)
    (yuzmad, ByAm, "युवाभ्याम्"), # SK386 (yuva) + SK393 (ā) + SK385 → yuvābhyām
    (asmad, ByAm, "आवाभ्याम्"),  # SK386 (Āva) + SK393 → āvābhyām
    # Inst pl (SK393+SK385) — needs avasāna for final visarga
    ((yuzmad, Bis), avasAna, "युष्माभिः ।"),  # SK393 (ā) + SK385 → yuṣmābhiḥ
    ((asmad, Bis), avasAna, "अस्माभिः ।"),   # SK393 → asmābhiḥ
    # Dat/abl pl (SK395+SK385)
    (yuzmad, Byas, "युष्मभ्यम्"), # SK395 (Byas→Byam) + SK385 → yuṣmabhyam
    (asmad, Byas, "अस्मभ्यम्"),  # SK395 → asmabhyam
    # Gen du (SK386+SK392+SK385) — needs avasāna for final visarga; SK404 optional enclitic vāṃ/nau
    ((yuzmad, os), avasAna, ["युवयोः ।", "वाम् ।"]),   # SK386 (yuva) + SK392 (a→ay) + SK385 → yuvayoḥ; SK404 optional vāṃ
    ((asmad, os), avasAna, ["आवयोः ।", "नौ ।"]),       # SK386 (Āva) + SK392 → āvayoḥ; SK404 optional nau
    # Loc sg (SK389+SK392+SK385)
    (yuzmad, Ni, "त्वयि"),        # SK389 (tva) + SK392 (a→ay) + SK385 → tvayi
    (asmad, Ni, "मयि"),          # SK389 (ma) + SK392 → mayi
    # Loc pl (SK393+SK385)
    (yuzmad, sup, "युष्मासु"),    # SK393 (ā) + SK385 → yuṣmāsu
    (asmad, sup, "अस्मासु"),     # SK393 → asmāsu
    # SK127: हे मपरे वा (8.3.26) — M before h+m: kiṃhmalyati (8.3.23) or kim्hmalyati
    ("किम्", "ह्मल्यति", ["किंह्मल्यति", "किम्ह्मल्यति"]),
    # SK129: न परे नः (8.3.27) — M before h+n: kiṃhnute (8.3.23) or kinhnute
    ("किम्", "ह्नुते", ["किंह्नुते", "किन्ह्नुते"]),
    # SK130: ङ्णोः कुक् टुक् शरि (8.3.28) — N before ṣ: prāṅṣaṣṭhaḥ or prāṅkṣaṣṭhaḥ
    ("प्राङ्", "षष्ठः", ["प्राङ्षष्ठः", "प्राङ्क्षष्ठः"]),
    # SK130: R before ṣ: suguṇṣaṣṭhaḥ or suguṇṭṣaṣṭhaḥ (virama on ट् → no inherent vowel)
    ("सुगण्", "षष्ठः", ["सुगण्षष्ठः", "सुगण्ट्षष्ठः"]),
    # SK131: डः सि धुट् (8.3.29) — ḍ before s: ṣaṭsantaḥ or ṣaṭtsantaḥ
    ("षड्", "सन्तः", ["षट्सन्तः", "षट्त्सन्तः"]),
    # SK132: नश्च (8.3.30) — n before s: sansaḥ or santsaḥ
    ("सन्", "सः", ["सन्सः", "सन्त्सः"]),
     ]

test_list_slp1_ru = [
    # SK135: समः सुटि (8.3.5) — sam m→ru before suw-tagged s
    # 8.3.2 always: ~r; 8.3.4 optional: Mr. Then 8.3.15 r→H; 8.3.36(vā) or 8.3.34 H→s
    (sam, luk_sup, in_context(PaninianObject("skartA"), "suw"),   # noqa: F405
     ["sa~sskartA", "saMsskartA", "sa~skartA", "saMskartA"]),
    # SK139: पुमः खय्यम्परे (8.3.6) — 8.2.23 pums→pum, then m→ru before khay+vowel
    # 8.3.2: ~r; 8.3.4 optional: Mr. 8.3.15 r→H; 8.3.34 H→s; 8.4.40 ścutva before c
    (pums, luk_sup, "cakravAka", ["puMScakravAka", "pu~ScakravAka"]),   # noqa: F405
    (pums, luk_sup, "kokila", ["puMskokila", "pu~skokila"]),   # noqa: F405
    # SK141: नॄन्पे (8.3.10) — nṝn → ru before p
    # 8.3.2: ~r; 8.3.4 optional: Mr. 8.3.15→H; 8.3.37 (kupvoḥ) before p
    ("nFn", "pAhi", ["nFMHpAhi", "nF~HpAhi"]),
    # SK143: कानाम्रेडिते (8.3.12) — n of kān → ru before āmreḍita kān
    # 8.3.2: ~r; 8.3.4 optional: Mr. 8.3.15 r→H before k (khar)
    ("kAn", "kAn", ["kAMskAn", "kA~skAn"]),
    # SK152: सोऽपदादौ (8.3.38) — H → s before pāśap/kalpap/kap/kāmyac (non-iṇ, non-avyaya stems)
    # Positive: s-stem neuters — payaH/yaśaH + satva_t → s
    (payas, pASap,  "payaspASa"),   # payaH + pāśap → payaspāśa
    (payas, kalpap, "payaskalpa"),  # payaH + kalpap → payaskalpa
    (yaSas, pASap,  "yaSaspASa"),   # yaśaH + pāśap → yaśaspāśa
    (yaSas, kalpap, "yaSaskalpa"),  # yaśaH + kalpap → yaśaskalpa
    # Negative: avyaya padas — SK152 blocked by ?!avyaya_pada; H stays (SK142 identity)
    (prAtar, kalpap, "prAtaHkalpa"),  # prātaḥ kalpam
    (punar, kalpap, "punaHkalpa"),   # punaḥ kalpam
    # SK153: इणः षः (8.3.39) — iṇ+H → ṣ before pāśap/kalpap/kap/kāmyac (satva_t pratyayas)
    # i+s stem (sarpis): sarpi-H before ku/pu satva_t pratyaya → sarpiṣ (H→z)
    (sarpis, pASap,  "sarpizpASa"),   # sarpiH + pāśap → sarpiṣpāśa
    (sarpis, kalpap, "sarpizkalpa"),  # sarpiH + kalpap → sarpiṣkalpa
    # u+s stem (yajus): yaju-H before ku/pu satva_t pratyaya → yajuṣ (H→z)
    (yajus, pASap,  "yajuzpASa"),    # yajuH + pāśap → yajuṣpāśa
    (yajus, kalpap, "yajuzkalpa"),   # yajuH + kalpap → yajuṣkalpa
    # SK154: नमस्पुरसोर्गत्योः (8.3.40) — namas/puras gati H → s before ku/pu
    (namas, "kftam", "namaskftam"),   # namaH + kṛtam → namaskṛtam
    (namas, "pAta",  "namaspAta"),    # namaH + pāta  → namaspāta
    (puras, "kftam", "puraskftam"),   # puraH + kṛtam → puraskṛtam
    (puras, "pAta",  "puraspAta"),    # puraH + pāta  → puraspāta
    # SK155: इदुदुपधस्य चाप्रत्ययस्य (8.3.41) — i/u-upadha non-suffix H → ṣ before ku/pu
    (nis, luk_sup, "kftam", "nizkftam"),      # niH + kṛtam → niṣkṛtam
    (nis, luk_sup, "pAta",  "nizpAta"),       # niH + pāta  → niṣpāta
    (dus, luk_sup, "kftam", "duzkftam"),      # duH + kṛtam → duṣkṛtam
    (bahis, luk_sup, "kftam", "bahizkftam"),    # bahiH + kṛtam → bahiṣkṛtam
    # SK156: तिरसोऽन्यतरस्याम् (8.3.42) — tiras (gati) H → s optionally before ku/pu
    (tiras, luk_sup, "kartA", ["tiraskartA", "tiraHkartA"]),
    (tiras, luk_sup, "pAnam", ["tiraspAnam", "tiraHpAnam"]),
    # SK157: द्विस्त्रिश्चतुरिति कृत्वोऽर्थे (8.3.43) — dvis/tris/catur suc (kṛtvas arthe) H → ṣ optionally before ku/pu
    (dvi, suc, luk_sup,  "karoti", ["dvizkaroti",  "dviHkaroti"]),
    (tri, suc, luk_sup,  "karoti", ["trizkaroti",  "triHkaroti"]),
    (catur, suc, luk_sup,  "karoti", ["catuzkaroti", "catuHkaroti"]),
    # SK158: इसुसोः सामर्थ्ये (8.3.44) — is/us-final pada H → ṣ optionally before ku/pu (vyapekṣā)
    (sarpis, su, "karoti", ["sarpizkaroti", "sarpiHkaroti"]),
    (yajus,  su, "karoti", ["yajuzkaroti",  "yajuHkaroti"]),
    (Danus,  su, "karoti", ["Danuzkaroti",  "DanuHkaroti"]),
    # SK159: नित्यं समासेऽनुत्तरपदस्थस्य (8.3.45) — is/us-pūrva-pada H → ṣ mandatorily in samāsa
    (as_purva_pada(sarpis), luk_sup,  "kuRqikA",   "sarpizkuRqikA"),
    (as_purva_pada(Danus), luk_sup,  "kapAlakam", "DanuzkapAlakam"),
    # SK160: अतः कृकमिकंसकुम्भपात्रकुशाकर्णीष्वनव्ययस्य (8.3.46)
    # a-final samāsa pūrva (non-avyaya) + word-list uttara → H → s
    (as_purva_pada(ayas), luk_sup, kAra, su,  "ayaskAras"),
    (as_purva_pada(ayas), luk_sup, kAma, su, "ayaskAmas"),
    (as_purva_pada(ayas), luk_sup, kaMsa, su,  "ayaskaMsas"),
    (as_purva_pada(ayas), luk_sup,  kumBa, su,  "ayaskumBas"),
    (as_purva_pada(ayas), luk_sup,  pAtra, su, "ayaspAtram"),
    (as_purva_pada(ayas), luk_sup,  kuSA, su,   "ayaskuSA"),
    (as_purva_pada(ayas), luk_sup,  karRI, su,  "ayaskarRI"),
    (as_purva_pada(payas), luk_sup, kAra, su,  "payaskAras"),
    # Negative: uttarapada not in word-list → H stays (SK142/8.3.37 identity)
    (as_purva_pada(payas), luk_sup, "gamana", "payogamana"),
    # SK161: अधः शिरसी पदे (8.3.47) — aDas/Siras pūrva + pada uttara → H → s
    (as_purva_pada(aDas),  pada, su, "aDaspadam"),
    (as_purva_pada(Siras), pada, su,  "Siraspadam"),
    # Negative: uttarapada is not pada → H stays
    (as_purva_pada(Siras), luk_sup, "gamana", "Sirogamana"),
    # SK172: रोऽसुपि (8.2.69) — ahan's ?ru stays as r before non-sup (word boundary)
    (ahan, luk_sup, gaRa, su, ["ahargaRas","aharggaRas"] ),
    # SK176: एतत्तदोः सुलोपोऽकोरनञ्समासे हलि (6.1.132) — tad su-lopa (H deleted) before consonant
    (tad, su, vizRu, su, "savizRus"),
    (etad, su, vizRu, su, "ezavizRus"),
    # SK176 akoḥ exception (अकोः): no su-lopa when the tad/etad stem ends in a
    # ka-pratyaya (saka/eṣaka via kan, SK463/464). lc is "saka"/"eṣaka", not the
    # bare "sa"/"eṣa" that 6.1.132 requires, so su-r is preserved → 6.1.114 → 'o'.
    (tad, kan, su, vizRu, su, "sakovizRus"),    # saka(ḥ) viṣṇuḥ → sako viṣṇuḥ (NOT sa viṣṇuḥ)
    (etad, kan, su, vizRu, su, "ezakovizRus"),  # eṣaka(ḥ) viṣṇuḥ → eṣako viṣṇuḥ
]

