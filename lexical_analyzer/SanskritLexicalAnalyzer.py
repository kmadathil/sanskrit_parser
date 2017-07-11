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

class SanskritLexicalGraph(object):
    """ DAG class to hold Lexical Analysis Results

        Represents the results of lexical analysis as a DAG
        Nodes are SanskritObjects
    """
    def __init__(self,elem=None,end=False):
        self.adjacency_list={}
        self.roots = []
        self.paths = []
        if elem is not None:
            self.rootElement(elem,end)
    # FIXME Improve docstrings below
    def append_single_root(self,rdag):
        """ append rdag to self, assuming a single root element """
        # Single root
        assert len(self.roots) == 1 
        self.adjacency_list[self.roots[0]] = rdag.roots
        self.adjacency_list.update(rdag.adjacency_list)
    def extend_root(self,rdag):
        """ Extend dag with rdag inserted at root """
        self.roots.extend(list(set(rdag.roots)-set(self.roots)))
        for k in rdag.adjacency_list:
            if k in self.adjacency_list:
                self.adjacency_list[k].extend(list(set(rdag.adjacency_list[k])-set(self.adjacency_list[k])))
            else:
                self.adjacency_list[k] = rdag.adjacency_list[k]
    def rootElement(self,s,end):
        """ Create root element optionally pointing to End """
        obj = SanskritBase.SanskritObject(s,encoding=SanskritBase.SLP1)
        self.roots.append(obj)
        if end:
            self.adjacency_list[obj]=[None]
        else:
            self.adjacency_list[obj]=[]
    def findAllPaths(self,n_paths=1000,debug=False):
        """ Find all paths through DAG to End """
        # Memo
        seen = {}
        def _find_paths():
            # BFS find_all_paths, to get shortest paths first
            # Initialize queue
            q = [(x,[x.transcoded(SanskritBase.SLP1)]) for x in self.roots]
            while q:
                # pop a vertex
                (v,path) = q.pop(0)
                if debug:
                    print "Tentative Path:", path
                for nv in self.adjacency_list[v]:
                    if nv is None:
                        if debug:
                            print "Found Path:",path
                        yield path
                    else:
                        nvs = nv.transcoded(SanskritBase.SLP1)
                        if debug:
                            print "Extending: ", path,nvs
                        q.append((nv, path + [nvs]))
        tp = []
        if not self.paths:
            for ix,p in enumerate(_find_paths()):
                tp.append(p)
                if ix==(n_paths-1):
                    break
        self.paths = tp
        if debug:
            print "All Paths:",self.paths
        return self.paths
    def __str__(self):
        """ Print representation of DAG """
        return "Roots: " + str([str(x) for x in self.roots]) +\
            "\nMatrix: " + str([str(x) + ":" +\
                                str([str(y) for y in self.adjacency_list[x]]) \
                                for x in self.adjacency_list])
    
class SanskritLexicalAnalyzer(object):
    """ Singleton class to hold methods for Sanksrit lexical analysis. 
    
        This class mostly reuses Dr. Dhaval Patel's work in wrapping
        Inria XML data 
    """
    dynamic_scoreboard = {}
    
    # Context Aware Sandhi Split map
    sandhi_context_map = dict([
            ((None,'A','[^ieouEOfFxX]'),('a_a','a_A','A_a','A_A')), # akaH savarNe dIrghaH
            ((None,'A','[^kKcCtTwWSzs]'),('As_',)), # bhobhago'dho'pUrvasya yo'shi, lopashshAkalyasya
            ((None,'a','[^akKcCtTwWSzs]'),('as_',)), # bhobhago'dho'pUrvasya yo'shi, lopashshAkalyasya - ato rorapludadaplute
            ((None,'I','[^ieouEOfFxX]'),('i_i','i_I','I_i','I_I')), # akaH savarNe dIrghaH 
            ((None,'U','[^ieouEOfFxX]'),('u_u','u_U','U_u','U_U')), # akaH savarNe dIrghaH
            ((None,'F','[^ieouEOfFxX]'),('f_f','f_x','x_f','F_x','x_F','F_F')), # akaH savarNe dIrghaH
            ((None,'e','[^ieouEOfFxX]'),('e_a','a_i','a_I','A_i','A_I')), # AdguNaH
            ((None,'o','[^ieouEOfFxX]'),('o_o','a_u','a_U','A_u','A_U')), # AdguNaH
            ((None,'o','[^ieouEOfFxXkKpP]'),('as_','as_a')), # sasajusho ruH, ato rorapludAdaplute, hashi cha
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

    def getSandhiSplits(self,o,debug=False):
        ''' Get all valid Sandhi splits for a string

            Params: 
              o(SanskritObject): Input object
            Returns:
              SanskritLexicalGraph : DAG all possible splits
        '''
        # Transform to internal canonical form
        s = o.transcoded(SanskritBase.SLP1)
        dag = self._possible_splits(s,debug)
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
        if debug:
            print "Splitting ", s
        def _is_valid_word(ss):
            # r = sanskritmark.analyser(ss,split=False)
            # if r=="????":
            #     r=False
            r = sanskritmark.quicksearch(ss)
            return r


        def _sandhi_splits(lsstr,rsstr):
            #do all possible sandhi replacements of c, get s_c_list= [(s_c_left0, s_c_right0), ...]
            s_c_list = []
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
                                s_c_list.append([clsstr, crsstr])
                        else:   #Null right context, do not prepend to rsstr
                            # Insert only if necessary to avoid duplicates
                            if [lsstr[0:-1]+cml, None] not in s_c_list: 
                                s_c_list.append([lsstr[0:-1]+cml, None])
            else:
                # No direct key, split is not forbidden
                s_c_list.append([lsstr,rsstr])
                

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
                            if debug:
                                print "Context Sandhi match:",csm,lsstr,rsstr
                            # Apply each replacement
                            for cm in self.sandhi_context_map[csm]:
                                if debug:
                                    print "Trying:",cm
                                # Split into left and right additions
                                cml,cmr=cm.split("_")
                                # Add to right context
                                crsstr = cmr + rsstr
                                clsstr = lsstr[0:-len(csm[1])] + cml
                                # FIXME check added to prevent loops like A-A_A etc.
                                # Check if this causes real problems
                                if crsstr != s:
                                    s_c_list.append([clsstr, crsstr])
            return s_c_list                 
            
        splits = False
        
        # Memoization for dynamic programming - remember substrings that've been seen before
        if s in self.dynamic_scoreboard:
            if debug:
                print "Found {} in scoreboard".format(s)
            return self.dynamic_scoreboard[s]

        # Iterate over the string, looking for valid left splits
        for (ix,c) in enumerate(s):
            # Left and right substrings
            lsstr = s[0:ix+1] 
            rsstr = s[ix+1:]
            if debug:
                print "Left, Right substrings = {} {}".format(lsstr,rsstr)
            # Get all possible splits as a list of lists 
            s_c_list = _sandhi_splits(lsstr,rsstr)
            if debug:
                print "s_c_list:", s_c_list
            for (s_c_left,s_c_right) in s_c_list:
                # Is the left side a valid word?
                if _is_valid_word(s_c_left):
                    if debug:
                        print "Valid left word: ", s_c_left
                    # For each split with a valid left part, check it there are valid splits of the right part
                    if s_c_right:
                        if debug:
                            print "Trying to split:",s_c_right
                        rdag = self._possible_splits(s_c_right,debug)
                        # if there are valid splits of the right side
                        if rdag:
                            # Make sure we got a graph back
                            assert isinstance(rdag,SanskritLexicalGraph)
                            # if there are valid splits of the right side
                            # Extend splits list with s_c_left appended with possible splits of s_c_right
                            t = SanskritLexicalGraph(s_c_left,end=False)
                            t.append_single_root(rdag)
                            if not splits:
                                splits = SanskritLexicalGraph()
                            splits.extend_root(t)
                    else: # Null right part
                        # Splits is initialized with s_c_left -> None
                        splits = SanskritLexicalGraph(s_c_left,end=True)
                else:
                    if debug:
                        print "Invalid left word: ", s_c_left
        # Update scoreboard for this substring, so we don't have to split again  
        self.dynamic_scoreboard[s]=splits
        if debug:
            print "Returning: ",splits
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
        parser.add_argument('--debug',action='store_true')
        parser.add_argument('--max-paths',type=int,default=10)
        return parser.parse_args()

    def main():
        args=getArgs()
        print "Input String:", args.data
 
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
            graph=s.getSandhiSplits(i,debug=args.debug)
            print "End DAG generation:", datetime.datetime.now()
            if graph:
                splits=graph.findAllPaths(debug=args.debug,n_paths=args.max_paths)
                print "End pathfinding:", datetime.datetime.now()
                print splits
            else:
                print "No Valid Splits Found"
    main()

