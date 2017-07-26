#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
""" Lexical Analyzer for Sanskrit words

    Author: Karthik Madathil <kmadathil@gmail.com>

    Heavily uses https://github.com/drdhaval2785/inriaxmlwrapper/sanskritmark
    Thank you, Dr. Dhaval Patel!

    Based on Linguistic data released by Gerard Huet (Thank you!)
    http://sanskrit.rocq.inria.fr/DATA/XML
"""

import base.SanskritBase as SanskritBase
import sanskritmark
import re
import networkx as nx
from itertools import islice,imap
from  sandhi import Sandhi
import logging
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
            return list(imap(lambda x: [y.transcoded(SanskritBase.SLP1) for y in x[1:-1]],\
                             islice(nx.shortest_simple_paths(self.G, self.start, self.end), max_paths)))
        else: # Fall back to all_simple_paths
            ps = list(imap(lambda x: [y.transcoded(SanskritBase.SLP1) for y in x[1:-1]],\
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
    
        This class mostly reuses Dr. Dhaval Patel's work in wrapping
        Inria XML data 
    """
    
    sandhi = Sandhi() # Singleton!
    
    # Context Aware Sandhi Split map
    sandhi_context_map = dict([
            ((None,'A','[^ieouEOfFxX]'),('a_a','a_A','A_a','A_A')), # akaH savarNe dIrghaH
            ((None,'A','[^kKcCtTwWSzsH]'),('As_',)), # bhobhago'dho'pUrvasya yo'shi, lopashshAkalyasya
            ((None,'a','[^akKcCtTwWSzsH]'),('as_',)), # bhobhago'dho'pUrvasya yo'shi, lopashshAkalyasya - ato rorapludadaplute
            ((None,'I','[^ieouEOfFxX]'),('i_i','i_I','I_i','I_I')), # akaH savarNe dIrghaH 
            ((None,'U','[^ieouEOfFxX]'),('u_u','u_U','U_u','U_U')), # akaH savarNe dIrghaH
            ((None,'F','[^ieouEOfFxX]'),('f_f','f_x','x_f','F_x','x_F','F_F')), # akaH savarNe dIrghaH
            ((None,'e','[^ieouEOfFxX]'),('e_a','a_i','a_I','A_i','A_I')), # AdguNaH
            # AdguNaH / sasajusho ruH, ato rorapludAdaplute, hashi cha
            ((None,'o','[^ieouEOfFxX]'),('o_o','a_u','a_U','A_u','A_U','as_a')), 
            ((None,'o','[^ieouEOfFxXkKpP]'),('as_',)), # sasajusho ruH, ato rorapludAdaplute, hashi cha
            ((None,'E','[^ieouEOfFxX]'),('E_E','a_e','A_e','a_E','A_E')), # vRddhirechi
            ((None,'O','[^ieouEOfFxX]'),('O_O','a_o','A_o','a_O','A_O')), # vRddhirechi
            (('a','r','[^ieouEOfFxX]'),('f_',)), # uraN raparaH
            (('a','l','[^ieouEOfFxX]'),('x_',)), # uraN raparaH
            (('[iIuUeEoO]','r',None),('s_',)), # sasjusho ruH
            ('d',('t_','d_')), # Partial jhalAM jhasho'nte
            ('g',('k_','g_')), # Partial jhalAM jhasho'nte
            ('q',('w_','q_')), # Partial jhalAM jhasho'nte
            ((None,'H','[kKpPtTwW]'),('s_','r_')), # kupvoH xk xp vA
            ((None,'s','[tTkKpP]'),('s_','r_')), # visarjanIyasya sa
            # Does this overdo things?
            ((None,'z','[wWkKpP]'),('s_','r_')), # visarjanIyasya sa, ShTuNa Shtu
            ((None,'S','[cC]'),('s_','r_')), # visarjanIyasya sa, schuna schu
            (('[iIuUfFxX]','S',None),('s_',)), # apadAntasya mUrdhanyaH, iNkoH
            ('M',('m_','M_')), # mo'nusvAraH
            ((None,'y','[aAuUeEoO]'),('i_','I_')), # iko yaNachi
            ((None,'v','[aAiIeEoO]'),('u_','U_')),  # iko yaNachi
            ('N',('N_','M_','m_')), # anusvArasya yayi pararavarNaH
            ('Y',('Y_','M_','m_')), # do
            ('R',('R_','M_','m_')), # do
            ('n',('n_','M_','m_')), # do
            ('m',('m_','M_')), # do
            ((None,'H','$'),('s_','r_')), # Visarga at the end
            ('s',None), # Forbidden to split at an s except for cases already matched
            ('S',None), # Forbidden to split at an S except for cases already matched
            ('z',None), # Forbidden to split at an z except for cases already matched
            ((None,'ay','[aAiIuUeEoO]'),('e_',)), # echo ayavAyAvaH
            ((None,'Ay','[aAiIuUeEoO]'),('o_',)), # echo ayavAyAvaH
            ((None,'av','[aAiIuUeEoO]'),('E_',)), # echo ayavAyAvaH
            ((None,'Av','[aAiIuUeEoO]'),('O_',)), # echo ayavAyAvaH
            ((None,'a','[aAiIuUeEoO]'),('e_',)), # echo ayavAyAvaH, lopashshAkalyasya
            ((None,'A','[aAiIuUeEoO]'),('o_',)), # echo ayavAyAvaH, lopashshAkalyasya
            ((None,'a','[aAiIuUeEoO]'),('E_',)), # echo ayavAyAvaH, lopashshAkalyasya
            ((None,'A','[aAiIuUeEoO]'),('O_',)), # echo ayavAyAvaH, lopashshAkalyasya
            ((None,'gG',None),('k_h','K_h','g_h','G_h')), # partial jhayo ho'nyatarasyAm
            # FIXME: Check if these will happen
            #((None,'kK',None),('k_h','K_h','g_h','G_h')), # partial jhayo ho'nyatarasyAm 
            #((None,'wW',None),('w_h','W_h','q_h','Q_h')), # partial jhayo ho'nyatarasyAm 
            ((None,'qQ',None),('w_h','W_h','q_h','Q_h')), # partial jhayo ho'nyatarasyAm 
       ])
        # FIXME: more jhalAM jhasho
        # FIXME: Lots more hal sandhi missing
        
    tagmap = {
             'प्राथमिकः':'v-cj-prim',
             'णिजन्तः':'v-cj-ca',
             'यङन्तः':'v-cj-int',
             'सन्नन्तः':'v-cj-des',
             'लट्':'sys-prs-md-pr',
             'लोट्':'sys-prs-md-ip',
             'विधिलिङ्':'sys-prs-md-op',
             'लङ्':'sys-prs-md-im',
             'लट्-कर्मणि':'sys-pas-md-pr',
             'लोट्-कर्मणि':'sys-pas-md-ip',
             'विधिलिङ्-कर्मणि':'sys-pas-md-op',
             'लङ्-कर्मणि':'sys-pas-md-im',
             'लृट्':'sys-tp-fut',
             'लिट्':'sys-tp-prf',
             'लुङ्':'sys-tp-aor',
             'आगमाभावयुक्तलुङ्':'sys-tp-inj',
             'लृङ्':'sys-tp-cnd',
             'आशीर्लिङ्':'sys-tp-ben',
             'लुट्':'sys-pef',
             'एकवचनम्':'np-sg',
             'द्विवचनम्':'np-du',
             'बहुवचनम्':'np-pl',
             'उत्तमपुरुषः':'fst',
             'मध्यमपुरुषः':'snd',
             'प्रथमपुरुषः':'trd',
             'प्रथमाविभक्तिः':'na-nom',
             'संबोधनविभक्तिः':'na-voc',
             'द्वितीयाविभक्तिः':'na-acc',
             'तृतीयाविभक्तिः':'na-ins',
             'चतुर्थीविभक्तिः':'na-dat',
             'पञ्चमीविभक्तिः':'na-abl',
             'षष्ठीविभक्तिः':'na-gen',
             'सप्तमीविभक्तिः':'na-loc',
             'एकवचनम्':'sg',
             'द्विवचनम्':'du',
             'बहुवचनम्':'pl',
             'पुंल्लिङ्गम्':'mas',
             'स्त्रीलिङ्गम्':'fem',
             'नपुंसकलिङ्गम्':'neu',
             'सङ्ख्या':'dei',
             'अव्ययम्':'uf',
             'क्रियाविशेषणम्':'ind',
             'उद्गारः':'interj',
             'निपातम्':'parti',
             'चादिः':'prep',
             'संयोजकः':'conj',
             'तसिल्':'tasil',
             'अव्ययधातुरूप-प्राथमिकः':'vu-cj-prim',
             'अव्ययधातुरूप-णिजन्तः':'vu-cj-ca',
             'अव्ययधातुरूप-यङन्तः':'vu-cj-int',
             'अव्ययधातुरूप-सन्नन्तः':'vu-cj-des',
            'तुमुन्':'iv-inf',
            'क्त्वा':'iv-abs',
            'per':'iv-per',
             'क्त्वा-प्राथमिकः':'ab-cj-prim',
             'क्त्वा-णिजन्तः':'ab-cj-ca',
             'क्त्वा-यङन्तः':'ab-cj-int',
             'क्त्वा-सन्नन्तः':'ab-cj-des',
             'प्राथमिकः':'kr-cj-prim-no',
             'णिजन्तः':'kr-cj-ca-no',
             'यङन्तः':'kr-cj-int-no',
             'सन्नन्तः':'kr-cj-des-no',
             '':'kr-vb-no',
             'कर्मणिभूतकृदन्तः':'ppp',
             'कर्तरिभूतकृदन्तः':'ppa',
             'कर्मणिवर्तमानकृदन्तः':'pprp',
             'कर्तरिवर्तमानकृदन्त-परस्मैपदी':'ppr-para',
             'कर्तरिवर्तमानकृदन्त-आत्मनेपदी':'ppr-atma',
             'पूर्णभूतकृदन्त-परस्मैपदी':'ppft-para',
             'पूर्णभूतकृदन्त-आत्मनेपदी':'ppft-atma',
             'कर्मणिभविष्यत्कृदन्तः':'pfutp',
             'कर्तरिभविष्यत्कृदन्त-परस्मैपदी':'pfut-para',
             'कर्तरिभविष्यत्कृदन्त-आत्मनेपदी':'pfut-atma',
             'य':'gya',
             'ईय':'iya',
             'तव्य':'tav',
             'कर्तरि':'para',
             'कर्तरि':'atma',
             'कर्मणि':'pass',
             'कृदन्तः':'pa',
	     'समासपूर्वपदनामपदम्':'iic',
	     'समासपूर्वपदकृदन्तः':'iip',
	     'समासपूर्वपदधातुः':'iiv',
	     'उपसर्गः':'upsrg'
            
        }
    tag_cache = {}

    def __init__(self):
        pass
    
    def getInriaLexicalTags(self,obj):
        """ Get Inria-style lexical tags for a word

            Params:
                obj(SanskritObject): word
            Returns
                list: List of (base, tagset) pairs
        """
        ot = obj.transcoded(SanskritBase.SLP1)
        # Check in cache first
        if ot in self.tag_cache:
            return self.tag_cache[ot]
        s = sanskritmark.analyser(ot,split=False)
        if s=="????":  # Not found
            return None
        else:
            # Split into list of tags
            l=s.split("|")
            # Further split each tag into a list
            l=[li.split("-") for li in l]
            # Convert into name, tagset pairs
            l=[(li[0],set(li[1:])) for li in l]
            # Insert into cache
            self.tag_cache[ot] = l
            return l
        
    def hasInriaTag(self,obj,name,tagset):
        """ Check if word matches Inria-style lexical tags

            Params:
                obj(SanskritObject): word
                name(str): name in Inria tag
                tagset(set): set of Inria tag elements
            Returns
                list: List of (base, tagset) pairs for obj that 
                      match (name,tagset), or None
        """
        l = self.getInriaLexicalTags(obj)
        if l is None:
            return None
        assert (name is not None) or (tagset is not None)
        r = []
        for li in l:
            # Name is none, or name matches
            # Tagset is None, or all its elements are found in Inria tagset
            if ((name is None) or\
                name.transcoded(SanskritBase.SLP1)==li[0]) and \
               ((tagset is None) or\
                tagset.issubset(li[1])):
                r.append(li)
        if r==[]:
            return None
        else:
            return r

    def getSandhiSplits(self,o,use_internal_sandhi_splitter=True,debug=False):
        ''' Get all valid Sandhi splits for a string

            Params: 
              o(SanskritObject): Input object
            Returns:
              SanskritLexicalGraph : DAG all possible splits
        '''
        # Transform to internal canonical form
        self.dynamic_scoreboard = {}
        s = o.transcoded(SanskritBase.SLP1)
        dag = self._possible_splits(s,use_internal_sandhi_splitter,debug)
        if not dag:
            return None
        else:
            return dag
        
    def _possible_splits(self,s,use_internal_sandhi_splitter=True,debug=False):
        ''' private method to dynamically compute all sandhi splits

        Used by getSandhiSplits
           Params: 
              s(string): Input SLP1 encoded string
            Returns:
              SanskritLexicalGraph : DAG of possible splits
        '''
        logger.debug("Splitting "+s)
        def _is_valid_word(ss):
            # r = sanskritmark.analyser(ss,split=False)
            # if r=="????":
            #     r=False
            r = sanskritmark.quicksearch(ss)
            return r


        def _sandhi_splits(lsstr,rsstr):
            #do all possible sandhi replacements of c, get s_c_list= [(s_c_left0, s_c_right0), ...]
            s_c_list = set()
            c = lsstr[-1]
            # Unconditional Sandhi reversal
            if c in self.sandhi_context_map:
                # Unconditional/Forbidden splits are marked by direct keys
                if self.sandhi_context_map[c] is not None: # Not a forbidden split
                    for cm in self.sandhi_context_map[c]:
                        # Split into left/right context additions
                        cml,cmr=cm.split("_")
                        if rsstr: # Right context is non-empty
                            # Addition to right context
                            crsstr = cmr + rsstr
                            # Addition to left context
                            clsstr = lsstr[0:-1]+cml
                            # FIXME check added to prevent loops like A-A_A etc.
                            # Check if this causes real problems
                            if crsstr != s:
                                # Addition to left context
                                s_c_list.add((clsstr, crsstr))
                        else:   #Null right context, do not prepend to rsstr
                            # Insert only if necessary to avoid duplicates
                            s_c_list.add((lsstr[0:-1]+cml, None)) 
            else:
                # No direct key, split is not forbidden
                s_c_list.add((lsstr, rsstr))
                 
 
            # Conditional (context sensitive sandhi reversal)
            for csm in self.sandhi_context_map:
                # Tuple indicates a context-sensitive split
                if isinstance(csm,tuple):
                    assert len(csm)==3 
                    # Match end varnas of left string to key.
                    # How many varnas to match depends on key size
                    cmatch=(csm[1]==lsstr[-len(csm[1]):])
                    if cmatch:
                        # If left key is not None, check if left context matches
                        lmatch=(csm[0] is None) or ((len(lsstr)>1) and re.match(csm[0],lsstr[-2]))
                        # If right key is not None, check if right context matches or is None
                        # Special match for empty right context = $
                        rmatch=(csm[2] is None) or ((len(rsstr) and re.match(csm[2],rsstr[0])) or
                                                    (not len(rsstr)) and (csm[2]=='$'))
                        if rmatch and lmatch: # Both match
                            logger.debug("Context Sandhi match: {} {} {}".format(csm,lsstr,rsstr))
                            # Apply each replacement
                            for cm in self.sandhi_context_map[csm]:
                                logger.debug("Trying: "+cm)
                                # Split into left and right additions
                                cml,cmr=cm.split("_")
                                # Add to right context
                                crsstr = cmr + rsstr
                                clsstr = lsstr[0:-len(csm[1])] + cml
                                # FIXME check added to prevent loops like A-A_A etc.
                                # Check if this causes real problems
                                if crsstr != s:
                                    s_c_list.add((clsstr, crsstr))
            return s_c_list                 
         
        def _sandhi_splits_all(s, use_internal_sandhi_splitter, start=None, stop=None):
            if use_internal_sandhi_splitter:
                splits = set()
                start = start or 0
                stop = stop or len(s)
                for ix in xrange(start, stop):
                    # Left and right substrings
                    lsstr = s[start:ix+1] 
                    rsstr = s[ix+1:]
                    logger.debug("Left, Right substrings = {} {}".format(lsstr,rsstr))
                    # Get all possible splits as a list of lists 
                    s_c_list = _sandhi_splits(lsstr,rsstr)
                    if s_c_list:
                        splits |= s_c_list
            else:
                # For Sandhi Splitter
                obj = SanskritBase.SanskritObject(s,encoding=SanskritBase.SLP1)
                splits = self.sandhi.split_all(obj, start, stop)
            return splits
                
        splits = False

        # Memoization for dynamic programming - remember substrings that've been seen before
        if s in self.dynamic_scoreboard:
            logger.debug("Found {} in scoreboard".format(s))
            return self.dynamic_scoreboard[s]

        # If a space is found in a string, stop at that space
        spos = s.find(' ')
        if spos!=-1:
            # Replace the first space only
            s=s.replace(' ','',1)
            
        s_c_list = _sandhi_splits_all(s, use_internal_sandhi_splitter, start=0, stop=spos+1)
        logger.debug("s_c_list: "+str(s_c_list))

        node_cache = {}

        for (s_c_left,s_c_right) in s_c_list:
            # Is the left side a valid word?
            if _is_valid_word(s_c_left):
                logger.debug("Valid left word: "+s_c_left)
                # For each split with a valid left part, check it there are valid splits of the right part
                if s_c_right and s_c_right != '':
                    logger.debug("Trying to split:"+s_c_right)
                    rdag = self._possible_splits(s_c_right,use_internal_sandhi_splitter,debug)
                    # if there are valid splits of the right side
                    if rdag:
                        # Make sure we got a graph back
                        assert isinstance(rdag,SanskritLexicalGraph)
                        # if there are valid splits of the right side
                        if s_c_left not in node_cache:
                            # Extend splits list with s_c_left appended with possible splits of s_c_right
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
                        # Extend splits list with s_c_left appended with possible splits of s_c_right
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
        # Update scoreboard for this substring, so we don't have to split again  
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
#        parser.add_argument('--no-sort',action='store_true')
#        parser.add_argument('--no-flatten',action='store_true')
        parser.add_argument('--use-internal-sandhi-splitter',action='store_true')
        parser.add_argument('--debug',action='store_true')
        parser.add_argument('--max-paths',type=int,default=10)
        return parser.parse_args()

    def main():
        args=getArgs()
        print "Input String:", args.data

        if args.debug:
            logging.basicConfig(filename='SanskritLexicalAnalyzer.log', filemode='w', level=logging.DEBUG)
        else:
            logging.basicConfig(filename='SanskritLexicalAnalyzer.log', filemode='w', level=logging.INFO)

        s=SanskritLexicalAnalyzer()
        if args.input_encoding is None:
            ie = None
        else:
            ie = SanskritBase.SCHEMES[args.input_encoding]
        i=SanskritBase.SanskritObject(args.data,encoding=ie)
        print "Input String in SLP1:",i.transcoded(SanskritBase.SLP1)
        if not args.split:
            ts=s.getInriaLexicalTags(i)
            print ts
            if args.tag_set or args.base:
                if args.tag_set:
                    g=set(args.tag_set)
                print s.hasInriaTag(i,SanskritBase.SanskritObject(args.base),g)
        else:
            import datetime
            print "Start Split:", datetime.datetime.now()
            graph=s.getSandhiSplits(i,use_internal_sandhi_splitter=args.use_internal_sandhi_splitter,debug=args.debug)
            print "End DAG generation:", datetime.datetime.now()
            if graph:
                splits=graph.findAllPaths(max_paths=args.max_paths,debug=args.debug)
                print "End pathfinding:", datetime.datetime.now()
                print "Splits:"
                if splits:
                    for split in splits:
                        print split
                else:
                    print "None"                
            else:
                print "No Valid Splits Found"
    main()

