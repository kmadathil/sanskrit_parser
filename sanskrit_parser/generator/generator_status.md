# Generator Implementation Status

Sutras are implemented following the Siddhantakaumudi (SK) order from
https://drdhaval2785.github.io/siddhantakaumudi/

**Last implemented:** SK 487/488/489/490/491/492 — 4.1.29/4.1.30/4.1.32/4.1.33/4.1.34/4.1.35 (saṃjñā/chandas obligatory-ṅīp pair + pati i→n cluster). New stems: `surAjan`-context via `ati`+`rAjan`+`?saMjYA` (SK487), nine `?keval_Adi` stems `kevala`/`mAmaka`/`BAgaDeya`/`pApa`/`apara_488`/`samAna`/`AryakRta`/`sumaNgala`/`Bezaja` (SK488), `gRha` (SK491 test), `sapati`/`ekapati`/`vIrapati` `?sapatnyAdi`+`?pati` (SK492), `antarvat`/`pativat` `?antarvat_pativat` (SK489). SK487 makes 4.1.28's optional NIp mandatory in saṃjñā/chandas (overrides 4.1.4/4.1.12/4.1.13/4.1.28) → सुराज्ञी, अतिराज्ञी. SK488 takes ?saMjYA/?Candas keval_Adi gaṇa to NIp → केवली/मामकी/सुमङ्गली; laukika negative arm → 4.1.4 ṭāp + SK463 idādeśa → मामिका. SK488.1 niyama-blocker (मामकग्रहणं नियमार्थम्) overrides SK470 for ?mAmaka outside saṃjñā/chandas (currently inert — mAmaka stem lacks ?NIp_taddhita; forward-compatible). SK490 substitutes i→n on plain pati (?pati + ?!samAsa) → पत्नी; SK491 same on compound pati (?pati + ?samAsa) → गृहपत्नी; SK492 same on ?sapatnyAdi class → सपत्नी/एकपत्नी/वीरपत्नी. The substituted n-final stem then takes NIp via SK453 (4.1.5). SK489 appends नुक् 'n' to antarvat/pativat at bahiranga 1 → SK453 NIp → अन्तर्वत्नी/पतिवत्नी. Per Q2 deferral, semantic restrictions (?yajYasaMyoga / ?garBiNi / ?jIvadBartfka) not encoded. Per Q3 deferral, समानस्य सभावोऽपि niyama for SK492 handled by registering pre-substituted `sapati` rather than a paired left-substitution. Engine fix tied to SK491: a `--verbose-prakriya --tag-display` trace on gRhapatnī-cat-ek revealed that `?Gi` was being set on the in-compound pati at the (pati|strI_abs) window by 1.4.7 (arm 1, since lp had no `?strI` yet) and again at the (gRhapatnī|Ne) vibhakti window by 1.4.8 (lp had `?pati`+`?samAsa`), causing 7.3.111 (घेर्ङिति) to substitute ī→e on the merged stem and mis-route 4 oblique-sg cells (गृहपत्नयै etc.). Fix: 1.4.7 carries `rp: ?!strI` on all three arms; 1.4.8 carries `lp: ?!strI` (post-feminine window) and `rp: ?!strI` (pre-feminine window). gRhapatnī now declines as the textbook nadī (गृहपत्न्यै/गृहपत्न्याः/गृहपत्न्याम्). gaṇapati (compound pati masc, where Ghi-saṃjña should still apply) unaffected since the masculine sup pratyayas are not `?strI`.
**Next to be implemented:** SK 493 (4.1.36 पूतक्रतोरै च); deferred: SK 465-468 (7.3.46-49, northern variants); 4.1.31 रात्रेश्चाजसौ (no SK#); the vārttika **वुग्युटावुवङ्यणोः सिद्धौ वक्तव्यौ** (carves vuk-augment, yuṭ-augment, uvaṅ, yaṇ out of 6.4.22 — they remain siddha to other ābhīya rules; not yet implemented).

---

## Summary

| Category | Count |
|---|---|
| Sutras implemented | 348 |
| Sutras skipped / deferred | 54 |
| Sutras uncatalogued / not yet planned | ~67 |
| **Total sutras accounted for** | **~452** |
| Stems with full vibhakti test tables | 236 |
| Stems with partial vibhakti test tables | 3 |

---

## Implemented Sutras (SK order)

The "Forms affected" column uses the convention:
- **nom/acc/ins/dat/abl/gen/loc/voc** for vibhakti
- **sg/du/pl** for vacana
- **m/f/n** for linga where relevant
- Stem class in parentheses where the rule is class-specific

| SK | Sutra ID | Sutra | Forms affected |
|----|----------|-------|----------------|
| 47 | 6.1.77 | इको यणचि | ik before ac: yaṇ (i→y, u→v, ṛ→r) — core vowel sandhi |
| 52 | 8.4.53 | झलां जश् झशि | Jhal before jhaś: jaś substitute (jihvā+mūlīya etc.) |
| 54 | 8.2.23 | संयोगान्तस्य लोपः | Saṃyoga-final pada: last consonant deleted |
| 59 | 8.4.46 | अचो रहाभ्यां द्वे | ac after ra/ha: double the following ac (dvitva sandhi) |
| 60 | 8.4.64 | हलो यमां यमि लोपः | yama hal before yama hal: delete the first yama (geminate simplification) |
| 61 | 6.1.78 | एचोऽयवायावः | ec before ac: e→ay, o→av, ai→āy, au→āv |
| 63 | 6.1.79 | वान्तो यि प्रत्यये | o/av before y-initial pratyaya: av |
| 64 | 6.1.80 | धातोस्तन्निमित्तस्यैव | Restricts yaṇ-sandhi to dhātu context only |
| 65 | 6.1.81 | क्षय्यजय्यौ शक्यार्थे | Fixed forms kṣayya, jayya |
| 66 | 6.1.82 | क्रय्यस्तदर्थे | Fixed form krayya |
| 67 | 8.3.19 | लोपः शाकल्यस्य | Śākalya's option: delete y between vowels (Vedic) |
| 69 | 6.1.87 | आद्गुणः | a/ā + vowel → guṇa — core sandhi (rāma + iti → rāmeti) |
| 71 | 8.4.65 | झरो झरि सवर्णे | jhar before savarna jhar: lopa of first |
| 72 | 6.1.88 | वृद्धिरेचि | a/ā + e/o/ai/au → vṛddhi (rāma + eva → rāmaiva) |
| 73 | 6.1.89 | एत्येधत्यूठ्सु | iyaṅ/uvaṅ not applied before eṭ (iR, eDa dhātu) |
| 74 | 6.1.91 | उपसर्गादृति धातौ | ṛ-initial dhātu after upasarga: guṇa applies |
| 76 | 8.3.15 | खरवसानयोर्विसर्जनीयः | ru/r before khar or at avasāna → visarjanīya (ḥ) |
| 78 | 6.1.94 | एङि पररूपम् | Upasarga ending in e/o before a-initial dhātu: pararūpa (e.g. upa + eti → upeti) |
| 80 | 6.1.95 | ओमाङोश्च | om + māṅ: pararūpa |
| 84 | 8.2.39 | झलां जशोऽन्ते | Jhal at pada-end → jaś (k→g, t→d, etc.) |
| 85 | 6.1.101 | अकः सवर्णे दीर्घः | Savarna vowels merge to dīrgha (ā+a→ā, i+i→ī etc.) |
| 86 | 6.1.109 | एङः पदान्तादति | Pada-final e/o before short a: e/o preserved, a elided |
| 87 | 6.1.122 | सर्वत्र विभाषा गोः | Optional: skip SK86 (r:null) when go-stem (lc=g, l=o) at pada-end before a |
| 88 | 6.1.123 | अवङ् स्फोटायनस्य | Optional avayav for go-stems before vowel |
| 89 | 6.1.124 | इन्द्रे च | Mandatory avayav before indra-pada |
| 90 | 6.1.125 | प्लुतप्रगृह्या अचि नित्यम् | Pluta and pragṛhya vowels before vowels: no sandhi |
| 100 | 1.1.11 | ईदूदेद्द्विवचनं प्रगृह्यम् | Dual endings -ī, -ū, -e are pragṛhya (no sandhi): nom/acc du of ī/ū/e-final stems |
| 101 | 1.1.12 | अदसोमात् | adasaḥ: the form amā (inst sg of adas) is pragṛhya |
| 111 | 8.4.40 | स्तोः श्चुना श्चुः | s/t-group + ś-group → ś-group (śaśca → śaśca; rāmasya+janī → °śjanī) |
| 112 | 8.4.44 | शात् | After ś: exception to ścutva |
| 113 | 8.4.41 | ष्टुना ष्टुः | s/t-group + ṣ-group → ṣ-group (ṣṭutva) |
| 114 | 8.4.42 | न पदान्ताट्टोरनाम् | Exception to ṣṭutva: ṭ/ṭh at pada-end before nāman |
| 115 | 8.4.43 | तोः षि | t/th + ṣ → ṭ/ṭh (ṣṭutva) |
| 116 | 8.4.45 | यरोऽनुनासिकेऽनुनासिको वा | Yar before anunāsika: optionally anunāsika |
| 117 | 8.4.60 | तोर्लि | t/th before l → l (tad + labhate → tallabhate) |
| 118 | 8.4.61 | उदः स्थास्तम्भोः पूर्वस्य | ud + sthā/stambh: d → t |
| 119 | 8.4.62 | झयो होऽन्यतरस्याम् | Jha before h: optionally h → jha (tad+hi → tajjhi) |
| 120 | 8.4.63 | शश्छोऽटि | ś + aṭ: ch (namaś + ca → namaścca) |
| 121 | 8.4.55 | खरि च | Jhal before khar: jhar → car (t before k etc.) |
| 122 | 8.3.23 | मोऽनुस्वारः | m at pada-end → anusvāra (rāmam → rāmaṁ) |
| 123 | 8.3.24 | नश्चापदान्तस्य झलि | non-pada-final n before jhal → anusvāra |
| 124 | 8.4.58 | अनुस्वारस्य ययि परसवर्णः | Anusvāra before yay: parasavarna (rāmaṁ karoti → rāmaṅ k°) |
| 125 | 8.4.59 | वा पदान्तस्य | Pada-final anusvāra: parasavarna optional |
| 127 | 8.3.26 | हे मपरे वा | optional reversion: anusvāra M → m before h when h is m-para (rr=m); overrides SK123 |
| 129 | 8.3.27 | न परे नः | optional: anusvāra M → n before h when h is n-para (rr=n); overrides SK123 |
| 130 | 8.3.28 | ङ्णोः कुक् टुक् शरि | optional: ṅ/ṇ at pada-end before śar → append kuk (k) or ṭuk (ṭ) |
| 131 | 8.3.29 | डः सि धुट् | optional: ḍ at pada-end before s → prepend dhuṭ (dh) to right pada |
| 132 | 8.3.30 | नश्च | optional: n at pada-end before s → prepend dhuṭ (extends SK131 to n) |
| 133 | 8.3.31 | शि तुक् | śi (neuter pl marker): tuk inserted before it after certain stems |
| 134 | 8.3.32 | ङमो ह्रस्वादचि ङमुण् नित्यम् | Ṅam after hrasva before vowel: ṅamuṇ (kam-api → kamapi) |
| 135 | 8.3.5 | समः सुटि | sam prefix m→ru before suw-tagged pada (backtrigger 8.3.2/4 via ?ru_anu) |
| 136 | 8.3.2 | अत्रानुनासिकः पूर्वस्य तु वा | Non-optional: r → ~r (anunāsika) after any ru substitution; keeps ?ru_anu so 8.3.4 fires next |
| 137 | 8.3.4 | अनुनासिकात् परोऽनुस्वारः | Optional: ~r → Mr (anusvāra), strips ~ from lc; fires on 8.3.2's output |
| 138 | 8.3.34 | विसर्जनीयस्य सः | visarjanīya → s before khar (prathama tripādī) |
| 139 | 8.3.6 | पुमः खय्यम्परे | 8.2.23 deletes pums→pum first; m→ru before khay+vowel (backtrigger 8.3.2/4) |
| 140 | 8.3.7 | नश्छव्यप्रशान् | n before ch-group: ś inserted (rāmāṃś ca) |
| 141 | 8.3.10 | नॄन्पे | nṝn (acc pl nṛ) n→ru before p (backtrigger 8.3.2/4) |
| 142 | 8.3.37 | कुप्वोः कपौ च | visarjanīya before ku/pu consonants → ka |
| 143 | 8.3.12 | कानाम्रेडिते | n of kān → ru before āmreḍita kān (backtrigger 8.3.2/4) |
| 146 | 6.1.73 | छे च | c-initial pratyaya: insert t (tuk) before it |
| 147 | 6.1.74 | आङ्माङोश्च | āṅ/māṅ before vowel: chandas/veda usage |
| 148 | 6.1.75 | दीर्घात् | Long vowel + ch: tuk inserted |
| 149 | 6.1.76 | पदान्ताद्वा | Pada-final + ch: tuk optionally |
| 150 | 8.3.35 | शर्परे विसर्जनीयः | visarjanīya before śar group preserved as visarjanīya |
| 151 | 8.3.36 | वा शरि | optionally visarjanīya before śar (vibhāṣā to SK150) |
| 152 | 8.3.38 | सोऽपदादौ | visarjanīya → s before pāśap/kalpap/kap/kāmyac pratyayas (non-iṇ stems); rāmas+pāśap→rāmaspāśa |
| 153 | 8.3.39 | इणः षः | visarjanīya → ṣ after iṇ (i/u/ṛ/ḷ) before pāśap/kalpap/kap/kāmyac pratyayas (satva_t tag); sarpis+pāśap→sarpiṣpāśa, yajus+kalpap→yajuṣkalpa |
| 154 | 8.3.40 | नमस्पुरसोर्गत्योः | visarjanīya → s for namas/puras (tagged ?gati) before any ku/pu; namas+kṛtam→namaskṛtam, puras+pāta→puraspāta |
| 155 | 8.3.41 | इदुदुपधस्य चाप्रत्ययस्य | visarjanīya → ṣ for i/u-upadha non-suffix stems (?!viBakti_pada) before any ku/pu; niH+kṛtam→niṣkṛtam, duH+kṛtam→duṣkṛtam **(partial: muhus exception and vṛddhi forms — naiṣkulyam/dauṣkulyam — deferred)** |
| 156 | 8.3.42 | तिरसोऽन्यतरस्याम् | tiras (gati) visarjanīya → s optionally before ku/pu; tiraH+kartā → tiraskartā / tiraHkartā **(partial: non-gati tiras context not distinguished)** |
| 157 | 8.3.43 | द्विस्त्रिश्चतुरिति कृत्वोऽर्थे | dvis/tris/catur as kṛtvas-adverbs: visarjanīya → ṣ optionally before ku/pu; dviH+karoti → dviṣkaroti / dviḥkaroti |
| 158 | 8.3.44 | इसुसोः सामर्थ्ये | is/us-final pada visarjanīya → ṣ optionally before ku/pu in vyapekṣā (sāmarthya); sarpiH+karoti → sarpiṣkaroti / sarpiḥkaroti |
| 159 | 8.3.45 | नित्यं समासेऽनुत्तरपदस्थस्य | is/us-final pūrva-pada in samāsa: visarjanīya → ṣ mandatorily before ku/pu (anuttarapadastha via rp:?!samAsaPurva); sarpis+kuṇḍikā → sarpiṣkuṇḍikā |
| 160 | 8.3.46 | अतः कृकमिकंसकुम्भपात्रकुशाकर्णीष्वनव्ययस्य | a-final samāsa pūrvapada (non-avyaya) H → s before {kāra, kāma, kaṃsa, kumbha, pātra, kuśā, karṇī} (tag satva_kfkamkaMsAdi_pada on uttara); partial — kṛ/kam kṛdanta forms deferred |
| 161 | 8.3.47 | अधः शिरसी पदे | aDas/Siras samāsa pūrvapada H → s before any vibhakti form of pada (tag pada_p_pada on uttara via pada_p propagation); full 8×3 vibhakti test for aDaspada and Siraspada |
| 162 | 8.2.66 | ससजुषो रुः | s/sajuṣ at pada-end → ru (visarga source: rāmaḥ) |
| 163 | 6.1.113 | अतो रोरप्लुतादप्लुते | a-final pada + ru before a: ro'r (rāmaH + asti → rāmo'sti) |
| 164 | 6.1.102 | प्रथमयोः पूर्वसवर्णः | nom/acc du: stem-final a/ā + O ending → long vowel (e.g. rāma + O → rāmau) |
| 165 | 6.1.104 | नादिचि | pragṛhya ā-final: no sandhi before vowel (ā preserved) |
| 166 | 6.1.114 | हशि च | e/o-final + h-initial: pararūpa sandhi (also covers haśi before śi) |
| 167 | 8.3.17 | भोभगोअघोअपूर्वस्य योऽशि | bho/bhago/agho etc.: y inserted before aśi vowels |
| 169 | 8.3.20 | ओतो गार्ग्यस्य | Gārgya's option for o |
| 172 | 8.2.69 | रोऽसुपि | ahan's ?ru stays as r in non-sup contexts; blocks 6.1.113/114/8.3.17 at word boundaries. Partial: vārttikās (ahorUpam/ahorAtriH/ahorathantaram; pati-group optional r) deferred |
| 173 | 8.3.14 | रो रि | ru (=r) before r: lopa of ru, pūrva-dīrgha |
| 174 | 6.3.111 | ढ्रलोपे पूर्वस्य दीर्घोऽणः | Compensatory lengthening after ḍh/r lopa |
| 176 | 6.1.132 | एतत्तदोः सुलोपोऽकोरनञ्समासे हलि | tad/etad: r (su→r via 8.2.66) deleted before consonant at word boundary, blocking 6.1.114/8.3.15. akoH (अकोः) handled by exact lc match (=sa/=eza): ka-pratyaya stems saka/eṣaka keep su-r → sako/eṣako viṣṇuḥ (tested). Partial: nañsamāsa exception still deferred |
| 191 | 6.1.97 | अतो गुणे | a + guṇa vowel (e/o/ai/au): pūrvarūpa (a absorbed) |
| 193 | 6.1.69 | एङ्ह्रस्वात्संबुद्धेः | voc sg of ī/ū-final stems: drop su (śe drops) — rāma→rāma, e→e |
| 194 | 6.1.107 | अमिपूर्वः | Stem vowel before am: pūrvarūpa (e.g. go + am → gām) |
| 196 | 6.1.103 | तस्माच्छसो नः पुंसि | masculine: śas (acc pl) → nas after pronoun-base ending in that |
| 197 | 8.4.2 | अट्कुप्वाङ्नुम्व्यवायेऽपि | ṇatva even with aṭ/ku/pu/āṅ/num intervening |
| 198 | 8.4.37 | पदान्तस्य | Exception: no ṇatva at pada-end |
| 199 | 1.4.13 | यस्मात्प्रत्ययविधिस्तदादि प्रत्ययेऽङ्गम् | āṅga saṁjñā: portion from which a pratyaya operation is ordained is anga |
| 201 | 7.1.12 | टाङसिङसामिनात्स्याः | ins sg → inā; abl/gen sg → āt, sya (a-stems: rāmeṇa, rāmāt, rāmasya) |
| 202 | 7.3.102 | सुपि च | a-stem before sup: guṇa of final a — loc sg rāme, ins rāmeṇa |
| 203 | 7.1.9 | अतो भिस ऐस् | a-stem + bhis → ais (ins pl: rāmaiḥ) |
| 204 | 7.1.13 | ङेर्यः | dat sg e-ending → ya (a-stem: rāmāya; sarvanāma: sarvasmai) |
| 205 | 7.3.103 | बहुवचने झल्येत् | a-stem before hal-initial bahuvacana sup: guṇa → e (dat/abl/loc pl: rāmebhyaḥ, rāmeṣu) |
| 206 | 8.4.56 | वाऽवसाने | Optionally at avasāna: jhal → car |
| 207 | 7.3.104 | ओसि च | a-stem before os: guṇa → e (gen/loc du: rāmayoḥ) |
| 208 | 7.1.54 | ह्रस्वनद्यापो नुट् | nadī/āp-stems + am/āṁ: inserts nut (n) — gen pl nadīnām, rāmāṇām |
| 209 | 6.4.3 | नामि | aṅga lengthening before nāmī (gen pl am) — rājñām |
| 211 | 8.3.57 | इण्कोः | Adhikāra — enables ṇatva in ādeśa/pratyaya context; active sutras are SK434 (8.3.58) and SK212 (8.3.59) |
| 212 | 8.3.59 | आदेशप्रत्यययोः | ādeśa/pratyaya context: ṇatva applies |
| 213 | 1.1.27 | सर्वादीनि सर्वनामानि | Defines the sarvanāma class (sarva, viśva, etc.) |
| 214 | 7.1.17 | जसः शी | ī-final feminine nom pl: jas → śī (nadyaḥ → nadyaḥ via śī+sandhi) |
| 215 | 7.1.14 | सर्वनाम्नः स्मै | sarvanāma + dat sg e → smai (sarvasmai, tasmai, etc.) |
| 216 | 7.1.15 | ङसिङ्योः स्मात्स्मिनौ | sarvanāma abl sg → smāt; loc sg → smin (sarvasmāt, sarvasmin) |
| 217 | 7.1.52 | आमि सर्वनाम्नः सुट् | sarvanāma + āṁ: inserts su → sām (gen pl sarveṣām) |
| 228 | 6.1.63 | पद्दन्नोमास्… | Samprasāraṇa: special alternants for pada, danta, nāman etc. stems in certain forms |
| 229 | 1.1.43 | सुडनपुंसकस्य | su/ḍ of non-neuter gender = sarvānāmasthāna |
| 230 | 1.4.17 | स्वादिष्वसर्वनामस्थाने | su-ādi non-sarvānāmasthāna: triggers bha saṁjñā for anga |
| 231 | 1.4.18 | यचि भम् | before yac pratyaya: anga gets bha saṁjñā |
| 234 | 6.4.134 | अल्लोपोऽनः | n-final stem: delete n before yāsut (gen pl rājñām) |
| 235 | 8.4.1 | रषाभ्यां नो णः समानपदे | n → ṇ after r/ṣ in same pada (ṇatva: rāmāṇām) |
| 236 | 8.2.7 | नलोपः प्रातिपदिकान्तस्य | n-final prātipadika at pada-end: n deleted (rājan+su → rājā) |
| 237 | 6.4.136 | विभाषा ङिश्योः | optional al-lopa of n before Ṅi/ŚI (vibhāṣā apavāda to SK234) |
| 238 | 6.3.110 | सङ्ख्याविसायपूर्वस्याह्नस्याऽहन्नन्यतरस्यां ङौ | optional ahani substitute for pUrvapada ahan before ṅit; dvya-hni/dvya-hani variants |
| 239 | 6.1.105 | दीर्घाज्जसि च | after dīrgha-final + jas: exception (no further sandhi change) |
| 240 | 6.4.140 | आतो धातोः | ā-final dhātu + kta: ā deleted (sthā + ta → sthita) |
| 241 | 7.3.109 | जसि च | ī/ū-final feminine + jas: guṇa (suDiyaḥ, BrūvaḥÀ) |
| 242 | 7.3.108 | ह्रस्वस्य गुणः | Short ī/ū-final: guṇa before certain sup (nadī → nade in loc sg) |
| 243 | 1.4.7 | शेषो घ्यसखि | Remaining i/u-final (non-nadī, non-sakhi) stems: ghy-saṃjñā — affects aṅga rules |
| 244 | 7.3.120 | आङो नाऽस्त्रियाम् | āṅ: ā not lengthened in non-feminine context |
| 245 | 7.3.111 | घेर्ङिति | ghi-final anga + ṅit suffix: guṇa of i (nau: nauh; strī + ṅi: stry-ām bha) |
| 246 | 6.1.110 | ङसिङसोश्च | ṛ-final + gen sg/abl sg: uraṇ + dirgha — pitṛ → pituḥ, pitroḥ |
| 247 | 7.3.119 | अच्च घेः | ac-initial suffix after ghe: guṇa applies |
| 248 | 7.1.93 | अनङ् सौ | n-final neuter + su: anañ substitute — nom sg rājā, but neuter: nāma |
| 250 | 6.4.8 | सर्वनामस्थाने चासम्बुद्धौ | n-final + sarvānāmasthāna (non-voc): lengthening (rājā nom sg) |
| 252 | 6.1.68 | हल्ङ्याब्भ्यो दीर्घात्… | Drop apṛkta hal su/si/s after long vowel or ṅī/āp (nadī nom sg: nadī) |
| 253 | 7.1.92 | सख्युरसंबुद्धौ | sakhi: special oblique stem sakhā- (non-voc forms) |
| 254 | 7.2.115 | अचोञ्णिति | ac-final anga before Ñit/Ṇit suffix: vṛddhi (primary vṛddhi rule) |
| 255 | 6.1.112 | ख्यत्यात्परस्य | khyāt-endings: pararūpa before certain vowels |
| 256 | 7.3.118 | औत् | o → au in certain anga positions (au-substitution) |
| 257 | 1.4.8 | पतिः समास एव | pati gets ghī-saṃjñā only in compound; standalone uses regular i-stem |
| 259 | 1.1.25 | डति च | Numeral daśan class: daśa, etc. defined as saṃkhyā with ḍati |
| 261 | 7.1.22 | षड्भ्यो लुक् | ṣaṭ-group: sup luk (lopa) in certain forms — ṣaḍbhiḥ, etc. |
| 263 | 1.1.63 | न लुमताङ्गस्य | aṅga rules do not apply when pratyaya has been luked (luk marker) |
| 264 | 7.1.53 | त्रेस्त्रयः | tri → traya (nom/acc pl m: trayaḥ) |
| 265 | 7.2.102 | त्यदादीनामः | tya-group (tat, etad, idam, adas) + su: āḥ substitute — saḥ, eṣaḥ |
| 266 | 1.4.3 | यू स्त्र्याख्यौ नदी | Defines nadī-saṃjñā for ī/ū-final feminines (nadī, vadhū etc.) |
| 267 | 7.3.107 | अम्बार्थनद्योर्ह्रस्वः | nadī + sambuddhi: hrasva (amba! devi!) |
| 268 | 7.3.112 | आण्नद्याः | nadī + ṅe (dat sg): āṇ substitute → nadyai |
| 269 | 6.1.90 | आटश्च | āṭ augment + short vowel: guṇa — affects ā-stem āp forms (rāmāyai) |
| 270 | 7.3.116 | ङेराम्नद्याम्नीभ्यः | nadī/āp/nī + ṅer (dat sg): āṁ (rāmāyāḥ gen = same) |
| 271 | 6.4.77 | अचिश्नुधातुभ्रुवां य्वोरियङुवङौ | i/u-final dhātu/bhrū before ac: iyaṅ/uvaṅ (bhrū → bhruvau, suDī → suDiyaḥ) |
| 272 | 6.4.82 | एरनेकाचोऽसंयोगपूर्वस्य | Multi-syllable i-final (non-saṃyoga) + ac: iyaṅ (suDī forms) |
| 273 | 6.4.85 | न भूसुधियोः | Exception: BU and suDī do NOT get iyaṅ/uvaṅ (6.4.77 blocked) |
| 274 | 7.1.95 | तृज्वत्क्रोष्टुः | kroṣṭu inflects like tṛc (ṛ-final) — kroṣṭā, kroṣṭuḥ etc. |
| 275 | 7.3.110 | ऋतो ङिसर्वनामस्थानयोः | ṛ-final anga before ṅi or sarvānāmasthāna: guṇa (ṛ→ar; kartari etc.) |
| 276 | 7.1.94 | ऋदुशनस्पुरुदंसोऽनेहसां च | ṛtu, uśanas, purudaṃsas, anehas: special nom sg |
| 277 | 6.4.11 | अप्तृन्तृच्… | ṛ-final stems (pitṛ, mātṛ, tvaṣṭṛ etc.): aṅga lengthening before sarvānāmasthāna — pitāram |
| 278 | 7.1.97 | विभाषा तृतीयादिष्वचि | ṛ-final + tṛtīyādi vowel-initial sup: optional uraṇ (pitrā or pitarā) |
| 279 | 6.1.111 | ऋत उत् | ṛ-final + gen/loc du os: ṛ→ur (pituḥ, pitroḥ) |
| 280 | 8.2.24 | रात्सस्य | s after r in pada: deleted (pitṛ+su → pitā, not pitarsu) |
| 281 | 6.4.83 | ओः सुपि | go + sup: o→av (govā etc.) |
| 282 | 6.4.84 | वर्षाभ्वश्च | varzāBU and similar compound BU-stems: o→av |
| 283 | 6.4.6 | नृ च | nṛ-stem: special aṅga form nara- before sarvānāmasthāna |
| 284 | 7.1.90 | गोतो णित् | go + certain sup: treated as ṇit (long ā) — gāṁ, gāḥ |
| 285 | 6.1.93 | औतोऽम्शसोः | go + am/śas: au→āv (gām, gāḥ) |
| 286 | 7.2.85 | रायो हलि | rāy-stem (rE) + hal-initial sup: guṇa → rāye etc. |
| 287 | 7.1.18 | औङ आपः | āp-stem + au (nom du): auṅ substitute (rāme → rāmau, but āp: rāme) |
| 288 | 7.3.106 | संबुद्धौ च | āp-stem + sambuddhi: hrasva (rāme voc sg) |
| 289 | 7.3.105 | आङि चापः | āp-stem + āṅi (loc sg): ā→ai (rāmāyāṁ) |
| 290 | 7.3.113 | याडापः | āp + ṅe (dat sg): yāṭ inserted (rāmāyai) |
| 291 | 7.3.114 | सर्वनाम्नः स्याड्ढ्रस्वश्च | sarvanāma + ṅe: syāṭ, hrasva (sarvāsyai fem) |
| 293 | 7.3.115 | विभाषा द्वितीयातृतीयाभ्याम् | Optionally extends SK291 syāṭ to dvitīyā/tṛtīyā f. dat sg: dvitīyasyai/tṛtīyasyai (optional) vs dvitīyāyai/tṛtīyāyai (yāṭ) |
| 294 | 8.2.36 | व्रश्चभ्रस्ज… षः | ś/ch at pada-end → ṣ (lih → liṭ etc.) |
| 295 | 8.2.41 | षढोः कः सि | ṣ/ḍh at pada-end + si → k (lih+su → liṭ) |
| 296 | 1.4.6 | ङिति ह्रस्वश्च | Long ī/ū-final feminines + ṅit sup: optional hrasva + nadī-saṃjñā |
| 297 | 7.3.117 | इदुद्भ्याम् | i/u-final nadī anga before Ṅi: suffix → ām (nadī loc sg: nadyām, vadhvām); overrides SK256 (7.3.118) and 7.3.116 |
| 298 | 7.2.99 | त्रिचतुरोः स्त्रियां तिसृचतसृ | tri/catur fem: tisṛ/catasṛ substitutes |
| 299 | 7.2.100 | अचि र ऋतः | tisṛ/catasṛ + vowel-initial: ṛ→ar (tisṝṇām → tisṛ forms) |
| 300 | 6.4.4 | न तिसृचतसृ | Exception: tisṛ/catasṛ don't get lengthening before nāmī |
| 301 | 6.4.79 | स्त्रियाः | Feminine aṅga operations: governs strī-stem changes |
| 302 | 6.4.80 | वाम्शसोः | Feminine stem before vā (am) and śas: special form |
| 303 | 1.4.4 | नेयङुवङ्स्थानावस्त्री | Defines: iyaṅ/uvaṅ substituted stems are NOT nadī (so no nadī rules apply) |
| 304 | 1.4.5 | वामि | Long ī/ū-final Snu/dhātu/bhrū + Am: optionally nadī |
| 305 | 7.1.96 | स्त्रियां च | Feminine tṛc-forms: same as tṛj-pattern |
| 306 | 4.1.5 | ऋन्नेभ्यो ङीप् | ṛn/n-final pum stems → ṅīp suffix for feminine (rājñī etc.) |
| 307 | 8.4.12 | एकाजुत्तरपदे णः | ṇatva in ekāc samāsa compounds: n→ṇ in suffixes when pūrva-pada contains r/ṛ/ṣ and uttara-pada is monosyllabic; ekāc tracked via ?ekac tag (survives guṇa/vṛddhi); samasta_Ratva_pada feeds 8.4.1/8.4.2 arm B |
| 308 | 4.1.10 | न षट्स्वस्रादिभ्यः | Exception to 4.1.5: ṣaṭ-group and svasṛ etc. don't take ṅīp |
| 309 | 7.1.24 | अतोऽम् | a-stem + am (acc sg): no change — rāmam |
| 310 | 7.1.19 | नपुंसकाच्च | Neuter + au: am substitute (jñānam nom/acc du) |
| 311 | 6.4.148 | यस्येति च | Stem-final i/a deleted before ī (e.g. in taddhita/kṛt formations) |
| 312 | 7.1.20 | जश्शसोः शिः | Neuter + jas/śas: śi substitute (jñānāni nom/acc pl) |
| 313 | 1.1.42 | शि सर्वनामस्थानम् | Defines śi as sarvānāmasthāna (triggers strong stem forms) |
| 314 | 7.1.72 | नपुंसकस्य झलचः | Hal-final neuter + śi: nu-āgama inserted (jaganti) |
| 315 | 7.1.25 | अद्ड्डतरादिभ्यः पञ्चम्यः | adaḍ etc.: ḍ-āgama in pañcamī |
| 316 | 6.4.143 | टेः | ṭi (= from last vowel of anga) deleted before certain kṛt suffixes |
| 317 | 6.4.10 | सान्तमहतः संयोगस्य | Saṃyoga-final + nāmī: last consonant of saṃyoga deleted (mahat → mahā before sarvānāmasthāna) |
| 318 | 1.2.47 | ह्रस्वो नपुंसके | Neuter prātipadika: hrasva before su/am |
| 319 | 7.1.23 | स्वमोर्नपुंसकात् | Neuter + su/am: su/am → am (jñānam) |
| 320 | 7.1.73 | इकोऽचि विभक्तौ | ik-final + vowel-initial vibhakti: tuk inserted (akṣṇā, akṣṇoḥ) |
| 322 | 7.1.75 | अस्थिदधिसक्थ्यक्ष्णामनङुदात्तः | asthi/dadhi/sakthi/akṣan stems: anaN augment (udātta) before sarvānāmasthāna |
| 324 | 8.2.31 | हो ढः | h at pada-end → ḍh (lih → liḍh) |
| 325 | 8.2.32 | दादेर्धातोर्घः | dā-initial dhātu h → gh at pada-end |
| 326 | 8.2.37 | एकाचो बशो भष् | Single-syllable stem ending in b/g/ḍ/j + s/dh: bhāṣ substitute |
| 327 | 8.2.33 | वा द्रुहमुहष्णुहष्णिहाम् | druh/muh/ṣṇuh/ṣṇih: optionally gh or ḍh at pada-end |
| 329 | 6.4.132 | वाह ऊठ् | vāh-stem: āḥ → ūṭh in strong forms |
| 330 | 6.1.108 | संप्रसारणाच्च | After samprasāraṇa: pūrvarūpa |
| 331 | 7.1.98 | चतुरनडुहोरामुदात्तः | catur/anaḍuh + am: āṁ (gen pl caturṇām, anaḍuhām) |
| 332 | 7.1.82 | सावनडुहः | anaḍuh + su: ā (anaḍvā nom sg) |
| 333 | 7.1.99 | अम् संबुद्धौ | anaḍuh + sambuddhi: am → anaḍvan (voc sg) |
| 334 | 8.2.72 | वसुस्रंसुध्वंस्वनडुहां दः | anaḍuh at pada-end: h→d (anaḍud) |
| 335 | 8.3.56 | सहेः साडः सः | sah-stem: s at start of certain forms |
| 336 | 7.1.84 | दिव औत् | div-stem + sup: au substitute (dyauḥ nom sg) |
| 337 | 6.1.131 | दिव उत् | div-stem: u substituted for iv before certain endings (dyauḥ, divam, etc.) |
| 338 | 7.1.55 | षट्चतुर्भ्यश्च | ṣaṭ/catur + am: nuk inserted (ṣaṭṇām, caturṇām) |
| 339 | 8.3.16 | रोः सुपि | r(u) before sup → visarjanīya (ḥ); source of pada-final visarga before sup |
| 340 | 8.4.49 | शरोऽचि | śar after anusvāra before vowel: no change (exception to 8.4.46) |
| 341 | 8.2.64 | मो नो धातोः | m-final dhātu at pada-end → n (pra-gam → pragan) |
| 342 | 7.2.103 | किमः कः | kim → ka substitute before most sup (kasya, kasmai etc.) |
| 343 | 7.2.108 | इदमो मः | idam: m substituted in certain positions (idaṁ, imaṁ etc.) |
| 344 | 7.2.111 | इदोऽय् पुंसि | idas masculine: ay substituted (masculine idam forms: ayam etc.) |
| 345 | 7.2.109 | दश्च | kim + daḥ (abl sg daḥ form): ka |
| 346 | 7.2.112 | अनाप्यकः | remaining idam substitutions (non-āp, non-a-final contexts) |
| 347 | 7.2.113 | हलि लोपः | kim before hal-initial sup: lopa (kena etc.) |
| 349 | 7.1.11 | नेदमदसोरकोः | idam/adas: no ka-substitute (1.1.11 blocks) |
| 350 | 2.4.32 | इदमोऽन्वादेशेऽशनुदात्तः | idam in anuvādeśa context (tṛtīyādi): substitute a (asmāt etc.) |
| 351 | 2.4.34 | द्वितीयाटौस्स्वेनः | idam anuvādeśa + acc/ins/gen du: svena substitute (anena, ābhyām, anayoḥ) |
| 352 | 8.2.8 | न ङिसम्बुद्ध्योः | Exception: n-lopa (8.2.7) does NOT apply before ṅi/sambuddhi (rājni, rājan!) |
| 354 | 8.2.77 | हलि च | upadhā-dīrgha of v/r-final dhātu upadhā-ik before hal-initial suffix |
| 355 | 6.4.137 | न संयोगाद्वमन्तात् | blocks al-lopa of -an stems when saṃyoga ends in v or m; ensures parvan/yajvan bha forms |
| 356 | 6.4.12 | इन्हन्पूषार्यम्णां शौ | blocks upadhā-dīrgha (6.4.8) for in/han/pūṣan/aryaman before all sarvānāmasthāna except śi; hastinau (no dīrgha) in du |
| 357 | 6.4.13 | सौ च | re-enables upadhā-dīrgha for in/pūṣan/aryaman before su: hastī, pūṣā, aryamā (nom sg) |
| 358 | 7.3.54 | हो हन्तेर्ञ्णिन्नेषु | h of han-stem → G (gh) before ṅit/ṇit/n; vṛtraghna- forms in bha position |
| 359 | 8.4.22 | हन्तेरत्पूर्वस्य | blocks ṇatva (n→ṇ) after G in han-stems; vṛtraghna not *vṛtraghṇa |
| 360 | 6.4.128 | मघवा बहुलम् | optional tṛ-substitute for maGavan (bahulam); both maGavat- and maGo- paradigms |
| 361 | 7.1.70 | उगिदचां सर्वनामस्थानेऽधातोः | nUM before sarvanamasthana for ugit-marked (++f) stems; enables -ant strong forms |
| 362 | 6.4.133 | श्वयुवमघोनामतद्धिते | samprasāraṇa (v→u) for śvan/yuvan/maGavan in bha (vowel-initial non-sarvanamasthana) |
| 364 | 6.4.127 | अर्वणस्त्रसावनञः | mandatory tṛ-substitute for arvan before all suffixes except su; arvant- strong, arvat- bha **(partial: nañ exception — anarvan → yajvan-type — deferred; needs nañ tag propagation)** |
| 365 | 7.1.85 | पथिमथ्यृभुक्षामात् | ā for final n of paTin/maTin/fBukzin before su (both nom and voc sg); panthāḥ, manthāḥ, ṛbhukṣāḥ |
| 366 | 7.1.86 | इतोऽत्सर्वनामस्थाने | i→a of paTin-group before sarvanamasthana; combines with 6.4.8 for dīrgha in strong forms |
| 367 | 7.1.87 | थो न्थः | th→nth in paTin/maTin (not fBukzin) before sarvanamasthana; panthān- strong forms |
| 368 | 7.1.88 | भस्य टेर्लोपः | ṭi-lopa (delete final i+n) for paTin-group in bha position; path-, math-, ṛbhukṣ- before vowels |
| 369 | 1.1.24 | ष्णान्ता षट् | saṃjñā: ṣ/n-final numerals tagged ?zaT; enables ṣaṭ-class rules for pañcan, ṣaṣ, saptan, aṣṭan, navan, daśan |
| 370 | 6.4.7 | नोपधायाः | upadhā-dīrgha + n-lopa before gen pl (nāmi); paYcAnAm, azwAnAm, saptAnAm, navAnAm, daSAnAm |
| 371 | 7.2.84 | अष्टन आ विभक्तौ | optional n→ā for aṣṭan before hal-initial vibhakti; aṣṭābhis/aṣṭabhis, aṣṭābhyas/aṣṭabhyas, aṣṭāsu/aṣṭasu |
| 372 | 7.1.21 | अष्टाभ्य औश् | optional jas/śas → au (O) for aṣṭan; aṣṭau (nom/acc pl); overrides SK261 (7.1.22) |
| 376 | 7.1.71 | युजेरसमासे | num (ñ) augment for non-compound yuj before sarvanamasthāna; yuñjau, yuñjaḥ strong; yuṅ nom sg. Compound yuj (aśvayuk type): `yuj_kvin_samAsa` with `?samAsa` tag blocks nUM; SK257 pattern |
| 377 | 8.2.62 | क्विन्प्रत्ययस्य कुः | ku-sub for kvin stems at pada-end: j→g (then 8.4.56→k), Y(ñ)→N(ṅ), ś-path (8.2.36 S→ṣ, 8.2.39 ṣ→ḍ, then here q→g); gives ṛtvik, srak, yuṅ, dik. **PARTIAL**: condition covers only cu/S/q; c-final stems (dadhṛc, kruñc, añc) need extension when added |
| 378 | 8.2.30 | चोः कुः | c/ch/j/jh/ñ at pada-end → k-group |
| 379 | 6.3.128 | विश्वस्य वसुराटोः | viśva pūrva-pada final a→ā before vasu or rāj+kvip (= rāṭ) in compound; viśvāvasu, viśvārāṭ. Requires ?samAsa/?vasu/?rAj tag propagation in join_objects() |
| 380 | 8.2.29 | स्कोः संयोगाद्योरन्ते च | s/k deletion from conjunct-initial at pada-end. Test pratipadika: √takṣ+kvip (`takz_kvip`); nom sg taṭ/taḍ via k-deletion + 8.2.39 ṣ→ḍ + 8.4.56 ḍ→ṭ |
| 381 | 7.2.106 | तदोः सः सावनन्त्ययोः | Non-final t/d of tyadAdi → s before su (nom sg m); tad→saḥ, etad→eṣaḥ, tyad→syaḥ, adas→asa (→asau via SK437) |
| 382 | 7.1.28 | ङेप्रथमयोरम् | For yuṣmad/asmad: ṅe (dat sg) and prathamā (nom sg su) suffix → am; enables tvam/aham nom sg formation with SK384+SK385 |
| 384 | 7.2.94 | त्वाहौ सौ | For yuṣmad/asmad: mparyanta (up to m portion) → tv / ah before su (nom sg); two YAML blocks (7.2.94 for yuzmad→tv, 7.2.94.1 for asmad→ah) |
| 385 | 7.2.90 | शेषे लोपः | For yuṣmad/asmad: lopa of final d in all vibhakti positions (śeṣa = remainder after mparyanta substitution); yields yuzma-/asma- oblique base; nom sg: tvam, aham |
| 386 | 7.2.92 | युवावौ द्विवचने | Dual mparyanta: yuzmad→yuv, asmad→Āv (preserving trailing a); two YAML blocks (7.2.92 yuzmad, 7.2.92.1 asmad); base for all dual forms |
| 387 | 7.2.88 | प्रथमायाश्च द्विवचने भाषायाम् | Nom du suffix O → ām for yuzmad/asmad; overrides SK392 (7.2.89); yuvām, āvām |
| 388 | 7.2.93 | यूयवयौ जसि | Nom pl mparyanta: yuzmad→yūy, asmad→vay (drops trailing a); two YAML blocks; with SK382 (jas→am): yūyam, vayam |
| 389 | 7.2.97 | त्वमावेकवचने | All-sg mparyanta: yuzmad→tv, asmad→m (preserving trailing a for SK392/393 to act on); two YAML blocks; blocked by SK384 (nom sg), SK394 (dat sg), SK392 (vowel-initial) |
| 390 | 7.2.87 | द्वितीयायां च | Acc ā-ādeśa: suffix am/au → ām for yuzmad/asmad in dvitīyā (not pl); overrides SK392 (7.2.89); tvām, mām, yuvām, āvām |
| 391 | 7.1.29 | शसो न | Acc pl śas → n for yuzmad/asmad; SK393 then fires (l=a vowel, r=n hal) → ā; yuṣmān, asmān |
| 392 | 7.2.89 | योऽचि | y-ādeśa (a→ay) before vowel-initial suffix for yuzmad/asmad; overrides SK389 (7.2.97); tvayā, mayā, tvayi, mayi, yuvayoḥ, āvayoḥ |
| 393 | 7.2.86 | युष्मदस्मदोरनादेशे | ā-ādeśa (dirgha) for yuzmad/asmad before hal-initial suffix (excludes Byas for short-a dat/abl pl); yuṣmābhiḥ, asmābhiḥ, yuvābhyām, āvābhyām, yuṣmāsu, asmāsu, yuṣmān, asmān |
| 394 | 7.2.95 | तुभ्यमह्यौ ङयि | Dat sg mparyanta+suffix: yuzmad→tuBhy, asmad→mahy; ṅe→am; overrides SK389; tubhyam, mahyam |
| 395 | 7.1.30 | भ्यसोभ्यम् | Dat/abl pl Byas → Byam for yuzmad/asmad; SK393 excluded (?!Byas) keeping short a; yuṣmabhyam, asmabhyam |
| 396 | 7.1.32 | एकवचनस्य च | Abl sg at-ādeśa: full replacement → tvat (yuzmad), mat (asmad); overrides SK389/SK393/SK392 |
| 397 | 7.1.31 | पञ्चम्या अत् | Abl pl at-ādeśa: full replacement for ?Byas+?pancamI → yuzmAt, asmAt; wins over SK395 (71031 > 71030 SPSP) |
| 398 | 7.2.96 | तवममौ ङसि | Gen sg full replacement → tava (yuzmad), mama (asmad); overrides SK389/SK393/SK392 |
| 399 | 7.1.27 | युष्मदस्मद्भ्यां ङसोऽश् | yuzmad/asmad + gen sg Nas: suffix "as" → "a"; fires after SK398 which has higher _aps_num; junction tava+a→tava, mama+a→mama |
| 400 | 7.1.33 | साम आकम् | Gen pl Am → Akam; SK385 then d-lopa; sandhi a+A→A → yuzmAkam, asmAkam |
| 404 | 8.1.20 | युष्मदस्मदोः षष्ठीचतुर्थीद्वितीयास्थयोर्वांनावौ | yuzmad/asmad du gen/dat/acc → vāṃ/nau (optional) before pada; vibhakti tags disambiguate syncretic du forms |
| 405 | 8.1.21 | बहुवचनस्य वस्नसौ | yuzmad/asmad pl gen/dat/acc → vaḥ/naḥ (optional) before pada |
| 406 | 8.1.22 | तेमयावेकवचनस्य | yuzmad/asmad sg gen/dat → te/me (optional) before pada |
| 407 | 8.1.23 | त्वामौ द्वितीयायाः | yuzmad/asmad sg acc → tvā/mā (optional) before pada |
| 414 | 6.4.130 | पादः पत् | pAda → pad (shorten ā→a) when anga is bha; applies to compound pAd-final stems (supAd etc.); inst/dat/abl/gen/loc sg + acc/gen pl all show pad- base |
| 415 | 6.4.24 | अनिदितां हल उपधायाः क्ङिति | anidita hal-stem: drop nasal upadhā (Y=ñ or n) before kit/Ṅit krit suffix; fires at (aYc_u\|kvin) window; aYc → ac; enables dynamic añcatir derivation |
| 416 | 6.4.138 | अचः | delete 'a' of añc (post-SK415 form 'ac') in bha-anga context; ll:'a' condition excludes prAc (long A); ?!udanc excludes ud-prefix (SK420 apavāda); pratyac/tiryac bha forms use pratīc/tiryc base |
| 417 | 6.3.138 | चौ | lengthen final vowel of preceding member before añc reduced to 'c'; fires at (prefix\|c_result) after SK416; prati→pratI, pra→prA; yaṇ (6.1.77) blocked by akṛtavyūhā paribhāṣā |
| 418 | 6.3.92 | विष्वग्देवयोश्च टेरद्र्यञ्चतावप्रत्यये | ṭi→adri before añcatir (viṣvag/deva/tad/yad/kim/etad/idam/adas/sarva); ticAdesha_adri helper; luk_sup propagates sarvanAma→sarvanAma_pada; bahiranga:1 fires before SK417 |
| 420 | 6.4.139 | उद ईत् | apavāda of SK416: ud+añc in bha → substitute ī for 'a' of ac (udac→udIc); overrides: 6.4.138; ?udanc tag (via in_udanc helper) identifies ud compounds; fixes udac bha forms |
| 421 | 6.3.93 | समः समि | sam- → sami- before añcatir; bahiranga:1 fires before SK417; samyañc paradigm: samīcā bha via SK417 i→ī |
| 422 | 6.3.95 | सहस्य सध्रिः | saha- → sadhrī- before añcatir; bahiranga:1; sadhryañc paradigm; SK417 dirgha(ī)=ī no-op → sadhrīcā bha |
| 425 | 6.4.14 | अत्वसन्तस्य चाऽधातोः | upadhā dīrgha for u-it pum anga ending in -at (matup/ktavatu) or -as (Iyasun) before su (nom sg), not sambuddhi; bahiranga:3 fires before nUM; dhīmān, gomān |
| 427 | 7.1.78 | नाभ्यस्ताच्छतुः | Blocks nUM for abhyasta+śatṛ (–at) stems; apavāda of SK361 (7.1.70); condition: ?abhyasta + ?Satf; jakshat, jAgrat (and other jakshi-class) nom sg = plain -at form (no -an) |
| 428 | 6.1.6 | जक्षित्यादयः षट् | Tags 7 jakshi-class roots as inherently abhyasta: jakzat (SLP1 z=ṣ), jAgrat, daridrat, cakAsat, SAsat, dIDyat, vevyat; its=["f"]+other_tags=["Satf","abhyasta"] in pratipadika.py |
| 430 | 6.3.91 | आ सर्वनाम्नः | ā-substitution for sarvanāma pūrva-pada before dṛg/dṛś/vat compounds; creates tādṛk/tādṛśa forms from tyadAdi + dfS + kvin/kaY |
| 431 | 8.2.63 | नशेर्वा | optional kutva at pada-end for ?naS (naś+kvip); apavāda of SK294 (8.2.36); two pakṣas: nak/nag (kutva) and naṭ/naḍ (ṣatva); naś_kvip pratipadika added |
| 433 | 8.2.76 | र्वोरुपधाया दीर्घ इकः | upadhā-dīrgha for r/v-final dhātu upadhā-ik before pada-end; r/v-final dhātu stems (gir, pur etc.) get long vowel in nom/voc sg |
| 434 | 8.3.58 | नुम्विसर्जनीयशर्व्यवायेऽपि | ṣatva with vyavāya: s→ṣ after iṇ/ku even when num(M)/visarga(H)/śar(S/z/s) intervenes; ādeśa/pratyaya context; dhanus nom/acc plu dhanūṃṣi |
| 435 | 6.4.131 | वसोः संप्रसारणम् | samprasāraṇa v→u + ṣatva (s→ṣ/z) in bha for ?vasAnta (kvasu) stems; viduṣaḥ/ā/e/oḥ/ām bha forms of vidvas |
| 436 | 7.1.89 | पुंसोऽसुङ् | s→as (asun, u-it) before sarvānāmasthāna for ?puMs; SK425+SK361 give pumān nom sg; bha forms: puṃsaḥ/ā etc. |
| 440 | 8.2.34 | नहो धः | h→dh (D) before jhal or at pada-end for ?nah stems; upānat nom sg (via 8.4.56), upānadbhyām du/pl |
| 441 | 7.2.110 | यः सौ | idam + strī before su: lc → "iya" (idam f nom sg iyam); fires on ?idam+?strI before ?su; overrides 7.2.109; manually implemented |
| 442 | 7.4.48 | अपो भि | p→t before bhi-initial suffix for ?ap (nityabahuvacana feminine); 8.4.53 gives t→d before voiced bh → adbhiḥ, adbhyaḥ |
| 443 | 8.2.68 | अहन् | n→ru at pada-end for ?ahan (neuter day stem); ahaḥ nom/acc/voc sg via ru→visarga; apavāda of 8.2.7 (n-lopa) |
| 444 | 7.1.79 | वा नपुंसकस्य | Optional nUM for neuter abhyasta Śatṛ stems before sarvnāmasthāna (plural only); apavāda of SK427 (7.1.78); ददन्ति/ददति both valid for neuter pl of dadat |
| 445 | 7.1.80 | आच्छीनद्योर्नुम् | Optional nUM for śatṛ stems before SI (neuter dual, via 7.1.19 O→SI) and nadī-type feminine (lp ?nadI); SK446 overrides for ?Sap/?Syan making nUM mandatory |
| 446 | 7.1.81 | शप्श्यनोर्नित्यम् | Mandatory nUM for class 1 śap (?Sap) and class 4 śyan (?Syan) śatṛ stems before SI/nadī; overrides SK445; class 6 (?Sa) remains optional via SK445 |
| 447 | 1.1.37 | स्वरादिनिपातमव्ययम् | svarAdi gaṇa and nipAta words get avyaya saṁjñā; enables SK452 sup-deletion |
| 452 | 2.4.82 | अव्ययादाप्सुपः | sup suffixes deleted after avyaya; all vibhakti forms identical to stem |
| 454 | 4.1.4 | अजाद्यतष्टाप् | a-final (l:at) OR ?ajAdi + strI_abs → Ap (TAp); all 34 gaṇa members in pratipadika.py; tests: rAma_A, aja_A, kokila_A, SUdra_A, kruYc_A, uzRih_A. Also covers tyadAdi/kim feminine via SK441/SK440 commentary ("त्यदाद्यत्वं टाप्"): 7.2.102/103/109 extended to fire before ?strI_abs (in addition to ?viBakti), exposing a short-a stem to SK454; SK454 sets +TAp_added on olp so 7.2.102/103 don't re-fire post-TAp (et+Am after 6.1.107). Tests: tad_strI, etad_strI, yad_strI, kim_strI (sā/tā/etā/yā/kā paradigms) |
| 455 | 4.1.6 | उगितश्च | uk-it (u/ū/ṛ/ṝ/ḷ) + strI_abs → NIp; tests: pacat_NI (f-it, nUM → pacantī), Bavat_uNI (u-it, no nUM → BavatI) |
| 456 | 4.1.7 | वनो र च | van-final stems (vanip/kvanip/Dvanip) + strI_abs → NIp and final n→r; e.g. Sf+vanip → Sarvan → SarvarI (vārttikas "vano na haśaḥ" and "bahuvrīhau vā" deferred) |
| 457 | 4.1.8 | पादोऽन्यतरस्याम् | pAd-final compound stem + strI_abs → optional NIp; e.g. dvi+pAd → dvipadī (NIp+SK414) ~ dvipāt (no-NIp) |
| 459 | 4.1.11 | मनः | man-final stems → ṅīp blocked (apavāda to 4.1.5); सीमन्+strI_abs → halanta n-stem feminine सीमा |
| 460 | 4.1.12 | अनो बहुव्रीहेः | an-final bahuvrīhi (?bahuvrIhi tag) → ṅīp blocked (apavāda to 4.1.5/4.1.7); बहुयज्वन्→बहुयज्वा |
| 461 | 4.1.13 | डाबुभाभ्यामन्यतरस्याम् | optional DAp after man-final / an-bahuvrīhi; DAp q-it → ṭi-lopa (6.4.143) → ramā-type ā-stem (सीमे, बहुयज्वे) |
| 462 | 4.1.28 | अन उपधालोपिनोऽन्यतरस्याम् | optional ṅīp for an-final upadhālopin bahuvrīhi (re-permits ṅīp SK460 blocked); ṅīp ṅit → 6.4.134 al-lopa + śacutva → बहुराज्ञी; $$upaDAlopI excludes बहुयज्वन् |
| 463 | 7.3.44 | प्रत्ययस्थात्कात्पूर्वस्यात इदाप्यसुपः | idādeśa: 'a' before 'k' of a pratyaya (?ka_pratyaya stems via kap/kan) → 'i' when Ap follows. sarva+kan+strI_abs → sarvaka+Ap → सर्विका; parivrAjaka→परिव्राजिका. bahiranga:1 (beats 6.1.101 savarṇa-dīrgha). $$aka_anta + xform lc[:-2]+"ik". asuwapaH (असुपः) implemented via ?!bahuvrIhi guard: बहुपरिव्राजका takes no idādeśa |
| 464 | 7.3.45 | न यासयोः | blocks 7.3.44 for yad-/tad-derived ka-stems (yad→ya, tad→ta via 7.2.102, +kan → yaka/taka). $$yas_ka_anta (yaka/taka/saka). yakā, takā (nom sg sakā via 7.2.106; tyadAdi propagated through kan) |
| 469 | 4.1.14 | अनुपसर्जनात् | adhikāra only (no YAML rule). Establishes तदन्तविधि for the strī affixes (lets SK470 read "stem ending in" the affixes) and the anupasarjana scope (naturally honoured — strī affixes attach to the head stem) |
| 470 | 4.1.15 | टिड्ढाणञ्द्वयसज्दघ्नञ्मात्रच्तयप्ठक्ठञ्कञ्क्वरपः | ṅīp for a-final taddhita stems (apavāda to 4.1.4 ṭāp). Named affixes via ?NIp_taddhita; ṭiṭ via the +w it-marker (propagated through the krt/tadDita setIt loop). Working — **all 12 affixes**: ṭiṭ (कुरुचरी via wac), ḍha (सौपर्णेयी), aṇ (ऐन्द्री), añ (औत्सी), dvayasac/daghnac/mātrac (ऊरुद्वयसी/ऊरुदघ्नी/ऊरुमात्री), tayap (पञ्चतयी), ṭhak (आक्षिकी), ṭhañ (लावणिकी), kañ (यादृशी, reuses kaY), kvarap (नश्वरी). Supporting rules: 7.3.50 (ṭha→ika), 7.1.2 ḍh→eya arm, 7.2.118 (k-it ādivṛddhi), and the 1.4.18 -pada fix |
| 471 | 4.1.16 | यञश्च | ṅīp after yañ-final (?yaY), apavāda to 4.1.4. gārgya → +ṅīp → SK472 → गार्गी |
| 472 | 6.4.150 | हलस्तद्धितस्य | taddhita ya-kāra after hal elided before ṅīp ī. General over taddhita ya-affixes (yat/ṣyañ/yañ), guarded by ?tadDita_ya so a base-internal 'y' is not elided (विद्या+अण्→वैद्य → वैद्यी, not वैदी — SC Vasu). **Self-sufficient condition (lp ends hal+y+a, l='a'): the rule detects the upadhā 'y' directly on the snapshot, not via 6.4.148's output**. xform `lc: lc[:-1]` drops the 'y'. With 6.4.22 asiddhavat (see below), 6.4.148 and 6.4.150 fire against the same gārgya snapshot; their diffs compose: 148 drops 'a', 150 drops 'y' → गार्ग, merge with ī → गार्गी. helper `hal_taddhita_ya_upaDa(lp)` |
| 473 | 4.1.17 | प्राचां ष्फ तद्धितः | (no YAML rule) — optional ष्फ taddhita after yañ. The affix `sPa` is defined in pratyaya.py (its=["z"]); tests compose [..., yaY_t, sPa, strI_abs] explicitly. Surface test गार्ग्यायणी now works via the 6.4.22 ābhīya asiddhavat |
| 474 | 1.3.6 | षः प्रत्ययस्य | (saṁjñā only, no YAML rule) — affix-initial ष is an it. Encoded directly in each pratyaya's `its` list (e.g. `sPa = Pratyaya("Pa", its=["z"], ...)`) |
| 475 | 7.1.2 | आयनेयीनीयियः फढखछघां प्रत्ययादीनाम् | All 5 arms implemented via `phaDhakhachagha_adesha`: फ→आयन्, ढ→एय्, ख→ईन्, छ→ईय्, घ→इय्. **Now fully tested**: ḍh-arm (सुपर्णा+ढक् → सौपर्णेयी); फ-arm (गार्ग्यायणी / लौहित्यायनी / कौरव्यायणी) via SK473/476/477 |
| 476 | 4.1.18 | सर्वत्र लोहितादिकतन्तेभ्यः | (no YAML rule) — adhikāra-style. In all schools (sarvatra, not only Eastern Grammarians), ष्फ obligatorily attaches after stems of the lohitādi gaṇa and after stems formed by the kaN affix. Modelled like SK473: the test composer includes `sPa` for such bases. Surface test: लौहित्यायनी = [lohita, yaY_t, sPa, strI_abs] |
| 477 | 4.1.19 | कौरव्यमाण्डूकाभ्यां च | (no YAML rule) — adhikāra-style. ष्फ obligatorily attaches after कौरव्य (kuru+yaY) and माण्डूक. Surface test: कौरव्यायणी = [kuru, yaY_t, sPa, strI_abs] (ṇatva via the r of kuru) |
| 478 | 4.1.20 | वयसि प्रथमे | ṅīp after an a-final stem denoting "early age" (prathama vayas); apavāda to 4.1.4 ṭāp. Stems carry ?vayasi_prathama (kumAra, kiSora, barkara) → कुमारी / किशोरी / बर्करी. Surface test: कुमारी = [kumAra, strI_abs] |
| 479 | 4.1.21 | द्विगोः | ṅīp after an a-final Dvigu samāsa; apavāda to 4.1.4. New ?dvigu tag (analogous to ?bahuvrIhi) set by the test composer via `in_context(in_compound(loka), "dvigu")` and propagated through `join_objects()` (paninian_object.py allowlist). Surface tests: त्रिलोकी = [as_purva_pada(tri), luk_sup, in_context(in_compound(loka), "dvigu"), strI_abs]; पञ्चाश्वी = same shape with aSva — exercises the 4.1.4.2 niyama (aśva has ?ajAdi but not ?ajAdi_in_Dvigu, so 4.1.4.2 does not fire and SK479 wins) |
| – | 4.1.4.1 | अजाद्यतष्टाप् (ajādi-prabalatva, non-Dvigu) | Vārttika-style apavāda: a ?ajAdi stem takes ṭāp, overriding the non-Dvigu ṅīp rules (`overrides: [4.1.6, 4.1.15, 4.1.16, 4.1.20]`). Paired with samāsa-gated `_propagate(last, ["ajAdi", "ajAdi_in_Dvigu"])` in `join_objects()` so the tag rides from the uttara-pada to a compound. The ?ajAdi arm formerly in 4.1.4 was removed; 4.1.4 now keeps only its general `l: at` arm. The 4.1.21 override moved to 4.1.4.2 below (Vasu's N.B. on gaṇa items 19–20) |
| – | 4.1.4.2 | अजाद्यतष्टाप् (ajādi-prabalatva over 4.1.21 Dvigu) | Narrow apavāda over SK479: fires only for the phala/puṣpa compound-class subgroup of the ajādi-gaṇa (items 15–26 + Pala/anIka), tagged ?ajAdi_in_Dvigu. Vasu's N.B. on items 19–20: "त्रिफला when a Dvigu Compound forms its feminine as त्रिफला". Other ajādi members (e.g. aśva, item 5) override 4.2.63 nish — which doesn't apply in Dvigu — so SK479 ṅīp wins for them in Dvigu, giving पञ्चाश्वी for samāhāra-Dvigu of aśva per Vasu/SK on SK480. Drives त्रिफला (tri+Pala) and त्र्यनीका (tri+anIka — anīka treated as phala-class by analogy) |
| 480 | 4.1.22 | अपरिमाणबिस्ताचितकम्बल्येभ्यो न तद्धितलुकि | Niṣedha to SK479 for an a-final Dvigu compound with a luk'd taddhita on top: blocks ṅīp (selects ṭāp via `orp: =Ap`) when the uttara-pada is NOT ?parimARa, OR is one of बिस्त/आचित/कम्बल्य (?bistAdi). `?!kARqa` excludes kāṇḍa-final stems (SK481 handles them); puruṣa is NOT excluded — SK482 optionally re-enables ṅīp on top. Built on a new `luk_tadDita` Pratyaya (empty, ?tadDita+?luk_tadDita); ?luk_tadDita rides through the (aṅga, luk_tadDita) merge via the aṅga-gated `_propagate(last, [...])`, and the semantic class tags ride from both first and last in `_propagate`. Drives पञ्चाश्वा, द्विबिस्ता, द्व्याचिता, द्विकम्बल्या; counters: द्व्याढकी (ādhaka = parimāṇa), trilokI (no luk) |
| 481 | 4.1.23 | काण्डान्तात्क्षेत्रे | Niyama on SK480 for kāṇḍa-final Dvigus: blocks ṅīp (selects ṭāp) only in the kṣetra ('field') sense via a semantic `?kzetre` tag attached by the test composer (`in_context(..., "kzetre")`). Non-kṣetra kāṇḍa-Dvigus fall through to SK479 → ṅīp (द्विकाण्डी रज्जुः). Drives द्विकाण्डा क्षेत्रभक्तिः |
| 482 | 4.1.24 | पुरुषात्प्रमाणेऽन्यतरस्याम् | Vibhāṣā: optionally re-enables ṅīp for puruṣa-final Dvigus in the pramāṇa sense via semantic `?pramARe` tag (`in_context(..., "pramARe")`). `overrides: 4.1.21` (NOT 4.1.22) — if SK482 overrode 4.1.22 the optional-fired branch would disable SK480 on v0 (engine's optional-overrides disabling in `antaranga_prakriya.py:712-715`), so the SK482-skip branch would lose its fallback. By overriding 4.1.21 instead, the skip branch leaves SK480 free to fire → ṭāp (द्विपुरुषा); the fire branch wins over SK480 by higher _aps_num → ṅīp (द्विपुरुषी). Both Vasu alternants produced. Non-pramāṇa puruṣa-Dvigu falls to SK480 only → द्विपुरुषा |
| 483 | 5.4.131 | ऊधसोऽनङ् | anaṅ substitute for final ūdhas in bahuvrīhi feminine: surface = replace final `s` of UDas with `n` (UDas → UDan). bahiranga: 1 fires before NIz/NIp selection. After SK484/485 adds the ī suffix, SK234 (6.4.134) drops the upadhā `a` of -an → kuRqoDnī, GhaToDnī, dvyUDnī, atyUDnī. New stem UDas tagged ?uDanta |
| 484 | 4.1.25 | बहुव्रीहेरूधसो ङीष् | ṅīṣ (NIz) after a bahuvrīhi ending in ūdhas (now ūdhan post-SK483), feminine. `overrides: [4.1.4, 4.1.13]` blocks the ṭāp/ḍāp candidates Vasu names. Drives कुण्डोध्नी and घटोध्नी; new test stems `kuRqa`, `Gawa` (ṭ in SLP1 = `w`) |
| 485 | 4.1.26 | संख्याऽव्ययादेर्ङीप् | Apavāda to SK484 (ṅīṣopavāda): NIp instead of NIz when the bahuvrīhi begins with a saṃkhyā or avyaya. Two condition arms (saṃkhyādi / avyayādi) read ?saMKyAdi / ?avyayAdi attached to UDas via test composer `in_context`. Drives द्व्यूध्नी (saṃkhyādi) and अत्यूध्नी (avyayādi; new avyaya stem `ati`) |
| 486 | 4.1.27 | दामहायनान्ताच्च | Bahuvrīhi beginning with saṃkhyā ending in दामन्/हायन: NIp in feminine. Two arms: (a) ?dAman — no semantic restriction (द्विदाम्नी; SK234 a-lopa); (b) ?hAyana + ?vayasi — restricted to age sense (द्विहायनी via 6.4.148 a-lopa). Non-age hāyana falls through to 4.1.4 ṭāp (द्विहायना). New stems `dAman`, `hAyana`. `overrides: [4.1.4]` |
| – | 4.1.27.1 | (vārttika) त्रिचतुर्भ्यां हायनस्य णत्वं वयोवाचकस्यैव | Upadhā n→ṇ in hāyana when pūrva-pada is tri/catur AND age (?vayasi) sense. `xform: lc: lc[:-1]+str("R")` makes hāyana → hāyaṇa; SK486 then NIp; 6.4.148 a-lopa → trihāyaṇī, caturhāyaṇī. ?triCatur attached via test composer `in_context`. bahiranga: 1 fires before SK486 (bahiranga: 2). Non-age trihāyana → no vārttika, no SK486 → 4.1.4 ṭāp → त्रिहायना (Vasu's exact शाला example). Engine adjustment in the pūrvāparayoḥ section: 6.1.87 (आद्गुणः) now strips `sarvanAmasTAna` from the post-guṇa suffix (`orp: -sarvanAmasTAna`), so 6.4.8 does not re-fire on the n-final surface produced by ṭāp + guṇa (hāyan|e). Broader pūrvāparayoḥ refactor pending — captured as a TODO |
| 487 | 4.1.29 | नित्यं संज्ञाछन्दसोः | Mandatory NIp on upadhā-lopin an-bahuvrīhi in saṃjñā or chandas. Apavāda to SK462 (4.1.28); `overrides: [4.1.4, 4.1.12, 4.1.13, 4.1.28]`. ?saMjYA / ?Candas attached via test composer in_context; reuses `$$upaDAlopI` from SK462. Drives अतिराज्ञी (saṃjñā example) |
| 488 | 4.1.30 | केवलमामकभागधेयपापापरसमानार्यकृतसुमङ्गलभेषजाच्च | Mandatory NIp for nine `?keval_Adi` stems in saṃjñā/chandas. `overrides: 4.1.4`. Positive arm → केवली / मामकी / सुमङ्गली; laukika negative arm → 4.1.4 ṭāp + SK463 idādeśa for `?ka_pratyaya`-tagged mAmaka → मामिका. Niyama-blocker 4.1.30.1 (मामकग्रहणं नियमार्थम्) overrides SK470 for ?mAmaka outside saṃjñā/chandas — currently inert (mAmaka lacks ?NIp_taddhita) but forward-compatible |
| 489 | 4.1.32 | अन्तर्वत्पतिवतोर्नुक् | नुक् augment (single 'n' at end of stem) on antarvat / pativat in feminine. Treated as single irregular pratipadikas (?antarvat_pativat). bahiranga: 1 left-substitution `lc: lc+l+str("n"), l: null` appends n; SK453 (4.1.5) at bahiranga 2 then supplies NIp → अन्तर्वत्नी / पतिवत्नी. Semantic restriction (?garBiNi / ?jIvadBartfka) not encoded — see Skipped table |
| 490 | 4.1.33 | पत्युर्नो यज्ञसंयोगे | i→n on plain pati before NIp. Condition `?pati + ?!samAsa`; bahiranga: 1. SK453 then supplies NIp → पत्नी. Semantic restriction (?yajYasaMyoga) not encoded — see Skipped table |
| 491 | 4.1.34 | विभाषा सपूर्वस्य | i→n on pati when uttara-pada of compound. Condition `?pati + ?samAsa`; bahiranga: 1. Vibhāṣā implemented as mandatory in this batch (the non-substituted गृहपतिः fork is deferred). Drives गृहपत्नी declining as the textbook nadī. Required guarding 1.4.7 (all three arms) and 1.4.8 with `rp: ?!strI`, and 1.4.8 additionally with `lp: ?!strI`, so Ghi-saṃjña never lands on the feminine path |
| 492 | 4.1.35 | नित्यं सपत्न्यादिषु | Mandatory i→n for ?sapatnyAdi class. `overrides: [4.1.33, 4.1.34]`. Pre-substituted stems sapati / ekapati / vIrapati (Q3 deferral: समानस्य सभावोऽपि niyama realised by registering सपति directly rather than a paired left-substitution). Drives सपत्नी / एकपत्नी / वीरपत्नी |
| 6.4.22 | 6.4.22 | असिद्धवदत्राभात् | (out-of-SK-order, engine-level) ābhīya asiddhavat — partial. Static-samanāśraya peers {6.4.148, 6.4.150, 6.4.134} are pair-wise asiddha to each other. `view()` walks past peer ancestors at the same window (returns the pre-section snapshot for condition AND xform input); `_compose_abhiya` derives a per-snapshot-position diff of `operate(snapshot)` vs `snapshot` and composes it with prior peer diffs into the current state — so both peers' edits land in the merged output. Unlocks the ṣpha cluster (गार्गी uses 148+150 composition; गार्ग्यायणी/लौहित्यायनी/कौरव्यायणी block 134 from seeing 148's output). The वुग्युट… vārttika and broader scope are deferred — see Skipped table |
| 423 | 6.3.94 | तिरसस्तिर्यलोपे | Natural — pre-applied: tiras- → tiry- before añcatir with a-lopa; tiryac stored as weak form; tests pass |
| 437 | 7.2.107 | अदस औ सुलोपश्च | Out-of-SK-order, added with SK381: adas nom sg — final a→au (O), su deleted; asa+su→asau=असौ |
| 419 | 8.2.80 | अदसोऽसेर्दादु दो मः | adas sg/du/pl (excl. inst sg, nom/acc du handled by 6.1.102): fires on ?pada ?adas — amu sg (acc amum, dat/abl/gen/loc sg via ṣatva), amU du (nom/acc amū), amī pl (nom/acc/voc via SK438); _special_siddha(82080,14007) and (82080,73120) for 1.4.7+7.3.120 |
| 438 | 8.2.81 | एत ईद्बहुवचने | adas nom/acc/voc pl: pada-level rule, ade→amI (amī); out of SK order |
| 439 | 8.2.3 | न मु ने | adas inst sg amunā: fires at ada\|wA, overrides 7.1.12+6.1.101, sets ?pada on ada enabling SK419; _special_siddha(82080,14007/73120) propagates amu→Gi→nā; out of SK order |
| 656 | 1.2.48 | गोस्त्रियोरुपसर्जनस्य | go/strī in compound: hrasva |
| 847 | 6.4.146 | ओर्गुणः | o → guṇa (e) in anga before certain suffixes (apavāda) |
| 1075 | 7.2.117 | तद्धितेष्वचामादेः | before taddhita suffix beginning with ac: vṛddhi of first vowel of anga |
| 1076 | 7.2.118 | किति च | (out-of-SK-order) extends 7.2.117 ādivṛddhi to k-it taddhita affixes (`rp: [and, ?tadDita, +k]` → adivriddhi(lc)). Completes ṭhak (अक्ष→आक्ष) and ḍha (सुपर्ण→साौपर्ण) — both k-it, uncovered by 7.2.117 (ñṇit) |
| 1170 | 7.3.50 | ठस्येकः | (out-of-SK-order) ठ of a taddhita affix → इक. Drives SK470's ṭhak/ṭhañ arm (आक्षिकी/लावणिकी). |
| 2168 | 7.3.84 | सार्वधातुकार्धधातुकयोः | anga before sārvadhatuka/ārdhadhatuka: guṇa of final vowel (core verb guṇa rule) |
| 2189 | 7.3.86 | पुगन्तलघूपधस्य च | puganta or laghu-upadha anga before sārvadh/ārdh: guṇa of upadhā |
| 2217 | 1.1.5 | क्ङिति च | kit/ṅit suffix: no guṇa/vṛddhi substitution (blocks SK2168, SK254 etc.) |
| 2280 | 8.2.40 | झषस्तथोर्धोऽधः | jhaṣ before t/th: t/th → dh/dh (voiced aspiration assimilation) |
| 2282 | 7.2.116 | अत उपधायाः | a-upadhā anga before Ñit/Ṇit suffix: vṛddhi of upadhā a |
| 2335 | 8.3.13 | ढो ढे लोपः | ḍh before ḍh: lopa of first ḍh |

---

## Implemented Sutras (additional, with SK numbers)

These sutras are implemented in `sutras_antaranga.yaml`. SK numbers sourced from `sk_map.md`.

| SK | Sutra ID | Sutra | Forms affected |
|----|----------|-------|----------------|
*(All sutras with SK numbers have been moved to the SK-order table above.)*

---

## Skipped / Deferred Sutras

| SK | Sutra ID | Sutra | Reason | Affects |
|----|----------|-------|--------|---------|
| 55 | 8.4.48 | नादिन्याक्रोशे पुत्रस्य | Skipping for now | Vedic/accent |
| 56 | 8.4.50 | त्रिप्रभृतिषु शाकटायनस्य | Skipping for now | Śākaṭāyana option |
| 57 | 8.4.51 | सर्वत्र शाकल्यस्य | Skipping for now | Śākalya option |
| 58 | 8.4.52 | दीर्घादाचार्याणाम् | Skipping for now | Āchārya option |
| 75 | 6.1.85 | अन्तादिवच्च | Skipping for now | Sandhi edge case |
| 77 | 6.1.92 | वासुप्यापिशलेः | Skipping for now | Āpiśali dialect |
| 81 | 6.1.98 | अव्यक्तानुकरणस्यात इतौ | Skipping for now | Sound-imitation words |
| 82 | 6.1.99 | नाम्रेडितस्यान्त्यस्य तु वा | Skipping for now | Āmreḍita (reduplicated) words |
| 126 | 8.3.25 | मो राजि समः क्वौ | For later | kvip formations |
| 144 | 8.3.48 | कस्कादिषु च | For later | kaska-group ṣatva in compounds; structurally different from ru-sandhi cluster |
| 145 | 6.1.72 | संहितायाम् | Natural — saṃhitā adhikāra implicit in engine | FIXME comment in YAML; engine always operates in saṃhitā context for sandhi; no explicit rule block needed |
| 156 | 8.3.42 | तिरसोऽन्यतरस्याम् | Partial — non-gati tiras context (tiraḥ kṛtvā) not distinguishable with current tagging | tiras as non-gati adverb: no ṣatva (should stay tiraḥ) |
| 160 | 8.3.46 | अतः कृकमिकंसकुम्भपात्रकुशाकर्णीष्वनव्ययस्य | Partial — kāra and kāma are fixed-form pratipadika placeholders; kṛ/kam dhātu-derived kṛdanta forms (karaṇa, karman, kṛtya, kāmana, kāmya, …) not yet auto-tagged satva_kfkamkaMsAdi | all kṛt-derivative forms of √kṛ/√kam as uttarapada |
| 172 | 8.2.69 | रोऽसुपि | Partial — vārttikās not implemented | ahorUpam/ahorAtriH/ahorathantaram: the ru→o transformation IS wanted for these three specific words despite SK172 blocking it in general (vā rūpārttikam). Optional-r before pati-group (aharādInAM patyAdiSu vA rephaH) also deferred |
| 176 | 6.1.132 | एतत्तदोः सुलोपोऽकोरनञ्समासे हलि | Partial — nañsamāsa exception not implemented (akoH now handled) | anañsamAse: no H-deletion for nañ-compound forms like a-saH (requires compound-type condition not yet in DSL). akoH is handled by the rule's exact lc=sa/=eza match — ka-affix stems (saka/eṣaka) keep su-r; validated by manual_list.py SK176 akoḥ tests |
| 210 | 8.3.55 | अपदान्तस्य मूर्धन्यः | Natural — adhikāra comment only; no rule block in YAML | Retroflexion adhikāra header; actual ṇatva logic handled by SK235 (8.4.1) and SK212 (8.3.59) |
| 258 | 1.1.23 | बहुगणवतुडति सङ्ख्या | For later | saṃkhyā definition |
| 292 | 1.1.28 | विभाषा दिक्समासे बहुव्रीहौ | For later | dik-compounds |
| 321 | 7.1.74 | तृतीयादिषु भाषितपुंस्कं पुंवद्गालवस्य | For later | Gālava's option for neuter |
| 323 | 1.1.48 | एच इग्घ्रस्वादेशे | Handled elsewhere | `hrasva()` in paribhāṣā.py |
| 348 | 1.1.21 | आद्यन्तवदेकस्मिन् | Natural | Falls out of engine behaviour |
| 353 | 8.2.2 | नलोपः सुप्स्वरसंज्ञातुग्विधिषु कृति | Natural + special siddha | n-lopa in kṛt/kyac/kyaṇ contexts |
| 363 | 6.1.37 | न संप्रसारणे संप्रसारणम् | For later — kṛt/verbal only | blocks double samprasāraṇa; not needed for nominal declension (SK362's samprasArana_van produces no further samprasāraṇa candidate) |
| 373 | 3.2.59 | ṛtvigdadhṛksragdiguṣṇigañcuyujikruñcāṃ ca | Natural — handled via pratipadika pre-definitions | kvin formation rule. Stems from sutra compound (8): ṛtvij (m., j-final), dadhṛc (m., c-final, from √dhṛṣ via ścutva), sraj (f., j-final), diś (f., ś-final), uṣṇij (m., j-final), añcu-compounds (prāñc/pratyañc/udañc/tiryañc etc., ñc-final), yuj (m., j-final, nirupapada only per SK376), kruñc (m., ñc-final). SK commentary "कनावितौ": the suffixes KAN and ĀVIT are excluded — only kvin applies (not additional stems). Implemented: ftvij/sraj/yuj/diS. Deferred: dadhṛc (c-final), uṣṇij (j-final, same phonology as ftvij — trivial to add), kruñc (ñc-final), añcu-compounds (compound-specific, many forms). Extending to c/ñc-finals requires SK377 (8.2.62) condition and kvinKutva extension — see SK377 PARTIAL note |
| 374 | 3.1.93 | कृदतिङ् | Natural | kṛt saṃjñā definition; falls out of generator framework |
| 375 | 6.1.67 | वेरपृक्तस्य | Natural | kvin v-lopa inherent in pratipadika pre-formation (suffix already absent) |
| 383 | 7.2.91 | मपर्यन्तस्य | Natural | adhikāra scope indicator ("up to m"); scope encoded directly in SK384's xform (lc replaced = yuzm+a portion); no YAML rule needed |
| 401 | 8.1.16 | पदस्य | Natural | adhikāra — pada-context (preceding pada) constraint; implied once SK401/402 formally implemented; optional SK404–407 currently fire on any preceding pada |
| 402 | 8.1.17 | पदात् | Natural | adhikāra — same as SK401; preceding-pada constraint deferred |
| 403 | 8.1.18 | अनुदात्तं सर्वमपादादौ | For later — accent | unaccented rule; accent not modelled in generator |
| 408 | 8.1.24 | न चवाहाऽहैवयुक्ते | For later — pada enclitics | exception to SK404–407 with ca/vā/ha/aha/eva |
| 409 | 8.1.25 | पश्यार्थैश्चाऽनालोचने | For later — pada enclitics | exception: no enclitics with non-visual-perception verbs |
| 410 | 8.1.26 | सपूर्वायाः प्रथमाया विभाषा | For later — pada enclitics | optional pada-enclitics for certain nom constructions |
| 411 | 2.3.48 | सामन्त्रितम् | For later | vocative definition; no impact on pronoun declension forms |
| 412 | 8.1.72 | आमन्त्रितं पूर्वमविद्यमानवत् | For later — accent | vocative accent; accent not modelled |
| 413 | 8.1.73 | नामन्त्रिते समानाधिकरणे सामान्यवचनम् | For later | vocative co-referential number; not needed for basic paradigm |
| 424 | 6.4.30 | नाञ्चेः पूजायाम् | For later — exception | blocks n-lopa (SK415/6.4.24) for añcatir in honorific/pūjā context; no test coverage yet |
| 426 | 6.1.5 | उभे अभ्यस्तम् | Natural + manual tagging; dvitva engine not yet implemented | abhyasta saṁjñā for all forms resulting from reduplication (dadat, bibhrat, etc.); jakshi-class manually tagged via SK428 |
| 429 | 3.2.60 | त्यदादिषु दृशोऽनालोचने कञ्च | Natural — kañ/kvin falls out of existing infrastructure | kaY pratyaya implemented; SK430 (6.3.91) is the active sutra for tādṛk/tādṛśa forms |
| 432 | 3.2.58 | स्पृशोऽनुदके क्विन् | For later — kṛt framework pending | kvin after √spṛś in compounds (ghṛtaspṛk etc.); tested via compound pratipadika with existing kvin machinery |
| 448 | 1.1.38 | तद्धितश्चाऽसर्वविभक्तिः | For later — taddhita engine pending | avyaya saṁjñā for taddhita-ending words that lack full vibhakti paradigms (tasil and similar) |
| 449 | 1.1.39 | कृन्मेजन्तः | For later — kṛt engine pending | avyaya saṁjñā for kṛt suffixes ending in m or ec (smāram smāram, jīvase, pibadhai) |
| 450 | 1.1.40 | क्त्वातोसुन्कसुनः | For later — kṛdanta forms not yet generated | avyaya saṁjñā for gerunds/absolutives: ktvā (kṛtvā), tosun (udetoḥ), kasun (visṛpaḥ) |
| 451 | 1.1.41 | अव्ययीभावश्च | For later — avyayībhāva samāsa not yet implemented | avyaya saṁjñā for avyayībhāva compounds (adhihari, upakṛṣṇam etc.) |
| 453 | 4.1.3 | स्त्रियाम् | Natural — adhikāra scope marker; domain: prakfti covers it | All stripratyaya rules SK454+ |
| 456 | 4.1.7 | वनो र च | Partial — vārttikas pending | "vano na haśaḥ" (no NIp/n→r when van follows a haś-pratyāhāra consonant in the underlying dhātu, e.g. sahayudhvan f. = sahayudhvā) and "bahuvrīhau vā" (optional NIp in bahuvrīhi, e.g. bahudhīvarī ~ bahudhīvā via ḍāp) — deferred; require dhātu-history tracking and a bahuvrīhi tag respectively |
| 458 | 4.1.9 | टाबृचि | For later — requires ṛk-meter semantic context (ऋचि वाच्यायाम्) | TAp after pād-final feminine in the sense of an ṛk verse (द्विपदा ऋक्); engine has no semantic tracking, would emit a spurious द्विपदा for dvipAd_strI |
| 463 | 7.3.44 | प्रत्ययस्थात्कात्पूर्वस्यात इदाप्यसुपः | Partial — vārttikas pending (asuwapaH now implemented) | idādeśa implemented (sarvika, parivrAjaka). asuwapaH (no idādeśa when the aka-stem ends a bahuvrīhi, e.g. बहुपरिव्राजका नगरी) now handled via ?!bahuvrIhi guard — tested (bahuparivrAjaka_strI). Deferred: vārttikas (māmaka/naraka, dākṣiṇātya/ihatya) not handled |
| 465 | 7.3.46 | उदीचामातः स्थाने यकपूर्वायाः | For later — northern-grammarian variant | Optional id for the shortened-ā (केऽणः 7.4.13) when preceded by yak/ka (āryikā, caṭakikā). Needs the केऽणः ka-hrasva chain + preceding-yak detection; same ka-affix infra as SK463 plus extra context |
| 466 | 7.3.47 | भस्त्रैषाजाज्ञाद्वास्वा नञ्पूर्वाणामपि | For later — northern-grammarian variant | Optional id for the listed stems (bhastrā, eṣā, ajā, jñā, dvā, svā) and their nañ-compounds; lexically-restricted, needs the same shortened-ā chain |
| 467 | 7.3.48 | अभाषितपुंस्काच्च | For later — northern-grammarian variant | Optional id for abhāṣita-puṃska stems (gaṅgā→gaṅgikā); needs abhāṣita-puṃska semantic tagging |
| 468 | 7.3.49 | आदाचार्याणाम् | For later — northern-grammarian variant (Ācārya alternative) | ā-substitute alternative in the SK467 domain (gaṅgākā ~ gaṅgikā); builds on SK467 |
| 473 | 4.1.17 | प्राचां ष्फ तद्धितः | DONE — moved to Implemented | गार्ग्यायणी etc. now derive via partial 6.4.22 ābhīya asiddhavat |
| — | (vārttika) | वुग्युटावुवङ्यणोः सिद्धौ वक्तव्यौ | Deferred — exception to 6.4.22 | The four operations vuk-augment, yuṭ-augment, uvaṅ, yaṇ are siddha (not asiddha) within the ābhīya section. Not yet implemented because the current static-samanāśraya list only enables asiddhavat for {6.4.148, 6.4.150, 6.4.134} and these don't interact with vuk/yuṭ/uvaṅ/yaṇ. Add a sidhya carve-out (or analogous `_special_siddha` entry) when extending the asiddhavat scope |
| — | 6.4.22 | असिद्धवदत्राभात् (broader) | Partial — only static-samanāśraya pairs | Current scope is limited to three rule pairs (148–150, 148–134). The full Pāṇinian principle covers the entire ābhīya section (6.4.22…end of 6.4) with dynamic samanāśraya. Broader rollout deferred — needs case-by-case verification because some same-window ābhīya pairs (e.g. 6.4.128 optional + 6.4.133 samprasāraṇa) are NOT samanāśraya and over-firing them produces conflicts |
| — | 4.1.31 | रात्रेश्चाजसौ | Not catalogued in SK | NIp after रात्रि in chandas/saṃjñā except jas. Sits between SK488 (4.1.30) and SK489 (4.1.32) in Ashtadhyayi order but Bhaṭṭoji Dīkṣita gives it no SK number. Vedic-context rule; deferred |
| 488 | 4.1.30 | केवलमामकभागधेयपापापरसमानार्यकृतसुमङ्गलभेषजाच्च | Partial — broader mAmaka niyama vārttikas not implemented | The niyama-blocker 4.1.30.1 (मामकग्रहणं नियमार्थम्) is wired but currently inert (mAmaka stem lacks ?NIp_taddhita); other gaṇa-specific vārttikas mentioned in Vasu's commentary not implemented |
| 489 | 4.1.32 | अन्तर्वत्पतिवतोर्नुक् | Partial — semantic restriction not encoded; live samāsa derivation deferred | (1) The ?garBiNi / ?jIvadBartfka semantic restriction (अन्तर्वत् = pregnant, पतिवत् = husband-living) is not encoded — SK489 fires unconditionally on antarvat/pativat. (2) Properly a samāsa-context operation (antar+matup, pati+matup); implemented as single irregular pratipadikas because the engine cannot yet peek into left/right neighbours of a samāsa from inside a pratyaya-window rule. Full Paninian implementation deferred pending that engine capability |
| 490 | 4.1.33 | पत्युर्नो यज्ञसंयोगे | Partial — semantic restriction not encoded | The ?yajYasaMyoga semantic restriction (wife in sacrificial sense) is not encoded — SK490 fires unconditionally, over-generating पत्नी in the laukika sense |
| 491 | 4.1.34 | विभाषा सपूर्वस्य | Partial — vibhāṣā non-substituted fork deferred | (1) Implemented as mandatory (the non-substituted गृहपतिः fork is deferred — the current engine would generate a masc-style i-stem decl in feminine slot which over-generates). (2) acāra-kvip alternative reading (पत्नियौ, पत्नियः) not handled. (3) The pūrva-pada's identity/properties are not visible at evaluation time, only the presence of `?samAsa` on pati via in_compound(); full implementation needs engine support for left-context introspection. (NB the ?Gi-leak through samāsa merge that previously broke the 4 oblique-sg cells is fixed in this batch — 1.4.7/1.4.8 both carry `rp: ?!strI` and 1.4.8 also carries `lp: ?!strI`. The trace was obtained via `pytest --verbose-prakriya --tag-display` on gRhapatnI-cat-ek after forcing a sentinel-fail.) |

---

## Uncatalogued / Not Yet Planned

SK numbers ≤ 452 absent from both the implemented and skipped/deferred tables, and not found in `sutras_antaranga.yaml`. These are mostly paribhāṣā, Vedic, adhikāra headers, or rules naturally subsumed by the engine.

| SK | Sutra ID | Notes |
|----|----------|-------|
| 48 | 8.4.47 | anusvāra before visarga — engine-level |
| 49 | 1.1.56 | sthānivad paribhāṣā |
| 50 | 1.1.57 | sthānivad exception |
| 51 | 1.1.58 | sthānivad adeśa |
| 53 | 1.1.60 | sthānivad na |
| 62 | 1.3.9 | paribhāṣā |
| 68 | 6.1.84 | ekaḥ pūrvaparayoḥ — core sandhi principle, engine-level |
| 70 | 1.1.51 | ur aṇ raparaḥ |
| 79 | 1.1.64 | dhātulopa paribhāṣā |
| 83 | 8.1.2 | āmreḍita — natural; jakṣi-class manually tagged via SK428 |
| 91–99 | — | Vedic/pluta/pragṛhya rules |
| 102–110 | — | pragṛhya, Vedic |
| 128 | 1.3.10 | paribhāṣā |
| 168 | 8.3.18 | |
| 170 | 8.3.21 |Handled by SK67/8.3.19 |
| 171 | 8.3.22 | |
| 175 | 1.4.2 | vipratiṣedha paribhāṣā |
| 177 | 6.1.134 | |
| 178–190 | — | technical definitions: prātipadika, pratyaya, vibhakti, etc. |
| 192 | 2.3.49 | |
| 195 | 1.3.8 | |
| 200 | 6.4.1 | adhikāra (bhasya scope header) |
| 218–227 | — | sarvanāma subgroup definitions |
| 232 | 1.4.1 | |
| 233 | 6.4.129 | |
| 249 | 1.1.65 | |
| 251 | 1.2.41 | |
| 260 | 1.1.61 | |
| 262 | 1.1.62 | |
| 328 | 1.1.45 | |

---

## Test Coverage

All tests run from the `generator` branch: `cd sanskrit_parser/generator/test && pytest`

### Stems with full 8×3 vibhakti tables (`vibhaktis_list.py`)

| Stem | Linga | Class | Notes |
|------|-------|-------|-------|
| rAma | m | a-stem | Basic masculine |
| hari | m | i-stem (ghy) | |
| pati | m | i-stem (pati) | Standalone (not ghy) |
| saKi | m | i-stem (sakhi) | Special oblique stem sakhā |
| SamBu | m | u-stem (ghy) | |
| krozwu | m | u-stem (kroṣṭu) | Inflects like ṛ-stem |
| go | m | go-stem | |
| rE | m | rāy-stem | |
| pitf | m | ṛ-stem | |
| tvazwf | m | ṛ-stem (naptrādi) | |
| mAtf | m | ṛ-stem | |
| rAjan | m | n-stem | |
| mahat | m | t-stem (mahat) | |
| lih | m | h-stem | |
| duh | m | h-stem | |
| druh | m | h-stem | |
| pra_vAh | m | h-stem | Compound |
| anaquh | m | anaḍuh-stem | |
| turAsAh | m | h-stem | |
| div | m | v-stem (div) | |
| catur | m | catur | Numeral |
| tri | m | tri | Numeral |
| praSAm | m | m-stem | |
| kim | m | sarvanāma | Pronoun |
| idam | m | sarvanāma | Demonstrative |
| idam_anu | m | sarvanāma | idam in anuvādeśa |
| sarva | m | sarvanāma (a-stem) | |
| pAda | m | a-stem (pādādi) | Alternant bha-stem pad |
| yUza | m | a-stem (pādādi) | Alternant bha-stem yūṣṇ |
| viSvapA | m | kvip/ā-stem | |
| hAhA | m | ā-stem | Interjection |
| nadI | f | ī-stem (nadī) | |
| ramA | f | ā-stem (āp) | |
| rAma_A | f | ā-stem (SK454 TAp via strI_abs) | rAma+strI_abs → Ap → rāmā; tests SK454 l:at branch |
| kruYc_A | f | ā-stem (SK454 TAp via strI_abs, ajādi) | kruYc+strI_abs → Ap → kruñcā; tests SK454 ?ajAdi branch (consonant-final); no ṇatva (ñ blocks) |
| aja_A | f | ā-stem (SK454 TAp, ajādi item 1) | aja+strI_abs → ajā; no r/ṣ/ṛ → no ṇatva; gen pl अजानाम् |
| kokila_A | f | ā-stem (SK454 TAp, ajādi item 3) | kokila+strI_abs → kokilā; l before n is a blocker, not trigger → no ṇatva; gen pl कोकिलानाम् |
| SUdra_A | f | ā-stem (SK454 TAp, ajādi item 27) | SUdra+strI_abs → śūdrā; r before n, no blocker → ṇatva fires; gen pl शूद्राणाम् |
| uzRih_A | f | ā-stem (SK454 TAp, ajādi item 29) | uzRih+strI_abs → uṣṇihā (?ajAdi, h-final); ṇ (R) blocks ṇatva; gen pl उष्णिहानाम् |
| sarva_A | f | ā-stem (sarvanāma) | |
| nAsikA | f | ā-stem | |
| niSA | f | ā-stem | |
| mati | f | i-stem (non-nadī) | |
| lakzmI | f | ī-stem (nadī) | |
| strI | f | ī-stem (strī) | |
| atistri | f | ī-stem (atistri, pūrvastrī) | |
| suDI | f | ī-stem (kvip) | Does not take iyaṅ |
| praDI | f | ī-stem (kvip) | |
| BrU | f | ū-stem | |
| svayamBU | f | ū-stem (compound BU) | |
| varzABU | f | ū-stem (compound BU) | Gets yaṇ, not iyaṅ |
| dfnBU | f | ū-stem (compound BU) | |
| karaBU | f | ū-stem (compound BU) | |
| punarBU | f | ū-stem (compound BU) | |
| KalapU | f | ū-stem (kvip) | |
| senAnI | f | ī-stem (kvip) | |
| nI | f | ī-stem (kvip) | |
| SrI | f | ī-stem | |
| Denu | f | u-stem (āp, non-nadī) | |
| tisf | f | tisṛ | Numeral fem |
| catasf | f | catasṛ | Numeral fem |
| jYAna | n | a-stem | |
| vAri | n | i-stem | |
| payas | n | s-stem | |
| Danus | n | us-stem | SK434 nom/acc/voc plu dhanūṃṣi (M vyavāya); SK212 all other ṣatva forms |
| SrIpA | n | ā-stem (neuter) | |
| akzi | n | i-stem (akṣi) | |
| atinO | n | u-stem (nau-type) | |
| anya | n | sarvanāma | |
| dvi | m/f/n | dvi | Numeral (dual-only) |
| dvi_s | f/n | dvi | Feminine/neuter dual-only numeral |
| kati | m | kati (qati) | Numeral |
| parvan | n | n-stem | Neuter; SK355 (6.4.137) blocks al-lopa |
| yajvan | m | van-stem | yajvan-type (-van with SK355) |
| hastin | m | in-stem | SK356/357: nom sg hastī, du hastinau |
| vftrahan | m | han-stem (compound) | SK356–359: vṛtraghna bha, vṛtrahaṇa strong |
| svan | m | śvan (n-stem) | SK362 samprasāraṇa: śuna- in bha |
| yuvan | m | van-stem | SK362 samprasāraṇa: yūna- in bha |
| maGavan | m | van-stem (optional tṛ) | SK360 optional tṛj; both paradigms listed |
| arvan | m | van-stem (mandatory tṛ) | SK364 mandatory tṛ except nom sg |
| paTin | m | paTin-group | SK365–368: panthāḥ nom/voc sg, panTāna- strong, paṭha- bha |
| maTin | m | paTin-group | same rules as paTin; manthāḥ nom/voc sg |
| fBukzin | m | paTin-group | SK365/366/368 only (no SK367 — no th); ṛbhukṣāḥ nom/voc sg; ṇatva in strong forms |
| gir | m | r-stem (kvip) | SK433 (8.2.76): upadhā-dīrgha at pada-end → gīḥ nom/voc sg; SK354 (8.2.77): before hal → gīrbhiḥ, gīrbhyām, gīrbhyaḥ, gīrṣu |
| pur | m | r-stem (kvip) | SK433 (8.2.76): upadhā-dīrgha at pada-end → pūḥ nom/voc sg; SK354 (8.2.77): before hal → pūrbhiḥ, pūrbhyām, pūrbhyaḥ, pūrṣu |
| ftvij | m | j-stem (kvin) | SK377 (8.2.62): j→g at pada-end; 8.4.56 opt g→k; ṛtvig/ṛtvik nom sg |
| sraj | f | j-stem (kvin) | SK377 (8.2.62): same as ftvij; srag/srak nom sg |
| yuj | m | j-stem (kvin, non-compound) | SK376 (7.1.71): num (Y=ñ) before sarvanāmasthāna; SK377 (8.2.62)+8.2.23: yuṅ nom sg |
| yuj_samAsa | m | j-stem (kvin, compound / aśvayuk type) | SK376 blocked by ?samAsa tag; no nUM; same phonology as ṛtvij: yug/yuk nom sg |
| diS | f | ś-stem (kvin) | SK377 (8.2.62): 8.2.36 S→ṣ(z), 8.2.39 ṣ→ḍ(q), 8.2.62 q→g; 8.4.56 opt g→k; dig/dik nom sg |
| takz | m | kṣ-stem (kvip) | SK380 (8.2.29): k deleted from kṣ at pada-end → ṣ→ḍ(8.2.39)→ṭ(8.4.56); nom sg taṭ/taḍ |
| gaRapati | m | i-stem (compound pati, ghī) | SK257 (1.4.8): pati in compound gets ghī-saṃjñā; inst -nā, dat -aye, abl/gen -eḥ, loc -au (cf. standalone patyuḥ gen) |
| aSvayuj | m | j-stem (kvin, compound) | SK376 (7.1.71) blocked by ?samAsa; no nUM; phonology as ṛtvij: aśvayug/aśvayuk nom sg |
| viSvAvasu | m | u-stem (compound, SK379) | SK379 (6.3.128): viśva final a→ā before ?vasu in compound; viśvāvasu |
| viSvArAj | m | j-stem (kvip rāj, compound, SK379) | SK379 (6.3.128): viśva final a→ā before ?rAj in compound; nom sg viśvārāṭ via SK294 (j→ṣ→ḍ→ṭ chain) |
| pratyac | m | añcatir kvin (SK415–417, dynamic) | Dynamic: [prati, aYc_u, kvin]; SK415 aYc→ac, 6.1.77 prati+ac→pratyac; SK361 nUM strong; SK416+417 bha: pratīcā (not pratyacā — 6.1.77 blocked by akṛtavyūhā) |
| prAc | m | añcatir kvin (SK415–417, dynamic) | Dynamic: [pra, aYc_u, kvin]; SK415 aYc→ac, 6.1.101 pra+ac→prAc; SK361 nUM; SK416+417 bha: prācā (dirgha('a')=A) |
| udac | m | añcatir kvin (SK420, dynamic) | Dynamic: in_udanc([ud, aYc_u, kvin]); SK415 aYc→ac; SK420 apavāda of SK416: udac bha→udīcā; fixes previously wrong bha forms |
| tiryac | m | añcatir kvin (SK415–417, dynamic) | Dynamic: [tiry, aYc_u, kvin]; SK415 aYc→ac; tiry ends in 'y' → dirgha no-op → bha tiryacā unchanged |
| supAd | m | d-stem (pāda compound, SK414) | SK414 (6.4.130): pAd→pad (ā→a) in bha context; inst/dat/abl/gen/loc sg + acc/gen pl use pad- base; nom/voc/acc sg+du+pl use supAd- base |
| Sf_vanip_strI | f | van-stem (SK456, dynamic) | Dynamic: [Sf, vanip, strI_abs]; SK2168 guṇa Sf→Sar; SK456 (4.1.7) NIp + n→r → SarvarI; each cell also accepts geminated SK 8.4.46 variant (Sarv-/Sarvv-) |
| dvipAd_strI | f | d-stem (pāda compound, SK457) | Dynamic: [as_purva_pada(dvi), luk_sup, in_compound(pAd_ut), strI_abs]; SK457 (4.1.8) optional NIp produces both dvipadī (NIp + SK414 bha pAd→pad) and dvipāt (no-NIp halanta) branches |
| sIman | f | man-final n-stem (SK459/461) | [sIman, strI_abs]; SK459 (4.1.11) blocks ṅīp → halanta n-stem feminine (सीमा, सीमानौ, सीम्नः); SK461 (4.1.13) optional DAp → ramā-type ā-stem (सीमा, सीमे) |
| bahuyajvan_strI | f | an-final bahuvrīhi (SK460/461) | [bahuyajvan, strI_abs]; prebuilt ?bahuvrIhi/?samasta_pada/?van; SK460 (4.1.12) blocks ṅīp (overrides 4.1.5/4.1.7) → halanta (बहुयज्वा, 6.4.137 keeps weak stem यज्वन्); SK461 optional DAp → बहुयज्वे |
| bahurAjan_strI | f | an-final upadhālopin bahuvrīhi (SK462) | [as_purva_pada(bahu), luk_sup, in_context(in_compound(rAjan),"bahuvrīhi"), strI_abs]; real बहु+राजन् compound; 3-way fork — ṅīp (SK462→बहुराज्ञी), DAp (SK461→बहुराजा), an-stem niṣedha (SK460→बहुराजानौ) |
| sarvika | f | ka-pratyaya a-stem (SK463) | [sarva, kan, strI_abs]; SK463 (7.3.44) idādeśa: sarva+kan → sarvaka, then a→i before ka-pratyaya when Ap follows → सर्विका (ramā-type; gen pl सर्विकाणाम् via ṇatva) |
| yaka_strI | f | yad-derived ka-stem (SK464) | [yad, kan, strI_abs]; yad→ya (7.2.102 before kan), +kan → yaka; SK464 (7.3.45) blocks SK463 → यका (NOT यिका) |
| saka_strI | f | tad-derived ka-stem (SK464) | [tad, kan, strI_abs]; tad→ta (7.2.102), +kan → taka; SK464 blocks SK463 → takā; nom sg सका via 7.2.106 (tyadAdi propagated through kan), rest त-forms |
| parivrAjaka_strI | f | ka-pratyaya stem (SK463) | [parivrAjaka, strI_abs]; ṇvul-derivative (aka-final, ?ka_pratyaya); SK463 idādeśa fires → परिव्राजिका (ramā-type) |
| bahuparivrAjaka_strI | f | bahuvrīhi ka-stem (SK463 asuwapaH) | RAW derivation [as_purva_pada(bahu), as_purva_pada(pari), luk_sup, in_context(in_compound(vrAja),"bahuvrIhi"), kap, strI_abs] — no pre-formed aka-stem. ?bahuvrIhi propagates (like samAsa, from first) through the vrAja+kap merge to the (bahuparivrAjaka\|Ap) window where ?!bahuvrIhi blocks SK463 → बहुपरिव्राजका (no idādeśa), declines like ramā |
| aindra_strI | f | aṇ-taddhita (SK470) | [indra, aR_t, strI_abs]; ādivṛddhi + ṅīp → ऐन्द्री (nadī-type) |
| autsa_strI | f | añ-taddhita (SK470) | [utsa, aY_t, strI_abs]; ādivṛddhi u→au + ṅīp → औत्सी |
| Uru_dvayasI | f | dvayasac (SK470) | [Uru, dvayasac, strI_abs]; ṅīp → ऊरुद्वयसी |
| UrudaGnI | f | daghnac (SK470) | [Uru, daGnac, strI_abs]; ṅīp → ऊरुदघ्नी |
| UrumAtrI | f | mātrac (SK470) | [Uru, mAtrac, strI_abs]; ṅīp → ऊरुमात्री (gen pl ṇatva → ऊरुमात्रीणाम्) |
| paYcatayI | f | tayap (SK470) | [paYca, tayap, strI_abs]; ṅīp → पञ्चतयी |
| yAdfSI | f | kañ (SK470, reuses kaY) | [yad, su, in_compound(dfS), kaY, strI_abs]; ṅīp → यादृशी |
| gArgI | f | yañ (SK471 + SK472) | [garga, yaY_t, strI_abs]; ṅīp then 6.4.150 ya-lopa → गार्गी |
| vEdyI | f | SK472 negative (?tadDita_ya guard) | [vidyA, aR_t, strI_abs]; base-internal 'y' (विद्या→वैद्य) NOT elided → वैद्यी (य retained: वैद्यी/वैद्य्यौ), not वैदी |
| kurucarI | f | ṭiṭ (SK470, +w) | [as_purva_pada(kuru), luk_sup, in_compound(car), wac, strI_abs]; wac's ṭ-it propagates → +w block → ṅīp → कुरुचरी (nadī-type) |
| naSvarI | f | kvarap (SK470) | [naS, kvarap, strI_abs]; naś+kvarap → नश्वर (no tuk — consonant-final base) → ṅīp → नश्वरी. kvarap retagged kṛt (not svAdi) to avoid spurious 1.4.17 pada-saṁjñā/jaśtva |
| suparReyI | f | ḍha (SK470) | [suparRA, Qhak, strI_abs]; SK475 (7.1.2) ḍh→eya + 7.2.118 ādivṛddhi सु→सौ → सौपर्णेयी (complete) |
| lAvaRikI | f | ṭhañ (SK470) | [lavaRa, WaY, strI_abs]; 7.3.50 ṭha→ika + 7.2.117 ñit vṛddhi → लावणिकी (complete; the 1.4.18 -pada fix removed the earlier doubled-ṇ) |
| akzikI | f | ṭhak (SK470) | [akza, Wak, strI_abs]; 7.3.50 ṭha→ika + 7.2.118 ādivṛddhi अ→आ → आक्षिकी (complete; 1.4.18 -pada fix removed the earlier 8.2.29 misfire अडिक) |
| gArgyAyaRI | f | ṣpha (SK473) — needs 6.4.22 | [garga, yaY_t, sPa, strI_abs]; गार्ग्यायणी. Drives 6.4.22 (148+150 compose) + 6.4.134 block on आयन् output |
| lOhityAyanI | f | ṣpha obligatory via SK476 (4.1.18) | [lohita, yaY_t, sPa, strI_abs]; लौहित्यायनी (no ṇatva trigger, so plain न) |
| kOravyAyaRI | f | ṣpha obligatory via SK477 (4.1.19) | [kuru, yaY_t, sPa, strI_abs]; कौरव्यायणी (ṇatva from r of kuru) |
| kumArI | f | vayasi prathame (SK478) | [kumAra, strI_abs]; kumAra carries ?vayasi_prathama → SK478 ṅīp (apavāda to 4.1.4) → कुमारी; gen pl कुमारीणाम् (8.4.1 ṇatva: r…n→ṇ) |
| trilokI | f | Dvigu samāsa (SK479) — exercises new ?dvigu tag | [as_purva_pada(tri), luk_sup, in_context(in_compound(loka), "dvigu"), strI_abs]; ?dvigu propagates through join_objects() (paninian_object.py allowlist, analogous to ?bahuvrIhi) → SK479 ṅīp → त्रिलोकी; gen pl त्रिलोकीनाम् (l blocks 8.4.1 ṇatva) |
| tryanIkA | f | Dvigu samāsa, ?ajAdi_in_Dvigu uttara-pada → ?dvigu **overridden** (4.1.4.2) | [as_purva_pada(tri), luk_sup, in_context(in_compound(anIka), "dvigu"), strI_abs]; ?ajAdi_in_Dvigu propagates from anIka via samāsa-gated `_propagate(last, ["ajAdi", "ajAdi_in_Dvigu"])`; 4.1.4.2 overrides SK479 → ṭāp → त्र्यनीका (ramā-type). Gen pl त्र्यनीकानाम् — y blocks ṇatva |
| triPalA | f | Dvigu samāsa with ?ajAdi_in_Dvigu (Vasu's exact example) | [as_purva_pada(tri), luk_sup, in_context(in_compound(Pala), "dvigu"), strI_abs]; same mechanism as tryanIkA → त्रिफला. Gen pl त्रिफलानाम् — l blocks ṇatva |
| paYcASvI | f | SK479 ṅīp on samāhāra-Dvigu of aśva (Vasu/SK on SK480) | [as_purva_pada(paYca), luk_sup, in_context(in_compound(aSva), "dvigu"), strI_abs]; aśva has ?ajAdi (gaṇa item 5) but NOT ?ajAdi_in_Dvigu — so 4.1.4.2 doesn't fire and SK479 ṅīp wins → पञ्चाश्वी. Gen pl पञ्चाश्वीनाम् — no r/ṛ/ṣ in stem, no ṇatva |
| paYcASvA | f | SK480 Dvigu+tadDita-luk non-parimāṇa → ṭāp | [as_purva_pada(paYca), luk_sup, in_context(in_compound(aSva), "dvigu"), luk_tadDita, strI_abs] → पञ्चाश्वा via SK480 niṣedha (note: 4.1.4.2 also doesn't fire here since aSva lacks ?ajAdi_in_Dvigu, so SK480 is the sole path) |
| dvibistA | f | SK480 bistāḍi arm | [as_purva_pada(dvi), luk_sup, in_context(in_compound(bista), "dvigu"), luk_tadDita, strI_abs]; ?bistAdi tag on bista → SK480 second arm fires → ṭāp → द्विबिस्ता |
| dvyAcitA | f | SK480 bistāḍi arm (napum uttara-pada, yan sandhi) | [as_purva_pada(dvi), luk_sup, in_context(in_compound(Acita), "dvigu"), luk_tadDita, strI_abs]; dvi+A → dvyA (yan sandhi) → द्व्याचिता |
| dvikambalyA | f | SK480 bistāḍi arm | [as_purva_pada(dvi), luk_sup, in_context(in_compound(kambalya), "dvigu"), luk_tadDita, strI_abs] → द्विकम्बल्या |
| dvyAQakI | f | SK480 counter (parimāṇa preserves ṅīp) | [as_purva_pada(dvi), luk_sup, in_context(in_compound(AQaka), "dvigu"), luk_tadDita, strI_abs]; AQaka carries ?parimARa → SK480 first arm `?!parimARa` fails, second arm `?bistAdi` fails → SK479 ṅīp wins → द्व्याढकी |
| dvikARqA_kzetre | f | SK481 (kāṇḍa-final Dvigu in kṣetra sense) | [as_purva_pada(dvi), luk_sup, in_context(in_context(in_compound(kARqa), "dvigu"), "kzetre"), luk_tadDita, strI_abs]; ?kzetre tag → SK481 fires → ṭāp → द्विकाण्डा |
| dvikARqI | f | SK481 negative (non-kzetra kāṇḍa-Dvigu keeps ṅīp) | same as dvikARqA_kzetre without the kzetre wrapper; SK481 doesn't fire (no ?kzetre); SK480 excludes ?kARqa → SK479 ṅīp wins → द्विकाण्डी (रज्जुः) |
| dvipuruzI_pramARe | f | SK482 vibhāṣā (puruṣa+pramāṇa) | [as_purva_pada(dvi), luk_sup, in_context(in_context(in_compound(puruza), "dvigu"), "pramARe"), luk_tadDita, strI_abs]; SK482 optional + overrides 4.1.21 → fire branch sets NIp (द्विपुरुषी), skip branch falls back to SK480 → ṭāp (द्विपुरुषा); both alternants per cell. ṣ in puruṣa triggers gen pl ṇatva → द्विपुरुषाणाम् / द्विपुरुषीणाम् |
| dvipuruzA | f | SK482 negative (non-pramāṇa puruṣa → only ṭāp) | same as dvipuruzI_pramARe without the pramARe wrapper; SK482 cannot fire (no ?pramARe) → SK480 alone → ṭāp → द्विपुरुषा only |
| kuRqoDnI | f | SK483/484 (ūdhas bahuvrīhi → NIz) | [as_purva_pada(kuRqa), luk_sup, in_context(in_compound(UDas), "bahuvrIhi"), strI_abs]; SK483 final s→n → kuRqoDan → SK484 NIz → 6.4.134 a-lopa → कुण्डोध्नी (nadī-type) |
| GawoDnI | f | SK483/484 (ghaṭa + ūdhas) | same pattern with GaTa pūrva-pada → घटोध्नी |
| dvyUDnI | f | SK485 saṃkhyādi arm | dvi (?saMKyA) + UDas with `in_context(..., "saMKyAdi")` on UDas → SK485 NIp overrides SK484 → द्व्यूध्नी; i+ū → yū (6.1.77 yaṇ) |
| atyUDnI | f | SK485 avyayādi arm | ati (new avyaya stem) + UDas with `in_context(..., "avyayAdi")` on UDas → SK485 NIp → अत्यूध्नी |
| dvidAmnI | f | SK486 dāman arm | dvi + dāman bahuvrīhi with ?saMKyAdi → SK486 arm 1 NIp → 6.4.134 drops -an upadhā 'a' → द्विदाम्नी |
| dvihAyanI | f | SK486 hāyana arm (age sense) | dvi + hāyana with ?saMKyAdi + ?vayasi → SK486 arm 2 NIp → 6.4.148 drops final 'a' → द्विहायनी |
| dvihAyanA | f | SK486 hāyana negative (non-age → ṭāp) | dvi + hāyana with ?saMKyAdi but NO ?vayasi → SK486 fails → 4.1.4 ṭāp → द्विहायना (ramā-type). Vasu: द्विहायना शाला 'a hall of two years' standing'. Required 6.1.87 to strip `sarvanAmasTAna` from the post-guṇa suffix so 6.4.8 does not re-fire on the n-final surface (hāyan|e) |
| trihAyaRI | f | SK486 vārttika (tri + hāyana, age) | tri (saMKyA, has 'r') + hāyana with ?saMKyAdi+?vayasi+?triCatur → vārttika (4.1.27.1) n→ṇ → SK486 NIp → 6.4.148 a-lopa → त्रिहायणी. 'h' intervening between r and final n of -nām blocks 8.4.2 ṇatva on suffix → gen pl त्रिहायणीनाम् |
| caturhAyaRI | f | SK486 vārttika (catur + hāyana, age) | catur + hāyana same as trihAyaRI → चतुर्हायणी (gen pl चतुर्हायणीनाम्; 'h' blocks 8.4.2) |
| trihAyanA | f | SK486 vārttika negative (non-age tri + hāyana → ṭāp) | tri + hāyana with ?saMKyAdi, NO ?vayasi → vārttika fails, SK486 fails → 4.1.4 ṭāp → त्रिहायना (Vasu's exact शाला example). 8.4.x ṇatva blocked by 'h' between r and stem n |
| atirAjJI | f | SK487 saṃjñā arm (4.1.29) | ati + rAjan saṃjñā-bahuvrīhi: ?saMjYA attached via in_context. SK487 overrides SK462's vibhāṣā making NIp mandatory → 6.4.134 a-lopa + 8.4.40 ścutva → अतिराज्ञी |
| kevalI | f | SK488 saṃjñā arm (4.1.30) | kevala (?keval_Adi) + ?saMjYA → SK488 NIp → 6.4.148 a-lopa → केवली |
| kevalA | f | SK488 laukika arm (4.1.30) | kevala + no saṃjñā tag → SK488 fails → 4.1.4 ṭāp → केवला (ramā-type) |
| mAmakI | f | SK488 saṃjñā arm (4.1.30) | mAmaka (?keval_Adi, ?mAmaka, ?ka_pratyaya) + ?saMjYA → SK488 NIp → मामकी |
| mAmikA | f | SK488 laukika arm (4.1.30) — niyama showcase | mAmaka + no saṃjñā/chandas → SK488 fails → 4.1.4 ṭāp → mAmaka+A → SK463 (7.3.44) idādeśa fires on ?ka_pratyaya + aka_anta → मामिका (Vasu: तेन लोकेऽसंज्ञायां मामिका) |
| sumaNgalI | f | SK488 saṃjñā arm (4.1.30) | sumaNgala (?keval_Adi) + ?saMjYA → SK488 NIp → सुमङ्गली |
| patnI | f | SK490 (4.1.33 पत्युर्नो यज्ञसंयोगे) | plain pati (?pati) + strī_abs: SK490 substitutes i→n (?pati + ?!samAsa) → patn → SK453 (4.1.5) NIp → पत्नी. Declines like nadī |
| gRhapatnI | f | SK491 (4.1.34 विभाषा सपूर्वस्य) | gRha + pati compound: in_compound(pati) attaches ?samAsa → SK491 substitutes i→n → patn → SK453 NIp → patnI → samasta merge with gRha → गृहपत्नी declining as the textbook nadī. The ?Gi-leak that previously broke the 4 oblique-sg cells is fixed by guarding 1.4.7/1.4.8 with `rp: ?!strI` (and 1.4.8 with `lp: ?!strI`) so Ghi-saṃjña never lands on the feminine path |
| sapatnI | f | SK492 (4.1.35 नित्यं सपत्न्यादिषु) | sapati (pre-substituted from sa+pati per Q3 deferral; ?sapatnyAdi + ?pati) + strī_abs: SK492 substitutes i→n → sapatn → SK453 NIp → सपत्नी |
| ekapatnI | f | SK492 (4.1.35 नित्यं सपत्न्यादिषु) | ekapati (?sapatnyAdi + ?pati) + strI_abs: SK492 → ekapatn → NIp → एकपत्नी |
| vIrapatnI | f | SK492 (4.1.35 नित्यं सपत्न्यादिषु) | vIrapati (?sapatnyAdi + ?pati) + strI_abs: SK492 → vIrapatn → NIp → वीरपत्नी |
| antarvatnI | f | SK489 (4.1.32 अन्तर्वत्पतिवतोर्नुक्) | antarvat (?antarvat_pativat) + strI_abs: SK489 appends nuk 'n' at end (bahiranga 1) → antarvatn → SK453 (4.1.5) NIp → अन्तर्वत्नी. Declines like nadī. Semantic restriction (?garBiNi) not encoded — see Skipped table |
| pativatnI | f | SK489 (4.1.32 अन्तर्वत्पतिवतोर्नुक्) | pativat (?antarvat_pativat) + strI_abs: same as antarvatnI → pativatn → NIp → पतिवत्नी |
| dhImat | m | -at stem (matup u-it, SK425) | SK425 (6.4.14): upadhā dīrgha before su → dhīmān nom sg; SK361 nUM for sarvānāmasthāna → dhīmant strong forms; dhīmat weak forms |
| gomat | m | -at stem (matup u-it, SK425) | SK425 (6.4.14): upadhā dīrgha before su → gomān nom sg; same pattern as dhīmat |
| jakzat | m | -at stem (śatṛ f-it, abhyasta, SK427+SK428) | SK427 blocks nUM → all forms use plain jakzat- base; nom sg जक्षत्/जक्षद् (not *जक्षन्); SLP1 z=ṣ |
| jAgrat | m | -at stem (śatṛ f-it, abhyasta, SK427+SK428) | same as jakshat; nom sg जाग्रत् (not *जाग्रन्) |
| dadat_napum | n | -at stem (śatṛ f-it, abhyasta napum, SK444) | SK444 optional nUM → pl: ददन्ति/ददति both valid; sg/du: no nUM (not sarvnāmasthāna for napum) |
| antar | m | svarAdi avyaya | SK447+SK452: all 24 vibhakti forms = antar |
| prati | m | nipAta avyaya | SK447+SK452: all 24 vibhakti forms = prati |
| pra | m | nipAta avyaya | SK447+SK452: all 24 vibhakti forms = pra |
| Bavat | m | -at stem (śatṛ f-it, regular, SK361) | SK361 +f block fires nUM → bhavant strong forms; nom sg भवन् (no SK425 — not u-it) |
| pacat | m | -at stem (śatṛ f-it, regular, SK361) | same as Bavat; nom sg पचन् |
| pacat_strI | f | -antī stem (śatṛ class 1, SK446) | SK446 mandatory nUM → always pacantī; nadī paradigm |
| pacat_NI | f | -antī stem (SK455 NIp via strI_abs, f-it) | pacat+strI_abs → NIp → pacantī; tests SK455 f-it (ṛ∈uk) branch |
| Bavat_uNI | f | -atī stem (SK455 NIp via strI_abs, u-it) | Bavat_u+strI_abs → NIp → BavatI; tests SK455 u-it branch; no nUM (no Satf/Sap) |
| pacat_napum | n | -at stem (śatṛ class 1, SK446+SK361) | du SK446 mandatory → पचन्ती; pl SK361 mandatory → पचन्ति |
| dIvyat_strI | f | -antī stem (śatṛ class 4, SK446) | SK446 mandatory nUM (?Syan) → always dīvyantī |
| dIvyat_napum | n | -at stem (śatṛ class 4, SK446+SK361) | du SK446 mandatory → दीव्यन्ती; pl SK361 mandatory → दीव्यन्ति |
| tudat_strI | f | -atī/-antī stem (śatṛ class 6, SK445) | SK445 optional (?Sa not ?Sap) → [tudantī, tudatī] both valid |
| tudat_napum | n | -at stem (śatṛ class 6, SK445+SK361) | du SK445 optional → [तुदती, तुदन्ती]; pl SK361 mandatory → तुदन्ति |
| BAt_strI | f | -ātī/-āntī stem (śatṛ ā-root, SK445) | SK445 optional (no ?Sap/?Syan) → [bhāntī, bhātī] both valid |
| yuzmad | — | 2nd person pronoun (alinga) | SK382–SK400: full pronoun paradigm; nom tvam, acc tvām, abl sg tvat, gen sg tava, gen pl yuṣmākam etc. |
| asmad | — | 1st person pronoun (alinga) | SK382–SK400: full pronoun paradigm; nom aham, acc mām, abl sg mat, gen sg mama, gen pl asmākam etc. |
| idam_strI | f | sarvanāma (idam feminine) | Full paradigm via [idam, strI_abs] TAp path; iyam, ime, imāḥ, anayā, asyai, āsām, etc. Nom sg iyam emerges from a 2-step apavāda chain on the post-TAp stem (idā|s): 7.2.110 (yas sau) sets lc='iya' keeping l='A' → "iyaA", then 7.2.108 (idamo maḥ) replaces final A with m → iyam. |
| tad_strI  | f | tyadAdi feminine (TAp via SK454) | SK454+SK441 path: tad+strI_abs → 7.2.102 → ta+strI_abs → SK454 → tA → vibhakti; 7.2.106 (sā), 8.3.59 etc. |
| etad_strI | f | tyadAdi feminine (TAp via SK454) | Same path as tad_strI; nom sg eṣā via 7.2.106 + 8.3.59 ṣ-substitution |
| yad_strI  | f | tyadAdi feminine (TAp via SK454) | Same path; nom sg yā |
| kim_strI  | f | kim feminine (TAp via SK454) | SK454+SK440 path: kim+strI_abs → 7.2.103 → ka+strI_abs → SK454 → kā |
| tad | m | tyadAdi demonstrative | SK381 (7.2.106): nom sg m saḥ; partial table (nom sg only) |
| Gftaspfk | m | kvin compound (samāsa) | SK432: √spṛś+kvin after Gfta; ghṛtaspṛk paradigm; SK377 (8.2.62) pada-end kutva |
| etad | m | tyadAdi demonstrative | SK381 (7.2.106): nom sg m eṣaḥ; partial table (nom sg only) |
| tyad | m | tyadAdi demonstrative | SK381 (7.2.106): nom sg m syaḥ; partial table (nom sg only) |
| adas | m | tyadAdi demonstrative | SK381+SK437 (7.2.106+7.2.107): nom sg asau; SK419 (8.2.80): amu sg/du/pl forms; SK438 (8.2.81): amī pl; SK439 (8.2.3): amunā inst sg; full vibhakti table (inst sg amunā, du amūbhyām, gen/loc du amuyoḥ) |
| tAdfk | m | j-stem (kvin, compound, SK430) | SK430 (6.3.91): tad→tA before dfS+kvin; SK377 j→g before bh; 8.4.56 opt g→k; nom sg tAdfk/tAdfg |
| tAdfSa | m | a-stem (kaY, compound, SK430) | SK430 (6.3.91): tad→tA before dfS+kaY; regular a-stem endings like rAma |
| yAdfk | m | j-stem (kvin, compound, SK430) | SK430 (6.3.91): yad→yA before dfS+kvin; same phonology as tAdfk |
| yAdfSa | m | a-stem (kaY, compound, SK430) | SK430 (6.3.91): yad→yA before dfS+kaY; regular a-stem endings like rAma |
| dvyahna | m | an-stem (compound) | [dvi, luk_sup, in_compound(ahan), wac]; SK238 → dvyahne/dvyahni/dvyahani variants |
| nf | m | ṛ-stem (nṛ) | SK283 (6.4.6): nara- before sarvānāmasthāna; acc pl nṝn via SK141 |
| ap | f | p-stem (nitya-bahuvacana) | Always plural; SK442 (7.4.48): p→t before bhi → adbhiḥ, adbhyaḥ |
| daDfc | m | c-stem (kvin) | [daDfc_kvin]; SK377 (8.2.62) partial: c-final path; dadhṛk/dadhṛg nom sg |
| naS | m | ś-stem (kvip) | [naS_kvip]; SK431 (8.2.63): optional kutva → nak/nag and naṭ/naḍ pakṣas |
| pums | m | s-stem (asun) | SK436 (7.1.89): s→as before sarvānāmasthāna; SK425+SK361 → pumān nom sg |
| mahat_n | n | t-stem (mahat, neuter) | SK317 (6.4.10): saṃyoga-final + nāmī; SK361 nUM for neuter strong forms |
| vidvas | m | s-stem (kvasu/vasAnta) | SK435 (6.4.131): samprasāraṇa v→u in bha; viduṣaḥ/ā/e/oḥ/ām bha forms |
| Bavat_u | m | -at stem (śatṛ u-it, SK361+SK425) | SK425 (6.4.14) dīrgha + SK361 nUM → bhavān nom sg; bhavant- other strong forms |
| dvitIyA | f | ā-stem (sarvanāma, Ap) | [dvitIya, Ap]; SK293 (7.3.115): optional syāṭ in dat sg → dvitīyasyai/dvitīyāyai |
| tftIyA | f | ā-stem (sarvanāma, Ap) | [tftIya, Ap]; SK293 (7.3.115): optional syāṭ in dat sg → tṛtīyasyai/tṛtīyāyai |
| paYcan | m | ṣaṭ-class numeral | SK369 (1.1.24) ?zaT; SK370 (6.4.7): upadhā-dīrgha+n-lopa before nāmi → pañcānām |
| saptan | m | ṣaṭ-class numeral | SK369 (1.1.24) ?zaT; SK370 (6.4.7) → saptānām; SK261 (7.1.22) luk |
| navan | m | ṣaṭ-class numeral | SK369 (1.1.24) ?zaT; SK370 (6.4.7) → navānām |
| daSan | m | ṣaṭ-class numeral | SK369 (1.1.24) ?zaT; SK370 (6.4.7) → daśānām |
| azwan | m | ṣaṭ-class numeral | SK369 ?zaT; SK371 (7.2.84): optional n→ā before hal; SK372 (7.1.21): optional jas/śas→au |
| upAnah | m | h-stem (nah) | SK440 (8.2.34): h→dh before jhal/pada-end; upānat nom sg (8.4.56), upānadbhyām |
| Sreyas | m | as-stem (Iyasun, comparative) | Comparative -as stem; SK209 (6.4.3): dīrgha before nāmi → śreyasām (gen pl) |
| Sreyas_n | n | as-stem (Iyasun, neuter) | Neuter comparative; SK318 (1.2.47) hrasva before su/am → śreyas sg |
| samyac | m | añcatir kvin (compound, SK421) | [sam, su, aYc_u, kvin]; SK421 (6.3.93): sam→sami before añcatir; samīcā bha |
| saDryac | m | añcatir kvin (compound, SK422) | [saha, su, aYc_u, kvin]; SK422 (6.3.95): saha→sadhrī; sadhrīcā bha |
| vizvadryac | m | añcatir kvin (compound, SK418) | [vizvag_pada, aYc_u, kvin]; SK418 (6.3.92): ṭi→adri; viṣvag→viṣvadṛk nom sg |
| etadryac | m | añcatir kvin (compound, SK418) | [etad, luk_sup, aYc_u, kvin]; SK418 ticādeśa_adri; etādṛk nom sg |
| idadryac | m | añcatir kvin (compound, SK418) | [idam, luk_sup, aYc_u, kvin]; SK418 ticādeśa_adri; idādṛk nom sg |
| amudryac | m | añcatir kvin (compound, SK418) | [adas, luk_sup, aYc_u, kvin]; SK418 ticādeśa_adri; amudṛk nom sg |
| sarvadryac | m | añcatir kvin (compound, SK418) | [sarva, luk_sup, aYc_u, kvin]; SK418 ticādeśa_adri; sarvadṛk nom sg |
| vasu | m | u-stem | Standalone test for SK379 (6.3.128) base; regular u-stem (ghy class) |
| tAvat_n | n | -at stem (vatup u-it, neuter) | [tad, in_context(vatup, napum)]; nUM du+pl → tāvatī, tāvanti |
| yAvat_n | n | -at stem (vatup u-it, neuter) | [yad, in_context(vatup, napum)]; same pattern as tAvat_n |
| etAvat_n | n | -at stem (vatup u-it, neuter) | [etad, in_context(vatup, napum)]; same pattern as tAvat_n |
| tAvAn | m | -at stem (vatup u-it, SK361+SK425) | [tad, in_context(vatup, pum)]; SK425+SK361 → tāvān nom sg; tāvant- strong forms |
| yAvAn | m | -at stem (vatup u-it, SK361+SK425) | [yad, in_context(vatup, pum)]; yāvān nom sg; same as tAvAn |
| etAvAn | m | -at stem (vatup u-it, SK361+SK425) | [etad, in_context(vatup, pum)]; etāvān nom sg; same as tAvAn |
| tAdfkza | m | a-stem (compound, SK430) | (samāsa) [tad_pada, in_compound(dfkza)]; SK430 kṣa arm; regular a-stem; tādṛkṣaḥ nom sg |
| yAdfkza | m | a-stem (compound, SK430) | (samāsa) [yad_pada, in_compound(dfkza)]; SK430 kṣa arm; yādṛkṣaḥ nom sg |
| SUrpanaKI | f | ī-stem (nadī compound) | (samāsa) [as_purva_pada(SUrpa), luk_sup, in_compound(naKI)]; Śūrpaṇakhā paradigm |
| kzIrapa | n | a-stem (compound) | (samāsa) [as_purva_pada(kzIra), luk_sup, in_compound(pa)]; kṣīrapa neuter a-stem |
| aDaspada | n | a-stem (compound) | (samāsa) [as_purva_pada(aDas), in_compound(pada)]; SK161 test — adhas+pada → adhaspadam |
| Siraspada | n | a-stem (compound) | (samāsa) [as_purva_pada(Siras), in_compound(pada)]; SK161 test — śiras+pada → śiraspadam |
