from sanskrit_parser.generator.paninian_object import PaninianObject
from sanskrit_parser.generator.prakriya import Prakriya, PrakriyaVakya
from sanskrit_parser.generator.pratyaya import *  # noqa: F403

from vibhaktis_list import ajanta, halanta, viBakti, prAtipadika, encoding

# @pytest.fixture(scope="module")
# def sutra_fixture():
#     return sutra_list


def pytest_addoption(parser):
    """Custom options for pytest command line
    """
    # Add an option to limit number of tests generated.
    ## TODO: Solve "ValueError: option names {'--test-count'} already added" below
    #parser.addoption("--test-count", action="store", default=0,
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
    _s = [x.replace(' ', "") for x in _s]
    j = [
        PaninianObject("".join([
            _o.transcoded(sanscript.SLP1) for _o in list(o)
        ]), encoding=sanscript.SLP1).transcoded(enc)
        for o in output
    ]
    if not (set(j) == set(_s)):
        print(set(j), set(_s))
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
                # Else it's a pada
                # For everything else, use predefined objects
                if (i == 0) and (s[i][-1] == "*"):
                    s0 = s[0][:-1]
                    l = PaninianObject(s0, encoding)  # noqa: E741
                    l.setTag("aNga")
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
    p = Prakriya(sutra_list, PrakriyaVakya(pl))
    p.execute()
    if verbose:
        p.describe()
    o = p.output(copy=True)
    assert _test(o, s, encoding)
    return None


def generate_vibhakti(pratipadika, vibhaktis, encoding=sanscript.DEVANAGARI):
    t = []
    for ix, pv in enumerate(vibhaktis):
        for jx, pvv in enumerate(pv):
            # For nitya eka/dvi/bahuvacana, generate only the appropriate
            if (((jx == 0) and pratipadika.hasTag("nityEkavacana")) or
                ((jx == 1) and pratipadika.hasTag("nityadvivacana")) or
                ((jx == 2) and pratipadika.hasTag("nityabahuvacana")) or
                (not (pratipadika.hasTag("nityEkavacana") or
                      pratipadika.hasTag("nityadvivacana") or
                      pratipadika.hasTag("nityabahuvacana")))):
                if isinstance(pvv, str):
                    _pvv = pvv+avasAna.transcoded(encoding)  # noqa: F405
                else:
                    _pvv = [x+avasAna.transcoded(encoding) for x in pvv]  # noqa: F405
                t.append([(pratipadika, sups[ix][jx]), avasAna, _pvv])  # noqa: F405
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
                                                          viBakti[v]))
        metafunc.parametrize("halanta_pum", halanta_pum_list)
    if 'halanta_stri' in metafunc.fixturenames:
        halanta_stri_list = []
        for v in halanta["strI"]:
            if (v in encoding) and (encoding[v] == sanscript.SLP1):
                pass
            else:
                halanta_stri_list.extend(generate_vibhakti(prAtipadika[v],
                                                           viBakti[v]))
        metafunc.parametrize("halanta_stri", halanta_stri_list)
    if 'halanta_napum' in metafunc.fixturenames:
        halanta_napum_list = []
        for v in halanta["napum"]:
            if (v in encoding) and (encoding[v] == sanscript.SLP1):
                pass
            else:
                halanta_napum_list.extend(generate_vibhakti(prAtipadika[v],
                                                            viBakti[v]))
        metafunc.parametrize("halanta_napum", halanta_napum_list)
    if 'ajanta_pum' in metafunc.fixturenames:
        ajanta_pum_list = []
        for v in ajanta["pum"]:
            if (v in encoding) and (encoding[v] == sanscript.SLP1):
                pass
            else:
                ajanta_pum_list.extend(generate_vibhakti(prAtipadika[v],
                                                         viBakti[v]))
        metafunc.parametrize("ajanta_pum", ajanta_pum_list)
    if 'ajanta_stri' in metafunc.fixturenames:
        ajanta_stri_list = []
        for v in ajanta["strI"]:
            if (v in encoding) and (encoding[v] == sanscript.SLP1):
                pass
            else:
                ajanta_stri_list.extend(generate_vibhakti(prAtipadika[v],
                                                          viBakti[v]))
        metafunc.parametrize("ajanta_stri", ajanta_stri_list)
    if 'ajanta_napum' in metafunc.fixturenames:
        ajanta_napum_list = []
        for v in ajanta["napum"]:
            if (v in encoding) and (encoding[v] == sanscript.SLP1):
                pass
            else:
                ajanta_napum_list.extend(generate_vibhakti(prAtipadika[v],
                                                           viBakti[v]))
        metafunc.parametrize("ajanta_napum", ajanta_napum_list)
    if 'vibhakti' in metafunc.fixturenames:
        vibhakti_list = []
        for v in viBakti:
            if (v in encoding) and (encoding[v] == sanscript.SLP1):
                pass
            else:
                vibhakti_list.extend(generate_vibhakti(prAtipadika[v],
                                                       viBakti[v]))
        metafunc.parametrize("vibhakti", vibhakti_list)
    if 'vibhakti_s' in metafunc.fixturenames:
        vibhakti_s_list = []
        for v in viBakti:
            if (v in encoding) and (encoding[v] == sanscript.SLP1):
                vibhakti_s_list.extend(generate_vibhakti(prAtipadika[v],
                                                         viBakti[v], sanscript.SLP1))
        metafunc.parametrize("vibhakti_s", vibhakti_s_list)
