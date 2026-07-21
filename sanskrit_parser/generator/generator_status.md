# Generator Implementation Status

Sutras are implemented following the Siddhantakaumudi (SK) order from
https://drdhaval2785.github.io/siddhantakaumudi/

_Earlier sets — the entire kāraka-prakaraṇam (SK 532–646, phases K0–K7 + K-UI), the
2026-06-27 kāraka review fixes, the avyayībhāva samāsa (SK 647–683, S0–S4 + composer/CLI),
and the complete tatpuruṣa prakaraṇa (SK 684–828, T0–T5 + T-liṅga + T-UI, with the
completeness audit) — are recorded in the Implemented-Sutras tables below, in
`karaka_plan.md` / `tatpuruza_plan.md`, and in git history._

**Last implemented:** **Bahuvrīhi samāsānta ādeśa/nipātana tail — B3 and B4 are now COMPLETE.** 12 rules: pāda 5.4.138/139 (व्याघ्रपात्, कुम्भपदी), datṛ 5.4.143/144/145 (फालदती, श्यावदन्, वृषदन्), kakud 5.4.147/148/149 (त्रिककुत्, उत्काकुत्, पूर्णकाकुत्), nipātanas 5.4.125/126 (सुजम्भा, दक्षिणेर्मा), and अच् 5.4.120/121 (चतुरश्रः, असक्थः/असक्थिः) via a new `ac_s` affix. **5.4.113 gained its own स्वाङ्गात् guard** plus an explicit नञ्/दुस्/सु exclusion — `overrides:` cannot reach across a vibhāṣā fork. Zero regressions (8243 passed).

**Next to be implemented:** **The केशाकेशि cluster** — SK846/2.2.27 (needs a new lp==rp sarūpa content check) + SK866/5.4.127 इच् + **6.3.137 अन्येषामपि दृश्यते** + avyaya tagging; it also unlocks 6.4.146 ओर्गुणः/बाहूबाहवि. Then the **physical pūrva-nipāta (2.2.30)** group — SK898–900/2.2.35–37 + the B0 reorder — which is the highest-leverage item left, since tatpuruṣa deferred the same mechanism. Then B1 6.3.35/36/39 (affix-context machinery). Latent gaps: **1.2.48's `?pum_abs` FIXME** (blocks upasarjana shortening — बहुनाडिः; would make 7.4.14 load-bearing), **5.4.153's नदी arm keying on `?NI` not the 1.4.3 saṁjñā** (excludes तन्त्री), general cross-member ṇatva (चोरभयेण). Tatpuruṣa deferrals unchanged.

---

## Summary

| Category | Count |
|---|---|
| Sutras implemented | 587 |
| Sutras skipped / deferred | 170 |
| Sutras uncatalogued / not yet planned | ~29 |
| **Total sutras accounted for** | **~742** |
| Stems with full vibhakti test tables | 315 |
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
| 75 | 6.1.85 | अन्तादिवच्च | pariBAzA for the 6.1.84 ekaḥ pūrvaparayoḥ adhikāra. The single ekādeśa substitute behaves as the final (anta) of pūrva and the initial (ādi) of para. **Uniform** engine mechanism (`purvapara: true` flag + `?antAdivat` saṁjñā): ALL ekādeśa rules (6.1.87/88/89/91/93/94/95/97/101/102/107) lump the substitute on the right (xform `l: null` + `r:` expr). The engine (`antaranga_prakriya._apply_antadivat`) marks the consonant-final residue ?antAdivat; `sutra._env` synthesises l = substitute **for condition checks only** (xform uses physical strings — no re-append), so phoneme-keyed rules (6.4.8 l:n) see the antavat boundary without the old `-aNga/-Ba/-pada` strips. The engine does no tag stripping at all: the one tag-keyed bha-rule that would mis-read the migrated anta (6.4.130 pādaḥ pat) carries its own `l: d`, which the synth (l = substitute vowel on a guṇa residue) fails — so all saṁjñās (?aNga/?Ba/?pada) survive (e.g. 6.1.103 reads ?aNga, 6.4.130 reads ?Ba). The ekādeśa set + every both-l-and-r vowel-junction rule (computed via `_cond_has_both_l_and_r`) are disabled at the resolved junction — this is the simultaneity caveat and subsumes the old 6.1.107→7.3.102 override and the 6.1.77/78 special-casing. The same tagging is replayed in the `_nitya` priority simulation, and the nitya disable-check reads the post-`s` output, so sutra-priority is consistent. Replaces all the old scattered tag-stripping / hrasva-trick / ad-hoc overrides. Also fixed a latent bug in 7.1.13 ṅeryaḥ (now requires the live ṅe content `=e`, not just the ?Ne tag) so it no longer mis-fires after 7.1.28 replaces ṅe→am in the yuzmad/asmad dative |
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
| 376 | 7.1.71 | युजेरसमासे | num (ñ) augment for non-compound yuj before sarvanamasthāna; yuñjau, yuñjaḥ strong; yuṅ nom sg. Compound yuj (aśvayuk type): the live `aSvayuj` = [aSva, in_compound(yuj_kvin)] gets `?samAsa` via in_compound, which blocks nUM (preformed `yuj_kvin_samAsa` retired); SK257 pattern |
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
| 416 | 6.4.138 | अचः | delete 'a' of añc (post-SK415 form 'ac') in bha-anga context; ll:'a' condition excludes prAc (long A); llp:=!ud excludes ud-prefix (SK420 apavāda, reads left-neighbour pada); pratyac/tiryac bha forms use pratīc/tiryc base |
| 417 | 6.3.138 | चौ | lengthen final vowel of preceding member before añc reduced to 'c'; fires at (prefix\|c_result) after SK416; prati→pratI, pra→prA; yaṇ (6.1.77) blocked by akṛtavyūhā paribhāṣā |
| 418 | 6.3.92 | विष्वग्देवयोश्च टेरद्र्यञ्चतावप्रत्यये | ṭi→adri before añcatir (viṣvag/deva/tad/yad/kim/etad/idam/adas/sarva); ticAdesha_adri helper; luk_sup propagates sarvanAma→sarvanAma_pada; bahiranga:1 fires before SK417 |
| 420 | 6.4.139 | उद ईत् | apavāda of SK416: ud+añc in bha → substitute ī for 'a' of ac (udac→udIc); overrides: 6.4.138; llp:=ud reads the ud prefix as the left-neighbour pada (no udanc tag); fixes udac bha forms |
| 421 | 6.3.93 | समः समि | sam- → sami- before añcatir; bahiranga:1 fires before SK417; samyañc paradigm: samīcā bha via SK417 i→ī |
| 422 | 6.3.95 | सहस्य सध्रिः | saha- → sadhrī- before añcatir; bahiranga:1; sadhryañc paradigm; SK417 dirgha(ī)=ī no-op → sadhrīcā bha |
| 425 | 6.4.14 | अत्वसन्तस्य चाऽधातोः | upadhā dīrgha for a pum anga before su (nom sg), not sambuddhi; bahiranga:3 fires before nUM; dhīmān, gomān. **-at arm**: u-it (matup/ktavatu). **-as arm: WIDENED — the old `+u` restriction limited it to īyasun, so an underived अस्-noun never lengthened (यशस्+su → यशः); now ANY non-dhātu masc अस्-final stem lengthens → यशाः, मनाः, बहुयशाः**, unlocking the SK891 pair बहुयशस्कः/बहुयशाः. Guarded `?!avyaya`/`?!nipAta`/`?!sarvanAma` so as-final non-declining/pronominal stems are untouched (तिरः, अधः, **असौ**); neuter unaffected (मनः/यशः); श्रेयान्/विद्वान् unchanged |
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
| – | 4.1.4.1 | अजाद्यतष्टाप् (ajādi-prabalatva, non-Dvigu) | Vārttika-style apavāda: a ?ajAdi stem takes ṭāp, overriding every ṅīp/ṅīṣ rule the gaṇa's subgroups invoke (`overrides: [4.1.6, 4.1.15, 4.1.16, 4.1.20, 4.1.63, 4.1.64]`). **4.1.63 (SK518) and 4.1.64 (SK519) added** per Vasu's per-item N.B. (items 1–6 jāti override 4.1.63; items 15–26 phala/puṣpa override 4.1.64); simple ajādi words keep ?ajAdi (कोकिला via the 4.1.63 override). The gaṇa's **compound** members (phala/puṣpa/lyuṬ/nañ/devaviś) are no longer baked: a second arm `lp: [and, ?samAsa, $$ajAdi_samasta]` detects them by the (pūrva,uttara) canonical pair (`paribhasha._AJADI_SAMASTA`), so भस्त्रफला takes ṭāp (override 4.1.64) while the jāti दासीफली stays ṅīṣ. Tests: kokila_A, BastraPalA. The simple-word path still rides `_propagate(last, ["ajAdi","ajAdi_in_Dvigu"])` in `join_objects()` (tryanīkā). The 4.1.21 override is in 4.1.4.2 below |
| – | 4.1.4.2 | अजाद्यतष्टाप् (ajādi-prabalatva over 4.1.21 Dvigu) | Narrow apavāda over SK479: fires only for the phala/puṣpa compound-class subgroup of the ajādi-gaṇa (items 15–26 + Pala/anIka), tagged ?ajAdi_in_Dvigu. Vasu's N.B. on items 19–20: "त्रिफला when a Dvigu Compound forms its feminine as त्रिफला". Other ajādi members (e.g. aśva, item 5) override 4.1.63 (SK518) jāti-ṅīṣ (Vasu prints "4.2.63", a cross-ref typo) — which doesn't apply in Dvigu — so SK479 ṅīp wins for them in Dvigu, giving पञ्चाश्वी for samāhāra-Dvigu of aśva per Vasu/SK on SK480. Drives त्रिफला (tri+Pala) and त्र्यनीका (tri+anIka — anīka treated as phala-class by analogy) |
| 480 | 4.1.22 | अपरिमाणबिस्ताचितकम्बल्येभ्यो न तद्धितलुकि | Niṣedha to SK479 for an a-final Dvigu compound with a luk'd taddhita on top: blocks ṅīp (selects ṭāp via `orp: =Ap`) when the uttara-pada is NOT ?parimARa, OR is one of बिस्त/आचित/कम्बल्य (?bistAdi). `?!kARqa` excludes kāṇḍa-final stems (SK481 handles them); puruṣa is NOT excluded — SK482 optionally re-enables ṅīp on top. Built on a new `luk_tadDita` Pratyaya (empty, ?tadDita+?luk_tadDita); ?luk_tadDita rides through the (aṅga, luk_tadDita) merge via the aṅga-gated `_propagate(last, [...])`, and the semantic class tags ride from both first and last in `_propagate`. Drives पञ्चाश्वा, द्विबिस्ता, द्व्याचिता, द्विकम्बल्या; counters: द्व्याढकी (ādhaka = parimāṇa), trilokI (no luk) |
| 481 | 4.1.23 | काण्डान्तात्क्षेत्रे | Niyama on SK480 for kāṇḍa-final Dvigus: blocks ṅīp (selects ṭāp) only in the kṣetra ('field') sense via a semantic `?kzetre` tag attached by the test composer (`in_context(..., "kzetre")`). Non-kṣetra kāṇḍa-Dvigus fall through to SK479 → ṅīp (द्विकाण्डी रज्जुः). Drives द्विकाण्डा क्षेत्रभक्तिः |
| 482 | 4.1.24 | पुरुषात्प्रमाणेऽन्यतरस्याम् | Vibhāṣā: optionally re-enables ṅīp for puruṣa-final Dvigus in the pramāṇa sense via semantic `?pramARe` tag (`in_context(..., "pramARe")`). `overrides: 4.1.21` (NOT 4.1.22) — if SK482 overrode 4.1.22 the optional-fired branch would disable SK480 on v0 (engine's optional-overrides disabling in `antaranga_prakriya.py:712-715`), so the SK482-skip branch would lose its fallback. By overriding 4.1.21 instead, the skip branch leaves SK480 free to fire → ṭāp (द्विपुरुषा); the fire branch wins over SK480 by higher _aps_num → ṅīp (द्विपुरुषी). Both Vasu alternants produced. Non-pramāṇa puruṣa-Dvigu falls to SK480 only → द्विपुरुषा |
| 483 | 5.4.131 | ऊधसोऽनङ् | anaṅ substitute for final ūdhas in bahuvrīhi feminine: surface = replace final `s` of UDas with `n` (UDas → UDan). bahiranga: 1 fires before NIz/NIp selection. After SK484/485 adds the ī suffix, SK234 (6.4.134) drops the upadhā `a` of -an → kuRqoDnī, GhaToDnī, dvyUDnī, atyUDnī. New stem UDas tagged ?uDanta |
| 484 | 4.1.25 | बहुव्रीहेरूधसो ङीष् | ṅīṣ (NIz) after a bahuvrīhi ending in ūdhas (now ūdhan post-SK483), feminine. `overrides: [4.1.4, 4.1.13]` blocks the ṭāp/ḍāp candidates Vasu names. Drives कुण्डोध्नी and घटोध्नी; new test stems `kuRqa`, `Gawa` (ṭ in SLP1 = `w`) |
| 485 | 4.1.26 | संख्याऽव्ययादेर्ङीप् | Apavāda to SK484 (ṅīṣopavāda): NIp instead of NIz when the bahuvrīhi begins with a saṃkhyā or avyaya. Two arms read the *pūrva-pada* by peeking the left neighbour: saṃkhyā via `llp: ?saMKyA`, avyaya via `llp: ?avyaya` (these pūrva-pada class tags are propagated to the neighbour in `join_objects`, gated on ?samAsaPurva, deleted at the samasta_pada merge) — replacing the old fake ?saMKyAdi/?avyayAdi tags on UDas. Drives द्व्यूध्नी (saṃkhyādi) and अत्यूध्नी (avyayādi; avyaya stem `ati`) |
| 486 | 4.1.27 | दामहायनान्ताच्च | Bahuvrīhi beginning with saṃkhyā ending in दामन्/हायन: NIp in feminine. Both arms peek the saṃkhyā pūrva-pada via `llp: ?saMKyA` (the tag is propagated to the neighbour in `join_objects`; replaces the fake ?saMKyAdi on the uttara-pada): (a) ?dAman — no semantic restriction (द्विदाम्नी; SK234 a-lopa); (b) ?hAyana + ?vayasi — restricted to age sense (द्विहायनी via 6.4.148 a-lopa). Non-age hāyana → 4.1.4 ṭāp (द्विहायना). Stems `dAman`, `hAyana`. `overrides: [4.1.4]` |
| – | 4.1.27.1 | (vārttika) त्रिचतुर्भ्यां हायनस्य णत्वं वयोवाचकस्यैव | Upadhā n→ṇ in hāyana when pūrva-pada is tri/catur AND age (?vayasi) sense. `xform: lc: lc[:-1]+str("R")` makes hāyana → hāyaṇa; SK486 then NIp; 6.4.148 a-lopa → trihāyaṇī, caturhāyaṇī. The tri/catur pūrva-pada is read via `llp: [=tri, =catur]` (a robust identity peek — a neighbour *tag* peek like ?saMKyA is not reliably visible at this bahiranga-2 window). bahiranga: 1 fires before SK486 (bahiranga: 2). Non-age trihāyana → no vārttika, no SK486 → 4.1.4 ṭāp → त्रिहायना (Vasu's exact शाला example). Engine adjustment in the pūrvāparayoḥ section: 6.1.87 (आद्गुणः) now strips `sarvanAmasTAna` from the post-guṇa suffix (`orp: -sarvanAmasTAna`), so 6.4.8 does not re-fire on the n-final surface produced by ṭāp + guṇa (hāyan|e). Broader pūrvāparayoḥ refactor pending — captured as a TODO |
| 487 | 4.1.29 | नित्यं संज्ञाछन्दसोः | Mandatory NIp on upadhā-lopin an-bahuvrīhi in saṃjñā or chandas. Apavāda to SK462 (4.1.28); `overrides: [4.1.4, 4.1.12, 4.1.13, 4.1.28]`. ?saMjYA / ?Candas attached via test composer in_context; reuses `$$upaDAlopI` from SK462. Drives अतिराज्ञी (saṃjñā example) |
| 488 | 4.1.30 | केवलमामकभागधेयपापापरसमानार्यकृतसुमङ्गलभेषजाच्च | Mandatory NIp for nine `?keval_Adi` stems in saṃjñā/chandas. `overrides: 4.1.4`. Positive arm → केवली / मामकी / सुमङ्गली; laukika negative arm → 4.1.4 ṭāp + SK463 idādeśa for `?ka_pratyaya`-tagged mAmaka → मामिका. Niyama-blocker 4.1.30.1 (मामकग्रहणं नियमार्थम्) overrides SK470 for ?mAmaka outside saṃjñā/chandas — currently inert (mAmaka lacks ?NIp_taddhita) but forward-compatible |
| 489 | 4.1.32 | अन्तर्वत्पतिवतोर्नुक् | नुक् augment (single 'n' at end of stem) on antarvat / pativat in feminine. Treated as single irregular pratipadikas (?antarvat_pativat). bahiranga: 1 left-substitution `lc: lc+l+str("n"), l: null` appends n; SK453 (4.1.5) at bahiranga 2 then supplies NIp → अन्तर्वत्नी / पतिवत्नी. Semantic restriction (?garBiNi / ?jIvadBartfka) not encoded — see Skipped table |
| 490 | 4.1.33 | पत्युर्नो यज्ञसंयोगे | i→n on plain pati before NIp. Condition `?pati + ?!samAsa`; bahiranga: 1. SK453 then supplies NIp → पत्नी. Semantic restriction (?yajYasaMyoga) not encoded — see Skipped table |
| 491 | 4.1.34 | विभाषा सपूर्वस्य | i→n on pati when uttara-pada of compound. Condition `?pati + ?samAsa`; bahiranga: 1. Vibhāṣā implemented as mandatory in this batch (the non-substituted गृहपतिः fork is deferred). Drives गृहपत्नी declining as the textbook nadī. Required guarding 1.4.7 (all three arms) and 1.4.8 with `rp: ?!strI`, and 1.4.8 additionally with `lp: ?!strI`, so Ghi-saṃjña never lands on the feminine path |
| 492 | 4.1.35 | नित्यं सपत्न्यादिषु | Mandatory (nitya) i→n for the sapatnyAdi gaṇa. `overrides: [4.1.33, 4.1.34]`. Detects the gaṇa by peeking the pūrva-pada identity `llp: [=sa, =eka, =vIra]` on live `pūrva + pati` compounds (mirrors the 4.1.57 llp precedent); the समानस्य सभावोऽपि niyama uses the reduced pūrva-pada `sa` (sa_pUrva). Pre-substituted `?sapatnyAdi` stems retired. Drives सपत्नी / एकपत्नी / वीरपत्नी |
| 493 | 4.1.36 | पूतक्रतोरै च | pūtakratu (live compound pūta + kratu): 4.1.36 peeks `llp: =pUta` + reads kratu in-window (`lp: =kratu`), final u → ai (`str("E")`) + NIp; `overrides: 4.1.4`; bahiranga 2. 6.1.78 sandhi → पूतक्रतायी (nadī). puṃyoga restriction deferred |
| 494 | 4.1.37 | वृषाकप्यग्निकुसितकुसिदानामुदात्तः | ?vfzAkapyAdi stems (vfzAkapi/agni/kusita/kusida) final vowel → ai + NIp → वृषाकपायी/अग्नायी/कुसितायी/कुसिदायी. kusita/kusida hrasva-madhya per SK (not Vasu's कुसीद) |
| 495 | 4.1.38 | मनोरौ वा | manu final u → au (`str("O")`) optionally + NIp → मनावी; skip-fork = plain u-stem मनुः. No `overrides` (ṭāp can't reach a u-stem). ai-variant मनायी deferred |
| 496 | 4.1.39 | वर्णादनुदात्तात्तोपधात्तो नः | ?varNa_topaDa colour stems: optional NIp + त्→न् (`lc: lc[:-1]+str("n")`) → एनी/रोहिणी (ṇatva); skip-fork → 4.1.4 ṭāp → एता. No `overrides: 4.1.4` (vibhāṣā two-fork design, cf. SK482); fire-fork wins by para-kāryam |
| 497 | 4.1.40 | अन्यतो ङीष् | ?varNa_anyatas colour stems (non-t-upadhā) → NIz; `overrides: 4.1.4` → सारङ्गी, कल्माषी, शबली (surface ī; accent not modelled) |
| 498 | 4.1.41 | षिद्गौरादिभ्यश्च | ṣit stems (`lp: +z` — the actual ṣ it-marker, which propagates from a ṣvun/ṣit affix via join_objects 1.2.46; nartaka given `its=["z"]`) and ?gaurAdi gaṇa stems → NIz; `overrides: 4.1.4` → नर्तकी, गौरी, मत्सी, हयी, शर्करी. gaurādi expanded to ~57 named simple members from Vasu's list |
| 499 | 6.4.149 | सूर्यतिष्यागस्त्यमत्स्यानां य उपधायाः | ābhīya upadhā y-lopa for ?sUryAdi (matsya) before the feminine ī (`lc: lc[:-1]`, condition `ll: y, rp: ?NI`); asiddha peer of 6.4.148 (`_ASIDDHA_PEERS`) so it composes with yasyeti's a-lopa → मत्सी. sūrya/tiṣya/agastya taddhita derivatives deferred |
| 500 | 4.1.42 | जानपदकुण्ड…कबरात् | 11 `?jAnapadAdi` stems → NIz (overrides 4.1.4) → जानपदी, कुण्डी, गोणी. The 11 distinct senses not modelled (fires unconditionally) |
| 501 | 4.1.43 | शोणात्प्राचाम् | śoṇa (`?SoRa`) → **optional** NIz (no overrides) → शोणी / शोणा (ṭāp skip-fork) |
| 502 | 4.1.44 | वोतो गुणवचनात् | u-final `?guRavacana` → optional NIz → मृद्वी / मृदुः (u-stem skip-fork). kharu/saṃyoga-upadhā exception deferred |
| 503 | 4.1.45 | बह्वादिभ्यश्च | `?bahvAdi` → optional NIz → बह्वी / बहुः, चण्डा/चण्डी, कपिः/कपी. bahvādi expanded to ~27 named simple members from Vasu's list. gaṇasūtras (रात्रि/शकटि/पद्धति) deferred |
| 504 | 4.1.48 | पुंयोगादाख्यायाम् | `?puMyoga` male-designation → NIz (overrides 4.1.4) → गोपी. puṃyoga semantics + vārttikas (गोपालिका, सूर्या) deferred |
| 505 | 4.1.49 | इन्द्रवरुण…आनुक् | `?indrAnuk` (12 stems): **ānuk augment** आन् (`lc: lc+dirgha(l)+str("n"), l: null`) + NIz (overrides 4.1.4/4.1.5) → इन्द्राणी/रुद्राणी (ṇatva), वरुणानी/हिमानी/अरण्यानी/मातुलानी (n stays). Required the 6.4.134 `ll: at` fix (pratyāhāra, short-अ only). Senses + मातुली optional-ānuk vārttika deferred |
| 6.4.134 | 6.4.134 | अल्लोपोऽनः (refinement) | `ll: a`→`ll: at` (pratyāhāra, the Pāṇinian term): अल् names only the short अ; a savarṇa match wrongly deleted the long आ of SK505's ānuk augment (इन्द्रान्→इन्द्र्णी). All real an-stems (rājan/takṣan/ahan) have short-a penult → unaffected. Additionally, `?sUryAdi` added to tier-3 taddhita propagation in `join_objects` → enables SK499 taddhita forms सौरी/तैषी |
| 506 | 4.1.50 | क्रीतात्करणपूर्वात् | karaṇa-pūrva (`llp: ?karaNa`) + krīta-final (`lp: =krIta`) compound → ṅīṣ; `overrides: 4.1.4` → वस्त्रक्रीती. (धनक्रीता deferred: dhana not tagged ?karaNa.) ?karaNa propagated through the pūrva+luk_sup merge (tier-1) so it is readable at the strī window's llp |
| 507 | 4.1.51 | क्तादल्पाख्यायाम् | `llp: ?karaNa` + `lp: ?ktAnta` → ṅīṣ; `overrides: 4.1.4` → अभ्रलिप्ती. alpa sense deferred (counter चन्दनलिप्ता: not ?karaNa) |
| 510 | 4.1.54 | स्वाङ्गाच्चोपसर्जनादसंयोगोपधात् | upasarjana svāṅga (`lp: [and, ?svAnga, ?samAsa, $$asaMyogopaDa]`), a-final → optional ṅīṣ → अतिकेशी/अतिकेशा, चन्द्रमुखी/चन्द्रमुखा. `$$asaMyogopaDa` (new helper) blocks conjunct-upadhā सुगुल्फा → ṭāp; bare शिखा (no ?samAsa) → ṭāp |
| 511 | 4.1.55 | नासिकोदरौष्ठजङ्घादन्तकर्णशृङ्गाच्च | optional ṅīṣ for a compound ending in one of the 7 named svāṅga words. **Refactored** to `lp: ?samAsa` (intrinsic compound-member test; 7 OR-arms) — replacing the earlier `llp: ?samAsaPurva`. → तुङ्गकर्णी/तुङ्गकर्णा. Now correctly guarded by the SK512/513/514 niṣedhas |
| 512 | 4.1.56 | न क्रोडादिबह्वचः | niṣedha: kroḍādi (`?kroqAdi`) or bahvac (`$$bahvac`, 3+ vowels) svāṅga compound → no ṅīṣ; `overrides: 4.1.54`, `update: null` → ṭāp. → कल्याणक्रोडा, सुजघना. The 7 named in 4.1.55 stay exempt (overrides 4.1.54 only) |
| 513 | 4.1.57 | सहनञ्विद्यमानपूर्वाच्च | niṣedha: svāṅga compound with saha/nañ/vidyamāna pūrva (`llp: [=sa, =a, =vidyamAna]`) → no ṅīṣ; `overrides: [4.1.54, 4.1.55]` (blocks even a named-7 word per विद्यमाननासिका), `update: null` → ṭāp. → सकेशा |
| 514 | 4.1.58 | नखमुखात्संज्ञायाम् | niṣedha: nakha/mukha-final compound in saṃjñā (`lp: [and, ?samAsa, ?saMjYA, =naKa/=muKa]`) → no ṅīṣ; `overrides: 4.1.54`, `update: null` → ṭāp. → शूर्पणखा, गौरमुखा. (counter ताम्रमुखी: no ?saMjYA → ṅīṣ) |
| 515 | 4.1.60 | दिक्पूर्वपदान्ङीप् | dik-pūrva (`llp: ?dik`) svāṅga compound → **ṅīp** (not ṅīṣ); `overrides: [4.1.4, 4.1.54]` → प्राङ्मुखी/प्राग्मुखी (8.4.45 optional anunāsika). The dik pūrva प्राच् is derived live (pra+añc+kvin, the prAc paradigm, tagged ?dik); ?dik propagated through the pūrva+luk_sup merge to the strī window's llp |
| 517 | 4.1.62 | सख्यशिश्वीति भाषायाम् | sakhi (?sakhyAdi) → NIz → सखी. Needed ?!strI guards on 7.1.92/7.1.93 (saKi tag rides onto the merged feminine). bhāṣā restriction deferred |
| 518 | 4.1.63 | जातेरस्त्रीविषयादयोपधात् | jāti, non-stree, non-y-upadhā (?jAti_ayopaDa) → NIz → ब्राह्मणी, कुक्कुटी, सूकरी. Restrictions encoded by tagging only eligible stems |
| 519 | 4.1.64 | पाककर्णपर्ण…उत्तरपदाच्च | a samāsa whose uttara is one of the 7 pākādi words → NIz. `lp: [and, ?samAsa, ?pAkAdi]`, `overrides: [4.1.4, 4.1.55]`. ?pAkAdi is intrinsic on pāka/parṇa/puṣpa/phala/mūla/vāla and **per-instance on karṇa** (shared with the SK511 svāṅga case, so tuṅgakarṇā keeps its ṭāp fork). **All 7 live** → ओदनपाकी, शङ्कुकर्णी, शालपर्णी, शङ्खपुष्पी, दासीफली, दर्भमूली, गोवाली. The ajādi/dvigu phala/puṣpa compounds (भस्त्रफला/त्रिफला) take ṭāp instead via `$$ajAdi_samasta` (4.1.4.1/4.1.4.2 override 4.1.64) |
| 520 | 4.1.65 | इतो मनुष्यजातेः | i-final manuṣya-jāti (?mAnuzya_jAti_i, l:i) → NIz → अवन्ती, कुन्ती, प्लाक्षी (plākṣi = post-iñ base) |
| 521 | 4.1.66 | ऊङुतः | u-final (l:ut, short-u), non-y-upadhā manuṣya-jāti (?manuzya_jAti_u) → **ūṅ (UN)** → कुरूः, ब्रह्मबन्धूः (vadhū-type; कुरूणाम् ṇatva) |
| 522 | 4.1.67 | बाह्वन्तात्संज्ञायाम् | bāhu-final saṃjñā (?bAhvanta_saMjYA) → ūṅ → भद्रबाहूः |
| 523 | 4.1.68 | पङ्गोश्च | paṅgu (?paNgu_class, l:ut) → ūṅ → पङ्गूः; śvaśrū pre-registered (श्वश्रूः; vārttika derivation deferred) |
| 524 | 4.1.69 | ऊरूत्तरपदादौपम्ये | upamāna-first ūru-compound (?Uru_upamAna) → ūṅ → करभोरूः |
| 525 | 4.1.70 | संहितशफलक्षणवामादेश्च | saṃhita/śapha/lakṣaṇa/vāma + ūru → ūṅ. Live compound: `lp: ?Uru_uttara` (ūru uttara-pada, in-window) + `llp: [=saMhita, =SaPa, =lakzaRa, =vAma]` (pūrva-pada identity peek); a+ū→o junction via 6.1.87 → संहितोरूः, शफोरूः, लक्षणोरूः, वामोरूः. Replaces preformed `?saMhitAdi_Uru` stems |
| 526 | 4.1.72 | संज्ञायाम् | kadrū/kamaṇḍalū in saṃjñā → ūṅ. Pre-registered as ū-strī prātipadikas (कद्रूः, कमण्डलूः); no YAML rule (the ū-finals decline directly) |
| 527 | 4.1.73 | शार्ङ्गरवाद्यञो ङीन् | **ṅīn (NIn)** for the full śārṅgaravādi gaṇa (?zANgaravAdi): śārṅgarava/kāpaṭava/gauggulava/baida/gautama (+ brāhmaṇa, registered for SK518; same ब्राह्मणी surface) → शार्ङ्गरवी/कापटवी/गौग्गुलवी/बैदी/गौतमी. gaṇasūtra नृनरयोर्वृद्धिश्च → नारी via live [nara, aR_t, strI_abs] (aṇ ādivṛddhi nara→nāra; surface-identical to ṅīn; नारीणाम् ṇatva). The 2nd arm (any añ-ending jāti → ṅīn) is covered for tagged stems, not as a general structural rule — see Skipped |
| 528 | 4.1.74 | यङश्चाप् | ñyaṅ/ṣyañ-derived stems (?yaNzdavya) → **cāp (cAp)** → आम्बष्ठ्या, कारीषगन्ध्या (ramā-type; surface = ṭāp, accent deferred) |
| 529 | 4.1.75 | आवट्याच्च | āvaṭya (?AvawI) → cāp; overrides 4.1.4 + 4.1.14 → आवट्या |
| 530 | 4.1.76 | तद्धिताः | Adhikāra — "the following are taddhita." No rule. Governs SK531+ |
| 531 | 4.1.77 | यूनस्तिः | yuvan + **ti (ti_t taddhita)** → युवतिः. Composed [yuvan, ti_t, strI_abs]; the i-final yuvati takes the feminine with vayasi-prathama dat/abl/loc-sg variants (युवतये/युवत्यै etc.) |
| 532 | 2.3.46 | प्रातिपदिकार्थलिङ्गपरिमाणवचनमात्रे प्रथमा | kāraka/vibhakti selection (pre-pass): prathamā for mere stem-meaning (arm 1: ?prAtipadika, no kāraka/vibhakti/śeṣa/sambodhana) and for an abhihita kāraka (arms 2–3: ?kAraka_karma + rp ?karmaRi; ?kAraka_kartA + rp ?kartari) → कृष्णः, हरिः सेव्यते, रामो हरिं भजति |
| 533 | 2.3.47 | संबोधने च | kāraka/vibhakti selection (pre-pass): semantic_samboDana → viBakti_8 (sup row 8, sambuddhi) → हे राम, हे हरे, हे हरयः |
| 534 | 1.4.23 | कारके | Adhikāra — engine semantics: the kāraka pre-pass scope (`AntarangaPrakriya._karaka_prepass`, window = noun \| sentence-dhātu). No YAML rule |
| 535 | 1.4.49 | कर्तुरीप्सिततमं कर्म | kāraka saṁjñā (pre-pass): semantic_Ipsitatama → kAraka_karma → हरिं भजति; counterexample: untagged co-participant (माष slot) stays kāraka-free |
| 536 | 2.3.1 | अनभिहिते | Adhikāra — engine semantics: the 2.3.x rules read the verb's prayoga tag via rp (kartari/karmaRi/BAve on the pre-formed tiṅanta pada); abhihita kārakas fall through to 2.3.46 prathamā. No YAML rule |
| 537 | 2.3.2 | कर्मणि द्वितीया | vibhakti (pre-pass): kAraka_karma + rp ?!karmaRi → viBakti_2 → हरिम्/हरी/हरीन् भजति |
| 538 | 1.4.50 | तथायुक्तं चानीप्सितम् | kāraka saṁjñā (K1): semantic_anIpsita → kAraka_karma (anīpsita-but-connected) → तृणं स्पृशति. Beats 2.3.46 by nitya |
| 539 | 1.4.51 | अकथितं च | kāraka saṁjñā (K1): in dvikarmaka (rp ?dvikarmaka, duhādi-12 + nī-ādi-4) the akathita kāraka (semantic_akaTita) → kAraka_karma → गां दोग्धि पयः; **vārttika** अकर्मकधातुभिर्योगे देशकालभावाध्वनः कर्म: semantic_deSakAlAdhvan + rp ?akarmaka → kAraka_karma → मासमास्ते |
| 540 | 1.4.52 | गतिबुद्धिप्रत्यवसानार्थशब्दकर्माकर्मकाणामणि कर्ता स णौ | kāraka saṁjñā (K1): ṇyanta kartṛ of gati/buddhi/pratyavasāna/śabdakarma/akarmaka → karma — semantic_svatantra + rp [and ?Ryanta ?<class>] (5-arm OR) → kAraka_karma, **overrides 1.4.54** → कृष्णं स्वर्गमगमयत्, वेदमध्यापयद्विधिम्; गत्यादि-किम् negative (ṇyanta non-gati verb पाचयति → stays kartṛ) |
| 541 | 1.4.53 | हृक्रोरन्यतरस्याम् | kāraka saṁjñā (K1, karma-only): ṇyanta hṛ/kṛ kartṛ — semantic_svatantra + rp [and ?Ryanta ?hfkf] → kAraka_karma, **overrides 1.4.54** → कारयति भृत्यं कटम्. The anyatarasyām tṛtīyā branch needs pre-pass optional-forking — **deferred to K3** (Skipped row) |
| 542 | 1.4.46 | अधिशीङ्स्थासां कर्म | kāraka saṁjñā (K1): ādhāra of adhi-pūrva śī/sthā/ās → karma — semantic_aDikaraRa + rp ?aDiSIN → kAraka_karma → अध्यास्ते वैकुण्ठं हरिः (locus dvitīyā, abhihita kartṛ prathamā). See SK544 TODO |
| 543 | 1.4.47 | अभिनिविशश्च | kāraka saṁjñā (K1): ādhāra of abhi-ni-viś → karma — semantic_aDikaraRa + rp ?aBiniviS → kAraka_karma → अभिनिविशते सन्मार्गम्. See SK544 TODO |
| 544 | 1.4.48 | उपान्वध्याङ्वसः | kāraka saṁjñā (K1): ādhāra of upa/anu/adhi/āṅ-pūrva vas → karma — semantic_aDikaraRa + rp ?upAdivas → kAraka_karma → उपवसति वैकुण्ठं हरिः. **TODO (post-tiṅanta):** SK542–544 currently match a hardcoded class tag (?aDiSIN / ?aBiniviS / ?upAdivas) baked onto the pre-formed verb pada; once tiṅanta derivation exists, these rules must instead **scan the verb's upasarga prefix(es)** — adhi (śī/sthā/ās), abhi-ni (viś), upa/anu/adhi/āṅ (vas) — to set that condition |
| 545 | 2.3.4 | अन्तरान्तरेण युक्ते | vibhakti (K1): noun adjacent (llp/rrp peek) to antarā/antareṇa → viBakti_2, **overrides 2.3.46** → अन्तरेण हरिम्, अन्तरा कृष्णम्; adjacency negative (non-adjacent noun → prathamā) |
| 546 | 1.4.83 | कर्मप्रवचनीयाः | Adhikāra — engine semantics: governs the karmapravacanīya saṁjñā set (1.4.84–96). No YAML rule |
| 547 | 1.4.84 | अनुर्लक्षणे | karmapravacanīya saṁjñā (K2, Pass A): =anu + semantic_lakzaRa → +karmapravacanIya +kp_dvitIyA (governs dvitīyā). Direction (kp_pUrva/kp_para) is a separate user input → जपमनु प्रावर्षत् (pūrva) |
| 548 | 2.3.8 | कर्मप्रवचनीययुक्ते द्वितीया | vibhakti (K2): noun governed by a kp_dvitIyA karmapravacanīya → viBakti_2, **overrides 2.3.46**. **Direction-keyed on the user's tag**: rrp ?karmapravacanIya ?kp_dvitIyA ?kp_pUrva (noun before particle) OR llp …?kp_para (noun after) → the user picks either reading (कृष्णम् अनु रामः vs कृष्णः अनु रामम्) |
| 549 | 1.4.85 | तृतीयार्थे | karmapravacanīya saṁjñā (K2): =anu + semantic_tftIyArTa → +kp_dvitIyA → नदीमन्ववसिता सेना (pūrva) |
| 550 | 1.4.86 | हीने | karmapravacanīya saṁjñā (K2): =anu + semantic_hIna → +kp_dvitIyA → अनु हरिं सुराः (para, user choice) |
| 551 | 1.4.87 | उपोऽधिके च | karmapravacanīya saṁjñā (K2): =upa + semantic_hIna → +kp_dvitIyA → उप हरिं सुराः (para). The adhika→saptamī arm (2.3.9) is K7 |
| 552 | 1.4.90 | लक्षणेत्थंभूताख्यानभागवीप्सासु प्रतिपर्यनवः | karmapravacanīya saṁjñā (K2): =prati/=pari + semantic_lakzaRa/itTamBUta → +kp_dvitIyA → वृक्षं प्रति, विष्णुं प्रति (pūrva). anu's senses are 1.4.84–86 (sidesteps the 1.4.84/90 overlap); bhāga/vīpsā senses deferred |
| 553 | 1.4.91 | अभिरभागे | karmapravacanīya saṁjñā (K2): =aBi + semantic_lakzaRa/itTamBUta (not bhāga) → +kp_dvitIyA → हरिमभि वर्तते (pūrva). vīpsā देवं देवमभि deferred |
| 554 | 1.4.93 | अधिपरी अनर्थकौ | **Deferred** (Skipped table) — **no vibhakti effect**: the karmapravacanīya saṁjñā here only blocks the gati/upasarga saṁjñā (कुतोऽध्यागच्छति), which matters for **accent/nighāta** alone, not for any sup choice; nothing to test until accent is modelled |
| 555 | 1.4.94 | सुः पूजायाम् | karmapravacanīya saṁjñā (K2, saṁjñā-only, no direction tag): =su + semantic_pUjA → +karmapravacanIya → सुसिक्तम् (no governed noun, so no 2.3.8 dvitīyā) |
| 556 | 1.4.95 | अतिरतिक्रमणे च | karmapravacanīya saṁjñā (K2): =ati + semantic_atikramaRa/pUjA → +kp_dvitIyA → अति देवान् कृष्णः (para; devān dvitīyā; non-adjacent kṛṣṇa → prathamā) |
| 557 | 1.4.96 | अपिः पदार्थसंभावनान्ववसर्गगर्हासमुच्चयेषु | karmapravacanīya saṁjñā (K2, saṁjñā-only): =api + semantic_saMBAvanA → +karmapravacanIya (no direction tag → 2.3.8 does not fire; द्वितीया तु नेह प्रवर्तते) → सर्पिषोऽपि (sarpis ṣaṣṭhī via 2.3.50). padArTa/anvavasarga/garhā/samuccaya senses deferred |
| 558 | 2.3.5 | कालाध्वनोरत्यन्तसंयोगे | vibhakti (K2): semantic_kAlADvan + semantic_atyantasaMyoga → viBakti_2, **overrides 2.3.46** → मासं कल्याणी, क्रोशं गिरिः; negative (अत्यन्तसंयोगे किम्) मासस्य द्विरधीते → ṣaṣṭhī (semantic_Seza, no atyantasaMyoga) |
| 559 | 1.4.54 | स्वतन्त्रः कर्ता | kāraka saṁjñā (pre-pass): semantic_svatantra → kAraka_kartA |
| 560 | 1.4.42 | साधकतमं करणम् | kāraka saṁjñā (pre-pass): semantic_sADakatama → kAraka_karaRa; 1.4.49 beats it by the param carve-out when a noun carries both |
| 561 | 2.3.18 | कर्तृकरणयोस्तृतीया | vibhakti (pre-pass): anabhihita kartṛ (rp ?!kartari) or karaṇa → viBakti_3 → रामेण सेव्यते, बाणेन |
| 562 | 1.4.43 | दिवः कर्म च | kāraka saṁjñā (K3, **vibhāṣā — pre-pass fork**): √div's sādhakatama (rp ?div) → kAraka_karma `optional: true`; apply branch → 2.3.2 dvitīyā (अक्षान्), skip branch → 1.4.42 karaṇa → 2.3.18 tṛtīyā (अक्षैः). Beats 1.4.42 by the param carve-out when it fires |
| 563 | 2.3.6 | अपवर्गे तृतीया | vibhakti (K3): semantic_kAlADvan + atyantasaMyoga + **semantic_apavarga** → viBakti_3, **overrides 2.3.46**, beats 2.3.5 dvitīyā by para → क्रोशेन (अनुवाकोऽधीतः); अपवर्गे किम् → क्रोशम् (2.3.5) |
| 564 | 2.3.19 | सहयुक्तेऽप्रधाने | vibhakti (K3): semantic_apraDAna + a saha-family particle (=saha/=sAkam/=sArDam/=samam) adjacent via llp/rrp peek → viBakti_3, **overrides 2.3.46** → पुत्रेण सह (पिता) |
| 565 | 2.3.20 | येनाङ्गविकारः | vibhakti (K3): semantic_aNgavikAra → viBakti_3, **overrides 2.3.46** → अक्ष्णा काणः; aṅgavikāraḥ kim → अक्षि (prathamā) |
| 566 | 2.3.21 | इत्थंभूतलक्षणे | vibhakti (K3): semantic_itTamBUtalakzaRa (distinct from K2's karmapravacanīya semantic_itTamBUta) → viBakti_3, **overrides 2.3.46** → जटाभिस्तापसः |
| 567 | 2.3.22 | संज्ञोऽन्यतरस्यां कर्मणि | vibhakti (K3, **vibhāṣā — pre-pass fork**): kAraka_karma of sam-√jñā (rp ?saMjYAna) → viBakti_3 `optional: true`, else fall-through to 2.3.2 dvitīyā → पित्रा / पितरं वा संजानीते; negative (non-saṁjñā verb भजति → plain dvitīyā, no तृतीया alternativ  **TODO (post-tiṅanta):**saMjYAna tag must be set on the fly  |
| 568 | 2.3.23 | हेतौ | vibhakti (K3): semantic_hetu → viBakti_3, **overrides 2.3.46** → धनेन कुलम्, पुण्येन दृष्टो हरिः |
| 569 | 1.4.32 | कर्मणा यमभिप्रैति स संप्रदानम् | kāraka saṁjñā (K4, general): semantic_aBipreta → kAraka_sampradAna → विप्राय गां ददाति |
| 570 | 2.3.13 | चतुर्थी संप्रदाने | vibhakti (K4): kAraka_sampradAna → viBakti_4 (no override — sampradāna noun has ?kAraka, so 2.3.46 arm-1 never fires) → हरये, देवदत्ताय, विप्राय |
| 571 | 1.4.33 | रुच्यर्थानां प्रीयमाणः | kāraka saṁjñā (K4): semantic_prIyamARa + rp ?rucyarTa → kAraka_sampradAna → हरये रोचते भक्तिः (bhakti = kartṛ → prathamā) |
| 572 | 1.4.34 | श्लाघह्नुङ्स्थाशपां ज्ञीप्स्यमानः | kāraka saṁjñā (K4): semantic_jYIpsyamAna + rp ?slAGAdi → kAraka_sampradAna |
| 573 | 1.4.35 | धारेरुत्तमर्णः | kāraka saṁjñā (K4): semantic_uttamarRa + rp ?DAri → kAraka_sampradAna → देवदत्ताय शतं धारयति (śata = karma → dvitīyā) |
| 574 | 1.4.36 | स्पृहेरीप्सितः | kāraka saṁjñā (K4): semantic_Ipsita_spfha + rp ?spfha → kAraka_sampradAna → पुष्पेभ्यः स्पृहयति |
| 575 | 1.4.37 | क्रुधद्रुहेर्ष्यासूयार्थानां यं प्रति कोपः | kāraka saṁjñā (K4, two arms): semantic_kopyamAna + rp ?kruDdruh / ?IrzyAsUya → kAraka_sampradAna → हरये क्रुध्यति. Beaten by 1.4.38 when the verb is upasṛṣṭa |
| 576 | 1.4.38 | क्रुधद्रुहोरुपसृष्टयोः कर्म | kāraka saṁjñā (K4, **param stress test**): semantic_kopyamAna + rp [and ?kruDdruh ?upasfzwa] → **kAraka_karma**, beats 1.4.37 by the kāraka-adhikāra param carve-out (14038 > 14037); ?!kAraka then keeps 1.4.37 off → अभिक्रुध्यति हरिम् (dvitīyā). upasfzwa = explicit tag on the pre-formed pada (post-tiṅanta TODO: scan the upasarga) |
| 577 | 1.4.39 | राधीक्ष्योर्यस्य विप्रश्नः | kāraka saṁjñā (K4): semantic_viprazwavya + rp ?rADIkz → kAraka_sampradAna → कृष्णाय राध्यति |
| 578 | 1.4.40 | प्रत्याङ्भ्यां श्रुवः पूर्वस्य कर्ता | kāraka saṁjñā (K4): semantic_pratiSrotf + rp ?pratiANSru → kAraka_sampradAna → देवदत्ताय प्रतिशृणोति |
| 579 | 1.4.41 | अनुप्रतिगृणश्च | kāraka saṁjñā (K4): semantic_pratiSrotf + rp ?anupratigF → kAraka_sampradAna → होत्रेऽनुगृणाति |
| 580 | 1.4.44 | परिक्रयणे संप्रदानमन्यतरस्याम् | kāraka saṁjñā (K4, **vibhāṣā — pre-pass fork**): semantic_parikrIta + rp ?parikrayaRa → kAraka_sampradAna `optional: true`; apply → 2.3.13 caturthī (शताय), skip → 1.4.42 karaṇa → 2.3.18 tṛtīyā (शतेन; noun also carries semantic_sADakatama). Beats 1.4.42 by param when it fires |
| 581 | 2.3.14 | क्रियार्थोपपदस्य च कर्मणि स्थानिनः | **Deferred (K4)** — Skipped table: needs kṛt/tumun-derived sthānin (karaka_plan.md §6) |
| 582 | 2.3.15 | तुमर्थाच्च भाववचनात् | **Deferred (K4)** — Skipped table: needs tum-artha bhāva-noun (karaka_plan.md §6) |
| 583 | 2.3.16 | नमःस्वस्तिस्वाहास्वधालंवषड्योगाच्च | vibhakti (K4): noun whose llp/rrp is a cluster word (=namas/=svasti/=svAhA/=svaDA/=alam/=vazaw) → viBakti_4, **overrides 2.3.46** → नमो देवेभ्यः (namas = neuter noun नमस् → its own prathamā नमः) |
| 584 | 2.3.17 | मन्यकर्मण्यनादरे विभाषाऽप्राणिषु | vibhakti (K4, **vibhāṣā — pre-pass fork**): kAraka_karma of man (rp ?manyarTa) + semantic_anAdara → viBakti_4 `optional: true`, else fall-through to 2.3.2 dvitīyā → तृणं / तृणाय मन्ये |
| 585 | 2.3.12 | गत्यर्थकर्मणि द्वितीयाचतुर्थ्यौ चेष्टायामनध्वनि | vibhakti (K4, **vibhāṣā — pre-pass fork**): kAraka_karma goal of a gatyartha verb (rp [and ?gatyarTa ?!Ryanta]) → viBakti_4 `optional: true`, else 2.3.2 dvitīyā → ग्रामं / ग्रामाय गच्छति. ?!Ryanta excludes the ṇyanta causative (स्वर्गम् in शत्रून् स्वर्गम् अगमयत् [SK540] stays plain dvitīyā); gatyartha-kim negative (भजति → no caturthī) |
| 586 | 1.4.24 | ध्रुवमपायेऽपादानम् | kāraka saṁjñā (K5, general): semantic_DruvApAya → kAraka_apAdAna (no verb gate) → ग्रामादायाति |
| 587 | 2.3.28 | अपादाने पञ्चमी | vibhakti (K5): kAraka_apAdAna → viBakti_5 (no override — apādāna noun has ?kAraka, so 2.3.46 arm-1 never fires) → ग्रामात्, चोराद्, उपाध्यायात् |
| 588 | 1.4.25 | भीत्रार्थानां भयहेतुः | kāraka saṁjñā (K5): semantic_Bayahetu + rp ?BItrA → kAraka_apAdAna → चोराद्बिभेति (SK उses चोराद्; Vasu वृकेभ्यो) |
| 589 | 1.4.26 | पराजेरसोढः | kāraka saṁjñā (K5): semantic_asoQa + rp ?parAji → kAraka_apAdAna → अध्ययनात्पराजयते; soḍha-kim negative शत्रून्पराजयते (abhibhava → karma → dvitīyā) |
| 590 | 1.4.27 | वारणार्थानामीप्सितः | kāraka saṁjñā (K5): semantic_Ipsita_vAraRa + rp ?vAraRArTa → kAraka_apAdAna → यवेभ्यो गां वारयति (go = karma) |
| 591 | 1.4.28 | अन्तर्धौ येनादर्शनमिच्छति | kāraka saṁjñā (K5): semantic_antardhi + rp ?antarDi → kAraka_apAdAna → मातुर्निलीयते कृष्णः |
| 592 | 1.4.29 | आख्यातोपयोगे | kāraka saṁjñā (K5): semantic_AKyAtf + rp ?upayoga → kAraka_apAdAna → उपाध्यायादधीते |
| 593 | 1.4.30 | जनिकर्तुः प्रकृतिः | kāraka saṁjñā (K5): semantic_janiprakfti + rp ?jani → kAraka_apAdAna → ग्रामात्प्रजायते (a-stem stand-in for ब्रह्मणः) |
| 594 | 1.4.31 | भुवः प्रभवः | kāraka saṁjñā (K5): semantic_praBava + rp ?praBava → kAraka_apAdAna → हिमवतो गङ्गा प्रभवति |
| 595 | 2.3.29 | अन्यारादितरर्तेदिक्शब्दाञ्चूत्तरपदाजाहियुक्ते | vibhakti (K5): noun whose llp/rrp is a yoga-word (=anya/=ArAt/=itara/=fte/=pUrva) → viBakti_5, **overrides 2.3.46** → अन्यो रामात् (ñc-uttarapada/āc/āhi-yukta yoga-words deferred) |
| 596 | 1.4.88 | अपपरी वर्जने | karmapravacanīya saṁjñā (K5, Pass A): =apa/=pari + semantic_varjana → karmapravacanIya + **kp_pancamI** (case marker, no direction; disjoint from kp_dvitIyA so 2.3.8 never fires). Direction is the user's kp_pUrva/kp_para → अप हरेः, परि हरेः (para) |
| 597 | 1.4.89 | आङ् मर्यादावचने | karmapravacanīya saṁjñā (K5, Pass A): =A + semantic_maryAdA → karmapravacanIya + kp_pancamI → आ मुक्तेः (para; āṅ surfaces आ) |
| 598 | 2.3.10 | पञ्चम्यपाङ्परिभिः | vibhakti (K5): noun adjacent to a karmapravacanIya + kp_pancamI → viBakti_5, **overrides 2.3.46**. Direction-keyed on the user's tag (rrp+kp_pUrva / llp+kp_para) → अप/परि/आ हरेः |
| 599 | 1.4.92 | प्रतिः प्रतिनिधिप्रतिदानयोः | karmapravacanīya saṁjñā (K5, Pass A): =prati + semantic_pratiniDi/semantic_pratidAna → karmapravacanIya + **kp_pancamI_pratinidhi** (its own marker → 2.3.11, distinct from the 2.3.10 apa/āṅ/pari scope) → कृष्णात्प्रति, तिलेभ्यः प्रति (pūrva) |
| 600 | 2.3.11 | प्रतिनिधिप्रतिदाने च यस्मात् | vibhakti (K5): noun adjacent to a karmapravacanIya + kp_pancamI_pratinidhi → viBakti_5, **overrides 2.3.46**. Direction-keyed on the user's tag; the marker keeps apa/āṅ/pari off this rule → हरेः प्रति |
| 601 | 2.3.24 | अकर्तर्यृणे पञ्चमी | vibhakti (K5): semantic_fRa (a non-agent hetu-debt, modelled by ?!kAraka — no kartṛ/karaṇa taken) → viBakti_5, **overrides 2.3.46** → शताद्बद्धः; akartari-kim शतेन बन्धितः (debt as karaṇa → 1.4.42 → 2.3.18 tṛtīyā) |
| 602 | 2.3.25 | विभाषा गुणेऽस्त्रियाम् | vibhakti (K5, **vibhāṣā — pre-pass fork**): semantic_guRahetu + ?!strI → viBakti_5 `optional: true`, **overrides 2.3.46 + 2.3.23**; skip branch → noun also carries semantic_hetu → 2.3.23 tṛtīyā → जाड्याज्जाड्येन वा. Yoga-vibhāga अगुणे/स्त्रियाम् deferred |
| 603 | 2.3.32 | पृथग्विनानानाभिस्तृतीयान्यतरस्याम् | vibhakti (K5, **three-way fork** via sub-sutra aps HIGH→LOW): noun whose llp/rrp is =pfTak/=vinA/=nAnA → {2.3.32.2 `optional` viBakti_3, 2.3.32.1 `optional` viBakti_5, 2.3.32 viBakti_2}, all **override 2.3.46** → पृथग् रामेण रामात् रामं वा |
| 604 | 2.3.33 | करणे च स्तोकाल्पकृच्छ्रकतिपयस्यासत्त्ववचनस्य | vibhakti (K5, **vibhāṣā — pre-pass fork**): semantic_stokAdi → viBakti_5 `optional: true`, **overrides 2.3.46**; skip branch → noun also carries semantic_sADakatama → 1.4.42 karaṇa → 2.3.18 tṛtīyā → स्तोकेन स्तोकाद्वा मुक्तः. dravye tu (स्तोकेन विषेण हतः) out of scope |
| 605 | 2.3.35 | दूरान्तिकार्थेभ्यो द्वितीया च | vibhakti (K5, **three-way fork** via sub-sutra aps HIGH→LOW): semantic_dUrAntika (दूर/अन्तिक decline as a-stem napuṃsaka pratipadikas) → {2.3.35.2 `optional` viBakti_2, 2.3.35.1 `optional` viBakti_5, 2.3.35 viBakti_3}, all **override 2.3.46** → दूरं दूरात् दूरेण वा; अन्तिकम् अन्तिकात् अन्तिकेन वा |
| 606 | 2.3.50 | षष्ठी शेषे | vibhakti (pre-pass, pulled forward from K6 as the śeṣa fallback): semantic_Seza, no kāraka → viBakti_6 → रामस्य पुत्रः |
| 607 | 2.3.26 | षष्ठी हेतुप्रयोगे | vibhakti (K6): yoga-word peek — hetu-word as physical neighbour (=hetoH/=hetunA via llp/rrp) → noun viBakti_6 → अन्नस्य हेतोः. Peek-words are passthrough avyaya |
| 608 | 2.3.27 | सर्वनाम्नस्तृतीया च | vibhakti (K6, **fork**): sarvanāman + hetu → tṛtīyā/ṣaṣṭhī → केन हेतुना / कस्य हेतोः |
| 609 | 2.3.30 | षष्ठ्यतसर्थप्रत्ययेन | vibhakti (K6): yoga-word peek =dakziRatas (atasartha pratyaya) → viBakti_6 → ग्रामस्य दक्षिणतः |
| 610 | 2.3.31 | एनपा द्वितीया | vibhakti (K6, **vibhāṣā — pre-pass fork**): =dakziRena (enap) neighbour → viBakti_2 `optional: true`, companion 2.3.31.1 supplies skip-branch viBakti_6 → दक्षिणेन ग्रामं / ग्रामस्य |
| 611 | 2.3.34 | दूरान्तिकार्थैः षष्ठ्यन्यतरस्याम् | vibhakti (K6, **vibhāṣā — pre-pass fork**): dūra/antika yoga-word → viBakti_6 `optional: true`, companion 2.3.34.1 supplies skip-branch viBakti_5 → दूरं ग्रामस्य / ग्रामात् |
| 612 | 2.3.51 | ज्ञोऽविदर्थस्य करणे | vibhakti (K6, verb-conditioned śeṣa): semantic_Seza + rp ?jYAvid → viBakti_6, **overrides 2.3.50** → सर्पिषो जानीते |
| 613 | 2.3.52 | अधीगर्थदयेशां कर्मणि | vibhakti (K6): semantic_Seza + rp ?aDIgartha → viBakti_6, **overrides 2.3.50** → मातुः स्मरति |
| 614 | 2.3.53 | कृञः प्रतियत्ने | vibhakti (K6): semantic_Seza + rp ?kfYpratiyatna → viBakti_6, **overrides 2.3.50** → एधोदकस्योपस्कुरुते |
| 615 | 2.3.54 | रुजार्थानां भाववचनानामज्वरेः | vibhakti (K6): semantic_Seza + rp ?rujArTa → viBakti_6, **overrides 2.3.50** → चौरस्य रुजति |
| 616 | 2.3.55 | आशिषि नाथः | vibhakti (K6): semantic_Seza + rp ?nATASis → viBakti_6, **overrides 2.3.50** → सर्पिषो नाथते |
| 617 | 2.3.56 | जासिनिप्रहणनाटक्राथपिषां हिंसायाम् | vibhakti (K6): semantic_Seza + rp ?hiMsArTa → viBakti_6, **overrides 2.3.50** → चौरस्योज्जासयति |
| 618 | 2.3.57 | व्यवहृपणोः समर्थयोः | vibhakti (K6): semantic_Seza + rp ?vyavahfpaR → viBakti_6, **overrides 2.3.50** → शतस्य व्यवहरति |
| 619 | 2.3.58 | दिवस्तदर्थस्य | vibhakti (K6): semantic_Seza + rp [and ?divtadarTa ?!upasfzwa] → viBakti_6, **overrides 2.3.50** → शतस्य दीव्यति |
| 620 | 2.3.59 | विभाषोपसर्गे | vibhakti (K6, **vibhāṣā — pre-pass fork**): upasṛṣṭa div (rp [and ?divtadarTa ?upasfzwa]) on a kAraka_karma → viBakti_6 `optional: true` (overrides 2.3.2), else 2.3.2 dvitīyā → शतस्य / शतं प्रतिदीव्यति |
| 621 | 2.3.61 | प्रेष्यब्रुवोर्हविषो देवतासंप्रदाने | vibhakti (K6): semantic_Seza + rp ?prezyabrU → viBakti_6, **overrides 2.3.50** → छागस्य प्रेष्यति |
| 622 | 2.3.64 | कृत्वोऽर्थप्रयोगे कालेऽधिकरणे | vibhakti (K6): yoga-word peek =paYcakftvas + a kāla śeṣa → viBakti_6 → पञ्चकृत्वोऽह्नः |
| 623 | 2.3.65 | कर्तृकर्मणोः कृति | vibhakti (K6, kṛd-yoga): governing kṛdanta noun carries `kft` (read via llp/rrp); the kāraka noun keeps its primitive but takes viBakti_6, **overrides 2.3.2 + 2.3.18** → ओदनस्य पाचकः, हरेः कृतिः. Guarded by ?!kft_aSazWI (2.3.69/70) |
| 625 | 2.3.67 | क्तस्य च वर्तमाने | vibhakti (K6, kṛd-yoga): governor carries kta_vartamAna → kartṛ-ṣaṣṭhī viBakti_6, **overrides 2.3.2 + 2.3.18** → राज्ञां मतः |
| 626 | 2.3.68 | अधिकरणवाचिनश्च | vibhakti (K6, kṛd-yoga): governor carries kta_aDikaraRa → viBakti_6, **overrides 2.3.2 + 2.3.18** → एतेषामासितम् |
| 627 | 2.3.69 | न लोकाव्ययनिष्ठाखलर्थतृनाम् | prohibition (K6, **guard-realized — no positive rule**): laṭ-ādeśa/avyaya/niṣṭhā/khalartha/tṛn governors carry kft_aSazWI → karman blocked from 2.3.65 → 2.3.2 dvitīyā → दैत्यान् घातुको हरिः |
| 628 | 2.3.70 | अकेनोर्भविष्यदाधमर्ण्ययोः | prohibition (K6, **guard-realized**): future-aka / ādhamarṇya-in governors carry kft_aSazWI → 2.3.2 dvitīyā → व्रजं गामी |
| 629 | 2.3.71 | कृत्यानां कर्तरि वा | vibhakti (K6, kṛd-yoga **vibhāṣā fork**): governor carries kftya → kartṛ viBakti_6 `optional: true`, else 2.3.18 tṛtīyā → मम/मे सेव्यः / मया सेव्यः |
| 632 | 1.4.45 | आधारोऽधिकरणम् | kāraka saṁjñā (K7): semantic_ADAra → kAraka_aDikaraRa → कटे आस्ते, स्थाल्यां पचति, मोक्षे इच्छास्ति |
| 633 | 2.3.36 | सप्तम्यधिकरणे च | vibhakti (K7): kAraka_aDikaraRa → viBakti_7, **overrides 2.3.46** → कटे आस्ते. The च-arm (dūra/antika) is split into optional 2.3.36.1 joining the 2.3.35 four-way fork → दूरे |
| 634 | 2.3.37 | यस्य च भावेन भावलक्षणम् | vibhakti (K7, sati-saptamī): noun whose adjacent llp/rrp partner is also semantic_BAvalakzaRa → viBakti_7, **overrides 2.3.46** → गोषु दुह्यमानासु गतः |
| 635 | 2.3.38 | षष्ठी चानादरे | vibhakti (K7, **vibhāṣā fork**): semantic_anAdara → viBakti_7 `optional: true` (overrides 2.3.50), skip → 2.3.50 ṣaṣṭhī → रुदति/रुदतो वा प्राव्राजीत् |
| 636 | 2.3.39 | स्वामीश्वराधिपतिदायादसाक्षिप्रतिभूप्रसूतैश्च | vibhakti (K7, **vibhāṣā fork**): svāmi-yoga word via llp/rrp → viBakti_7 `optional: true` else 2.3.50 ṣaṣṭhī → गवां/गोषु वा स्वामी |
| 637 | 2.3.40 | आयुक्तकुशलाभ्यां चासेवायाम् | vibhakti (K7, **vibhāṣā fork**): semantic_AsevA + āyukta/kuśala yoga-word → viBakti_7 `optional: true` else 2.3.50 → पूजने/पूजनस्य वा कुशलः |
| 638 | 2.3.41 | यतश्च निर्धारणम् | vibhakti (K7, **vibhāṣā fork**): semantic_nirDAraRa → viBakti_7 `optional: true` else 2.3.50 → नृणां/नृषु वा ब्राह्मणः श्रेष्ठः |
| 639 | 2.3.42 | पञ्चमी विभक्ते | vibhakti (K7): semantic_viBakta separation → viBakti_5 → माथुराः पाटलिपुत्रकेभ्यः |
| 640 | 2.3.43 | साधुनिपुणाभ्यामर्चायां सप्तम्यप्रतेः | vibhakti (K7): semantic_arcA + a sādhu/nipuṇa yoga-word via llp/rrp → viBakti_7 → मातरि साधुः |
| 641 | 2.3.44 | प्रसितोत्सुकाभ्यां तृतीया च | vibhakti (K7, **vibhāṣā fork**): semantic_prasitotsuka → viBakti_3 `optional: true` else 7 (overrides 2.3.36) → हरिणा/हरौ वा |
| 642 | 2.3.45 | नक्षत्रे च लुपि | vibhakti (K7, **vibhāṣā fork**): semantic_nakzatralup → viBakti_3 `optional: true` else 7 → मूलेन/मूले. taddhita-lup itself deferred (modelled on the plain stem मूल) |
| 643 | 2.3.7 | सप्तमीपञ्चम्यौ कारकमध्ये | vibhakti (K7, **vibhāṣā fork**): semantic_kArakamaDya (kāla/adhvan between two śaktis) → viBakti_5 `optional: true` else 7 → द्व्यहे/द्व्यहात्, क्रोशे/क्रोशात् |
| 644 | 1.4.97 | अधिरीश्वरे | karmapravacanīya saṁjñā (K7): adhi in the īśvara/sva-svāmi sense → karmapravacanIya + kp_saptamI; direction (kp_pUrva/kp_para) is the user's choice; rp ?!kfYi (before √kṛ the optional 1.4.98 governs) → अधि भुवि रामः / अधि रामे भूः (para) |
| 645 | 2.3.9 | यस्मादधिकं यस्य चेश्वरवचनम् | vibhakti (K7): noun adjacent to a karmapravacanIya + kp_saptamI (direction-keyed on the user's tag like 2.3.8) → viBakti_7, **overrides 2.3.8 and 2.3.46** (a saptamī kp has no kp_dvitIyA, so 2.3.8 no longer matches it → the prathamā override must be direct) → अधि भुवि; उप परार्धे (the 1.4.87.1 upa-adhika arm). Broader aiśvarya pakṣa deferred |
| 646 | 1.4.98 | विभाषा कृञि | saṁjñā (K7, **vibhāṣā fork**): adhi before √kṛ optionally karmapravacanīya else gati → यदत्र मामधिकरिष्यति. Surface (tiṅanta for adhi-√kṛ) deferred — saṁjñā fork only |
| 647 | 2.1.1 | समर्थः पदविधिः | Avyayībhāva (S0): samartha adhikāra — engine semantics (the samāsa pre-pass operates on the syntactically-related members); no rule block |
| 648 | 2.1.3 | प्राक्कडारात्समासः | Avyayībhāva (S0): samāsa-saṁjñā adhikāra; realized as the `?samAsa`/`?samAsaPurva` member tagging in the pre-pass |
| 649 | 2.1.4 | सह सुपा | Avyayībhāva (S0): a compound combines padas WITH their sups — satisfied by running the samāsa pre-pass after kāraka sup-insertion |
| 650 | 2.4.71 | सुपो धातुप्रातिपदिकयोः | Avyayībhāva (S0): main-scan luk of the pūrva member's internal sup (?samAsaPurva) → शाकप्रति/अक्षपरि (noun-pūrva) |
| 651 | 2.1.5 | अव्ययीभावः | Avyayībhāva (S1A): the samāsa-type saṁjñā; fused with 2.1.6 in the pre-pass (sets ?avyayIBAva on the uttara) |
| 652 | 2.1.6 | अव्ययं विभक्तिसमीप… | Avyayībhāva (S1A): the core vidhi — avyaya (समीप/विभक्ति/अत्यय/यौगपद्य senses) + noun → pūrva ?samAsaPurva, uttara ?samAsa+?avyayIBAva → उपकृष्णम्, अधिहरि, अतिहिमम् |
| 653 | 1.2.43 | प्रथमानिर्दिष्टं समास उपसर्जनम् | Avyayībhāva (S0): the prathamā-nirdiṣṭa member → ?upasarjana (pre-pass) |
| 655 | 1.2.44 | एकविभक्ति चापूर्वनिपाते | Avyayībhāva (S0): eka-vibhakti recorded in the pre-pass (avyaya is invariant — no further anya-vibhakti machinery needed) |
| 657 | 2.4.83 | नाव्ययीभावादतोऽम् त्वपञ्चम्याः | Avyayībhāva (S1A): a-stem avyayībhāva's last-member sup → अम् (overrides 2.4.82) → उपकृष्णम्. The **त्वपञ्चम्याः sub-rule 2.4.83.1** carves out the pañcamī (drops ?avyaya so the real ablative surfaces → उपकृष्णात्). Full vibhakti sweep tested: उपकृष्णम् in all but the ablative उपकृष्णात्, with the optional 2.4.84 उपकृष्णेन/उपकृष्णे |
| 658 | 2.4.84 | तृतीयासप्तम्योर्बहुलम् | Avyayībhāva (S3): bahula अम् for tṛtīyā/saptamī — optional fork dropping ?avyaya so the case ending surfaces → उपकृष्णम्/उपकृष्णे |
| 659 | 2.4.18 | अव्ययीभावश्च | Avyayībhāva (S1B; S4 → `bahiranga: -1`): the compound is napuṁsaka (?napum on the uttara). Moved into the samāsa pre-pass (condition rp ?avyayIBAva) so the uttara enters the main scan already napuṁsaka |
| 660 | 6.3.81 | अव्ययीभावे चाकाले | Avyayībhāva (S3): सहस्य सः — saha → sa in an avyayībhāva, ?!kAla guard → सचक्रम् |
| 661 | 2.1.7 | यथाऽसादृश्ये | Avyayībhāva (S1B): yathā (yogyatā/anativṛtti senses) + noun → यथाशक्ति |
| 662 | 2.1.8 | यावदवधारणे | Avyayībhāva (S1B): yāvat (avadhāraṇa) + noun → यावज्जीवम् (t→j junction sandhi) |
| 663 | 2.1.9 | सुप्प्रतिना मात्रार्थे | Avyayībhāva (S1B): noun (mātrā sense) + प्रति → शाकप्रति (NOUN-pūrva; uses 2.4.71) |
| 664 | 2.1.10 | अक्षशलाकासंख्याः परिणा | Avyayībhāva (S1B): akṣa/śalākā/saṁkhyā + परि → अक्षपरि (NOUN-pūrva) |
| 666 | 2.1.12 | अपपरिबहिरञ्चवः पञ्चम्या | Avyayībhāva (S2, vibhāṣā; S4 **kāraka-driven pañcamī**): apa/pari/bahis + a noun the kāraka layer put in pañcamī (apa + semantic_varjana → 1.4.88 → 2.3.10 → ?viBakti_5), which 2.1.12 checks on rp and CONSUMES (swap → prathamā via ?swap_viBakti + `_swap_sups`) so the compound declines as am → अपग्रामम् |
| 667 | 2.1.13 | आङ्मर्यादाभिविध्योः | Avyayībhāva (S2, vibhāṣā; S4): āṅ (maryādā/abhividhi) + a pañcamī noun (A + semantic_maryAdā → 1.4.89 → 2.3.10 → ?viBakti_5), consumed via ?swap_viBakti exactly as 2.1.12 → आसमुद्रम् |
| 668 | 2.1.14 | लक्षणेनाभिप्रती आभिमुख्ये | Avyayībhāva (S2, vibhāṣā): abhi/prati (ābhimukhya) + noun → प्रत्यग्नि |
| 669 | 2.1.15 | अनुर्यत्समया | Avyayībhāva (S2, vibhāṣā): anu (samayā) + noun → अनुवनम् |
| 670 | 2.1.16 | यस्य चायामः | Avyayībhāva (S2, vibhāṣā): anu (āyāma) + noun → अनुगङ्गम् (ā-stem → 2.4.18 napum → 1.2.47 hrasva → अम्) |
| 673 | 2.1.19 | संख्या वंश्येन | Avyayībhāva (S2, vibhāṣā): a saṁkhyā + vaṁśya noun → द्विमुनि |
| 674 | 2.1.20 | नदीभिश्च | Avyayībhāva (S2, vibhāṣā): a saṁkhyā + river-name → द्विगङ्गम् |
| 677 | 5.4.107 | अव्ययीभावे शरत्प्रभृतिभ्यः | Avyayībhāva (S3/S4, **rule-driven**): pre-pass rule sets ?samasanta_TaC on a śarat-prabhṛti uttara; the generic `_insert_samasanta` step inserts the TaC (wac) → उपशरदम्. The **full śaradādi gaṇa** is tagged ?SaratpraBfti in pratipadika.py (śarad, vipāś, anas, manas, div, diś, dṛś, viś, cetas, catur, tyad, tad, yad, kiyat, upānah, himavat, anaḍuh); s-/ś-stems derive cleanly (उपमनसम्, उपदिशम्) |
| 678 | 5.4.108 | अनश्च | Avyayībhāva (S4): a **non-napuṁsaka** (`?!napum`) an-final uttara → ?samasanta_TaC → TaC; with 6.4.144 (न-lopa) → उपराजम् (upa + rājan). Cedes napuṁsaka an-stems to 5.4.109 |
| 679 | 6.4.144 | नस्तद्धिते | S4: the ṭi (final vowel + न्) of a नकारान्त aṅga drops before a taddhita (overrides 6.4.134's an-ablaut) → rājan → rāj, + TaC अ → rāja → उपराजम्. Scoped by **?Ba (bha-saṁjñā)** — 6.4.144 is in the भस्य adhikāra, so it fires only before a य/अच्-initial affix (1.4.18); general (any नकारान्त bha) but correctly EXCLUDES yuvan+ति (SK531: ति consonant-initial → not bha → न् drops by 8.2.7 → युवती). Plus a 6.4.22 ābhīya **asiddhavat** edge (`_ASIDDHA_PEERS`: 6.4.144→6.4.148) so 6.4.144 does not see 6.4.148's a-lopa transient `van` (from a-stem vana, which IS bha before wac) → उपवनम् |
| 789 | 6.4.145 | अह्नष्टखोरेव | Niyama restricting 6.4.144 for **ahan**: the ṭi-lopa applies ONLY before a ट/ख-it taddhita, so for any other taddhita (rp neither `?wa` nor `?Ka`) 6.4.145 **overrides** (suppresses) 6.4.144, keeping the न् → 6.4.134 अल्लोपोऽनः runs instead (ahan → ahn) → dvi+ahan+wac → द्व्यह्न (not द्व्यह). Pure niyama-blocker (`xform: null`); added because the generalized `?Ba` 6.4.144 newly reached ahan+wac (dvyahna regression). **Tested** via the `dvyahna` vibhakti paradigm in `test/vibhaktis_list.py` (द्व्यह्ने/द्व्यह्नि/द्व्यहनि) |
| 680 | 5.4.109 | नपुंसकादन्यतरस्याम् | Avyayībhāva (S4): a **natively napuṁsaka** uttara → TaC **optional** (`optional: true`) → the samāsa pre-pass FORKS: उपचर्मम् (TaC) / उपचर्म (no TaC) (upa + carman). Reads native ?napum — clean because 2.4.18 defers to ?samasa_napum (committed to ?napum at end-of-sweep by `_commit_samasa_napum`). First genuine two-output vibhāṣā in samāsa; needed new fork support in `_samasa_window_fixpoint` |
| 681 | 5.4.110 | नदीपौर्णमास्याग्रहायणीभ्यः | Avyayībhāva (S4): a nadī (ī-fem, ?NI) uttara → ?samasanta_TaC → TaC → उपनदम् |
| 682 | 5.4.111 | झयः | Avyayībhāva (S4): a jhay-final (?jhayanta) uttara → ?samasanta_TaC → TaC → उपसमिधम् |
| 683 | 5.4.112 | गिरेश्च सेनकस्य | Avyayībhāva (S4, Senaka's view): giri uttara → ?samasanta_TaC → TaC → उपगिरम् |
| 684 | 2.1.22 | तत्पुरुषः | Tatpuruṣa (**T0**): the tatpuruṣa-saṁjñā adhikāra — fused into the 2.1.24 vidhi (sets ?tatpuruza on the uttara), as 2.1.5 was fused into 2.1.6. Unlike the avyayībhāva, the compound declines normally in the uttara's gender (no ?avyaya/?napum) |
| 686 | 2.1.24 | द्वितीया श्रितातीतपतितगतात्यस्तप्राप्तापन्नैः | Tatpuruṣa (**T0**, `bahiranga: -1`): a dvitīyā noun (?viBakti_2 + ?samAsa_vivakza) + a śrita-gaṇa uttara (?srita_gaRa) → pūrva ?samAsaPurva, uttara ?samAsa + ?tatpuruza → कृष्णश्रितः. Pūrva sup luks via 2.4.71 (no swap — the pūrva does not surface); uttara sup retained → declines as a-stem masc (full vibhakti sweep). 1.2.43 (upasarjana) reused |
| 687 | 2.1.25 | स्वयं क्तेन | Tatpuruṣa (**T0**): the indeclinable स्वयम् + a ?kta word → स्वयंकृतम् / स्वयङ्कृतम् (svayam avyaya-pūrva, no dvitīyā — SK687 द्वितीया न संबद्ध्यते; 8.3.23 म्→anusvāra + 8.4.58 optional parasavarṇa at the junction). Needs a semantic sense on the pūrva (as kāraka/CLI input has) to keep it ?pada |
| 688 | 2.1.26 | खट्वा क्षेपे | Tatpuruṣa (**T0**): खट्वा (dvitīyā) + a ?kta word, in निन्दा (?semantic_kzepa) → खट्वारूढः. Nitya in the kṣepa sense |
| 689 | 2.1.27 | सामि | Tatpuruṣa (**T0**): the indeclinable सामि + a ?kta word → सामिकृतम् (like 2.1.25; i-final, no anusvāra issue) |
| 690 | 2.1.28 | कालाः | Tatpuruṣa (**T0**): a time-word (?kAlavAcaka) in the dvitīyā + a ?kta word → मासप्रमितः (optional → ?samAsa_vivakza gate; restricted to non-atyantasaṃyoga) |
| 691 | 2.1.29 | अत्यन्तसंयोगे च | Tatpuruṣa (**T0**): a time-word (?kAlavAcaka) in the dvitīyā + ANY word (अक्तान्तार्थम्), in अत्यन्तसंयोग (?semantic_atyantasaMyoga) → मुहूर्तसुखम् |
| 812 | 2.4.26 | परवल्लिङ्गं द्वन्द्वतत्पुरुषयोः | Tatpuruṣa (**T0**, saṁjñā, `bahiranga: -1`): the compound takes the uttara's gender. Already realized by `join_objects` (merge prefers the last member's liṅga, `paninian_object.py` ~L154), so this is a documenting ?paravalliNga marker that the T-liṅga exceptions (2.4.19/29/30/31) will override |
| 692 | 2.1.30 | तृतीया तत्कृतार्थेन गुणवचनेन | Tatpuruṣa (**T1**, `bahiranga: -1`): a tṛtīyā noun (?viBakti_3 + ?samAsa_vivakza) + a guṇavacana (?guRavacana) uttara → tṛtīyā-tatpuruṣa. Same T0 shape (pūrva ?samAsaPurva, uttara ?samAsa +?tatpuruza; 2.4.71 luk, 2.4.26 gender) |
| 693 | 2.1.31 | पूर्वसदृशसमोनार्थकलहनिपुणमिश्रश्लक्ष्णैः | Tatpuruṣa (**T1**): a tṛtīyā noun + a पूर्व/सदृश/सम/… uttara (?pUrvasadfSa_gaRa) → मासपूर्वः |
| 694 | 2.1.32 | कर्तृकरणे कृता बहुलम् | Tatpuruṣa (**T1**): a tṛtīyā (kartṛ/karaṇa) + a ?kta uttara → अहिहतः (bahulam modelled non-optionally, gated on vivakṣā). 2.1.33–35 (kṛtya/anna/bhakṣya) deferred — Skipped table |
| 698 | 2.1.36 | चतुर्थी तदर्थार्थबलिहितसुखरक्षितैः | Tatpuruṣa (**T1**): a caturthī noun (?viBakti_4) + a तदर्थ/अर्थ/बलि/हित/सुख/रक्षित uttara (?tadarTa_gaRa) → धान्यार्थः, यूपदारु |
| 699 | 2.1.37 | पञ्चमी भयेन | Tatpuruṣa (**T1**): a pañcamī noun (?viBakti_5) + भय (?Baya_gaRa) → चोरभयम् (napuṁsaka; 2.4.26 → uttara भय napuṁsaka) |
| 700 | 2.1.38 | अपेतापोढमुक्तपतितापत्रस्तैरल्पशः | Tatpuruṣa (**T1**): a pañcamī noun + अपेत/अपोढ/मुक्त/पतित/अपत्रस्त (?apeta_gaRa) → स्वर्गपतितः |
| 701 | 2.1.39 | स्तोकान्तिकदूरार्थकृच्छ्राणि क्तेन | Tatpuruṣa (**T1**): a स्तोक/अन्तिक/दूर/कृच्छ्र-class pañcamī pūrva (?stoka_gaRa) + a ?kta uttara → स्तोकमुक्तः. NOTE: the classical **aluk** form स्तोकान्मुक्तः (pañcamī retained via 6.3.2 पञ्चम्याः स्तोकादिभ्यः) is deferred — this rule luks the pūrva sup like the others (Skipped table) |
| 702 | 2.2.8 | षष्ठी | Tatpuruṣa (**T1**, the canonical case): a ṣaṣṭhī noun (?viBakti_6 + ?samAsa_vivakza) + any noun → **राजपुरुषः**. Most general vibhakti-tatpuruṣa (any uttara). The an-stem pūrva राजन् takes 8.2.7 न-lopa → राज (needs the 2.4.71 ?Ba-clear fix). 2.2.9–11 exceptions deferred — Skipped table |
| 695 | 2.2.1 | पूर्वापराधरोत्तरमेकदेशिनैकाधिकरणे | Tatpuruṣa (**T1**): a diś-word (पूर्व/अपर/…, ?dikSabda) pūrva + an ekadeśin uttara (?ekadeSin) → पूर्वकायः. No viBakti gate (the part-word is prathamā-nirdiṣṭa). 2.2.2–5 deferred — Skipped table |
| 717 | 2.1.40 | सप्तमी शौण्डैः | Tatpuruṣa (**T1**): a saptamī noun (?viBakti_7) + a शौण्ड-gaṇa uttara (?SORqa_gaRa) → अक्षशौण्डः |
| 718 | 2.1.41 | सिद्धशुष्कपक्वबन्धैश्च | Tatpuruṣa (**T1**): a saptamī noun + सिद्ध/शुष्क/पक्व/बन्ध (?siDDa_gaRa) → सांकाश्यसिद्धः. 2.1.42–48 deferred — Skipped table |
| 736 | 2.1.57 | विशेषणं विशेष्येण बहुलम् | Tatpuruṣa (**T2** karmadhāraya, `bahiranga: -1`): a viśeṣaṇa (?viSezaRa) pūrva + a same-case noun (samānādhikaraṇa; pūrva ?viBakti_1) → नीलोत्पलम् (napuṁsaka), कृष्णसर्पः (masc). Sets +samAnADikaraRa so 1.2.42 names it karmadhāraya. Same declining-uttara shape (2.4.71 luk, 2.4.26 gender) |
| 726 | 2.1.49 | पूर्वकालैकसर्वजरत्पुराणनवकेवलाः समानाधिकरणेन | Tatpuruṣa (**T2** karmadhāraya): a pūrvakāla (?pUrvakAla) [or eka/sarva/…] pūrva + a same-case noun → स्नातानुलिप्तः. Same samānādhikaraṇa shape as 2.1.57 (eka/sarva/jarat/purāṇa/nava/kevala senses deferred — Skipped) |
| 745 | 1.2.42 | तत्पुरुषः समानाधिकरणः कर्मधारयः | Tatpuruṣa (**T2**, saṁjñā, `bahiranga: -1`): a samānādhikaraṇa tatpuruṣa (marked +samAnADikaraRa by 2.1.57/2.1.49) is named ?karmaDAraya (a ?tatpuruza sub-tag; still declines paravalliṅga via 2.4.26). Fires only on genuinely same-case compounds, NOT the ekadeśī पूर्वकायः (viBakti_1 pūrva but not samānādhikaraṇa) |
| 746 | 6.3.42 | पुंवत्कर्मधारयजातीयदेशीयेषु | Tatpuruṣa (**T2**, saṁjñā, `bahiranga: -1`): puṃvadbhāva — a feminine viśeṣaṇa pūrva of a karmadhāraya takes its masculine form (कल्याणी → कल्याण → कल्याणप्रियः). Modelled as the puṃvadbhāva saṁjñā on a ?puMvat pūrva; the composer supplies the masc form कल्याण directly (the full ṅīp-stripping derivation कल्याणी→कल्याण is deferred — Skipped) |
| 751 | 2.2.38 | कडाराः कर्मधारये | Tatpuruṣa (**T2**, saṁjñā, `bahiranga: -1`, optional): the kaḍāra-gaṇa (?kaqAra) words are optionally the pūrva of a karmadhāraya. Modelled as a ?kaqAra_pUrva saṁjñā tag; the optional physical reordering (2.2.30 pūrva-nipāta) stays deferred, so only the input-order compound surfaces |
| 685 | 2.1.23 | द्विगुश्च | Tatpuruṣa (**T2** dvigu saṁjñā): **fused into 2.1.52** (as 2.1.22 was fused into 2.1.24) — the द्विगु saṁjñā adhikāra is realized by 2.1.52 setting ?dvigu. No separate rule |
| 728 | 2.1.51 | तद्धितार्थोत्तरपदसमाहारे च | Tatpuruṣa (**T2** dvigu vidhi): the समाहार (aggregate) arm is **fused into 2.1.52** — the समाहार sense (?samAhAra) drives 2.4.1 → पञ्चगवम्/त्रिलोकम् (tested). The taddhitārtha / uttarapada arms (a saṅkhyā-pūrva before a taddhita, e.g. पाञ्चलोहितिकम्) need the taddhita machinery — deferred (Skipped) |
| 727 | 2.1.50 | दिक्संख्ये संज्ञायाम् | Tatpuruṣa (**T2** dvigu, **partial**): the saṅkhyā-pūrva saṁjñā arm overlaps 2.1.52; the dik-śabda saṁjñā arm (पूर्वेषुकामशमी etc.) needs saṁjñā-domain dik-pūrva tagging — deferred (Skipped) |
| 730 | 2.1.52 | संख्यापूर्वो द्विगुः | Tatpuruṣa (**T2** dvigu, `bahiranga: -1`): a saṅkhyā-pūrva (?saMKyA) tatpuruṣa is a DVIGU (fused vidhi + saṁjñā, subsuming 2.1.23 saṁjñā + 2.1.51 समाहार-vidhi). Forms पञ्च+गो, त्रि+लोक, त्रि+भुवन and sets ?dvigu; the tag rides to the merged stem (join_objects Tier-3) so the existing 4.1.21 (SK479) ṅīp fires on a **real dvigu** (त्रिलोकी), replacing the in_compound shim. Excludes the vaṁśya/nadī senses (2.1.19/2.1.20 avyayībhāva apavādas → द्विमुनि, द्विगङ्गम्) |
| 731 | 2.4.1 | द्विगुरेकवचनम् | Tatpuruṣa (**T2** dvigu, saṁjñā, `bahiranga: -1`): a समाहार (aggregate, ?samAhAra) dvigu is napuṁsaka ekavacana → पञ्चगवम्, त्रिलोकम् (nom=acc अम्). Reuses the deferred-napuṁsaka marker ?samasa_napum (→ ?napum via `_commit_samasa_napum`, which now also locks the gender against the wac samāsānta — see engine note). त्रिभुवनम् deferred (cross-member ṇatva, see Skipped) |
| 729 | 5.4.92 | गोरतद्धितलुकि | Tatpuruṣa (**T2** dvigu samāsānta, `bahiranga: -1`): a go-final dvigu/tatpuruṣa (no taddhita-luk) takes the ṬaC samāsānta (पञ्च+गो → पञ्चगो+अ → पञ्चगव, o→av before अ). Rule-driven via the proven ?samasanta_TaC + `_insert_samasanta` path (as avyayībhāva 5.4.107–112) |
| — | (engine) | (join_objects gender lock) | Tatpuruṣa (**T2** engine fix): `_commit_samasa_napum` now sets ?samasa_liNga_locked alongside ?napum; `join_objects` honours it so a samāsānta wac (which hard-codes ?pum for 2.4.29 rātrāhnāhāḥ puṃsi → द्व्यह्नः) does NOT override a samāhāra-dvigu's napuṁsaka at the (uttara \| wac) merge — पञ्चगवम् stays napuṁsaka, not पञ्चगवः. dvyahna (native ahan, no samasa_napum) is unaffected |
| 756 | 2.2.6 | नञ् | Tatpuruṣa (**T3** nañ, saṁjñā, `bahiranga: -1`): the नञ् (न, matched by `=na`) + a noun forms a tatpuruṣa — pūrva +samAsaPurva +naY, uttara +samAsa +tatpuruza. Reuses 1.2.43 (upasarjana) + 2.4.26 (paravalliṅga), so the compound declines normally in the uttara's gender → अब्राह्मणः, अनश्वः. The नञ् has no vigraha vibhakti. The `naY` avyaya (avyaya.py) surface corrected नञ्→न (ञ् is इत्) |
| 757 | 6.3.73 | नलोपो नञः | Tatpuruṣa (**T3** nañ, `bahiranga: -1`): the न of नञ् is elided before a CONSONANT → अ: न+ब्राह्मण → अब्राह्मणः. An xform rule in the samāsa pre-pass member-window (same (pūrva\|uttara) window 2.2.6 fires in — the uttara stem's first char is `r`, the un-lukked pūrva sup skipped; window fixpoint runs 2.2.6 first, then this). xform lc→"" (drops the न्). Doing the नलोप before the main scan means "a"\|ब्राह्मण never meets vowel sandhi |
| 758 | 6.3.74 | तस्मान्नुडचि | Tatpuruṣa (**T3** nañ, `bahiranga: -1`): before a VOWEL, नलोप + नुṭ (न्) augment → अ + नश्व: न+अश्व → अनश्वः, न+अज → अनजः. One xform (same pre-pass window as 6.3.73): pūrva "na"→"a" (lc→"") AND the नुṭ न् prepended to the UTTARA (r → न+r, अश्व→नश्व). नुṭ is टकित् (1.1.46 आद्यन्तौ टकितौ → front of the अच्/uttara); keeping it on the uttara (not an "an"-final pūrva) is essential — an "an"-final pūrva is hit by 8.2.7 नलोपः प्रातिपदिकान्तस्य (→ आश्वः). No 6.1.101 override needed (the नलोप precedes the main scan) |
| 761 | 2.2.18 | कुगतिप्रादयः | Tatpuruṣa (**T4** prādi/gati, saṁjñā, `bahiranga: -1`): a कु/गति/प्रादि particle (?ku \| ?gati \| ?prAdi) as pūrva + any subanta → tatpuruṣa: प्र+आचार्य → प्राचार्यः, कु+पुरुष → कुपुरुषः, अति+माल → अतिमालः. **NITYA-samāsa** (aswapada-vigraha) — NO ?samAsa_vivakza gate (unlike the vibhāṣā tatpuruṣas): fires on the semantic-sense window trigger like the nitya avyayībhāvas (2.1.6); ?nitya marks the class → प्राचार्यः forms with no vivakza. The particle is ?nipAta → avyaya (1.1.37), so its sup luks; no vigraha vibhakti. Reuses 1.2.43 + 2.4.26 → declines masc a-stem. Membership: ?prAdi (pra/ati), ?ku (ku), ?gati (assigned by the real gati saṁjñā 1.4.61/67/68). upapada (2.2.19/3.1.92) deferred — Skipped table |
| 762 | 1.4.61 | ऊर्यादिच्विडाचश्च | Gati saṁjñā (**T4**, `domain: saMjYA`, `bahiranga: -1`): an ऊर्यादि word (?UryAdi — ऊरी…) gets the गति saṁjñā → ?gati in the samāsa pre-pass window, feeding the gati arm of 2.2.18 → ऊरी+कृत = ऊरीकृतम्. A REAL rule (ऊरी is NOT intrinsically ?gati), replacing the earlier intrinsic-tag stand-in. cvi (X→Xī) / ḍāc denominal derivations deferred — Skipped table |
| 768 | 1.4.67 | पुरोऽव्ययम् | Gati saṁjñā (**T4**, `domain: saMjYA`, `bahiranga: 0`): the avyaya पुरस् gets ?gati. Now the REAL source of puras's gati (its intrinsic ?gati was removed) — a main-scan saṁjñā so the ?gati is present for the sandhi 8.3.40 नमस्पुरसोर्गत्योः (पुरस्कृतम्, H→s) on the non-pre-pass path |
| 769 | 1.4.68 | अस्तं च | Gati saṁjñā (**T4**, `domain: saMjYA`, `bahiranga: -1`): अस्तम् gets ?gati (=astam → +gati) in the pre-pass window, feeding the gati arm of 2.2.18 (अस्तम् is NOT intrinsically ?gati) |
| 787 | 5.4.87 | अहस्सर्वैकदेशसंख्यातपुण्याच्च रात्रेः | Tatpuruṣa (**T5** samāsānta, `bahiranga: -1`): a रात्रि-final tatpuruṣa after {अहन्/सर्व/एकदेश/संख्या/**पुण्य**} takes the समासान्त → रात्र: पुण्य+रात्रि → पुण्यरात्रः. Rule-driven via ?samasanta_TaC + `_insert_samasanta`; रात्रि is i-final so रात्रि+wac → रात्र (इ-lopa 6.4.148, as giri→उपगिरम्). With 2.4.29 (masc) declines as the राम a-stem (full vibhakti sweep). द्विरात्रः (संख्या pūrva → समाहार dvigu gender) deferred — Skipped table |
| 788 | 5.4.91 | राजाहःसखिभ्यष्टच् | Tatpuruṣa (**T5** samāsānta, `bahiranga: -1`): a rājan-final tatpuruṣa (?tatpuruza + ?rAjan) takes the टच् (ṬaC) → an a-stem: परम+राजन् → परमराज+अ → परमराजः (न-lopa 6.4.144, exactly as the avyayībhāva उपराजम्). Rule-driven via ?samasanta_TaC + `_insert_samasanta` (the proven avyayībhāva 5.4.107–112 path). Disjoint from 5.4.108 (?avyayIBAva). ahar/sakhi arms deferred — Skipped table |
| 807 | 6.3.46 | आन्महतः समानाधिकरणजातीययोः | Tatpuruṣa (**T5** samāsānta, `bahiranga: -1`): a महत् pūrva → महा (आत्) before a samānādhikaraṇa uttara: महत्+राजन् → महा+राजन् → (5.4.91 टच्) → महाराजः. A pūrva-substitution in the samāsa pre-pass member-window (like the nañ 6.3.73/74 and 6.3.81 saha→sa): lp `=mahat` + ?samAsaPurva, rp ?samAsa + ?samAnADikaraRa (the tag 2.1.57 sets on the UTTARA — gating rp pins the genuine karmadhāraya); xform wipes the pūrva to महा |
| 814 | 2.4.29 | रात्राह्नाहाः पुंसि | Tatpuruṣa (**T-liṅga** gender exception, saṁjñā, `bahiranga: -1`): a रात्र/अह्न/अह-final (?rAtri \| ?ahan) tatpuruṣa is MASCULINE, overriding the uttara's native gender (रात्रि f., अहन् n.) and 2.4.26. Pre-pass override: set +pum, drop the native ?strI/?napum, lock (?samasa_liNga_locked, which `join_objects` honours). Gated ?!samAhAra + ?!samasa_napum so it does not clobber a समाहार dvigu (napum by 2.4.1, द्व्यहम्/द्विरात्रम्). The **रात्रि arm has a full surface — पुण्यरात्रः** (5.4.87 → रात्र, then masc; full vibhakti sweep). The ahan-arm द्व्यहः a-stem surface still awaits the ahar टच् (5.4.91 ahar-arm). 2.4.19/30/31 deferred — Skipped table |
| 829/830 | 2.2.23, 2.2.24 | शेषो बहुव्रीहिः / अनेकमन्यपदार्थे | Bahuvrīhi (**B0**, `bahiranga: -1`): the EXOCENTRIC compound — two prathamānta words denoting an EXTERNAL referent (anyapadārtha). Gated `?bahuvrIhi_vivakza` (bahuvrīhi has no lexical/uttara-class discriminator — any two words). pūrva → `?samAsaPurva` (+`?upasarjana` via 1.2.43), uttara → `?samAsa` + `?bahuvrIhi`. The pūrva sup luks (2.4.71); the uttara sup (the referent's external case) is retained and declines. **Referent gender (fused, the one new mechanism)**: the compound declines in the EXTERNAL referent's gender, NOT the uttara's (contrast 2.4.26 परवल्लिङ्गम्) — the composer sets `?referent_pum/strI/napum` on the uttara (overriding its native gender), the rule pins it with `?samasa_liNga_locked` (the flag `join_objects` honours). पीत+अम्बर (n.) → पीताम्बरः / पीताम्बरा / पीताम्बरम् (gender sweep proves exocentricity) + a full masc vibhakti sweep; the fem ā-stem takes ṭāp via `strI_abs`. See `bahuvrihi_plan.md` |
| 831 | 6.3.34 | स्त्रियाः पुंवद्भाषितपुंस्कादनूङ्समानाधिकरणे स्त्रियामपूरणीप्रियादिषु | Bahuvrīhi (**B1** puṁvadbhāva, saṁjñā, `bahiranga: -1`): a bhāṣitapuṁska non-ūṅ FEMININE pūrva (`?puMvat`) before a feminine uttara (`?uttara_strI`) of a bahuvrīhi takes its MASCULINE form → दीर्घे जङ्घे यस्याः = दीर्घजङ्घा (दीर्घा→दीर्घ). Saṁjñā-marker model (like SK746/6.3.42): the composer supplies the masc form + `?puMvat`, the rule fires as `?puMvadBAva`; the real ṅīp/ṭāp-strip is deferred. The uttara's vigraha femininity is carried by `?uttara_strI` (its native `?strI` is overridden to the referent liṅga by B0). Excludes पूरणी/प्रियादि (6.3.38 + `?!priyAdi`); the other prohibitions (6.3.37/40/41) override it. **`?!pUraRI` guard added (2026-07-21):** the sūtra's own **अपूरणी** — no puṁvadbhāva when the uttara is an ORDINAL (कल्याणी पञ्चमी यासाम् = कल्याणीपञ्चमाः, कल्याणी stays fem), needed for SK832/5.4.116. Previously 6.3.34 wrongly fired here (surface was right only because its update is a marker, not a substitution) |
| 838/839/841/842 | 6.3.37, 6.3.38, 6.3.40, 6.3.41 | न कोपधायाः / संज्ञापूरण्योश्च / स्वाङ्गाच्चेतः / जातेश्च | Bahuvrīhi (**B1** puṁvadbhāva prohibitions, saṁjñā, `bahiranga: -1`, each `overrides: 6.3.34`): a feminine pūrva does NOT take the masc when it is 6.3.37 k-penult (`?kopaDa`, पाचिकाभार्यः), 6.3.38 a name/ordinal (`?saMjYA`/`?pUraRI`, दत्ताभार्यः), 6.3.40 a svāṅga ī-stem (`?svAnga_I`, सुकेशीभार्यः), or 6.3.41 a jāti (`?jAti`, ब्राह्मणीभार्यः). Each fires `?puMvadBAva_niziDDa` and blocks 6.3.34 so the fem form stays |
| 848 | 2.2.28 | तेन सहेति तुल्ययोगे | Bahuvrīhi (**B2** formation, `bahiranga: -1`): सह (with) + a noun in tulyayoga → bahuvrīhi (पुत्रेण सह = सपुत्रः/सहपुत्रः). सह is an indeclinable pūrva (no `?viBakti_1`, so the generic 2.2.24 does not fire); this rule tags the saha pūrva `?bahuvrIhi_saha` so 6.3.82 (not the avyayībhāva 6.3.81) handles saha→sa. Referent gender locked like B0 |
| 849 | 6.3.82 | वोपसर्जनस्य | Bahuvrīhi (**B2**, main-scan `bahiranga: 1`, `optional`): the upasarjana सह OPTIONALLY → स in a bahuvrīhi → सपुत्रः / सहपुत्रः (forks). Mirrors the avyayībhāva 6.3.81 (`lc=""`, `l="sa"`) but keyed on `?bahuvrIhi_saha` + guarded `?!ASis`; 6.3.81 gets a `?!bahuvrIhi_saha` guard so the two never overlap. Needs the saha sup present (fires before 2.4.71 luks it) |
| 850 | 6.3.83 | प्रकृत्याशिषि | Bahuvrīhi (**B2**, saṁjñā `bahiranga: -1`): in a benediction (`?ASis`) सह retains its form (prakṛtibhāva) → स्वस्ति राज्ञे सहपुत्राय. Fires `?prakftiBAva` and pairs with 6.3.82's `?!ASis` guard so only सहपुत्राय surfaces. The अगोवत्सहलेषु (go/vatsa/hala) exception deferred |
| 845 | 2.2.26 | दिङ्नामान्यन्तराले | Bahuvrīhi (**B2** formation, `bahiranga: -1`): direction-NAMES (`?dikSabda`), in the intermediate-direction sense, form a bahuvrīhi → दक्षिणपूर्वा (SE; fem diś referent, ā-stem via `strI_abs`). Gated on both members `?dikSabda`; fires before the generic 2.2.24 (higher _aps → para) |
| 891 | 5.4.154 | शेषाद्विभाषा | Bahuvrīhi (**B3** samāsānta कप्, `bahiranga: -1`): a residual (śeṣa) bahuvrīhi takes कप् when the speaker intends it — the विभाषा is modelled as a **VIVAKṢĀ** (`?kap_vivakzA` on the uttara, NOT an engine fork): बहुयशस्कम् WITH the tag, बहुयशः WITHOUT. Generalized samāsānta: sets `?samasanta_kap`, `_insert_samasanta` (`_SAMASANTA_AFFIXES` map) inserts `kap`. 5.4.155 overrides it |
| 889 | 5.4.151 | उरःप्रभृतिभ्यः कप् | Bahuvrīhi (**B3** samāsānta कप्, `bahiranga: -1`): an उरःप्रभृति-gaṇa stem (`?uras_praBfti`: उरस्/सर्पिस्/पयस्/लक्ष्मी) final in a bahuvrīhi takes कप् (nitya) → व्यूढोरस्कः, प्रियसर्पिष्कः, बहुपयस्कः, बहुलक्ष्मीकः. Sets `?samasanta_kap` |
| 833 | 5.4.153 | नद्यृतश्च | Bahuvrīhi (**B3** samāsānta कप्, `bahiranga: -1`): a bahuvrīhi whose uttara is a नदी-word (`?NI`) or ऋ-final takes कप् → बहुकुमारीकः, बहुनदीकः, बहुमातृकः, **बहुपितृकः**. **ऋतः arm WIDENED (2026-07-20)** from the `?svasrAdi` proxy to a true ṛ-final test (`$$is_ftanta`): स्वस्रादि is the FEMININE ṛ-kinship gaṇa, so masc ṛ-stems were silently missed — बहु+पितृ gave बहुपिता, no कप् (verified). ऋतः in the sūtra is unrestricted, and SK895/5.4.157 वन्दिते भ्रातुः presupposes भ्रातृ being in scope (its counterexample मूर्खभ्रातृकः IS a कप् form). A `$$` helper is needed because in a member window `r:` matches the uttara's FIRST char (cf. 6.3.73 `r: _hal`), not its last. Latent narrowness remaining: the नदी arm keys on the ṅīp/ṅīṣ AFFIX (`?NI`), not the नदी saṁjñā of 1.4.3, so an ī-final fem whose ī is not a strī-pratyaya (तन्त्री) is out of scope. SK834/7.4.13 + SK835/7.4.14 net to no change for कप्, so the ई/ऋ is retained without them |
| 853 | 5.4.114 | अङ्गुलेर्दारुणि | Bahuvrīhi (**B3** samāsānta षच्, `bahiranga: -1`): an अङ्गुलि-final bahuvrīhi in the दारु (wood) sense (`?dAru`) → षच् → पञ्चाङ्गुलम् (i-lopa 6.4.148; n.). Sets `?samasanta_Sac` |
| 893 | 5.4.155 | न संज्ञायाम् | Bahuvrīhi (**B3** samāsānta कप्, `bahiranga: -1`, `overrides: 5.4.154`): a bahuvrīhi that is a NAME (`?saMjYA`) takes NO कप् → बहुयशः (kap blocked, only the no-kap form). Fires the no-op `?samasanta_niziDDa` |
| 852/854 | 5.4.113, 5.4.115 | सक्थ्यक्ष्णोः स्वाङ्गात्षच् / द्वित्रिभ्यां ष मूर्ध्नः | Bahuvrīhi (**B3** samāsānta षच्, `bahiranga: -1`): a svāṅga सक्थि/अक्षि → षच् (दीर्घसक्थः; i-lopa 6.4.148), and द्वि/त्रि + मूर्धन् → ष (द्विमूर्धः; न-lopa 6.4.144). Sets `?samasanta_Sac` (→ `Sac` in `_SAMASANTA_AFFIXES`). A saṅkhyā pūrva carries NO vacana (`?nityadvivacana` vs forced vacana_1 → द्व). **Two guards added (2026-07-21):** (a) `?svAnga` — the sūtra's own **स्वाङ्गात्**, previously unmodelled though the comment claimed it; criterial and sense-based (स्वाङ्गात् किम् — दीर्घसक्थि शकटम्, स्थूलाक्षा वेणुयष्टिः), so composer-supplied like 5.4.159's नाडी. (b) an explicit **नञ्/दुस्/सु exclusion**, because SK861/5.4.121 is their apavāda and `overrides:` cannot reach across a vibhāṣā fork — 5.4.113 is nitya and fires in an earlier fixpoint iteration than the optional rule, so असक्थिः could not otherwise form. सक्थि in असक्थः IS a svāṅga, so the clash is real |
| 855 | 5.4.117 | अन्तर्बहिर्भ्यां च लोम्नः | Bahuvrīhi (**B3** samāsānta अप्, `bahiranga: -1`): अन्तर्/बहिस् + लोमन् → अप् → बहिर्लोमः (न-lopa 6.4.144; र्ल doubling optional). Sets `?samasanta_ap` |
| 832 | 5.4.116 | अप्पूरणीप्रमाण्योः | Bahuvrīhi (**B3** samāsānta अप्, `bahiranga: -1`): अप् after a uttara that is a feminine ORDINAL (`?pUraRI`: पञ्चमी) or प्रमाणी → **स्त्रीप्रमाणः**, **कल्याणीपञ्चमाः**. Sets `?samasanta_ap` (the `ap_s` affix, shared with 5.4.117); the uttara's ई drops before अप् by 6.4.148, then the referent gender governs (fem रात्रि → ṭāp → पञ्चमा). `overrides: 5.4.153` — a पूरणी/प्रमाणी is `?NI`, so 5.4.153 (कप्) would otherwise also grab it. **Also fixed 6.3.34** — see its row — to honour the sūtra's own **अपूरणी** (no puṁvadbhāva before an ordinal). NOT modelled: the वार्तिक प्रधानपूरण्यामेव (अप् only when the ordinal is pradhāna) |
| 867 | 5.4.128 | द्विदण्ड्यादिभ्यश्च | Bahuvrīhi (**B3** samāsānta इच्, `bahiranga: -1`): a dvidaṇḍi-ādi bahuvrīhi (weapon) → इच् → द्विदण्डि (a-lopa 6.4.148). Sets `?samasanta_ic` |
| 868/869 | 5.4.129, 5.4.130 | प्रसंभ्यां जानुनोर्ज्ञुः / ऊर्ध्वाद्विभाषा | Bahuvrīhi (**B4** samāsānta ādeśa, `bahiranga: -1`): प्र/सम् + जानु → ज्ञु → प्रज्ञुः (u-stem), and ऊर्ध्व + जानु → OPTIONALLY ज्ञु → ऊर्ध्वज्ञुः / ऊर्ध्वजानुः (5.4.130 vibhāṣā). Pre-pass uttara-substitution (`rc→""`, `r→"jYu"`), mirroring the tatpuruṣa 6.3.46 महत्→महा |
| 870 | 5.4.132 | धनुषश्च | Bahuvrīhi (**B4** samāsānta अनङ्, `bahiranga: -1`): a धनुस्-final bahuvrīhi → धन्वन् (n-stem) → nom sg सुधन्वा (शार्ङ्गधन्वा). Uttara-substitution धनुस्→धन्वन् |
| 871 | 5.4.133 | वा संज्ञायाम् | Bahuvrīhi (**B4** samāsānta अनङ्, `bahiranga: -1`, `optional: true`): in a **saṁjñā** the अनङ् of 5.4.132 is OPTIONAL → **शतधन्वा / शतधनुः** | The vibhāṣā fork comes free from the pre-pass (`antaranga_prakriya._run_fixpoint` clones the un-applied branch). 5.4.132 carries the matching `?!saMjYA` so exactly one of the pair is live per compound; दृढधन्वा (no `?saMjYA`) is the non-saṁjñā control, asserted `not_fired` on 5.4.133 |
| 860/861 | 5.4.120, 5.4.121 | सुप्रातसुश्व…प्रोष्ठपदाः / नञ्दुःसुभ्यो हलिसक्थ्योरन्यतरस्याम् | Bahuvrīhi (**B3** अच्, `bahiranga: -1`): new `ac_s` affix + `?samasanta_ac`. 5.4.120 is a nipātana LIST → **चतुरश्रः** (अश्रि+अच्, i-lopa by 6.4.148 exactly as षच् on सक्थि); 5.4.121 is OPTIONAL अच् after नञ्/दुस्/सु on हलि/सक्थि → **असक्थः / असक्थिः** | 5.4.120: only the अश्रि/कुक्षि members are modelled — the पाद members (एणीपद/अजपद/प्रोष्ठपद) need 5.4.139's पाद→पद substitute, and प्रातर्/श्वस्/दिव are heterogeneous consonant-final nipātanas. 5.4.121 required an explicit नञ्/दुस्/सु **exclusion in 5.4.113** (see its row): `overrides:` cannot reach across a vibhāṣā fork |
| 864/865 | 5.4.125, 5.4.126 | जम्भा सुहरिततृणसोमेभ्यः / दक्षिणेर्मा लुब्धयोगे | Bahuvrīhi (**B4** nipātana, `bahiranga: -1`): both are stated कृतसमासान्त (samāsānta already applied), modelled as an-stem substitutions (the सुधन्वा/5.4.132 shape) → **सुजम्भा**, **दक्षिणेर्मा** | 5.4.125 is gated on the सु/हरित/तृण/सोम list (स्वादिभ्यः किम् — पतितजम्भः keeps जम्भ). 5.4.126's `?lubDayoga` is a composer sense tag (व्याधेन कृतव्रणः); its ए is ordinary guṇa sandhi, not part of the nipātana |
| 877/878 | 5.4.138, 5.4.139 | पादस्य लोपोऽहस्त्यादिभ्यः / कुम्भपदीषु च | Bahuvrīhi (**B4** pāda-lopa, `bahiranga: -1`): after an **उपमान** (not हस्त्यादि) पाद loses its final → **व्याघ्रपात्/व्याघ्रपाद्**; हस्तिपादः is the अहस्त्यादिभ्यः counter. 5.4.139 nipātanas **both** the lopa AND the ṅīp in the feminine → **कुम्भपदी**; masc **कुम्भपादः** is the स्त्रियाम् counter | 5.4.139's substitute is **पद्** (short a, "पादः पत्"), not पाद् as in 5.4.138/140; it sets `+NI` for the nipātita ṅīp (so the su drops) and therefore needs `overrides: 5.4.153`, else the fresh `?NI` would pull in नद्यृतश्च's कप् (*कुम्भपदीकः). Reuses 5.4.137's `?upamAna` tag |
| 881/882/883 | 5.4.143, 5.4.144, 5.4.145 | स्त्रियां संज्ञायाम् / विभाषा श्यावारोकाभ्याम् / अग्रान्तशुद्धशुभ्रवृषवराहेभ्यश्च | Bahuvrīhi (**B4** दतृ, `bahiranga: -1`): all three reuse SK880/5.4.141's ऋ-**it** mechanism (`orp: [++f]` → उगित् → 7.1.70 नुम्). 5.4.143 is nitya in a fem saṁjñā → **फालदती** (the ī free from 4.1.6, as for सुदती); 5.4.144/145 are vibhāṣā → **श्यावदन्/श्यावदन्तः**, **वृषदन्/वृषदन्तः** | 5.4.145's **अग्रान्त arm is unexercised** (needs an अग्र-final pūrva; कुड्मलाग्रदन्). अयस् as a pūrva hits a separate ru→u visarga-sandhi gap (*अयर्दती), so फाल is used for 5.4.143 |
| 885/886/887 | 5.4.147, 5.4.148, 5.4.149 | त्रिककुत्पर्वते / उद्विभ्यां काकुदस्य / पूर्णाद्विभाषा | Bahuvrīhi (**B4** kakud/kākud-lopa, `bahiranga: -1`): **त्रिककुत्** (त्रि+ककुद as a MOUNTAIN name, `?parvata` sense tag), **उत्काकुत्**, **पूर्णकाकुत्/पूर्णकाकुदः** (vibhāṣā) | **काकुद "palate" (तालु) is a DIFFERENT word from ककुद "hump"** (5.4.146/147) — separate stems. 5.4.147 `overrides: 5.4.146` purely for attribution (both would give the same string); the पर्वत restriction is what it carries (त्रिककुदोऽन्यः) |
| 890 | 5.4.152 | इनः स्त्रियाम् | Bahuvrīhi (**B3** minor कप्, `bahiranga: -1`): NITYA कप् after an इन् uttara when the referent is FEMININE → **बहुदण्डिका** | Reuses B0's `?referent_strI` — स्त्रियाम् is exactly the anyapadārtha referent gender. For a masc referent there is no nitya कप् (**बहुदण्डी** राजा, Vasu 54152), only 5.4.154's vivakṣā. दण्डिन् is registered directly with `?in_anta` — no मतुप्/इनि matvarthīya machinery exists yet; 6.4.144 नस्तद्धिते drops the न् before कप्, then ṭāp |
| 892 | 7.4.15 | आपोऽन्यतरस्याम् | Bahuvrīhi (**B3** minor कप्, main scan, `optional: true`): an आबन्त uttara OPTIONALLY shortens before कप् → **बहुमालाकः / बहुमालकः** | The ONLY member of the 7.4.13–15 trio with a surface effect. 7.4.13 केऽणः / 7.4.14 न कपि are a **net no-op for कप्** and are NOT implemented: 7.4.13 is absent, and 1.2.48 (which Vasu says 7.4.14 also blocks) is gated on `?pum_abs` so it cannot reach the कप् path either. Verified: बहु+पाचिका under vivakṣā gives बहुपाचिकाकः, ā intact. **If 1.2.48's `?pum_abs` FIXME is ever widened, 7.4.14 becomes load-bearing and must be added** |
| 894 | 5.4.156 | ईयसश्च | Bahuvrīhi (**B3** minor कप्, `bahiranga: -1`): कप् blocked after an ईयसुन् uttara → **बहुश्रेयान्** | `overrides: [5.4.153, 5.4.154]` per the sūtra ("debars all the previous rules"), but only the **5.4.154 arm is reachable** — verified load-bearing (without it, ?kap_vivakzA gives *बहुश्रेयस्कः). The 5.4.153 arm would cover fem बहुश्रेयसी, but श्रेयसी's ṅīp comes from 4.1.6 in the MAIN SCAN, so at the pre-pass window the uttara is bare श्रेयस् with no `?NI` and 5.4.153 never fires — बहुश्रेयसी is already correct without this rule. Listed for correctness if the pre-pass ever learns derived ṅīp |
| 895 | 5.4.157 | वन्दिते भ्रातुः | Bahuvrīhi (**B3** minor कप्, `bahiranga: -1`): कप् blocked for a भ्रातृ uttara in the वन्दित ("praised") sense → **सुभ्राता**; outside it **मूर्खभ्रातृकः** | `?vandita` is a composer sense tag (like `?vayas`, `?saMKyeya`). **Required widening 5.4.153's ऋतः arm** — see its row: with the old `?svasrAdi` proxy भ्रातृ never took कप् and this prohibition had nothing to block |
| 896 | 5.4.159 | नाडीतन्त्र्योः स्वाङ्गे | Bahuvrīhi (**B3** minor कप्, `bahiranga: -1`): कप् blocked for नाडी/तन्त्री in the BODY-PART sense; outside it कप् applies → **बहुनाडीकः** स्तम्भः | `?svAnga` is composer-supplied (SK contrasts both senses for the SAME word), so it is NOT baked into the stems. **नाडी arm is load-bearing** (?NI → 5.4.153 → blocked); the **तन्त्री arm is vacuous** — तन्त्री lacks `?NI` so it was never in 5.4.153's scope (5.4.153 keys on the ṅīp/ṅīṣ affix, not the नदी saṁjñā of 1.4.3 — a latent narrowness). **बहुनाडिः's short इ is NOT asserted**: it is 1.2.48 upasarjana shortening, unreachable behind `?pum_abs`. बहुतन्त्रीः keeps its long ī correctly (unādi ī, not a strī-pratyaya) |
| 897 | 5.4.160 | निष्प्रवाणिश्च | Bahuvrīhi (**B3** minor कप्, `bahiranga: -1`): nipātana — कप् blocked AND प्रवाणी→प्रवाणि → **निष्प्रवाणिः** पटः | Strictly only the कबभाव is nipātita; the ī→i is 1.2.48 upasarjana shortening, folded into the nipātana here because 1.2.48 is unreachable (same root gap as 5.4.159's बहुनाडिः, which has no nipātana to hide behind and so is left unasserted). `-NI, -strI` tag-clear after the class-changing substitution (cf. 5.4.134). निष् is ordinary sandhi |
| 874/875/876 | 5.4.135, 5.4.136, 5.4.137 | गन्धस्येदुत्पूतिसुसुरभिभ्यः / अल्पाख्यायाम् / उपमानाच्च | Bahuvrīhi (**B4** samāsānta ādeśa, `bahiranga: -1`): गन्ध's final अ → इ (uttara-substitution गन्ध→गन्धि). Three licences: **5.4.135** the pūrva ∈ {उत्/पूति/सु/सुरभि} → सुगन्धिः, सुरभिगन्धिः; **5.4.136** the sense अल्प (`?alpa` composer tag) → सूपगन्धि, घृतगन्धि; **5.4.137** an उपमान pūrva (`?upamAna` tag, cf. करभोरूः) → पद्मगन्धिः. **5.4.135 NARROWED (2026-07-21)** from matching ANY `=gandha` pūrva to its own list — the old rule wrongly gave *घृतगन्धि / *तीव्रगन्धि (Vasu's "why after these only?") and grabbed the 5.4.136/137 cases, making them unreachable; the list gate is what lets them fire (घृत+गन्ध with no `?alpa` now keeps गन्ध → घृतगन्धम्). Fixed the `gandha` stem's canonical "gandha"→"ganDa" (proper SLP1, ध=D) — invisible until the un-substituted form became reachable. NOT modelled: the एकान्तग्रहण vārtika (गन्ध must be the QUALITY not the substance — सुगन्धि पुष्पम् vs सुगन्ध आपणिकः); we always take the quality reading |
| 879 | 5.4.140 | संख्यासुपूर्वस्य | Bahuvrīhi (**B4** samāsānta पाद-lopa, `bahiranga: -1`): a saṅkhyā/सु-pūrva bahuvrīhi ending in पाद → पाद् (consonant stem) → nom sg द्विपात् / द्विपाद् (8.4.56 वाऽवसाने). Uttara-substitution पाद→पाद् |
| 888 | 5.4.150 | सुहृद्दुर्हृदौ मित्रामित्रयोः | Bahuvrīhi (**B4** samāsānta nipātana, `bahiranga: -1`): सु/दुर् + हृदय → हृद् ('friend'/'foe') → सुहृत् / सुहृद् (8.4.56). Uttara-substitution हृदय→हृद् |
| 880 | 5.4.141 | वयसि दन्तस्य दतृ | Bahuvrīhi (**B4** samāsānta ādeśa, `bahiranga: -1`): after a saṅkhyā/सु pūrva, दन्त → दतृ in the AGE sense → **द्विदन्, सुदन्**. दतृ is दत् + an **ऋ-IT**: the rule substitutes the string AND sets `++f`, so the stem is उगित् and SK361/7.1.70 inserts नुम् (दत्→दन्त्), the nom sg su then dropping by 8.2.23 → द्विदन्. The feminine **सुदती** falls out free via 4.1.6 उगितश्च (ugit→ṅīp) — independent confirmation of the ऋ-it analysis. `?vayas` is criterial (वयसि किम् → द्विदन्तः करी) |
| 856/857 | 5.4.118, 8.4.3 | अञ् नासिकायाः संज्ञायां नसं चास्थूलात् / पूर्वपदात्संज्ञायामगः | Bahuvrīhi (**B3** अच् + **cross-compound ṇatva**): a नासिका-final SAṀJÑĀ bahuvrīhi → नस् (`-Ap` clear), and 8.4.3 ṇatva-ises the न across the pūrva/uttara boundary → **द्रुणसः**. The ṇatva is enabled the same way as SK307/8.4.12 — set `?samasta_Ratva` on the uttara → `?samasta_Ratva_pada` → arm B of 8.4.1/8.4.2 (arm A is blocked by `?merged_pada`). Gated on **`?saMjYA`** — the sūtra's OWN condition (संज्ञायाम्), which is also the right reason त्रिभुवनम् keeps its न: *it is not a name*. Validated by the pre-existing **शूर्पणखा / शूर्पनखी** minimal pair (identical members; only the `saMjYA` tag differs) — and Vasu cites शूर्पणखा under 8.4.3 itself, referring to 5.4.118 + 4.1.58. **अगः deliberately NOT modelled, following the Mahābhāṣya:** SK857 records "अग इति प्रत्याख्यातं भाष्ये" — ऋगयनम्'s lack of ṇatva already follows from the निपातन at 4.3.129 अण् ऋगयनादिभ्यः (SK1452), and ऋगयन is the only example either source cites. Modelling it would need a new lp+rp-spanning helper (the guard cannot go in the shared `ratva_string`, used by 8.4.1/8.4.2/8.4.22) for zero coverage. अस्थूलात् not modelled (no स्थूल stem) |
| 859 | 8.4.28 | उपसर्गाद्बहुलम् | Bahuvrīhi (**B3** cross-compound ṇatva, upasarga arm): after an upasarga the न of the 5.4.119 नस् → ण → **प्रणसः** (उन्नसः unaffected — उद् has no ṛ/ṣ/r). 5.4.119 marks the substitute `?nas_AdeSa`, which is propagated through the (uttara \| sup) merge (join_objects Tier-1 allowlist) so this rule can key on it; disjoint from 8.4.3's `?saMjYA_nas` |
| 862 | 5.4.122 | नित्यमसिच् प्रजामेधयोः | Bahuvrīhi (**B3** samāsānta असिच्, `bahiranga: -1`): after नञ्/दुस्/सु, a प्रजा/मेधा-final bahuvrīhi obligatorily takes असिच् (अस्) → **सुप्रजाः, सुमेधाः** (दुर्मेधाः too, with the optional र-sandhi forks). New `asic` Pratyaya + `_SAMASANTA_AFFIXES` entry; `-Ap, -strI` clear as in 5.4.134/5.4.119, and the nom sg masc अस्-dīrgha comes from the widened 6.4.14. अप्रजाः additionally needs the nañ-bahuvrīhi formation path |
| 872 | 5.4.134 | जायाया निङ् | Bahuvrīhi (**B4** samāsānta निङ्, `bahiranga: -1`): जाया final in a bahuvrīhi → जानि → युवतिर्जाया यस्य = **युवजानिः**. Uttara-substitution जाया→जानि PLUS `update: orp: [-Ap, -strI]` — जाया carries `?Ap`, which would otherwise drive ā-stem nom-sg su-elision and strip the visarga (जानि). This tag-clear is the general fix for any ādeśa out of a fem ā-stem |
| 858 | 5.4.119 | उपसर्गाच्च | Bahuvrīhi (**B3** samāsānta अच्, `bahiranga: -1`): उपसर्ग (प्र/उद्) + नासिका → नस् + अच् → उन्नता नासिकाऽस्य = **उन्नसः** (उद्नसः is the other fork of 8.4.45 यरोऽनुनासिके, वā). Same `-Ap` clear as 5.4.134. प्रणसः still needs SK859/8.4.28 ṇatva — deferred |
| 863 | 5.4.124 | धर्मादनिच्केवलात् | Bahuvrīhi (**B4** samāsānta अनिच्, `bahiranga: -1`): a धर्म-final bahuvrīhi (after a kevala pūrva) → धर्मन् (n-stem) → nom sg कल्याणधर्मा. Uttara-substitution धर्म→धर्मन् |
| 884 | 5.4.146 | ककुदस्यावस्थायां लोपः | Bahuvrīhi (**B4** samāsānta lopa, `bahiranga: -1`): the final of ककुद (age/condition sense) drops → ककुद् (consonant stem) → प्राप्तककुत् / प्राप्तककुद् (8.4.56). Uttara-substitution ककुद→ककुद् |
| 650 | 2.4.71 | सुपो धातुप्रातिपदिकयोः | (Tatpuruṣa **T1** engine fix) The pūrva sup luks; now also clears the stale `?Ba` (bha-saṁjñā from the vigraha sup via 1.4.18) per 1.1.63 न लुमताङ्गस्य, so an-stem pūrvas take 8.2.7 न-lopa (राजन्→राज→राजपुरुषः) instead of 6.4.134 अल्लोपोऽनः misfiring (राजन्→राज्ञ्→राक्…) |
| 451 | 1.1.41 | अव्ययीभावश्च | Avyayībhāva (S1A; out of SK order, was deferred; S4 → `bahiranga: -1`): avyaya saṁjñā on the avyayībhāva uttara → its sup luks (2.4.82) → अधिहरि. Moved into the samāsa pre-pass (condition rp ?avyayIBAva); ?avyaya now rides through the TaC merge (join_objects Tier-3) for उपशरदम् |
| 6.4.22 | 6.4.22 | असिद्धवदत्राभात् | (out-of-SK-order, engine-level) ābhīya asiddhavat — partial. Static-samanāśraya peers {6.4.148, 6.4.150, 6.4.149, 6.4.134} are pair-wise asiddha to each other (6.4.149 added with SK499: matsya y-lopa composes with 148's a-lopa → मत्सी). `view()` walks past peer ancestors at the same window (returns the pre-section snapshot for condition AND xform input); `_compose_abhiya` derives a per-snapshot-position diff of `operate(snapshot)` vs `snapshot` and composes it with prior peer diffs into the current state — so both peers' edits land in the merged output. Unlocks the ṣpha cluster (गार्गी uses 148+150 composition; गार्ग्यायणी/लौहित्यायनी/कौरव्यायणी block 134 from seeing 148's output). The वुग्युट… vārttika and broader scope are deferred — see Skipped table |
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
| 836 | 6.3.35 | तसिलादिष्वाकृत्वसुचः | Deferred (bahuvrīhi B1) — affix-context, not a bahuvrīhi rule | puṁvadbhāva before the tasil…kṛtvasuc (5.3.7–5.4.17) taddhita affixes; needs that affix machinery |
| 837 | 6.3.36 | क्यङ्मानिनोश्च | Deferred (bahuvrīhi B1) — affix-context, not a bahuvrīhi rule | puṁvadbhāva before kyaṅ (denominative) / mānin; needs the kyaṅ+mānin machinery (एतायते, दर्शनीयमानिनी) |
| 840 | 6.3.39 | वृद्धिनिमित्तस्य च तद्धितस्यारक्तविकारे | Deferred (bahuvrīhi B1) — needs taddhita-vṛddhi analysis | puṁvadbhāva prohibition for a fem formed by a vṛddhi-causing taddhita (except rakta/vikāra senses); the vṛddhi-nimitta test on the taddhita is not modelled |
| 843/851/844 | 2.2.25, 5.4.73, 6.4.142 | संख्ययाऽव्ययासन्नादूराधिकसंख्याः संख्येये / बहुव्रीहौ संख्येये डजबहुगणात् / ति विंशतेर्डिति | Bahuvrīhi (**B2 formation + B3 डच्**, `bahiranga: -1`): an avyaya (उप) / आसन्न / अदूर / अधिक / saṅkhyā + a saṅkhyā, in the **संख्येय** sense → bahuvrīhi, then डच् → **उपदशाः**, **आसन्नविंशाः** | The pūrva is indeclinable so SK830/2.2.24 cannot form it (same reason as 2.2.28). `?saMKyeya` is composer-supplied, like `?vayas` for 5.4.141. डच् is ḍit → 6.4.143 टेः drops दश**न्**'s ṭi → दश; दशन्'s `?nityabahuvacana` gives the plural. **अबहुगणात्** modelled via `=!bahu` / `=!gaRa` → **उपबहवः** keeps its u-stem (बहु/गण are saṅkhyā by 1.1.23). 6.4.142 is NOT subsumed by 6.4.143: ṭi of विंशति is only the final इ, so 6.4.143 alone gives *आसन्नविंश**त**ाः (verified by disabling 6.4.142) — hence `overrides: 6.4.143`. **Correction:** this was previously deferred as "accent-only", a misreading of Vasu 54073 — that remark describes the अबहुगण EXCEPTION (उपबहवः/उपगणाः, where डच् is *not* added), not उपदशाः |
| 846 | 2.2.27 | तत्र तेनेदमिति सरूपे | Deferred (bahuvrīhi B2) — surface needs 5.4.127 ic (B4) | homonym-reciprocity bahuvrīhi (केशाकेशि); needs a sarūpa lp==rp content check + इच् 5.4.127 + 6.3.137 अन्येषामपि दृश्यते + avyaya tagging — NOT reduplication (the vigraha केशेषु केशेषु supplies the word twice) |
| 898 | 2.2.35 | सप्तमीविशेषणे बहुव्रीहौ | Deferred (bahuvrīhi B2) — vyadhikaraṇa + physical pūrva-nipāta | a saptamī / viśeṣaṇa member goes first (कण्ठेकालः); needs the vyadhikaraṇa-bahuvrīhi formation + the deferred physical reorder (2.2.30) |
| 899 | 2.2.36 | निष्ठा | Deferred (bahuvrīhi B2) — physical pūrva-nipāta | a niṣṭhā goes first (कृतकृत्यः); needs the deferred physical member reorder (2.2.30) |
| 900 | 2.2.37 | वाहिताग्न्यादिषु | Deferred (bahuvrīhi B2) — ākṛtigaṇa + physical pūrva-nipāta | āhitāgnyādi optional niṣṭhā-first (आहिताग्निः/अग्न्याहितः); ākṛtigaṇa + the deferred reorder |
| 832/834/835/844/847/851/856–862/866/890/892/894–897 | 5.4.73,116,118–122,127,152,156,157,159,160, 7.4.13–15, 6.4.142/146, 8.4.3/28 | (bahuvrīhi samāsānta — affix insertion) | **COMPLETE** (2026-07-21) — every affix family landed: कप् core + minor, षच्, अप् (5.4.116/117), इच् 5.4.128, अनिच्, असिच्, डच्, **अच् (5.4.120/121, new `ac_s`)** | Still open in this range: **इच् reciprocal 5.4.127** (केशाकेशि — needs 2.2.27 sarūpa + 6.3.137 + avyaya tagging, NOT reduplication; it also unlocks 6.4.146 ओर्गुणः/बाहूबाहवि, already implemented but unreachable). 7.4.13/7.4.14 deliberately NOT implemented (net no-op for कप्). 5.4.120 partially modelled — see its row |
| 864–888 | 5.4.125–150, 6.1.66 | (bahuvrīhi samāsānta — ādeśa/lopa/nipātana) | **COMPLETE** (2026-07-21) — jñu, anaṅ + 5.4.133, niṅ, datṛ + 5.4.143/144/145, gandha 5.4.135/136/137, pāda 5.4.138/139/140, kakud 5.4.146/147/148/149, hṛd, jambhā/dakṣiṇerma nipātanas | **SK873/6.1.66 लोपो व्योर्वलि is neither implemented nor needed**: 5.4.134 substitutes जाया→जानि directly and the composer supplies युवन्, so युवजानिः derives without it. 5.4.145's अग्रान्त arm is unexercised |
| 55 | 8.4.48 | नादिन्याक्रोशे पुत्रस्य | Skipping for now | Vedic/accent |
| 56 | 8.4.50 | त्रिप्रभृतिषु शाकटायनस्य | Skipping for now | Śākaṭāyana option |
| 57 | 8.4.51 | सर्वत्र शाकल्यस्य | Skipping for now | Śākalya option |
| 58 | 8.4.52 | दीर्घादाचार्याणाम् | Skipping for now | Āchārya option |
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
| 493 | 4.1.36 | पूतक्रतोरै च | Partial — puṃyoga restriction not encoded | The triśloka (4.1.36–38) applies only in the puṃyoga ('wife of') sense (vārttika). Accent (udātta ai) is not modelled. SK493 fires unconditionally on pUtakratu |
| 495 | 4.1.38 | मनोरौ वा | Partial — ai-variant deferred | The ai-substitute form मनायी (from वा + anuvṛtti of 4.1.37's ai) is not generated; only the au-form मनावी and the no-substitute u-stem मनुः are produced |
| 496 | 4.1.39 | वर्णादनुदात्तात्तोपधात्तो नः | Partial — vārttikas + accent deferred | Accent (anudātta-ending) not modelled. The vārttikas पिशङ्गादुपसङ्ख्यानम् (पिशङ्गी), असितपलितयोर्न (no ṅīp → असिता/पलिता), and छन्दसि क्नमेके (असिक्नी/पलिक्नी) are not implemented. अवदात excluded (it is a viśuddha-, not varṇa-, word) — handled naturally by simply not tagging it |
| 497 | 4.1.40 | अन्यतो ङीष् | Partial — accent not modelled | ṅīṣ vs ṅīp differ only in accent, which the engine does not track; surface ī is identical. Colour-word scope encoded via the ?varNa_anyatas lexical tag |
| 498 | 4.1.41 | षिद्गौरादिभ्यश्च | Partial — anaḍuhī vārttika + ākṛtigaṇa tail | The vārttika आमनडुहः स्त्रियां वा (अनडुही ~ अनड्वाही) is deferred. gaurādi is an ākṛtigaṇa; the ~57 **named** simple members from Vasu's list are now registered (?gaurAdi), but the open-ended ākṛti tail and the samasta/special items (śvan/takṣan n-stems, anaḍuhī/anaḍvāhī) are not |
| 499 | 6.4.149 | सूर्यतिष्यागस्त्यमत्स्यानां य उपधायाः | Partial — āgastī deferred | The main taddhita path is now implemented: `?sUryAdi` propagates from sūrya/tiṣya through the aṇ-taddhita merge (tier-3 in `join_objects`) → SK499 fires on saurya/taiṣya bha-aṅga → सौरी/तैषी. The matsya direct ṅīṣ path (vārttika मत्स्यस्य ङ्याम् → मत्सी) was already working. Remaining deferred: āgastī (agastya via 4.1.114, a different taddhita affix not yet in the generator) and the tiṣya nakṣatra-sense vārttika |
| 500 | 4.1.42 | जानपदकुण्ड…कबरात् | Partial — 11 senses not modelled | Each of the 11 stems takes ṅīṣ only in a specific sense (जानपदी=vṛtti, कुण्डी=amatra, …); the engine doesn't model these, so the rule over-generates ṅīṣ in the other sense. कुण्ड's separate jāti-ṅīṣ reading also out of scope |
| 502 | 4.1.44 | वोतो गुणवचनात् | Partial — kharu/saṃyoga-upadhā exception | The vārttika खरुसंयोगोपधान्न (no ṅīṣ for kharu or a saṃyoga-upadhā u-stem like पाण्डु) is deferred — those stems are simply not tagged ?guRavacana. guṇavacana is an open class; representative members only |
| 503 | 4.1.45 | बह्वादिभ्यश्च | Partial — ākṛtigaṇa tail + gaṇasūtras | bahvādi is an **ākṛtigaṇa** (आकृतिगणोऽयम्). The ~27 named simple members from Vasu's list are now registered (?bahvAdi); excluded are the 3 gaṇasūtra entries (इतः प्राप्यंगात्, कृदिकारादक्तिनः, सर्वतोऽक्तिन्नर्थात्), candrabhāgā (special), the ajādi/svāṅga-overlapping members (bāla/ahan/kroḍa/nakha/khura/śikhā/śapha/guda), and the open ākṛti tail (bhaga/gala/rāga…). The gaṇasūtra alternants (रात्रि/रात्री; शकटि/शकटी; पद्धति/पद्धती) remain deferred |
| 504 | 4.1.48 | पुंयोगादाख्यायाम् | Partial — puṃyoga semantics + vārttikas | The 'wife-of' (puṃyoga) restriction is not modelled (fires unconditionally on ?puMyoga). Vārttikas पालकान्तान्न (गोपालिका) and सूर्याद्देवतायां चाप् (सूर्या) deferred |
| 505 | 4.1.49 | इन्द्रवरुण…आनुक् | Partial — senses + mātulī vārttika | The puṃyoga restriction (6 proper nouns) and the special senses (हिमानी=mahad-hima, यवानी=duṣṭa-yava, यवनानी=lipi) are not modelled. The optional-ānuk vārttika मातुलोपाध्याययोरानुग्वा (मातुली beside मातुलानी) is deferred — mātula takes mandatory ānuk here |
| 508 | 4.1.52 | बहुव्रीहेश्चान्तोदात्तात् | Deferred — antodātta accent | antodātta kta-final bahuvrīhi → ṅīṣ (ऊरुभिन्नी). The compound machinery now exists (llp peeking); only the **antodātta accent** gate is unmodelled (per user decision, no tag workaround). vārttikas (jāti-pūrva, jātānta, pāṇigṛhītī) also out of scope |
| 509 | 4.1.53 | अस्वाङ्गपूर्वपदाद्वा | Deferred — antodātta accent | SK508 + non-svāṅga pūrvapada (`llp: ?!svAnga`) → optional ṅīṣ (सुरापीती/सुरापीता). svāṅga classification is now available (?svAnga); only the antodātta gate remains unmodelled |
| 516 | 4.1.61 | वाहः | Deferred — Vedic/narrow | ṅīṣ after vāh-final (dityauhī); Vedic, narrow scope |
| 527 | 4.1.73 | शार्ङ्गरवाद्यञो ङीन् | Partial — general añ-arm not structural | The full named śārṅgaravādi gaṇa is implemented (5 tagged stems + brāhmaṇa + nara gaṇasūtra). The 2nd arm — "any jāti word ending in the affix añ → ṅīn" (e.g. aurvī from urva+añ) — is covered only for explicitly tagged stems, not as a general rule keyed on an ?añ-derived marker. Would need ?aY propagation through the añ merge |
| 7.1.92 / 7.1.93 | 7.1.92 / 7.1.93 | सख्युरसंबुद्धौ / अनङ् सौ | Refinement (SK517) | Added `?!strI` to both: saKi's tag propagates onto the merged feminine sakhī (via the strI-fork all-tags copy in join_objects); without the guard, the masculine sakhā / anaṅ nom-sg substitution mis-fired on sakhī. Mirrors the SK490/491 pati ?!strI guards |
| 541 | 1.4.53 | हृक्रोरन्यतरस्याम् (anyatarasyām branch) | Deferred to K3 — pre-pass optional-forking not yet built | K1 emits only the karma (dvitīyā) reading; the optional kartṛ→tṛtīyā alternative (हारयति भृत्येन) waits on the K3 fork mechanism |
| 540 | 1.4.52 | ṇyanta vārttikas | Deferred — vārttika long tail (karaka_plan.md §6) | नीवह्योर्न, नियन्तृकर्तृकस्य वहेरनिषेधः, आदिखाद्योर्न, भक्षेरहिंसार्थस्य न, जल्पतिप्रभृतीनामुपसङ्ख्यानम्, दृशेश्च, ज्ञानसामान्यार्थग्रहण (स्मरति/जिघ्रति excluded) — implement when their exemplar verbs are needed |
| 541 | 1.4.53 | अभिवादिदृशोरात्मनेपदे (vārttika) | Deferred — vārttika long tail + needs ātmanepada modelling | abhivad/dṛś optionally karma in ātmanepada (अभिवादयते देवं भक्तेन) |
| 544 | 1.4.48 | अभुक्त्यर्थस्य न (vārttika) | Deferred — needs saptamī (K7) | वने उपवसति "fasts in the forest" → locus stays saptamī, not karma |
| 545 | 2.3.4 | उभय/सर्वतस्/अभितः/परितः/समया/निकषा/हा/धिक्/उपरि dvitīyā vārttikas | Deferred — particle long tail | dvitīyā with these particles (उभयतः कृष्णम्, अभितः कृष्णम्, ग्रामं समया, धिक् कृष्णाभक्तम्…); implement alongside the K2 karmapravacanīya/particle work |
| 554 | 1.4.93 | अधिपरी अनर्थकौ | Deferred (K2) — **accent-only, no vibhakti effect** | adhi/pari when meaningless (anarthaka) get karmapravacanīya (कुतोऽध्यागच्छति), whose sole effect is to override the gati/upasarga saṁjñās → **nighāta (accent)**; it changes no sup/vibhakti, so there is nothing to derive or test until accent is modelled |
| 552 | 1.4.90 | bhāga / vīpsā senses; anu re-inclusion | Deferred (K2) — sense long tail | 1.4.90 here covers prati/pari × lakṣaṇa/itthaṁbhūta. bhāga (लक्ष्मीर्हरिं प्रति, ṣaṣṭhī-sense) and vīpsā (वृक्षंवृक्षं प्रति, reduplication) deferred; anu's lakṣaṇa/tṛtīyārtha/hīna are 1.4.84–86, so anu is kept out of 1.4.90 (avoids the 1.4.84-vs-1.4.90 higher-aps shadow) |
| 553 | 1.4.91 | vīpsā sense (abhi) | Deferred (K2) — needs reduplication | देवं देवमभि सिञ्चति (vīpsā) needs āmreḍita reduplication; 1.4.91 covers lakṣaṇa/itthaṁbhūta |
| 557 | 1.4.96 | padArtha/anvavasarga/garhā/samuccaya senses (api) | Deferred (K2) — sense long tail | 1.4.96 covers sambhāvanā; the other api senses are nuanced (mostly no dvitīyā) and deferred |
| 551 | 1.4.87 | upa adhika → saptamī | Deferred (K2) → K7 | उपोऽधिके च also covers the adhika sense, whose vibhakti is saptamī (2.3.9, SK645/K7); K2 implements only the hīna sense (→ dvitīyā) |
| 581 | 2.3.14 | क्रियार्थोपपदस्य च कर्मणि स्थानिनः | Deferred (K4) — needs kṛt-derivation (tumartha sthānin), karaka_plan.md §6 | the karma of an implied tum-artha action (एधेभ्योऽव्रजति = एधआहर्तुं व्रजति) → caturthī; the "sthānin" upapada has no kṛt/tumun modelling yet |
| 582 | 2.3.15 | तुमर्थाच्च भाववचनात् | Deferred (K4) — needs kṛt-derivation (tumartha bhāva-noun), karaka_plan.md §6 | a bhāva-noun in the tum-artha (purpose) sense → caturthī (पाकाय व्रजति); same tum-artha modelling gap as SK581 |
| 587 | 2.3.28 (vā) | जुगुप्साविरामप्रमादार्थानामुपसङ्ख्यानम् | Deferred (K5) — vārttika long tail | jugupsā/virāma/pramāda verbs add their object to apādāna → pañcamī (पापाज्जुगुप्सते, विरमति, धर्मात्प्रमाद्यति); the eight base apādāna sutras (1.4.24–31) are implemented, this vārttika extends the verb set |
| 594 | 1.4.31 (vā) | ल्यब्लोपे कर्मण्यधिकरणे च | Deferred (K5) — needs lyap-lopa / kṛt modelling | with an elided lyab (prāsādāt prekṣate = prāsādam āruhya), the karma/adhikaraṇa optionally → pañcamī; needs the absolutive (lyap) derivation, absent like the tum-artha kṛt |
| 595 | 2.3.29 (part) | ञ्च्-उत्तरपद / आच् / आहि-युक्त yoga-words | Deferred (K5) — yoga-word long tail | 2.3.29 also lists ñc-uttarapada (प्राक्/प्रत्यक्), āc, and āhi-yukta yoga-words; the implemented arm covers anya/ārāt/itara/ṛte and a dik-word (पूर्व), enough to exercise the llp/rrp peek |
| 602 | 2.3.25 (योगविभाग) | अगुणे स्त्रियां च क्वचित् | Deferred (K5) — yoga-vibhāga extension | the योगविभाग reading also gives optional pañcamī अगुणे (धूमादग्निमान्) and स्त्रियाम् (नास्ति घटोऽनुपलब्धेः); the main गुणेऽस्त्रियाम् fork is implemented |
| 624 | 2.3.66 | उभयप्राप्तौ कर्मणि | Deferred (K6) — needs a genuine dual-kāraka kṛt-valency frame | when both kartṛ and karman could take ṣaṣṭhī under 2.3.65, the karman (ubhaya-prāpti) is fixed as karman; requires a kṛt governor with two simultaneous kārakas, which the single-kāraka test frames do not model |
| 630 | 2.3.72 | तुल्यार्थैरतुलोपमाभ्यां तृतीयान्यतरस्याम् | Deferred (K6) — tulya-artha comparison long tail | with tulya-artha words (except atula/upamā) the standard of comparison optionally → tṛtīyā (else ṣaṣṭhī): तुल्यो देवदत्तेन / देवदत्तस्य; no tulya-yoga test frame yet |
| 631 | 2.3.73 | चतुर्थी चाशिष्यायुष्यमद्रभद्रकुशलसुखार्थहितैः | Deferred (K6) — āśiṣ benediction long tail | in benediction (āśiṣ) with āyuṣya/madra/bhadra/kuśala/sukha-artha/hita words the person optionally → caturthī (else ṣaṣṭhī): आयुष्यं देवदत्ताय / देवदत्तस्य; not yet modelled |
| 654 | 2.2.30 | उपसर्जनं पूर्वम् | Partial (avyayībhāva S0) — the upasarjana saṁjñā is recorded in the samāsa pre-pass, but physical pūrva-nipāta (moving the upasarjana to the front, carrying its sup) is deferred; avyayībhāva needs no reorder (avyaya is already pūrva) | tatpuruṣa/bahuvrīhi/dvandva where the upasarjana is not the pūrva |
| 694 | 2.1.33–35 | कृत्यैरधिकार्थवचने / अन्नेन व्यञ्जनम् / भक्ष्येण मिश्रीकरणम् | Deferred (tatpuruṣa T1) — tṛtīyā long tail; each needs a specialized lexical class (kṛtya-pratyaya words, anna/vyañjana, bhakṣya/miśrīkaraṇa) | दध्योदनः, गुडधानाः … |
| 704 | 2.2.2–5 / 2.2.9–11 | अर्धं नपुंसकम् … / याजकादिभिश्च / न निर्धारणे / पूरणगुण… | Deferred (tatpuruṣa T1) — ṣaṣṭhī extensions + exceptions; 2.2.8 (राजपुरुषः) + 2.2.1 (पूर्वकायः) implemented | अर्धपिप्पली, निर्धारण/pūraṇa exclusions |
| 719 | 2.1.42–48 | ध्वाङ्क्षेण… / पात्रेसमितादयश्च … | Deferred (tatpuruṣa T1) — saptamī long tail; specialized lexical classes; 2.1.40 (अक्षशौण्डः) + 2.1.41 (स्वर्गसिद्धः) implemented | ध्वाङ्क्षक्षेत्रम्, पात्रेसमिताः … |
| 701 | 6.3.2 | पञ्चम्याः स्तोकादिभ्यः (aluk) | Deferred (tatpuruṣa T1) — the स्तोक/अन्तिक/दूर/कृच्छ्र pañcamī is RETAINED (aluk-samāsa) → स्तोकान्मुक्तः; the 2.1.39 rule instead luks the pūrva sup (2.4.71) like every other branch, giving स्तोकमुक्तः. Needs an aluk carve-out on 2.4.71 for the stokādi pūrva | स्तोकान्मुक्तः, अन्तिकादागतः, दूरादागतः |
| 759–760 | 6.3.75, 6.3.77 | न भ्राष्ट्रादिना (नभ्राट्…) / नगोऽप्राणिषु (नगः) | Deferred (tatpuruṣa T3 stretch) — the nañ **prakṛtibhāva** exceptions: for a fixed lexical set the न is kept intact (नभ्राट्/नपात्/नवेदस्/नासत्य/नमुचि…; नक/नग for the non-living गम्), overriding 6.3.73/74. Needs a tagged uttara-stem exception list; low value | नभ्राट्, नपात्, नगः … |
| 781–785 | 2.2.19, 3.1.92 | उपपदमतिङ् / तत्रोपपदं सप्तमीस्थम् | Deferred (tatpuruṣa T4) — upapada compounds need the **kṛt-pratyaya** machinery (कुम्भकारः = कुम्भ + √कृ + अण्), not yet in samāsa scope. 2.2.18 (प्राचार्यः, कुपुरुषः) implemented; the gati long-tail (1.4.66, 1.4.70–79) is also deferred — only the core ऊर्यादि/पुरस्/अस्तम् feeds 2.2.18 (carried as the intrinsic ?gati tag) | कुम्भकारः, कुरुचरः … |
| 789 | 5.4.91 (ahar/sakhi), 5.4.86/94/101 | राजाहःसखिभ्यष्टच् (ahar/sakhi) / अङ्गुलेर्दारुणि / अन्नोऽच् / खार्याः … | Deferred (tatpuruṣa T5) — 5.4.91 rājan-arm (परमराजः) + 6.3.46 (महाराजः) implemented; the ahar/sakhi arms (द्व्यहः) collide with the existing dvyahna न्-retention (the samāsānta wac is deliberately non-ट-marked → द्व्यह्न, SK238), and 5.4.86 अङ्गुलि / 5.4.94 an-final (अक्ष्णः) / 5.4.101 khārī need stems not added | द्व्यहः, अक्ष्णः, द्विखारि … |
| 822 | 2.4.19, 2.4.30, 2.4.31 | तत्पुरुषोऽनञ्कर्मधारयः / अपथं नपुंसकम् / अर्धर्चाः पुंसि च | Deferred (tatpuruṣa T-liṅga) — 2.4.29 रात्राह्नाहाः पुंसि (ahan-family → masc) implemented. 2.4.19 (napuṁsaka only in the 2.4.17 saṃjñā-doubtful domain — inert without saṃjñā tagging, would wrongly napuṁsaka-ise ordinary masc tatpuruṣas like राजपुरुषः); 2.4.30 needs the pathin अच् samāsānta (5.4.74); 2.4.31 needs the अर्धर्चादि stems | अपथम्, अर्धर्चः/अर्धर्चम् … |
| 706–711 | 2.2.12–17 (+ 2.2.7, 2.2.20–22) | क्तेन च पूजायाम् / अधिकरणवाचिना / कर्मणि / तृजकाभ्यां कर्तरि / कर्तरि च / नित्यं क्रीडाजीविकयोः; ईषदकृता; अमैवाव्ययेन / तृतीयाप्रभृतीनि / क्त्वा च | Deferred (tatpuruṣa audit) — the **ṣaṣṭhī + kṛt / aluk** block: each compounds a ṣaṣṭhī (or aluk/avyaya) noun with a kṛt-derivate (kta / tṛc / aka / ktvā) in a specific sense (pūjā, adhikaraṇa, karman, kartṛ, krīḍā-jīvikā). Needs the kṛt-pratyaya + aluk machinery (same dependency as upapada 2.2.19/3.1.92) | कुम्भकारकः, अक्षधूर्तः, गेहेशूरः … |
| 732–754 | 2.1.53–72 | कुत्सितानि कुत्सनैः / पापाणके / उपमानानि सामान्यवचनैः / उपमितं व्याघ्रादिभिः / पूर्वापर… / श्रेण्यादयः / क्तेन नञ्विशिष्टेन / सन्महत्… पूज्यमानैः / वृन्दारक… / कतरकतमौ / किं क्षेपे / पोटायुवति… / प्रशंसावचनैः / युवा खलति… / कृत्यतुल्याख्या / वर्णो वर्णेन / कुमारः श्रमणादिभिः / चतुष्पादो गर्भिण्या / मयूरव्यंसकादयश्च | Deferred (tatpuruṣa audit) — the **lexical-gaṇa / sense-class karmadhāraya** block: each keys on a specific word-set (kutsita/pāpa/upamāna-vyāghrādi/śreṇyādi/pūjyamāna/mayūravyaṁsakādi…) or a semantic condition (kṣepa, praśaṁsā, upamā, jāti-pariprašna). Needs per-sutra lexical gaṇas / sense tags; low generation value | कृष्णसर्प (done via 2.1.57); पुरुषव्याघ्रः, मयूरव्यंसकः … |
| 763–780 | 1.4.62–79 | अनुकरणं चानितिपरम् / आदरानादरयोः / भूषणेऽलम् / अन्तरपरिग्रहे / अच्छ गत्यर्थवत्… / तिरोऽन्तर्द्धौ / विभाषा कृञि / उपाजेऽन्वाजे / साक्षात्प्रभृतीनि / अनत्याधान… / मध्ये पदे… / नित्यं हस्ते… / प्राध्वं बन्धने / जीविकोपनिषदौ | Deferred (tatpuruṣa T4) — the **gati long-tail**: each gives the गति saṁjñā to a specific lexical word / class (anukaraṇa, alam, sākṣāt, madhye, haste…), mostly consumed with kṛ/bhū/as (cvi/kṛt). Only ऊर्यादि/पुरस्/अस्तम् (1.4.61/67/68) are in scope | साक्षात्कृत्य, अलंकृत्य, मध्येगुरु … |
| 790–811 | 5.4.88–105 (minus 92), 6.3.47–49, 6.3.76, 8.4.7, 8.4.39 | अह्नोऽह्न एतेभ्यः / न संख्यादेः समाहारे / उत्तमैकाभ्यां / अग्राख्यायामुरसः / ग्रामकौटाभ्यां तक्ष्णः / अतेः शुनः / उपमानादप्राणिषु / उत्तरमृगपूर्वात् सक्थ्नः / नावो द्विगोः / अर्धात् / द्वित्रिभ्यामञ्जलेः / ब्रह्मणो जानपदाख्यायाम् / कुमहद्भ्याम्; द्व्यष्टनः / त्रेस्त्रयः / विभाषा चत्वारिंशत्; एकादिश्चादुक्; अह्नोऽदन्तात् / क्षुभ्नादिषु | Deferred (tatpuruṣa audit) — **specialized per-stem samāsāntas** (aṅga-/uras-/takṣan-/śvan-/sakthi-/nau-/añjali-/brahman- finals) + **numeral-pūrva phonology** (dvi/aṣṭan, tri→traya, ekādi-nuṭ) + the **ahar अच्** (5.4.88, ties to the deferred 5.4.91 ahar-arm / 6.4.145 द्व्यह्न) + ṇatva 8.4.7/39. Each needs its stem/numeral gaṇa; the proven ?samasanta_TaC path can host them when scoped | द्व्यहः, पञ्चनावम्, द्व्यङ्गुलम्, त्रयोदश … |
| 813–828 | 2.4.20–27, 1.2.58–63 | संज्ञायां कन्थोशीनरेषु / उपज्ञोपक्रमम् / छाया बाहुल्ये / सभा राजामनुष्यपूर्वा / अशाला च / विभाषा सेनासुरा… / पूर्ववदश्ववडवौ; जात्याख्यायाम्… बहुवचनम् / अस्मदो द्वयोश्च / फल्गुनीप्रोष्ठपदानाम् / तिष्यपुनर्वस्वोः | Deferred (tatpuruṣa T-liṅga) — **saṃjñā-domain gender + number** rules (kanthā/upajñā/chāyā/sabhā/aśālā/senā gender; jāti-bahuvacana, asmad-dual, nakṣatra-number). Inert without saṃjñā / nakṣatra-number tagging, same class as the deferred 2.4.19 | उपज्ञम्, राजसभम्, फल्गुनी/फल्गुन्यौ … |
| 8.4.1 | 8.4.1/8.4.2 | रषाभ्यां नो णः समानपदे (pūrva-trigger cross-member) | Deferred — PRE-EXISTING (not a T1 rule gap): a pūrva-only र/ष trigger reaching the uttara's न-bearing sup (चोरात् भयम् → चोरभयेण) does not fire; the CLI `in_compound` path shows the same (coraBayena), so it is independent of the samāsa pre-pass. Uttara-side / same-segment ṇatva now WORKS via `_nest_samasa_members` (राजपुरुषेण, कृष्णपुरुषेण, मासपूर्वेण) | a compound whose ONLY र/ष trigger is in the pūrva |
| 665 | 2.1.11 | विभाषा | Natural (avyayībhāva S2) — the "only-when-intended" adhikāra is realized as the `?samAsa_vivakza` gate on the ≥SK665 rules; not a standalone rule block | S2 vibhāṣā block (अपग्रामम्, प्रत्यग्नि …) |
| 671 | 2.1.17 | तिष्ठद्गुप्रभृतीनि च | For later (avyayībhāva) — tiṣṭhadgu-gaṇa of ready-made avyayībhāvas (a lexical list) | gaṇa members (tiṣṭhadgu, āyatīgavam, …) |
| 672 | 2.1.18 | पारे मध्ये षष्ठ्या वा | For later (avyayībhāva) — pāre/madhye need pre-inflected irregular pūrva members (पारेगङ्गम्) | pāre/madhye ṣaṣṭhī-vā compounds |
| 675 | 2.1.21 | अन्यपदार्थे च संज्ञायाम् | For later (avyayībhāva) — anyapadārtha (bahuvrīhi-like) avyayībhāva as a saṁjñā | named anyapadārtha compounds (कण्ठेकालम् etc.) |
| 676 | 5.4.68 | समासान्ताः | Natural (avyayībhāva S3) — samāsānta adhikāra; realized as the rule-driven ?samasanta_TaC + `_insert_samasanta` path (5.4.107–112). The 2.4.84 सुमद्रम्/उन्मत्तगङ्गम् nitya-am exception list remains deferred | samāsānta affixes |

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

### Kāraka sentence cases (`karaka_list.py` / `test_karaka.py`)

67 cases from the SK commentary. **K0 (26, SK532–537, 559–561, 606):** हरिं भजति
(+ dual/plural/napuṁsaka), रामो हरिं भजति, हरिः सेव्यते, रामेण सेव्यते, बाणेन (karaṇa,
both prayogas + plural), हे राम/हरे/हरयः, रामस्य पुत्रः (+ plural śeṣa, śeṣa-in-verb-
sentence), कृष्णः/ज्ञानम्/रामौ (bare prathamā), plus negatives: माष slot stays
kāraka-free, the 1.4.49-beats-1.4.42 param carve-out, the skip-guard no-op, two
karma nouns, sambodhana inside a verb sentence. **K1 (15, SK538–545):** तृणं स्पृशति
(anīpsita), गां दोग्धि पयः (akathita dvikarmaka), मासमास्ते (akarmaka vārttika),
कृष्णं स्वर्गमगमयत् / वेदमध्यापयद्विधिम् (ṇyanta gati/buddhi kartṛ→karma), कारयति भृत्यं
कटम् (hṛ/kṛ karma-only), अध्यास्ते/उपवसति वैकुण्ठं हरिः, अभिनिविशते सन्मार्गम् (locus→karma),
अन्तरेण हरिम् / अन्तरा कृष्णम् (antarā-yoga dvitīyā), plus negatives: akathita with a
non-dvikarmaka verb, the गत्यादि-किम् ṇyanta-non-gati check, and the 2.3.4 adjacency
guard (a non-adjacent noun stays prathamā). **K2 (14, SK546–558):** जपमनु (anu
lakṣaṇa, dir=pūrva), नदीमनु (tṛtīyārtha), अनु/उप हरिम् (hīna, dir=para), वृक्षं/विष्णुं
प्रति (1.4.90), हरिमभि (1.4.91), अति देवान् कृष्णः (atikramaṇa), कृष्णम् अनु रामः
(between-two-nouns direction disambiguation — pūrva tags only kṛṣṇa), सु (1.4.94
saṁjñā-only), सर्पिषोऽपि (api saṁjñā-only, sarpis ṣaṣṭhī, 2.3.8 not fired), मासं
कल्याणी / क्रोशं गिरिः (2.3.5 atyanta-saṁyoga), plus the मासस्य negative (not
continuous → ṣaṣṭhī). **K3 (12, SK562–568, tṛtīyā cluster):** अक्षैरक्षान्वा दीव्यति
(1.4.43 **vibhāṣā** karma/karaṇa — both forks), क्रोशेन (अपवर्ग, beats 2.3.5 by para)
+ the अपवर्गे-किम् negative (क्रोशम्), पुत्रेण सह (पिता) / सह पुत्रेण / पुत्रेण साकम् (2.3.19
saha-yoga, llp+rrp arms), अक्ष्णा काणः (aṅga-vikāra) + अक्षि negative, जटाभिस्तापसः
(itthambhūta-lakṣaṇa), पित्रा पितरं वा संजानीते (2.3.22 **vibhāṣā** — both forks) +
the non-saṁjñā negative, धनेन कुलम् (hetu). The two vibhāṣā cases assert *both*
branches (karaka_log aggregated by index across forks; surface set via output()).
Three assertion levels per case (kAraka_* tag, viBakti_N tag set, surface forms) +
fired-trace checks.

### Kāraka sentences from the CLI (`scripts/sanskrit_generator`)

`cmd_line.py` gains `-k`/`--karaka <stem> [vacana] [sem…]` (a participant noun:
deep-copies the predefined pratipadika by its SLP1 name, sets `vacana_<N>` and each
`semantic_<prim>` tag) and `-w`/`--word <name> [sem…]` (a verb pada / plain
particle / **karmapravacanīya particle**: deep-copies the predefined object —
`Bajati`, `sevyate`, `he`, `anu_kp`, … — and, positionally like `-k` minus vacana,
sets each following token as a `semantic_<prim>` sense tag on it, e.g.
`-w anu_kp lakzaRa` = anu in the lakṣaṇa sense). Both share one dest so word order
is preserved. The engine's pre-pass then assigns the kāraka/karmapravacanīya/
vibhakti tags and inserts sups. Default output is avasāna-separated per-word forms;
`--sandhi` runs the words together for the connected sentence. Examples:

```
scripts/sanskrit_generator -k hari 1 Ipsitatama -w Bajati            # हरिम् । भजति
scripts/sanskrit_generator -k hari 1 Ipsitatama -w Bajati --sandhi   # हरिं भजति
scripts/sanskrit_generator -k hari 1 Ipsitatama -k rAma 1 svatantra -w sevyate  # हरिः । रामेण । सेव्यते
scripts/sanskrit_generator -w he -k rAma 1 samboDana                 # हे राम
scripts/sanskrit_generator -k rAma 1 Seza -k putra 1                 # रामस्य । पुत्रः
scripts/sanskrit_generator -k japa 1 -w anu_kp lakzaRa               # जपम् । अनु  (K2: noun precedes anu → dvitīyā)
scripts/sanskrit_generator -w anu_kp hIna -k hari 1                  # अनु । हरिम्  (K2: noun follows anu → dvitīyā)
scripts/sanskrit_generator -k kfzRa 1 -w anu_kp lakzaRa -k rAma 1    # कृष्णम् । अनु । रामः  (K2: only the preceding noun is governed)
```

It prints the per-word kāraka summary (kAraka_*/viBakti_N + the karmapravacanīya
saṁjñā/direction + fired sutras); `-a` (the existing trailing-avasāna option on the
`-p/-d/-t/-s` path) is untouched.

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
| udac | m | añcatir kvin (SK420, dynamic) | Dynamic: [ud, su, aYc_u, kvin]; SK415 aYc→ac; SK420 (llp:=ud reads ud prefix) apavāda of SK416: udac bha→udīcā |
| tiryac | m | añcatir kvin (SK415–417, dynamic) | Dynamic: [tiry, aYc_u, kvin]; SK415 aYc→ac; tiry ends in 'y' → dirgha no-op → bha tiryacā unchanged |
| supAd | m | d-stem (pāda compound, SK414) | SK414 (6.4.130): pAd→pad (ā→a) in bha context; inst/dat/abl/gen/loc sg + acc/gen pl use pad- base; nom/voc/acc sg+du+pl use supAd- base |
| Sf_vanip_strI | f | van-stem (SK456, dynamic) | Dynamic: [Sf, vanip, strI_abs]; SK2168 guṇa Sf→Sar; SK456 (4.1.7) NIp + n→r → SarvarI; each cell also accepts geminated SK 8.4.46 variant (Sarv-/Sarvv-) |
| dvipAd_strI | f | d-stem (pāda compound, SK457) | Dynamic: [as_purva_pada(dvi), luk_sup, in_compound(pAd_ut), strI_abs]; SK457 (4.1.8) optional NIp produces both dvipadī (NIp + SK414 bha pAd→pad) and dvipāt (no-NIp halanta) branches |
| sIman | f | man-final n-stem (SK459/461) | [sIman, strI_abs]; SK459 (4.1.11) blocks ṅīp → halanta n-stem feminine (सीमा, सीमानौ, सीम्नः); SK461 (4.1.13) optional DAp → ramā-type ā-stem (सीमा, सीमे) |
| bahuyajvan_strI | f | an-final bahuvrīhi (SK460/461) | [as_purva_pada(bahu), luk_sup, in_context(in_compound(yajvan), "bahuvrIhi"), strI_abs] (live compound, mirrors bahurAjan_strI); yajvan carries ?van so SK456 (4.1.7) competes and SK460 (4.1.12) overrides it, blocking ṅīp → halanta (बहुयज्वा, 6.4.137 keeps weak stem यज्वन्); SK461 optional DAp → बहुयज्वे |
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
| paYcatayI | f | tayap (SK470) | [paYcan, tayap, strI_abs]; ṅīp → पञ्चतयी |
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
| paYcASvI | f | SK479 ṅīp on samāhāra-Dvigu of aśva (Vasu/SK on SK480) | [as_purva_pada(paYcan), luk_sup, in_context(in_compound(aSva), "dvigu"), strI_abs]; aśva has ?ajAdi (gaṇa item 5) but NOT ?ajAdi_in_Dvigu — so 4.1.4.2 doesn't fire and SK479 ṅīp wins → पञ्चाश्वी. Gen pl पञ्चाश्वीनाम् — no r/ṛ/ṣ in stem, no ṇatva |
| paYcASvA | f | SK480 Dvigu+tadDita-luk non-parimāṇa → ṭāp | [as_purva_pada(paYcan), luk_sup, in_context(in_compound(aSva), "dvigu"), luk_tadDita, strI_abs] → पञ्चाश्वा via SK480 niṣedha (note: 4.1.4.2 also doesn't fire here since aSva lacks ?ajAdi_in_Dvigu, so SK480 is the sole path) |
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
| dvyUDnI | f | SK485 saṃkhyādi arm | dvi + UDas; SK485 peeks `llp:?saMKyA` → NIp overrides SK484 → द्व्यूध्नी; i+ū → yū (6.1.77 yaṇ) |
| atyUDnI | f | SK485 avyayādi arm | ati (avyaya stem) + UDas; SK485 peeks `llp:?avyaya` → NIp → अत्यूध्नी |
| dvidAmnI | f | SK486 dāman arm | dvi + dāman bahuvrīhi; SK486 peeks `llp:?saMKyA` → arm 1 NIp → 6.4.134 drops -an upadhā 'a' → द्विदाम्नी |
| dvihAyanI | f | SK486 hāyana arm (age sense) | dvi + hāyana (?vayasi); SK486 peeks `llp:?saMKyA` → arm 2 NIp → 6.4.148 drops final 'a' → द्विहायनी |
| dvihAyanA | f | SK486 hāyana negative (non-age → ṭāp) | dvi + hāyana, `llp:?saMKyA` but NO ?vayasi → SK486 fails → 4.1.4 ṭāp → द्विहायना (ramā-type). Vasu: द्विहायना शाला 'a hall of two years' standing'. Required 6.1.87 to strip `sarvanAmasTAna` from the post-guṇa suffix so 6.4.8 does not re-fire on the n-final surface (hāyan|e) |
| trihAyaRI | f | SK486 vārttika (tri + hāyana, age) | tri + hāyana (?vayasi); the 4.1.27.1 vārttika peeks `llp:[=tri,=catur]` → n→ṇ → SK486 (`llp:?saMKyA`) NIp → 6.4.148 a-lopa → त्रिहायणी. 'h' intervening between r and final n of -nām blocks 8.4.2 ṇatva on suffix → gen pl त्रिहायणीनाम् |
| caturhAyaRI | f | SK486 vārttika (catur + hāyana, age) | catur + hāyana same as trihAyaRI → चतुर्हायणी (gen pl चतुर्हायणीनाम्; 'h' blocks 8.4.2) |
| trihAyanA | f | SK486 vārttika negative (non-age tri + hāyana → ṭāp) | tri + hāyana (saṃkhyā pūrva) but NO ?vayasi → vārttika & SK486 (`llp:?saMKyA`) fail → 4.1.4 ṭāp → त्रिहायना (Vasu's exact शाला example). 8.4.x ṇatva blocked by 'h' between r and stem n |
| atirAjJI | f | SK487 saṃjñā arm (4.1.29) | ati + rAjan saṃjñā-bahuvrīhi: ?saMjYA attached via in_context. SK487 overrides SK462's vibhāṣā making NIp mandatory → 6.4.134 a-lopa + 8.4.40 ścutva → अतिराज्ञी |
| kevalI | f | SK488 saṃjñā arm (4.1.30) | kevala (?keval_Adi) + ?saMjYA → SK488 NIp → 6.4.148 a-lopa → केवली |
| kevalA | f | SK488 laukika arm (4.1.30) | kevala + no saṃjñā tag → SK488 fails → 4.1.4 ṭāp → केवला (ramā-type) |
| mAmakI | f | SK488 saṃjñā arm (4.1.30) | mAmaka (?keval_Adi, ?mAmaka, ?ka_pratyaya) + ?saMjYA → SK488 NIp → मामकी |
| mAmikA | f | SK488 laukika arm (4.1.30) — niyama showcase | mAmaka + no saṃjñā/chandas → SK488 fails → 4.1.4 ṭāp → mAmaka+A → SK463 (7.3.44) idādeśa fires on ?ka_pratyaya + aka_anta → मामिका (Vasu: तेन लोकेऽसंज्ञायां मामिका) |
| sumaNgalI | f | SK488 saṃjñā arm (4.1.30) | sumaNgala (?keval_Adi) + ?saMjYA → SK488 NIp → सुमङ्गली |
| patnI | f | SK490 (4.1.33 पत्युर्नो यज्ञसंयोगे) | plain pati (?pati) + strī_abs: SK490 substitutes i→n (?pati + ?!samAsa) → patn → SK453 (4.1.5) NIp → पत्नी. Declines like nadī |
| gRhapatnI | f | SK491 (4.1.34 विभाषा सपूर्वस्य) | gRha + pati compound: in_compound(pati) attaches ?samAsa → SK491 substitutes i→n → patn → SK453 NIp → patnI → samasta merge with gRha → गृहपत्नी declining as the textbook nadī. The ?Gi-leak that previously broke the 4 oblique-sg cells is fixed by guarding 1.4.7/1.4.8 with `rp: ?!strI` (and 1.4.8 with `lp: ?!strI`) so Ghi-saṃjña never lands on the feminine path |
| sapatnI | f | SK492 (4.1.35 नित्यं सपत्न्यादिषु) | [as_purva_pada(sa_pUrva), luk_sup, in_compound(pati), strI_abs] (live compound): SK492 peeks `llp:=sa` → i→n → sapatn → SK453 NIp → सपत्नी. Declines like nadī (gṛhapatnī pattern) |
| ekapatnI | f | SK492 (4.1.35 नित्यं सपत्न्यादिषु) | [as_purva_pada(eka_pUrva), luk_sup, in_compound(pati), strI_abs]: SK492 peeks `llp:=eka` → ekapatn → NIp → एकपत्नी |
| vIrapatnI | f | SK492 (4.1.35 नित्यं सपत्न्यादिषु) | [as_purva_pada(vIra_pUrva), luk_sup, in_compound(pati), strI_abs]: SK492 peeks `llp:=vIra` → vIrapatn → NIp → वीरपत्नी |
| antarvatnI | f | SK489 (4.1.32 अन्तर्वत्पतिवतोर्नुक्) | antarvat (?antarvat_pativat) + strI_abs: SK489 appends nuk 'n' at end (bahiranga 1) → antarvatn → SK453 (4.1.5) NIp → अन्तर्वत्नी. Declines like nadī. Semantic restriction (?garBiNi) not encoded — see Skipped table |
| pativatnI | f | SK489 (4.1.32 अन्तर्वत्पतिवतोर्नुक्) | pativat (?antarvat_pativat) + strI_abs: same as antarvatnI → pativatn → NIp → पतिवत्नी |
| pUtakratAyI | f | SK493 (4.1.36 पूतक्रतोरै च) | [as_purva_pada(pUta), luk_sup, in_compound(kratu), strI_abs] (live): 4.1.36 peeks llp:=pUta + lp:=kratu → u→ai + NIp; 6.1.78 → पूतक्रतायी (nadī) |
| vfzAkapAyI | f | SK494 (4.1.37) | vfzAkapi (?vfzAkapyAdi): final i→ai + NIp → वृषाकपायी; gen pl वृषाकपायीणाम् (ṇatva from ṛ) |
| agnAyI | f | SK494 (4.1.37) | agni (?vfzAkapyAdi): i→ai + NIp → अग्नायी |
| kusitAyI | f | SK494 (4.1.37) | kusita (?vfzAkapyAdi, hrasva-madhya per SK): a→ai + NIp → कुसितायी |
| kusidAyI | f | SK494 (4.1.37) | kusida (?vfzAkapyAdi, hrasva-madhya per SK): a→ai + NIp → कुसिदायी |
| manAvI | f | SK495 (4.1.38 मनोरौ वा) | manu (?manu) + strI_abs: optional u→au + NIp → मनावी; skip-fork = plain u-stem मनुः (both forks in the table) |
| enI | f | SK496 (4.1.39) | eta (?varNa_topaDa) + strI_abs: optional त्→न् + NIp → एनी; skip-fork = ṭāp एता (both forks) |
| rohiNI | f | SK496 (4.1.39) | rohita (?varNa_topaDa): त्→न् + NIp + ṇatva (8.4.1) → रोहिणी; skip-fork = ṭāp रोहिता (both forks) |
| sAraNgI | f | SK497 (4.1.40 अन्यतो ङीष्) | sAraNga (?varNa_anyatas): NIz → सारङ्गी |
| kalmAzI | f | SK497 (4.1.40) | kalmAza (?varNa_anyatas): NIz → कल्माषी |
| nartakI | f | SK498 (4.1.41 षिद्गौरादिभ्यश्च) | nartaka (ṣ it-marker `its=["z"]`, ṣvun-derived; SK498 `lp: +z`): NIz → नर्तकी |
| gOrI | f | SK498 (4.1.41) | gaura (?gaurAdi): NIz → गौरी |
| hayI | f | SK498 (4.1.41) | haya (?gaurAdi, expanded gaṇa): NIz → हयी |
| SarkArI | f | SK498 (4.1.41) | śarkāra (?gaurAdi): NIz → शर्करी (ṇatva in शर्करीणाम्) |
| caRqI | f | SK503 (4.1.45) | caṇḍa (?bahvAdi, expanded gaṇa): optional NIz → चण्डा/चण्डी (both forks) |
| kapI | f | SK503 (4.1.45) | kapi (?bahvAdi, i-final): optional NIz → कपिः/कपी (both forks) |
| SUrpI | f | SK498 (4.1.41) | śūrpa (gaurādi #42; ?gaurAdi added in place to existing def): NIz → शूर्पी |
| vArI | f | SK503 (4.1.45) | vāri (bahvādi #9; ?bahvAdi added to the ?napum 'water' def): optional NIz → वारिः/वारी |
| yUzI | f | SK498 (4.1.41) + 6.1.63 | yūṣa (gaurādi #44 + pādādi): NIz gives यूषी; the optional 6.1.63 yūṣan alternant also yields यूष्णी (rājan→rājñī parallel) — both forks |
| matsI | f | SK498+SK499 (4.1.41 + 6.4.149) | matsya (?gaurAdi+?sUryAdi): NIz, then 6.4.149 upadhā y-lopa composing with 6.4.148 a-lopa (asiddha peers) → मत्सी |
| sOrI | f | SK499 (6.4.149) taddhita path | sUrya (?sUryAdi) + aR_t: ?sUryAdi propagates through taddhita merge → SK499 y-lopa on saurya-bha → सौर् + SK470 NIp_taddhita ī → सौरी (ṇatva in gen pl सौरीणाम्) |
| tEzI | f | SK499 (6.4.149) taddhita path | tizya (?sUryAdi) + aR_t: vṛddhi → taiṣya, then SK499 y-lopa + NIp_taddhita ī → तैषी (ṇatva in तैषीणाम्) |
| sakhI | f | SK517 (4.1.62) | saKi (?sakhyAdi) → NIz → सखी (nadī); 7.1.92/93 ?!strI-guarded |
| brAhmaRI | f | SK518 (4.1.63) | brAhmaRa (?jAti_ayopaDa) → NIz → ब्राह्मणी |
| kukkuwI | f | SK518 (4.1.63) | kukkuwa (?jAti_ayopaDa) → NIz → कुक्कुटी |
| odanapAkI | f | SK519 (4.1.64) | [as_purva_pada(odana), luk_sup, in_compound(pAka), strI_abs] (live; pāka ?pAkAdi) → NIz → ओदनपाकी |
| SaNkukarRI | f | SK519 (4.1.64) | [as_purva_pada(SaNku), luk_sup, in_context(in_compound(karRa), "pAkAdi"), strI_abs] (live; per-instance ?pAkAdi keeps tuṅgakarṇā's SK511 fork) → NIz → शङ्कुकर्णी |
| SAlaparRI | f | SK519 (4.1.64) | [as_purva_pada(SAla), luk_sup, in_compound(parRa), strI_abs] (live; parRa ?pAkAdi) → NIz → शालपर्णी |
| SaNKapuzpI | f | SK519 (4.1.64) | [as_purva_pada(SaNKa), luk_sup, in_compound(puzpa), strI_abs] (live) → NIz → शङ्खपुष्पी (gen-pl ṇatva शङ्खपुष्पीणाम्) |
| dAsIPalI | f | SK519 (4.1.64) | [as_purva_pada(dAsI), luk_sup, in_compound(Pala), strI_abs] (live; clean Pala ?pAkAdi → ṅīṣ, while ajādi भस्त्रफला/त्रिफला diverge via $$ajAdi_samasta) → NIz → दासीफली |
| darBamUlI | f | SK519 (4.1.64) | [as_purva_pada(darBa), luk_sup, in_compound(mUla), strI_abs] (live) → NIz → दर्भमूली |
| govAlI | f | SK519 (4.1.64) | [as_purva_pada(go), luk_sup, in_compound(vAla), strI_abs] (live) → NIz → गोवाली |
| avantI | f | SK520 (4.1.65) | avanti (?mAnuzya_jAti_i, i-final) → NIz → अवन्ती |
| plAkzI | f | SK520 (4.1.65) | plAkzi (post-iñ base, ?mAnuzya_jAti_i) → NIz → प्लाक्षी |
| kurU | f | SK521 (4.1.66) | kuru (?manuzya_jAti_u, l:ut) → UN (ūṅ) → कुरूः (vadhū-type; कुरूणाम् ṇatva) |
| brahmabanDU | f | SK521 (4.1.66) | brahmabanDU (?manuzya_jAti_u) → ūṅ → ब्रह्मबन्धूः |
| BadrabAhU | f | SK522 (4.1.67) | BadrabAhu (?bAhvanta_saMjYA) → ūṅ → भद्रबाहूः |
| paNgU | f | SK523 (4.1.68) | paNgu (?paNgu_class) → ūṅ → पङ्गूः |
| SvaSrU | f | SK523 (4.1.68) | śvaśrū pre-registered ū-strī → श्वश्रूः |
| karaBorU | f | SK524 (4.1.69) | karaBoru (?Uru_upamAna) → ūṅ → करभोरूः |
| saMhitorU | f | SK525 (4.1.70) | [as_purva_pada(saMhita), luk_sup, in_compound(Uru), strI_abs] (live compound): 4.1.70 peeks `llp:=saMhita` + `lp:?Uru_uttara` → ūṅ; a+ū→o (6.1.87) → संहितोरूः |
| kadrU | f | SK526 (4.1.72) | kadrū pre-registered ū-strī (saṃjñā) → कद्रूः |
| kamaRqalU | f | SK526 (4.1.72) | kamaṇḍalū pre-registered ū-strī → कमण्डलूः |
| SArNgaravI | f | SK527 (4.1.73) | SArNgarava (?zANgaravAdi) → NIn (ṅīn) → शार्ङ्गरवी (nadī) |
| kApawavI | f | SK527 (4.1.73) | kApawava (?zANgaravAdi) → NIn → कापटवी |
| gOggulavI | f | SK527 (4.1.73) | gOggulava (?zANgaravAdi) → NIn → गौग्गुलवी |
| gOtamI | f | SK527 (4.1.73) | gOtama (?zANgaravAdi, 4.1.114 aṇ) → NIn → गौतमी |
| baidI | f | SK527 (4.1.73) | bEda (?zANgaravAdi, añ-derived) → NIn → बैदी |
| nArI | f | SK527 (4.1.73) gaṇasūtra | [nara, aR_t, strI_abs]: aṇ supplies ādivṛddhi (nara→nāra, the gaṇasūtra vṛddhi) + taddhita-ṅīp → नारी (nadī; नारीणाम् ṇatva) |
| AmbazWyA | f | SK528 (4.1.74) | AmbazWya (?yaNzdavya, post-ṣyañ) → cAp → आम्बष्ठ्या (ramā-type) |
| AvawyA | f | SK529 (4.1.75) | Avawya (?AvawI) → cAp → आवट्या |
| yuvatI | f | SK531 (4.1.77) | [yuvan, ti_t, strI_abs]: ti taddhita → युवतिः (i-stem; vayasi-prathama variants in oblique sg) |
| jAnapadI | f | SK500 (4.1.42) | jAnapada (?jAnapadAdi) → NIz → जानपदी |
| kuRqI | f | SK500 (4.1.42) | kuRqa (?jAnapadAdi) → NIz → कुण्डी |
| goRI | f | SK500 (4.1.42) | goRa (?jAnapadAdi) → NIz → गोणी |
| SoRI | f | SK501 (4.1.43) | SoRa (?SoRa) → optional NIz → शोणी / शोणा (both forks) |
| mfdvI | f | SK502 (4.1.44) | mfdu (?guRavacana, u-final) → optional NIz → मृद्वी / मृदुः (both forks) |
| laGvI | f | SK502 (4.1.44) | laGu (?guRavacana, u-final) → optional NIz → लघ्वी / लघुः (both forks) |
| bahvI | f | SK503 (4.1.45) | bahu (?bahvAdi, u-final) → optional NIz → बह्वी / बहुः (both forks) |
| gopI | f | SK504 (4.1.48) | gopa (?puMyoga) → NIz → गोपी |
| tuNgakarRA | f | SK511 (4.1.55) — lp:?samAsa | [as_purva_pada(tuNga), luk_sup, in_compound(karRa), strI_abs]; refactored to `lp: ?samAsa` → optional NIz → तुङ्गकर्णी / तुङ्गकर्णा (both forks) |
| vastrakrItI | f | SK506 (4.1.50) — llp:?karaNa | [as_purva_pada(vastra), luk_sup, in_compound(krIta), strI_abs] → वस्त्रक्रीती (mandatory ṅīṣ) |
| aBraliptI | f | SK507 (4.1.51) — llp:?karaNa | [as_purva_pada(aBra), luk_sup, in_compound(lipta), strI_abs] → अभ्रलिप्ती |
| atikeSI | f | SK510 (4.1.54) — lp svāṅga | [as_purva_pada(ati), luk_sup, in_compound(keSa), strI_abs] → अतिकेशी/अतिकेशा (both forks) |
| candramuKI | f | SK510 (4.1.54) | [as_purva_pada(candra), luk_sup, in_compound(muKa), strI_abs] → चन्द्रमुखी/चन्द्रमुखा |
| suguláA | f | SK510 counter — conjunct upadhā | [as_purva_pada(su_pUrva), luk_sup, in_compound(gulPa), strI_abs]: $$asaMyogopaDa False → ṭāp only सुगुल्फा |
| kalyARakroqA | f | SK512 (4.1.56) — kroḍādi block | [as_purva_pada(kalyARa), luk_sup, in_compound(kroqa), strI_abs] → ṭāp only कल्याणक्रोडा |
| sujaGanA | f | SK512 (4.1.56) — bahvac block | [as_purva_pada(su_pUrva), luk_sup, in_compound(jaGana), strI_abs]: $$bahvac → ṭāp only सुजघना |
| sakeSA | f | SK513 (4.1.57) — saha-pūrva block | [as_purva_pada(sa_pUrva), luk_sup, in_compound(keSa), strI_abs]: llp=sa → ṭāp only सकेशा |
| SUrpaRaKA | f | SK514 (4.1.58) — nakha saṃjñā block | [as_purva_pada(SUrpa), luk_sup, in_context(in_compound(naKa),"saMjYA"), strI_abs] → ṭāp only शूर्पणखा. **The ण comes from SK857/8.4.3** (pūrvapada ṇatva in a saṁjñā): the fixture previously recorded शूर्प**न**खा because 8.4.3 was unimplemented, contradicting both its own stem key and this row — corrected when 8.4.3 landed. Forms the minimal pair with `SUrpanaKI` below (same members, no `saMjYA` → no ṇatva) |
| tAmramuKI | f | SK514 counter — non-saṃjñā | [as_purva_pada(tAmra), luk_sup, in_compound(muKa), strI_abs]: no ?saMjYA → SK510 ṅīṣ → ताम्रमुखी/ताम्रमुखा |
| prANmuKI | f | SK515 (4.1.60) — dik-pūrva ṅīp | [pra, luk_sup, in_context(aYc_u,"dik"), kvin, luk_sup, in_compound(muKa), strI_abs]: dik pūrva प्राच् derived live (prAc añc-paradigm), ?dik propagates to llp → ṅīp प्राङ्मुखी/प्राग्मुखी (8.4.45 optional anunāsika) |
| indrARI | f | SK505 (4.1.49) | indra (?indrAnuk): ānuk आन् + NIz + ṇatva → इन्द्राणी |
| varuRAnI | f | SK505 (4.1.49) | varuRa (?indrAnuk): ānuk + NIz, dental n (no r/ṣ) → वरुणानी |
| rudrARI | f | SK505 (4.1.49) | rudra (?indrAnuk): ānuk + NIz + ṇatva → रुद्राणी |
| himAnI | f | SK505 (4.1.49) | hima (?indrAnuk): ānuk + NIz, dental n → हिमानी |
| araRyAnI | f | SK505 (4.1.49) | araRya (?indrAnuk): ānuk + NIz; ṇ/y blocks 8.4.2 aṭ-vyavāya → dental n → अरण्यानी |
| mAtulAnI | f | SK505 (4.1.49) | mAtula (?indrAnuk): ānuk + NIz, dental n → मातुलानी |
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
| SUrpanaKI | f | ī-stem (nadī compound) | (samāsa) [as_purva_pada(SUrpa), luk_sup, in_compound(naKI)] — **NOT tagged `saMjYA`**, so SK857/8.4.3 correctly does NOT fire → शूर्प**न**खी keeps its न (SK307 negative test). The minimal pair with `SUrpaRaKA`: identical members, differing only by the `saMjYA` tag — 8.4.3's exact condition |
| kzIrapa | n | a-stem (compound) | (samāsa) [as_purva_pada(kzIra), luk_sup, in_compound(pa)]; kṣīrapa neuter a-stem |
| aDaspada | n | a-stem (compound) | (samāsa) [as_purva_pada(aDas), in_compound(pada)]; SK161 test — adhas+pada → adhaspadam |
| Siraspada | n | a-stem (compound) | (samāsa) [as_purva_pada(Siras), in_compound(pada)]; SK161 test — śiras+pada → śiraspadam |
