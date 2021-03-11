# -*- coding: utf-8 -*-
"""
@author: Karthik Madathil (github: @kmadathil)

"""
from os.path import dirname, basename, splitext, join
from argparse import ArgumentParser
import logging
from sanskrit_parser import Parser
from sanskrit_parser.base.sanskrit_base import SCHEMES, SanskritNormalizedString
from sanskrit_parser.base.sanskrit_base import outputctx
from sanskrit_parser.parser.sandhi_analyzer import LexicalSandhiAnalyzer
from sanskrit_parser import enable_file_logger, enable_console_logger
import csv

logger = logging.getLogger(__name__)


def getVakyaArgs(argv=None):
    """
      Argparse routine.
      Returns args variable
    """
    # Parser Setup
    parser = ArgumentParser(description='Vakya Analyzer')
    # String to encode
    parser.add_argument('data', nargs="?", type=str, default="astyuttarasyAMdishidevatAtmA")
    # Input Encoding (autodetect by default)
    parser.add_argument('--input-encoding', type=str, default=None)
    # Need a lakara
    parser.add_argument('--need-lakara', action='store_true')
    parser.add_argument('--max-paths', type=int, default=1)
    parser.add_argument('--split-above', type=int, default=5)
    parser.add_argument('--lexical-lookup', type=str, default="combined")
    parser.add_argument('--pre-segmented', action='store_true',
                        help="Expect pre-segmented space separated string (Usually for test only)")
    parser.add_argument('--strict-io', action='store_true',
                        help="Do not modify the input/output string to match conventions", default=False)
    parser.add_argument('--score', dest="score", action='store_true',
                        help="Use the lexical scorer to score the splits and reorder them")
    parser.add_argument('--slow-merge', dest='fast_merge', action='store_false', help="Development Only: use if you see issues in divide and conquer")
    parser.add_argument('--dot-file', type=str, default=None, help='Dotfile')
    parser.add_argument('--conll', action="store_true", help="display CONLL")
    parser.add_argument('--conll-file', type=str, default=None, help='CONLL output file')
    parser.add_argument('--conll-append', action="store_true", help="append to CONLL file rather than recreate")
    parser.add_argument('--min-cost', action="store_true", help="Only return min-cost parses")
    return parser.parse_args(argv)


def vakya(argv=None):
    args = getVakyaArgs(argv)
    if args.strict_io:
        print("Interpreting input strictly")
    else:
        print("Interpreting input loosely (strict_io set to false)")
    logger.info(f"Input String: {args.data}")
    parser = Parser(input_encoding=args.input_encoding,
                    strict_io=args.strict_io,
                    output_encoding="SLP1",
                    replace_ending_visarga=None,
                    score=args.score,
                    split_above=args.split_above,
                    lexical_lookup=args.lexical_lookup)
    logger.debug('Splits:')
    for si, split in enumerate(parser.split(args.data,
                                            limit=args.max_paths,
                                            pre_segmented=args.pre_segmented)):
        logger.info(f'Sandhi Split: {split}')
        logger.info(f'Min cost only {args.min_cost}')
        for pi, parse in enumerate(split.parse(limit=999,
                                               min_cost_only=args.min_cost)):
            logger.debug(f'Parse {pi}')
            logger.debug(f'{parse}')
            print(f'Parse {pi} : (Cost = {parse.cost})')
            if args.conll:
                for line in parse.to_conll():
                    print(line)
            else:
                print(f'{parse}')
            if args.conll_file is not None:
                path = args.conll_file
                d = dirname(path)
                be = basename(path)
                b, e = splitext(be)
                conllbase = join(d, b + f"_split{si}_parse{pi}" + e)
                if args.conll_append:
                    tfile = open(conllbase, "a")
                else:
                    tfile = open(conllbase, "w")
                twriter = csv.writer(tfile, delimiter='\t')
                for line in parse.to_conll():
                    twriter.writerow(line)
                twriter.writerow([])
                tfile.close()
        # Write dot files
        if args.dot_file is not None:
            path = args.dot_file
            d = dirname(path)
            be = basename(path)
            b, e = splitext(be)
            splitbase = join(d, b + f"_split{si}" + e)
            split.write_dot(splitbase)

    return None


def getSandhiArgs(argv=None):
    """
      Argparse routine.
      Returns args variable
    """
    # Parser Setup
    parser = ArgumentParser(description='Sandhi Analyzer')
    # String to encode
    parser.add_argument('data', nargs="?", type=str, default="astyuttarasyAMdishidevatAtmA")
    # Input Encoding (autodetect by default)
    parser.add_argument('--input-encoding', type=str, default=None)
    parser.add_argument('--max-paths', type=int, default=10)
    parser.add_argument('--lexical-lookup', type=str, default="combined")
    parser.add_argument('--pre-segmented', action='store_true',
                        help="Expect pre-segmented space separated string (Usually for test only)")
    parser.add_argument('--strict-io', action='store_true',
                        help="Do not modify the input/output string to match conventions", default=False)
    parser.add_argument('--no-score', dest="score", action='store_false',
                        help="Use the lexical scorer to score the splits and reorder them")
    return parser.parse_args(argv)


def sandhi(argv=None):
    args = getSandhiArgs(argv)
    if args.strict_io:
        print("Interpreting input strictly")
    else:
        print("Interpreting input loosely (strict_io set to false)")
    logger.info(f"Input String: {args.data}")
    parser = Parser(input_encoding=args.input_encoding,
                    strict_io=args.strict_io,
                    output_encoding="SLP1",
                    replace_ending_visarga=None,
                    score=args.score,
                    lexical_lookup=args.lexical_lookup)
    logger.debug('Splits:')
    for si, split in enumerate(parser.split(args.data,
                                            limit=args.max_paths,
                                            pre_segmented=args.pre_segmented)):
        logger.info(f'Split: {split}')
    return None


def getTagsArgs(argv=None):
    """
      Argparse routine.
      Returns args variable
    """
    # Parser Setup
    parser = ArgumentParser(description='Morphological tags')
    # String to encode
    parser.add_argument('data', nargs="?", type=str, default="adhi")
    # Input Encoding (autodetect by default)
    parser.add_argument('--input-encoding', type=str, default=None)
    # Filter by base name
    parser.add_argument('--base', type=str, default=None)
    # Filter by tag set
    parser.add_argument('--tag-set', type=str, default=None, nargs="+")
    parser.add_argument('--tags', dest='split', action='store_false')
    parser.add_argument('--lexical-lookup', type=str, default="combined")
    parser.add_argument('--strict-io', action='store_true',
                        help="Do not modify the input/output string to match conventions", default=False)
    parser.add_argument('--no-map-tags', dest='map_tags',
                        action='store_false', help="show raw (unmapped to our standard set) tags")
    return parser.parse_args(argv)


def tags(argv=None):
    args = getTagsArgs(argv)
    if args.strict_io:
        print("Interpreting input strictly")
    else:
        print("Interpreting input loosely (strict_io set to false)")
    logger.info(f"Input String: {args.data}")
    if args.input_encoding is None:
        ie = None
    else:
        ie = SCHEMES[args.input_encoding]
    s = LexicalSandhiAnalyzer(args.lexical_lookup)
    with outputctx(args.strict_io):
        i = SanskritNormalizedString(args.data, encoding=ie,
                                     strict_io=args.strict_io,
                                     replace_ending_visarga='s')
        print("Input String in SLP1:", i.canonical())
        ts = s.getMorphologicalTags(i, tmap=args.map_tags)
        print("Morphological tags:")
        if ts is not None:
            for t in ts:
                print(t)
        # Possible rakaranta
        # Try by replacing end visarga with 'r' instead
        elif not args.strict_io:
            i = SanskritNormalizedString(args.data, encoding=ie,
                                         strict_io=args.strict_io,
                                         replace_ending_visarga='r')
            ts = s.getMorphologicalTags(i)
            if ts is not None:
                print("Input String in SLP1:", i.canonical())
                for t in ts:
                    print(t)
        if args.tag_set or args.base:
            if args.tag_set is not None:
                g = set(args.tag_set)
            else:
                g = None
            if args.base is not None:
                b = SanskritNormalizedString(args.base)
            else:
                b = None
            print(s.hasTag(i, b, g))


def cmd_line():
    """ Command Line Wrapper Function
    """
    parser = ArgumentParser(description='Sanskrit Parser',
                            usage='%(prog)s [sandhi|vakya|tag]  [options] \n\n Use %(prog)s [sandhi|vakya|tag] --help for further options',
                            add_help=False)

    parser.add_argument('command', help='Subcommand to run',
                        choices=["sandhi", "vakya", "tags"])
    parser.add_argument('--debug', action='store_true')

    # parse_args defaults to [1:] for args, but you need to
    # exclude the rest of the args too, or validation will fail
    args, rest = parser.parse_known_args()

    # Logging
    enable_console_logger(level=logging.INFO)
    if args.debug:
        enable_file_logger(level=logging.DEBUG)
    # else:
    #    enable_file_logger(level=logging.INFO)

    if not hasattr(args, 'command'):
        print('Unrecognized command')
        parser.print_help()
        exit(1)
    # use dispatch pattern to invoke method with same name
    eval(getattr(args, 'command')+"(rest)")
