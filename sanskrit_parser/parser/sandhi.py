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

    >>> from sanskrit_parser.parser.sandhi import Sandhi
    >>> sandhi = Sandhi()
    >>> word1 = SanskritImmutableString('te')
    >>> word2 = SanskritImmutableString('eva')
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

    >>> w = SanskritImmutableString('taeva')
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

    $ python -m sanskrit_parser.parser.sandhi --join te eva
    Joining te eva
    set([u'teeva', u'taeva', u'ta eva', u'tayeva'])

    $ python -m sanskrit_parser.parser.sandhi --split taeva 1
    Splitting taeva at 1
    set([(u'tar', u'eva'), (u'tas', u'eva'), (u'taH', u'eva'), (u'ta', u'eva')])

    $ python -m sanskrit_parser.parser.sandhi --split taeva --all
    All possible splits for taeva
    set([(u't', u'aeva'), (u'tar', u'eva'), (u'taev', u'a'), (u'to', u'eva'),
    (u'ta', u'eva'), (u'te', u'eva'), (u'taH', u'eva'), (u'tae', u'va'),
    (u'taeva', u''), (u'tas', u'eva')])



"""

import itertools
import pickle
import logging
import datetime
from zipfile import ZipFile
from sanskrit_parser.base.sanskrit_base import SanskritNormalizedString, SCHEMES, outputctx
from sanskrit_parser.util.data_manager import data_file_path


class Sandhi(object):
    """
    Class to hold all the sandhi rules and methods for joining and splitting.
    Uses SLP1 encoding for all internal operations.
    """

    def __init__(self, rules_dir=None, use_default_rules=True, logger=None):
        """
        Sandhi class constructor

        :param rules_dir: directory to read rules from
        :param use_default_rules: reads pre-built-rules from sandhi_rules dir under module directory
        :param logger: instance of python logger to use
        """
        self.forward = None
        self.backward = None
        self.logger = logger or logging.getLogger(__name__)

    @staticmethod
    def _load_rules_pickle(filename):
        zip_path = data_file_path('sandhi_rules.zip')
        with ZipFile(zip_path) as myzip:
            with myzip.open(filename) as f:
                return pickle.load(f)

    def _load_forward(self):
        if self.forward is None:
            self.forward = self._load_rules_pickle('sandhi_forward.pkl')
            keys = self.forward.keys()
            self.lc_len_max = max(len(k[0]) for k in keys)
            self.rc_len_max = max(len(k[1]) for k in keys)

    def _load_backward(self):
        if self.backward is None:
            self.backward = self._load_rules_pickle('sandhi_backward.pkl')
            keys = self.backward.keys()
            self.after_len_max = max(len(k) for k in keys)

    def join(self, first_in, second_in):
        """
        Performs sandhi.
        **Warning**: May generate forms that are not lexically valid.

        :param first_in: SanskritImmutableString first word of the sandhi
        :param second_in: SanskritImmutableString word of the sandhi
        :return: list of strings of possible sandhi forms, or None if no sandhi can be performed
        """
        self._load_forward()
        first = first_in.canonical()
        second = second_in.canonical()
        self.logger.debug("Join: {}, {}".format(first, second))
        if first is None or len(first) == 0:
            return second
        if second is None:
            return first
        left_chars = [first[i:] for i in range(max(0, len(first)-self.lc_len_max), len(first))]
        left_chars.append("^"+first)
        right_chars = [second[0:i] for i in range(min(self.rc_len_max, len(second))+1)]
        self.logger.debug("left_chars = %s, right_chars %s", left_chars, right_chars)
        joins = set()
        for key in itertools.product(left_chars, right_chars):
            afters = self.forward.get(key)
            if afters:
                for after, annotation in afters:
                    self.logger.debug("Found sandhi %s = %s (%s)", key, after, annotation)
                    joins.add(first[:-len(key[0])] + after + second[len(key[1]):])
        if len(joins) == 0:
            self.logger.debug("No joins found")
            return None
        else:
            return joins

    def split_at(self, word_in, idx):
        """
        Split sandhi at the given index of word.
        **Warning**: Will generate splits that are not lexically valid.

        :param word_in: SanskritImmutableString word to split
        :param idx: position within word at which to try the split
        :return: set of tuple of strings of possible split forms, or None if no split can be performed
        """
        self._load_backward()
        word = word_in.canonical()
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
                    # Do we have a beginning-of-line match rule
                    if before[0][0] == "^":
                        if idx != 0:
                            # Can't allow matches at any other position
                            continue
                        else:
                            # drop the ^ in the result
                            before = (before[0][1:], before[1])
                    left = word[:idx] + before[0]
                    right = before[1] + word[idx+len(after):]
                    splits.add((left, right))

        if len(splits) == 0:
            self.logger.debug("No split found")
            return None
        else:
            return splits

    def split_all(self, word_in, start=None, stop=None):
        """
        Split word at all possible locations and return splits.
        **Warning**: Will generate splits that are not lexically valid.

        :param word_in: SanskritImmutableString word to split
        :return: set of tuple of strings of possible split forms, or None if no split can be performed
        """
        splits = set()
        word = word_in.canonical()
        start = start or 0
        stop = stop or len(word)
        for idx in range(start, stop):
            split = self.split_at(word_in, idx)
            if split:
                splits |= split
        if len(splits) == 0:
            self.logger.debug("No split found")
            return None
        else:
            return splits


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
        parser.add_argument('word', nargs='?', type=str,
                            default="tasminniti",
                            help="First word of sandhi if join, or word to split")
        parser.add_argument('word_or_pos', nargs="?", type=str,
                            default="eva",
                            help="Second word of sandhi if join, or position to split")

        return parser.parse_args()

    def main():
        args = getArgs()
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
                word_in = SanskritNormalizedString(args.word, encoding=ie, strict_io=args.strict_io)
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
                first_in = SanskritNormalizedString(args.word, encoding=ie, strict_io=args.strict_io)
                second_in = SanskritNormalizedString(args.word_or_pos, encoding=ie, strict_io=args.strict_io)
                joins = sandhi.join(first_in, second_in)
                print(joins)

        logging.info("Finished processing at %s", datetime.datetime.now())
        logging.info("---------------------------------------------------")
        logging.shutdown()

    main()
