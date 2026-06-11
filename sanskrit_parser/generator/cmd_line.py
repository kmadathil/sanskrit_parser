# -*- coding: utf-8 -*-
"""
@author: Karthik Madathil (github: @kmadathil)

"""
from argparse import ArgumentParser, Action

import logging
# First we disable the root logger handlers
rootlogger = logging.getLogger()
for h in rootlogger.handlers:
    rootlogger.removeHandler(h)
rootlogger.addHandler(logging.NullHandler())


import sys
import codecs
from copy import deepcopy

from indic_transliteration import sanscript
from sanskrit_parser.generator.paninian_object import PaninianObject
from sanskrit_parser.generator.prakriya import PrakriyaVakya
from sanskrit_parser.generator.prakriya_factory import PrakriyaFactory
from sanskrit_parser.generator.pratyaya import *  # noqa: F403
from sanskrit_parser.generator.dhatu import *  # noqa: F403
from sanskrit_parser.generator.pratipadika import *  # noqa: F403
from sanskrit_parser.generator.avyaya import *  # noqa: F403, F401
from sanskrit_parser.generator.sutras_yaml import SutraFactory
from sanskrit_parser import enable_file_logger, enable_console_logger

logger = logging.getLogger(__name__)


def run_pp(s, prakriya, sutra_list, verbose=False, tag_display=False):
    pl = [Adya]
    # Assemble list of inputs
    for i in range(len(s)):
        def _gen_obj(s, i):
            if isinstance(s[i], tuple) or isinstance(s[i], list):
                lelem = [_gen_obj(s[i], ii) for (ii, ss) in enumerate(s[i])]
            else:
                lelem = s[i]
            return lelem
        lelem = _gen_obj(s, i)
        pl.append(lelem)
    p = PrakriyaFactory(prakriya, sutra_list, PrakriyaVakya(pl))
    p.execute()
    if verbose:
        p.describe(tag_display=tag_display)
    o = p.output()
    return o


# Kāraka sentence: assemble tagged participant nouns + verb/particle padas
# (built by the -k/-w options) into one input list and run the engine. The
# AntarangaPrakriya pre-pass assigns kāraka/vibhakti tags and inserts sups.
def run_karaka(words, prakriya, sutra_list, sandhi=False, verbose=False, tag_display=False):
    # A single Adya marks sentence start (added once). By default each word is
    # followed by its own avasAna (isolated per-word forms, no inter-word
    # sandhi); with sandhi=True only a trailing avasAna is added so adjacent
    # words sandhi together.
    pl = [Adya]  # noqa: F405
    for w in words:
        pl.append(w)
        if not sandhi:
            pl.append(avasAna)  # noqa: F405
    if sandhi:
        pl.append(avasAna)  # noqa: F405
    for w in words:
        logger.info(f"{w} {w.tags}")
    p = PrakriyaFactory(prakriya, sutra_list, PrakriyaVakya(pl))
    p.execute()
    if verbose:
        p.describe(tag_display=tag_display)
    o = p.output()
    outs = [''.join([str(x) for x in y]) for y in o]
    out_devs = [sanscript.transliterate(s, sanscript.SLP1, sanscript.DEVANAGARI) for s in outs]
    print("Output:")
    for s, d in zip(outs, out_devs):
        print(f"  {d}  ({s})")
    # Per-word kāraka summary from the pre-pass log.
    klog = getattr(p, "karaka_log", [])
    if klog:
        print("Kāraka pre-pass:")
        for e in klog:
            kv = [t for t in e["tags"]
                  if t.startswith("kAraka_")
                  or (t.startswith("viBakti_") and t[8:].isdigit())]
            fired = ", ".join(e["fired"]) if e["fired"] else "—"
            print(f"  @{e['index']}: {', '.join(kv) or 'no tags'}  (fired: {fired})")
    return o


# Insert all sup vibhaktis one after the other, with avasAnas
# Return results with avasAnas stripped as 8x3 list of lists
def generate_vibhakti(pratipadika, prakriya, sutra_list, verbose=False, tag_display=False):
    r = []
    if isinstance(pratipadika, list):
        pratipadikax = pratipadika [-1]
    else:
        pratipadikax = pratipadika
    for ix, s in enumerate(sups):  # noqa: F405
        # Sarvanāmas (pronouns) have no vocative (sambōdhana = row 8)
        if ix == 7 and pratipadikax.hasTag("sarvanAma"):
            continue
        if verbose:
            logger.info(f"Vibhakti {ix+1} {s}")
        else:
            logger.debug(f"Vibhakti {ix+1} {s}")
        r.append([])
        for jx, ss in enumerate(s):
            # For nitya eka/dvi/bahuvacana, generate only the appropriate
            if (((jx == 0) and pratipadikax.hasTag("nityEkavacana")) or
                ((jx == 1) and pratipadikax.hasTag("nityadvivacana")) or
                ((jx == 2) and pratipadikax.hasTag("nityabahuvacana")) or
                (not (pratipadikax.hasTag("nityEkavacana") or
                      pratipadikax.hasTag("nityadvivacana") or
                      pratipadikax.hasTag("nityabahuvacana")))):
                if prakriya=="AntarangaPrakriya":
                    t = [*pratipadika, ss, avasAna]  # noqa: F405
                else:
                    t = [(pratipadika, ss), avasAna]  # noqa: F405
                _r = run_pp(t, prakriya, sutra_list, verbose, tag_display=tag_display)
                r[-1].append(_r)
                p = [''.join([str(x) for x in y]) for y in _r]
                pp = ", ".join([x.strip('.') for x in p])
                if verbose:
                    logger.info(f"Vacana {jx+1} {ss} {pp}")
                else:
                    logger.debug(f"Vacana {jx+1} {ss} {pp}")
    return r



last_option = False


class CustomAction(Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        # if nargs is not None:
        #   raise ValueError("nargs not allowed")
        super(CustomAction, self).__init__(option_strings, dest, nargs, **kwargs)
        logger.debug(f"Initializing CustomAction {option_strings}, {dest}")

    def __call__(self, parser, namespace, values, option_string=None):
        logger.debug('%r %r %r' % (namespace, values, option_string))
        global last_option
        assert not last_option, f"Option {option_string} added after avasana"
        if getattr(namespace, self.dest) is None:
            _n = []
            # This tracks the hierarchical input list
            setattr(namespace, self.dest, _n)
            # Last item of this is always the current level of the input
            setattr(namespace, "pointer", [_n])
        if values is not None:
            if isinstance(values, str):
                values = [values]
            for v in values:
                assert v in globals(), f"{v} is not defined!"
                getattr(namespace, "pointer")[-1].append(globals()[v])
        else:
            if option_string == "-o":  # Open
                _l = []
                # Add a new level at the end of current list
                getattr(namespace, "pointer")[-1].append(_l)
                # Designate new list as current list
                getattr(namespace, "pointer").append(_l)
            elif option_string == "-c":  # Close
                # Current is updated to previous
                getattr(namespace, "pointer").pop()
            elif option_string == "-a":  # AvasAna
                # Add avasana
                lav = getattr(namespace, self.dest)
                setattr(namespace, self.dest, [lav, avasAna])  # noqa: F405
                last_option = True
            else:
                logger.error(f"Unrecognized Option {option_string}")


class CustomActionSamasa(Action):
    """Like CustomAction but wraps each looked-up pratipadika with in_compound().

    Used for -m / --samasta-pratipadika: marks the uttara-pada as being in
    compound (samāsa) context by deep-copying and setting the ?samAsa tag.
    """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(CustomActionSamasa, self).__init__(option_strings, dest, nargs, **kwargs)
        logger.debug(f"Initializing CustomActionSamasa {option_strings}, {dest}")

    def __call__(self, parser, namespace, values, option_string=None):
        logger.debug('%r %r %r' % (namespace, values, option_string))
        global last_option
        assert not last_option, f"Option {option_string} added after avasana"
        if getattr(namespace, self.dest) is None:
            _n = []
            setattr(namespace, self.dest, _n)
            setattr(namespace, "pointer", [_n])
        if isinstance(values, str):
            values = [values]
        for v in values:
            assert v in globals(), f"{v} is not defined!"
            getattr(namespace, "pointer")[-1].append(in_compound(globals()[v]))  # noqa: F405


class CustomActionSamasaTagged(Action):
    """Like CustomActionSamasa but additionally sets one extra tag (e.g. ?dvigu,
    ?bahuvrIhi) on each pratipadika.

    Equivalent to in_context(in_compound(x), <tag>) — used by the --dvigu and
    --bahuvrihi options so the user can mark a compound's uttara-pada with the
    relevant compound-type saṁjñā for testing SK479/480/481/482 etc. from the CLI.
    The ?samAsa tag is added automatically (via in_compound).
    """
    # extra_tag is set per-option via partial / subclass below.
    extra_tag = None

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(CustomActionSamasaTagged, self).__init__(option_strings, dest, nargs, **kwargs)
        logger.debug(f"Initializing CustomActionSamasaTagged ({self.extra_tag}) "
                     f"{option_strings}, {dest}")

    def __call__(self, parser, namespace, values, option_string=None):
        logger.debug('%r %r %r' % (namespace, values, option_string))
        global last_option
        assert not last_option, f"Option {option_string} added after avasana"
        assert self.extra_tag is not None, "extra_tag must be set on subclass"
        if getattr(namespace, self.dest) is None:
            _n = []
            setattr(namespace, self.dest, _n)
            setattr(namespace, "pointer", [_n])
        if isinstance(values, str):
            values = [values]
        for v in values:
            assert v in globals(), f"{v} is not defined!"
            wrapped = in_context(in_compound(globals()[v]), self.extra_tag)  # noqa: F405
            getattr(namespace, "pointer")[-1].append(wrapped)


class CustomActionDvigu(CustomActionSamasaTagged):
    """--dvigu / -D: wrap each pratipadika with ?samAsa + ?dvigu."""
    extra_tag = "dvigu"


class CustomActionBahuvrihi(CustomActionSamasaTagged):
    """--bahuvrihi / -B: wrap each pratipadika with ?samAsa + ?bahuvrIhi."""
    extra_tag = "bahuvrIhi"


class CustomActionPurvaPada(Action):
    """Like CustomAction but wraps each looked-up pratipadika with as_purva_pada().

    Used for -u / --purva-pada: marks a pratipadika as the pūrva-pada in a
    compound by deep-copying and setting the ?samAsaPurva tag.
    """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(CustomActionPurvaPada, self).__init__(option_strings, dest, nargs, **kwargs)
        logger.debug(f"Initializing CustomActionPurvaPada {option_strings}, {dest}")

    def __call__(self, parser, namespace, values, option_string=None):
        logger.debug('%r %r %r' % (namespace, values, option_string))
        global last_option
        assert not last_option, f"Option {option_string} added after avasana"
        if getattr(namespace, self.dest) is None:
            _n = []
            setattr(namespace, self.dest, _n)
            setattr(namespace, "pointer", [_n])
        if isinstance(values, str):
            values = [values]
        for v in values:
            assert v in globals(), f"{v} is not defined!"
            getattr(namespace, "pointer")[-1].append(as_purva_pada(globals()[v]))  # noqa: F405


class CustomActionKaraka(Action):
    """-k / --karaka <stem> [vacana] [sem ...]: a kāraka participant noun.

    Builds a deep copy of the predefined pratipadika <stem>, sets vacana_<N>
    (a digit token; default vacana_1) and each semantic primitive as a
    semantic_<prim> tag (used as-is if it already starts with "semantic_").
    Appends to dest="karaka_words" — shared with --word so the sentence word
    order is preserved across the two options. Does NOT touch last_option/pointer.
    """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(CustomActionKaraka, self).__init__(option_strings, dest, nargs, **kwargs)
        logger.debug(f"Initializing CustomActionKaraka {option_strings}, {dest}")

    def __call__(self, parser, namespace, values, option_string=None):
        logger.debug('%r %r %r' % (namespace, values, option_string))
        if getattr(namespace, self.dest) is None:
            setattr(namespace, self.dest, [])
        stem = values[0]
        assert stem in globals(), f"{stem} is not defined!"
        obj = deepcopy(globals()[stem])
        vacana = 1
        sems = []
        for tok in values[1:]:
            if tok.isdigit():
                vacana = int(tok)
            elif tok.startswith("semantic_"):
                sems.append(tok)
            else:
                sems.append("semantic_" + tok)
        obj.setTag(f"vacana_{vacana}")
        for s in sems:
            obj.setTag(s)
        getattr(namespace, self.dest).append(obj)


class CustomActionWord(Action):
    """-w / --word <name> ...: any predefined object by name (verb pada like
    Bajati/sevyate, or a particle like he), appended as a deep copy with no
    added tags. Shares dest="karaka_words" with --karaka to preserve order.
    """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(CustomActionWord, self).__init__(option_strings, dest, nargs, **kwargs)
        logger.debug(f"Initializing CustomActionWord {option_strings}, {dest}")

    def __call__(self, parser, namespace, values, option_string=None):
        logger.debug('%r %r %r' % (namespace, values, option_string))
        if getattr(namespace, self.dest) is None:
            setattr(namespace, self.dest, [])
        if isinstance(values, str):
            values = [values]
        for v in values:
            assert v in globals(), f"{v} is not defined!"
            getattr(namespace, self.dest).append(deepcopy(globals()[v]))


class CustomActionString(Action):
    def __init__(self, option_strings, dest, nargs=None, encoding=sanscript.SLP1, **kwargs):
        # if nargs is not None:
        #   raise ValueError("nargs not allowed")
        self.encoding = encoding
        super(CustomActionString, self).__init__(option_strings, dest, nargs, **kwargs)
        logger.debug(f"Initializing CustomAction {option_strings}, {dest}")

    def __call__(self, parser, namespace, values, option_string=None):
        global last_option
        assert not last_option, f"Option {option_string} added after avasana"
        encoding = self.encoding

        def _exec(value):
            # Shortcuts for two input tests not using predefined objects
            # If a string in the first place ends with * it's an anga
            # Else it's a pada
            # For everything else, use predefined objects
            if (value[-1] == "*"):
                value = value[:-1]
                value = PaninianObject(value, encoding)  # noqa: F405
                value.setTag("aNga")
            elif (value[-1] == "_"):
                value = value[:-1]
                value = PaninianObject(value, encoding)  # noqa: F405
                value.setTag("pada")
            else:
                value = PaninianObject(value, encoding)  # noqa: F405
            getattr(namespace, "pointer")[-1].append(value)

            logger.debug('%r %r %r' % (namespace, values, option_string))
        if getattr(namespace, self.dest) is None:
            _n = []
            # This tracks the hierarchical input list
            setattr(namespace, self.dest, _n)
            # Last item of this is always the current level of the input
            setattr(namespace, "pointer", [_n])
        if isinstance(values, list):
            for v in values:
                _exec(v)
        else:
            _exec(values)


def get_args(argv=None):
    """
      Argparse routine.
      Returns args variable
    """

    parser = ArgumentParser(description='Paninian Generator: Prakriti + Pratyaya')
    # String to encode
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('-p', '--pratyaya', nargs="+", dest="inputs", action=CustomAction)
    parser.add_argument('-d', '--dhatu', dest="inputs", action=CustomAction)
    parser.add_argument('-t', '--pratipadika', dest="inputs", action=CustomAction)
    parser.add_argument('-m', '--samasta-pratipadika', nargs="+", dest="inputs", action=CustomActionSamasa)
    parser.add_argument('-u', '--purva-pada', nargs="+", dest="inputs", action=CustomActionPurvaPada)
    parser.add_argument('-D', '--dvigu', nargs="+", dest="inputs", action=CustomActionDvigu,
                        help="Mark uttara-pada(s) as in_compound(...) + ?dvigu (samāsa added automatically)")
    parser.add_argument('-B', '--bahuvrihi', nargs="+", dest="inputs", action=CustomActionBahuvrihi,
                        help="Mark uttara-pada(s) as in_compound(...) + ?bahuvrIhi (samāsa added automatically)")
    parser.add_argument('-s', '--string', nargs="+", dest="inputs", encoding=sanscript.SLP1, action=CustomActionString)
    parser.add_argument('-k', '--karaka', nargs="+", dest="karaka_words", action=CustomActionKaraka,
                        help="Kāraka participant noun: <stem> [vacana] [semantic_primitive ...] "
                             "(e.g. -k hari 1 Ipsitatama)")
    parser.add_argument('-w', '--word', nargs="+", dest="karaka_words", action=CustomActionWord,
                        help="Predefined object (verb pada, particle) by name for a kāraka sentence "
                             "(e.g. -w Bajati)")
    parser.add_argument("--sandhi", action="store_true",
                        help="Kāraka sentence: apply inter-word sandhi (connected sentence) "
                             "instead of the default avasāna-separated per-word forms")
    parser.add_argument('-o', nargs="?", dest="inputs", action=CustomAction, help="Open bracket")  # Open Brace
    parser.add_argument('-c', nargs="?", dest="inputs", action=CustomAction, help="Close bracket")
    parser.add_argument('-a', nargs="?", dest="inputs", action=CustomAction, help="Avasana")
    parser.add_argument("--vibhakti", action="store_true", help="generate all vibhaktis")
    parser.add_argument("--gen-test", action="store_true", help="generate vibhakti test")
    parser.add_argument("--prakriya", default="AntarangaPrakriya", help="Prakriya type")
    parser.add_argument("--sutra-file", default="sutras_antaranga.yaml", help="Sutra File Name")
    parser.add_argument("--verbose", action="store_true", help="verbose")
    parser.add_argument("--tag-display", action="store_true", help="display tags and its on objects (requires --verbose)")

    return parser.parse_args(argv)


def cmd_line():
    # Windows doesn't work correctly without this
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    # Logging
    enable_console_logger()
    args = get_args()
    sutra_list = SutraFactory(args.sutra_file)
    if args.debug:
        enable_file_logger(level=logging.DEBUG)
    # Kāraka sentence path (-k / -w): assemble a tagged sentence and run it
    # through the engine, which does the kāraka pre-pass + sup insertion.
    if getattr(args, "karaka_words", None):
        run_karaka(args.karaka_words, args.prakriya, sutra_list,
                   sandhi=args.sandhi, verbose=args.verbose,
                   tag_display=args.tag_display)
        return
    logger.info(f"Inputs {args.inputs}")
    for i in args.inputs:
        def _i(x):
            if isinstance(x, list):
                for _x in x:
                    _i(_x)
            else:
                logger.info(f"{x} {x.tags}")
        _i(i)
    logger.info("End Inputs")
    if args.vibhakti:
        if args.prakriya=="AntarangaPrakriya":    # We can handle multiple inputs
            pp = args.inputs
        elif ((len(args.inputs) != 1) or (not isinstance(args.inputs[0], Pratipadika))):  # noqa: F405
            logger.info(f"Need a single pratipadika for vibhaktis, got {len(args.inputs)} inputs, first one of type {type(args.inputs[0])}")
            logger.info("Simplifying")
            r = run_pp(args.inputs, args.prakriya, sutra_list, args.verbose, tag_display=args.tag_display)
            logger.debug(f"Output: {[''.join([str(x) for x in y]) for y in r]}")
            assert len(r) == 1, "Got multiple outputs"
            pp = PaninianObject.join_objects(r)
            logger.info(f"Output {pp} {pp.tags}")
        else:
            pp = args.inputs[0]
        r = generate_vibhakti(pp,  args.prakriya, sutra_list, args.verbose, tag_display=args.tag_display)
        print("Output")
        if args.gen_test:
            rr = [[[y[0].transcoded(sanscript.DEVANAGARI).strip('।') for y in va] if len(va) > 1
                   else va[0][0].transcoded(sanscript.DEVANAGARI).strip('।') for va in vi] for vi in r]
            print(f"prAtipadika[\"{str(pp)}\"] = {str(pp)}")
            print(f"viBakti[\"{str(pp)}\"] = [")
            for vi in rr:
                print(f"{vi},")
            print("]")
        else:
            for ix, vi in enumerate(r):
                print(f"{', '.join(['/'.join([''.join([x.transcoded(sanscript.DEVANAGARI) for x in y]).strip('।') for y in va]) for va in vi])}")
    else:
        r = run_pp(args.inputs, args.prakriya, sutra_list, args.verbose, tag_display=args.tag_display)
        print(f"Output: {[''.join([str(x) for x in y]) for y in r]}")
