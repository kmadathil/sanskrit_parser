# -*- coding: utf-8 -*-
"""
Sandhi splitter for Samskrit.
Builds up a database of sandhi rules and utilizes them for both
performing sandhi and splitting words.

Will generate splits that may not all be valid words. That is left to the
calling module to validate. See for example SanskritLexicalAnalyzer

Example usage:
    from sandhi import Sandhi
    sandhi = Sandhi()
    joins = sandhi.join('tasmin', 'iti')
    splits = sandhi.split_at('tasminniti', 5)

If running script directly from console, please ensure that your console
supports unicode display. See for example
https://stackoverflow.com/questions/10651975/unicode-utf-8-with-git-bash
    
Draws inspiration from by https://github.com/sanskrit/sanskrit

@author: Avinash Varna (github: @avinashvarna)
"""

from collections import defaultdict
import itertools
import codecs
import os
import re
import inspect
import logging
import datetime
from base.SanskritBase import SanskritObject, DEVANAGARI, SLP1, SCHEMES

class Sandhi(object):
    """
    Class to hold all the sandhi rules and methods for joining and splitting.
    Uses SLP1 encoding for all internal operations.
    """
    
    def __init__(self, rules_dir = None, use_default_rules = True, logger = None):
        """
        Sandhi class constructor
        
        :param rules_dir: directory to read rules from
        :param use_default_rules: reads pre-built-rules from sandhi_rules dir under module directory
        :param logger: instance of python logger to use
        """
        self.forward = defaultdict(set)
        self.backward = defaultdict(set)
        self.lc_len_max = 0
        self.rc_len_max = 0
        self.logger = logger or logging.getLogger(__name__)
        if rules_dir:
            self.add_rules_from_dir(rules_dir)
        if use_default_rules:
            base_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            self.add_rules_from_dir(os.path.join(base_dir,"sandhi_rules"))
        
    def add_rule(self, before, after):
        """
        Adds a single sandhi rule to the rule database
        
        :param before: tuple of length two of the varNas involved in the sandhi
        :param after: result of the sandhi
        """
        self.forward[before].add(after)
        self.backward[after].add(before)
        self.lc_len_max = max(self.lc_len_max, len(before[0]))
        self.rc_len_max = max(self.rc_len_max, len(before[1]))
    
    def join(self, first_in, second_in):
        """
        Performs sandhi.
        **Warning**: May generate forms that are not lexically valid.
        
        :param first_in: SanskritObject first word of the sandhi
        :param second_in: SanskritObject word of the sandhi
        :return: list of strings of possible sandhi forms, or None if no sandhi can be performed 
        
        """
        first = first_in.transcoded(SLP1)
        second = second_in.transcoded(SLP1)
        self.logger.debug("Join: %s, %s", first, second)
        if first is None or len(first) == 0:
            return second
        # FIXME Will we need to change this to handle mo'nusvAraH and similar forms?
        if second is None or len(second) == 0:
            return first
        left_chars = [first[i:] for i in range(max(0, len(first)-self.lc_len_max), len(first))]
        right_chars = [second[0:i] for i in range(min(self.rc_len_max, len(second))+1)]
        self.logger.debug("left_chars = %s, right_chars %s", left_chars, right_chars)
        
        joins = []
        for key in itertools.product(left_chars, right_chars):
            afters = self.forward.get(key)
            if afters:
                for after in afters:
                    self.logger.debug("key (before) = %s, value (after) = %s", key, after)
                    joins.append(first[:-len(key[0])] + after + second[len(key[1]):])
        if len(joins) == 0:
            self.logger.debug("No joins found")
            return None
        else:
            return joins
            
    def split_at(self, word_in, idx):
        """
        Split sandhi at the given index of word.
        **Warning**: Will generate splits that are not lexically valid.
        
        :param word_in: SanskritObject word to split
        :param idx: position within word at which to try the split
        :return: list of list of strings of possible split forms, or None if no split can be performed 
        
        """
        word = word_in.transcoded(SLP1)
        self.logger.debug("Split: %s, %d", word, idx)
        left_chars = [word[i:idx+1] for i in range(max(0, idx-self.lc_len_max), idx+1)]
        right_chars = [word[idx+1:idx+i] for i in range(1, min(self.rc_len_max, len(word)-idx)+1)]
        self.logger.debug("left_chars = %s, right_chars %s", left_chars, right_chars)
        splits = []
        for after in itertools.product(left_chars, right_chars):
            key = ''.join(after)
            self.logger.debug("Trying key %s", key)
            befores = self.backward[key]
            if befores:
                for before in befores:
                    self.logger.debug("Found split %s -> %s", key, before)
                    splits.append([ word[:idx+1-len(after[0])] + before[0], before[1] + word[idx+1+len(after[1]):] ])
        if len(splits) == 0:
            self.logger.debug("No split found")
            return None
        else:
            return splits
            
    def expand_rule(self, rule):
        """
        Expands a given sandhi rule from the rules file to generate all possible combinations
        
        :param rule: Rule to expand
        :return: A generator of all possible expanded rules
        """
        self.logger.debug("Expanding rule %s", rule)
        
        b, afters = map(unicode.strip, rule.split("="))
        before = map(unicode.strip, b.split("+"))
        left_classes = re.split('\[(.*?)\]', before[0])
        self.logger.debug("Left classes = %s", left_classes)
        
        # Split after forms into individual forms
        afters = map(unicode.strip, afters.split("/"))
        
        # Could have used list comprehension, but this is easier to read
        before_left = []
        for c in left_classes:
            if c != '':
                before_left.append(map(unicode.strip, c.split(",")))
        self.logger.debug("before_left iterator = %s", before_left)
        
        
        right_class = re.match('\[(.*)\]', before[1])
        # Could have used list comprehension, but this is easier to read
        if right_class:
            before_right = (map(unicode.strip, right_class.group(1).split(",")))
        else:
            before_right = [before[1].strip()]
        self.logger.debug("before_right iterator = %s", before_right)
        
        for after, before_l, right in itertools.product(afters, itertools.product(*before_left), before_right):
            left = ''.join(before_l)
            left_right = (left, right)        
            a = after.format(*(list(before_l) + [right]))
            self.logger.debug("Final rule = %s -> %s", left_right, a)
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
        with codecs.open(path, "rb", 'utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or line == '':
                    continue
                self.logger.debug("Processing rule %s", line)
                rule = SanskritObject(line).transcoded(SLP1)
                for r in self.expand_rule(rule):
                    self.add_rule(*r)
                
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

if __name__ == "__main__":
    from argparse import ArgumentParser
    def getArgs():
        """
          Argparse routine. 
          Returns args variable
        """
        # Parser Setup
        parser = ArgumentParser(description='Sandhi Utility')
        # Input Encoding (autodetect by default)
        parser.add_argument('--input-encoding', type=str, default=None)
        # Filter by tag set
        parser.add_argument('--split', action='store_true')
        parser.add_argument('--pos', type=int, default=5)
        parser.add_argument('--join', action='store_true')
        parser.add_argument('--loglevel', type=str, default="INFO")
        # String to encode
        parser.add_argument('word1', nargs="?", type=str, default="tasminniti")
        parser.add_argument('word2', nargs="?", type=str, default="eva")

        return parser.parse_args()

    def main():
        args=getArgs()
        if args.input_encoding is None:
            ie = None
        else:
            ie = SCHEMES[args.input_encoding]
        
        # Setup logging
        numeric_level = getattr(logging, args.loglevel.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % args.loglevel)
        logging.basicConfig(filename="sandhi.log", filemode = "wb", level = numeric_level)
        logging.info("---------------------------------------------------")
        logging.info("Started processing at %s", datetime.datetime.now())
        
        sandhi = Sandhi()
        # if neither split nor join is chosen, just demo both
        if not args.split and not args.join:
            print "Neither split nor join option chosen. Here's a demo of both"
            args.split = True
            args.join = True
        if args.split:
            print "Splitting %s at %d" % (args.word1, args.pos)
            word_in = SanskritObject(args.word1, encoding=ie)
            splits = sandhi.split_at(word_in, args.pos)
            print splits
        if args.join:
            print "Joining", args.word1, args.word2
            first_in = SanskritObject(args.word1, encoding=ie)
            second_in = SanskritObject(args.word2, encoding=ie)
            joins = sandhi.join(first_in, second_in)
            print joins
        
        logging.info("Finished processing at %s", datetime.datetime.now())
        logging.info("---------------------------------------------------")
        logging.shutdown()

    main()
