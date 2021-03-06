#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Intro
=====

Sandhi Analyzer for Sanskrit words

@author: Karthik Madathil (github: @kmadathil)

Usage
=====

Use the ``LexicalSandhiAnalyzer`` to split a sentence (wrapped in a
``SanskritObject``) and retrieve the top 10 splits:

.. code:: python

    >>> from __future__ import print_function
    >>> from sanskrit_parser.parser.sandhi_analyzer import LexicalSandhiAnalyzer
    >>> from sanskrit_parser.base.sanskrit_base import SanskritObject, SLP1
    >>> sentence = SanskritObject("astyuttarasyAMdishidevatAtmA")
    >>> analyzer = LexicalSandhiAnalyzer()
    >>> splits = analyzer.getSandhiSplits(sentence).findAllPaths(10)
    >>> for split in splits:
    ...    print(split)
    ...
    [u'asti', u'uttarasyAm', u'diSi', u'devatA', u'AtmA']
    [u'asti', u'uttarasyAm', u'diSi', u'devat', u'AtmA']
    [u'asti', u'uttarasyAm', u'diSi', u'devata', u'AtmA']
    [u'asti', u'uttara', u'syAm', u'diSi', u'devatA', u'AtmA']
    [u'asti', u'uttarasyAm', u'diSi', u'devatA', u'at', u'mA']
    [u'asti', u'uttarasyAm', u'diSi', u'de', u'vatA', u'AtmA']
    [u'asti', u'uttarasyAm', u'diSi', u'devata', u'at', u'mA']
    [u'asti', u'uttas', u'rasyAm', u'diSi', u'devat', u'AtmA']
    [u'asti', u'uttara', u'syAm', u'diSi', u'devat', u'AtmA']
    [u'asti', u'uttarasyAm', u'diSi', u'de', u'avatA', u'AtmA']

The sandhi_analyzer can also be used to look up the tags for a given
word form: (Note that the database stores words
ending in visarga with an 's' at the end)

.. code:: python

    >>> word = SanskritObject('hares')
    >>> tags = analyzer.getMorphologicalTags(word)
    >>> for tag in tags:
    ...    print(tag)
    ...
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
from sanskrit_parser.util.lexical_lookup_factory import LexicalLookupFactory
import sanskrit_parser.base.sanskrit_base as SanskritBase

from .sandhi import Sandhi
import logging
from .datastructures import SandhiGraph
from argparse import ArgumentParser


try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

logger = logging.getLogger(__name__)


class LexicalSandhiAnalyzer(object):
    """ Singleton class to hold methods for Sanskrit lexical sandhi analysis.

        We define lexical sandhi analysis to be the process of taking an input sequence
        and transforming it to a collection (represented by a DAG) of potential sandhi
        splits of the sequence. Each member of a split is guaranteed to be a valid
        lexical form.
    """

    sandhi = Sandhi()  # Singleton!

    def __init__(self, lexical_lookup="combined"):
        forms = LexicalLookupFactory.create(lexical_lookup)
        self.forms = forms
        pass

    def getMorphologicalTags(self, obj, tmap=True):
        """ Get Morphological tags for a word

            Params:
                obj(SanskritString): word
                tmap(Boolean=True): If True, maps
                    tags to our format
            Returns
                list: List of (base, tagset) pairs
        """
        ot = obj.canonical()
        tags = self.forms.get_tags(ot, tmap)
        return tags

    def hasTag(self, obj, name, tagset):
        """ Check if word matches morhphological tags

            Params:
                obj(SanskritString): word
                name(str): name in tag
                tagset(set): set of tag elements
            Returns
                list: List of (base, tagset) pairs for obj that
                      match (name,tagset), or None
        """
        morphological_tags = self.getMorphologicalTags(obj)
        if morphological_tags is None:
            return None
        assert (name is not None) or (tagset is not None)
        r = []
        for li in morphological_tags:
            # Name is none, or name matches
            # Tagset is None, or all its elements are found in tagset
            if ((name is None) or name.canonical() == li[0]) and \
                    ((tagset is None) or tagset.issubset(li[1])):
                r.append(li)
        if r == []:
            return None
        else:
            return r

    def tagSandhiGraph(self, g):
        ''' Tag a Sandhi Graph with morphological tags for each node

         Params:
            g (SandhiGraph) : input lexical sandhi graph
        '''
        for n in g:
            # Avoid start and end
            if isinstance(n, SanskritBase.SanskritObject):
                t = self.getMorphologicalTags(n)
                logger.debug("Got tags %s for %s", t, n)
                n.setMorphologicalTags(t)

    def preSegmented(self, sl, tag=False):
        ''' Get a SandhiGraph for a pre-segmented sentence

            Params:
              sl (list of SanskritString): Input object
              tag(Boolean)     : When True (def=False), return a
                                 morphologically tagged graph
            Returns:
              SandhiGraph : DAG all possible splits
        '''
        self.sentence = SandhiGraph()
        prev = None
        for s in sl[::-1]:
            self.sentence.add_node(s)
            if prev is None:
                self.sentence.add_end_edge(s)
            else:
                self.sentence.append_to_node(s, [prev])
            prev = s
        self.sentence.add_roots([prev])
        if tag:
            self.tagSandhiGraph(self.sentence)
        self.sentence.lock_start()
        return self.sentence

    def getSandhiSplits(self, o, tag=False):
        ''' Get all valid Sandhi splits for a string

            Params:
              o(SanskritString): Input object
              tag(Boolean)     : When True (def=False), return a
                                 morphologically tagged graph
            Returns:
              SandhiGraph : DAG all possible splits
        '''
        self.dynamic_scoreboard = {}
        # Transform to internal canonical form
        s = o.canonical()
        # Initialize an empty graph to hold the splits
        self.splits = SandhiGraph()
        # _possible_splits updates graph in self.splits with nodes and returns roots
        roots = self._possible_splits(s)
        if tag and len(roots) > 0:
            self.tagSandhiGraph(self.splits)
        if len(roots) == 0:
            return None
        else:
            self.splits.add_roots(roots)
            return self.splits

    def _possible_splits(self, s):
        ''' private method to dynamically compute all sandhi splits

            Used by getSandhiSplits
            Adds the individual splits to the graph self.splits and returns
            the roots of the subgraph corresponding to the split of s
           Params:
              s(string): Input SLP1 encoded string
            Returns:
              roots : set of roots of subgraph corresponding to possible splits of s
        '''
        logger.debug("Splitting " + s)

        @lru_cache(256)
        def _is_valid_word(ss):
            r = self.forms.valid(ss)
            return r

        def _sandhi_splits_all(s, start=None, stop=None):
            obj = SanskritBase.SanskritImmutableString(s, encoding=SanskritBase.SLP1)
            splits = self.sandhi.split_all(obj, start, stop)
            return splits

        roots = set()

        # Memoization for dynamic programming - remember substrings that've
        # been seen before
        if s in self.dynamic_scoreboard:
            logger.debug("Found {} in scoreboard".format(s))
            return self.dynamic_scoreboard[s]

        # If a space is found in a string, stop at that space
        spos = s.find(" ")
        stop = None if spos == -1 else spos

        s_c_list = _sandhi_splits_all(s, start=0, stop=stop)
        logger.debug("s_c_list: " + str(s_c_list))
        if s_c_list is None:
            s_c_list = []

        node_cache = {}

        for (s_c_left, s_c_right) in s_c_list:
            # Is the left side a valid word?
            if _is_valid_word(s_c_left):
                logger.debug("Valid left word: " + s_c_left)
                # For each split with a valid left part, check it there are
                # valid splits of the right part
                if s_c_right and s_c_right != '':
                    logger.debug("Trying to split:" + s_c_right)
                    r_roots = self._possible_splits(s_c_right.strip())
                    # if there are valid splits of the right side
                    if r_roots:
                        # Make sure we got a set of roots back
                        assert isinstance(r_roots, set)
                        # if there are valid splits of the right side
                        if s_c_left not in node_cache:
                            # Extend splits list with s_c_left appended with
                            # possible splits of s_c_right
                            t = SanskritBase.SanskritObject(s_c_left, encoding=SanskritBase.SLP1)
                            node_cache[s_c_left] = t
                        else:
                            t = node_cache[s_c_left]
                        roots.add(t)
                        if not self.splits.has_node(t):
                            self.splits.add_node(t)
                        self.splits.append_to_node(t, r_roots)
                else:  # Null right part
                    # Why cache s_c_left here? To handle the case
                    # where the same s_c_left appears with a null and non-null
                    # right side.
                    if s_c_left not in node_cache:
                        t = SanskritBase.SanskritObject(s_c_left, encoding=SanskritBase.SLP1)
                        node_cache[s_c_left] = t
                    else:
                        t = node_cache[s_c_left]
                    # Extend splits list with s_c_left appended with
                    # possible splits of s_c_right
                    roots.add(t)
                    if not self.splits.has_node(t):
                        self.splits.add_node(t)
                    self.splits.add_end_edge(t)
            else:
                logger.debug("Invalid left word: " + s_c_left)
        # Update scoreboard for this substring, so we don't have to split
        # again
        self.dynamic_scoreboard[s] = roots
        if len(roots) == 0:
            logger.debug("No splits found, returning empty set")
        else:
            logger.debug("Roots: %s", roots)
        return roots


def getArgs(argv=None):
    """
      Argparse routine.
      Returns args variable
    """
    # Parser Setup
    parser = ArgumentParser(description='Lexical Sandhi Analyzer')
    # String to encode
    parser.add_argument('data', nargs="?", type=str, default="adhi")
    # Input Encoding (autodetect by default)
    parser.add_argument('--input-encoding', type=str, default=None)
    # Filter by base name
    parser.add_argument('--base', type=str, default=None)
    # Filter by tag set
    parser.add_argument('--tag-set', type=str, default=None, nargs="+")
    parser.add_argument('--tags', dest='split', action='store_false')
    parser.add_argument('--max-paths', type=int, default=10)
    parser.add_argument('--lexical-lookup', type=str, default="combined")
    parser.add_argument('--strict-io', action='store_true',
                        help="Do not modify the input/output string to match conventions", default=False)
    parser.add_argument('--no-score', dest="score", action='store_false',
                        help="Don't use the lexical scorer to score the splits and reorder them")
    parser.add_argument('--no-map-tags', dest='map_tags',
                        action='store_false', help="show raw (unmapped to our standard set) tags")
    return parser.parse_args(argv)


def main(argv=None):
    graph = None
    args = getArgs(argv)
    if args.strict_io:
        print("Interpreting input strictly")
    else:
        print("Interpreting input loosely (strict_io set to false)")
    print("Input String:", args.data)

    s = LexicalSandhiAnalyzer(args.lexical_lookup)
    if args.input_encoding is None:
        ie = None
    else:
        ie = SanskritBase.SCHEMES[args.input_encoding]
    with SanskritBase.outputctx(args.strict_io):
        if not args.split:
            i = SanskritBase.SanskritNormalizedString(args.data, encoding=ie,
                                                      strict_io=args.strict_io,
                                                      replace_ending_visarga='s')
            print("Input String in SLP1:", i.canonical())
            ts = s.getMorphologicalTags(i, tmap=args.map_tags)
            print("Morphological tags:")
            if ts is not None:
                for t in ts:
                    print(t)
            # Possible rakaranta
            # Try by replacing end visarga with 'r' instead
            elif not args.strict_io:
                i = SanskritBase.SanskritNormalizedString(args.data, encoding=ie,
                                                          strict_io=args.strict_io,
                                                          replace_ending_visarga='r')
                ts = s.getMorphologicalTags(i)
                if ts is not None:
                    print("Input String in SLP1:", i.canonical())
                    for t in ts:
                        print(t)
            if args.tag_set or args.base:
                if args.tag_set is not None:
                    g = set(args.tag_set)
                else:
                    g = None
                if args.base is not None:
                    b = SanskritBase.SanskritNormalizedString(args.base)
                else:
                    b = None
                print(s.hasTag(i, b, g))
        else:
            import time
            i = SanskritBase.SanskritNormalizedString(args.data, encoding=ie,
                                                      strict_io=args.strict_io,
                                                      replace_ending_visarga=None)
            print("Input String in SLP1:", i.canonical())
            print("Start Split")
            start_split = time.time()
            graph = s.getSandhiSplits(i)
            end_graph = time.time()
            print("End DAG generation")
            if graph:
                logger.debug("Graph has %d nodes and %d edges" % (len(graph.G.nodes()), len(graph.G.edges())))
                splits = graph.find_all_paths(max_paths=args.max_paths, score=args.score)
                print("End pathfinding", time.time())
                print("Splits:")
                if splits:
                    for split in splits:
                        print(split)
                else:
                    print("None")
            else:
                print("No Valid Splits Found")
            end_split = time.time()
            print("-----------")
            print("Performance")
            print("Time for graph generation = {0:0.6f}s".format(end_graph - start_split))
            print("Total time for graph generation + find paths = {0:0.6f}s".format(end_split - start_split))
        return graph


if __name__ == "__main__":
    main()
