'''
Base class + factory for lexical lookup classes

@author: avinashvarna
'''

from __future__ import print_function
import abc
from argparse import ArgumentParser
from sanskrit_parser.base.sanskrit_base import SanskritImmutableString, SCHEMES


class LexicalLookup(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def valid(self, word):
        """ Return True if word is a valid pada """

    @abc.abstractmethod
    def get_tags(self, word, tmap=True):
        """ Return lexical tags of word """

    @staticmethod
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
        parser.add_argument('--no-map-tags', dest='map_tags',
                            action='store_false')

        parser.add_argument('word', nargs='?', type=str,
                            default=None,
                            help="Word to look up")

        return parser.parse_args()

    def main(self, args):
        if args.input_encoding is None:
            ie = None
        else:
            ie = SCHEMES[args.input_encoding]

        word_in = SanskritImmutableString(args.word,
                                          encoding=ie).canonical()
        print("Getting tags for", word_in)
        tags = self.get_tags(word_in, tmap=args.map_tags)
        if tags is not None:
            for tag in tags:
                print(tag)
