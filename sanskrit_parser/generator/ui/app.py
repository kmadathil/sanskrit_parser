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
    vftrahan,
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
    daDfc_kvin, pratyac_kvin, prAc_kvin, udac_kvin, tiryac_kvin,
    takz_kvip, vAh_kvip, praSAm_kvip,
    gaRa, aSva, viSva, rAj_kvip,
    in_compound,
    tri, dvi, dvi_s, catur, kati,
    paYcan, saptan, navan, daSan, azwan, catasf,
    atinO,
    Sreyas, Sreyas_n,
)
from sanskrit_parser.generator.pratyaya import avasAna, sups, pra  # noqa: E402
from sanskrit_parser.generator.sutras_yaml import SutraFactory          # noqa: E402
from sanskrit_parser.generator.prakriya_factory import PrakriyaFactory  # noqa: E402
from sanskrit_parser.generator.prakriya import PrakriyaVakya            # noqa: E402

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

_STEMS_RAW = [
    # ── a / ā stems ───────────────────────────────────────────────────────
    ("rAma",     rAma,        "a-stems (pum)",    "rāma  (rāma-)"),
    ("pAda",     pAda,        "a-stems (pum)",    "pāda  (pāda-)  [pādādi opt]"),
    ("yUza",     yUza,        "a-stems (pum)",    "yūṣa  (yūṣa-)  [pādādi opt]"),
    ("jYAna",    jYAna,       "a-stems (napum)",  "jñāna  (jñāna-)"),
    ("ramA",     ramA,        "ā-stems (strī)",   "ramā  (ramā-)"),
    ("nAsikA",   nAsikA,      "ā-stems (strī)",   "nāsikā  (nāsikā-)  [pādādi]"),
    ("niSA",     niSA,        "ā-stems (strī)",   "niśā  (niśā-)  [pādādi]"),
    ("mahat",    mahat,       "t-stems",          "mahat  (mahat-)"),
    ("mahat_n",  mahat_n,     "t-stems",          "mahat  (mahat-)  [napum]"),
    ("payas",    payas,       "s-stems",          "payas  (payas-)"),

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
    ("vftrahan", vftrahan,    "han-stems",        "vṛtrahān  (vṛtrahān-)  [SK358–359]"),

    # ── napum i-stems ─────────────────────────────────────────────────────
    ("asTi",     asTi,        "i-stems (napum)",  "asthi  (asthi-)"),
    ("daDi",     daDi,        "i-stems (napum)",  "dadhi  (dadhi-)"),
    ("akzi",     akzi,        "i-stems (napum)",  "akṣi  (akṣi-)"),
    ("atinO",    atinO,       "i-stems (napum)",  "atinau  (atinau-)"),

    # ── Pronouns ──────────────────────────────────────────────────────────
    ("kim",      kim,         "Pronouns",         "kim  (kim-)"),
    ("idam",     idam,        "Pronouns",         "idam  (idam-)"),
    ("idam_anu", [idam_anu],  "Pronouns",         "idam  (anvādeśa)"),
    ("sarva",    sarva,       "Pronouns",         "sarva  (sarva-)  [sarvādi]"),
    ("anya",     anya,        "Pronouns",         "anya  (anya-)  [qatarādi]"),
    ("yuzmad",   yuzmad,      "Pronouns",         "yuṣmad  [2nd person]"),
    ("asmad",    asmad,       "Pronouns",         "asmad  [1st person]"),

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
    ("praVAh",   _praVAh_cpd, "kvip-stems",       "pravāh  (pra+vāh-)  [cpd kvip]"),

    # ── kvin-stems (SK373–377) ────────────────────────────────────────────
    ("ftvij",    ftvij_kvin,  "kvin-stems",       "ṛtvij  (ṛtvij-)  [SK373]"),
    ("sraj",     sraj_kvin,   "kvin-stems",       "sraj  (sraj-)  [SK374]"),
    ("yuj",      yuj_kvin,    "kvin-stems",       "yuj  (yuj-)  [SK375]"),
    ("diS",      diS_kvin,    "kvin-stems",       "diś  (diś-)  [SK377]"),
    ("daDfc",    daDfc_kvin,  "kvin-stems",       "dadhṛc  (dadhṛc-)  [c-final]"),
    ("pratyac",  pratyac_kvin,"kvin-stems",       "pratyañc  (pratyac-)  [SK361 aYc]"),
    ("prAc",     prAc_kvin,   "kvin-stems",       "prāñc  (prāc-)  [SK361 aYc]"),
    ("udac",     udac_kvin,   "kvin-stems",       "udañc  (udac-)  [SK361 aYc]"),
    ("tiryac",   tiryac_kvin, "kvin-stems",       "tiryañc  (tiryac-)  [SK361 aYc]"),
    ("yuj_samAsa", [yuj_kvin_samAsa], "kvin-stems", "yuj-in-cpd  [samāsa no nUM]"),

    # ── samāsa (compounds) ────────────────────────────────────────────────
    ("gaRapati",  _gaRapati_cpd,  "samāsa",  "gaṇapati  [SK257 pati-in-cpd]"),
    ("aSvayuj",   _aSvayuj_cpd,   "samāsa",  "aśvayuj  [SK376 yuj-in-cpd]"),
    ("viSvAvasu", _viSvAvasu_cpd, "samāsa",  "viśvāvasu  [SK379]"),
    ("viSvArAj",  _viSvArAj_cpd,  "samāsa",  "viśvārāj  [SK379 rāṭ/rāj forms]"),

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
# Core generation logic
# ---------------------------------------------------------------------------


def _slp1_to_display(slp1_form, enc):
    """Strip avasāna marker and transliterate to target encoding."""
    form = slp1_form.rstrip(".").strip()
    if not form:
        return "—"
    return sanscript.transliterate(form, sanscript.SLP1, enc)


def _generate_cell(plist, sup, enc):
    """
    Run the prakriyā for one declension cell.

    Returns:
        forms  (list[str]) : output form(s) in the requested encoding
        trace  (str)       : multi-line sutra-trace text from p.describe()
    """
    # Compound (multi-element plist) requires hierarchical structure so that
    # pūrva-pada rules (e.g. SK379) fire *after* the uttara-pada + sup merge,
    # matching the test infrastructure: [[*plist, sup], avasāna].
    if len(plist) > 1:
        inputs = [[*plist, sup], avasAna]
    else:
        inputs = [*plist, sup, avasAna]
    pv = PrakriyaVakya(inputs)
    p = PrakriyaFactory("AntarangaPrakriya", sutra_list, pv)
    p.execute()
    output = p.output()

    # Capture describe() which prints to stdout
    buf = io.StringIO()
    with redirect_stdout(buf):
        p.describe()
    trace = buf.getvalue()

    # Convert outputs to display strings
    forms = []
    for o in output:
        slp1 = "".join(obj.transcoded(sanscript.SLP1) for obj in list(o))
        forms.append(_slp1_to_display(slp1, enc))

    return forms, trace


def generate_table(stem_key, enc):
    """
    Generate the full 8×3 declension table for a stem.

    Returns:
        table  : list of 8 rows, each a list of 3 display strings
        traces : matching list of 8 rows × 3 trace strings
    """
    obj = STEM_MAP[stem_key]
    plist = obj if isinstance(obj, list) else [obj]

    # Determine nitya-vacana restrictions
    pratipadika = plist[-1]
    nityaEka  = pratipadika.hasTag("nityEkavacana")
    nityaDvi  = pratipadika.hasTag("nityadvivacana")
    nityaBahu = pratipadika.hasTag("nityabahuvacana")

    table = []
    traces = []
    for vib_idx in range(8):
        row = []
        row_traces = []
        for vac_idx in range(3):
            # Skip non-applicable vacana for nitya stems
            skip = (
                (nityaEka  and vac_idx != 0) or
                (nityaDvi  and vac_idx != 1) or
                (nityaBahu and vac_idx != 2)
            )
            if skip:
                row.append("—")
                row_traces.append("")
                continue

            sup = sups[vib_idx][vac_idx]
            try:
                forms, trace = _generate_cell(plist, sup, enc)
                row.append(" | ".join(forms) if forms else "?")
                row_traces.append(trace)
            except Exception as exc:  # noqa: BLE001
                row.append("[error]")
                row_traces.append(str(exc))

        table.append(row)
        traces.append(row_traces)

    return table, traces


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
    stem_key = request.args.get("stem", "")
    enc_name = request.args.get("encoding", "devanagari")

    if stem_key not in STEM_MAP:
        return jsonify({"error": f"Unknown stem: {stem_key!r}"}), 400

    enc = ENCODING_MAP.get(enc_name, sanscript.DEVANAGARI)

    try:
        table, traces = generate_table(stem_key, enc)
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": str(exc)}), 500

    return jsonify({
        "stem":      stem_key,
        "enc":       enc_name,
        "table":     table,
        "traces":    traces,
        "vibhaktis": VIBHAKTI_NAMES,
        "vacanas":   VACANA_NAMES,
    })


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
