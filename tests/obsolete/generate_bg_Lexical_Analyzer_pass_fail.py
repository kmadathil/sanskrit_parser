#!/usr/bin/env python

from __future__ import print_function

import codecs
import inspect
import json
import logging
import os
import re
import progressbar

from indic_transliteration import sanscript
from sanskrit_parser.base.sanskrit_base import SanskritObject
from sanskrit_parser.lexical_analyzer.sanskrit_lexical_analyzer import SanskritLexicalAnalyzer

logger = logging.getLogger(__name__)

logging.basicConfig(filename='gen_bg_lexan_passfail.log', filemode='w',
                    level=logging.INFO)


def process_bg_file(fn, m):
    ''' Process a single Bg file, up to a max of m lines
    '''
    fs = []
    logger.info("Processing tests from file %s", fn)
    basename = os.path.basename(fn)  # Save
    with codecs.open(fn, "rb", 'utf-8') as f:
        # "S0" "S1" "S2" "S3" "S4"
        state = "S0"  # Wait state
        for lnum, l in enumerate(f):
            if m != 0:
                line = l.strip()
                # Samasa splitters
                line = line.replace(r'\-', ' ')
                # ITRANS Halanta symbol, not handled right?
                line = line.replace('.h', '')
                logger.info("State {}".format(state))
                if line:
                    if line[0] == '%':
                        logger.info("Skipping comment: {}".format(line))
                        continue
                    if line[0] == '\\':
                        logger.info("Skipping command: {}".format(line))
                        continue
                if state == "S0":  # Default State
                    if not line:
                        logger.info("Skipping blank: {}".format(line))
                        continue
                    elif line[-2:] == " .":  # Found |
                        prev = line
                        pnum = lnum
                        state = "S1"
                        logger.info("Moving to S1: {}".format(line))
                    else:
                        logger.info("Skipping unknown: {}".format(line))
                        continue
                elif state == "S1":
                    if not line:
                        logger.info("Found blank, moving to S0: {}".format(line))
                        state = "S0"
                        continue
                    if line[-2:] == " .":  # Found | , non verse
                        prev = line
                        pnum = lnum
                        state = "S0"
                        r = [prev[:-2], line.split(" ")[:-1], prev, line, False,
                             basename, pnum]
                        logger.info("Appending {}".format(r))
                        fs.append(r)
                        if m > 0:
                            m = m - 1
                        logger.info("Moving to S0: {}".format(line))
                    elif line[-2:] == "..":  # Found ||, verse
                        prev2 = line
                        pnum2 = lnum
                        state = "S2"
                        logger.info("Moving to S2: {}".format(line))
                    else:
                        logger.info("Going to S0: unknown: {}".format(line))
                        state = "S0"
                    continue
                elif state == "S2":
                    if not line:
                        logger.info("Found blank: {}".format(line))
                        continue
                    if line[-2:] == " .":  # Found | verse split 1
                        split1 = line
                        # snum1  = lnum
                        state = "S3"
                    else:
                        logger.info("Going to S0: unknown: {}".format(line))
                        state = "S0"
                    continue
                elif state == "S3":
                    if not line:
                        logger.info("Found blank, going to S0: {}".format(line))
                        state = "S0"
                        continue
                    if line[-2:] == "..":  # Found |  verse split 2
                        split2 = line
                        # snum2 = lnum
                        state = "S0"
                        r = [prev[:-2], split1.split(" ")[:-1], prev, split1, False,
                             basename, pnum]
                        logger.info("Appending {}".format(r))
                        fs.append(r)
                        rprev2 = prev2[:prev2.find("..")].strip()
                        rsplit2 = split2[:split2.find("..")].strip().split(" ")
                        r = [rprev2, rsplit2, prev2, split2, False,
                             basename, pnum2]
                        logger.info("Appending {}".format(r))
                        fs.append(r)
                        if m > 0:
                            m = m - 1
                        logger.info("Going to S0: {}".format(line))
                    else:
                        logger.info("Going to S0: unknown: {}".format(line))
                        state = "S0"
                    continue
            else:
                break
    return fs


def get_bg_refs(lexan, maxrefs=200):
    fs = []
    # Max splits for the next file, initialize
    m = maxrefs
    flist = ["sandhi_test_data/gitAanvayasandhivigraha.itx"]
    for fn in flist:
        if m != 0:
            r = process_bg_file(fn, m)
            if r is not None:
                fs.extend(r)
                m = m - len(r)
        else:
            break
    return fs


# FIXME - need to store the modified f,s instead of input references
def test_splits(lexan, bg_refs):
    # Check if s is in splits
    def _in_splits(s, splits):
        return s in [list(map(str, ss)) for ss in splits]

    f = bg_refs[0]
    s = [re.sub('H$', 's', SanskritObject(sx, encoding=sanscript.ITRANS).canonical()) for sx in bg_refs[1]]
    i = SanskritObject(f, encoding=sanscript.ITRANS)
    try:
        # for sss in s:
        #   if not lexan.forms.valid(sss):
        #       return "Skip"
        graph = lexan.getSandhiSplits(i)
        if graph is None:
            logger.error("FAIL: Empty split for {}".format(i.canonical().encode('utf-8')))
            return False
        # Reducing max_paths to 100
        splits = graph.findAllPaths(max_paths=100, sort=False)
        r = _in_splits(s, splits)
        if splits is None or (not r):
            logger.error("FAIL: {} not in {}".format(s, splits))
        return r
    except:  # noqa
        logger.warning("Split Exception: {}".format(i.canonical().encode('utf-8')))
        return "Error"


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    directory = os.path.join(base_dir, "test_data_SanskritLexicalAnalyzer")
    passing = codecs.open(os.path.join(directory, "bg_passing.txt"), "w", encoding='utf-8')
    split_passing = codecs.open(os.path.join(directory, "bg_split_passing.txt"), "w", encoding='utf-8')
    failing = codecs.open(os.path.join(directory, "bg_failing.txt"), "w", encoding='utf-8')
    skip = codecs.open(os.path.join(directory, "bg_skip.txt"), "w", encoding='utf-8')
    error = codecs.open(os.path.join(directory, "bg_error.txt"), "w", encoding='utf-8')
    lexan = SanskritLexicalAnalyzer()
    maxrefs = 20000
    bar = progressbar.ProgressBar(maxval=maxrefs)
    fail_count = skip_count = error_count = pass_count = split_count = 0
    for full, split, ofull, osplit, splitp, filename, linenum in \
            bar(get_bg_refs(lexan=lexan, maxrefs=maxrefs)):
        test = json.dumps({"full": full,
                           "split": split,
                           "orig_full": ofull,
                           "orig_split": osplit,
                           "filename": filename,
                           "linenum": linenum}) + "\n"
        sr = test_splits(lexan, (full, split))
        if sr == "Skip":
            skip.write(test)
            skip_count += 1
        elif sr == "Error":
            error.write(test)
            error_count += 1
        elif sr:
            if splitp:
                split_passing.write(test)
                split_count += 1
            else:
                passing.write(test)
                pass_count += 1
        else:
            failing.write(test)
            fail_count += 1

    passing.close()
    failing.close()
    error.close()
    skip.close()

    print("Pass = %d, Split Pass = %d, Fail = %d, Skip = %d, Error = %d" % (pass_count, split_count, fail_count, skip_count, error_count))
