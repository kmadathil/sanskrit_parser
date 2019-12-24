#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
""" Sandhi Analyzer for Sanskrit words

    Author: Karthik Madathil <kmadathil@gmail.com>
"""

from __future__ import print_function
from sanskrit_parser.util.lexical_lookup_factory import LexicalLookupFactory
import sanskrit_parser.base.sanskrit_base as SanskritBase
from sanskrit_parser.util import lexical_scorer

import networkx as nx
from itertools import islice
from .sandhi import Sandhi
import logging
import six
import operator

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

logger = logging.getLogger(__name__)


class SandhiGraph(object):
    """ DAG class to hold Sandhi Lexical Analysis Results

        Represents the results of lexical sandhi analysis as a DAG
        Nodes are SanskritObjects
    """
    start = "__start__"
    end = "__end__"

    def __init__(self):
        ''' DAG Class Init

        Params:
            elem (SanskritObject :optional:): Optional initial element
            end  (bool :optional:): Add end edge to initial element
        '''
        self.roots = []
        self.G = nx.DiGraph()
        self.scorer = lexical_scorer.Scorer()

    def __iter__(self):
        ''' Iterate over nodes '''
        return self.G.__iter__()

    def hasNode(self, t):
        ''' Does a given node exist in the graph?

            Params:
               t (SanskritObject): Node
            Returns:
               boolean
        '''
        return t in self.G

    def appendToNode(self, t, nodes):
        """ Create edges from t to nodes

            Params:
                t (SanskritObject)      : Node to append to
                nodes (iterator(nodes)) : Nodes to append to t
        """
        # t is in our graph
        assert t in self.G
        for r in nodes:
            self.G.add_edge(t, r)

    def addNode(self, node):
        """ Extend dag with node inserted at root

            Params:
                Node (SanskritObject)      : Node to add
                root (Boolean)             : Make a root node
                end  (Boolean)             : Add an edge to end
        """
        assert node not in self.G
        self.G.add_node(node)

    def addEndEdge(self, node):
        ''' Add an edge from node to end '''
        assert node in self.G
        self.G.add_edge(node, self.end)

    def addRoots(self, roots):
        self.roots.extend(roots)

    def lockStart(self):
        ''' Make the graph ready for search by adding a start node

        Add a start node, add arcs to all current root nodes, and clear
        self.roots
        '''
        self.G.add_node(self.start)
        for r in self.roots:
            self.G.add_edge(self.start, r)
        self.roots = []

    def scoreGraph(self):
        edges = self.G.edges()
        edges_list = []
        edges_to_score = []
        for edge in edges:
            edges_list.append(edge)
            if edge[0] == self.start:
                edges_to_score.append([edge[1]])
            elif edge[1] == self.end:
                edges_to_score.append([edge[0]])
            else:
                edges_to_score.append(edge)
        scores = self.scorer.score_splits(edges_to_score)
        for edge, score in zip(edges_list, scores):
            # Score is log-likelihood, so higher is better.
            # For graph path-finding, smaller weight is better, so use negative
            edges[edge]['weight'] = -score
        for u, v, w in self.G.edges(data='weight'):
            logger.debug("u = %s, v = %s, w = %s", u, v, w)

    def findAllPaths(self, max_paths=10, sort=True, score=True):
        """ Find all paths through DAG to End

            Params:
               max_paths (int :default:=10): Number of paths to find
                          If this is > 1000, all paths will be found
               sort (bool)                 : If True (default), sort paths
                                             in ascending order of length
        """
        if self.roots:
            self.lockStart()
        if score:
            self.scoreGraph()
        # shortest_simple_paths is slow for >1000 paths
        if max_paths <= 1000:
            if score:
                paths = list(six.moves.map(lambda x: x[1:-1],
                                           islice(nx.shortest_simple_paths(
                                                        self.G, self.start, self.end, weight='weight'),
                                                  max_paths)))
                scores = self.scorer.score_splits(paths)
                path_scores = zip(paths, scores)
                sorted_path_scores = sorted(path_scores, key=operator.itemgetter(1), reverse=True)
                logger.debug("Sorted paths with scores:\n %s", sorted_path_scores)
                # Strip the scores from the returned result, to be consistent with no-scoring option
                sorted_paths, _ = zip(*sorted_path_scores)
                return list(sorted_paths)
            else:
                paths = list(six.moves.map(lambda x: x[1:-1],
                                           islice(nx.shortest_simple_paths(
                                                        self.G, self.start, self.end),
                                                  max_paths)))
                return paths
        else:  # Fall back to all_simple_paths
            ps = list(six.moves.map(lambda x: x[1:-1],
                                    nx.all_simple_paths(self.G, self.start, self.end)))
            # If we do not intend to display paths, no need to sort them
            if sort:
                ps.sort(key=lambda x: len(x))
            return ps

    def __str__(self):
        """ Print representation of DAG """
        return str(self.G)


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
            self.splits.addRoots(roots)
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
                        if not self.splits.hasNode(t):
                            self.splits.addNode(t)
                        self.splits.appendToNode(t, r_roots)
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
                    if not self.splits.hasNode(t):
                        self.splits.addNode(t)
                    self.splits.addEndEdge(t)
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


if __name__ == "__main__":

    from argparse import ArgumentParser

    def getArgs():
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
        parser.add_argument('--debug', action='store_true')
        parser.add_argument('--max-paths', type=int, default=10)
        parser.add_argument('--lexical-lookup', type=str, default="combined")
        parser.add_argument('--strict-io', action='store_true',
                            help="Do not modify the input/output string to match conventions", default=False)
        parser.add_argument('--no-score', dest="score", action='store_false',
                            help="Don't use the lexical scorer to score the splits and reorder them")
        return parser.parse_args()

    def main():
        args = getArgs()
        if args.strict_io:
            print("Interpreting input strictly")
        else:
            print("Interpreting input loosely (strict_io set to false)")
        print("Input String:", args.data)

        if args.debug:
            logging.basicConfig(filename='LexicalSandhiAnalyzer.log',
                                filemode='w', level=logging.DEBUG)
        else:
            logging.basicConfig(filename='LexicalSandhiAnalyzer.log',
                                filemode='w', level=logging.INFO)

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
                ts = s.getMorphologicalTags(i)
                print("Morphological tags:")
                if ts is not None:
                    for t in ts:
                        print(t)
                # Possible rakaranta
                # Try by replacing end visarga with 'r' instead
                if not args.strict_io:
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
                    splits = graph.findAllPaths(max_paths=args.max_paths, score=args.score)
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
    main()
