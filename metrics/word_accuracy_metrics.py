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
import os
import time
import logging
import itertools
import argparse
import progressbar
from openpyxl import Workbook
from dcs_wrapper import DCS
from dcs_wrapper import DCSTagMapper

from indic_transliteration import sanscript
from sanskrit_parser.util.lexical_lookup_factory import LexicalLookupFactory
from sanskrit_parser.base.sanskrit_base import SanskritObject
from joblib import Parallel, delayed


logger = logging.getLogger(__name__)


class WordLevelMetrics(object):
    ''' Compute word level metrics for a lexical lookup'''

    def __init__(self, lookup):
        self.name = lookup
        self.lookup = LexicalLookupFactory.create(lookup)
        self.count = 0
        self.recognized = 0
        self.correct_root = 0

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

    def metrics(self):
        return self.count, self.recognized, self.correct_root


def print_stats(lookup_scheme, stats):
    print("-"*50)
    print("Metrics for", lookup_scheme)
    print("-"*50)
    print("Recognized %d / %d words, accuracy = %.2f%%" %
          (stats['recognized'], stats['count'],
           percentage(stats['recognized'], stats['count']))
          )
    print("Correct root for %d / %d recognized words, accuracy = %.2f%%" %
          (stats['correct_root'], stats['recognized'],
           percentage(stats['correct_root'], stats['recognized']))
          )
    print("="*50)


def percentage(a, b):
    return (a * 100.0 / b)


def process(sentences, tag_mapper, ws):
    inria_metrics = WordLevelMetrics("inria")
    sdata_metrics = WordLevelMetrics("sanskrit_data")
    comb_metrics = WordLevelMetrics("combined")

    stats = {'inria': (0, 0, 0), 'sdata': (0, 0, 0), 'combo': (0, 0, 0)}
    missing = []
    for sent in sentences:
        if sent is None:
            continue
        text_obj = SanskritObject(sent.text, encoding=sanscript.IAST,
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
            word_slp = SanskritObject(w, encoding=sanscript.IAST,
                                      strict_io=False).canonical()
            tags = tag_mapper(word_analysis.dcsGrammarHint)
            root = SanskritObject(word_analysis.root,
                                  encoding=sanscript.IAST,
                                  strict_io=False).canonical()
            i_valid = inria_metrics.update(word_slp, root, tags)
            s_valid = sdata_metrics.update(word_slp, root, tags)
            comb_metrics.update(word_slp, root, tags)
            if not i_valid or not s_valid:
                missing.append([word_slp, word_analysis.root,
                                word_analysis.dcsGrammarHint,
                                i_valid, s_valid,
                                not i_valid and not s_valid,
                                i_valid and not s_valid,
                                not i_valid and s_valid
                                ])

    stats['inria'] = inria_metrics.metrics()
    stats['sdata'] = sdata_metrics.metrics()
    stats['combo'] = comb_metrics.metrics()
    stats['missing'] = missing
    return stats


def main(count=None, jobs=None):
    tag_mapper = DCSTagMapper().map_tag

    wb = Workbook()
    ws = wb.active
    ws.append(["Word", "Root", "DCS Tag", "Inria", "Sanskrit Data",
               "Both missed", "Inria only", "Sanskrit only"])

    with DCS() as dcs:
        sentences = itertools.islice(dcs.iter_sentences(), count)

        def chunk(n, iterable, fill=None):
            return itertools.zip_longest(*[iter(iterable)]*n, fillvalue=fill)

        # Number of parallel jobs, default to use all processors
        job_count = -1 if jobs is None else jobs
        chunk_size = 10000 if count is None else int(count/os.cpu_count())
        bar = progressbar.ProgressBar(max_value=jobs)
        backend = 'sequential' if job_count == 1 else 'multiprocessing'

        r = Parallel(n_jobs=job_count, backend=backend)(
            delayed(process)(sent, tag_mapper, ws)
            for sent in bar(chunk(chunk_size, sentences)))
        inria = {'count': 0, 'recognized': 0, 'correct_root': 0, 'missing': []}
        sdata = {'count': 0, 'recognized': 0, 'correct_root': 0, 'missing': []}
        combo = {'count': 0, 'recognized': 0, 'correct_root': 0, 'missing': []}

        def total(result, key, stat):
            stat['count'] += result[key][0]
            stat['recognized'] += result[key][1]
            stat['correct_root'] += result[key][2]

        for v in r:
            total(v, 'inria', inria)
            total(v, 'sdata', sdata)
            total(v, 'combo', combo)
            for x in v['missing']:
                ws.append(x)

        wb.save("lookup_results.xlsx")
        print_stats('inria', inria)
        print_stats('sanskrit_data', sdata)
        print_stats('combined', combo)


if __name__ == "__main__":
    logging.basicConfig(filename="accuracy_metrics.log", filemode="w",
                        level=logging.INFO)
    start = time.time()

    parser = argparse.ArgumentParser("Collect word level accuracy metrics")
    parser.add_argument('--count', type=int, default=None,
                        help="Limit to no. of sentences from DCS")
    parser.add_argument('--jobs', type=int, default=None,
                        help="Number of parallel jobs")

    args = parser.parse_args()

    main(args.count, args.jobs)

    logging.shutdown()
    end = time.time()
    print("Took %0.2fs" % (end - start))
