#!/usr/bin/env python

import pytest
from sanskrit_parser.lexical_analyzer.SanskritLexicalAnalyzer import SanskritLexicalAnalyzer
import sanskritmark
from sanskrit_parser.base.SanskritBase import SanskritObject,SLP1,DEVANAGARI
import logging
import re
logger = logging.getLogger(__name__)

logging.basicConfig(filename='uohd.log', filemode='w', level=logging.INFO)

@pytest.fixture(scope="module")
def lexan():
    return SanskritLexicalAnalyzer()

def get_uohd_refs(maxrefs=200):
    def _dumpchars(str):
        s = str
        # Random characters in UOHD files
        for c in ",'-;().?!\"":
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

        with open(fn) as f:
            for l in f:
                l = l.strip()
                if l and l[0] != '#':
                    if l.find('=>') == -1:
                        continue
                    logger.info(u"{}".format(unicode(l,"utf-8")))
                    full,split=l.split('=>')
                    full=unicode(full.strip(),'utf-8')
                    full=full.replace(u'|','')
                    full=_dumpchars(SanskritObject(full).transcoded(SLP1))
                    split=unicode(split.strip(),'utf-8')
                    split=split.replace(u'|','')
                    splits=map(lambda x:_dumpchars(SanskritObject(x).transcoded(SLP1).strip()),split.split('+'))
                    if splits[-1]=='':
                        splits.pop()

                    # Empty full string
                    if len(full)==0:
                        logger.info("Skipping")
                    
                    # UOHD errors, final visarga is sometimes missing
                    if len(splits[-1])>1 and splits[-1][-2:]=="AH" and full[-1]=="A":
                        full=full+"H"
                    if len(splits[-1])>1 and splits[-1][-2:]=="aH" and full[-1]=="a":
                        full=full+"H"
                    if splits[-1][-1]=="A" and len(full)>1 and full[-2:]=="AH":
                        splits[-1]=splits[-1]+"H"
                    if splits[-1][-1]=="a" and len(full)>1 and full[-2:]=="aH":
                        splits[-1]=splits[-1]+"H"
                        
                    fs.append((full,splits))
                    logger.info(u"{} => {}".format(full," ".join(splits)))
                    # -1 = run all tests
                    if maxrefs > 0:
                        m=m-1
                        if m<=0:
                            return fs
    return fs

    
def test_uohd_file_splits(lexan,uohd_refs):
    f = uohd_refs[0]
    su = uohd_refs[1]
    s = []
    for ss in su:
        # Check if this word is in our db
        # Rakarantas
        sss=ss.replace('punaH','punar')
        # Sakarantas
        sss=re.sub('H$','s',sss)
        if sss.find('punas')!=-1:
            logger.error("ERROR: found {}".format(sss))
        if sanskritmark.quicksearch(sss):
            s.append(sss)
        else:
            # If not, treat it as a word to be split
            graph=lexan.getSandhiSplits(SanskritObject(ss,encoding=SLP1),use_internal_sandhi_splitter=False)
            if graph is None:
                # Catch stray unicode symbols with the encode
                logger.warning("Skipping: {} is not in db".format(ss.encode('utf-8')))
                return
            # First split
            ssp=graph.findAllPaths(max_paths=1)[0]
            # Add it to split list
            s.extend(ssp)
            
    # UOHD stores sandhied final words!
    # This is not a full fix
    f=re.sub("o$","aH",f)
    i=SanskritObject(f,encoding=SLP1)
    graph=lexan.getSandhiSplits(i,use_internal_sandhi_splitter=False)
    assert graph is not None
    splits=graph.findAllPaths(max_paths=1000,sort=False)
    if s not in splits:
        # Currently, this triggers a fallback to all_simple_paths
        splits=graph.findAllPaths(max_paths=10000,sort=False)
    if splits is None or s not in splits:
        logger.error("FAIL: {} not in {}".format(s,splits))
    assert s in splits
       
def pytest_generate_tests(metafunc):

    if 'uohd_refs' in metafunc.fixturenames:
        uohd_refs = get_uohd_refs(maxrefs=10000)
        metafunc.parametrize("uohd_refs", uohd_refs)
