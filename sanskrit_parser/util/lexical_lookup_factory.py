'''
Created on Aug 4, 2017

@author: alvarna
'''

from sanskrit_parser.util.inriaxmlwrapper import InriaXMLWrapper
from sanskrit_parser.util.sanskrit_data_wrapper import SanskritDataWrapper
from sanskrit_parser.util.lexical_lookup import LexicalLookup
import logging


class CombinedWrapper(LexicalLookup):

    def __init__(self, logger=None):
        self.inria = LexicalLookupFactory.create("inria")
        self.sanskrit_data = LexicalLookupFactory.create("sanskrit_data")
        self.logger = logger or logging.getLogger(__name__)

    def valid(self, word):
        return self.inria.valid(word) or self.sanskrit_data.valid(word)

    def get_tags(self, word, tmap=True):
        tags = self.inria.get_tags(word, tmap) or []
        sanskrit_data_tags = self.sanskrit_data.get_tags(word, tmap)
        if sanskrit_data_tags is not None:
            tags.extend(sanskrit_data_tags)
        if tags == []:
            return None
        else:
            return tags


class LexicalLookupFactory(object):

    @staticmethod
    def create(name):
        if name == "inria":
            return InriaXMLWrapper()
        if name == "sanskrit_data":
            return SanskritDataWrapper()
        if name == "combined":
            return CombinedWrapper()
        raise Exception("invalid type", name)
