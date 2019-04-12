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
import requests
import os
import shutil
import inspect
from lxml import etree
from collections import defaultdict
from io import BytesIO
import logging
import time
import datetime
from sanskrit_parser.base.sanskrit_base import SanskritObject, SCHEMES
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
    base_url = "https://github.com/kmadathil/sanskrit_parser/raw/karthik/data/"
    xml_files = ["roots", "nouns", "adverbs", "final", "parts", "pronouns", "upasargas", "all"]
    old_base_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    folder = "data"
    old_dir = os.path.join(old_base_dir, folder)

    def __init__(self, files_list=['all'], logger=None):
        for f in files_list:
            if f not in self.xml_files:
                raise Exception(f + "is not a valid file name")
        self.files = files_list
        self.files.sort()
        self.pickle_file = "_".join(self.files) + ".pickle"
        if ["all"] == self.files:
            self.files = self.xml_files[:-1]
            self.pickle_file = "_all.pickle"
        self.logger = logger or logging.getLogger(__name__)
        self._relocate_data()
        self._load_forms()

    @staticmethod
    def _relocate_data():
        if os.path.exists(InriaXMLWrapper.old_dir):
            shutil.move(InriaXMLWrapper.old_dir, InriaXMLWrapper.base_dir)

    def _get_files(self):
        """ Download files if not present in cache """
        if not os.path.exists(self.base_dir):
            self.logger.debug("Data cache not found. Creating.")
            os.makedirs(self.base_dir)
        for f in self.files:
            filename = "SL_" + f + ".xml"
            if not os.path.exists(os.path.join(self.base_dir, filename)):
                self.logger.debug("%s not found. Downloading it", filename)
                r = requests.get(self.base_url + filename, stream=True)
                with open(os.path.join(self.base_dir, filename), "wb") as fd:
                    for chunk in r.iter_content(chunk_size=128):
                        fd.write(chunk)

    def _generate_dict(self):
        """ Create dict with mapping
            form : set([<tag 1>, ... , <tag n>])
            and pickle it
        """
        self._get_files()
        self.logger.debug("Parsing files into dict for faster lookup")
        self.forms = defaultdict(list)
        for f in self.files:
            filename = "SL_" + f + ".xml"
            self.logger.debug("Parsing %s", filename)
            tree = etree.parse(os.path.join(self.base_dir, filename))
            for elem in tree.iterfind('f'):
                form = elem.get('form')
                self.forms[form].append(etree.tostring(elem).strip())
        self.logger.debug("Pickling forms database for faster loads")
        with open(os.path.join(self.base_dir, self.pickle_file), "wb") as fd:
            pickle.dump(self.forms, fd, pickle.HIGHEST_PROTOCOL)

    def _load_forms(self):
        """ Load/create dict of tags for forms """
        pickle_path = os.path.join(self.base_dir, self.pickle_file)
        if os.path.exists(pickle_path):
            self.logger.info("Pickle file found, loading at %s", datetime.datetime.now())
            start = time.time()
            with open(pickle_path, "rb") as fd:
                self.forms = pickle.load(fd)
            self.logger.info("Loading finished at %s, took %f s",
                             datetime.datetime.now(),
                             time.time() - start
                             )
        else:
            self.logger.debug("Pickle file not found, creating ...")
            self._generate_dict()
        self.logger.info("Cached %d forms for fast lookup", len(self.forms))

    def _xml_to_tags(self, word):
        # FIXME - This is currently from sanskritmark. Check if this can be simplified
        if word in self.forms:
            tags = self.forms[word]
            results = []
            for tag in tags:
                root = etree.parse(BytesIO(tag)).getroot()
                # The next two steps require explanation. In Gerard's XML files,
                # All possible attributes are given as children of 'f'. The last
                # child is always 's' which stores the stem. All other children
                # are the various possible word attributes. Given as 'na' or 'v'
                # etc. Gio
                children = root.getchildren()[:-1]  # attributes
                baseword = root.getchildren()[-1].get('stem').strip()  # 's' stem
                attributes = []
                for child in children:
                    taglist = child.xpath(
                        './/*')  # Fetches all elements (abbreviations) of a particular verb / word characteristics.
                    output = [child.tag]  # The first member of output list is the tag of element 'v', 'na' etc.
                    output = output + [tagitem.tag for tagitem in
                                       taglist]  # Other tags (abbreviations) and add it to output list.
                    attributes.append(output)
                for attrib in attributes:
                    results.append((baseword, set(attrib)))
            return results
        else:
            return None

    def valid(self, word):
        return word in self.forms

    def get_tags(self, word, tmap=True):
            tags = self._xml_to_tags(word)
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

        word_in = SanskritObject(args.word, encoding=ie).canonical()
        xmlDB = InriaXMLWrapper()
        print("Getting tags for", word_in)
        tags = xmlDB.get_tags(word_in)
        if tags is not None:
            map(print, tags)

    main()
