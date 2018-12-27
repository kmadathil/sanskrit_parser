#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
""" Lexical Analyzer for Sanskrit words

    Author: Karthik Madathil <kmadathil@gmail.com>
"""

from __future__ import print_function
from sanskrit_parser.util.lexical_lookup_factory import LexicalLookupFactory
import sanskrit_parser.base.sanskrit_base as SanskritBase

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


class SanskritLexicalGraph(object):
    """ DAG class to hold Lexical Analysis Results

        Represents the results of lexical analysis as a DAG
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

    def findAllPaths(self, max_paths=10, sort=True, score=False):
        """ Find all paths through DAG to End

            Params:
               max_paths (int :default:=10): Number of paths to find
                          If this is > 1000, all paths will be found
               sort (bool)                 : If True (default), sort paths
                                             in ascending order of length
        """
        if self.roots:
            self.lockStart()
        # shortest_simple_paths is slow for >1000 paths
        if max_paths <= 1000:
            paths = list(six.moves.map(lambda x: x[1:-1],
                                       islice(nx.shortest_simple_paths(
                                              self.G, self.start, self.end),
                                              max_paths)))
            if score:
                from sanskrit_parser.util import lexical_scorer
                scorer = lexical_scorer.Scorer()
                path_scores = [(path, scorer.score(path)) for path in paths]
                sorted_path_scores = sorted(path_scores, key=operator.itemgetter(1), reverse=True)
                logger.debug("Sorted paths with scores:\n %s", sorted_path_scores)
                return sorted_path_scores
            else:
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


class SanskritLexicalAnalyzer(object):
    """ Singleton class to hold methods for Sanskrit lexical analysis. """

    sandhi = Sandhi()  # Singleton!

    def __init__(self, lexical_lookup="combined"):
        forms = LexicalLookupFactory.create(lexical_lookup)
        self.forms = forms
        pass

    def getLexicalTags(self, obj, tmap=True):
        """ Get Lexical tags for a word

            Params:
                obj(SanskritObject): word
                tmap(Boolean=True): If True, maps
                    tags to our format
            Returns
                list: List of (base, tagset) pairs
        """
        ot = obj.canonical()
        tags = self.forms.get_tags(ot, tmap)
        return tags

    def hasTag(self, obj, name, tagset):
        """ Check if word matches lexical tags

            Params:
                obj(SanskritObject): word
                name(str): name in tag
                tagset(set): set of tag elements
            Returns
                list: List of (base, tagset) pairs for obj that
                      match (name,tagset), or None
        """
        lexical_tags = self.getLexicalTags(obj)
        if lexical_tags is None:
            return None
        assert (name is not None) or (tagset is not None)
        r = []
        for li in lexical_tags:
            # Name is none, or name matches
            # Tagset is None, or all its elements are found in Inria tagset
            if ((name is None) or name.canonical() == li[0]) and \
                    ((tagset is None) or tagset.issubset(li[1])):
                r.append(li)
        if r == []:
            return None
        else:
            return r

    def tagLexicalGraph(self, g):
        ''' Tag a Lexical Graph with lexical tags

         Params:
            g (SanskritLexicalGraph) : input lexical graph
        '''
        for n in g:
            # Avoid start and end
            if isinstance(n, SanskritBase.SanskritObject):
                t = self.getLexicalTags(n)
                logger.debug("Got tags %s for %s", t, n)
                n.setLexicalTags(t)

    def getSandhiSplits(self, o, tag=False):
        ''' Get all valid Sandhi splits for a string

            Params:
              o(SanskritObject): Input object
              tag(Boolean)     : When True (def=False), return a
                                 lexically tagged graph
            Returns:
              SanskritLexicalGraph : DAG all possible splits
        '''
        self.dynamic_scoreboard = {}
        # Transform to internal canonical form
        s = o.canonical()
        # Initialize an empty graph to hold the splits
        self.splits = SanskritLexicalGraph()
        # _possible_splits updates graph in self.splits with nodes and returns roots
        roots = self._possible_splits(s)
        if tag and len(roots) > 0:
            self.tagLexicalGraph(self.splits)
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
            obj = SanskritBase.SanskritObject(s, encoding=SanskritBase.SLP1)
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
        parser = ArgumentParser(description='Lexical Analyzer')
        # String to encode
        parser.add_argument('data', nargs="?", type=str, default="adhi")
        # Input Encoding (autodetect by default)
        parser.add_argument('--input-encoding', type=str, default=None)
        # Filter by base name
        parser.add_argument('--base', type=str, default=None)
        # Filter by tag set
        parser.add_argument('--tag-set', type=str, default=None, nargs="+")
        parser.add_argument('--split', action='store_true')
        parser.add_argument('--debug', action='store_true')
        parser.add_argument('--max-paths', type=int, default=10)
        parser.add_argument('--lexical-lookup', type=str, default="combined")
        parser.add_argument('--strict-io', action='store_true',
                            help="Do not modify the input/output string to match conventions", default=False)
        parser.add_argument('--score', action='store_true')
        return parser.parse_args()

    def main():
        args = getArgs()
        if args.strict_io:
            print("Interpreting input strictly")
        else:
            print("Interpreting input loosely (strict_io set to false)")
        print("Input String:", args.data)

        if args.debug:
            logging.basicConfig(filename='SanskritLexicalAnalyzer.log',
                                filemode='w', level=logging.DEBUG)
        else:
            logging.basicConfig(filename='SanskritLexicalAnalyzer.log',
                                filemode='w', level=logging.INFO)

        s = SanskritLexicalAnalyzer(args.lexical_lookup)
        if args.input_encoding is None:
            ie = None
        else:
            ie = SanskritBase.SCHEMES[args.input_encoding]
        with SanskritBase.outputctx(args.strict_io):
            if not args.split:
                i = SanskritBase.SanskritObject(args.data, encoding=ie,
                                                strict_io=args.strict_io,
                                                replace_ending_visarga='s')
                print("Input String in SLP1:", i.canonical())
                ts = s.getLexicalTags(i)
                print(ts)
                # Possible rakaranta
                # Try by replacing end visarga with 'r' instead
                if not args.strict_io:
                    i = SanskritBase.SanskritObject(args.data, encoding=ie,
                                                    strict_io=args.strict_io,
                                                    replace_ending_visarga='r')
                    ts = s.getLexicalTags(i)
                    if ts is not None:
                        print("Input String in SLP1:", i.canonical())
                        print(ts)
                if args.tag_set or args.base:
                    if args.tag_set:
                        g = set(args.tag_set)
                    print(s.hasTag(i, SanskritBase.SanskritObject(args.base), g))
            else:
                import time
                i = SanskritBase.SanskritObject(args.data, encoding=ie,
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
                    print("End pathfinding")
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
