#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
""" Lexical Analyzer for Sanskrit words

    Author: Karthik Madathil <kmadathil@gmail.com>
"""

from __future__ import print_function
import sanskrit_parser.base.sanskrit_base as SanskritBase
import sanskrit_parser.util.inriaxmlwrapper as inriaxmlwrapper
import sanskrit_parser.util.inriatagmapper as inriatagmapper
from sanskrit_parser.util import normalization

import re
import networkx as nx
from itertools import islice
from .sandhi import Sandhi
import logging
import six

logger = logging.getLogger(__name__)


class SanskritLexicalGraph(object):
    """ DAG class to hold Lexical Analysis Results

        Represents the results of lexical analysis as a DAG
        Nodes are SanskritObjects
    """
    start = "__start__"
    end = "__end__"
    def __init__(self,elem=None,end=False):
        ''' DAG Class Init
        
        Params:
            elem (SanskritObject :optional:): Optional initial element
            end  (bool :optional:): Add end edge to initial element
        '''
        self.roots = []
        self.G     = nx.DiGraph()
        if elem is not None:
            self.addNode(elem,root=True,end=end)
    def __iter__(self):
        ''' Iterate over nodes '''
        return self.G.__iter__()
    def hasNode(self,t):
        ''' Does a given node exist in the graph?

            Params:
               t (SanskritObject): Node
            Returns:
               boolean
        '''
        return t in self.G
    def appendToNode(self,t,rdag):
        """ append rdag to self, adding edges from a given node to rdag's roots 

            Params:
                t (SanskritObject)      : Node to append to
             rdag (SanskritLexicalGraph): Graph to append to node
        """
        # t is in our graph
        assert t in self.G
        self.G = nx.compose(self.G,rdag.G)
        for r in rdag.roots:
            self.G.add_edge(t,r)
    def addNode(self,node,root=False,end=False):
        """ Extend dag with node inserted at root             

            Params:
                Node (SanskritObject)      : Node to add
                root (Boolean)             : Make a root node
                end  (Boolean)             : Add an edge to end
        """
        assert node not in self.G
        self.G.add_node(node)
        if root:
            self.roots.append(node)
        if end:
            self.G.add_edge(node,self.end)
    def addEndEdge(self,node):
        ''' Add an edge from node to end '''
        assert node in self.G
        self.G.add_edge(node,self.end)
    def lockStart(self):
        ''' Make the graph ready for search by adding a start node

        Add a start node, add arcs to all current root nodes, and clear
        self.roots
        '''
        self.G.add_node(self.start)
        for r in self.roots:
            self.G.add_edge(self.start,r)
        self.roots=[]
    def findAllPaths(self,max_paths=10,sort=True,debug=False):
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
        if max_paths <=1000:
            return list(six.moves.map(lambda x: x[1:-1],\
                             islice(nx.shortest_simple_paths(self.G,
                                                             self.start,
                                                             self.end),
                                    max_paths)))
        else: # Fall back to all_simple_paths
            ps = list(six.moves.map(lambda x: x[1:-1],\
                             nx.all_simple_paths(self.G, self.start, self.end)))
            # If we do not intend to display paths, no need to sort them
            if sort:
                ps.sort(key=lambda x: len(x))
            return ps

    def __str__(self):
        """ Print representation of DAG """
        return str(self.G)
    
class SanskritLexicalAnalyzer(object):
    """ Singleton class to hold methods for Sanksrit lexical analysis. 
    
    """
    
    sandhi = Sandhi() # Singleton!
    forms  = inriaxmlwrapper.InriaXMLWrapper()

    def __init__(self):
        pass
    
    def getLexicalTags(self,obj,tmap=True):
        """ Get Lexical tags for a word

            Params:
                obj(SanskritObject): word
                tmap(Boolean=True): If True, maps
                    tags to our format
            Returns
                list: List of (base, tagset) pairs
        """
        ot = obj.canonical()
        tags=self.forms.get_tags(ot)
        if tmap and (tags is not None):
            tags=inriatagmapper.inriaTagMapper(tags)
        return tags
        
    def hasTag(self,obj,name,tagset):
        """ Check if word matches lexical tags

            Params:
                obj(SanskritObject): word
                name(str): name in tag
                tagset(set): set of tag elements
            Returns
                list: List of (base, tagset) pairs for obj that 
                      match (name,tagset), or None
        """
        l = self.getLexicalTags(obj)
        if l is None:
            return None
        assert (name is not None) or (tagset is not None)
        r = []
        for li in l:
            # Name is none, or name matches
            # Tagset is None, or all its elements are found in Inria tagset
            if ((name is None) or\
                name.canonical()==li[0]) and \
               ((tagset is None) or\
                tagset.issubset(li[1])):
                r.append(li)
        if r==[]:
            return None
        else:
            return r

    def tagLexicalGraph(self,g):
        ''' Tag a Lexical Graph with lexical tags

         Params:
            g (SanskritLexicalGraph) : input lexical graph
        '''
        for n in g:
            # Avoid start and end
            if isinstance(n,SanskritBase.SanskritObject):
                t=self.getLexicalTags(n)
                n.setLexicalTags(t)
        
    def getSandhiSplits(self,o,tag=False,debug=False):
        ''' Get all valid Sandhi splits for a string

            Params: 
              o(SanskritObject): Input object
              tag(Boolean)     : When True (def=False), return a 
                                 lexically tagged graph
            Returns:
              SanskritLexicalGraph : DAG all possible splits
        '''
        # Transform to internal canonical form
        self.dynamic_scoreboard = {}
        s = o.canonical()
        dag = self._possible_splits(s,debug)
        if tag and dag:
            self.tagLexicalGraph(dag)
        if not dag:
            return None
        else:
            return dag
        
    def _possible_splits(self,s,debug=False):
        ''' private method to dynamically compute all sandhi splits

        Used by getSandhiSplits
           Params: 
              s(string): Input SLP1 encoded string
            Returns:
              SanskritLexicalGraph : DAG of possible splits
        '''
        logger.debug("Splitting "+s)
        def _is_valid_word(ss):
            r = self.forms.valid(ss)
            return r
         
        def _sandhi_splits_all(s, start=None,
                               stop=None):
            obj = SanskritBase.SanskritObject(s,encoding=SanskritBase.SLP1)
            splits = self.sandhi.split_all(obj, start, stop)
            return splits
                
        splits = False

        # Memoization for dynamic programming - remember substrings that've
        # been seen before
        if s in self.dynamic_scoreboard:
            logger.debug("Found {} in scoreboard".format(s))
            return self.dynamic_scoreboard[s]

        # If a space is found in a string, stop at that space
        spos = s.find(' ')
        if spos!=-1:
            # Replace the first space only
            s=s.replace(' ','',1)
            
        s_c_list = _sandhi_splits_all(s, start=0, stop=spos+1)
        logger.debug("s_c_list: "+str(s_c_list))
        if s_c_list == None: s_c_list = []

        node_cache = {}

        for (s_c_left,s_c_right) in s_c_list:
            # Is the left side a valid word?
            if _is_valid_word(s_c_left):
                logger.debug("Valid left word: "+s_c_left)
                # For each split with a valid left part, check it there are
                # valid splits of the right part
                if s_c_right and s_c_right != '':
                    logger.debug("Trying to split:"+s_c_right)
                    rdag = self._possible_splits(s_c_right,debug)
                    # if there are valid splits of the right side
                    if rdag:
                        # Make sure we got a graph back
                        assert isinstance(rdag,SanskritLexicalGraph)
                        # if there are valid splits of the right side
                        if s_c_left not in node_cache:
                            # Extend splits list with s_c_left appended with
                            # possible splits of s_c_right
                            t = SanskritBase.SanskritObject(s_c_left,encoding=SanskritBase.SLP1)
                            node_cache[s_c_left] = t
                        else:
                            t = node_cache[s_c_left]
                        if not splits:
                            splits = SanskritLexicalGraph()
                        if not splits.hasNode(t):
                            splits.addNode(t,root=True)
                        splits.appendToNode(t,rdag)
                else: # Null right part
                    # Why cache s_c_left here? To handle the case
                    # where the same s_c_left appears with a null and non-null
                    # right side.
                    if s_c_left not in node_cache:
                        # Extend splits list with s_c_left appended with
                        # possible splits of s_c_right
                        t = SanskritBase.SanskritObject(s_c_left,encoding=SanskritBase.SLP1)
                        node_cache[s_c_left] = t
                    else:
                        t = node_cache[s_c_left]
                    if not splits:
                        splits = SanskritLexicalGraph()
                    if not splits.hasNode(t):
                        splits.addNode(t,root=True,end=True)
                    else:
                        splits.addEndEdge(t)
            else:
                logger.debug("Invalid left word: "+s_c_left)
        # Update scoreboard for this substring, so we don't have to split
        # again  
        self.dynamic_scoreboard[s]=splits
        if not splits:
            logger.debug("Returning:"+str(splits))
        else:
            logger.debug("Returning: "+" ".join(map(str,splits.G.nodes())))
        return splits

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
        parser.add_argument('data',nargs="?",type=str,default="adhi")
        # Input Encoding (autodetect by default)
        parser.add_argument('--input-encoding',type=str,default=None)
        # Filter by base name
        parser.add_argument('--base',type=str,default=None)
        # Filter by tag set
        parser.add_argument('--tag-set',type=str,default=None,nargs="+")
        parser.add_argument('--split',action='store_true')
        parser.add_argument('--debug',action='store_true')
        parser.add_argument('--max-paths',type=int,default=10)
        parser.add_argument('--strict-io', action='store_true',
                            help="Do not modify the input/output string to match conventions", default=False)
        return parser.parse_args()

    def main():
        args = getArgs()
        print("Input String:", args.data)

        if args.debug:
            logging.basicConfig(filename='SanskritLexicalAnalyzer.log',
                                filemode='w', level=logging.DEBUG)
        else:
            logging.basicConfig(filename='SanskritLexicalAnalyzer.log',
                                filemode='w', level=logging.INFO)

        s = SanskritLexicalAnalyzer()
        if args.input_encoding is None:
            ie = None
        else:
            ie = SanskritBase.SCHEMES[args.input_encoding]
        i = SanskritBase.SanskritObject(args.data,encoding=ie,
                                        strict_io=args.strict_io,
                            strict_io_replace_ending_visarga=(not args.split))
        print("Input String in SLP1:",i.canonical())
        with SanskritBase.outputctx(args.strict_io):
            if not args.split:
                ts=s.getLexicalTags(i)
                print(ts)
                if args.tag_set or args.base:
                    if args.tag_set:
                        g=set(args.tag_set)
                    print(s.hasTag(i,SanskritBase.SanskritObject(args.base),g))
            else:
                import datetime
                print("Start Split:", datetime.datetime.now())
                graph=s.getSandhiSplits(i,debug=args.debug)
                print("End DAG generation:", datetime.datetime.now())
                if graph:
                    splits=graph.findAllPaths(max_paths=args.max_paths,
                                              debug=args.debug)
                    print("End pathfinding:", datetime.datetime.now())
                    print("Splits:")
                    if splits:
                        for split in splits:
                            print(split)
                    else:
                        print("None")
                else:
                    print("No Valid Splits Found")
    main()

