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
    ftvij_kvin, sraj_kvin, yuj_kvin, diS_kvin,
    daDfc_kvin, tiryac_kvin,
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
    sIman, bahu, pAd_ut,
    # SK463 ka-pratyaya stem (asuwapaH demo) + raw pieces (bahuvrIhi propagation)
    parivrAjaka, pari, vrAja,
    # SK470/471 taddhita-ṅīp test bases
    indra, utsa, paYca, garga,
    vidyA, kuru, car, suparRA, akza, lavaRa,
    # SK476 (lohitādi) ṣpha test base
    lohita,
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
    # SK470 taddhita ṅīp-triggering affixes
    aY_t, dvayasac, daGnac, mAtrac, tayap, kvarap, Qhak, Wak, WaY,
    # SK473 ṣpha taddhita (with फ → आयन् via 7.1.2)
    sPa,
    # ka-pratyaya taddhita (SK463/464)
    kan,
    # ti taddhita (SK531 yuvan → yuvati) + taddhita-luk (SK480 dvigu)
    ti_t, luk_tadDita,
    # van-class kṛt
    vanip,
    # luk / UW
    luk, UW,
)
from sanskrit_parser.generator.dhatu import (  # noqa: E402
    dfS, aYc_u, han, spfS,
    BU, iR, sTA, ji, vid, kzI, lUY, vah, duh, mud, Cad, Sam,
    eDa, fcCa, gfj, guhU, qukrIY, qulaBaz, veY, veY_smp, as_dhatu,
    Sf, naS,
)
from sanskrit_parser.generator.sutras_yaml import SutraFactory          # noqa: E402
from sanskrit_parser.generator.prakriya_factory import PrakriyaFactory  # noqa: E402
from sanskrit_parser.generator.prakriya import PrakriyaVakya            # noqa: E402
from sanskrit_parser.generator.antaranga_prakriya import AntarangaPrakriya  # noqa: E402
from sanskrit_parser.generator.paninian_object import PaninianObject        # noqa: E402

# Kāraka layer (karaka_plan.md §4 — Vākya Composer). The composer builds tagged
# sentences by introspecting the same generator modules the test driver uses, so
# whole modules are imported here (not just the curated globals above).
import os                                                                   # noqa: E402
from copy import deepcopy                                                   # noqa: E402
import sanskrit_parser.generator.dhatu as _dhatu_module                     # noqa: E402
import sanskrit_parser.generator.avyaya as _avyaya_module                   # noqa: E402

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
_udac_cpd      = [ud,    su, aYc_u, kvin]
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
_bahuyajvan_strI_cpd = [as_purva_pada(bahu), luk_sup,
                        in_context(in_compound(yajvan), "bahuvrIhi"), strI_abs]  # SK460/461 an-bahuvrīhi (live)
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

# SK470/471 (4.1.15/16) taddhita-ṅīp demos — a-final taddhita stems → ṅīp (nadī-type)
_aindra_strI_cpd = [indra, aR_t, strI_abs]            # SK470 aṇ → ऐन्द्री
_autsa_strI_cpd  = [utsa, aY_t, strI_abs]             # SK470 añ → औत्सी
_paYcatayI_cpd   = [paYca, tayap, strI_abs]           # SK470 tayap → पञ्चतयी
_yAdfSI_cpd      = [yad, su, in_compound(dfS), kaY, strI_abs]  # SK470 kañ → यादृशी
_gArgI_cpd       = [garga, yaY_t, strI_abs]           # SK471+SK472 yañ → गार्गी
_kurucarI_cpd    = [as_purva_pada(kuru), luk_sup, in_compound(car), wac, strI_abs]  # SK470 ṭiṭ → कुरुचरी
_naSvarI_cpd     = [naS, kvarap, strI_abs]            # SK470 kvarap → नश्वरी
_vEdyI_cpd       = [vidyA, aR_t, strI_abs]            # SK472 negative: base-ya → वैद्यी
_suparReyI_cpd   = [suparRA, Qhak, strI_abs]          # SK470 ḍha (PARTIAL): SK475 ḍh→eya → सुपर्णेयी
_lAvaRikI_cpd    = [lavaRa, WaY, strI_abs]            # SK470 ṭhañ → लावणिकी (complete)
_akzikI_cpd      = [akza, Wak, strI_abs]              # SK470 ṭhak (PARTIAL): अक्षिकी (vṛddhi pending)
# SK473/476/477 ṣpha-stem strī forms — driven by 6.4.22 ābhīya asiddhavat
# (148+150 compose for gārgī; 134 blocked from 148's output for the
# -āyana stems' acc/ins/etc. surfaces).
_gArgyAyaRI_cpd  = [garga, yaY_t, sPa, strI_abs]      # SK473 + SK475 → गार्ग्यायणी
_lOhityAyanI_cpd = [lohita, yaY_t, sPa, strI_abs]     # SK476 → लौहित्यायनी
_kOravyAyaRI_cpd = [kuru, yaY_t, sPa, strI_abs]       # SK477 → कौरव्यायणी

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
    ("aindra_strI", _aindra_strI_cpd, "Strī-pratyaya (SK469-472 taddhita-ṅīp)", "aindrī  (SK470 aṇ)"),
    ("autsa_strI",  _autsa_strI_cpd,  "Strī-pratyaya (SK469-472 taddhita-ṅīp)", "autsī  (SK470 añ)"),
    ("paYcatayI",   _paYcatayI_cpd,   "Strī-pratyaya (SK469-472 taddhita-ṅīp)", "pañcatayī  (SK470 tayap)"),
    ("yAdfSI",      _yAdfSI_cpd,      "Strī-pratyaya (SK469-472 taddhita-ṅīp)", "yādṛśī  (SK470 kañ)"),
    ("gArgI",       _gArgI_cpd,       "Strī-pratyaya (SK469-472 taddhita-ṅīp)", "gārgī  (SK471 yañ + SK472 ya-lopa)"),
    ("kurucarI",    _kurucarI_cpd,    "Strī-pratyaya (SK469-472 taddhita-ṅīp)", "kurucarī  (SK470 ṭiṭ, +w via wac)"),
    ("naSvarI",     _naSvarI_cpd,     "Strī-pratyaya (SK469-472 taddhita-ṅīp)", "naśvarī  (SK470 kvarap)"),
    ("vEdyI",       _vEdyI_cpd,       "Strī-pratyaya (SK469-472 taddhita-ṅīp)", "vaidyī  (SK472 negative: base-ya not elided)"),
    ("suparReyI",   _suparReyI_cpd,   "Strī-pratyaya (SK469-472 taddhita-ṅīp)", "sauparṇeyī  (SK470 ḍha; 7.1.2 ḍh→eya + 7.2.118 vṛddhi)"),
    ("lAvaRikI",    _lAvaRikI_cpd,    "Strī-pratyaya (SK469-472 taddhita-ṅīp)", "lāvaṇikī  (SK470 ṭhañ; 7.3.50 ṭha→ika)"),
    ("akzikI",      _akzikI_cpd,      "Strī-pratyaya (SK469-472 taddhita-ṅīp)", "ākṣikī  (SK470 ṭhak; 7.3.50 + 7.2.118 vṛddhi)"),
    ("gArgyAyaRI",  _gArgyAyaRI_cpd,  "Strī-pratyaya (SK473-477 ṣpha)",          "gārgyāyaṇī  (SK473 ṣpha + SK475 फ→आयन्; 6.4.22 asiddhavat composes 148+150)"),
    ("lOhityAyanI", _lOhityAyanI_cpd, "Strī-pratyaya (SK473-477 ṣpha)",          "lauhityāyanī  (SK476 lohitādi: ṣpha obligatory)"),
    ("kOravyAyaRI", _kOravyAyaRI_cpd, "Strī-pratyaya (SK473-477 ṣpha)",          "kauravyāyaṇī  (SK477 kuru/maṇḍūka: ṣpha obligatory)"),

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
    ("tiryac",   tiryac_kvin, "kvin-stems",       "tiryañc  (tiryac-)  [SK361 aYc]"),
    # (yuj-in-compound demo lives under the samāsa group as "aSvayuj")
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
# Auto-register the remaining strī-pratyaya stems from the test data
# ---------------------------------------------------------------------------
# The test suite's vibhaktis_list.py maintains `prAtipadika[key] = composition`
# for every tested stem, built from the same generator objects this UI imports.
# The hand-curated _STEMS_RAW above only demos SK454-477; here we pull in every
# *other* feminine composition (those ending in the strI_abs marker) so the whole
# 4.1.x strī chapter (through SK531) is browsable without duplicating the
# compositions. This stays in sync with the test suite automatically.
try:
    from sanskrit_parser.generator.test.vibhaktis_list import (  # noqa: E402
        prAtipadika as _TEST_STEMS,
    )
except Exception as _exc:  # noqa: BLE001
    logging.getLogger(__name__).warning(
        "Could not import test stem catalogue (strī auto-registration skipped): %s", _exc)
    _TEST_STEMS = {}

def _deva(slp1):
    return sanscript.transliterate(slp1, sanscript.SLP1, sanscript.DEVANAGARI)


# Reverse map: canonical base name → the clean module-level Pratipadika global.
# Used to expose the *base* stems of strī compositions in the builder so the
# "+ strī" toggle has something to attach to (Pratyaya is a disjoint class, so
# bases are exactly the Pratipadika-but-not-Pratyaya elements).
from sanskrit_parser.generator.pratipadika import Pratipadika as _Pratipadika  # noqa: E402
from sanskrit_parser.generator.pratyaya import Pratyaya as _Pratyaya          # noqa: E402
import sanskrit_parser.generator.pratipadika as _pp_module                    # noqa: E402

_PP_BY_NAME = {}
for _n, _o in vars(_pp_module).items():
    if isinstance(_o, _Pratipadika) and not isinstance(_o, _Pratyaya):
        _PP_BY_NAME.setdefault(_o.canonical(), _o)

_STRI_GROUP = "Strī-pratyaya (SK478–531, test suite)"
_STRI_BASE_GROUP = "Strī bases (test suite)"
_stri_extra = []
_stri_base_names = set()
for _key, _comp in _TEST_STEMS.items():
    # Feminine compositions are lists ending in the strI_abs marker singleton.
    if not (isinstance(_comp, list) and _comp and _comp[-1] is strI_abs):
        continue
    # Collect the base stems referenced (clean globals, by canonical name).
    for _el in _comp:
        if isinstance(_el, _Pratipadika) and not isinstance(_el, _Pratyaya):
            _cn = _el.canonical()
            if _cn in _PP_BY_NAME:
                _stri_base_names.add(_cn)
    if _key in STEM_MAP:
        continue  # already curated (e.g. the SK454-477 keys) — don't duplicate
    _stri_extra.append((_key, _comp, f"{_deva(_key.split('_')[0])}  ({_key})"))

# Register the full feminine forms (catalogue dropdown).
for _key, _comp, _label in sorted(_stri_extra, key=lambda t: t[0]):
    STEM_MAP[_key] = _comp
    STEM_GROUPS.setdefault(_STRI_GROUP, []).append({"key": _key, "label": _label})

# Register the base stems (single-object → also selectable in the builder picker,
# where they pair with the "+ strī" toggle to derive the feminine).
for _cn in sorted(_stri_base_names):
    if _cn in STEM_MAP:
        continue
    STEM_MAP[_cn] = _PP_BY_NAME[_cn]
    STEM_GROUPS.setdefault(_STRI_BASE_GROUP, []).append(
        {"key": _cn, "label": f"{_deva(_cn)}  ({_cn})"})

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
    # strī-triggering taddhita (combine with strī_abs → ṅīp/ṣpha feminines, SK470-531)
    "aY_t":      (aY_t,      "aÑ — taddhita (-a, SK470 → औत्सी)"),
    "kan":       (kan,       "kan — ka-pratyaya (-ka, SK463 idādeśa)"),
    "dvayasac":  (dvayasac,  "dvayasac — measure taddhita (-dvayasa)"),
    "daGnac":    (daGnac,    "daghnac — measure taddhita (-daghna)"),
    "mAtrac":    (mAtrac,    "mātrac — measure taddhita (-mātra)"),
    "tayap":     (tayap,     "tayap — collective taddhita (-taya, SK470 → पञ्चतयी)"),
    "kvarap":    (kvarap,    "kvarap — kṛt (-vara, SK470 → नश्वरी)"),
    "Qhak":      (Qhak,      "ḍhak — taddhita (ḍha→eya, SK470/475 → सौपर्णेयी)"),
    "Wak":       (Wak,       "ṭhak — taddhita (ṭha→ika + vṛddhi, SK470 → आक्षिकी)"),
    "WaY":       (WaY,       "ṭhañ — taddhita (ṭha→ika + ñit vṛddhi, SK470 → लावणिकी)"),
    "sPa":       (sPa,       "ṣpha — taddhita (फ→आयन्, SK473-477 → गार्ग्यायणी)"),
    "ti_t":      (ti_t,      "ti — taddhita (SK531 yuvan → युवति)"),
    "vanip":     (vanip,     "vanip — van-kṛt (-van, SK456 → शर्वरी)"),
    "luk_tadDita": (luk_tadDita, "luk-taddhita — elided taddhita (SK480 dvigu)"),
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
# Kāraka layer — Vākya Composer (karaka_plan.md §4)
# ---------------------------------------------------------------------------
#
# The kāraka-prakaraṇam (SK532–646) derives a whole sentence in ONE prakriyā:
# a tagging pre-pass assigns kAraka_*/viBakti_* tags, a sup-insertion step turns
# them into case endings, then the existing phonology runs. This section drives
# that pipeline exactly as generator/test/test_karaka.py does (the authoritative
# reference) and presents the result sentence-first instead of table-first.

# --- ground-truth inventories, lifted from the kāraka test data ----------------
# karaka_list.py is pure data (no engine imports); the stems/verbs/particles/
# semantic tags it exercises are precisely the combinations the rules support, so
# the composer dropdowns stay in sync with the rule set automatically.
import sys as _sys                                                          # noqa: E402
_KARAKA_TEST_DIR = os.path.join(os.path.dirname(__file__), "..", "test")
if _KARAKA_TEST_DIR not in _sys.path:
    _sys.path.insert(0, _KARAKA_TEST_DIR)
try:
    from karaka_list import karaka_tests as _KARAKA_TESTS                   # noqa: E402
except Exception as _exc:  # noqa: BLE001
    logging.getLogger(__name__).warning("Could not import karaka_list: %s", _exc)
    _KARAKA_TESTS = []
try:
    from samasa_list import samasa_tests as _SAMASA_TESTS                  # noqa: E402
except Exception as _exc:  # noqa: BLE001
    logging.getLogger(__name__).warning("Could not import samasa_list: %s", _exc)
    _SAMASA_TESTS = []

# Human-readable labels for the semantic primitives the sutras condition on.
# (The sutra wording's primitive — īpsitatama, dhruva-apāya … — never a kāraka
# name; see karaka_plan.md §2.) Unlisted tags fall back to a prettified name.
_SEM_LABELS = {
    "semantic_Ipsitatama":    "īpsitatama — most desired by the agent (→ karma)",
    "semantic_svatantra":     "svatantra — independent (→ kartṛ)",
    "semantic_sADakatama":    "sādhakatama — most effective means (→ karaṇa)",
    "semantic_samboDana":     "sambodhana — one addressed (→ vocative)",
    "semantic_anIpsita":      "anīpsita — undesired, yet reached (→ karma)",
    "semantic_akaTita":       "akathita — the unnamed second karma (dvikarmaka)",
    "semantic_apraDAna":      "apradhāna — subordinate (saha-yoga → tṛtīyā)",
    "semantic_prIyamARa":     "prīyamāṇa — the one pleased (ruc-class → sampradāna)",
    "semantic_DruvApAya":     "dhruva (apāye) — fixed point of separation (→ apādāna)",
    "semantic_Bayahetu":      "bhaya-hetu — cause of fear (→ apādāna)",
    "semantic_asoQa":         "asoḍha — what is not endured (parā-ji → apādāna)",
    "semantic_Ipsita_vAraRa": "īpsita (vāraṇe) — what one is kept from (→ apādāna)",
    "semantic_antardhi":      "antardhi — concealment locus (→ apādāna)",
    "semantic_AKyAtf":        "ākhyātṛ (upayoge) — the teacher learnt from (→ apādāna)",
    "semantic_janiprakfti":   "jani-prakṛti — source of birth (→ apādāna)",
    "semantic_praBava":       "prabhava — point of origin (→ apādāna)",
    "semantic_Seza":          "śeṣa — mere relation, no kāraka (→ ṣaṣṭhī)",
    "semantic_ADAra":         "ādhāra — locus/substratum (→ adhikaraṇa)",
    "semantic_aDikaraRa":     "adhikaraṇa — locus (→ saptamī)",
    "semantic_uttamarRa":     "uttamarṇa — the creditor (dhṛ → sampradāna)",
    "semantic_fRa":           "ṛṇa — debt (akartari → tṛtīyā/ṣaṣṭhī)",
    "semantic_hetu":          "hetu — cause/motive (→ tṛtīyā)",
    "semantic_guRahetu":      "guṇa-hetu — qualitative cause (vibhāṣā)",
    "semantic_aNgavikAra":    "aṅga-vikāra — bodily defect (→ tṛtīyā)",
    "semantic_itTamBUtalakzaRa": "itthambhūta-lakṣaṇa — characterising mark (→ tṛtīyā)",
    "semantic_apavarga":      "apavarga — completion (→ tṛtīyā)",
    "semantic_prAtipadikArTa": "prātipadikārtha — bare stem-meaning (→ prathamā)",
    "semantic_atyantasaMyoga": "atyanta-saṁyoga — uninterrupted extent (kāla/adhvan → dvitīyā)",
    "semantic_kAlADvan":      "kāla/adhvan — time / road extent",
    "semantic_deSakAlAdhvan": "deśa/kāla/adhvan — place/time/road (akarmaka karma)",
    "semantic_nirDAraRa":     "nirdhāraṇa — selection from a group (→ ṣaṣṭhī/saptamī)",
    "semantic_viBakta":       "vibhakta — separated/distinguished (→ pañcamī)",
    "semantic_arcA":          "arcā — esteem (sādhu/nipuṇa → saptamī)",
    "semantic_prasitotsuka":  "prasita/utsuka — engrossed/eager (→ saptamī)",
    "semantic_BAvalakzaRa":   "bhāva-lakṣaṇa — one act marking another (sati-saptamī)",
    "semantic_anAdara":       "anādara — disregard (→ ṣaṣṭhī/saptamī)",
    "semantic_kArakamaDya":   "kāraka-madhye — amid the kārakas (→ saptamī/pañcamī)",
    "semantic_dUrAntika":     "dūra/antika — far / near",
    "semantic_AsevA":         "āsevā — repeated action context",
    "semantic_aBipreta":      "abhipreta — intended recipient",
    "semantic_parikrIta":     "parikrīta — hired (parikrayaṇa, vibhāṣā)",
    "semantic_kopyamAna":     "kopyamāna — the one angered at (krudh-class)",
    "semantic_stokAdi":       "stoka/alpa/kṛcchra/katipaya — small-quantity karaṇa",
    "semantic_pratidAna":     "pratidāna — return/exchange",
    "semantic_nakzatralup":   "nakṣatra (lupi) — asterism with luk",
    # particle (karmapravacanīya) senses
    "semantic_lakzaRa":       "lakṣaṇa — sign/along (karmapravacanīya)",
    "semantic_itTamBUta":     "itthambhūta — characterised state",
    "semantic_hIna":          "hīna — short of / below",
    "semantic_aDika":         "adhika — in excess of",
    "semantic_varjana":       "varjana — exclusion (apa/pari)",
    "semantic_maryAdA":       "maryādā — limit (āṅ)",
    "semantic_pratiniDi":     "pratinidhi — substitution (prati)",
    "semantic_atikramaRa":    "atikramaṇa — surpassing",
    "semantic_pUjA":          "pūjā — honour (api)",
    "semantic_saMBAvanA":     "sambhāvanā — esteeming/inclusion",
    "semantic_ESvara":        "aiśvarya — lordship (adhi → īśvara)",
    "semantic_tftIyArTa":     "tṛtīyā-artha — instrumental sense",
}


def _sem_label(tag):
    if tag in _SEM_LABELS:
        return _SEM_LABELS[tag]
    return tag[len("semantic_"):] if tag.startswith("semantic_") else tag


def _obj_deva(obj):
    """Devanagari surface of a generator object (best-effort)."""
    try:
        return sanscript.transliterate(obj.canonical(), sanscript.SLP1, sanscript.DEVANAGARI)
    except Exception:  # noqa: BLE001
        return str(obj)


_PRAYOGAS = ("kartari", "karmaRi", "BAve")
_STRUCTURAL_VERB_TAGS = {"pada", "tiNanta", *_PRAYOGAS}


def _build_karaka_inventories():
    """Build the composer dropdown inventories from the kāraka test corpus.

    Returns dicts of:
      stems     : sorted [{name, deva}]
      verbs     : sorted [{name, deva, prayoga, meaning}]
      particles : sorted [{name, deva}]
      sem_tags  : ordered [{tag, label}]   (noun semantic primitives)
      psem_tags : ordered [{tag, label}]   (particle karmapravacanīya senses)
    """
    stems, verbs, words, sems, psems = set(), set(), set(), set(), set()
    for c in _KARAKA_TESTS:
        for w in c["sentence"]:
            if "stem" in w:
                stems.add(w["stem"]); sems.update(w.get("sem", []))
            elif "verb" in w:
                verbs.add(w["verb"])
            elif "word" in w:
                words.add(w["word"]); psems.update(w.get("sem", []))

    stem_items = []
    for n in sorted(stems):
        obj = getattr(_pp_module, n, None)
        if obj is not None:
            stem_items.append({"name": n, "deva": _obj_deva(obj)})

    verb_items = []
    for n in sorted(verbs):
        obj = getattr(_dhatu_module, n, None)
        if obj is None:
            continue
        prayoga = next((t for t in obj.tags if t in _PRAYOGAS), "")
        meaning = sorted(t for t in obj.tags if t not in _STRUCTURAL_VERB_TAGS)
        verb_items.append({"name": n, "deva": _obj_deva(obj),
                           "prayoga": prayoga, "meaning": meaning})

    particle_items = []
    for n in sorted(words):
        obj = getattr(_avyaya_module, n, None)
        if obj is not None:
            particle_items.append({"name": n, "deva": _obj_deva(obj)})

    # Samāsa inventory: the avyayas (pūrva/uttara), stems and senses used by the
    # avyayībhāva cases — merged into the stem/particle dropdowns, plus a
    # dedicated samāsa-sense list for the composer's samāsa toggle.
    sam_words, sam_stems, sam_sems = set(), set(), set()
    for c in _SAMASA_TESTS:
        for m in (c.get("purva"), c.get("uttara")):
            if not m:
                continue
            if "avyaya" in m:
                sam_words.add(m["avyaya"])
            elif "stem" in m:
                sam_stems.add(m["stem"])
            if m.get("sem"):
                sam_sems.add(m["sem"])
    for n in sorted(sam_words):
        obj = getattr(_avyaya_module, n, None)
        if obj is not None and not any(p["name"] == n for p in particle_items):
            particle_items.append({"name": n, "deva": _obj_deva(obj)})
    for n in sorted(sam_stems):
        obj = getattr(_pp_module, n, None)
        if obj is not None and not any(s["name"] == n for s in stem_items):
            stem_items.append({"name": n, "deva": _obj_deva(obj)})
    particle_items.sort(key=lambda d: d["name"])
    stem_items.sort(key=lambda d: d["name"])

    sem_items = [{"tag": t, "label": _sem_label(t)} for t in sorted(sems)]
    psem_items = [{"tag": t, "label": _sem_label(t)} for t in sorted(psems)]
    sam_sem_items = [{"tag": t, "label": _sem_label(t)} for t in sorted(sam_sems)]
    return {
        "stems":     stem_items,
        "verbs":     verb_items,
        "particles": particle_items,
        "sem_tags":  sem_items,
        "psem_tags": psem_items,
        "sam_sem_tags": sam_sem_items,
    }


KARAKA_INVENTORIES = _build_karaka_inventories()

# aps → sutra text (the engine stores names in SLP1; show them in Devanagari).
_APS_TO_TEXT = {}
for _s in sutra_list:
    try:
        _APS_TO_TEXT[_s.aps] = sanscript.transliterate(
            str(_s.name), sanscript.SLP1, sanscript.DEVANAGARI)
    except Exception:  # noqa: BLE001
        pass

# aps → SK number, parsed from the §7 table in karaka_plan.md (rows like
# "| K0 | 532 | 2.3.46 |"). Best-effort: a parse miss just drops the SK label.
_APS_TO_SK = {}
try:
    import re as _re
    _plan_path = os.path.join(os.path.dirname(__file__), "..", "karaka_plan.md")
    with open(_plan_path, encoding="utf-8") as _pf:
        for _m in _re.finditer(r"\|\s*K\S*\s*\|\s*(\d+)\s*\|\s*([\d.]+)\s*\|", _pf.read()):
            _APS_TO_SK[_m.group(2)] = f"SK{_m.group(1)}"
except Exception as _exc:  # noqa: BLE001
    logging.getLogger(__name__).warning("Could not parse SK map from karaka_plan.md: %s", _exc)


def _aps_key(aps):
    """Sort key for an aps id like '1.4.49' → (1, 4, 49)."""
    try:
        return tuple(int(x) for x in aps.split("."))
    except Exception:  # noqa: BLE001
        return (9999,)


def _yoga_dir_tag(spec):
    """yoga_pUrva/yoga_para for a non-kp yoga-word's user-chosen governance
    direction: pūrva governs the preceding noun (the word is the noun's rrp),
    para the following (the word is the noun's llp). Returns None when the spec
    carries no "dir". Mirrors test_karaka.py:_yoga_dir_tag."""
    d = spec.get("dir")
    if d is None:
        return None
    return "yoga_pUrva" if d == "pUrva" else "yoga_para"


def _build_word(spec):
    """Turn one sentence-element spec into a tagged PaninianObject.

    1:1 mirror of generator/test/test_karaka.py:_build_word. Three shapes:
      {"stem", "vacana", "sem":[...], "dir":...} → pratipadika + vacana_N +
          semantic_* tags; an optional governance direction when the noun is
          itself a nominal yoga-word (anya/namas/svāmin/dik/prasita/utsuka…)
          → yoga_pUrva/yoga_para.
      {"verb"}                         → pre-formed tiṅanta pada (carries prayoga)
      {"word", "sem":[...], "dir":...} → avyaya particle + optional sense tags +
          optional governance direction. A karmapravacanīya (sense present) maps
          the direction to kp_pUrva/kp_para (default "pUrva"); a sense-less
          yoga-word particle (saha/dakṣiṇataḥ/hetoḥ…) maps it to yoga_pUrva/
          yoga_para; a plain particle (he) with no sense and no dir gets neither.
    """
    # A samāsa member carries the ?samAsa_vivakza intent tag (the samāsa
    # pre-pass scans for it); an avyaya member skips the karmapravacanīya tags.
    samasa = bool(spec.get("samasa"))
    if "stem" in spec:
        obj = getattr(_pp_module, spec["stem"], None)
        if obj is None:
            raise KeyError(f"Unknown stem {spec['stem']!r}")
        p = deepcopy(obj)
        p.setTag(f"vacana_{int(spec.get('vacana', 1))}")
        for t in spec.get("sem", []):
            p.setTag(t)
        if int(spec.get("vibhakti", 0)):   # a pre-supplied external vibhakti (2.4.84)
            p.setTag(f"viBakti_{int(spec['vibhakti'])}")
            p.setTag("has_viBakti")
        yt = _yoga_dir_tag(spec)
        if yt is not None:
            p.setTag(yt)
        if samasa:
            p.setTag("samAsa_vivakza")
        return p
    if "verb" in spec:
        obj = getattr(_dhatu_module, spec["verb"], None)
        if obj is None:
            raise KeyError(f"Unknown verb {spec['verb']!r}")
        return deepcopy(obj)
    if "word" in spec:
        obj = getattr(_avyaya_module, spec["word"], None)
        if obj is None:
            raise KeyError(f"Unknown particle {spec['word']!r}")
        p = deepcopy(obj)
        sems = spec.get("sem", [])
        for t in sems:
            p.setTag(t)
        if samasa:
            # samāsa avyaya member: intent tag + kp_para (it governs the
            # FOLLOWING uttara). For a kp sense (apa/pari varjana, āṅ maryAdā)
            # this lets the kāraka layer assign the noun pañcamī (1.4.88/89 →
            # 2.3.10 → viBakti_5) which 2.1.12/2.1.13 require; for a non-kp sense
            # (samīpa etc.) a bare kp_para is inert.
            p.setTag("samAsa_vivakza")
            p.setTag("kp_para")
        elif sems:
            # karmapravacanīya: direction is a user choice, default "pUrva".
            direction = spec.get("dir") or "pUrva"
            p.setTag("kp_pUrva" if direction == "pUrva" else "kp_para")
        else:
            # sense-less yoga-word particle: yoga_* only when a dir is given.
            yt = _yoga_dir_tag(spec)
            if yt is not None:
                p.setTag(yt)
        return p
    raise ValueError(f"Unknown word spec {spec!r}")


def _obj_enc(obj, enc):
    """Window object → target-encoding string (skip None/list/markers)."""
    if obj is None or isinstance(obj, list):
        return ""
    slp1 = obj.transcoded(sanscript.SLP1) if hasattr(obj, "transcoded") else str(obj)
    if not slp1.strip("."):
        return ""
    return sanscript.transliterate(slp1, sanscript.SLP1, enc)


def _node_window_tags(node):
    """In/out window object tags for one PrakriyaNode (for the tag display)."""
    ix = node.index

    def tg(seq, k):
        obj = seq[k] if 0 <= k < len(seq) else None
        if obj is None or isinstance(obj, list):
            return None
        return sorted(obj.tags) if getattr(obj, "tags", None) else []

    return {"in_l": tg(node.inputs, ix), "in_r": tg(node.inputs, ix + 1),
            "out_l": tg(node.outputs, ix), "out_r": tg(node.outputs, ix + 1)}


def _eval_summary(eval_log):
    """Compact view of a node's eval_log: which sutras matched at this window.
    Mirrors the data the declension explorer captures (condition_pass / disabled
    / priority). Returns {candidates:[{aps,dev,fired,disabled_by}], n_evaluated}."""
    if not eval_log:
        return None
    cands = []
    for rec in eval_log.get("sutras", []):
        if rec.get("condition_pass"):
            cands.append({"aps": rec["aps"], "dev": rec.get("dev", ""),
                          "disabled_by": rec.get("disabled_by")})
    return {"candidates": cands, "n_evaluated": len(eval_log.get("sutras", []))}


def _collect_phon_steps(tree, enc, want_tags, want_eval):
    """DFS-walk a PrakriyaTree collecting the (phonological/main-scan) sutra
    firings — everything the kāraka pre-pass does NOT cover. Deduplicates
    identical (aps, before, after) steps so vibhāṣā branches don't repeat the
    shared phonology. Returns an ordered list of step dicts."""
    steps, seen = [], set()

    def visit(n):
        s = getattr(n, "sutra", None)
        if s is not None and not isinstance(s, str) and getattr(s, "aps", None) not in (None, "0.0.0"):
            ix = n.index
            f = " | ".join(x for x in (_obj_enc(n.inputs[ix] if ix < len(n.inputs) else None, enc),
                                       _obj_enc(n.inputs[ix + 1] if ix + 1 < len(n.inputs) else None, enc)) if x)
            t = " | ".join(x for x in (_obj_enc(n.outputs[ix] if ix < len(n.outputs) else None, enc),
                                       _obj_enc(n.outputs[ix + 1] if ix + 1 < len(n.outputs) else None, enc)) if x)
            key = (s.aps, f, t)
            if key not in seen:
                seen.add(key)
                step = {"aps": s.aps, "name": s.name.devanagari(),
                        "opt": bool(getattr(s, "optional", False)),
                        "from": f, "to": t, "changed": f != t}
                if want_tags:
                    step["tags"] = _node_window_tags(n)
                if want_eval:
                    step["eval"] = _eval_summary(getattr(n, "eval_log", None))
                steps.append(step)
        for c in tree.children.get(n, []):
            visit(c)

    for r in tree.get_root():
        visit(r)
    return steps


def run_karaka(sentence, enc, want_tags=False, want_eval=False, sandhi=False):
    """Build the tagged vākya, run the engine, and read back per-word kāraka/
    vibhakti, the vibhāṣā branch sentences, the fired kāraka-sutra trace, and the
    phonological (non-kāraka) sutra steps (with optional per-step tags/eval).

    With sandhi=False (default) each word is followed by its own avasAna, so the
    words stay isolated (no inter-word sandhi) and the joined output splits cleanly
    into per-word forms. With sandhi=True only a single trailing avasAna is added,
    so adjacent words sandhi together — but the fused output can no longer be split,
    so per-word/compound surface forms are omitted (only the derived sentence(s)).

    Returns {words, branches, fired, phon, compounds}. Raises on a bad spec.
    """
    # 1. Build [Adya, w0, avasAna, w1, avasAna, …]; record each word's index.
    #    Compound grouping: a maximal run of consecutive specs flagged "samasa"
    #    forms ONE compound — its members sit adjacent (no avasAna between), so
    #    the samāsa pre-pass + main scan combine them. Every other boundary gets
    #    an avasAna. With no samāsa specs this is the original per-word build.
    #    In sandhi mode we drop the internal avasAnas (only a trailing one below)
    #    so every boundary is a saMhitā juncture where inter-word sandhi applies.
    pl = [Adya]
    word_ix = []
    groups = []   # list of [spec_index, …]; one entry per surface piece
    for si, spec in enumerate(sentence):
        word_ix.append(len(pl))
        pl.append(_build_word(spec))
        prev_same = spec.get("samasa") and si > 0 and sentence[si - 1].get("samasa")
        (groups[-1].append(si) if prev_same else groups.append([si]))
        next_same = (spec.get("samasa") and si + 1 < len(sentence)
                     and sentence[si + 1].get("samasa"))
        if not sandhi and not next_same:
            pl.append(avasAna)
    if sandhi:
        pl.append(avasAna)
    p = AntarangaPrakriya(sutra_list, PrakriyaVakya(pl), capture_eval=want_eval)
    p.execute()

    # 2. Aggregate the pre-pass log by word index, unioning across vibhāṣā
    #    branches (exactly as test_karaka.py does).
    agg = {}
    for e in p.karaka_log:
        a = agg.setdefault(e["index"], {"tags": set(), "fired": set()})
        a["tags"].update(e["tags"])
        a["fired"].update(e["fired"])

    # 3. Per-branch surface sentences + per-position form sets. Splitting the
    #    joined SLP1 on the avasAna marker recovers one piece per GROUP (a
    #    compound is one piece); each piece's form attaches to every member of
    #    its group (Adya contributes nothing).
    sep = avasAna.canonical()
    group_forms = [set() for _ in groups]
    branches, seen = [], set()
    for o in p.output():
        slp = "".join(x.transcoded(sanscript.SLP1) for x in list(o))
        pieces = [w for w in slp.split(sep) if w != ""]
        # In sandhi mode there is a single fused piece — it is the derived
        # sentence, but it cannot be split back into per-word/compound forms.
        if not sandhi:
            for gi, w in enumerate(pieces):
                if gi < len(group_forms):
                    group_forms[gi].add(sanscript.transliterate(w, sanscript.SLP1, enc))
        sent = " ".join(sanscript.transliterate(w, sanscript.SLP1, enc) for w in pieces)
        if sent not in seen:
            seen.add(sent)
            branches.append(sent)
    # Per-spec forms: a compound's surface attaches to each of its members. Left
    # empty in sandhi mode (group_forms unpopulated — the fused output can't split).
    pos_forms = [set() for _ in sentence]
    for gi, grp in enumerate(groups):
        for si in grp:
            pos_forms[si] = group_forms[gi]

    _SAMASA_ROLE = ("samAsa", "samAsaPurva", "upasarjana",
                    "avyayIBAva", "bahuvrIhi", "dvigu",
                    "tatpuruza", "karmaDAraya")

    # Per-spec samāsa role tags: read from the final pre-pass branch by member
    # order (the samāsa pre-pass logs POST-sup-insertion indices, which don't
    # line up with word_ix, so karaka_log is unreliable for the role tags). The
    # k-th prātipadika member in the branch is the k-th non-verb spec.
    samasa_by_spec = {}
    if any(sp.get("samasa") for sp in sentence):
        branch = (getattr(p, "_karaka_branches", None) or [None])[0]
        if branch is not None:
            # A declining compound (tatpuruṣa) nests its members into a sub-list
            # (_nest_samasa_members → one samasta_pada), so flatten one level
            # before scanning for member objects (avyayībhāva stays flat).
            flat = []
            for o in branch:
                flat.extend(o if isinstance(o, list) else [o])
            members = [o for o in flat
                       if getattr(o, "hasTag", None) and o.canonical()
                       and o.hasTag("prAtipadika") and not o.hasTag("sup")
                       and not o.hasTag("tiNanta")]
            non_verb = [i for i, sp in enumerate(sentence) if "verb" not in sp]
            for k, si in enumerate(non_verb):
                if k < len(members):
                    samasa_by_spec[si] = sorted(
                        t for t in members[k].tags if t in _SAMASA_ROLE)

    # 4. Per-word view.
    words_out = []
    for i, spec in enumerate(sentence):
        entry = agg.get(word_ix[i], {"tags": set(), "fired": set()})
        karakas = sorted(t for t in entry["tags"] if t.startswith("kAraka_"))
        vibhaktis = sorted(
            (t for t in entry["tags"] if t.startswith("viBakti_") and t[8:].isdigit()),
            key=lambda t: int(t[8:]))
        samasa = samasa_by_spec.get(
            i, sorted(t for t in entry["tags"] if t in _SAMASA_ROLE))
        words_out.append({
            "input":   _spec_label(spec, enc),
            "kind":    "verb" if "verb" in spec else ("particle" if "word" in spec else "noun"),
            "karaka":  karakas,
            "vibhakti": vibhaktis,
            "samasa":  samasa,
            "forms":   sorted(pos_forms[i]),
            "fired":   sorted(entry["fired"], key=_aps_key),
        })

    # 4b. Compound view: one entry per multi-member group (the samāsa output).
    compounds = []
    for gi, grp in enumerate(groups):
        if len(grp) < 2:
            continue
        ctype = sorted({t for si in grp for t in samasa_by_spec.get(si, [])
                        if t in ("avyayIBAva", "bahuvrIhi", "dvigu",
                                 "tatpuruza", "karmaDAraya")})
        compounds.append({
            "members": [_spec_label(sentence[si], enc) for si in grp],
            "type":    ctype,
            "surface": sorted(group_forms[gi]),
        })

    fired_all = sorted({a for e in agg.values() for a in e["fired"]}, key=_aps_key)
    fired_out = [{"aps": a, "sk": _APS_TO_SK.get(a), "text": _APS_TO_TEXT.get(a, "")}
                 for a in fired_all]

    # 5. Phonological (non-kāraka) sutra steps from the main derivation tree,
    #    plus any inner (compound) prakriyās — the same trace the declension
    #    explorer shows, scoped to whatever the kāraka pre-pass did not do.
    phon = _collect_phon_steps(p.tree, enc, want_tags, want_eval)
    for hp in getattr(p, "hier_prakriyas", []):
        if getattr(hp, "tree", None) is not None:
            phon.extend(_collect_phon_steps(hp.tree, enc, want_tags, want_eval))

    return {"words": words_out, "branches": branches, "fired": fired_out,
            "phon": phon, "compounds": compounds}


def _spec_label(spec, enc):
    """Readable label for a sentence-element spec (input word, in target enc)."""
    if "verb" in spec:
        obj = getattr(_dhatu_module, spec["verb"], None)
    elif "word" in spec:
        obj = getattr(_avyaya_module, spec["word"], None)
    else:
        obj = getattr(_pp_module, spec.get("stem", ""), None)
    if obj is None:
        return spec.get("stem") or spec.get("verb") or spec.get("word") or "?"
    try:
        return sanscript.transliterate(obj.canonical(), sanscript.SLP1, enc)
    except Exception:  # noqa: BLE001
        return _obj_deva(obj)


def _expected_karaka_set(exp):
    k = exp.get("karaka", None)
    if k is None:
        return set()
    return {k} if isinstance(k, str) else set(k)


_KARAKA_CASES_CACHE = {}


def _run_karaka_cases(enc):
    """Run every karaka_list.py case through the engine and tag each with a
    pass/fail status (saṁjñā + vibhakti + fired-trace, mirroring test_karaka.py).
    Cached per-encoding after first build (one engine run per case)."""
    if enc in _KARAKA_CASES_CACHE:
        return _KARAKA_CASES_CACHE[enc]

    results = []
    n_pass = 0
    for case in _KARAKA_TESTS:
        row = {"label": case["label"], "sutras": case.get("sutras", []),
               "sentence": case["sentence"],   # raw spec → composer prefill
               "words": [], "branches": [], "status": "pass", "reason": ""}
        try:
            res = run_karaka(case["sentence"], enc)
        except Exception as exc:  # noqa: BLE001
            row["status"] = "error"
            row["reason"] = str(exc)
            results.append(row)
            continue
        row["branches"] = res["branches"]
        fired_all = {f["aps"] for f in res["fired"]}
        # fired-trace check
        missing = [s for s in case.get("sutras", []) if s not in fired_all]
        if missing:
            row["status"] = "fail"
            row["reason"] = f"missing sutras {missing}"
        # per-word saṁjñā / vibhakti check
        for spec, exp, got in zip(case["sentence"], case["expect"], res["words"]):
            exp_k = _expected_karaka_set(exp)
            got_k = set(got["karaka"])
            ok_k = ("karaka" not in exp) or (got_k == exp_k)
            exp_v = set(exp.get("vibhakti", got["vibhakti"]))
            got_v = set(got["vibhakti"])
            ok_v = ("vibhakti" not in exp) or (got_v == exp_v)
            if not (ok_k and ok_v) and row["status"] == "pass":
                row["status"] = "fail"
                row["reason"] = (f"{got['input']}: kāraka {sorted(got_k)}≠{sorted(exp_k)} "
                                 f"or vibhakti {sorted(got_v)}≠{sorted(exp_v)}")
            row["words"].append({
                "input": got["input"], "kind": got["kind"],
                "karaka": got["karaka"], "vibhakti": got["vibhakti"],
                "exp_karaka": sorted(exp_k), "exp_vibhakti": sorted(exp_v),
                "forms": got["forms"], "ok": bool(ok_k and ok_v),
            })
        if row["status"] == "pass":
            n_pass += 1
        results.append(row)

    out = {"cases": results, "n_pass": n_pass, "n_total": len(results)}
    _KARAKA_CASES_CACHE[enc] = out
    return out


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
        {"group": "Strī — Feminine suffixes",          "items": _py_items(["strI_abs", "NIp", "NIz", "Ap"])},
        {"group": "Taddhita — from prātipadika",       "items": _py_items(["yat_t", "zyaY_t", "yaY_t", "aR_t"])},
        {"group": "Taddhita — strī-triggering (combine with strī)", "items": _py_items([
            "aY_t", "kan", "dvayasac", "daGnac", "mAtrac", "tayap", "kvarap",
            "Qhak", "Wak", "WaY", "sPa", "ti_t", "vanip", "luk_tadDita"])},
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
# Kāraka routes (Vākya Composer)
# ---------------------------------------------------------------------------

@app.route("/karaka")
def karaka_page():
    return render_template(
        "karaka.html",
        inventories=KARAKA_INVENTORIES,
        vibhaktis=VIBHAKTI_NAMES,
        vacanas=VACANA_NAMES,
    )


@app.route("/karaka/gallery")
def karaka_gallery_page():
    return render_template("karaka_gallery.html")


@app.route("/api/karaka", methods=["POST"])
def api_karaka():
    body      = request.get_json(force=True) or {}
    sentence  = body.get("sentence", [])
    enc_name  = body.get("encoding", "devanagari")
    want_tags = bool(body.get("tags", False))
    want_eval = bool(body.get("eval", False))
    want_sandhi = bool(body.get("sandhi", False))

    if not sentence:
        return jsonify({"error": "Empty sentence"}), 400

    enc = ENCODING_MAP.get(enc_name, sanscript.DEVANAGARI)
    try:
        result = run_karaka(sentence, enc, want_tags=want_tags, want_eval=want_eval,
                            sandhi=want_sandhi)
    except (KeyError, ValueError) as exc:
        return jsonify({"error": f"Sentence error: {exc}"}), 400
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": str(exc)}), 500

    result["enc"] = enc_name
    return jsonify(result)


@app.route("/api/karaka/cases")
def api_karaka_cases():
    enc_name = request.args.get("encoding", "devanagari")
    enc = ENCODING_MAP.get(enc_name, sanscript.DEVANAGARI)
    try:
        data = _run_karaka_cases(enc)
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": str(exc)}), 500
    return jsonify(data)


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
