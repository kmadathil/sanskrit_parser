#! /usr/bin/env python
import multiprocessing
import os.path
import argparse
import csv
from argparse import ArgumentParser
from sanskrit_parser import Parser
from itertools import islice

    

def conll_tests(conll_file):
    # CONLL files are treated as tsv
    print(conll_file.name)
    treader = csv.reader(conll_file, delimiter='\t')
    intest = 0
    tl = []
    for row in treader:
        if len(row):
            tl.append(row[1])
        else:
            yield tl
            tl = []
            
def parse_test(test, max_splits=1, max_parses=1):
    parser = Parser(input_encoding="SLP1",
                    strict_io=False,
                    output_encoding="SLP1",
                    replace_ending_visarga=None,
                    score=False,
                    split_above=5,
                    lexical_lookup="combined")
    parse_result = parser.parse(" ".join(test), pre_segmented=True)
    if parse_result is not None:
        print('Splits:')
        for si, split in enumerate(parse_result.splits(max_splits=max_splits)):
            print(f'Lexical Split: {split}')
            for pi, parse in islice(enumerate(split.parses()), max_parses):
                print(f'Parse {pi} : (Cost = {parse.cost})')
                print(f'{parse}')
                if pi > 8:
                    break
    return None



if __name__ == "__main__":
    def getArgs(argv=None):
        # Parser Setup
        parser = ArgumentParser(description='CONLL Reader')
        # String to encode
        parser.add_argument('files', nargs="+", type=str)
        args = parser.parse_args(argv)
        return args

    def main(args):
        for fname in args.files:
            print(fname)
            with open(fname, "rt") as f:
                for test in islice(conll_tests(f),5):
                    print(f"Test: {test}")
                    print("\n")
                    parse_test(test)

    main(getArgs())
