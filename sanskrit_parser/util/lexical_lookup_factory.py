'''
Created on Aug 4, 2017

@author: alvarna
'''

from sanskrit_parser.util.inriaxmlwrapper import InriaXMLWrapper
from sanskrit_parser.util.sanskrit_data_wrapper import SanskritDataWrapper
from sanskrit_parser.util.lexical_lookup import LexicalLookup
import logging


def _merge_tags(tags):
    ''' Merge tags from multiple sources

        Inputs
           tags: List of elements of form (baseword, tagset)
        Outputs
           list of elements of form (baseword, tagset), with
           tagsets properly merged
    '''
    tdict = {}
    # Convert to a dict of sets for proper set union
    for t in tags:
        base = t[0]
        if base not in tdict:
            tdict[base] = {frozenset(t[1])}
        else:
            ttags = frozenset(t[1])
            rs = set()
            add = True
            for tbs in tdict[base]:
                if ttags == tbs:  # Already in there
                    break
                elif ttags.issuperset(tbs):  # Superset, add and remove subset
                    rs.add(tbs)
                elif ttags.issubset(tbs):  # Subset, don't add
                    add = False
                    break
            if rs:
                tdict[base].difference_update(rs)
            if add:
                tdict[base].add(ttags)
    tlist = []
    # Convert back to list of tuples
    for base in tdict:
        tlist.extend([(base, set(s)) for s in tdict[base]])
    return tlist


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
        tags = _merge_tags(tags)
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
