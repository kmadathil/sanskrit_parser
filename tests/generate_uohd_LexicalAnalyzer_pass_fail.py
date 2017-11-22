#!/usr/bin/env python

from __future__ import print_function

from sanskrit_parser.lexical_analyzer.SanskritLexicalAnalyzer import SanskritLexicalAnalyzer
from sanskrit_parser.base.SanskritBase import SanskritObject,SLP1,DEVANAGARI
import logging
import re
import six
import json
import os
import codecs
import inspect

logger = logging.getLogger(__name__)

logging.basicConfig(filename='gen_uohd_lexan_passfail.log', filemode='w',
                    level=logging.INFO)


def get_uohd_refs(maxrefs=200):
    def _dumpchars(str):
        s = str
        # Random characters in UOHD files
        for c in ",'-;().?!\"0123456789":
            s=s.replace(c,'')
        # Some bad visargas
        s=s.replace(':','H')
        # UOHD RHS has word-ending anusvaras
        s=re.sub('M$','m',s)
        return s
    fs = []
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
        logger.info("Processing tests from file %s", fn)
        basename = os.path.basename(fn) # Save
        with codecs.open(fn,"rb", 'utf-8') as f:
            for lnum,l in enumerate(f):
                l = l.strip()
                if l and l[0] != '#':
                    if l.find('=>') == -1:
                        continue
                    logger.info(u"{}".format(l))
                    full,split=l.split('=>')
                    full=full.strip()
                    full=full.replace(u'|','')
                    ofull=full # Save
                    full=_dumpchars(SanskritObject(full).transcoded(SLP1))
                    split=split.strip()
                    split=split.replace(u'|','')
                    osplit=split # Save 
                    splits=map(lambda x:_dumpchars(SanskritObject(x).transcoded(SLP1).strip()),split.split('+'))
                    if splits[-1]=='':
                        splits.pop()

                    # Empty full string
                    if len(full)==0:
                        logger.info("Skipping")
                    
                    # UOHD errors, final visarga is sometimes missing
                    if len(splits[-1])>1 and splits[-1][-2:]=="AH" and \
                       full[-1]=="A":
                        full=full+"H"
                    if len(splits[-1])>1 and splits[-1][-2:]=="aH" and \
                       full[-1]=="a":
                        full=full+"H"
                    if splits[-1][-1]=="A" and len(full)>1 and full[-2:]=="AH":
                        splits[-1]=splits[-1]+"H"
                    if splits[-1][-1]=="a" and len(full)>1 and full[-2:]=="aH":
                        splits[-1]=splits[-1]+"H"
                        
                    fs.append((full,splits,ofull,osplit,basename,lnum))
                    logger.info(u"{} => {}".format(full," ".join(splits)))
                    # -1 = run all tests
                    if maxrefs > 0:
                        m=m-1
                        if m<=0:
                            return fs
    return fs


# FIXME - need to store the modified f,s instead of input references
def test_splits(lexan,uohd_refs):
    # Check if s is in splits
    def _in_splits(s,splits):
        return s in [map(str,ss) for ss in splits]
    f = uohd_refs[0]
    su = uohd_refs[1]
    s = []
    for ss in su:
        # Check if this word is in our db
        # Rakarantas
        sss=ss.replace('punaH','punar')
        sss=ss.replace('antaH','antar')
        sss=ss.replace('bahiH','bahir')
        # Sakarantas
        sss=re.sub('H$','s',sss)
        if sss.find('punas')!=-1:
            logger.error("ERROR: found {}".format(sss))
        # Is in our database
        if lexan.forms.valid(sss):
            s.append(sss)
        else:
            # If not, treat it as a word to be split
            try:
                graph=lexan.getSandhiSplits(SanskritObject(ss,encoding=SLP1))
                if graph is None:
                    # Catch stray unicode symbols with the encode
                    logger.warning("Skipping: {} is not in db".format(ss.encode('utf-8')))
                    return "Skip"
            except:
                logger.warning("Split Error: {}".format(ss.encode('utf-8')))
                return "Error"
            # First split
            ssp=map(str,graph.findAllPaths(max_paths=1)[0])
            # Add it to split list
            s.extend(map(str,ssp))
            
    # UOHD stores sandhied final words!
    # This is not a full fix
    f=re.sub("o$","aH",f)
    i=SanskritObject(f,encoding=SLP1)
    try:
        graph=lexan.getSandhiSplits(i)
        if graph is None:
            return False
        splits=graph.findAllPaths(max_paths=1000,sort=False)
        if not _in_splits(s,splits):
            # Currently, this triggers a fallback to all_simple_paths
            splits=graph.findAllPaths(max_paths=10000,sort=False)
        if splits is None or not _in_splits(s,splits):
            logger.error("FAIL: {} not in {}".format(s,splits))
        return _in_splits(s,splits)
    except:
        logger.warning("Split Exception: {}".format(i.canonical().encode('utf-8')))
        return "Error"
        

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    directory = os.path.join(base_dir, "test_data_SanskritLexicalAnalyzer")
    passing = codecs.open(os.path.join(directory, "uohd_passing.txt"), "w", encoding='utf-8')
    failing = codecs.open(os.path.join(directory, "uohd_failing.txt"), "w", encoding='utf-8')
    skip    = codecs.open(os.path.join(directory, "uohd_skip.txt"), "w", encoding='utf-8')
    error   = codecs.open(os.path.join(directory, "uohd_error.txt"), "w", encoding='utf-8')
    lexan   = SanskritLexicalAnalyzer()
    for full, split, ofull, osplit, filename, linenum in \
        get_uohd_refs(maxrefs=10000):
        test = json.dumps({"full":full,
                           "split":split,
                           "filename": filename,
                           "linenum":linenum}) + "\n"
        if test_splits(lexan,(full,split))=="Error":
            error.write(test)
        elif test_splits(lexan,(full,split))=="Skip":
            skip.write(test)
        elif test_splits(lexan,(full,split)):
            passing.write(test)
        else:
            failing.write(test)

    passing.close()
    failing.close()
    error.close()
    skip.close()
