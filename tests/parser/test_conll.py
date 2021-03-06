#! /usr/bin/env python
import csv
from argparse import ArgumentParser
from sanskrit_parser import Parser
from sanskrit_parser.api import ParseEdge
from itertools import islice, zip_longest


def conll_tests(conll_file):
    # CONLL files are treated as tsv
    treader = csv.reader(conll_file, delimiter='\t')
    tl = []
    for row in treader:
        if len(row):
            tl.append(row)
        else:
            yield tl
            tl = []


def parse_test_f(test, testpadas, max_splits=1, max_parses=100,
                 verbose=False):
    parser = Parser(input_encoding="SLP1",
                    strict_io=False,
                    output_encoding="SLP1",
                    replace_ending_visarga=None,
                    score=False,
                    split_above=5,
                    lexical_lookup="combined")
    parse_result = parser.parse(" ".join(testpadas), pre_segmented=True)
    parse = None
    if parse_result is not None:
        if verbose:
            print('Splits:')
        for si, split in enumerate(parse_result.splits(max_splits=max_splits)):
            if verbose:
                print(f'Lexical Split: {split}')
            for pi, parse in islice(enumerate(split.parses(min_cost_only=True)), max_parses):
                if verbose:
                    print(f'Parse {pi} : (Cost = {parse.cost})')
                if check_parse(parse, test, verbose=verbose):
                    if verbose:
                        print(f'{parse}')
                    return True, parse
    return False, parse


def check_parse(a, b, verbose=False):
    result = True
    for z in zip_longest(a, b):
        p = z[0]
        t = z[1]
        if isinstance(p, ParseEdge):
            r = (str(p.node.index+1) == t[0]) and \
                (p.node.parse_tag.root == t[3]) and \
                (str(p.predecessor.index+1) == t[5]) and \
                (p.label == t[6]) and \
                (set(p.node.parse_tag.tags) == set(eval(t[4])))
            if not r:
                if verbose:
                    print(f"{p.node.index+1} {t[0]} {p.node} {t[3]} {t[4]}  {p.predecessor.index+1} {t[5]} {p.label} {t[6]} {set(p.node.parse_tag.tags)} {set(eval(t[4]))}")  # noqa E501
                result = False
                break
        else:
            r = (str(p.index+1) == t[0]) and \
                (p.parse_tag.root == t[3]) and \
                (t[5] == "0") and \
                (t[6] == "root") and \
                (set(p.parse_tag.tags) == set(eval(t[4])))
            if not r:
                if verbose:
                    print(f"{p.index+1} {p.parse_tag.root} {t[3]} {t[0]} _ {t[5]} _ {t[6]}  {set(p.parse_tag.tags)} {set(eval(t[4]))}")
                result = False
                break
    return result


if __name__ == "__main__":
    def getArgs(argv=None):
        # Parser Setup
        parser = ArgumentParser(description='CONLL Reader')
        # String to encode
        parser.add_argument('files', nargs="+", type=str)
        parser.add_argument('-o', '--output', type=str, required=True)
        parser.add_argument('--max-tests', type=int, default=100000)
        parser.add_argument('-v', '--verbose', action="store_true")
        args = parser.parse_args(argv)
        return args

    def main(args):
        with open(args.output, "wt") as of:
            conll_writer = csv.writer(of, delimiter='\t')
            passed = 0
            failed = 0
            for fname in args.files:
                print(fname)
                with open(fname, "rt") as f:
                    for test in islice(conll_tests(f), args.max_tests):
                        testpadas = [t[1] for t in test]
                        print(f"Test: {testpadas}")
                        status, parse = parse_test_f(test, testpadas, verbose=args.verbose)
                        if status:
                            print(f"PASSED {testpadas}\n")
                            passed = passed + 1
                        else:
                            print(f"FAILED {testpadas}\n")
                            failed = failed + 1
                        if conll_writer is not None:
                            if parse is None:
                                for i, t in enumerate(testpadas):
                                    conll_writer.writerow([i+1, t, "_",
                                                           ["unknown"], "0", "unknown"])
                                conll_writer.writerow([])
                            else:
                                for line in parse.to_conll():
                                    conll_writer.writerow(line)
                                conll_writer.writerow([])
                    print(f"{failed} Failed and {passed} Passed")
    main(getArgs())
