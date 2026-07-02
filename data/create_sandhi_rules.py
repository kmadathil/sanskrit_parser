# -*- coding: utf-8 -*-
"""
Pre-expand and save the rules for sandhi.py

"""

import itertools
import codecs
import os
import re
import inspect
import logging
import pickle
from marisa_trie import BytesTrie


from zipfile import ZipFile, ZIP_DEFLATED
from collections import defaultdict

from indic_transliteration import sanscript
from sanskrit_parser.base.sanskrit_base import SanskritImmutableString
from sanskrit_parser.base.maheshvara_sutra import MaheshvaraSutras


class Sandhi(object):

    def __init__(self):
        """
        Sandhi class constructor

        :param rules_dir: directory to read rules from
        :param use_default_rules: reads pre-built-rules from sandhi_rules dir under module directory
        :param logger: instance of python logger to use
        """
        self.lc_len_max = 0
        self.rc_len_max = 0
        self.forward = []
        self.backward = []
        self.logger = logging.getLogger(__name__)

        base_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        self.add_rules_from_dir(os.path.join(base_dir, "sandhi_rules"))


    def add_rule(self, before, after, annotation=None):
        """
        Adds a single sandhi rule to the rule database

        :param before: tuple of length two of the varNas involved in the sandhi
        :param after: result of the sandhi
        """
        self.lc_len_max = max(self.lc_len_max, len(before[0]))
        self.rc_len_max = max(self.rc_len_max, len(before[1]))
        self.forward.append((f"{before[0]}+{before[1]}", f"{after},{annotation}".encode()))
        self.backward.append((after, f"{before[0]},{before[1]},{annotation}".encode()))

    def expand_rule(self, rule):
        """
        Expands a given sandhi rule from the rules file to generate all possible combinations

        :param rule: Rule to expand
        :return: A generator of all possible expanded rules
        """
        self.logger.debug("Expanding rule %s", rule)

        ms = MaheshvaraSutras()

        b, afters = map(str.strip, rule.split("="))
        before = list(map(str.strip, b.split("+", 1)))
        left_classes = re.split(r'\[(.*?)\]', before[0])
        self.logger.debug("Left classes = %s", left_classes)

        # Split after forms into individual forms
        afters = map(str.strip, afters.split("/"))

        before_left = []
        for c in left_classes:
            if c != '':
                if c.startswith("*"):
                    # This is a mAheswara sUtra pratyAhAra
                    splits = list(map(str.strip, c.split('-')))
                    varnas = set(ms.getPratyahara(
                        SanskritImmutableString(splits[0][1:], encoding=sanscript.SLP1),
                        longp=False, remove_a=True, dirghas=True).canonical())
                    if len(splits) == 2:
                        varnas -= set(splits[1])
                    self.logger.debug("Found pratyAhAra %s = %s", c, varnas)
                    before_left.append(varnas)
                else:
                    before_left.append(map(str.strip, c.split(",")))
        self.logger.debug("before_left iterator = %s", before_left)

        right_classes = re.split(r'\[(.*?)\]', before[1])
        # Could have used list comprehension, but this is easier to read
        self.logger.debug("right_classes = %s", right_classes)
        if right_classes:
            before_right = []
            for c in right_classes:
                if c != '':
                    if c.startswith("*"):
                        # This is a mAheswara sUtra pratyAhAra
                        splits = list(map(str.strip,
                                          re.split('([+-])', c)))
                        varnas = set(
                            ms.getPratyahara(
                                SanskritImmutableString(splits[0][1:], encoding=sanscript.SLP1),
                                longp=False, remove_a=True, dirghas=True)
                            .canonical()
                        )
                        if len(splits) == 3:
                            if splits[1] == '-':
                                varnas -= set(splits[2])
                            elif splits[1] == '+':
                                varnas |= set(splits[2])
                        self.logger.debug("Found pratyAhAra %s (%s) = %s", c, splits[0][1:], varnas)
                        before_right.append(varnas)
                    else:
                        before_right.append(map(str.strip, c.split(",")))
        else:
            before_right = [before[1].strip()]
        self.logger.debug("before_right iterator = %s", before_right)

        for after, before_l, before_r in itertools.product(afters,
                                                           itertools.product(*before_left),
                                                           itertools.product(*before_right)):
            left = ''.join(before_l)
            right = ''.join(before_r)
            list_before_r = list(before_r)
            left_right = (left, right)
            a = after.format(*(list(before_l) + list_before_r))
            # The below is just too much logging - should be silenced in production:
            # self.logger.debug("Final rule = %s -> %s", left_right, a)
            yield (left_right, a)

    def add_rules_from_file(self, path):
        """
        Add sandhi rules from file.
        Each line of the input file should contain one rule. E.g. अ + अ = आ
        Lines starting with a # are treated as comments and skipped.
        Empty lines are ignored as well.

        :param path: file to read rules from

        See also add_rules_from_dir
        """
        filename = os.path.basename(path)
        with codecs.open(path, "rb", 'utf-8') as f:
            for linenum, line in enumerate(f):
                line = line.strip()
                if line.startswith('#') or line == '':
                    continue
                self.logger.debug("Processing rule %s", line)
                rule = SanskritImmutableString(line).canonical()
                for r in self.expand_rule(rule):
                    self.add_rule(*r, annotation="%s:%d" % (filename[0], linenum+1))

    def add_rules_from_dir(self, directory):
        """
        Add sandhi rules from an entire directory.
        Reads all .txt files from the given directory and adds rules from them


        :param directory: path to directory with rules files

        See also add_rules_from_file
        """
        self.logger.debug("Adding rules from directory %s", directory)
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                self.logger.debug("Processing rules from file %s", filename)
                self.add_rules_from_file(os.path.join(directory, filename))
            else:
                continue

    def save_rules(self, output_path):
        assert self.lc_len_max < 255 and self.rc_len_max < 255
        self.forward.append(("__lc_len_max__", self.lc_len_max.to_bytes(1, "big")))
        self.forward.append(("__rc_len_max__", self.rc_len_max.to_bytes(1, "big")))
        zip_path = os.path.join(output_path, 'sandhi_rules.zip')
        with ZipFile(zip_path, mode='w', compression=ZIP_DEFLATED) as myzip:
            with myzip.open('sandhi_forward.marisa', mode='w') as f:
                trie = BytesTrie(self.forward)
                f.write(trie.tobytes())
            with myzip.open('sandhi_backward.marisa', mode='w') as f:
                trie = BytesTrie(self.backward)
                f.write(trie.tobytes())


if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.dirname(__file__))
    output_path = os.path.join(root_dir, 'sanskrit_parser', 'data')
    print(f'Saving sandhi rules to {output_path}')

    s = Sandhi()
    s.save_rules(output_path)
