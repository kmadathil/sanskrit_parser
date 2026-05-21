"""
Sanskrit Generator Web UI
=========================
Single-page Flask app that lets you browse the declension tables produced by
the Paninian grammar engine.

Run from the worktree root:
    PYTHONPATH=. python sanskrit_parser/generator/ui/app.py
Then open http://localhost:5001
"""

import io
import logging
from contextlib import redirect_stdout

from flask import Flask, jsonify, render_template, request
from indic_transliteration import sanscript

# Suppress noisy loggers before importing generator modules
logging.getLogger().addHandler(logging.NullHandler())

from sanskrit_parser.generator.pratipadika import (     # noqa: E402
    rAma, ramA, jYAna, mahat, mahat_n, payas,
    kavi, hari, pati, saKi, mati, vAri,
    nadI, lakzmI, strI,
    SamBu, krozwu, Denu, vasu_pum, BrU, svayamBU,
    pitf, nf, mAtf, svasf, tisf, tvazwf,
    go, rE,
    rAjan, pUzan, yajvan, parvan_napum,
    svan, yuvan, maGavan, arvan,
    hastin, yogin,
    paTin, maTin, fBukzin,
    vftra, as_purva_pada,
    asTi, daDi, akzi,
    kim, idam, idam_anu, yuzmad, asmad,
    sarva, anya,
    div_kvip, lih_kvip, duh_kvip, druh_kvip, anaquh, senAnI, turAsAh,
    nI, SrI, SrIpA,
    varzABU, dfnBU, karaBU, punarBU, KalapU,
    suDI, praDI, atistri,
    viSvapA, hAhA,
    nAsikA, niSA,
    pAda, yUza,
    ftvij_kvin, sraj_kvin, yuj_kvin, yuj_kvin_samAsa, diS_kvin,
    daDfc_kvin, udac_kvin, tiryac_kvin,
    takz_kvip, vAh_kvip, praSAm_kvip,
    gaRa, aSva, viSva, rAj_kvip,
    in_compound,
    tri, dvi, dvi_s, catur, kati,
    paYcan, saptan, navan, daSan, azwan, catasf,
    atinO,
    Sreyas, Sreyas_n,
    # New imports
    upAnah, dhImat, gomat,
    jakzat, jAgrat, daridrat, cakAsat, SAsat, dIDyat, vevyat, dadat_napum,
    Bavat, Bavat_u, pacat,
    Danus, ahan, vidvas, pums,
    tad, etad, yad, tyad, adas,
    naS_kvip, idam_strI, dfkza,
    in_context,
    pra, prati, tiras, ud, sam, saha,
    ap,
    pacat_strI, dIvyat_strI, tudat_strI, BAt_strI,
    pacat_napum, dIvyat_napum, tudat_napum,
    dvitIya, tftIya,
    vizvag,
    SUrpa, naKI,
    kzIra, pa,
    Gfta,
    aDas, Siras, pada,
    # SK454-462 strī-pratyaya stems
    aja, kokila, SUdra, kruYc, uzRih,
    sIman, bahuyajvan, bahu, pAd_ut,
    # SK463 ka-pratyaya stem (asuwapaH demo) + raw pieces (bahuvrIhi propagation)
    parivrAjaka, pari, vrAja,
)
from sanskrit_parser.generator.pratyaya import (  # noqa: E402
    avasAna, sups, su, kvin, kvip, kaY, vatup, NIp, NIz, Ap, luk_sup, Adya,
    tfc, GaY, kta, ktvA, yat, Ryat, anIya, wac, kanin,
    pASap, kalpap, kap, kAmyac, suc,
    Si, OS, adaq,
    # tiN verbal endings
    tip, sip,
    # vikaraṇa / ṇic
    Sap, yak, Ric,
    # upasargas
    AN_upasarga, mAN_upasarga, upa_upasarga, pra_upasarga,
    ava_upasarga, ud_upasarga, ati_upasarga,
    # gender / number markers
    pum_abs, napum_abs, strI_abs,
    # taddhita from prātipadika
    yat_t, zyaY_t, yaY_t, aR_t,
    # ka-pratyaya taddhita (SK463/464)
    kan,
    # van-class kṛt
    vanip,
    # luk / UW
    luk, UW,
)
from sanskrit_parser.generator.dhatu import (  # noqa: E402
    dfS, aYc_u, han, spfS,
    BU, iR, sTA, ji, vid, kzI, lUY, vah, duh, mud, Cad, Sam,
    eDa, fcCa, gfj, guhU, qukrIY, qulaBaz, veY, veY_smp, as_dhatu,
    Sf,
)
from sanskrit_parser.generator.sutras_yaml import SutraFactory          # noqa: E402
from sanskrit_parser.generator.prakriya_factory import PrakriyaFactory  # noqa: E402
from sanskrit_parser.generator.prakriya import PrakriyaVakya            # noqa: E402
from sanskrit_parser.generator.antaranga_prakriya import AntarangaPrakriya  # noqa: E402
from sanskrit_parser.generator.paninian_object import PaninianObject        # noqa: E402

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = Flask(__name__)

# Load sutra list once at startup (expensive)
sutra_list = SutraFactory("sutras_antaranga.yaml")

# ---------------------------------------------------------------------------
# Stem catalogue
# ---------------------------------------------------------------------------
# Each entry: (key, pratipadika_obj, group_label, display_name)
#
# key          → used as ?stem= query parameter
# pratipadika  → Pratipadika object (or list [prefix..., pratipadika])
# group_label  → <optgroup> label in the dropdown
# display_name → human-readable label shown in the dropdown

# Pre-built compound pratipadika lists: [pūrva-pada, in_compound(uttara-pada)]
# in_compound() deep-copies so each UI request gets a fresh object.
_gaRapati_cpd  = [gaRa,  in_compound(pati)]      # SK257 gaṇapati
_aSvayuj_cpd   = [aSva,  in_compound(yuj_kvin)]  # SK376 aśvayuj
_viSvAvasu_cpd = [viSva, in_compound(vasu_pum)]  # SK379 viśvāvasu
_viSvArAj_cpd  = [viSva, in_compound(rAj_kvip)]  # SK379 viśvārāj
_praVAh_cpd    = [pra,   vAh_kvip]               # pravāh (upasarga + √vāh+kvip)

# SK429/SK430 — tādṛk/yādṛk compounds (tyadAdi + dṛś + kvin/kaY)
_tAdfk_cpd     = [tad, luk_sup, in_compound(dfS), kvin]
_yAdfk_cpd     = [yad, su, in_compound(dfS), kvin]
_tAdfSa_cpd    = [tad, luk_sup, in_compound(dfS), in_context(kaY, "pum")]
_yAdfSa_cpd    = [yad, su, in_compound(dfS), in_context(kaY, "pum")]
_tAdfkza_cpd   = [tad, luk_sup, in_compound(dfkza)]
_yAdfkza_cpd   = [yad, su, in_compound(dfkza)]

# SK430 vatup arm — measure stems
_tAvat_n_cpd   = [tad, in_context(vatup, "napum")]
_yAvat_n_cpd   = [yad, in_context(vatup, "napum")]
_etAvat_n_cpd  = [etad, in_context(vatup, "napum")]
_tAvAn_cpd     = [tad, in_context(vatup, "pum")]
_yAvAn_cpd     = [yad, in_context(vatup, "pum")]
_etAvAn_cpd    = [etad, in_context(vatup, "pum")]

# añcatir compounds (prefix + aYc + kvin); upasargas take su (deleted by SK452)
_pratyac_cpd   = [prati, su, aYc_u, kvin]
_prAc_cpd      = [pra,   su, aYc_u, kvin]
_udac_cpd      = [ud,    su, in_context(aYc_u, "udanc"), kvin]
_tiryac_cpd    = [tiras, su, aYc_u, kvin]
_samyac_cpd    = [sam,   su, aYc_u, kvin]
_saDryac_cpd   = [saha,  su, aYc_u, kvin]

# vṛtrahān — dynamic compound (as_purva_pada = in_context(·, "samAsaPurva"))
_vftrahan_cpd  = [as_purva_pada(vftra), luk_sup, in_compound(han), kvip]

# Ordinal (dvitīyādi) feminine compounds
_dvitIyA_cpd   = [dvitIya, Ap]
_tftIyA_cpd    = [tftIya,  Ap]

# viśvadryañc — viśvag + añc + kvin
_vizvadryac_cpd = [vizvag, luk_sup, in_context(aYc_u, "aYc"), kvin]

# Luk-sup compounds (pūrva-pada with empty sup)
_SUrpanaKI_cpd = [as_purva_pada(SUrpa), luk_sup, in_compound(naKI)]
_kzIrapa_cpd   = [as_purva_pada(kzIra), luk_sup, in_compound(pa)]

# ghṛtaspṛk — SK432 (8.2.76): upadhā-dīrgha for spṛś+kvin
_Gftaspfk_cpd  = [Gfta, in_compound(spfS), kvin]

# pada-compounds — SK161 (8.3.47): visarjanīya → s before any pada-form
_aDaspada_cpd  = [as_purva_pada(aDas), in_compound(pada)]
_Siraspada_cpd = [as_purva_pada(Siras), in_compound(pada)]

# Feminine śatṛ-stems (with NI-p pratyaya)
_pacat_strI_cpd  = [pacat_strI,  NIp]
_dIvyat_strI_cpd = [dIvyat_strI, NIp]
_tudat_strI_cpd  = [tudat_strI,  NIp]
_BAt_strI_cpd    = [BAt_strI,    NIp]

# SK454-462 — strI-pratyaya (strI_abs) flow demonstrations
_rAma_A_cpd   = [rAma,  strI_abs]   # SK454: a-final → Ap → rāmā
_pacat_NI_cpd = [pacat, strI_abs]   # SK455: f-it ugit → NIp → pacantī
_aja_A_cpd    = [aja,    strI_abs]  # SK454 ajādi → TAp → ajā
_kokila_A_cpd = [kokila, strI_abs]  # SK454 ajādi → TAp → kokilā
_SUdra_A_cpd  = [SUdra,  strI_abs]  # SK454 ajādi → TAp → śūdrā
_kruYc_A_cpd  = [kruYc,  strI_abs]  # SK454 ajādi (consonant-final)
_uzRih_A_cpd  = [uzRih,  strI_abs]  # SK454 ajādi (consonant-final)
_tad_strI_cpd  = [tad,  strI_abs]   # SK454 tyadādi feminine
_etad_strI_cpd = [etad, strI_abs]
_yad_strI_cpd  = [yad,  strI_abs]
_kim_strI_cpd  = [kim,  strI_abs]
_adas_strI_cpd = [adas, strI_abs]
_Bavat_uNI_cpd = [Bavat_u, strI_abs]        # SK455 u-it → NIp → bhavatī
_Sf_vanip_strI_cpd = [Sf, vanip, strI_abs]  # SK456 (4.1.7 vano ra ca): van → NIp + n→r
_sIman_strI_cpd      = [sIman,      strI_abs]  # SK459 (4.1.11 manaH): man-final, ṅīp blocked
_bahuyajvan_strI_cpd = [bahuyajvan, strI_abs]  # SK460/461 an-bahuvrīhi
# SK457 — dvipād (dvi + pād) feminine compound
_dvipAd_strI_cpd = [as_purva_pada(dvi), luk_sup, in_compound(pAd_ut), strI_abs]
# SK462 — bahurājan (bahu + rājan) an-final upadhālopin bahuvrīhi feminine
_bahurAjan_strI_cpd = [as_purva_pada(bahu), luk_sup,
                       in_context(in_compound(rAjan), "bahuvrIhi"), strI_abs]
# SK463/464 — ka-pratyaya idādeśa demos
_sarvika_cpd   = [sarva, kan, strI_abs]  # SK463 idādeśa fires → sarvika
_yaka_strI_cpd = [yad,   kan, strI_abs]  # SK464 blocks SK463 → yakā
_saka_strI_cpd = [tad,   kan, strI_abs]  # SK464 blocks; nom sg sakā (7.2.106)
_parivrAjaka_strI_cpd = [parivrAjaka, strI_abs]  # SK463 fires → parivrājikā
# SK463 asuwapaH, RAW derivation (bahu+pari+vrAja+kap): ?bahuvrIhi propagates
# through the vrAja+kap merge → ?!bahuvrIhi guard blocks → bahuparivrājakā.
_bahuparivrAjaka_strI_cpd = [as_purva_pada(bahu), as_purva_pada(pari), luk_sup,
                             in_context(in_compound(vrAja), "bahuvrIhi"),
                             kap, strI_abs]

_STEMS_RAW = [
    # ── a / ā stems ───────────────────────────────────────────────────────
    ("rAma",     rAma,        "a-stems (pum)",    "rāma  (rāma-)"),
    ("pAda",     pAda,        "a-stems (pum)",    "pāda  (pāda-)  [pādādi opt]"),
    ("yUza",     yUza,        "a-stems (pum)",    "yūṣa  (yūṣa-)  [pādādi opt]"),
    ("gaRa",     gaRa,        "a-stems (pum)",    "gaṇa  (gaṇa-)"),
    ("aSva",     aSva,        "a-stems (pum)",    "aśva  (aśva-)"),
    ("viSva",    viSva,       "a-stems (pum)",    "viśva  (viśva-)"),
    ("vftra",    vftra,       "a-stems (pum)",    "vṛtra  (vṛtra-)"),
    ("SUrpa",    SUrpa,       "a-stems (pum)",    "śūrpa  (śūrpa-)"),
    ("jYAna",    jYAna,       "a-stems (napum)",  "jñāna  (jñāna-)"),
    ("Gfta",     Gfta,        "a-stems (napum)",  "ghṛta  (ghṛta-)"),
    ("kzIra",    kzIra,       "a-stems (napum)",  "kṣīra  (kṣīra-)"),
    ("ramA",     ramA,        "ā-stems (strī)",   "ramā  (ramā-)"),
    ("nAsikA",   nAsikA,      "ā-stems (strī)",   "nāsikā  (nāsikā-)  [pādādi]"),
    ("niSA",     niSA,        "ā-stems (strī)",   "niśā  (niśā-)  [pādādi]"),
    ("mahat",    mahat,       "t-stems",          "mahat  (mahat-)"),
    ("mahat_n",  mahat_n,     "t-stems",          "mahat  (mahat-)  [napum]"),
    ("payas",    payas,       "s-stems",          "payas  (payas-)"),
    ("Siras",    Siras,       "s-stems",          "śiras  (śiras-)"),

    # ── matup-stems (SK425 u-it) ─────────────────────────────────────────────
    ("dhImat",   dhImat,      "matup-stems",      "dhīmat  (dhīmat-)  [SK425 u-it]"),
    ("gomat",    gomat,       "matup-stems",      "gomat  (gomat-)  [SK425 u-it]"),

    # ── śatṛ-stems ─────────────────────────────────────────────────────────
    ("jakzat",    jakzat,      "śatṛ-stems (abhyasta)", "jakṣat  (jakṣat-)  [SK428 abhyasta]"),
    ("jAgrat",    jAgrat,      "śatṛ-stems (abhyasta)", "jāgrat  (jāgrat-)  [SK428 abhyasta]"),
    ("dadat_napum", dadat_napum, "śatṛ-stems (abhyasta napum)", "dadat  (dadat-)  [SK444 opt nUM]"),
    ("Bavat",    Bavat,       "śatṛ-stems (regular)",  "bhavat  (bhavant-)  [SK361 nUM]"),
    ("Bavat_u",  Bavat_u,     "śatṛ-stems (u-it)",     "bhavat  (bhavat-)  [SK425 u-it]"),
    ("pacat",    pacat,       "śatṛ-stems (regular)",  "pacat  (pacant-)  [SK361 nUM]"),
    ("pacat_napum",  pacat_napum,      "śatṛ-stems (napum)",  "pacat  (napum)  [SK446 mandatory nUM]"),
    ("dIvyat_napum", dIvyat_napum,     "śatṛ-stems (napum)",  "dīvyat  (napum)  [SK446 mandatory nUM]"),
    ("tudat_napum",  tudat_napum,      "śatṛ-stems (napum)",  "tudat  (napum)  [SK445 optional nUM]"),
    ("pacat_strI",   _pacat_strI_cpd,  "śatṛ-stems (strī)",   "pacat  (strī)  [SK446 mandatory → pacantī]"),
    ("dIvyat_strI",  _dIvyat_strI_cpd, "śatṛ-stems (strī)",   "dīvyat  (strī)  [SK446 mandatory → dīvyantī]"),
    ("tudat_strI",   _tudat_strI_cpd,  "śatṛ-stems (strī)",   "tudat  (strī)  [SK445 optional]"),
    ("BAt_strI",     _BAt_strI_cpd,    "śatṛ-stems (strī)",   "bhāt  (strī)  [SK445 optional]"),

    # ── Strī-pratyaya (SK454-464) — strI_abs flow demos ──────────────────
    ("rAma_A",   _rAma_A_cpd,   "Strī-pratyaya (SK454-464)", "rāmā  (SK454 TAp: rāma+strI_abs → rāmā)"),
    ("aja_A",    _aja_A_cpd,    "Strī-pratyaya (SK454-464)", "ajā  (SK454 ajādi → TAp)"),
    ("kokila_A", _kokila_A_cpd, "Strī-pratyaya (SK454-464)", "kokilā  (SK454 ajādi → TAp)"),
    ("SUdra_A",  _SUdra_A_cpd,  "Strī-pratyaya (SK454-464)", "śūdrā  (SK454 ajādi → TAp)"),
    ("kruYc_A",  _kruYc_A_cpd,  "Strī-pratyaya (SK454-464)", "kruñcā  (SK454 ajādi, consonant-final)"),
    ("uzRih_A",  _uzRih_A_cpd,  "Strī-pratyaya (SK454-464)", "uṣṇihā  (SK454 ajādi, consonant-final)"),
    ("pacat_NI", _pacat_NI_cpd, "Strī-pratyaya (SK454-464)", "pacantī  (SK455 NIp: pacat+strI_abs → pacantī)"),
    ("Bavat_uNI", _Bavat_uNI_cpd, "Strī-pratyaya (SK454-464)", "bhavatī  (SK455 u-it → NIp)"),
    ("tad_strI",  _tad_strI_cpd,  "Strī-pratyaya (SK454-464)", "sā  (SK454 tyadādi feminine)"),
    ("etad_strI", _etad_strI_cpd, "Strī-pratyaya (SK454-464)", "eṣā  (SK454 tyadādi feminine)"),
    ("yad_strI",  _yad_strI_cpd,  "Strī-pratyaya (SK454-464)", "yā  (SK454 tyadādi feminine)"),
    ("kim_strI",  _kim_strI_cpd,  "Strī-pratyaya (SK454-464)", "kā  (SK454 kim feminine)"),
    ("adas_strI", _adas_strI_cpd, "Strī-pratyaya (SK454-464)", "asau  (SK454 adas feminine)"),
    ("Sf_vanip_strI", _Sf_vanip_strI_cpd, "Strī-pratyaya (SK454-464)", "śarvarī  (SK456 4.1.7 vano ra ca: van → NIp + n→r)"),
    ("dvipAd_strI",   _dvipAd_strI_cpd,   "Strī-pratyaya (SK454-464)", "dvipadī/dvipād  (SK457 4.1.8 pādo'nyatarasyām)"),
    ("sIman_strI",    _sIman_strI_cpd,    "Strī-pratyaya (SK454-464)", "sīmā  (SK459 4.1.11 manaH: man-final, ṅīp blocked)"),
    ("bahuyajvan_strI", _bahuyajvan_strI_cpd, "Strī-pratyaya (SK454-464)", "bahuyajvā  (SK460/461 an-bahuvrīhi: ṅīp blocked / opt DAp)"),
    ("bahurAjan_strI",  _bahurAjan_strI_cpd,  "Strī-pratyaya (SK454-464)", "bahurājñī  (SK462 4.1.28: an-upadhālopin bahuvrīhi, opt ṅīp)"),
    ("sarvika",   _sarvika_cpd,   "Strī-pratyaya (SK454-464)", "sarvika  (SK463 7.3.44 idādeśa: sarva+kan → sarvika)"),
    ("yaka_strI", _yaka_strI_cpd, "Strī-pratyaya (SK454-464)", "yakā  (SK464 7.3.45 blocks SK463: yad+kan)"),
    ("saka_strI", _saka_strI_cpd, "Strī-pratyaya (SK454-464)", "sakā/takā  (SK464 blocks SK463: tad+kan)"),
    ("parivrAjaka_strI", _parivrAjaka_strI_cpd, "Strī-pratyaya (SK454-464)", "parivrājikā  (SK463 idādeśa: ṇvul aka-stem)"),
    ("bahuparivrAjaka_strI", _bahuparivrAjaka_strI_cpd, "Strī-pratyaya (SK454-464)", "bahuparivrājakā  (SK463 asuwapaH: ?!bahuvrīhi blocks)"),

    # ── i stems ───────────────────────────────────────────────────────────
    ("kavi",     kavi,        "i-stems (pum)",    "kavi  (kavi-)"),
    ("hari",     hari,        "i-stems (pum)",    "hari  (hari-)"),
    ("pati",     pati,        "i-stems (pum)",    "pati  (pati-)  [SK248 special]"),
    ("saKi",     saKi,        "i-stems (pum)",    "sakhī  (sakhi-)  [SK248]"),
    ("mati",     mati,        "i-stems (strī)",   "mati  (mati-)"),
    ("vAri",     vAri,        "i-stems (napum)",  "vāri  (vāri-)"),

    # ── ī stems ───────────────────────────────────────────────────────────
    ("nadI",     nadI,        "ī-stems (strī)",   "nadī  (nadī-)"),
    ("lakzmI",   lakzmI,      "ī-stems (strī)",   "lakṣmī  (lakṣmī-)"),
    ("strI",     strI,        "ī-stems (strī)",   "strī  (strī-)"),

    # ── u stems ───────────────────────────────────────────────────────────
    ("SamBu",    SamBu,       "u-stems (pum)",    "śambhu  (śambhu-)"),
    ("krozwu",   krozwu,      "u-stems (pum)",    "kroṣṭu  (kroṣṭu-)"),
    ("vasu",     vasu_pum,    "u-stems (pum)",    "vasu  (vasu-)"),
    ("Denu",     Denu,        "u-stems (strī)",   "dhenu  (dhenu-)"),

    # ── ū stems ───────────────────────────────────────────────────────────
    ("BrU",      BrU,         "ū-stems (strī)",   "bhrū  (bhrū-)"),
    ("svayamBU", svayamBU,    "ū-stems (kvip)",   "svayambhū  (svayambhū-)"),
    ("atistri",  atistri,     "ū-stems (kvip)",   "atistri  [strī_p]"),

    # ── ṛ stems ───────────────────────────────────────────────────────────
    ("pitf",     pitf,        "ṛ-stems (pum)",    "pitṛ  (pitṛ-)"),
    ("nf",       nf,          "ṛ-stems (pum)",    "nṛ  (nṛ-)"),
    ("tvazwf",   tvazwf,      "ṛ-stems (pum)",    "tvaṣṭṛ  (tvaṣṭṛ-)  [naptrādi]"),
    ("mAtf",     mAtf,        "ṛ-stems (strī)",   "mātṛ  (mātṛ-)"),
    ("svasf",    svasf,       "ṛ-stems (strī)",   "svasṛ  (svasṛ-)"),
    ("tisf",     tisf,        "ṛ-stems (strī)",   "tisṛ  (tisṛ-)  [nityabahuvacana]"),

    # ── o / ai stems ──────────────────────────────────────────────────────
    ("go",       go,          "o/ai-stems",       "go  (go-)"),
    ("rE",       rE,          "o/ai-stems",       "rāi  (rāi-)"),

    # ── n-stems ───────────────────────────────────────────────────────────
    ("rAjan",    rAjan,       "n-stems (pum)",    "rājan  (rājan-)"),
    ("pUzan",    pUzan,       "n-stems (pum)",    "pūṣan  (pūṣan-)"),
    ("yajvan",   yajvan,      "n-stems (pum)",    "yajvan  (yajvan-)"),
    ("parvan",   parvan_napum,"n-stems (napum)",  "parvan  (parvan-)"),

    # ── śvan-group: samprasāraṇa in bha (SK362) ───────────────────────────
    ("svan",     svan,        "śvan-group",       "śvan  (śvan-)  [SK362]"),
    ("yuvan",    yuvan,       "śvan-group",       "yuvan  (yuvan-)  [SK362]"),
    ("maGavan",  maGavan,     "śvan-group",       "maghavan  (maghavan-)  [SK363]"),
    ("arvan",    arvan,       "śvan-group",       "arvan  (arvan-)  [SK364]"),

    # ── in-stems ──────────────────────────────────────────────────────────
    ("hastin",   hastin,      "in-stems (pum)",   "hastin  (hastin-)"),
    ("yogin",    yogin,       "in-stems (pum)",   "yogin  (yogin-)"),

    # ── paTin-group: SK365-368 ────────────────────────────────────────────
    ("paTin",    paTin,       "paTin-group",      "pathin  (pathin-)  [SK365–368]"),
    ("maTin",    maTin,       "paTin-group",      "mathin  (mathin-)  [SK365–368]"),
    ("fBukzin",  fBukzin,     "paTin-group",      "ṛbhukṣin  (ṛbhukṣin-)  [SK365–368]"),

    # ── han-stems ─────────────────────────────────────────────────────────
    ("vftrahan", _vftrahan_cpd, "han-stems",      "vṛtrahān  [vṛtra+han+kvip, SK358–359]"),

    # ── ahan-stems (SK443) ────────────────────────────────────────────────
    ("ahan",     ahan,        "ahan-stems",       "ahan  (ahan-)  [SK443]"),

    # ── nah-stems ──────────────────────────────────────────────────────────
    ("upAnah",   upAnah,      "nah-stems",        "upānah  (upānah-)  [SK440]"),

    # ── vasanta/pums-stems ─────────────────────────────────────────────────
    ("vidvas",   vidvas,      "vasanta-stems",    "vidvas  (vidvas-)  [SK435 kvasu]"),
    ("pums",     pums,        "puṃs-stems",       "puṃs  (puṃs-)  [SK436]"),

    # ── ap-stems (p-final, nityabahuvacana) ──────────────────────────────
    ("ap",       ap,          "ap-stems",         "ap  (strī, nityabahuvacana)  [SK442]"),

    # ── napum i-stems ─────────────────────────────────────────────────────
    ("asTi",     asTi,        "i-stems (napum)",  "asthi  (asthi-)"),
    ("daDi",     daDi,        "i-stems (napum)",  "dadhi  (dadhi-)"),
    ("akzi",     akzi,        "i-stems (napum)",  "akṣi  (akṣi-)"),
    ("atinO",    atinO,       "i-stems (napum)",  "atinau  (atinau-)"),
    ("Danus",    Danus,       "i-stems (napum)",  "dhanus  (dhanus-)  [ādeśa-s]"),

    # ── Pronouns ──────────────────────────────────────────────────────────
    ("kim",      kim,         "Pronouns",         "kim  (kim-)"),
    ("idam",     idam,        "Pronouns",         "idam  (idam-)"),
    ("idam_anu", [idam_anu],  "Pronouns",         "idam  (anvādeśa)"),
    ("idam_strI", idam_strI,  "Pronouns",         "idam  (strī)"),
    ("sarva",    sarva,       "Pronouns",         "sarva  (sarva-)  [sarvādi]"),
    ("anya",     anya,        "Pronouns",         "anya  (anya-)  [qatarādi]"),
    ("yuzmad",   yuzmad,      "Pronouns",         "yuṣmad  [2nd person]"),
    ("asmad",    asmad,       "Pronouns",         "asmad  [1st person]"),
    ("tad",      tad,         "Pronouns",         "tad  (tad-)  [tyadādi]"),
    ("etad",     etad,        "Pronouns",         "etad  (etad-)  [tyadādi]"),
    ("yad",      yad,         "Pronouns",         "yad  (yad-)  [tyadādi]"),
    ("tyad",     tyad,        "Pronouns",         "tyad  (tyad-)  [tyadādi]"),
    ("adas",     adas,        "Pronouns",         "adas  (adas-)  [tyadādi]"),

    # ── dvitīyādi ordinal compounds ───────────────────────────────────────
    ("dvitIyA",  _dvitIyA_cpd,  "dvitīyādi (ordinals)", "dvitīyā  [dvitīya+Āp]"),
    ("tftIyA",   _tftIyA_cpd,   "dvitīyādi (ordinals)", "tṛtīyā  [tṛtīya+Āp]"),

    # ── kvip / special ────────────────────────────────────────────────────
    ("div",      div_kvip,    "kvip-stems",       "div  (div-)"),
    ("lih",      lih_kvip,    "kvip-stems",       "lih  (lih-)"),
    ("duh",      duh_kvip,    "kvip-stems",       "duh  (duh-)"),
    ("druh",     druh_kvip,   "kvip-stems",       "druh  (druh-)"),
    ("anaquh",   anaquh,      "kvip-stems",       "anaḍuh  (anaḍuh-)"),
    ("senAnI",   senAnI,      "kvip-stems",       "senānī  (senānī-)"),
    ("viSvapA",  viSvapA,     "kvip-stems",       "viśvapā  (viśvapā-)  [vic]"),
    ("hAhA",     hAhA,        "kvip-stems",       "hāhā  (hāhā-)"),
    ("nI",       nI,          "kvip-stems",       "nī  (nī-)  [kvip]"),
    ("SrI",      SrI,         "kvip-stems",       "śrī  (śrī-)  [kvip strī]"),
    ("SrIpA",    SrIpA,       "kvip-stems",       "śrīpā  (śrīpā-)  [kvip napum]"),
    ("suDI",     suDI,        "kvip-stems",       "sudhī  [kvip pūrvastrī]"),
    ("praDI",    praDI,       "kvip-stems",       "pradhī  [kvip pūrvastrī]"),
    ("varzABU",  varzABU,     "kvip-stems",       "varṣābhū  [kvip BU]"),
    ("dfnBU",    dfnBU,       "kvip-stems",       "dṛṃbhū  [kvip BU]"),
    ("karaBU",   karaBU,      "kvip-stems",       "karabhū  [kvip BU]"),
    ("punarBU",  punarBU,     "kvip-stems",       "punarbhū  [kvip BU]"),
    ("KalapU",   KalapU,      "kvip-stems",       "khalapū  [kvip]"),
    ("turAsAh",  turAsAh,     "kvip-stems",       "turāsāh  [kvip]"),
    ("praSAm",   praSAm_kvip, "kvip-stems",       "praśām  [kvip]"),
    ("takz",     takz_kvip,   "kvip-stems",       "takṣ  (takṣ-)  [SK380]"),
    ("naS",      naS_kvip,    "kvip-stems",       "naś  (naś-)  [SK431 optional]"),
    ("praVAh",   _praVAh_cpd, "kvip-stems",       "pravāh  (pra+vāh-)  [cpd kvip]"),

    # ── kvin-stems (SK373–377) ────────────────────────────────────────────
    ("ftvij",    ftvij_kvin,  "kvin-stems",       "ṛtvij  (ṛtvij-)  [SK373]"),
    ("sraj",     sraj_kvin,   "kvin-stems",       "sraj  (sraj-)  [SK374]"),
    ("yuj",      yuj_kvin,    "kvin-stems",       "yuj  (yuj-)  [SK375]"),
    ("diS",      diS_kvin,    "kvin-stems",       "diś  (diś-)  [SK377]"),
    ("daDfc",    daDfc_kvin,  "kvin-stems",       "dadhṛc  (dadhṛc-)  [c-final]"),
    ("udac",     udac_kvin,   "kvin-stems",       "udañc  (udac-)  [SK361 aYc]"),
    ("tiryac",   tiryac_kvin, "kvin-stems",       "tiryañc  (tiryac-)  [SK361 aYc]"),
    ("yuj_samAsa", [yuj_kvin_samAsa], "kvin-stems", "yuj-in-cpd  [samāsa no nUM]"),
    # añcatir compounds (dynamic derivation via aYc_u)
    ("pratyac_cpd",  _pratyac_cpd,  "kvin-stems",  "pratyañc  [prati+añc+kvin]"),
    ("prAc_cpd",     _prAc_cpd,     "kvin-stems",  "prāñc  [pra+añc+kvin]"),
    ("udac_cpd",     _udac_cpd,     "kvin-stems",  "udañc  [ud+añc+kvin]"),
    ("tiryac_cpd",   _tiryac_cpd,   "kvin-stems",  "tiryañc  [tiras+añc+kvin]"),
    ("samyac_cpd",   _samyac_cpd,   "kvin-stems",  "samyañc  [sam+añc+kvin]"),
    ("saDryac_cpd",  _saDryac_cpd,  "kvin-stems",  "sadhryañc  [saha+añc+kvin]"),
    ("vizvadryac",   _vizvadryac_cpd, "kvin-stems", "viśvadryañc  [viśvag+añc+kvin]"),

    # ── samāsa (compounds) ────────────────────────────────────────────────
    ("gaRapati",  _gaRapati_cpd,  "samāsa",  "gaṇapati  [SK257 pati-in-cpd]"),
    ("aSvayuj",   _aSvayuj_cpd,   "samāsa",  "aśvayuj  [SK376 yuj-in-cpd]"),
    ("viSvAvasu", _viSvAvasu_cpd, "samāsa",  "viśvāvasu  [SK379]"),
    ("viSvArAj",  _viSvArAj_cpd,  "samāsa",  "viśvārāj  [SK379 rāṭ/rāj forms]"),
    # SK429/SK430 tādṛk/yādṛk compounds
    ("tAdfk",    _tAdfk_cpd,     "samāsa",  "tādṛk  [tad+dṛś+kvin]"),
    ("yAdfk",    _yAdfk_cpd,     "samāsa",  "yādṛk  [yad+dṛś+kvin]"),
    ("tAdfSa",   _tAdfSa_cpd,    "samāsa",  "tādṛśa  [tad+dṛś+kaY]"),
    ("yAdfSa",   _yAdfSa_cpd,    "samāsa",  "yādṛśa  [yad+dṛś+kaY]"),
    ("tAdfkza",  _tAdfkza_cpd,   "samāsa",  "tādṛkṣa  [tad+dṛkṣa]"),
    ("yAdfkza",  _yAdfkza_cpd,   "samāsa",  "yādṛkṣa  [yad+dṛkṣa]"),
    # SK430 vatup arm — measure stems
    ("tAvat_n",  _tAvat_n_cpd,   "samāsa",  "tāvat  (napum)  [tad+vatup]"),
    ("yAvat_n",  _yAvat_n_cpd,   "samāsa",  "yāvat  (napum)  [yad+vatup]"),
    ("etAvat_n", _etAvat_n_cpd,  "samāsa",  "etāvat  (napum)  [etad+vatup]"),
    ("tAvAn",    _tAvAn_cpd,     "samāsa",  "tāvān  (pum)  [tad+vatup]"),
    ("yAvAn",    _yAvAn_cpd,     "samāsa",  "yāvān  (pum)  [yad+vatup]"),
    ("etAvAn",   _etAvAn_cpd,    "samāsa",  "etāvān  (pum)  [etad+vatup]"),
    # luk-sup compounds (pūrva-pada with empty sup)
    ("SUrpanaKI",  _SUrpanaKI_cpd,  "samāsa",  "śūrpaṇakhī  [śūrpa+naḳī]"),
    ("kzIrapa",    _kzIrapa_cpd,    "samāsa",  "kṣīrapā  [kṣīra+pa]  [SK176]"),
    # SK432: ghṛtaspṛk (spṛś+kvin after ghṛta)
    ("Gftaspfk",   _Gftaspfk_cpd,   "samāsa",  "ghṛtaspṛk  [ghṛta+spṛś+kvin]  [SK432]"),
    # SK161 pada-compounds
    ("aDaspada",   _aDaspada_cpd,   "samāsa",  "adaḥpada  [adas+pada]  [SK161]"),
    ("Siraspada",  _Siraspada_cpd,  "samāsa",  "śiraḥpada  [śiras+pada]  [SK161]"),

    # ── Numerals ──────────────────────────────────────────────────────────
    ("tri",      tri,         "Numerals",         "tri  [nityabahuvacana]"),
    ("dvi",      dvi,         "Numerals",         "dvi  [nityadvivacana]"),
    ("dvi_s",    dvi_s,       "Numerals",         "dvi  (strī)  [nityadvivacana]"),
    ("catur",    catur,       "Numerals",         "catur  [nityabahuvacana]"),
    ("catasf",   catasf,      "Numerals",         "catasṛ  (catasṛ-)  [strī nityabahuvacana]"),
    ("kati",     kati,        "Numerals",         "kati  [nityabahuvacana]"),
    ("paYcan",   paYcan,      "Numerals",         "pañcan  [SK369 nityabahuvacana]"),
    ("saptan",   saptan,      "Numerals",         "saptan  [nityabahuvacana]"),
    ("navan",    navan,       "Numerals",         "navan  [nityabahuvacana]"),
    ("daSan",    daSan,       "Numerals",         "daśan  [nityabahuvacana]"),
    ("azwan",    azwan,       "Numerals",         "aṣṭan  [SK371–372 opt]"),

    # ── Iyasun (comparatives) ─────────────────────────────────────────────
    ("Sreyas",   Sreyas,      "Iyasun (comparatives)", "śreyas  (pum)  [SK361 ugit]"),
    ("Sreyas_n", Sreyas_n,    "Iyasun (comparatives)", "śreyas  (napum)  [7.1.72]"),
]

# Build lookup map and ordered groups
STEM_MAP = {}     # key → pratipadika obj (or list)
STEM_GROUPS = {}  # group_label → list of {key, label}

for key, obj, group, label in _STEMS_RAW:
    STEM_MAP[key] = obj
    if group not in STEM_GROUPS:
        STEM_GROUPS[group] = []
    STEM_GROUPS[group].append({"key": key, "label": label})

# ---------------------------------------------------------------------------
# Vibhakti / vacana metadata
# ---------------------------------------------------------------------------

VIBHAKTI_NAMES = [
    "Nominative (prathamā)",
    "Accusative (dvitīyā)",
    "Instrumental (tṛtīyā)",
    "Dative (caturthī)",
    "Ablative (pañcamī)",
    "Genitive (ṣaṣṭhī)",
    "Locative (saptamī)",
    "Vocative (sambodhana)",
]

VACANA_NAMES = ["Singular", "Dual", "Plural"]

ENCODING_MAP = {
    "devanagari": sanscript.DEVANAGARI,
    "iast":       sanscript.IAST,
    "slp1":       sanscript.SLP1,
}

# ---------------------------------------------------------------------------
# Custom input catalogs (for /api/objects and token resolution)
# ---------------------------------------------------------------------------

_VIB_ABBREV = ["nom", "acc", "inst", "dat", "abl", "gen", "loc", "voc"]
_VAC_ABBREV = ["sg", "du", "pl"]

# Canonical Pāṇinian sup names (SLP1) for display in the UI
_SUP_SLP1 = [
    ["su",   "O",    "jas"],
    ["am",   "Ow",   "Sas"],
    ["wA",   "ByAm", "Bis"],
    ["Ne",   "ByAm", "Byas"],
    ["Nasi", "ByAm", "Byas"],
    ["Nas",  "os",   "Am"],
    ["Ni",   "os",   "sup"],
    ["su",   "O",    "jas"],
]

_PRATYAYA_CATALOG = {}
for _vi in range(8):
    for _vj in range(3):
        _k = f"sup.{_VIB_ABBREV[_vi]}.{_VAC_ABBREV[_vj]}"
        _PRATYAYA_CATALOG[_k] = (
            sups[_vi][_vj],
            f"{_SUP_SLP1[_vi][_vj]} — {VIBHAKTI_NAMES[_vi]} {VACANA_NAMES[_vj]}",
        )
_PRATYAYA_CATALOG.update({
    # kṛt — verbal derivatives
    "tfc":    (tfc,    "tfc — agent noun (-tṛ, e.g. kartṛ)"),
    "GaY":    (GaY,    "GaY — action noun (-a, e.g. yoga)"),
    "kta":    (kta,    "kta — PPP (-ta, e.g. kṛta)"),
    "ktvA":   (ktvA,   "ktvā — absolutive (-tvā, e.g. gatvā)"),
    "yat":    (yat,    "yat — gerundive (-ya)"),
    "Ryat":   (Ryat,   "Ryat — gerundive (-ya, e.g. gantavya)"),
    "anIya":  (anIya,  "anīya — gerundive (-anīya)"),
    "kvin":   (kvin,   "kvin — kṛt verbal-adj (zero)"),
    "kvip":   (kvip,   "kvip — kṛt noun (zero)"),
    "kaY":    (kaY,    "kaY — kṛt agent (-a)"),
    "wac":    (wac,    "wac — kṛt participle (-a, samāsa)"),
    "kanin":  (kanin,  "kanin — kṛt participle (-an)"),
    "vatup":  (vatup,  "vatup — tāvat- (-vat)"),
    # strī-pratyayas
    "NIp":    (NIp,    "NĪp — strī-pratyaya (-ī)"),
    "NIz":    (NIz,    "NĪz — strī-pratyaya (-ī, alt)"),
    "Ap":     (Ap,     "Āp — strī-pratyaya (-ā)"),
    # taddhita
    "pASap":  (pASap,  "pāśap — taddhita (-pāśa, similarity)"),
    "kalpap": (kalpap, "kalpap — taddhita (-kalpa, similarity)"),
    "kap":    (kap,    "kap — taddhita (-ka, similarity)"),
    "kAmyac": (kAmyac, "kāmyac — taddhita (-kāmya, desiderative)"),
    "suc":    (suc,    "suc — taddhita (-s)"),
    # special sup
    "Si":     (Si,     "Śi — jasaḥ Śī replacement (neuter pl)"),
    "OS":     (OS,     "OS — sup (alt O)"),
    "adaq":   (adaq,   "adaq — sup for qatarādi"),
    "luk_sup": (luk_sup, "luk-sup — zero sup (pūrva-pada)"),
    # tiN — verbal endings (partial; full paradigm not yet in engine)
    "tip":    (tip,    "tip — 3sg present active (ti)"),
    "sip":    (sip,    "sip — 2sg present active (si)"),
    # vikaraṇa — stem-forming
    "Sap":    (Sap,    "Śap — vikaraṇa class 1/4 (-a-)"),
    "yak":    (yak,    "yak — passive vikaraṇa (-ya-)"),
    # ṇic — causative
    "Ric":    (Ric,    "Ric — ṇic causative (-i-)"),
    # upasarga — preverbs
    "pra":    (pra_upasarga,  "pra — upasarga (pra-)"),
    "upa":    (upa_upasarga,  "upa — upasarga (upa-)"),
    "ava":    (ava_upasarga,  "ava — upasarga (ava-)"),
    "ud":     (ud_upasarga,   "ud — upasarga (ud-)"),
    "ati":    (ati_upasarga,  "ati — upasarga (ati-)"),
    "AN":     (AN_upasarga,   "ā — upasarga (ā-, ṅit)"),
    "mAN":    (mAN_upasarga,  "mā — upasarga (mā-, ṅit)"),
    # taddhita from prātipadika
    "yat_t":  (yat_t,  "yat — taddhita (-ya)"),
    "zyaY_t": (zyaY_t, "zyaṄ — taddhita (-ya, zy-it)"),
    "yaY_t":  (yaY_t,  "yaṄ — taddhita (-ya, Y-it)"),
    "aR_t":   (aR_t,   "aṆ — taddhita (-a)"),
    # gender / number markers
    "pum_abs":   (pum_abs,   "pum-abs — masculine marker (zero)"),
    "napum_abs": (napum_abs, "napum-abs — neuter marker (zero)"),
    "strI_abs":  (strI_abs,  "strī-abs — feminine marker (zero)"),
    # luk / UW
    "luk":    (luk,    "luk — general zero replacement"),
    "UW":     (UW,     "UW — samprasāraṇam (Ū)"),
})

_DHATU_CATALOG = {
    # Group 1: most common roots
    "BU":     (BU,     "√bhū (be, become)"),
    "as_dhatu": (as_dhatu, "√as (be, exist)"),
    "iR":     (iR,     "√i (go)"),
    "sTA":    (sTA,    "√sthā (stand)"),
    "ji":     (ji,     "√ji (conquer)"),
    "vid":    (vid,    "√vid (know)"),
    "vah":    (vah,    "√vah (carry)"),
    "duh":    (duh,    "√duh (milk)"),
    "mud":    (mud,    "√mud (rejoice)"),
    "Sam":    (Sam,    "√śam (be calm)"),
    "Cad":    (Cad,    "√chad (cover)"),
    "kzI":    (kzI,    "√kṣī (diminish)"),
    "lUY":    (lUY,    "√lū (cut)"),
    # Group 2: specific/derived
    "dfS":    (dfS,    "√dṛś (see)"),
    "spfS":   (spfS,   "√spṛś (touch)"),
    "han":    (han,    "√han (strike)"),
    "aYc_u":  (aYc_u,  "√añc (go, bend)"),
    "eDa":    (eDa,    "√edh (prosper)"),
    "fcCa":   (fcCa,   "√ṛcch (go)"),
    "gfj":    (gfj,    "√garj (roar)"),
    "guhU":   (guhU,   "√guh (hide)"),
    "qukrIY": (qukrIY, "√krī (buy)"),
    "qulaBaz":(qulaBaz,"√labh (obtain)"),
    "veY":    (veY,    "√ve (weave)"),
    "veY_smp":(veY_smp,"√ve (samprasāraṇa)"),
}

# ---------------------------------------------------------------------------
# Core generation logic
# ---------------------------------------------------------------------------


def _slp1_to_display(slp1_form, enc):
    """Strip avasāna marker and transliterate to target encoding."""
    form = slp1_form.rstrip(".").strip()
    if not form:
        return "—"
    return sanscript.transliterate(form, sanscript.SLP1, enc)


def _generate_cell(plist, sup, enc, tag_display=False, capture_eval=False):
    """
    Run the prakriyā for one declension cell.

    Returns:
        forms     (list[str])        : output form(s) in the requested encoding
        trace     (str)              : multi-line sutra-trace text from p.describe()
        eval_logs (list | None)      : per-step evaluation records (if capture_eval)
    """
    # Compound (multi-element plist) requires hierarchical structure so that
    # pūrva-pada rules (e.g. SK379) fire *after* the uttara-pada + sup merge,
    # matching the test infrastructure: [[*plist, sup], avasāna].
    if len(plist) > 1:
        inputs = [Adya, [*plist, sup], avasAna]
    else:
        inputs = [Adya, *plist, sup, avasAna]
    pv = PrakriyaVakya(inputs)
    p = AntarangaPrakriya(sutra_list, pv, capture_eval=capture_eval)
    p.execute()
    output = p.output()

    # Capture describe() which prints to stdout
    buf = io.StringIO()
    with redirect_stdout(buf):
        p.describe(tag_display=tag_display)
    trace = buf.getvalue()

    outer_eval = p.tree.get_eval_logs_dfs() if capture_eval else None
    inner_eval = []
    if capture_eval:
        for hp in p.hier_prakriyas:
            if not getattr(hp, 'triggering_sutra_aps', None):
                inner_eval.append(hp.tree.get_eval_logs_dfs())
    eval_logs = {"outer": outer_eval, "inner": inner_eval} if capture_eval else None

    # Convert outputs to display strings
    forms = []
    for o in output:
        slp1 = "".join(obj.transcoded(sanscript.SLP1) for obj in list(o))
        forms.append(_slp1_to_display(slp1, enc))

    return forms, trace, eval_logs


def _generate_table_from_plist(plist, enc, tag_display=False, capture_eval=False):
    """Generate the full 8×3 declension table from a pre-resolved pratipadika list."""
    pratipadika = plist[-1]
    nityaEka  = pratipadika.hasTag("nityEkavacana")
    nityaDvi  = pratipadika.hasTag("nityadvivacana")
    nityaBahu = pratipadika.hasTag("nityabahuvacana")

    table = []
    traces = []
    eval_logs_grid = []
    for vib_idx in range(8):
        row = []
        row_traces = []
        row_evals = []
        for vac_idx in range(3):
            skip = (
                (nityaEka  and vac_idx != 0) or
                (nityaDvi  and vac_idx != 1) or
                (nityaBahu and vac_idx != 2)
            )
            if skip:
                row.append("—")
                row_traces.append("")
                row_evals.append(None)
                continue

            sup = sups[vib_idx][vac_idx]
            try:
                forms, trace, elogs = _generate_cell(plist, sup, enc, tag_display=tag_display,
                                                     capture_eval=capture_eval)
                row.append(" | ".join(forms) if forms else "?")
                row_traces.append(trace)
                row_evals.append(elogs)
            except Exception as exc:  # noqa: BLE001
                row.append("[error]")
                row_traces.append(str(exc))
                row_evals.append(None)

        table.append(row)
        traces.append(row_traces)
        eval_logs_grid.append(row_evals)

    return table, traces, eval_logs_grid


def generate_table(stem_key, enc, tag_display=False, capture_eval=False):
    """Generate the full 8×3 declension table for a catalog stem key."""
    obj = STEM_MAP[stem_key]
    plist = obj if isinstance(obj, list) else [obj]
    return _generate_table_from_plist(plist, enc, tag_display=tag_display, capture_eval=capture_eval)


# ---------------------------------------------------------------------------
# Custom input: token resolution and single-form runner
# ---------------------------------------------------------------------------

def _resolve_token(tok):
    """Convert one JSON token descriptor to a list of PaninianObjects (may be nested)."""
    t = tok["type"]
    if t == "pratipadika":
        name = tok["name"]
        if name in STEM_MAP:
            obj = STEM_MAP[name]
        else:
            raise KeyError(name)
        obj_list = list(obj) if isinstance(obj, list) else [obj]
        mod = tok.get("modifier", "")
        if mod == "in_compound":
            obj_list = [*obj_list[:-1], in_compound(obj_list[-1])]
        elif mod == "as_purva_pada":
            obj_list = [*obj_list[:-1], as_purva_pada(obj_list[-1])]
        elif mod == "in_context":
            ctx = tok.get("context", "")
            if ctx:
                obj_list = [*obj_list[:-1], in_context(obj_list[-1], ctx)]
        return obj_list
    elif t == "pratyaya":
        pratyaya_obj, _ = _PRATYAYA_CATALOG[tok["name"]]
        mod = tok.get("modifier", "")
        if mod == "in_context":
            ctx = tok.get("context", "")
            if ctx:
                pratyaya_obj = in_context(pratyaya_obj, ctx)
        return [pratyaya_obj]
    elif t == "dhatu":
        dhatu_obj, _ = _DHATU_CATALOG[tok["name"]]
        mod = tok.get("modifier", "")
        if mod == "in_context":
            ctx = tok.get("context", "")
            if ctx:
                dhatu_obj = in_context(dhatu_obj, ctx)
        return [dhatu_obj]
    elif t == "string":
        o = PaninianObject(tok["value"], sanscript.SLP1)
        if tok.get("tag"):
            o.setTag(tok["tag"])
        return [o]
    elif t == "group":
        inner = []
        for child in tok["tokens"]:
            inner.extend(_resolve_token(child))
        return [inner]
    else:
        raise ValueError(f"Unknown token type: {t!r}")


def _resolve_token_list(tokens):
    """Convert a JSON token list to a Python object list (may contain nested lists)."""
    result = []
    for tok in tokens:
        result.extend(_resolve_token(tok))
    return result


def _run_single_form(objects, enc, tag_display=False, capture_eval=False):
    """Run a single prakriyā on an arbitrary sequence of resolved objects."""
    inputs = [Adya, *objects, avasAna]
    pv = PrakriyaVakya(inputs)
    p = AntarangaPrakriya(sutra_list, pv, capture_eval=capture_eval)
    p.execute()

    buf = io.StringIO()
    with redirect_stdout(buf):
        p.describe(tag_display=tag_display)
    trace = buf.getvalue()

    outer_eval = p.tree.get_eval_logs_dfs() if capture_eval else None
    inner_eval = []
    if capture_eval:
        for hp in p.hier_prakriyas:
            if not getattr(hp, 'triggering_sutra_aps', None):
                inner_eval.append(hp.tree.get_eval_logs_dfs())
    eval_logs = {"outer": outer_eval, "inner": inner_eval} if capture_eval else None

    forms = []
    for o in p.output():
        slp1 = "".join(obj.transcoded(sanscript.SLP1) for obj in list(o))
        forms.append(_slp1_to_display(slp1, enc))

    return forms, trace, eval_logs


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template(
        "index.html",
        groups=STEM_GROUPS,
        vibhaktis=VIBHAKTI_NAMES,
        vacanas=VACANA_NAMES,
        default_stem=list(STEM_MAP.keys())[0],
    )


@app.route("/api/generate")
def api_generate():
    stem_key     = request.args.get("stem", "")
    enc_name     = request.args.get("encoding", "devanagari")
    tag_display  = request.args.get("tags", "") == "true"
    capture_eval = request.args.get("eval", "") == "true"

    if stem_key not in STEM_MAP:
        return jsonify({"error": f"Unknown stem: {stem_key!r}"}), 400

    enc = ENCODING_MAP.get(enc_name, sanscript.DEVANAGARI)

    try:
        table, traces, eval_logs_grid = generate_table(stem_key, enc, tag_display=tag_display,
                                                       capture_eval=capture_eval)
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": str(exc)}), 500

    return jsonify({
        "stem":      stem_key,
        "enc":       enc_name,
        "table":     table,
        "traces":    traces,
        "eval_logs": eval_logs_grid if capture_eval else None,
        "vibhaktis": VIBHAKTI_NAMES,
        "vacanas":   VACANA_NAMES,
    })


@app.route("/api/objects")
def api_objects():
    """Return grouped catalogs of selectable pratipadika, pratyaya, and dhatu objects."""
    # Pratipadika: single-component only (exclude list entries = compounds)
    pratipadika_groups = [
        {"group": grp, "items": [
            [s["key"], s["label"]] for s in items
            if not isinstance(STEM_MAP.get(s["key"]), list)
        ]}
        for grp, items in STEM_GROUPS.items()
    ]
    # Drop groups that became empty after filtering
    pratipadika_groups = [g for g in pratipadika_groups if g["items"]]

    # Pratyaya: organized by category
    def _py_items(keys):
        return [[k, _PRATYAYA_CATALOG[k][1]] for k in keys if k in _PRATYAYA_CATALOG]

    sup_keys = [k for k in _PRATYAYA_CATALOG if k.startswith("sup.")]
    pratyaya_groups = [
        {"group": "sup — Nominal case endings",        "items": _py_items(sup_keys)},
        {"group": "kṛt — Verbal derivatives",          "items": _py_items([
            "tfc", "GaY", "kta", "ktvA", "yat", "Ryat", "anIya",
            "kvin", "kvip", "kaY", "wac", "kanin", "vatup"])},
        {"group": "Strī — Feminine suffixes",          "items": _py_items(["NIp", "NIz", "Ap", "strI_abs"])},
        {"group": "Taddhita — from prātipadika",       "items": _py_items(["yat_t", "zyaY_t", "yaY_t", "aR_t"])},
        {"group": "Taddhita — similarity",             "items": _py_items(["pASap", "kalpap", "kap", "kAmyac", "suc"])},
        {"group": "tiN — Verbal endings",              "items": _py_items(["tip", "sip"])},
        {"group": "Vikaraṇa — Stem-forming",           "items": _py_items(["Sap", "yak", "Ric"])},
        {"group": "Upasarga — Preverbs",               "items": _py_items(["pra", "upa", "ava", "ud", "ati", "AN", "mAN"])},
        {"group": "Gender / number markers",           "items": _py_items(["pum_abs", "napum_abs", "strI_abs"])},
        {"group": "Special",                           "items": _py_items(["Si", "OS", "adaq", "luk_sup", "luk", "UW"])},
    ]

    _common_dhatus = ["BU", "as_dhatu", "iR", "sTA", "ji", "vid", "vah",
                      "duh", "mud", "Sam", "Cad", "kzI", "lUY"]
    _specific_dhatus = ["dfS", "spfS", "han", "aYc_u", "eDa", "fcCa",
                        "gfj", "guhU", "qukrIY", "qulaBaz", "veY", "veY_smp"]
    dhatu_groups = [
        {"group": "Common roots",   "items": [[k, _DHATU_CATALOG[k][1]] for k in _common_dhatus if k in _DHATU_CATALOG]},
        {"group": "Specific roots", "items": [[k, _DHATU_CATALOG[k][1]] for k in _specific_dhatus if k in _DHATU_CATALOG]},
    ]

    return jsonify({
        "pratipadika": pratipadika_groups,
        "pratyaya":    pratyaya_groups,
        "dhatu":       dhatu_groups,
    })


@app.route("/api/run", methods=["POST"])
def api_run():
    body         = request.get_json(force=True) or {}
    tokens       = body.get("tokens", [])
    mode         = body.get("mode", "single")
    enc_name     = body.get("encoding", "devanagari")
    tag_display  = bool(body.get("tags", False))
    capture_eval = bool(body.get("eval", False))

    if not tokens:
        return jsonify({"error": "No tokens provided"}), 400

    enc = ENCODING_MAP.get(enc_name, sanscript.DEVANAGARI)

    try:
        objects = _resolve_token_list(tokens)
    except (KeyError, ValueError) as exc:
        return jsonify({"error": f"Token error: {exc}"}), 400

    try:
        if mode == "vibhakti":
            table, traces, eval_logs_grid = _generate_table_from_plist(
                objects, enc, tag_display=tag_display, capture_eval=capture_eval)
            return jsonify({
                "mode":      "vibhakti",
                "enc":       enc_name,
                "table":     table,
                "traces":    traces,
                "eval_logs": eval_logs_grid if capture_eval else None,
                "vibhaktis": VIBHAKTI_NAMES,
                "vacanas":   VACANA_NAMES,
            })
        else:  # single
            forms, trace, eval_logs = _run_single_form(
                objects, enc, tag_display=tag_display, capture_eval=capture_eval)
            return jsonify({
                "mode":      "single",
                "enc":       enc_name,
                "forms":     forms,
                "trace":     trace,
                "eval_logs": eval_logs if capture_eval else None,
            })
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": str(exc)}), 500


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Sanskrit Generator Web UI")
    parser.add_argument("--port", type=int, default=5001,
                        help="Port to listen on (default 5001)")
    parser.add_argument("--debug", action="store_true",
                        help="Enable Flask debug mode")
    args = parser.parse_args()

    print(f"\nSanskrit Generator UI  →  http://localhost:{args.port}\n")
    app.run(port=args.port, debug=args.debug)
