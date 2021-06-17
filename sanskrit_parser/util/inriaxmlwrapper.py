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

import pickle
import sqlite3
import logging
from collections import namedtuple

from sanskrit_parser.base.sanskrit_base import SanskritImmutableString, SCHEMES
from sanskrit_parser.util.lexical_lookup import LexicalLookup
from sanskrit_parser.util.inriatagmapper import inriaTagMapper
from sanskrit_parser.util.data_manager import data_file_path

_db = namedtuple('_db', ['db_file', 'tags', 'stems', 'buf'])


class InriaXMLWrapper(LexicalLookup):
    """
    Class to interface with the INRIA XML database released
    by Prof. Gerard Huet
    https://gitlab.inria.fr/huet/Heritage_Resources
    """

    '''
    The custom database format has two parts:
        1. A pickle file that contains a list of stems,
           a list of tags, and a serialized buffer of the
           indices of stems and tags for each form. The indices
           are used as it is more efficient to store such integers
           instead of the string for each tag.
        2. An sqlite file that maps each form to the position
           within the buffer that contains the serialized tuple
           of stems and tags for that form. An sqlite database
           is used to avoid having to build a huge dict in
           memory for the 600K forms that are present in this db,
           which consumes a lot of memory. (See
           https://github.com/kmadathil/sanskrit_parser/issues/151)

    To lookup the tag for a form, we use the sqlite db to find the
    position in the buffer, deserialize the data at that position,
    which gives us a list of the tag set for that form. For each
    item in that list, we then lookup the right stem and tag in
    the list of stems and tags loaded from the pickle file
    '''

    def __init__(self, logger=None):
        self.pickle_file = "inria_forms.pickle"
        self.logger = logger or logging.getLogger(__name__)
        db_file = data_file_path("inria_forms_pos.db")
        pkl_path = data_file_path("inria_stems_tags_buf.pkl")
        self.db = self._load_db(db_file, pkl_path)

    @staticmethod
    def _load_db(db_file, pkl_path):
        with open(pkl_path, 'rb') as f:
            stems = pickle.load(f)
            tags = pickle.load(f)
            buf = f.read()
        db = _db(db_file, tags, stems, buf)
        return db

    def _get_tags(self, word):
        db = self.db
        conn = sqlite3.connect(db.db_file)
        cursor = conn.cursor()
        res = cursor.execute('SELECT * FROM forms WHERE form=?', (word,)).fetchone()
        if res is None:
            return None
        pos = res[1]
        tag_index_list = pickle.loads(db.buf[pos:])
        tags = []
        for tag_index in tag_index_list:
            tags.append(self._decode_tags(tag_index, db.tags, db.stems))
        return tags

    @staticmethod
    def _decode_tags(tag_index, tags, stems):
        t = [tags[x] for x in tag_index[1]]
        stem = stems[tag_index[0]]
        return (stem, set(t))

    def valid(self, word):
        conn = sqlite3.connect(self.db.db_file)
        cursor = conn.cursor()
        res = cursor.execute('SELECT COUNT(1) FROM forms WHERE form = ?', (word,)).fetchone()
        return res[0] > 0

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
