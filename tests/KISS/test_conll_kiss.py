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
            
def parse_test(test, conll_writer=None, max_splits=1, max_parses=1):
    parser = Parser(input_encoding=sanscript.SLP1,
                    strict_io=False,
                    output_encoding=sanscript.SLP1,
                    replace_ending_visarga=None,
                    score=False,
                    split_above=5,
                    lexical_lookup="combined")
    written = False
    for si, split in enumerate(parser.split(" ".join(test),
                                                  limit=max_splits,
                                                  pre_segmented=True)):
        print(f'Lexical Split: {split}')
        for pi, parse in enumerate(split.parse(limit=max_parses)):
            print(f'Parse {pi} : (Cost = {parse.cost})')
            print(f'{parse}')
            if conll_writer is not None:
                for line in parse.to_conll():
                    conll_writer.writerow(line)
                conll_writer.writerow([])
                written = True
            if pi > 8:
                break
    if not written:
        for i,t in enumerate(test):
            conll_writer.writerow([i+1, t, "_",
                                   ["unknown"], "0", "unknown"])
        conll_writer.writerow([])
    return None



if __name__ == "__main__":
    def getArgs(argv=None):
        # Parser Setup
        parser = ArgumentParser(description='CONLL Reader')
        # String to encode
        parser.add_argument('files', nargs="+", type=str)
        parser.add_argument('-o', '--output', type=str)
        args = parser.parse_args(argv)
        return args

    def main(args):
        with open(args.output, "wt") as of:
            cwriter = csv.writer(of, delimiter='\t')
            for fname in args.files:
                print(fname)
                with open(fname, "rt") as f:
                    for test in islice(conll_tests(f),5):
                        print(f"Test: {test}")
                        print("\n")
                        parse_test(test, conll_writer=cwriter)

    main(getArgs())
