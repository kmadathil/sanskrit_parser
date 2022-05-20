'''
Created on Jul 7, 2017

@author: alvarna
'''
from __future__ import print_function
import codecs
import os
import inspect
from sanskrit_parser.lexical_analyzer.sandhi import Sandhi
from indic_transliteration import sanscript
from sanskrit_parser.base.sanskrit_base import SanskritObject
import logging
import re
import six
import json

logger = logging.getLogger(__name__)


def sandhi_join_pass(sandhiobj, split, join):
    objs = map(lambda x: SanskritObject(x, encoding=sanscript.SLP1), split)
    joins = sandhiobj.join(*objs)
    d = {
        "input": map(to_devanagari, split),
        "expected": to_devanagari(join),
        "file": filename,
        "line": linenum}
    if joins and join in joins:
        res = True
    else:
        d["actual"] = map(to_devanagari, joins) if joins else None
        res = False
    s = json.dumps(d, ensure_ascii=False) + "\n"
    return (res, s)


def sandhi_split_pass(sandhiobj, split, join):
    splits = sandhiobj.split_all(SanskritObject(join, encoding=sanscript.SLP1))
    d = {
        "input": to_devanagari(join),
        "expected": map(to_devanagari, split),
        #         "actual": map(to_devanagari, splits) if splits else None,
        "file": filename,
        "line": linenum}
    if splits and split in splits:
        res = True
    else:
        res = False
    s = json.dumps(d, ensure_ascii=False) + "\n"
    return (res, s)


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


def clean_references(splits, full):
    def _dumpchars(str):
        # Remove whitespace characters
        s = re.sub(r"\W+", "", str)
        # Random characters in UOHD files
        for c in ",'-;().?!\"0123456789":
            s = s.replace(c, '')
        # Some bad visargas
        s = s.replace(':', 'H')
        # UOHD RHS has word-ending anusvaras
        s = re.sub('M$', 'm', s)
        return s

    full = _dumpchars(full)
    splits = list(map(_dumpchars, splits))
    if splits[-1] == '':
        splits.pop()
    if splits[0] == '':
        splits.pop(0)
    if len(splits) != 2:
        return None

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

    # UOHD stores sandhied final words!
    # This is not a full fix
    full = re.sub("o$", "aH", full)
    full = re.sub("d$", "t", full)

    return splits, full


def load_reference_data_from_file(filename):
    sandhi_references = []
    basename = os.path.basename(filename)
    logger.debug("Processing tests from file %s", basename)
    with codecs.open(filename, "rb", 'utf-8') as f:
        for linenum, line in enumerate(f):
            line = line.strip()
            if line.startswith('#') or line == '':
                continue
            ref = SanskritObject(line).transcoded(sanscript.SLP1)
            if "=>" in line:
                joined, splits = map(six.text_type.strip, ref.split("=>"))
            elif "=" in line:
                splits, joined = map(six.text_type.strip, ref.split("="))
            else:
                continue
            split = list(map(six.text_type.strip, splits.split('+')))
            clean = clean_references(split, joined)
            if clean:
                split, joined = clean
                sandhi_references.append((tuple(split), joined, basename, linenum + 1))
    return sandhi_references


def to_devanagari(obj):
    if isinstance(obj, (six.text_type, six.string_types)):
        obj = SanskritObject(obj, encoding=sanscript.SLP1)
    if isinstance(obj, SanskritObject):
        return obj.devanagari()
    else:
        return map(to_devanagari, obj)


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    directory = os.path.join(base_dir, "sandhi_test_data")
    join_passing = codecs.open(os.path.join(directory, "sandhi_join_passing.txt"), "w", encoding='utf-8')
    join_failing = codecs.open(os.path.join(directory, "sandhi_join_failing.txt"), "w", encoding='utf-8')
    split_passing = codecs.open(os.path.join(directory, "sandhi_split_passing.txt"), "w", encoding='utf-8')
    split_failing = codecs.open(os.path.join(directory, "sandhi_split_failing.txt"), "w", encoding='utf-8')
    sandhiobj = Sandhi()
    num_join_pass, num_join_fail, num_split_pass, num_split_fail = 0, 0, 0, 0
    for split, join, filename, linenum in load_reference_data():
        (res, s) = sandhi_join_pass(sandhiobj, split, join)
        if res:
            join_passing.write(s)
            num_join_pass += 1
        else:
            join_failing.write(s)
            num_join_fail += 1

        (res, s) = sandhi_split_pass(sandhiobj, split, join)
        if res:
            split_passing.write(s)
            num_split_pass += 1
        else:
            split_failing.write(s)
            num_split_fail += 1
    join_passing.close()
    join_failing.close()
    split_failing.close()
    split_failing.close()

    print("Join:")
    print("Pass: {0} / {2} Fail: {1} / {2}".format(num_join_pass, num_join_fail, (num_join_fail + num_join_pass)))
    print("Split:")
    print("Pass: {0} / {2} Fail: {1} / {2}".format(num_split_pass, num_split_fail, (num_split_fail + num_split_pass)))
