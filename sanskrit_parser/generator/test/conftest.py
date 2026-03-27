import logging
# First we disable the root logger handlers
rootlogger = logging.getLogger()
for h in rootlogger.handlers:
    rootlogger.removeHandler(h)
rootlogger.addHandler(logging.NullHandler())

from sanskrit_parser.generator.paninian_object import PaninianObject
from sanskrit_parser.generator.prakriya import PrakriyaVakya
from sanskrit_parser.generator.prakriya_factory import PrakriyaFactory
from sanskrit_parser.generator.pratyaya import *  # noqa: F403
from indic_transliteration import sanscript

from vibhaktis_list import ajanta, halanta, samAsa, viBakti, prAtipadika, encoding

import pytest

from sanskrit_parser.generator.sutras_yaml import SutraFactory
#sutra_list = SutraFactory("sutras_hier.yaml")
#prakriya_name = "HierPrakriya"
sutra_list = SutraFactory("sutras_antaranga.yaml")
prakriya_name = "AntarangaPrakriya"



# @pytest.fixture(scope="module")
# def sutra_fixture():
#     return sutra_list


def pytest_addoption(parser):
    """Custom options for pytest command line
    """
    # Add an option to limit number of tests generated.
    # # TODO: Solve "ValueError: option names {'--test-count'} already added" below
    # parser.addoption("--test-count", action="store", default=0,
    #                help="Number of tests to generate")
    pass


def get_testcount(config):
    """Gets number of tests to generate.

    :param config: pytest configuration
    """
    return int(config.getoption("--test-count"))


def _test(output, s, enc):
    _s = s[-1]
    if not isinstance(_s, list):
        # Single element
        _s = [_s]
    # Remove spaces in reference
    _s = [sanscript.transliterate(x.replace(' ', ""), enc, sanscript.SLP1) for x in _s]
    j = [
        PaninianObject("".join([
            _o.transcoded(sanscript.SLP1) for _o in list(o)
        ]), encoding=sanscript.SLP1).canonical()
        for o in output
    ]
    if not (set(j) == set(_s)):
        print(f"Got {set(j)} expected {set(_s)}")
    return (set(j) == set(_s))


def run_test(s, sutra_list, encoding=sanscript.SLP1, verbose=False):
    pl = []
    print(f"Testing {s}")
    # Assemble list of inputs
    for i in range(len(s)-1):
        def _gen_obj(s, i):
            if isinstance(s[i], str):
                # Shortcuts for two input tests not using predefined objects
                # If a string in the first place ends with * it's an anga
                # If a string in the first place ends with ! it has no tag (raw phonetic input)
                # Else it's a pada
                # For everything else, use predefined objects
                if (i == 0) and (s[i][-1] == "*"):
                    s0 = s[0][:-1]
                    l = PaninianObject(s0, encoding)  # noqa: E741
                    l.setTag("aNga")
                elif (i == 0) and (s[i][-1] == "!"):
                    s0 = s[0][:-1]
                    l = PaninianObject(s0, encoding)  # noqa: E741
                    # no tag: raw phonetic input, not an anga or pada
                    return l
                else:
                    s0 = s[i]
                    l = PaninianObject(s[i], encoding)  # noqa: E741
                    if i == 0:
                        l.setTag("pada")
                    return l
            elif isinstance(s[i], tuple) or isinstance(s[i], list):
                l = [_gen_obj(s[i], ii) for (ii, ss) in enumerate(s[i])]   # noqa: E741
            else:
                l = s[i]  # noqa: E741
            return l
        l = _gen_obj(s, i)  # noqa: E741
        pl.append(l)
        
    print(f"Canonical Input {pl} - ")
    p = PrakriyaFactory(prakriya_name, sutra_list, PrakriyaVakya(pl))
    p.execute()
    #if verbose:
    #    p.describe()
    o = p.output(copy=True)
    assert _test(o, s, encoding)
    return None


_VIBHAKTI_ROW_NAMES = ["pra", "dvi", "tft", "cat", "paY", "zaz", "sap", "sam"]
_VIBHAKTI_COL_NAMES = ["ek", "dv", "bh"]


def generate_vibhakti(pratipadika_i, vibhaktis, encoding=sanscript.DEVANAGARI, stem_key=None):
    t = []

    # If we get a list, treat as prefixes + prAtipadika
    if isinstance(pratipadika_i, list):
        plist = pratipadika_i
        pratipadika = pratipadika_i[-1]
        # Handle nested lists (e.g. [prati, [aYc_u, kvin]]): drill to innermost scalar
        while isinstance(pratipadika, list):
            pratipadika = pratipadika[-1]
    else:
        plist = [pratipadika_i]
        pratipadika = pratipadika_i

    for ix, pv in enumerate(vibhaktis):
        for jx, pvv in enumerate(pv):
            # For nitya eka/dvi/bahuvacana, generate only the appropriate
            if (((jx == 0) and pratipadika.hasTag("nityEkavacana")) or
                ((jx == 1) and pratipadika.hasTag("nityadvivacana")) or
                ((jx == 2) and pratipadika.hasTag("nityabahuvacana")) or
                (not (pratipadika.hasTag("nityEkavacana") or
                      pratipadika.hasTag("nityadvivacana") or
                      pratipadika.hasTag("nityabahuvacana")))):
                if pvv is None:
                    continue  # Skip cells with no expected form (partial tables)
                if isinstance(pvv, str):
                    _pvv = pvv+avasAna.transcoded(encoding)  # noqa: F405
                else:
                    _pvv = [x+avasAna.transcoded(encoding) for x in pvv]  # noqa: F405
                entry = [(*plist, sups[ix][jx]), avasAna, _pvv]  # noqa: F405
                if stem_key is not None:
                    row = _VIBHAKTI_ROW_NAMES[ix] if ix < len(_VIBHAKTI_ROW_NAMES) else str(ix)
                    col = _VIBHAKTI_COL_NAMES[jx] if jx < len(_VIBHAKTI_COL_NAMES) else str(jx)
                    t.append(pytest.param(entry, id=f"{stem_key}-{row}-{col}"))
                else:
                    t.append(entry)
    return t


# Manual test
def check_vibhakti(t, sutra_list, encoding=sanscript.DEVANAGARI, verbose=False):
    for s in t:
        run_test(s, sutra_list, encoding=encoding, verbose=verbose)


def test_prakriya(sutra_list, test_list, test_list_d, verbose=False):
    for s in test_list:
        run_test(s, sutra_list, sanscript.SLP1, verbose=verbose)
    for s in test_list_d:
        run_test(s, sutra_list, sanscript.DEVANAGARI, verbose=verbose)


def pytest_generate_tests(metafunc):
    if 'halanta_pum' in metafunc.fixturenames:
        halanta_pum_list = []
        for v in halanta["pum"]:
            if (v in encoding) and (encoding[v] == sanscript.SLP1):
                pass
            else:
                halanta_pum_list.extend(generate_vibhakti(prAtipadika[v],
                                                          viBakti[v], stem_key=v))
        metafunc.parametrize("halanta_pum", halanta_pum_list)
    if 'halanta_stri' in metafunc.fixturenames:
        halanta_stri_list = []
        for v in halanta["strI"]:
            if (v in encoding) and (encoding[v] == sanscript.SLP1):
                pass
            else:
                halanta_stri_list.extend(generate_vibhakti(prAtipadika[v],
                                                           viBakti[v], stem_key=v))
        metafunc.parametrize("halanta_stri", halanta_stri_list)
    if 'halanta_napum' in metafunc.fixturenames:
        halanta_napum_list = []
        for v in halanta["napum"]:
            if (v in encoding) and (encoding[v] == sanscript.SLP1):
                pass
            else:
                halanta_napum_list.extend(generate_vibhakti(prAtipadika[v],
                                                            viBakti[v], stem_key=v))
        metafunc.parametrize("halanta_napum", halanta_napum_list)
    if 'ajanta_pum' in metafunc.fixturenames:
        ajanta_pum_list = []
        for v in ajanta["pum"]:
            if (v in encoding) and (encoding[v] == sanscript.SLP1):
                pass
            else:
                ajanta_pum_list.extend(generate_vibhakti(prAtipadika[v],
                                                         viBakti[v], stem_key=v))
        metafunc.parametrize("ajanta_pum", ajanta_pum_list)
    if 'ajanta_stri' in metafunc.fixturenames:
        ajanta_stri_list = []
        for v in ajanta["strI"]:
            if (v in encoding) and (encoding[v] == sanscript.SLP1):
                pass
            else:
                ajanta_stri_list.extend(generate_vibhakti(prAtipadika[v],
                                                          viBakti[v], stem_key=v))
        metafunc.parametrize("ajanta_stri", ajanta_stri_list)
    if 'ajanta_napum' in metafunc.fixturenames:
        ajanta_napum_list = []
        for v in ajanta["napum"]:
            if (v in encoding) and (encoding[v] == sanscript.SLP1):
                pass
            else:
                ajanta_napum_list.extend(generate_vibhakti(prAtipadika[v],
                                                           viBakti[v], stem_key=v))
        metafunc.parametrize("ajanta_napum", ajanta_napum_list)
    if 'vibhakti' in metafunc.fixturenames:
        vibhakti_list = []
        for v in viBakti:
            if (v in encoding) and (encoding[v] == sanscript.SLP1):
                pass
            else:
                vibhakti_list.extend(generate_vibhakti(prAtipadika[v],
                                                       viBakti[v], stem_key=v))
        metafunc.parametrize("vibhakti", vibhakti_list)
    if 'vibhakti_s' in metafunc.fixturenames:
        vibhakti_s_list = []
        for v in viBakti:
            if (v in encoding) and (encoding[v] == sanscript.SLP1):
                vibhakti_s_list.extend(generate_vibhakti(prAtipadika[v],
                                                         viBakti[v], sanscript.SLP1,
                                                         stem_key=v))
        metafunc.parametrize("vibhakti_s", vibhakti_s_list)
    if 'samAsa_pum' in metafunc.fixturenames:
        samAsa_pum_list = []
        for v in samAsa["pum"]:
            samAsa_pum_list.extend(generate_vibhakti(prAtipadika[v], viBakti[v], stem_key=v))
        metafunc.parametrize("samAsa_pum", samAsa_pum_list)
