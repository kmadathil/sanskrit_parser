# -*- coding: utf-8 -*-
"""
@author: Karthik Madathil (github: @kmadathil)


Command line usage
==================

The sanskrit_parser script can be used to view parses as below.

If the --dot option is provided, a graph is output in .dot fomat with
all the possible morphologies as nodes, and possible relations as
edges. The valid parses extracted from this graph are also written out
as _parse.dot files


::

    $ sanskrit_parser vakya astyuttarasyAMdiSi --input SLP1 --dot vakya.dot
    ...
    Lexical Split: [asti, uttarasyAm, diSi]
    ...
    Parse 0
    asti=>['as#1', {prATamikaH, praTamapuruzaH, kartari, ekavacanam, law}]
    diSi=>['diS#2', {ekavacanam, strIliNgam, saptamIviBaktiH}]
    uttarasyAm=>['uttara#1', {ekavacanam, strIliNgam, saptamIviBaktiH}]
    ...

    $ dot -Tpng vakya.dot -o vakya.png
    $ eog vakya.png
    $ dot -Tpng vakya_parse0.dot -o vakya.png
    $ eog vakya_parse0.png

"""
from os.path import dirname, basename, splitext, join
from argparse import ArgumentParser
import logging
from sanskrit_parser import Parser

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
    parser.add_argument('--strict-io', action='store_true',
                        help="Do not modify the input/output string to match conventions", default=False)
    parser.add_argument('--score', dest="score", action='store_true',
                        help="Use the lexical scorer to score the splits and reorder them")
    parser.add_argument('--slow-merge', dest='fast_merge', action='store_false', help="Development Only: use if you see issues in divide and conquer")
    parser.add_argument('--dot-file', type=str, default=None, help='Dotfile')
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
    parse_result = parser.parse(args.data)
    print('Splits:')
    logger.debug('Splits:')
    for si, split in enumerate(parse_result.splits(max_splits=args.max_paths)):
        logger.info(f'Lexical Split: {split}')
        for pi, parse in enumerate(split.parses()):
            logger.debug(f'Parse {pi}')
            logger.debug(f'{parse}')
            print(f'Parse {pi}')
            print(f'{parse}')
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
    parser.add_argument('--strict-io', action='store_true',
                        help="Do not modify the input/output string to match conventions", default=False)
    parser.add_argument('--no-score', dest="score", action='store_false',
                        help="Use the lexical scorer to score the splits and reorder them")
    parser.add_argument('--dot-file', type=str, default=None, help='Dotfile')
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
    parse_result = parser.parse(args.data)
    print('Splits:')
    logger.debug('Splits:')
    for si, split in enumerate(parse_result.splits(max_splits=args.max_paths)):
        logger.info(f'Split: {split}')
    # Write dot files
    if args.dot_file is not None:
        parse_result.write_dot(args.dot_file)

    return None
