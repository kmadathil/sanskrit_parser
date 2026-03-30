# Generator Implementation Status

Sutras are implemented following the Siddhantakaumudi (SK) order from
https://drdhaval2785.github.io/siddhantakaumudi/

**Last implemented:** SK 443 — 8.2.68 अहन् (ahan n→ru at pada-end; neuter day stem); SK429–434 and SK441 deferred
**Next to implement:** SK 444 (7.1.79 — vā napuṃsakasya; defer if not needed for current stems)

---

## Summary

| Category | Count |
|---|---|
| SK-numbered sutras, implemented | 177 |
| SK-numbered sutras, skipped/deferred | 59 |
| Implemented sutras without SK number yet | ~92 |
| Stems with full vibhakti test tables | 100 |
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
| 64 | 6.1.80 | धातोस्तन्निमित्तस्यैव | Restricts yaṇ-sandhi to dhātu context only |
| 65 | 6.1.81 | क्षय्यजय्यौ शक्यार्थे | Fixed forms kṣayya, jayya |
| 66 | 6.1.82 | क्रय्यस्तदर्थे | Fixed form krayya |
| 73 | 6.1.89 | एत्येधत्यूठ्सु | iyaṅ/uvaṅ not applied before eṭ (iR, eDa dhātu) |
| 74 | 6.1.91 | उपसर्गादृति धातौ | ṛ-initial dhātu after upasarga: guṇa applies |
| 78 | 6.1.94 | एङि पररूपम् | Upasarga ending in e/o before a-initial dhātu: pararūpa (e.g. upa + eti → upeti) |
| 80 | 6.1.95 | ओमाङोश्च | om + māṅ: pararūpa |
| 90 | 6.1.125 | प्लुतप्रगृह्या अचि नित्यम् | Pluta and pragṛhya vowels before vowels: no sandhi |
| 100 | 1.1.11 | ईदूदेद्द्विवचनं प्रगृह्यम् | Dual endings -ī, -ū, -e are pragṛhya (no sandhi): nom/acc du of ī/ū/e-final stems |
| 101 | 1.1.12 | अदसोमात् | adasaḥ: the form amā (inst sg of adas) is pragṛhya |
| 164 | 6.1.102 | प्रथमयोः पूर्वसवर्णः | nom/acc du: stem-final a/ā + O ending → long vowel (e.g. rāma + O → rāmau) |
| 193 | 6.1.69 | एङ्ह्रस्वात्संबुद्धेः | voc sg of ī/ū-final stems: drop su (śe drops) — rāma→rāma, e→e |
| 194 | 6.1.107 | अमिपूर्वः | Stem vowel before am: pūrvarūpa (e.g. go + am → gām) |
| 201 | 7.1.12 | टाङसिङसामिनात्स्याः | ins sg → inā; abl/gen sg → āt, sya (a-stems: rāmeṇa, rāmāt, rāmasya) |
| 202 | 7.3.102 | सुपि च | a-stem before sup: guṇa of final a — loc sg rāme, ins rāmeṇa |
| 203 | 7.1.9 | अतो भिस ऐस् | a-stem + bhis → ais (ins pl: rāmaiḥ) |
| 204 | 7.1.13 | ङेर्यः | dat sg e-ending → ya (a-stem: rāmāya; sarvanāma: sarvasmai) |
| 205 | 7.3.103 | बहुवचने झल्येत् | a-stem before hal-initial bahuvacana sup: guṇa → e (dat/abl/loc pl: rāmebhyaḥ, rāmeṣu) |
| 207 | 7.3.104 | ओसि च | a-stem before os: guṇa → e (gen/loc du: rāmayoḥ) |
| 208 | 7.1.54 | ह्रस्वनद्यापो नुट् | nadī/āp-stems + am/āṁ: inserts nut (n) — gen pl nadīnām, rāmāṇām |
| 209 | 6.4.3 | नामि | aṅga lengthening before nāmī (gen pl am) — rājñām |
| 211 | 8.3.57 | इण्कोः | n→ṇ after iṇ or ku (ṇatva) in ādeśa/pratyaya context |
| 213 | 1.1.27 | सर्वादीनि सर्वनामानि | Defines the sarvanāma class (sarva, viśva, etc.) |
| 214 | 7.1.17 | जसः शी | ī-final feminine nom pl: jas → śī (nadyaḥ → nadyaḥ via śī+sandhi) |
| 216 | 7.1.15 | ङसिङ्योः स्मात्स्मिनौ | sarvanāma abl sg → smāt; loc sg → smin (sarvasmāt, sarvasmin) |
| 217 | 7.1.52 | आमि सर्वनाम्नः सुट् | sarvanāma + āṁ: inserts su → sām (gen pl sarveṣām) |
| 228 | 6.1.63 | पद्दन्नोमास्… | Samprasāraṇa: special alternants for pada, danta, nāman etc. stems in certain forms |
| 234 | 6.4.134 | अल्लोपोऽनः | n-final stem: delete n before yāsut (gen pl rājñām) |
| 240 | 6.4.140 | आतो धातोः | ā-final dhātu + kta: ā deleted (sthā + ta → sthita) |
| 241 | 7.3.109 | जसि च | ī/ū-final feminine + jas: guṇa (suDiyaḥ, BrūvaḥÀ) |
| 242 | 7.3.108 | ह्रस्वस्य गुणः | Short ī/ū-final: guṇa before certain sup (nadī → nade in loc sg) |
| 243 | 1.4.7 | शेषो घ्यसखि | Remaining i/u-final (non-nadī, non-sakhi) stems: ghy-saṃjñā — affects aṅga rules |
| 246 | 6.1.110 | ङसिङसोश्च | ṛ-final + gen sg/abl sg: uraṇ + dirgha — pitṛ → pituḥ, pitroḥ |
| 248 | 7.1.93 | अनङ् सौ | n-final neuter + su: anañ substitute — nom sg rājā, but neuter: nāma |
| 252 | 6.1.68 | हल्ङ्याब्भ्यो दीर्घात्… | Drop apṛkta hal su/si/s after long vowel or ṅī/āp (nadī nom sg: nadī) |
| 253 | 7.1.92 | सख्युरसंबुद्धौ | sakhi: special oblique stem sakhā- (non-voc forms) |
| 255 | 6.1.112 | ख्यत्यात्परस्य | khyāt-endings: pararūpa before certain vowels |
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
| 294 | 8.2.36 | व्रश्चभ्रस्ज… षः | ś/ch at pada-end → ṣ (lih → liṭ etc.) |
| 295 | 8.2.41 | षढोः कः सि | ṣ/ḍh at pada-end + si → k (lih+su → liṭ) |
| 296 | 1.4.6 | ङिति ह्रस्वश्च | Long ī/ū-final feminines + ṅit sup: optional hrasva + nadī-saṃjñā |
| 298 | 7.2.99 | त्रिचतुरोः स्त्रियां तिसृचतसृ | tri/catur fem: tisṛ/catasṛ substitutes |
| 299 | 7.2.100 | अचि र ऋतः | tisṛ/catasṛ + vowel-initial: ṛ→ar (tisṝṇām → tisṛ forms) |
| 300 | 6.4.4 | न तिसृचतसृ | Exception: tisṛ/catasṛ don't get lengthening before nāmī |
| 301 | 6.4.79 | स्त्रियाः | Feminine aṅga operations: governs strī-stem changes |
| 302 | 6.4.80 | वाम्शसोः | Feminine stem before vā (am) and śas: special form |
| 303 | 1.4.4 | नेयङुवङ्स्थानावस्त्री | Defines: iyaṅ/uvaṅ substituted stems are NOT nadī (so no nadī rules apply) |
| 304 | 1.4.5 | वामि | Long ī/ū-final Snu/dhātu/bhrū + Am: optionally nadī |
| 305 | 7.1.96 | स्त्रियां च | Feminine tṛc-forms: same as tṛj-pattern |
| 306 | 4.1.5 | ऋन्नेभ्यो ङीप् | ṛn/n-final pum stems → ṅīp suffix for feminine (rājñī etc.) |
| 308 | 4.1.10 | न षट्स्वस्रादिभ्यः | Exception to 4.1.5: ṣaṭ-group and svasṛ etc. don't take ṅīp |
| 309 | 7.1.24 | अतोऽम् | a-stem + am (acc sg): no change — rāmam |
| 310 | 7.1.19 | नपुंसकाच्च | Neuter + au: am substitute (jñānam nom/acc du) |
| 311 | 6.4.148 | यस्येति च | Stem-final i/a deleted before ī (e.g. in taddhita/kṛt formations) |
| 312 | 7.1.20 | जश्शसोः शिः | Neuter + jas/śas: śi substitute (jñānāni nom/acc pl) |
| 313 | 1.1.42 | शि सर्वनामस्थानम् | Defines śi as sarvānāmasthāna (triggers strong stem forms) |
| 314 | 7.1.72 | नपुंसकस्य झलचः | Hal-final neuter + śi: nu-āgama inserted (jaganti) |
| 315 | 7.1.25 | अद्ड्डतरादिभ्यः पञ्चम्यः | adaḍ etc.: ḍ-āgama in pañcamī |
| 317 | 6.4.10 | सान्तमहतः संयोगस्य | Saṃyoga-final + nāmī: last consonant of saṃyoga deleted (mahat → mahā before sarvānāmasthāna) |
| 318 | 1.2.47 | ह्रस्वो नपुंसके | Neuter prātipadika: hrasva before su/am |
| 319 | 7.1.23 | स्वमोर्नपुंसकात् | Neuter + su/am: su/am → am (jñānam) |
| 320 | 7.1.73 | इकोऽचि विभक्तौ | ik-final + vowel-initial vibhakti: tuk inserted (akṣṇā, akṣṇoḥ) |
| 326 | 8.2.37 | एकाचो बशो भष् | Single-syllable stem ending in b/g/ḍ/j + s/dh: bhāṣ substitute |
| 329 | 6.4.132 | वाह ऊठ् | vāh-stem: āḥ → ūṭh in strong forms |
| 330 | 6.1.108 | संप्रसारणाच्च | After samprasāraṇa: pūrvarūpa |
| 331 | 7.1.98 | चतुरनडुहोरामुदात्तः | catur/anaḍuh + am: āṁ (gen pl caturṇām, anaḍuhām) |
| 332 | 7.1.82 | सावनडुहः | anaḍuh + su: ā (anaḍvā nom sg) |
| 333 | 7.1.99 | अम् संबुद्धौ | anaḍuh + sambuddhi: am → anaḍvan (voc sg) |
| 334 | 8.2.72 | वसुस्रंसुध्वंस्वनडुहां दः | anaḍuh at pada-end: h→d (anaḍud) |
| 335 | 8.3.56 | सहेः साडः सः | sah-stem: s at start of certain forms |
| 336 | 7.1.84 | दिव औत् | div-stem + sup: au substitute (dyauḥ nom sg) |
| 338 | 7.1.55 | षट्चतुर्भ्यश्च | ṣaṭ/catur + am: nuk inserted (ṣaṭṇām, caturṇām) |
| 340 | 8.4.49 | शरोऽचि | śar after anusvāra before vowel: no change (exception to 8.4.46) |
| 341 | 8.2.64 | मो नो धातोः | m-final dhātu at pada-end → n (pra-gam → pragan) |
| 342 | 7.2.103 | किमः कः | kim → ka substitute before most sup (kasya, kasmai etc.) |
| 345 | 7.2.109 | दश्च | kim + daḥ (abl sg daḥ form): ka |
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
| 364 | 6.4.127 | अर्वणस्त्रसावनञः | mandatory tṛ-substitute for arvan before all suffixes except su; arvant- strong, arvat- bha |
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
| 418 | 6.3.92 | विष्वग्देवयोश्च टेरद्र्यञ्चतावप्रत्यये | ṭi→adri before añcatir (viṣvag/deva forms); fires on ?sarvanAma_pada (tad/yad/kim) using ticAdesha_adri helper; bahiranga:1 fires before SK417 |
| 420 | 6.4.139 | उद ईत् | apavāda of SK416: ud+añc in bha → substitute ī for 'a' of ac (udac→udIc); overrides: 6.4.138; ?udanc tag (via in_udanc helper) identifies ud compounds; fixes udac bha forms |
| 421 | 6.3.93 | समः समि | sam- → sami- before añcatir; bahiranga:1 fires before SK417; samyañc paradigm: samīcā bha via SK417 i→ī |
| 422 | 6.3.95 | सहस्य सध्रिः | saha- → sadhrī- before añcatir; bahiranga:1; sadhryañc paradigm; SK417 dirgha(ī)=ī no-op → sadhrīcā bha |
| 425 | 6.4.14 | अत्वसन्तस्य चाऽधातोः | upadhā dīrgha for u-it pum anga ending in -at (matup/ktavatu) or -as (Iyasun) before su (nom sg), not sambuddhi; bahiranga:3 fires before nUM; dhīmān, gomān |
| 427 | 7.1.78 | नाभ्यस्ताच्छतुः | Blocks nUM for abhyasta+śatṛ (–at) stems; apavāda of SK361 (7.1.70); condition: ?abhyasta + ?Satf; jakshat, jAgrat (and other jakshi-class) nom sg = plain -at form (no -an) |
| 428 | 6.1.6 | जक्षित्यादयः षट् | Tags 7 jakshi-class roots as inherently abhyasta: jakzat (SLP1 z=ṣ), jAgrat, daridrat, cakAsat, SAsat, dIDyat, vevyat; its=["f"]+other_tags=["Satf","abhyasta"] in pratipadika.py |
| 435 | 6.4.131 | वसोः संप्रसारणम् | samprasāraṇa v→u + ṣatva (s→ṣ/z) in bha for ?vasAnta (kvasu) stems; viduṣaḥ/ā/e/oḥ/ām bha forms of vidvas |
| 436 | 7.1.89 | पुंसोऽसुङ् | s→as (asun, u-it) before sarvānāmasthāna for ?puMs; SK425+SK361 give pumān nom sg; bha forms: puṃsaḥ/ā etc. |
| 440 | 8.2.34 | नहो धः | h→dh (D) before jhal or at pada-end for ?nah stems; upānat nom sg (via 8.4.56), upānadbhyām du/pl |
| 442 | 7.4.48 | अपो भि | p→t before bhi-initial suffix for ?ap (nityabahuvacana feminine); 8.4.53 gives t→d before voiced bh → adbhiḥ, adbhyaḥ |
| 443 | 8.2.68 | अहन् | n→ru at pada-end for ?ahan (neuter day stem); ahaḥ nom/acc/voc sg via ru→visarga; apavāda of 8.2.7 (n-lopa) |
| 437 | 7.2.107 | अदस औ सुलोपश्च | Out-of-SK-order, added with SK381: adas nom sg — final a→au (O), su deleted; asa+su→asau=असौ |
| 419 | 8.2.80 | अदसोऽसेर्दादु दो मः | adas sg/du/pl (excl. inst sg, nom/acc du handled by 6.1.102): fires on ?pada ?adas — amu sg (acc amum, dat/abl/gen/loc sg via ṣatva), amU du (nom/acc amū), amī pl (nom/acc/voc via SK438); _special_siddha(82080,14007) and (82080,73120) for 1.4.7+7.3.120 |
| 438 | 8.2.81 | एत ईद्बहुवचने | adas nom/acc/voc pl: pada-level rule, ade→amI (amī); out of SK order |
| 439 | 8.2.3 | न मु ने | adas inst sg amunā: fires at ada\|wA, overrides 7.1.12+6.1.101, sets ?pada on ada enabling SK419; _special_siddha(82080,14007/73120) propagates amu→Gi→nā; out of SK order |
| 656 | 1.2.48 | गोस्त्रियोरुपसर्जनस्य | go/strī in compound: hrasva |

---

## Implemented Sutras (additional, with SK numbers)

These sutras are implemented in `sutras_antaranga.yaml`. SK numbers sourced from `sk_map.md`.

| SK | Sutra ID | Sutra | Forms affected |
|----|----------|-------|----------------|
| 47 | 6.1.77 | इको यणचि | ik before ac: yaṇ (i→y, u→v, ṛ→r) — core vowel sandhi |
| 52 | 8.4.53 | झलां जश् झशि | Jhal before jhaś: jaś substitute (jihvā+mūlīya etc.) |
| 54 | 8.2.23 | संयोगान्तस्य लोपः | Saṃyoga-final pada: last consonant deleted |
| 61 | 6.1.78 | एचोऽयवायावः | ec before ac: e→ay, o→av, ai→āy, au→āv |
| 63 | 6.1.79 | वान्तो यि प्रत्यये | o/av before y-initial pratyaya: av |
| 67 | 8.3.19 | लोपः शाकल्यस्य | Śākalya's option: delete y between vowels (Vedic) |
| 69 | 6.1.87 | आद्गुणः | a/ā + vowel → guṇa — core sandhi (rāma + iti → rāmeti) |
| 72 | 6.1.88 | वृद्धिरेचि | a/ā + e/o/ai/au → vṛddhi (rāma + eva → rāmaiva) |
| 84 | 8.2.39 | झलां जशोऽन्ते | Jhal at pada-end → jaś (k→g, t→d, etc.) |
| 85 | 6.1.101 | अकः सवर्णे दीर्घः | Savarna vowels merge to dīrgha (ā+a→ā, i+i→ī etc.) |
| 86 | 6.1.109 | एङः पदान्तादति | Pada-final e/o before short a: e/o preserved, a elided |
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
| 124 | 8.4.58 | अनुस्वारस्य ययि परसवर्णः | Anusvāra before yay: parasavarna (rāmaṁ karoti → rāmaṅ k°) |
| 125 | 8.4.59 | वा पदान्तस्य | Pada-final anusvāra: parasavarna optional |
| 133 | 8.3.31 | शि तुक् | śi (neuter pl marker): tuk inserted before it after certain stems |
| 134 | 8.3.32 | ङमो ह्रस्वादचि ङमुण् नित्यम् | Ṅam after hrasva before vowel: ṅamuṇ (kam-api → kamapi) |
| 137 | 8.3.4 | अनुनासिकात् परोऽनुस्वारः | After anunāsika: anusvāra |
| 140 | 8.3.7 | नश्छव्यप्रशान् | n before ch-group: ś inserted (rāmāṃś ca) |
| 146 | 6.1.73 | छे च | c-initial pratyaya: insert t (tuk) before it |
| 147 | 6.1.74 | आङ्माङोश्च | āṅ/māṅ before vowel: chandas/veda usage |
| 148 | 6.1.75 | दीर्घात् | Long vowel + ch: tuk inserted |
| 149 | 6.1.76 | पदान्ताद्वा | Pada-final + ch: tuk optionally |
| 162 | 8.2.66 | ससजुषो रुः | s/sajuṣ at pada-end → ru (visarga source: rāmaḥ) |
| 163 | 6.1.113 | अतो रोरप्लुतादप्लुते | a-final pada + ru before a: ro'r (rāmaH + asti → rāmo'sti) |
| 169 | 8.3.20 | ओतो गार्ग्यस्य | Gārgya's option for o |
| 173 | 8.3.14 | रो रि | ru (=r) before r: lopa of ru, pūrva-dīrgha |
| 174 | 6.3.111 | ढ्रलोपे पूर्वस्य दीर्घोऽणः | Compensatory lengthening after ḍh/r lopa |
| 197 | 8.4.2 | अट्कुप्वाङ्नुम्व्यवायेऽपि | ṇatva even with aṭ/ku/pu/āṅ/num intervening |
| 198 | 8.4.37 | पदान्तस्य | Exception: no ṇatva at pada-end |
| 206 | 8.4.56 | वाऽवसाने | Optionally at avasāna: jhal → car |
| 212 | 8.3.59 | आदेशप्रत्यययोः | ādeśa/pratyaya context: ṇatva applies |
| 235 | 8.4.1 | रषाभ्यां नो णः समानपदे | n → ṇ after r/ṣ in same pada (ṇatva: rāmāṇām) |
| 236 | 8.2.7 | नलोपः प्रातिपदिकान्तस्य | n-final prātipadika at pada-end: n deleted (rājan+su → rājā) |
| 250 | 6.4.8 | सर्वनामस्थाने चासम्बुद्धौ | n-final + sarvānāmasthāna (non-voc): lengthening (rājā nom sg) |
| 324 | 8.2.31 | हो ढः | h at pada-end → ḍh (lih → liḍh) |
| 325 | 8.2.32 | दादेर्धातोर्घः | dā-initial dhātu h → gh at pada-end |
| 327 | 8.2.33 | वा द्रुहमुहष्णुहष्णिहाम् | druh/muh/ṣṇuh/ṣṇih: optionally gh or ḍh at pada-end |
| 378 | 8.2.30 | चोः कुः | c/ch/j/jh/ñ at pada-end → k-group |
| 59 | 8.4.46 | अचो रहाभ्यां द्वे | ac after ra/ha: double the following ac (dvitva sandhi) |
| 60 | 8.4.64 | हलो यमां यमि लोपः | yama hal before yama hal: delete the first yama (geminate simplification) |
| 71 | 8.4.65 | झरो झरि सवर्णे | jhar before savarna jhar: lopa of first |
| 76 | 8.3.15 | खरवसानयोर्विसर्जनीयः | ru/r before khar or at avasāna → visarjanīya (ḥ) |
| 123 | 8.3.24 | नश्चापदान्तस्य झलि | non-pada-final n before jhal → anusvāra |
| 138 | 8.3.34 | विसर्जनीयस्य सः | visarjanīya → s before khar (prathama tripādī) |
| 142 | 8.3.37 | कुप्वोः कपौ च | visarjanīya before ku/pu consonants → ka |
| 150 | 8.3.35 | शर्परे विसर्जनीयः | visarjanīya before śar group preserved as visarjanīya |
| 151 | 8.3.36 | वा शरि | optionally visarjanīya before śar (vibhāṣā to SK150) |
| 165 | 6.1.104 | नादिचि | pragṛhya ā-final: no sandhi before vowel (ā preserved) |
| 166 | 6.1.114 | हशि च | e/o-final + h-initial: pararūpa sandhi (also covers haśi before śi) |
| 167 | 8.3.17 | भोभगोअघोअपूर्वस्य योऽशि | bho/bhago/agho etc.: y inserted before aśi vowels |
| 191 | 6.1.97 | अतो गुणे | a + guṇa vowel (e/o/ai/au): pūrvarūpa (a absorbed) |
| 196 | 6.1.103 | तस्माच्छसो नः पुंसि | masculine: śas (acc pl) → nas after pronoun-base ending in that |
| 199 | 1.4.13 | यस्मात्प्रत्ययविधिस्तदादि प्रत्ययेऽङ्गम् | āṅga saṁjñā: portion from which a pratyaya operation is ordained is anga |
| 215 | 7.1.14 | सर्वनाम्नः स्मै | sarvanāma + dat sg e → smai (sarvasmai, tasmai, etc.) |
| 229 | 1.1.43 | सुडनपुंसकस्य | su/ḍ of non-neuter gender = sarvānāmasthāna |
| 230 | 1.4.17 | स्वादिष्वसर्वनामस्थाने | su-ādi non-sarvānāmasthāna: triggers bha saṁjñā for anga |
| 231 | 1.4.18 | यचि भम् | before yac pratyaya: anga gets bha saṁjñā |
| 237 | 6.4.136 | विभाषा ङिश्योः | optional al-lopa of n before Ṅi/ŚI (vibhāṣā apavāda to SK234) |
| 239 | 6.1.105 | दीर्घाज्जसि च | after dīrgha-final + jas: exception (no further sandhi change) |
| 244 | 7.3.120 | आङो नाऽस्त्रियाम् | āṅ: ā not lengthened in non-feminine context |
| 245 | 7.3.111 | घेर्ङिति | ghi-final anga + ṅit suffix: guṇa of i (nau: nauh; strī + ṅi: stry-ām bha) |
| 247 | 7.3.119 | अच्च घेः | ac-initial suffix after ghe: guṇa applies |
| 254 | 7.2.115 | अचोञ्णिति | ac-final anga before Ñit/Ṇit suffix: vṛddhi (primary vṛddhi rule) |
| 256 | 7.3.118 | औत् | o → au in certain anga positions (au-substitution) |
| 275 | 7.3.110 | ऋतो ङिसर्वनामस्थानयोः | ṛ-final anga before ṅi or sarvānāmasthāna: guṇa (ṛ→ar; kartari etc.) |
| 316 | 6.4.143 | टेः | ṭi (= from last vowel of anga) deleted before certain kṛt suffixes |
| 322 | 7.1.75 | अस्थिदधिसक्थ्यक्ष्णामनङुदात्तः | asthi/dadhi/sakthi/akṣan stems: anaN augment (udātta) before sarvānāmasthāna |
| 337 | 6.1.131 | दिव उत् | div-stem: u substituted for iv before certain endings (dyauḥ, divam, etc.) |
| 339 | 8.3.16 | रोः सुपि | r(u) before sup → visarjanīya (ḥ); source of pada-final visarga before sup |
| 343 | 7.2.108 | इदमो मः | idam: m substituted in certain positions (idaṁ, imaṁ etc.) |
| 344 | 7.2.111 | इदोऽय् पुंसि | idas masculine: ay substituted (masculine idam forms: ayam etc.) |
| 346 | 7.2.112 | अनाप्यकः | remaining idam substitutions (non-āp, non-a-final contexts) |
| 847 | 6.4.146 | ओर्गुणः | o → guṇa (e) in anga before certain suffixes (apavāda) |
| 1075 | 7.2.117 | तद्धितेष्वचामादेः | before taddhita suffix beginning with ac: vṛddhi of first vowel of anga |
| 2168 | 7.3.84 | सार्वधातुकार्धधातुकयोः | anga before sārvadhatuka/ārdhadhatuka: guṇa of final vowel (core verb guṇa rule) |
| 2189 | 7.3.86 | पुगन्तलघूपधस्य च | puganta or laghu-upadha anga before sārvadh/ārdh: guṇa of upadhā |
| 2217 | 1.1.5 | क्ङिति च | kit/ṅit suffix: no guṇa/vṛddhi substitution (blocks SK2168, SK254 etc.) |
| 2280 | 8.2.40 | झषस्तथोर्धोऽधः | jhaṣ before t/th: t/th → dh/dh (voiced aspiration assimilation) |
| 2282 | 7.2.116 | अत उपधायाः | a-upadhā anga before Ñit/Ṇit suffix: vṛddhi of upadhā a |
| 2335 | 8.3.13 | ढो ढे लोपः | ḍh before ḍh: lopa of first ḍh |
| 297 | 7.3.117 | इदुद्भ्याम् | i/u-final nadī anga before Ṅi: suffix → ām (nadī loc sg: nadyām, vadhvām); overrides SK256 (7.3.118) and 7.3.116 |

---

## Skipped / Deferred Sutras

| SK | Sutra ID | Sutra | Reason | Affects |
|----|----------|-------|--------|---------|
| 145 | 6.1.72 | संहितायाम् | Natural — saṃhitā adhikāra implicit in engine | FIXME comment in YAML; engine always operates in saṃhitā context for sandhi; no explicit rule block needed |
| 210 | 8.3.55 | अपदान्तस्य मूर्धन्यः | Natural — adhikāra comment only; no rule block in YAML | Retroflexion adhikāra header; actual ṇatva logic handled by SK235 (8.4.1) and SK212 (8.3.59) |
| 426 | 6.1.5 | उभे अभ्यस्तम् | Natural + manual tagging; dvitva engine not yet implemented | abhyasta saṁjñā for all forms resulting from reduplication (dadat, bibhrat, etc.); jakshi-class manually tagged via SK428 |
| 418 | 6.3.92 | विष्वग्देवयोश्च टेरद्र्यञ्चतावप्रत्यये | Partial — remaining sarvanāma | etad/idam/adas/sarva etc.; add sarvanAma+sarvanAma_pada tags to auto-extend SK418 |
| 55 | 8.4.48 | नादिन्याक्रोशे पुत्रस्य | Skipping for now | Vedic/accent |
| 56 | 8.4.50 | त्रिप्रभृतिषु शाकटायनस्य | Skipping for now | Śākaṭāyana option |
| 57 | 8.4.51 | सर्वत्र शाकल्यस्य | Skipping for now | Śākalya option |
| 58 | 8.4.52 | दीर्घादाचार्याणाम् | Skipping for now | Āchārya option |
| 75 | 6.1.85 | अन्तादिवच्च | Skipping for now | Sandhi edge case |
| 77 | 6.1.92 | वासुप्यापिशलेः | Skipping for now | Āpiśali dialect |
| 81 | 6.1.98 | अव्यक्तानुकरणस्यात इतौ | Skipping for now | Sound-imitation words |
| 82 | 6.1.99 | नाम्रेडितस्यान्त्यस्य तु वा | Skipping for now | Āmreḍita (reduplicated) words |
| 87 | 6.1.122 | सर्वत्र विभाषा गोः | Skipping for now | go-stem optional sandhi |
| 88 | 6.1.123 | अवङ् स्फोटायनस्य | Skipping for now | Sphoṭāyana option |
| 89 | 6.1.124 | इन्द्रे च | Skipping for now | indra compounds |
| 126 | 8.3.25 | मो राजि समः क्वौ | For later | kvip formations |
| 127 | 8.3.26 | हे मपरे वा | Skipping for now | hal-sandhi |
| 129 | 8.3.27 | न परे नः | Skipping for now | hal-sandhi |
| 130 | 8.3.28 | ङ्णोः कुक् टुक् शरि | Skipping for now | hal-sandhi |
| 131 | 8.3.29 | डः सि धुट् | Skipping for now | hal-sandhi |
| 132 | 8.3.30 | नश्च | Skipping for now | hal-sandhi |
| 135 | 8.3.5 | समः सुटि | For later | ru-sandhi |
| 139 | 8.3.6 | पुमः खय्यम्परे | For later | ru-sandhi |
| 141 | 8.3.10 | नॄन्पे | For later | ru-sandhi |
| 143 | 8.3.12 | कानाम्रेडिते | For later | ru-sandhi |
| 144 | 8.3.48 | कस्कादिषु च | For later | ru-sandhi |
| 238 | 6.3.110 | सङ्ख्याविसायपूर्वस्याह्नस्याऽहन्नन्यतरस्यां ङौ | For later | ahna/ahan in compounds |
| 258 | 1.1.23 | बहुगणवतुडति सङ्ख्या | For later | saṃkhyā definition |
| 292 | 1.1.28 | विभाषा दिक्समासे बहुव्रीहौ | For later | dik-compounds |
| 293 | 7.3.115 | विभाषा द्वितीयातृतीयाभ्याम् | For later | sarvanāma f. dat/ins |
| 307 | 8.4.12 | एकाजुत्तरपदे णः | For later | ṇatva in compounds |
| 321 | 7.1.74 | तृतीयादिषु भाषितपुंस्कं पुंवद्गालवस्य | For later | Gālava's option for neuter |
| 323 | 1.1.48 | एच इग्घ्रस्वादेशे | Handled elsewhere | `hrasva()` in paribhāṣā.py |
| 348 | 1.1.21 | आद्यन्तवदेकस्मिन् | Natural | Falls out of engine behaviour |
| 353 | 8.2.2 | नलोपः सुप्स्वरसंज्ञातुग्विधिषु कृति | Natural + special siddha | n-lopa in kṛt/kyac/kyaṇ contexts |
| 363 | 6.1.37 | न संप्रसारणे संप्रसारणम् | For later — kṛt/verbal only | blocks double samprasāraṇa; not needed for nominal declension (SK362's samprasArana_van produces no further samprasāraṇa candidate) |
| 364 | 6.4.127 | अर्वणस्त्रसावनञः | Partial — nañ exception pending | anarvan (nañ compound) should decline like yajvan but "arvan" tag is not propagated through compounds; structurally handled once nañ compound formation is added; verify then |
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
| 423 | 6.3.94 | तिरसस्तिर्यलोपे | Natural — pre-applied | tiras- → tiry- before añcatir with a-lopa; tiryac stored as weak form; tests pass |
| 424 | 6.4.30 | नाञ्चेः पूजायाम् | For later — exception | blocks n-lopa (SK415/6.4.24) for añcatir in honorific/pūjā context; no test coverage yet |
| 429 | 3.2.60 | त्यदादिषु दृशोऽनालोचने कञ्च | For later — kṛt | kañ/kvin after tyādi+dṛś; requires kṛt suffix machinery |
| 430 | 6.3.91 | सर्वनाम्नः पूर्वपदस्य | For later — compounds | ā for sarvanāma pūrva-pada before dṛg/dṛś/vat (tādṛk etc.); compound-only |
| 431 | 8.2.63 | नशेर्वा | For later | optional ś→ṣ for naś at pada-end; no naś prātipadika yet |
| 432 | 3.2.58 | स्पृशोऽनुदके क्विन् | For later — kṛt | kvin after √spṛś; requires kṛt suffix machinery |
| 433 | 8.2.76 | इटोऽत् | For later — verbal | upadhā-dīrgha for intensive/kṛdanta forms; not needed for current nominal test suite |
| 434 | 8.3.58 | नुम्विसर्जनीयशर्व्यवायेऽपि | For later — verbal | ṣatva with intervening chars; mainly verbal/intensive, not needed for nominal test suite |
| 441 | 7.2.110 | इदोऽय् पुंसि | For later | d→y of idam before su for feminine iyam; requires separate feminine idam prātipadika and several additional rules |

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
| dhImat | m | -at stem (matup u-it, SK425) | SK425 (6.4.14): upadhā dīrgha before su → dhīmān nom sg; SK361 nUM for sarvānāmasthāna → dhīmant strong forms; dhīmat weak forms |
| gomat | m | -at stem (matup u-it, SK425) | SK425 (6.4.14): upadhā dīrgha before su → gomān nom sg; same pattern as dhīmat |
| jakzat | m | -at stem (śatṛ f-it, abhyasta, SK427+SK428) | SK427 blocks nUM → all forms use plain jakzat- base; nom sg जक्षत्/जक्षद् (not *जक्षन्); SLP1 z=ṣ |
| jAgrat | m | -at stem (śatṛ f-it, abhyasta, SK427+SK428) | same as jakshat; nom sg जाग्रत् (not *जाग्रन्) |
| Bavat | m | -at stem (śatṛ f-it, regular, SK361) | SK361 +f block fires nUM → bhavant strong forms; nom sg भवन् (no SK425 — not u-it) |
| pacat | m | -at stem (śatṛ f-it, regular, SK361) | same as Bavat; nom sg पचन् |
| yuzmad | — | 2nd person pronoun (alinga) | SK382–SK400: full pronoun paradigm; nom tvam, acc tvām, abl sg tvat, gen sg tava, gen pl yuṣmākam etc. |
| asmad | — | 1st person pronoun (alinga) | SK382–SK400: full pronoun paradigm; nom aham, acc mām, abl sg mat, gen sg mama, gen pl asmākam etc. |
| tad | m | tyadAdi demonstrative | SK381 (7.2.106): nom sg m saḥ; partial table (nom sg only) |
| etad | m | tyadAdi demonstrative | SK381 (7.2.106): nom sg m eṣaḥ; partial table (nom sg only) |
| tyad | m | tyadAdi demonstrative | SK381 (7.2.106): nom sg m syaḥ; partial table (nom sg only) |
| adas | m | tyadAdi demonstrative | SK381+SK437 (7.2.106+7.2.107): nom sg asau; SK419 (8.2.80): amu sg/du/pl forms; SK438 (8.2.81): amī pl; SK439 (8.2.3): amunā inst sg; full vibhakti table (inst sg amunā, du amūbhyām, gen/loc du amuyoḥ) |
