# -*- coding: utf-8 -*-
"""
Intro
=====
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

Draws inspiration from https://github.com/sanskrit/sanskrit

@author: Avinash Varna (github: @avinashvarna)

Usage
=====
The ``Sandhi`` class can be used to join/split words:

.. code:: python

    >>> from sanskrit_parser.lexical_analyzer.sandhi import Sandhi
    >>> sandhi = Sandhi()
    >>> word1 = SanskritObject('te')
    >>> word2 = SanskritObject('eva')
    >>> joins = sandhi.join(word1, word2)
    >>> for join in joins:
    ...    print(join)
    ...
    teeva
    taeva
    ta eva
    tayeva

To split at a specific position, use the ``Sandhi.split_at()`` method:

.. code:: python

    >>> w = SanskritObject('taeva')
    >>> splits = sandhi.split_at(w, 1)
    >>> for split in splits:
    ...    print(split)
    ...
    (u'tar', u'eva')
    (u'tas', u'eva')
    (u'taH', u'eva')
    (u'ta', u'eva')

To split at all possible locations, use the ``Sandhi.split_all()``
method:

.. code:: python

    >>> splits_all = sandhi.split_all(w)
    >>> for split in splits_all:
    ...    print(split)
    ...
    (u't', u'aeva')
    (u'tar', u'eva')
    (u'taev', u'a')
    (u'to', u'eva')
    (u'ta', u'eva')
    (u'te', u'eva')
    (u'taH', u'eva')
    (u'tae', u'va')
    (u'taeva', u'')
    (u'tas', u'eva')

**Note**: As mentioned previously, both over-generation and
under-generation are possible with the ``Sandhi`` class.


Command line usage
==================

::

    $ python -m sanskrit_parser.lexical_analyzer.sandhi --join te eva
    Joining te eva
    set([u'teeva', u'taeva', u'ta eva', u'tayeva'])

    $ python -m sanskrit_parser.lexical_analyzer.sandhi --split taeva 1
    Splitting taeva at 1
    set([(u'tar', u'eva'), (u'tas', u'eva'), (u'taH', u'eva'), (u'ta', u'eva')])

    $ python -m sanskrit_parser.lexical_analyzer.sandhi --split taeva --all
    All possible splits for taeva
    set([(u't', u'aeva'), (u'tar', u'eva'), (u'taev', u'a'), (u'to', u'eva'), (u'ta', u'eva'), (u'te', u'eva'), (u'taH', u'eva'), (u'tae', u'va'), (u'taeva', u''), (u'tas', u'eva')])



"""

from __future__ import print_function
from collections import defaultdict
import itertools
import codecs
import os
import re
import inspect
import logging
import datetime
import six
from sanskrit_parser.base.sanskrit_base import SanskritObject, SLP1, SCHEMES, outputctx
from sanskrit_parser.base.maheshvara_sutra import MaheshvaraSutras

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
        self.after_len_max = 0
        self.logger = logger or logging.getLogger(__name__)
        if rules_dir:
            self.add_rules_from_dir(rules_dir)
        if use_default_rules:
            base_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            self.add_rules_from_dir(os.path.join(base_dir,"sandhi_rules"))
        
    def add_rule(self, before, after, annotation = None):
        """
        Adds a single sandhi rule to the rule database
        
        :param before: tuple of length two of the varNas involved in the sandhi
        :param after: result of the sandhi
        """
        self.forward[before].add((after, annotation))
        self.backward[after].add((before, annotation))
        if len(before[0]) > self.lc_len_max:
            self.logger.debug("Setting lc_len_max to %d", len(before[0]))
        if len(before[1]) > self.rc_len_max:
            self.logger.debug("Setting rc_len_max to %d", len(before[1]))
        if len(after) > self.after_len_max:
            self.logger.debug("Setting after_len_max to %d", len(after))
        self.lc_len_max = max(self.lc_len_max, len(before[0]))
        self.rc_len_max = max(self.rc_len_max, len(before[1]))
        self.after_len_max = max(self.after_len_max, len(after))
    
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
        if second is None:
            return first
        left_chars = [first[i:] for i in range(max(0, len(first)-self.lc_len_max), len(first))]
        right_chars = [second[0:i] for i in range(min(self.rc_len_max, len(second))+1)]
        self.logger.debug("left_chars = %s, right_chars %s", left_chars, right_chars)
        
        joins = set()
        for key in itertools.product(left_chars, right_chars):
            afters = self.forward.get(key)
            if afters:
                for after, annotation in afters:
                    self.logger.debug("Found sandhi %s = %s (%s)", key, after, annotation)
                    joins.add(first[:-len(key[0])] + after+ second[len(key[1]):])
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
        :return: set of tuple of strings of possible split forms, or None if no split can be performed 
        
        """
        word = word_in.transcoded(SLP1)
        self.logger.debug("Split: %s, %d", word, idx)
        splits = set()
        # Figure out how may chars we can extract for the afters
        stop = min(idx+self.after_len_max, len(word))
        afters = [word[idx:i] for i in range(idx+1, stop+1)]
        for after in afters:
            self.logger.debug("Trying after %s", after)
            befores = self.backward[after]
            if befores:
                for before, annotation in befores:
                    self.logger.debug("Found split %s -> %s (%s)", after, before, annotation)
                    left = word[:idx] + before[0]
                    right = before[1] + word[idx+len(after):]
                    splits.add( ( left, right ) )
                
        if len(splits) == 0:
            self.logger.debug("No split found")
            return None
        else:
            return splits
        
    def split_all(self, word_in, start=None, stop=None):
        """
        Split word at all possible locations and return splits.
        **Warning**: Will generate splits that are not lexically valid.
        
        :param word_in: SanskritObject word to split
        :return: set of tuple of strings of possible split forms, or None if no split can be performed 
        
        """
        splits = set()
        word = word_in.transcoded(SLP1)
        start = start or 0
        stop = stop or len(word)
        for idx in six.moves.range(start, stop):
            split = self.split_at(word_in, idx)
            if split:
                splits |= split
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
        
        ms = MaheshvaraSutras()
        
        b, afters = map(six.text_type.strip, rule.split("="))
        before = list(map(six.text_type.strip, b.split("+", 1)))
        left_classes = re.split('\[(.*?)\]', before[0])
        self.logger.debug("Left classes = %s", left_classes)
        
        # Split after forms into individual forms
        afters = map(six.text_type.strip, afters.split("/"))
        
        before_left = []
        for c in left_classes:
            if c != '':
                if c.startswith("*"):
                    # This is a mAheswara sUtra pratyAhAra
                    splits = list(map(six.text_type.strip, c.split('-')))
                    varnas = set(ms.getPratyahara(SanskritObject(splits[0][1:], encoding=SLP1), longp=False, remove_a=True, dirghas=True).transcoded(SLP1))
                    if len(splits) == 2:
                        varnas -= set(splits[1])
                    self.logger.debug("Found pratyAhAra %s = %s", c, varnas)
                    before_left.append(varnas)
                else:
                    before_left.append(map(six.text_type.strip, c.split(",")))
        self.logger.debug("before_left iterator = %s", before_left)
        
        
        right_classes = re.split('\[(.*?)\]', before[1])
        # Could have used list comprehension, but this is easier to read
        self.logger.debug("right_classes = %s", right_classes)
        if right_classes:
            before_right = []
            for c in right_classes:
                if c != '':
                    if c.startswith("*"):
                        # This is a mAheswara sUtra pratyAhAra
                        splits = list(map(six.text_type.strip, re.split('([+-])', c)))
                        varnas = set(ms.getPratyahara(SanskritObject(splits[0][1:], encoding=SLP1), longp=False, remove_a=True, dirghas=True).transcoded(SLP1))
                        if len(splits) == 3:
                            if splits[1] == '-':
                                varnas -= set(splits[2])
                            elif splits[1] == '+':
                                varnas |= set(splits[2])
                        self.logger.debug("Found pratyAhAra %s (%s) = %s", c, splits[0][1:], varnas)
                        before_right.append(varnas)
                    else:
                        before_right.append(map(six.text_type.strip, c.split(",")))
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
                rule = SanskritObject(line).transcoded(SLP1)
                for r in self.expand_rule(rule):
                    self.add_rule(*r, annotation= "%s:%d" % (filename, linenum+1))
                
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
        parser.add_argument('--loglevel', type=str, help="logging level. Can be any level supported by logging module")
        parser.add_argument('--split', action='store_true', help="Split the given word using sandhi rules")
        parser.add_argument('--join', action='store_true', help="Join the given words using sandhi rules")
        parser.add_argument('--all', action='store_true', help="Return splits at all possible locations")
        parser.add_argument('--strict-io', action='store_true',
                            help="Do not modify the input/output string to match conventions", default=False)
        
        # String to encode
        parser.add_argument('word', nargs = '?', type=str, 
                            default="tasminniti", 
                            help="First word of sandhi if join, or word to split")
        parser.add_argument('word_or_pos', nargs="?", type=str, 
                            default="eva", 
                            help="Second word of sandhi if join, or position to split")

        return parser.parse_args()

    def main():
        args=getArgs()
        if args.input_encoding is None:
            ie = None
        else:
            ie = SCHEMES[args.input_encoding]
        
        # Setup logging
        if args.loglevel:
            numeric_level = getattr(logging, args.loglevel.upper(), None)
            if not isinstance(numeric_level, int):
                raise ValueError('Invalid log level: %s' % args.loglevel)
            logging.basicConfig(filename="sandhi.log", filemode="wb", level=numeric_level)
            
        logging.info("---------------------------------------------------")
        logging.info("Started processing at %s", datetime.datetime.now())
        
        sandhi = Sandhi()
        # if neither split nor join is chosen, just demo both
        if not args.split and not args.join:
            print("Neither split nor join option chosen. Here's a demo of joining")
            args.join = True
        with outputctx(args.strict_io):
            if args.split:
                word_in = SanskritObject(args.word, encoding=ie, strict_io=args.strict_io)
                if args.all:
                    print("All possible splits for {}".format(args.word))
                    splits = sandhi.split_all(word_in)
                else:
                    pos = int(args.word_or_pos)
                    print("Splitting {0} at {1}".format(args.word, pos))
                    splits = sandhi.split_at(word_in, pos)
                print(splits)
            if args.join:
                print("Joining {0} {1}".format(args.word, args.word_or_pos))
                first_in = SanskritObject(args.word, encoding=ie, strict_io=args.strict_io)
                second_in = SanskritObject(args.word_or_pos, encoding=ie, strict_io=args.strict_io)
                joins = sandhi.join(first_in, second_in)
                print(joins)

        logging.info("Finished processing at %s", datetime.datetime.now())
        logging.info("---------------------------------------------------")
        logging.shutdown()

    main()
