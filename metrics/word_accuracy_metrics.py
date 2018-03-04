# -*- coding: utf-8 -*-
"""
Test accuracy of different word-level lookup schemes.
Uses annotated data from the Digital Corpus of Sanskrit
database to evaluate how many words are recognized by
each of the lexical lookup schemes. Also checks if the
annotated root of the word in the DCS matches the stems
returned by the lexical lookup schemes.

Saves a log of which words are not correctly recognized for
further analysis.

Current output should look similar to:
```
--------------------------------------------------
Metrics for inria
--------------------------------------------------
Recognized 1438669 / 1932518 words, accuracy = 74.45%
Correct root for 1181208 / 1438669 recognized words, accuracy = 82.10%
==================================================
--------------------------------------------------
Metrics for sanskrit_data
--------------------------------------------------
Recognized 1670698 / 1932518 words, accuracy = 86.45%
Correct root for 1375194 / 1670698 recognized words, accuracy = 82.31%
==================================================
--------------------------------------------------
Metrics for combined
--------------------------------------------------
Recognized 1692948 / 1932518 words, accuracy = 87.60%
Correct root for 1429996 / 1692948 recognized words, accuracy = 84.47%
==================================================
```

### Dependencies

Depends on dcs_wrapper python package for the data and openpyxl
for logging some results. All dependencies can be installed using
```pip install dcs_wrapper openpyxl progressbar2```

### TODO:
- Compute precision metrics as well

@author: alvarna
"""

from __future__ import print_function, division
import time
import logging
import itertools
import argparse
import progressbar
from openpyxl import Workbook
from dcs_wrapper import DCS
from dcs_wrapper import DCSTagMapper
from sanskrit_parser.util.lexical_lookup_factory import LexicalLookupFactory
from sanskrit_parser.base.sanskrit_base import SanskritObject, IAST


logger = logging.getLogger(__name__)


class WordLevelMetrics(object):
    ''' Compute word level metrics for a lexical lookup'''

    def __init__(self, lookup):
        self.name = lookup
        self.lookup = LexicalLookupFactory.create(lookup)
        self.recognized = 0
        self.correct_root = 0
        self.count = 0

    def update(self, word, ref_root, ref_tags):
        '''Update the metrics using the given word and tag.
            The input word is expected to be in SLP1'''
        valid = self.lookup.valid(word)
        if valid:
            self.recognized += 1
            tag_list = self.lookup.get_tags(word)
            correct_root = False
            for (stem, tag_set) in tag_list:
                if(stem.split("#")[0]) == ref_root:
                    correct_root = True
                    break
            if correct_root:
                self.correct_root += 1
            else:
                logger.info("%s: Incorrect root for %s (ref = %s). Got %s",
                            self.name, word, ref_root, tag_list)
        self.count += 1
        return valid

    def print_metrics(self):
        print("-"*50)
        print("Metrics for", self.name)
        print("-"*50)
        print("Recognized %d / %d words, accuracy = %.2f%%" %
              (self.recognized, self.count,
               percentage(self.recognized, self.count))
              )
        print("Correct root for %d / %d recognized words, accuracy = %.2f%%" %
              (self.correct_root, self.recognized,
               percentage(self.correct_root, self.recognized))
              )
        print("="*50)


def percentage(a, b):
    return (a * 100.0 / b)


def main(count=None):
    inria_metrics = WordLevelMetrics("inria")
    sdata_metrics = WordLevelMetrics("sanskrit_data")
    comb_metrics = WordLevelMetrics("combined")

    tag_mapper = DCSTagMapper().map_tag

    wb = Workbook()
    ws = wb.active
    ws.append(["Word", "Root", "DCS Tag", "Inria", "Sanskrit Data",
               "Both missed", "Inria only", "Sanskrit only"])

    bar = progressbar.ProgressBar(max_value=count)
    with DCS() as dcs:
        sentences = itertools.islice(dcs.iter_sentences(), count)
        for sent in bar(sentences):
            text_obj = SanskritObject(sent.text, encoding=IAST,
                                      strict_io=False)
            words = text_obj.canonical().strip().split(" ")
            if len(words) != len(sent.dcsAnalysisDecomposition):
                continue
            for w, analysis in zip(words, sent.dcsAnalysisDecomposition):
                if len(analysis) != 1:
                    continue
                word_analysis = analysis[0]
                if word_analysis.dcsGrammarHint == []:
                    continue
                word_slp = SanskritObject(w, encoding=IAST,
                                          strict_io=False).canonical()
                tags = tag_mapper(word_analysis.dcsGrammarHint)
                root = SanskritObject(word_analysis.root,
                                      encoding=IAST,
                                      strict_io=False).canonical()
                i_valid = inria_metrics.update(word_slp, root, tags)
                s_valid = sdata_metrics.update(word_slp, root, tags)
                comb_metrics.update(word_slp, root, tags)
                if not i_valid or not s_valid:
                    ws.append([word_slp, word_analysis.root,
                               word_analysis.dcsGrammarHint,
                               i_valid, s_valid,
                               not i_valid and not s_valid,
                               i_valid and not s_valid,
                               not i_valid and s_valid
                               ])

    wb.save("lookup_results.xlsx")
    inria_metrics.print_metrics()
    sdata_metrics.print_metrics()
    comb_metrics.print_metrics()


if __name__ == "__main__":
    logging.basicConfig(filename="accuracy_metrics.log", filemode="w",
                        level=logging.INFO)
    start = time.time()

    parser = argparse.ArgumentParser("Collect word level accuracy metrics")
    parser.add_argument('--count', type=int, default=None, help="Limit to no. of sentences from DCS")

    args = parser.parse_args()

    main(args.count)

    logging.shutdown()
    end = time.time()
    print("Took %0.2fs" % (end - start))
