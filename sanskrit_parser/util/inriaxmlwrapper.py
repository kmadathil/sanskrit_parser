# -*- coding: utf-8 -*-

"""
Intro
=====
Provide interface with the INRIA XML database released
by Prof. Gerard Huet
https://gitlab.inria.fr/huet/Heritage_Resources
(Thanks Prof. Huet for making the data available!)

Inspired by https://github.com/drdhaval2785/inriaxmlwrapper
(Thanks @drdhaval2785!)

@author: Avinash Varna (@avinashvarna)

Usage
=====
The InriaXMLWrapper utility class can also be used to lookup tags:

.. code:: python

    >>> from sanskrit_parser.util.inriaxmlwrapper import InriaXMLWrapper
    >>> db = InriaXMLWrapper()
    >>> db_tags = db.get_tags('hares')
    >>> tags == db_tags
    True


Command line usage
==================

::

    $ python -m sanskrit_parser.util.inriaxmlwrapper hares
    INFO:root:Pickle file found, loading at 2017-07-31 14:35:56.093000
    INFO:root:Loading finished at 2017-07-31 14:35:59.159000, took 3.066000 s
    INFO:root:Cached 666994 forms for fast lookup
    Getting tags for hares
    ('hf#1', set(['cj', 'snd', 'prim', 'para', 'md', 'sys', 'prs', 'v', 'np', 'sg', 'op']))
    ('hari#1', set(['na', 'mas', 'sg', 'gen']))
    ('hari#1', set(['na', 'mas', 'abl', 'sg']))
    ('hari#1', set(['na', 'fem', 'sg', 'gen']))
    ('hari#1', set(['na', 'fem', 'abl', 'sg']))
    ('hari#2', set(['na', 'mas', 'sg', 'gen']))
    ('hari#2', set(['na', 'mas', 'abl', 'sg']))
    ('hari#2', set(['na', 'fem', 'sg', 'gen']))
    ('hari#2', set(['na', 'fem', 'abl', 'sg']))

"""

from __future__ import print_function
import os
import logging
import importlib.resources

from sanskrit_parser.base.sanskrit_base import SanskritImmutableString, SCHEMES
from sanskrit_parser.util.lexical_lookup import LexicalLookup
from sanskrit_parser.util.inriatagmapper import inriaTagMapper

try:
    import cPickle as pickle
except ImportError:
    import pickle


class InriaXMLWrapper(LexicalLookup):
    """
    Class to interface with the INRIA XML database released
    by Prof. Gerard Huet
    https://gitlab.inria.fr/huet/Heritage_Resources
    """

    def __init__(self, logger=None):
        self.pickle_file = "inria_forms.pickle"
        self.logger = logger or logging.getLogger(__name__)
        self._load_forms()

    def _load_forms(self):
        """ Load/create dict of tags for forms """
        with importlib.resources.path('sanskrit_parser', 'data') as base_dir:
            pickle_path = os.path.join(base_dir, self.pickle_file)
            with open(pickle_path, "rb") as fd:
                self.forms = pickle.load(fd)
                self.index = pickle.load(fd)

    def _decode_tags(self, tag_index):
        tags = [self.index[x] for x in tag_index]
        return (tags[0], set(tags[1:]))

    def _get_tags(self, word):
        if word in self.forms:
            tag_index_list = self.forms[word]
            tags = []
            for tag_index in tag_index_list:
                tags.append(self._decode_tags(tag_index))
            return tags
        else:
            return None

    def valid(self, word):
        return word in self.forms

    def get_tags(self, word, tmap=True):
        tags = self._get_tags(word)
        if tmap and (tags is not None):
            tags = inriaTagMapper(tags)
        return tags


if __name__ == "__main__":
    from argparse import ArgumentParser

    def getArgs():
        """
          Argparse routine.
          Returns args variable
        """
        # Parser Setup
        parser = ArgumentParser(description='Interface to INRIA XML database')
        # Input Encoding (autodetect by default)
        parser.add_argument('--input-encoding', type=str, default=None)
        parser.add_argument('--loglevel', type=str, default="info",
                            help="logging level. Can be any level supported by logging module")

        parser.add_argument('word', nargs='?', type=str,
                            default=None,
                            help="Word to look up")
        parser.add_argument('--no-map-tags', dest='map_tags',
                            action='store_false')
        return parser.parse_args()

    def main():
        args = getArgs()
        if args.input_encoding is None:
            ie = None
        else:
            ie = SCHEMES[args.input_encoding]

        if args.loglevel:
            numeric_level = getattr(logging, args.loglevel.upper(), None)
            if not isinstance(numeric_level, int):
                raise ValueError('Invalid log level: %s' % args.loglevel)
            logging.basicConfig(level=numeric_level)

        word_in = SanskritImmutableString(args.word, encoding=ie).canonical()
        xmlDB = InriaXMLWrapper()
        print("Getting tags for", word_in)
        tags = xmlDB.get_tags(word_in, tmap=args.map_tags)
        if tags is not None:
            for t in tags:
                print(t)

    main()
