#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from sanskrit_parser.parser.sandhi_analyzer import LexicalSandhiAnalyzer
from sanskrit_parser.base.sanskrit_base import SanskritObject, DEVANAGARI, outputctx
import pandas as pd
import multiprocessing
import os.path
import inspect

le = LexicalSandhiAnalyzer()


def get_kosh_entries(test_count=0):
    kosh_entries = []
    base_dir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
    data_dir = os.path.join(base_dir, 'SandhiKosh')
    aa_kosh = pd.read_excel(os.path.join(data_dir, "Astaadhyaayii Corpus.xls"))[['S. No.', 'Word', 'Split']]
    aa_kosh['File'] = "Astaadhyaayii Corpus.xls"
    bg_kosh = pd.read_excel(os.path.join(data_dir, "Bhagvad_Gita Corpus.xls"))[['S. No.', 'Word', 'Split']]
    bg_kosh['File'] = "Bhagvad_Gita Corpus.xls"
    uoh_kosh = pd.read_excel(os.path.join(data_dir, "UoH_Corpus.xls"))[['S. No.', 'Word', 'Split']]
    uoh_kosh['File'] = "UoH_Corpus.xls"
    lit_kosh_dict = pd.read_excel(os.path.join(data_dir, "Rule-based Corpus and Literature Corpus.xls"), sheet_name=None)
    for k in ['Internal', 'External', 'Literature']:
        t_kosh = lit_kosh_dict[k].loc[:, ['S. No.', 'Word', 'Split']]
        t_kosh['File'] = f"Rule-based Corpus and Literature Corpus.xls:{k}"
        kosh_entries.extend(t_kosh.to_dict(orient='records'))
    kosh_entries.extend(bg_kosh.to_dict(orient='records'))
    kosh_entries.extend(uoh_kosh.to_dict(orient='records'))
    kosh_entries.extend(aa_kosh.to_dict(orient='records'))
    return kosh_entries[:test_count] if test_count > 0 else kosh_entries


def sort_file_splits(kosh_entry):
    global le
    clean_input = False
    f = kosh_entry['Word']
    s = kosh_entry['Split']
    clean_input = True
    with outputctx(False):
        i = SanskritObject(f, encoding=DEVANAGARI, strict_io=True, replace_ending_visarga=None)
        if not(isinstance(s, str)):
            # Bad input
            return "Bad_Input"
        if clean_input:
            sl = [SanskritObject(x, encoding=DEVANAGARI, strict_io=True,
                                 replace_ending_visarga=None).canonical()
                  for x in s.strip().replace(" ", "+").split('+')]
        else:
            sl = [SanskritObject(x, encoding=DEVANAGARI, strict_io=True, replace_ending_visarga=None).canonical() for x in s.split('+')]
        graph = le.getSandhiSplits(i)
        if graph is not None:
            splits = graph.find_all_paths(max_paths=300, sort=False)
            if sl in [list(map(str, ss)) for ss in splits]:
                # Pass
                print("P", end='', flush=True)
                return "Pass"
            else:
                print("F", end='', flush=True)
                return "Fail"
        else:
            print("S", end='', flush=True)
            return "Split_Fail"


entries = get_kosh_entries()
print(f"Collected {len(entries)} tests")
with multiprocessing.Pool(4) as p:
    result = p.map(sort_file_splits, entries)
# result = map(sort_file_splits, entries)
print("")  # Newline
odf = pd.DataFrame.from_records(entries)
odf['Status'] = result
odf.to_excel("Result.xls")
print("Wrote to Result.xls")
passcount = result.count("Pass")
failcount = result.count("Fail")
splitfailcount = result.count("Split_Fail")
badcount = result.count("Bad_Input")
print(f"{passcount} Passed, {failcount} Failed, {splitfailcount} No_Split, {badcount} Bad tests")
