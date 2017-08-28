'''
Created on Aug 4, 2017

@author: alvarna
'''

from sanskrit_parser.util.inriaxmlwrapper import InriaXMLWrapper
from sanskrit_parser.util.sanskrit_data_wrapper import SanskritDataWrapper
from sanskrit_parser.util.lexical_lookup import LexicalLookup

class CombinedWrapper(LexicalLookup):
    
    def __init__(self):
        self.inria = LexicalLookupFactory.create("inria")
        self.sanskrit_data = LexicalLookupFactory.create("sanskrit_data")
        
    def valid(self, word):
        return self.inria.valid(word) or self.sanskrit_data.valid(word)

    def get_tags(self, word):
        tags = self.inria.get_tags(word) or []
        tags.extend(self.sanskrit_data.get_tags(word))
        if tags == []:
            return None

class LexicalLookupFactory(object):
    
    @staticmethod
    def create(name):
        if name == "inria": return InriaXMLWrapper()
        if name == "sanskrit_data": return SanskritDataWrapper()
        if name == "combined": return CombinedWrapper()
        raise Exception("invalid type", name)