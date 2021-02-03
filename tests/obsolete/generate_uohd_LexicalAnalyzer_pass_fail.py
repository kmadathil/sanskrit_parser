#!/usr/bin/env python

from __future__ import print_function

import codecs
import inspect
import json
import logging
import os
import re
import progressbar

from sanskrit_parser.base.sanskrit_base import SanskritObject, SLP1
from sanskrit_parser.lexical_analyzer.sanskrit_lexical_analyzer import SanskritLexicalAnalyzer

logger = logging.getLogger(__name__)

logging.basicConfig(filename='gen_uohd_lexan_passfail.log', filemode='w',
                    level=logging.INFO)


def _dumpchars(sr):
    s = sr
    # Random characters in UOHD files
    for c in ",'-;().?!*\"0123456789":
        s = s.replace(c, '')
    # Some bad visargas
    s = s.replace(':', 'H')
    # UOHD RHS has word-ending anusvaras
    s = re.sub('M$', 'm', s)
    return s


def process_line(lnum, line_in):
    '''Process a single line'''
    logging.info("Processing Line {}: {}".format(lnum, line_in))
    r = None
    subsplitp = False
    line = line_in.strip()
    if line and line[0] == '#':
        logging.info("Skipping Comment")
        return None
    if line.find('=>') == -1:
        logging.info("Cannot find =>")
        return None
    full, split = line.split('=>')
    full = full.strip()
    full = full.replace(u'|', '')
    # Zero width joiner/nonjoiner
    full = full.replace(u"\u200c", "")
    full = full.replace(u"\u200d", "")
    ofull = full  # Save
    full = _dumpchars(SanskritObject(full).transcoded(SLP1))
    split = split.strip()
    split = split.replace(u'|', '')
    # Zero width joiner/nonjoiner
    split = split.replace(u"\u200c", "")
    split = split.replace(u"\u200d", "")
    osplit = split  # Save
    splits = list(map(lambda x: _dumpchars(SanskritObject(x).transcoded(SLP1).strip()), split.split('+')))
    if splits[-1] == '':
        splits.pop()
    # Empty full string
    if len(full) == 0:
        logger.info("Skipping")

    # UOHD errors, final visarga is sometimes missing
    if len(splits[-1]) > 1 and splits[-1][-2:] == "AH" and \
       full[-1] == "A":
        full = full + "H"
    if len(splits[-1]) > 1 and splits[-1][-2:] == "aH" and \
       full[-1] == "a":
        full = full + "H"
    if splits[-1][-1] == "A" and len(full) > 1 and full[-2:] == "AH":
        splits[-1] = splits[-1] + "H"
    if splits[-1][-1] == "a" and len(full) > 1 and full[-2:] == "aH":
        splits[-1] = splits[-1] + "H"

    # FIXME - this creates problems, eg on 'aho', 'prabho'
    # UOHD stores sandhied final words!
    # This is not a full fix
    full = re.sub("o$", "aH", full)
    # Modified splits
    s = []

    for ss in splits:
        # Check if this word is in our db
        # Rakarantas
        # FIXME - these four replacements aren't working
        # Check intent and actual operation
        sss = ss.replace('punaH', 'punar')
        sss = ss.replace('antaH', 'antar')
        sss = ss.replace('bahiH', 'bahir')
        sss = ss.replace('prAtaH', 'prAtar')
        # FIXME - the above four replacements aren't working
        # Sakarantas
        sss = re.sub('H$', 's', sss)
        if sss.find('punas') != -1:
            logger.error("ERROR: found {}".format(sss))
            # Is in our database
        if (subsplitp == "Skip") or lexan.forms.valid(sss):
            s.append(sss)
        else:
            # If not, treat it as a word to be split
            try:
                graph = lexan.getSandhiSplits(SanskritObject(ss, encoding=SLP1))
                if graph is None:
                    # Catch stray unicode symbols with the encode
                    logger.warning("Skipping: {} is not in db".format(ss.encode('utf-8')))
                    subsplitp = "Skip"
                    s.append(sss)
                    continue
                else:
                    subsplitp = True
            except:  # noqa
                logger.warning("Split Error: {}".format(ss.encode('utf-8')))
                s.append(sss)
                continue
            # First split
            ssp = list(map(str, graph.findAllPaths(max_paths=1)[0]))
            # Add it to split list
            s.extend(map(str, ssp))
    logger.info(u"{} => {}".format(full, " ".join(s)))
    r = [full, s, ofull, osplit, subsplitp]
    return r


def process_uohd_file(fn, m):
    ''' Process a single UoHD file, up to a max of m lines
    '''
    fs = []
    logger.info("Processing tests from file %s", fn)
    basename = os.path.basename(fn)  # Save
    with codecs.open(fn, "rb", 'utf-8') as f:
        for lnum, l in enumerate(f):
            if m != 0:
                r = process_line(lnum, l)
                if r is not None:
                    r.extend([basename, lnum])
                    logger.info("Appending {}".format(r))
                    fs.append(r)
                    if m > 0:
                        m = m - 1
            else:
                break
    return fs


def get_uohd_refs(lexan, maxrefs=200):
    fs = []
    # Max splits for the next file, initialize
    m = maxrefs
    flist = ["sandhi_test_data/130-short-stories-extracted.txt",
             "sandhi_test_data/agnipuran-1-111-sandhi_ext.txt",
             "sandhi_test_data/Sanskritkathakunj_ext.txt",
             "sandhi_test_data/1.abhishakanatakam-ext.txt",
             "sandhi_test_data/astanga-hridayam-sandhi-extract1-27.txt",
             "sandhi_test_data/sanskritkathashatkam1_ext.txt",
             "sandhi_test_data/2.karnabhara-ext.txt",
             "sandhi_test_data/balaramayanam_ext.txt",
             "sandhi_test_data/tarkabhasha-ext.txt",
             "sandhi_test_data/3.dutavakyam-ext.txt",
             "sandhi_test_data/madhavi-ext.txt",
             "sandhi_test_data/tarkchudamani-ext.txt",
             "sandhi_test_data/4.dutaghatotgajam-ext.txt",
             "sandhi_test_data/madyama_ext.txt",
             "sandhi_test_data/vetalkatha_ext.txt",
             "sandhi_test_data/5.balacharitham-ext.txt",
             "sandhi_test_data/manjusa-ext.txt",
             "sandhi_test_data/vinodini-ext.txt",
             "sandhi_test_data/7.charudattam-ext.txt",
             "sandhi_test_data/nyayasara-ext.txt",
             "sandhi_test_data/vrubhangam_ext.txt",
             "sandhi_test_data/Aakhyanvallari_ext.txt",
             "sandhi_test_data/Rajkathakunj_ext.txt",
             "sandhi_test_data/vyutpattivada-ext.txt"]
    for fn in flist:
        if m != 0:
            r = process_uohd_file(fn, m)
            if r is not None:
                fs.extend(r)
                m = m - len(r)
        else:
            break
    return fs


# FIXME - need to store the modified f,s instead of input references
def test_splits(lexan, uohd_refs):
    # Check if s is in splits
    def _in_splits(s, splits):
        return s in [list(map(str, ss)) for ss in splits]

    f = uohd_refs[0]
    s = uohd_refs[1]
    i = SanskritObject(f, encoding=SLP1)
    try:
        # for sss in s:
        #    if not lexan.forms.valid(sss):
        #        return "Skip"
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
    passing = codecs.open(os.path.join(directory, "uohd_passing.txt"), "w", encoding='utf-8')
    split_passing = codecs.open(os.path.join(directory, "uohd_split_passing.txt"), "w", encoding='utf-8')
    failing = codecs.open(os.path.join(directory, "uohd_failing.txt"), "w", encoding='utf-8')
    skip = codecs.open(os.path.join(directory, "uohd_skip.txt"), "w", encoding='utf-8')
    error = codecs.open(os.path.join(directory, "uohd_error.txt"), "w", encoding='utf-8')
    lexan = SanskritLexicalAnalyzer()
    maxrefs = 20000
    bar = progressbar.ProgressBar(maxval=maxrefs)
    fail_count = skip_count = error_count = pass_count = split_count = 0
    for full, split, ofull, osplit, splitp, filename, linenum in \
            bar(get_uohd_refs(lexan=lexan, maxrefs=maxrefs)):
        test = json.dumps({"full": full,
                           "split": split,
                           "orig_full": ofull,
                           "orig_split": osplit,
                           "filename": filename,
                           "linenum": linenum}) + "\n"
        sr = test_splits(lexan, (full, split))
        if splitp == "Skip":
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
