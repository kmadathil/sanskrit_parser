# -*- coding: utf-8 -*-
"""Test cases for समासाश्रयविधिप्रकरणम् (SK 985–1071) — samasa_asraya_plan.md.

Driver: test_samasa_asraya.py. Case shape:

    {
        "label":   "X1-<form>-SK<n>-<a.b.c>",   # dual sutra numbering (mandatory)
        "type":    "zazWI" | "karmaDAraya" | "ku" | "saha_bv",   # the formation used
        "purva":   {"stem": ..., "vibhakti": ..., "tags": [...], "sem": ...},
        "uttara":  {"stem": ..., "vacana": ..., "tags": [...]},
        "fired":   [<Ashtadhyayi ids that must appear in the pre-pass trace>],
        "not_fired": [<ids that must NOT fire — the negative controls>],
        "surface": "देवनागरी"  |  "surfaces": ["…", "…"],   # optional rules fork
    }

Kept separate from samasa_list.py (which already carries five lists) to keep both
modules readable.
"""

samasa_asraya_tests = [
    # ══════════════════════════════════════════════════════════════════════════
    # X1 — कु → कत् / का / कव (SK1027–1033 / 6.3.101–107)
    #
    # कु forms a NITYA tatpuruṣa (SK761/2.2.18 कुगतिप्रादयः) — hence type "ku": the
    # pūrva carries only a semantic sense, no vivakṣā. These rules then rewrite the
    # कु in that landed compound. SK writes कदश्वः / कद्रथः, which are the SANDHI
    # outputs of the substitute कत् (pada-final त् → द् by 8.2.39 झलां जशोऽन्ते).
    # ══════════════════════════════════════════════════════════════════════════
    {
        # कुत्सितोऽश्वः = कदश्वः — vowel-initial uttara (अचि), so कत्.
        "label": "X1-kadaSvaH-SK1027-6.3.101",
        "type": "ku",
        "purva": {"stem": "ku", "sem": "semantic_1"},
        "uttara": {"stem": "aSva", "vacana": 1},
        "fired": ["2.2.18", "6.3.101"],
        "surface": "कदश्वः",
    },
    {
        # कदन्नम् — same rule, napuṁsaka uttara (अन्न) → अम् nom sg.
        "label": "X1-kadannam-SK1027-6.3.101",
        "type": "ku",
        "purva": {"stem": "ku", "sem": "semantic_1"},
        "uttara": {"stem": "anna", "vacana": 1},
        "fired": ["2.2.18", "6.3.101"],
        "surface": "कदन्नम्",
    },
    {
        # कद्रथः — रथ is CONSONANT-initial, so 6.3.101 (अचि) cannot reach it; 6.3.102
        # supplies कत् by अनुवृत्ति. Negative control on 6.3.101 in the same case.
        "label": "X1-kadraTaH-SK1028-6.3.102",
        "type": "ku",
        "purva": {"stem": "ku", "sem": "semantic_1"},
        "uttara": {"stem": "raTa", "vacana": 1},
        "fired": ["2.2.18", "6.3.102"],
        "not_fired": ["6.3.101"],
        "surface": "कद्रथः",
    },
    {
        # कद्वदः — 6.3.102's second member.
        "label": "X1-kadvadaH-SK1028-6.3.102",
        "type": "ku",
        "purva": {"stem": "ku", "sem": "semantic_1"},
        "uttara": {"stem": "vada", "vacana": 1},
        "fired": ["2.2.18", "6.3.102"],
        "surface": "कद्वदः",
    },
    {
        # कत्तृणम् — जातौ (a species of grass). त् survives: त् before त् is not झश्,
        # so 8.2.39 jaśtva does not apply (contrast कदश्वः / कद्रथः).
        "label": "X1-kattfRam-SK1029-6.3.103",
        "type": "ku",
        "purva": {"stem": "ku", "sem": "semantic_1"},
        "uttara": {"stem": "tfRa", "vacana": 1, "tags": ["jAti"]},
        "fired": ["2.2.18", "6.3.103"],
        "surface": "कत्तृणम्",
    },
    {
        # तृणे च JĀTAU किम् — without the jāti sense 6.3.103 cannot fire. तृण is
        # consonant-initial, so no rule of this set applies → कुतृणम्.
        "label": "X1-kutfRam-negative-SK1029-6.3.103",
        "type": "ku",
        "purva": {"stem": "ku", "sem": "semantic_1"},
        "uttara": {"stem": "tfRa", "vacana": 1},
        "fired": ["2.2.18"],
        "not_fired": ["6.3.101", "6.3.102", "6.3.103"],
        "surface": "कुतृणम्",
    },
    {
        # काक्षः — अक्ष is vowel-initial, so 6.3.101 would give *कदक्षः; 6.3.104 is
        # para and overrides it. आ + अ → आ (6.1.101 अकः सवर्णे दीर्घः).
        "label": "X1-kAkzaH-SK1030-6.3.104",
        "type": "ku",
        "purva": {"stem": "ku", "sem": "semantic_1"},
        "uttara": {"stem": "akza", "vacana": 1},
        "fired": ["2.2.18", "6.3.104"],
        "not_fired": ["6.3.101"],
        "surface": "काक्षः",
    },
    {
        # ईषज्जलं = काजलम् — the ईषत् ("slight") sense, so 6.3.105's का, overriding
        # 6.3.101's कत् even though जल is consonant-initial (here 6.3.101 is
        # inapplicable anyway; the override matters for काम्लः).
        "label": "X1-kAjalam-SK1031-6.3.105",
        "type": "ku",
        "purva": {"stem": "ku", "sem": "semantic_1", "tags": ["IzadarTa"]},
        "uttara": {"stem": "jala", "vacana": 1},
        "fired": ["2.2.18", "6.3.105"],
        "surface": "काजलम्",
    },
    {
        # कापुरुषः / कुपुरुषः — विभाषा, so the pre-pass forks. This is the landed
        # T4-kupuruSaH compound (samasa_list.py) gaining its second form.
        "label": "X1-kApuruzaH-SK1032-6.3.106",
        "type": "ku",
        "purva": {"stem": "ku", "sem": "semantic_1"},
        "uttara": {"stem": "puruza", "vacana": 1},
        "fired": ["2.2.18", "6.3.106"],
        "surfaces": ["कापुरुषः", "कुपुरुषः"],
    },
    {
        # अप्राप्तविभाषा: in the ईषत् sense 6.3.105 is NITYA, so 6.3.106's vibhāṣā is
        # blocked (?!IzadarTa) and only कापुरुषः surfaces — ईषत्पुरुषः = कापुरुषः.
        "label": "X1-kApuruzaH-Izat-SK1031-6.3.105",
        "type": "ku",
        "purva": {"stem": "ku", "sem": "semantic_1", "tags": ["IzadarTa"]},
        "uttara": {"stem": "puruza", "vacana": 1},
        "fired": ["2.2.18", "6.3.105"],
        "not_fired": ["6.3.106"],
        "surface": "कापुरुषः",
    },
    {
        # कवोष्णम् / कोष्णम् — 6.3.107 is वा: the कव branch is this rule, the other
        # branch falls through to 6.3.105's का → का + उष्ण → कोष्ण (6.1.87 आद्गुणः).
        "label": "X1-kavozRam-SK1033-6.3.107",
        "type": "ku",
        "purva": {"stem": "ku", "sem": "semantic_1", "tags": ["IzadarTa"]},
        "uttara": {"stem": "uzRa", "vacana": 1},
        "fired": ["2.2.18", "6.3.107"],
        "surfaces": ["कवोष्णम्", "कोष्णम्"],
    },
    {
        # 6.3.104's OTHER member, पथिन्. The कु → का substitution fires correctly; the
        # surface is कापन्थाः rather than SK's कापथम् because the पथिन्-final compound's
        # अच् samāsānta is SK/5.4.74 ऋक्पूरब्धूःपथामानक्षे, which is a STANDING DEFERRAL
        # from the sarvasamāsānta phase (generator_status.md) — only the नञ्-scoped
        # 5.4.72 पथो विभाषा is implemented (अपथम् / अपन्थाः). So पथिन् declines natively.
        "label": "X1-kApanTAH-SK1030-6.3.104",
        "type": "ku",
        "purva": {"stem": "ku", "sem": "semantic_1"},
        "uttara": {"stem": "paTin", "vacana": 1},
        "fired": ["2.2.18", "6.3.104"],
        "surface": "कापन्थाः",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # X1 — हृदय → हृद् (SK988–989 / 6.3.50–51), पाद → पद/पत् (SK990–994 / 6.3.52–56),
    # उदक → उद (SK995–998 / 6.3.57–60). All formed as ṣaṣṭhī-tatpuruṣas
    # (SK702/2.2.8): हृदयस्य लेखः, पादस्य अजिः, उदकस्य कुम्भः.
    # ══════════════════════════════════════════════════════════════════════════
    {
        # हृदयं लिखतीति = हृल्लेखः. हृद् + लेख: द् → ल् by 8.4.60 तोर्लि.
        "label": "X1-hfllaeKaH-SK988-6.3.50",
        "type": "zazWI",
        "purva": {"stem": "hfdaya"},
        "uttara": {"stem": "leKa", "vacana": 1},
        "fired": ["2.2.8", "6.3.50"],
        "surface": "हृल्लेखः",
    },
    {
        # वा — हृद्रोगः / हृदयरोगः. The pūrva keeps its pada-hood, so 8.2.39 झलां जशोऽन्ते
        # turns the substitute's त् into द् before रोग.
        "label": "X1-hfdrogaH-SK989-6.3.51",
        "type": "zazWI",
        "purva": {"stem": "hfdaya"},
        "uttara": {"stem": "roga", "vacana": 1},
        "fired": ["2.2.8", "6.3.51"],
        "surfaces": ["हृद्रोगः", "हृदयरोगः"],
    },
    {
        # पादाभ्यामजतीति = पदाजिः. 6.3.52's substitute is the ADANTA पद, so its final अ
        # merges with अजि's initial अ → आ (6.1.101 अकः सवर्णे दीर्घः). This is exactly why
        # SK spells out "पद इत्यदन्त आदेशः" here and "पादस्य पत्" from 6.3.53 on.
        "label": "X1-padAjiH-SK990-6.3.52",
        "type": "zazWI",
        "purva": {"stem": "pAda"},
        "uttara": {"stem": "aji", "vacana": 1},
        "fired": ["2.2.8", "6.3.52"],
        "surface": "पदाजिः",
    },
    {
        # पत्काषी — the consonant-final substitute पत् (6.3.54), kept as त् before क् by
        # 8.4.55 खरि च. काषिन् is an in-stem → nom sg पत्काषी.
        "label": "X1-patkAzI-SK992-6.3.54",
        "type": "zazWI",
        "purva": {"stem": "pAda"},
        "uttara": {"stem": "kAzin", "vacana": 1},
        "fired": ["2.2.8", "6.3.54"],
        "surface": "पत्काषी",
    },
    {
        # पद्धतिः — same rule; पत् + हति → द् (8.2.39) and then the ह् OPTIONALLY assimilates
        # to the preceding jha by 8.4.62 झयो होऽन्यतरस्याम्, whose non-application branch
        # leaves पद्हतिः. That fork is pre-existing engine behaviour (cf. तज्झि / तद्हि,
        # generator_status.md SK119), not something this sūtra introduces.
        "label": "X1-paddDatiH-SK992-6.3.54",
        "type": "zazWI",
        "purva": {"stem": "pAda"},
        "uttara": {"stem": "hati", "vacana": 1},
        "fired": ["2.2.8", "6.3.54"],
        "surfaces": ["पद्धतिः", "पद्हतिः"],
    },
    {
        # वा — पद्घोषः / पादघोषः.
        "label": "X1-padGozaH-SK994-6.3.56",
        "type": "zazWI",
        "purva": {"stem": "pAda"},
        "uttara": {"stem": "Goza", "vacana": 1},
        "fired": ["2.2.8", "6.3.56"],
        "surfaces": ["पद्घोषः", "पादघोषः"],
    },
    {
        # उदमेघः — संज्ञायाम्, so ?saMjYA on the pūrva (the SK857/8.4.3 convention).
        "label": "X1-udameGaH-SK995-6.3.57",
        "type": "zazWI",
        "purva": {"stem": "udaka", "tags": ["saMjYA"]},
        "uttara": {"stem": "meGa", "vacana": 1},
        "fired": ["2.2.8", "6.3.57"],
        "surface": "उदमेघः",
    },
    {
        # संज्ञायां किम् — without the saṁjñā 6.3.57 cannot fire, and मेघ is in none of the
        # other lists → उदकमेघः.
        "label": "X1-udakameGaH-negative-SK995-6.3.57",
        "type": "zazWI",
        "purva": {"stem": "udaka"},
        "uttara": {"stem": "meGa", "vacana": 1},
        "fired": ["2.2.8"],
        "not_fired": ["6.3.57", "6.3.58", "6.3.59", "6.3.60"],
        "surface": "उदकमेघः",
    },
    {
        # उदधिर्घटः — 6.3.58's धि member; NITYA (no saṁjñā needed, unlike 6.3.57).
        "label": "X1-udaDiH-SK996-6.3.58",
        "type": "zazWI",
        "purva": {"stem": "udaka"},
        "uttara": {"stem": "Di", "vacana": 1},
        "fired": ["2.2.8", "6.3.58"],
        "surface": "उदधिः",
    },
    {
        # 6.3.58's वाहन member. SK writes उदवाहनः (masc); the generator takes the
        # compound's gender from the uttara (2.4.26) and वाहन is lexically neuter, so
        # the nom sg is उदवाहनम् — the substitution under test is unaffected.
        "label": "X1-udavAhanam-SK996-6.3.58",
        "type": "zazWI",
        "purva": {"stem": "udaka"},
        "uttara": {"stem": "vAhana", "vacana": 1},
        "fired": ["2.2.8", "6.3.58"],
        "surface": "उदवाहनम्",
    },
    {
        # अन्यतरस्याम् — उदकुम्भः / उदककुम्भः. कुम्भ opens with a SINGLE hal (क् + उ), and a
        # pot is पूरयितव्य, so both of 6.3.59's conditions hold.
        "label": "X1-udakumBaH-SK997-6.3.59",
        "type": "zazWI",
        "purva": {"stem": "udaka"},
        "uttara": {"stem": "kumBa", "vacana": 1, "tags": ["pUrayitavya"]},
        "fired": ["2.2.8", "6.3.59"],
        "surfaces": ["उदकुम्भः", "उदककुम्भः"],
    },
    {
        # एकेति किम् — स्थाली opens with TWO hal (स् + थ्), so it is not एकहलादि: उदकस्थाली.
        "label": "X1-udakasTAlI-negative-SK997-6.3.59",
        "type": "zazWI",
        "purva": {"stem": "udaka"},
        "uttara": {"stem": "sTAlI", "vacana": 1, "tags": ["pUrayitavya"]},
        "fired": ["2.2.8"],
        "not_fired": ["6.3.59"],
        "surface": "उदकस्थाली",
    },
    {
        # पूरयितव्येति किम् — a mountain is not something to be filled: उदकपर्वतः. (पर्वत IS
        # एकहलादि, so this case isolates the second condition.)
        "label": "X1-udakaparvataH-negative-SK997-6.3.59",
        "type": "zazWI",
        "purva": {"stem": "udaka"},
        "uttara": {"stem": "parvata", "vacana": 1},
        "fired": ["2.2.8"],
        "not_fired": ["6.3.59"],
        "surface": "उदकपर्वतः",
    },
    {
        # 6.3.60's च carries अन्यतरस्याम् over from 6.3.59 → उदमन्थः / उदकमन्थः.
        "label": "X1-udamanTaH-SK998-6.3.60",
        "type": "zazWI",
        "purva": {"stem": "udaka"},
        "uttara": {"stem": "manTa", "vacana": 1},
        "fired": ["2.2.8", "6.3.60"],
        "surfaces": ["उदमन्थः", "उदकमन्थः"],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # X1 — सह → स (SK1009–1011 / 6.3.78–80). Formed as the tulyayoga bahuvrīhi
    # (SK848/2.2.28), declining in the referent's liṅga (anyapadārtha). These three
    # rules are NITYA and fire in the PRE-PASS, so SK849/6.3.82's optional saha→sa
    # (main scan, `=saha` gate) can no longer see a saha pūrva → no spurious fork.
    # ══════════════════════════════════════════════════════════════════════════
    {
        # सपलाशम् — a place name, so ?saMjYA. Neuter referent.
        "label": "X1-sapalASam-SK1009-6.3.78",
        "type": "saha_bv",
        "referent_linga": "napum",
        "purva": {"stem": "saha", "tags": ["saMjYA"]},
        "uttara": {"stem": "palASa", "vacana": 1},
        "fired": ["2.2.28", "6.3.78"],
        "not_fired": ["6.3.82"],
        "surface": "सपलाशम्",
    },
    {
        # संज्ञायां किम् — without the saṁjñā this rule is silent, and the compound falls
        # back to 6.3.82's VIBHĀṢĀ → सपलाशम् / सहपलाशम् (the सहयुध्वा contrast in SK).
        # 6.3.82 is `bahiranga: 1` (main scan), so it is absent from the PRE-PASS trace
        # this level asserts on — its effect shows up at level 3, in the two surfaces.
        "label": "X1-sahapalASam-negative-SK1009-6.3.78",
        "type": "saha_bv",
        "referent_linga": "napum",
        "purva": {"stem": "saha"},
        "uttara": {"stem": "palASa", "vacana": 1},
        "fired": ["2.2.28"],
        "not_fired": ["6.3.78"],
        "surfaces": ["सपलाशम्", "सहपलाशम्"],
    },
    {
        # समुहूर्तं ज्योतिषमधीते — the ग्रन्थान्त sense (he studies astronomy up to the
        # muhūrta chapter). ?granTAntADika covers both of 6.3.79's senses.
        "label": "X1-samuhUrtam-SK1010-6.3.79",
        "type": "saha_bv",
        "referent_linga": "napum",
        "purva": {"stem": "saha", "tags": ["granTAntADika"]},
        "uttara": {"stem": "muhUrta", "vacana": 1},
        "fired": ["2.2.28", "6.3.79"],
        "not_fired": ["6.3.82"],
        "surface": "समुहूर्तम्",
    },
    {
        # सराक्षसीका निशा — the rākṣasī is अनुपाख्य (inferred, not seen). Feminine referent
        # (निशा), so the driver appends the ṭāp; the कप् is SK/5.4.154's ?kap_vivakzA.
        "label": "X1-sarAkzasIkA-SK1011-6.3.80",
        "type": "saha_bv",
        "referent_linga": "strI",
        "purva": {"stem": "saha", "tags": ["anupAKya"]},
        "uttara": {"stem": "rAkzasI", "vacana": 1, "tags": ["kap_vivakzA"]},
        "fired": ["2.2.28", "6.3.80", "5.4.154"],
        "not_fired": ["6.3.82"],
        "surface": "सराक्षसीका",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # X1 — समान → स (SK1012–1017 / 6.3.84–89) and इदम् → ईश् / किम् → की
    # (SK1018 / 6.3.90). Formed as karmadhārayas (2.1.57, समान the विशेषण).
    # ══════════════════════════════════════════════════════════════════════════
    {
        # अनु भ्राता सगर्भ्यः — छन्दसि, with the यत् taddhita the sūtra's examples all carry.
        "label": "X1-sagarByaH-SK1012-6.3.84",
        "type": "karmaDAraya",
        "purva": {"stem": "samAna", "tags": ["Candas"]},
        "uttara": {"stem": "garBa", "vacana": 1},
        "uttara_affix": "yat_t",
        "fired": ["2.1.57", "6.3.84"],
        "surface": "सगर्भ्यः",
    },
    {
        # अमूर्धादिषु किम् — मूर्धन् is explicitly excluded: समानमूर्धा (n-stem nom sg).
        "label": "X1-samAnamUrDA-negative-SK1012-6.3.84",
        "type": "karmaDAraya",
        "purva": {"stem": "samAna", "tags": ["Candas"]},
        "uttara": {"stem": "mUrDan", "vacana": 1},
        "fired": ["2.1.57"],
        "not_fired": ["6.3.84"],
        "surface": "समानमूर्धा",
    },
    {
        # सज्योतिः — 6.3.85's first member; ज्योतिस् is an s-stem, nom sg सज्योतिः. No
        # chandas restriction here (contrast 6.3.84).
        "label": "X1-sajyotiH-SK1013-6.3.85",
        "type": "karmaDAraya",
        "purva": {"stem": "samAna"},
        "uttara": {"stem": "jyotis", "vacana": 1},
        "fired": ["2.1.57", "6.3.85"],
        "surface": "सज्योतिः",
    },
    {
        # सजनपदः — 6.3.85's second member (a-stem).
        "label": "X1-sajanapadaH-SK1013-6.3.85",
        "type": "karmaDAraya",
        "purva": {"stem": "samAna"},
        "uttara": {"stem": "janapada", "vacana": 1},
        "fired": ["2.1.57", "6.3.85"],
        "surface": "सजनपदः",
    },
    {
        # समानः (चरणः) सः = सब्रह्मचारी — the sameness is one of चरण (Vedic branch).
        "label": "X1-sabrahmacArI-SK1014-6.3.86",
        "type": "karmaDAraya",
        "purva": {"stem": "samAna", "tags": ["caraRa"]},
        "uttara": {"stem": "brahmacArin", "vacana": 1},
        "fired": ["2.1.57", "6.3.86"],
        "surface": "सब्रह्मचारी",
    },
    {
        # समानतीर्थे वासी = सतीर्थ्यः. The sūtra's own condition is ये — a य-initial affix
        # being INTENDED (यादौ प्रत्यये विवक्षिते) — hence the ?tadDita_ya_para vivakṣā tag
        # plus the physical यत्. तीर्थ is neuter but the derivative denotes a person, so the
        # case overrides the liṅga to masc (see _build_one's "linga").
        "label": "X1-satIrTyaH-SK1015-6.3.87",
        "type": "karmaDAraya",
        "purva": {"stem": "samAna"},
        "uttara": {"stem": "tIrTa", "vacana": 1, "linga": "pum",
                   "tags": ["tadDita_ya_para"]},
        "uttara_affix": "yat_t",
        "fired": ["2.1.57", "6.3.87"],
        "surface": "सतीर्थ्यः",
    },
    {
        # ये किम् — without a य-initial affix intended, 6.3.87 cannot fire → समानतीर्थम्.
        "label": "X1-samAnatIrTam-negative-SK1015-6.3.87",
        "type": "karmaDAraya",
        "purva": {"stem": "samAna"},
        "uttara": {"stem": "tIrTa", "vacana": 1},
        "fired": ["2.1.57"],
        "not_fired": ["6.3.87"],
        "surface": "समानतीर्थम्",
    },
    {
        # विभाषा — सोदर्यः / समानोदर्यः. Each fork additionally doubles the य after र् by
        # 8.4.46 अचो रहाभ्यां द्वे (a landed optional rule), so four surfaces in all.
        "label": "X1-sodaryaH-SK1016-6.3.88",
        "type": "karmaDAraya",
        "purva": {"stem": "samAna"},
        "uttara": {"stem": "udara", "vacana": 1, "linga": "pum",
                   "tags": ["tadDita_ya_para"]},
        "uttara_affix": "yat_t",
        "fired": ["2.1.57", "6.3.88"],
        "surfaces": ["सोदर्यः", "सोदर्य्यः", "समानोदर्यः", "समानोदर्य्यः"],
    },
    {
        # सदृशः — 6.3.89's दृश (a-stem) member.
        "label": "X1-sadfSaH-SK1017-6.3.89",
        "type": "karmaDAraya",
        "purva": {"stem": "samAna"},
        "uttara": {"stem": "dfSa", "vacana": 1},
        "fired": ["2.1.57", "6.3.89"],
        "surface": "सदृशः",
    },
    {
        # ईदृशः — इदम् → ईश्, a शित् substitute, so 1.1.55 अनेकाल्शित्सर्वस्य replaces the
        # WHOLE pronoun (इदम् → ई), not just its final phoneme.
        "label": "X1-IdfSaH-SK1018-6.3.90",
        "type": "karmaDAraya",
        "purva": {"stem": "idam"},
        "uttara": {"stem": "dfSa", "vacana": 1},
        "fired": ["2.1.57", "6.3.90"],
        "surface": "ईदृशः",
    },
    {
        # कीदृशः — the किमः की arm of the same sūtra (rule id 6.3.90.1).
        "label": "X1-kIdfSaH-SK1018-6.3.90",
        "type": "karmaDAraya",
        "purva": {"stem": "kim"},
        "uttara": {"stem": "dfSa", "vacana": 1},
        "fired": ["2.1.57", "6.3.90.1"],
        "surface": "कीदृशः",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # X1 — अन्य + दुक् (SK1025–1026 / 6.3.99–100). दुक् is an AUGMENT (क्-it → 1.1.46
    # आद्यन्तौ टकितौ attaches it at the end) → अन्य + द् = अन्यद्.
    # ══════════════════════════════════════════════════════════════════════════
    {
        # अन्यद्रागः — राग is in 6.3.99's list. The द् of the augment is retained before र्.
        "label": "X1-anyadrAgaH-SK1025-6.3.99",
        "type": "karmaDAraya",
        "purva": {"stem": "anya"},
        "uttara": {"stem": "rAga", "vacana": 1},
        "fired": ["2.1.57", "6.3.99"],
        "surface": "अन्यद्रागः",
    },
    {
        # अन्यदुत्सुकः — the उत्सुक member (उत्सुक already exists as a stem, ?prasitotsuka).
        "label": "X1-anyadutsukaH-SK1025-6.3.99",
        "type": "karmaDAraya",
        "purva": {"stem": "anya"},
        "uttara": {"stem": "utsuka", "vacana": 1},
        "fired": ["2.1.57", "6.3.99"],
        "surface": "अन्यदुत्सुकः",
    },
    {
        # अषष्ठ्यतृतीयास्थस्य किम् — with अन्य in the ṢAṢṬHĪ (अन्यस्य रागः) there is no दुक्:
        # अन्यरागः. (SK's own contrast is अन्यस्य/अन्येन आशीः = अन्याशीः.)
        "label": "X1-anyarAgaH-negative-SK1025-6.3.99",
        "type": "zazWI",
        "purva": {"stem": "anya"},
        "uttara": {"stem": "rAga", "vacana": 1},
        "fired": ["2.2.8"],
        "not_fired": ["6.3.99"],
        "surface": "अन्यरागः",
    },
    {
        # विभाषा — अन्यदर्थः / अन्यार्थः.
        "label": "X1-anyadarTaH-SK1026-6.3.100",
        "type": "karmaDAraya",
        "purva": {"stem": "anya"},
        "uttara": {"stem": "arTa", "vacana": 1},
        "fired": ["2.1.57", "6.3.100"],
        "surfaces": ["अन्यदर्थः", "अन्यार्थः"],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # X2 — PŪRVAPADA HRASVA of a ङी / आप् pūrva (SK985–1006 / 6.3.43–65).
    #
    # Same lever as X1, opposite operation: `l: hrasva(l)` instead of a whole-stem
    # rewrite. The ङी/आप् distinction rides on the existing ?NI / ?Ap stem tags.
    # Formed as ṣaṣṭhī-tatpuruṣas, except SK1002/6.3.64 which is not a compound at
    # all (see its case). SK986/6.3.44 + SK987/6.3.45 are Skipped rows — every
    # example SK gives for them is a तरप् (affix) context.
    # ══════════════════════════════════════════════════════════════════════════
    {
        # ब्राह्मणी + गोत्र = ब्राह्मणिगोत्रम्. Three conditions all hold: ब्राह्मणी is ङी-final
        # (?NI), भाषितपुंस्क (?puMvat — it has the masc ब्राह्मण), and अनेकाच्.
        "label": "X2-brAhmaRigotram-SK985-6.3.43",
        "type": "zazWI",
        "purva": {"stem": "brAhmaRI"},
        "uttara": {"stem": "gotra", "vacana": 1},
        "fired": ["2.2.8", "6.3.43"],
        "surface": "ब्राह्मणिगोत्रम्",
    },
    {
        # ब्राह्मणिब्रुवः — the ब्रुव member of the same list.
        "label": "X2-brAhmaRibruvaH-SK985-6.3.43",
        "type": "zazWI",
        "purva": {"stem": "brAhmaRI"},
        "uttara": {"stem": "bruva", "vacana": 1},
        "fired": ["2.2.8", "6.3.43"],
        "surface": "ब्राह्मणिब्रुवः",
    },
    {
        # ब्राह्मणिमतः — the मत member. (मत/हत are ordinary a-stems, so these two arms
        # cost nothing beyond the alternation.)
        "label": "X2-brAhmaRimataH-SK985-6.3.43",
        "type": "zazWI",
        "purva": {"stem": "brAhmaRI"},
        "uttara": {"stem": "mata", "vacana": 1},
        "fired": ["2.2.8", "6.3.43"],
        "surface": "ब्राह्मणिमतः",
    },
    {
        # चेलडादिषु किम् — पुत्र is in none of 6.3.43's lists, so the ङी stays long:
        # ब्राह्मणीपुत्रः. Also a negative control on 6.3.61, which cannot reach a
        # ङी-final pūrva (अङ्यः).
        "label": "X2-brAhmaRIputraH-negative-SK985-6.3.43",
        "type": "zazWI",
        "purva": {"stem": "brAhmaRI"},
        "uttara": {"stem": "putra", "vacana": 1},
        "fired": ["2.2.8"],
        "not_fired": ["6.3.43", "6.3.61"],
        "surface": "ब्राह्मणीपुत्रः",
    },
    {
        # अन्यतरस्याम् — ग्रामणिपुत्रः / ग्रामणीपुत्रः. ग्रामणी is इक्-final (ī) but NOT
        # ङी-formed — it is a क्विप् derivation (ग्रामं नयति), so 6.3.61 reaches it.
        "label": "X2-grAmaRiputraH-SK999-6.3.61",
        "type": "zazWI",
        "purva": {"stem": "grAmaRI", "tags": ["gAlava_hrasva"]},
        "uttara": {"stem": "putra", "vacana": 1},
        "fired": ["2.2.8", "6.3.61"],
        "surfaces": ["ग्रामणिपुत्रः", "ग्रामणीपुत्रः"],
    },
    {
        # अङ्यः किम् — गौरी IS ङी-formed, so 6.3.61 is blocked: गौरीपुत्रः stays long.
        # (SK's own example is गौरीपतिः.)
        "label": "X2-gOrIputraH-negative-SK999-6.3.61",
        "type": "zazWI",
        "purva": {"stem": "gOrI", "tags": ["gAlava_hrasva"]},
        "uttara": {"stem": "putra", "vacana": 1},
        "fired": ["2.2.8"],
        "not_fired": ["6.3.61"],
        "surface": "गौरीपुत्रः",
    },
    {
        # A SHORT इक् final has no hrasva, so 6.3.61 must not fire on हरि — otherwise this
        # vibhāṣā would fork every i-final pūrva in the language for no change in surface.
        # This is what `$$ik_dIrGa_anekAc` guards (see paribhasha.py).
        "label": "X2-hariputraH-negative-SK999-6.3.61-hrasva",
        "type": "zazWI",
        "purva": {"stem": "hari", "tags": ["gAlava_hrasva"]},
        "uttara": {"stem": "putra", "vacana": 1},
        "fired": ["2.2.8"],
        "not_fired": ["6.3.61"],
        "surface": "हरिपुत्रः",
    },
    {
        # The sūtra's own vārtika इयङुवङ्भाविनामव्ययानां च न — श्री is monosyllabic (एकाच्), so
        # it keeps its ī: श्रीपुत्रः (SK's example is श्रीमदः). The अनेकाच् half of the helper.
        "label": "X2-SrIputraH-negative-SK999-6.3.61-ekAc",
        "type": "zazWI",
        "purva": {"stem": "SrI", "tags": ["gAlava_hrasva"]},
        "uttara": {"stem": "putra", "vacana": 1},
        "fired": ["2.2.8"],
        "not_fired": ["6.3.61"],
        "surface": "श्रीपुत्रः",
    },
    {
        # एकक्षीरम् — एका → एक before an uttarapada. NITYA (no अन्यतरस्याम् in 6.3.62), so a
        # single surface. The taddhita arm (एकरूप्यम्) is not modelled.
        "label": "X2-ekakzIram-SK1000-6.3.62",
        "type": "zazWI",
        "purva": {"stem": "ekA"},
        "uttara": {"stem": "kzIra", "vacana": 1},
        "fired": ["2.2.8", "6.3.62"],
        "surface": "एकक्षीरम्",
    },
    {
        # बहुलम् → optional. रेवती (a NAME, so ?saMjYA) + पुत्र = रेवतिपुत्रः / रेवतीपुत्रः.
        # The ङी arm of 6.3.63.
        "label": "X2-revatiputraH-SK1001-6.3.63",
        "type": "zazWI",
        "purva": {"stem": "revatI", "tags": ["saMjYA"]},
        "uttara": {"stem": "putra", "vacana": 1},
        "fired": ["2.2.8", "6.3.63"],
        "surfaces": ["रेवतिपुत्रः", "रेवतीपुत्रः"],
    },
    {
        # The आप् arm of 6.3.63: अजा + क्षीर = अजक्षीरम् / अजाक्षीरम्.
        "label": "X2-ajakzIram-SK1001-6.3.63",
        "type": "zazWI",
        "purva": {"stem": "ajA", "tags": ["saMjYA"]},
        "uttara": {"stem": "kzIra", "vacana": 1},
        "fired": ["2.2.8", "6.3.63"],
        "surfaces": ["अजक्षीरम्", "अजाक्षीरम्"],
    },
    {
        # संज्ञाछन्दसोः किम् — without ?saMjYA or ?Candas, 6.3.63 is silent: अजाक्षीरम्.
        "label": "X2-ajAkzIram-negative-SK1001-6.3.63",
        "type": "zazWI",
        "purva": {"stem": "ajA"},
        "uttara": {"stem": "kzIra", "vacana": 1},
        "fired": ["2.2.8"],
        "not_fired": ["6.3.63"],
        "surface": "अजाक्षीरम्",
    },
    {
        # अजत्वम् / अजात्वम् — NOT a compound: this is stem + the त्व taddhita, so the rule is
        # a MAIN-SCAN rule at the (अजा | त्व) window and is therefore absent from the
        # pre-pass trace (hence `fired: []`, as for 6.3.82 in X1). The sup is supplied
        # explicitly because automatic sup insertion lives in the kāraka pre-pass, which a
        # bare stem+taddhita derivation never enters. ?napum rides on the AFFIX — a
        # त्व-derivative is neuter whatever it is built on.
        "label": "X2-ajatvam-SK1002-6.3.64",
        "type": "affix",
        "purva": {"stem": "ajA"},
        "uttara_affix": "tva_t",
        "sup": [1, 1],
        "fired": [],
        "surfaces": ["अजत्वम्", "अजात्वम्"],
    },
    {
        # The ङी arm of 6.3.64: रोहिणी + त्व = रोहिणित्वम् / रोहिणीत्वम्.
        "label": "X2-rohiRitvam-SK1002-6.3.64",
        "type": "affix",
        "purva": {"stem": "rohiRI"},
        "uttara_affix": "tva_t",
        "sup": [1, 1],
        "fired": [],
        "surfaces": ["रोहिणित्वम्", "रोहिणीत्वम्"],
    },
    {
        # 6.3.65's first ordered pair (क्रमात्): इष्टका–चित → इष्टकचितम्.
        "label": "X2-izwakacitam-SK1006-6.3.65",
        "type": "zazWI",
        "purva": {"stem": "izwakA"},
        "uttara": {"stem": "cita", "vacana": 1},
        "fired": ["2.2.8", "6.3.65"],
        "surface": "इष्टकचितम्",
    },
    {
        # Second pair: इषीका–तूल → इषीकतूलम्.
        "label": "X2-izIkatUlam-SK1006-6.3.65",
        "type": "zazWI",
        "purva": {"stem": "izIkA"},
        "uttara": {"stem": "tUla", "vacana": 1},
        "fired": ["2.2.8", "6.3.65"],
        "surface": "इषीकतूलम्",
    },
    {
        # Third pair: माला–भारिन् → मालभारि (भारिन् is an in-stem, napuṁsaka nom sg).
        "label": "X2-mAlaBAri-SK1006-6.3.65",
        "type": "zazWI",
        "purva": {"stem": "mAlA"},
        "uttara": {"stem": "BArin", "vacana": 1},
        "fired": ["2.2.8", "6.3.65"],
        "surface": "मालभारि",
    },
    {
        # क्रमात् is load-bearing: the pairs are ORDERED, so इष्टका before तूल gets no hrasva
        # (इष्टकातूलम्). A single `or` over both lists would wrongly license *इष्टकतूलम् —
        # which is why 6.3.65 is written as three separate arms.
        "label": "X2-izwakAtUlam-negative-SK1006-6.3.65",
        "type": "zazWI",
        "purva": {"stem": "izwakA"},
        "uttara": {"stem": "tUla", "vacana": 1},
        "fired": ["2.2.8"],
        "not_fired": ["6.3.65"],
        "surface": "इष्टकातूलम्",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # X3 — the मुम् AUGMENT (SK1007–1008 / 6.3.70, 6.3.72).
    #
    # मुम् is मित्, so 1.1.47 मिदचोऽन्त्यात्परः puts it after the pūrva's last vowel — an
    # append, for these vowel-final pūrvas. Every surface below carries an extra fork
    # from 8.4.59 वा पदान्तस्य, which makes the parasavarṇa of 8.4.58 optional at a pada
    # boundary: so the anusvāra spelling stands beside SK's class-nasal one.
    # ══════════════════════════════════════════════════════════════════════════
    {
        # सत्यङ्कारः — मुम् gives सत्यम्, then 8.3.23 मोऽनुस्वारः + 8.4.58 परसवर्णः give ङ्.
        # सत्यंकारः is 8.4.59's non-parasavarṇa branch.
        "label": "X3-satyaNkAraH-SK1007-6.3.70",
        "type": "zazWI",
        "purva": {"stem": "satya"},
        "uttara": {"stem": "kAra", "vacana": 1},
        "fired": ["2.2.8", "6.3.70"],
        "surfaces": ["सत्यङ्कारः", "सत्यंकारः"],
    },
    {
        # अगदङ्कारः — 6.3.70's second pūrva.
        "label": "X3-agadaNkAraH-SK1007-6.3.70",
        "type": "zazWI",
        "purva": {"stem": "agada"},
        "uttara": {"stem": "kAra", "vacana": 1},
        "fired": ["2.2.8", "6.3.70"],
        "surfaces": ["अगदङ्कारः", "अगदंकारः"],
    },
    {
        # कारे किम् — before anything but कार, सत्य takes no मुम्: सत्यक्षीरम्.
        "label": "X3-satyakzIram-negative-SK1007-6.3.70",
        "type": "zazWI",
        "purva": {"stem": "satya"},
        "uttara": {"stem": "kzIra", "vacana": 1},
        "fired": ["2.2.8"],
        "not_fired": ["6.3.70"],
        "surface": "सत्यक्षीरम्",
    },
    {
        # विभाषा — रात्रिञ्चरः / रात्रिचरः (SK's two forms), plus रात्रिंचरः from 8.4.59.
        # चर carries ?krt, which is the sūtra's own कृति condition.
        "label": "X3-rAtriYcaraH-SK1008-6.3.72",
        "type": "zazWI",
        "purva": {"stem": "rAtri"},
        "uttara": {"stem": "cara", "vacana": 1},
        "fired": ["2.2.8", "6.3.72"],
        "surfaces": ["रात्रिञ्चरः", "रात्रिंचरः", "रात्रिचरः"],
    },
    {
        # कृति किम् — पुत्र is not a कृदन्त, so no मुम्: रात्रिपुत्रः.
        "label": "X3-rAtriputraH-negative-SK1008-6.3.72",
        "type": "zazWI",
        "purva": {"stem": "rAtri"},
        "uttara": {"stem": "putra", "vacana": 1},
        "fired": ["2.2.8"],
        "not_fired": ["6.3.72"],
        "surface": "रात्रिपुत्रः",
    },
]
