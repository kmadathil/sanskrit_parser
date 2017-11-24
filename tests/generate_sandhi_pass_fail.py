'''
Created on Jul 7, 2017

@author: alvarna
'''
from __future__ import print_function
import codecs
import os
import inspect
from sanskrit_parser.lexical_analyzer.sandhi import Sandhi
from sanskrit_parser.base.SanskritBase import SanskritObject, SLP1, DEVANAGARI
import logging
import re
import six
import json

logger = logging.getLogger(__name__)

def sandhi_join_pass(sandhiobj, before, after):
    objs = map(lambda x:SanskritObject(x, encoding = DEVANAGARI), before)
    joins = sandhiobj.join(*objs)
    try:
        return after in joins
    except TypeError:
        return False

def sandhi_split_pass(sandhiobj, before, after):
    obj = SanskritObject(after, encoding=DEVANAGARI)
    splits = sandhiobj.split_all(obj)
    try:
        return before in splits
    except TypeError:
        return False

def load_reference_data():
    files = [
            'refs.txt',
            '2.karnabhara-ext.txt',
            '130-short-stories-extracted.txt',
            'vetalkatha_ext.txt',
            '4.dutaghatotgajam-ext.txt',
            '3.dutavakyam-ext.txt',
            'madyama_ext.txt',
            'vrubhangam_ext.txt',
            'balaramayanam_ext.txt',
            '5.balacharitham-ext.txt',
            '1.abhishakanatakam-ext.txt',
            '7.charudattam-ext.txt',
            'vinodini-ext.txt',
            'astanga-hridayam-sandhi-extract1-27.txt',
            'madhavi-ext.txt',
            'manjusa-ext.txt',
            'tarkabhasha-ext.txt',
            'Rajkathakunj_ext.txt',
            'Aakhyanvallari_ext.txt',
            'sanskritkathashatkam1_ext.txt',
            'nyayasara-ext.txt',
            'tarkchudamani-ext.txt',
            'Sanskritkathakunj_ext.txt',
            'agnipuran-1-111-sandhi_ext.txt',
            'vyutpattivada-ext.txt'
             ]
    sandhi_references = []
    base_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    directory = os.path.join(base_dir, "sandhi_test_data")
    for filename in files:
            sandhi_references.extend(load_reference_data_from_file(os.path.join(directory, filename)))
    return sandhi_references

def load_reference_data_from_file(filename):
    sandhi_references = []
    basename = os.path.basename(filename)
    logger.debug("Processing tests from file %s", basename)
    with codecs.open(filename, "rb", 'utf-8') as f:
        for linenum, line in enumerate(f):
            line = line.strip()
            if line.startswith('#') or line == '':
                continue
            ref = SanskritObject(line).transcoded(SLP1)
            if "=>" in line:
                after, b = map(six.text_type.strip, ref.split("=>"))
            elif "=" in line:
                b, after = map(six.text_type.strip, ref.split("="))
            else:
                continue
            before = list(map(six.text_type.strip, b.split('+')))
            if len(before) == 2:
                before[0] = re.sub("\W+", "", before[0])
                before[1] = re.sub("\W+", "", before[1])
                after = re.sub("\W+", "", after)
                sandhi_references.append((tuple(before), after, basename, linenum+1))
    return sandhi_references

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    directory = os.path.join(base_dir, "sandhi_test_data")
    join_passing = codecs.open(os.path.join(directory, "sandhi_join_passing.txt"), "w", encoding='utf-8')
    join_failing = codecs.open(os.path.join(directory, "sandhi_join_failing.txt"), "w", encoding='utf-8')
    split_passing = codecs.open(os.path.join(directory, "sandhi_split_passing.txt"), "w", encoding='utf-8')
    split_failing = codecs.open(os.path.join(directory, "sandhi_split_failing.txt"), "w", encoding='utf-8')   
    sandhiobj = Sandhi()  
    for before, after, filename, linenum in load_reference_data():
        test = json.dumps({"before":before, "after":after, "filename": filename, "linenum":linenum}) + "\n"
#         print(test)
        if sandhi_join_pass(sandhiobj, before, after):
            join_passing.write(test)
        else:
            join_failing.write(test)
        if sandhi_split_pass(sandhiobj, before, after):
            split_passing.write(test)
        else:
            split_failing.write(test)
    join_passing.close()
    join_failing.close()
    split_failing.close()
    split_failing.close()
