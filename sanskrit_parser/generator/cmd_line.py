# -*- coding: utf-8 -*-
"""
@author: Karthik Madathil (github: @kmadathil)

"""
from argparse import ArgumentParser, Action
import logging

from indic_transliteration import sanscript
from sanskrit_parser.generator.paninian_object import PaninianObject
from sanskrit_parser.generator.prakriya import Prakriya, PrakriyaVakya
from sanskrit_parser.generator.pratyaya import *  # noqa: F403
from sanskrit_parser.generator.dhatu import *  # noqa: F403
from sanskrit_parser.generator.pratipadika import *  # noqa: F403
from sanskrit_parser.generator.sutras_yaml import sutra_list
from sanskrit_parser import enable_file_logger, enable_console_logger

logger = logging.getLogger(__name__)


def run_pp(s, verbose=False):
    pl = []
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
    p = Prakriya(sutra_list, PrakriyaVakya(pl))
    p.execute()
    if verbose:
        p.describe()
    o = p.output()
    return o


# Insert all sup vibhaktis one after the other, with avasAnas
# Return results with avasAnas stripped as 8x3 list of lists
def generate_vibhakti(pratipadika, verbose=False):
    r = []
    for ix, s in enumerate(sups):  # noqa: F405
        if verbose:
            logger.info(f"Vibhakti {ix+1} {s}")
        else:
            logger.debug(f"Vibhakti {ix+1} {s}")
        r.append([])
        for jx, ss in enumerate(s):
            # For nitya eka/dvi/bahuvacana, generate only the appropriate
            if (((jx == 0) and pratipadika.hasTag("nityEkavacana")) or
                ((jx == 1) and pratipadika.hasTag("nityadvivacana")) or
                ((jx == 2) and pratipadika.hasTag("nityabahuvacana")) or
                (not (pratipadika.hasTag("nityEkavacana") or
                      pratipadika.hasTag("nityadvivacana") or
                      pratipadika.hasTag("nityabahuvacana")))):
                t = [(pratipadika, ss), avasAna]  # noqa: F405
                _r = run_pp(t, verbose)
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

            logger.info('%r %r %r' % (namespace, values, option_string))
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
    parser.add_argument('-s', '--string', nargs="+", dest="inputs", encoding=sanscript.SLP1, action=CustomActionString)
    parser.add_argument('-o', nargs="?", dest="inputs", action=CustomAction, help="Open bracket")  # Open Brace
    parser.add_argument('-c', nargs="?", dest="inputs", action=CustomAction, help="Close bracket")
    parser.add_argument('-a', nargs="?", dest="inputs", action=CustomAction, help="Avasana")
    parser.add_argument("--vibhakti", action="store_true", help="generate all vibhaktis")
    parser.add_argument("--gen-test", action="store_true", help="generate vibhakti test")
    parser.add_argument("--verbose", action="store_true", help="verbose")

    return parser.parse_args(argv)


def cmd_line():
    # Logging
    enable_console_logger()
    args = get_args()
    if args.debug:
        enable_file_logger(level=logging.DEBUG)
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
        if ((len(args.inputs) != 1) or (not isinstance(args.inputs[0], Pratipadika))):  # noqa: F405
            logger.info(f"Need a single pratipadika for vibhaktis, got {len(args.inputs)} inputs, first one of type {type(args.inputs[0])}")
            logger.info("Simplifying")
            r = run_pp(args.inputs, args.verbose)
            logger.debug(f"Output: {[''.join([str(x) for x in y]) for y in r]}")
            assert len(r) == 1, "Got multiple outputs"
            pp = PaninianObject.join_objects(r)
            logger.info(f"Output {pp} {pp.tags}")
        else:
            pp = args.inputs[0]
        r = generate_vibhakti(pp, args.verbose)
        print("Output")
        if args.gen_test:
            rr = [[[y[0].transcoded(sanscript.DEVANAGARI) for y in va] if len(va) > 1 else va[0][0].transcoded(sanscript.DEVANAGARI) for va in vi] for vi in r]
            print(f"prAtipadika[\"{str(pp)}\"] = {str(pp)}")
            print(f"viBakti[\"{str(pp)}\"] = [")
            for vi in rr:
                print(f"{vi},")
            print("]")
        else:
            for ix, vi in enumerate(r):
                print(f"{', '.join(['/'.join([''.join([x.transcoded(sanscript.DEVANAGARI) for x in y]).strip('।') for y in va]) for va in vi])}")
    else:
        r = run_pp(args.inputs, args.verbose)
        print(f"Output: {[''.join([str(x) for x in y]) for y in r]}")
