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
from indic_transliteration import sanscript

# TODO Integrate with the SanskritObject class


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
    
    def join(self, first, second):
        """
        Performs sandhi.
        **Warning**: May generate forms that are not lexically valid.
        
        :param first: SLP1 encoded first word of the sandhi
        :param second: SLP1 encoded first word of the sandhi
        :return: list of strings of possible sandhi forms, or None if no sandhi can be performed 
        
        """
        self.logger.debug("Join: %s, %s", first, second)
        if first is None or len(first) == 0:
            return second
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
            
    def split_at(self, word, idx):
        """
        Split sandhi at the given index of word.
        **Warning**: Will generate splits that are not lexically valid.
        
        :param word: SLP1 encoded word to split
        :param idx: position within word at which to try the split
        :return: list of list of strings of possible split forms, or None if no split can be performed 
        
        """
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
                    self.logger.debug("Found split %s -> %s", before, key)
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
        for after in map(unicode.strip, afters.split("/")):
            self.logger.debug("found after form %s", after)
            for before_l in itertools.product(*before_left):
                left = ''.join(before_l)
                for right in before_right:
                    left_right = (left, right)        
                    a = after.format(*(list(before_l) + [right]))
                    self.logger.debug("Final rule = %s -> %s", left_right, a)
                    yield (left_right, a)

    def add_rules_from_file(self, path):
        """
        Add sandhi rules from file.
        Rules in the sandhi file are written in devanagari (for who would 
        honestly WANT to read and write SLP1)
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
                rule = sanscript.transliterate(line, sanscript.DEVANAGARI, sanscript.SLP1)
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
    # ---------------------------------------------------------------
    # some sample test cases to show usage
    # TODO move to pytest framwork with more extensive testing
    # ---------------------------------------------------------------
    def print_list(li):
        if li:
            for l in li:
                if type(l) == list:
                    l = ' '.join(l)
                e = sanscript.transliterate(l, sanscript.SLP1, sanscript.DEVANAGARI)
                print "\t", e, "(SLP1:", l, ")"
        else:
            print "\t None"
            
    def test_join(first, second):
        first_e = sanscript.transliterate(first, sanscript.DEVANAGARI, sanscript.SLP1)
        second_e = sanscript.transliterate(second, sanscript.DEVANAGARI, sanscript.SLP1)
        print first, u"+", second, u"= (SLP1:", first_e, "+", second_e, ")"
        joins = sandhi.join(first_e, second_e)
        print_list(joins)
        
    def test_split(word, pos):
        print "split %s @ %d" % (word, pos)
        splits = sandhi.split_at(sanscript.transliterate(word, sanscript.DEVANAGARI, sanscript.SLP1), pos)
        print_list(splits)
            
    def test():
        print "-----------"
        print "Test joins:"
        print "-----------"
        test_join(u"ते", u"एव")
        test_join(u"तस्मिन्", u"इति")
        test_join(u"अक्ष", u"ऊहिन्याम्")
        test_join(u"सुख", u"ऋतेभ्यः")
        
        print "------------"
        print "Test splits:"
        print "------------"
        test_split(u"तस्मिन्निति", 5)
        test_split(u"दीर्घायुः", 4)
        test_split(u"त एव", 2)
        test_split(u"अक्षौहिण्यः", 3)
        test_split(u"सुखार्तैः", 3)

    if 'PYTHONIOENCODING' not in os.environ or os.environ['PYTHONIOENCODING'] != 'UTF-8':
        print "*******"
        print "WARNING: PYTHONIOENCODING environment variable not detected or not 'UTF-8'"
        print "If you see an error about not being able to decode a unicode character"
        print "please set the PYTHONIOENCODING environment variable to 'UTF-8'"
        print "*******"
    logging.basicConfig(filename="sandhi.log", filemode = "wb", level=logging.DEBUG)
    logging.info("---------------------------------------------------")
    logging.info("Started processing at %s", datetime.datetime.now())
    
    sandhi = Sandhi()
    test()
      
    logging.info("Finished processing at %s", datetime.datetime.now())
    logging.info("---------------------------------------------------")
    logging.shutdown()
    
    