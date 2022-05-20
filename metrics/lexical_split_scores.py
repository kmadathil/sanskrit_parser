'''
Computes scores for lexical splits. Currently computes BLEU
and chrF (character F1 score) using sacrebleu.

Uses reference data from https://github.com/cvikasreddy/skt
which itself is derived from the DCS.

### Prerequisites
sacrebleu can be installed using
```pip install sacrebleu```
or can be downloaded from https://github.com/awslabs/sockeye/tree/master/contrib/sacrebleu

'''

from __future__ import print_function, unicode_literals
import os
import time
import logging
import argparse
import operator
import itertools
import subprocess
import progressbar

from indic_transliteration import sanscript
from sanskrit_parser.base.sanskrit_base import SanskritObject, outputctx

## TODO: Fix missing import below.
from sanskrit_parser.lexical_analyzer.sanskrit_lexical_analyzer import SanskritLexicalAnalyzer


curr_dir = os.path.dirname(__file__)
data_dir = os.path.join(curr_dir, "data")
input_file = os.path.join(data_dir, "splits_input_test.txt")
ref_file = os.path.join(data_dir, "splits_output_test.txt")
ref_output_file = os.path.join(curr_dir, "refs.txt")

score_cmd = ["./sacrebleu.py", ref_output_file, "-m", "bleu", "chrf"]

logger = logging.getLogger(__name__)


class LexicalSplitMetrics(object):
    ''' Compute metrics for lexical splits '''

    def __init__(self, lexical_lookup, score_and_sort=None):
        self.name = lexical_lookup
        self.analyzer = SanskritLexicalAnalyzer(lexical_lookup=lexical_lookup)
        self.score_and_sort = score_and_sort
        self.num_paths = score_and_sort or 1
        self.fp = open(self.name + ".txt", "a")
        if score_and_sort:
            from sanskrit_parser.util import lexical_scorer
            self.scorer = lexical_scorer.Scorer()
            self.score_fp = open(self.name + "_" + str(score_and_sort) + ".txt", "a")

    def update(self, sentence):
        graph = self.analyzer.getSandhiSplits(sentence)
        split = ''
        splits = None
        if graph:
            splits = graph.findAllPaths(self.num_paths)
            if splits:
                split = ' '.join(map(str, splits[0]))
            else:
                logger.debug("%s: No splits", self.name)
        else:
            logger.debug("%s: No graph", self.name)
        self.fp.write(split + "\n")
        logger.debug("%s: %s", self.name, split)
        # Repeat with sorted scores
        if self.score_and_sort:
            if splits:
                splits_scores = [(s, self.scorer.score(s)) for s in splits]
                sorted_splits_scores = sorted(splits_scores,
                                              key=operator.itemgetter(1),
                                              reverse=True)
                logger.debug("Sorted splits with scores:\n %s", sorted_splits_scores)
                split = ' '.join(map(str, sorted_splits_scores[0][0]))
            else:
                logger.debug("%s_%s: No splits", self.name, self.score_and_sort)
        self.score_fp.write(split + "\n")
        logger.debug("%s_%s: %s", self.name, self.score_and_sort, split)

    @staticmethod
    def print_metrics_file(filename):
        with open(filename) as fp:
            output = subprocess.check_output(score_cmd, stdin=fp, universal_newlines=True)
            lines = output.splitlines()
            bleu_score = lines[0].split("=", 1)[1].split("(")[0].strip()
            chrf = lines[1].split("=", 1)[1].strip()
            print("{:20s} | {:30s} | {:5s}".format(os.path.splitext(fp.name)[0],
                                                   bleu_score, chrf))
        return (bleu_score, chrf)

    def print_metrics(self):
        # Flush and close file
        self.fp.close()
        LexicalSplitMetrics.print_metrics_file(self.fp.name)
        if self.score_and_sort:
            self.score_fp.close()
            LexicalSplitMetrics.print_metrics_file(self.score_fp.name)


def main(count=None, start=0):
    # Collect inputs
    with open(input_file) as fp:
        inputs = fp.readlines()
    num_inputs = len(inputs)
    stop = start + count if count else None
    inputs = itertools.islice(inputs, start, stop)
    max_value = count or num_inputs - start

    # Write the reference outputs
    with open(ref_file) as fp, open(ref_output_file, "w") as out:
        refs = fp.readlines()
        refs = itertools.islice(refs, stop)
        out.write("".join(refs))

    # Create the objects for scoring
    inria = LexicalSplitMetrics("inria", 10)
    combined = LexicalSplitMetrics("combined", 10)

    bar = progressbar.ProgressBar(max_value=max_value)
    with outputctx(strict_io=False):
        for line in bar(inputs):
            s = SanskritObject(line.strip(), encoding=sanscript.SLP1, replace_ending_visarga=None)
            logger.debug("Input in SLP1 = %s", s.canonical())
            # Compute splits
            inria.update(s)
            combined.update(s)
        print("{:20s} | {:30s} | {:5s}".format("Name", "BLEU", "CHRF"))
        print("-"*70)
        inria.print_metrics()
        combined.print_metrics()


if __name__ == "__main__":
    start = time.time()

    parser = argparse.ArgumentParser("Compute lexical split score metrics")
    parser.add_argument('--count', type=int, default=None, help="Limit to no. of sentences from reference")
    parser.add_argument('--start', type=int, default=None, help="Offset to start from")
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(filename="lexical_split_scores.log", filemode="w",
                            level=logging.DEBUG)
    else:
        logging.basicConfig(filename="lexical_split_scores.log", filemode="w",
                            level=logging.INFO)

    main(count=args.count, start=args.start)
    # LexicalSplitMetrics.print_metrics_file('inria.txt')
    # LexicalSplitMetrics.print_metrics_file('inria_10.txt')
    # LexicalSplitMetrics.print_metrics_file('combined.txt')
    # LexicalSplitMetrics.print_metrics_file('combined_10.txt')

    logging.shutdown()
    end = time.time()
    print("Took %0.2fs" % (end - start))
