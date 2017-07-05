#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
""" Lexical Analyzer for Sanskrit words

    Author: Karthik Madathil <kmadathil@gmail.com>

    Heavily uses https://github.com/drdhaval2785/inriaxmlwrapper/sanskritmark
    Thank you, Dr. Dhaval Patel!
"""

import base.SanskritBase as SanskritBase
import sanskritmark

class SanskritLexicalAnalyzer(object):
    """ Singleton class to hold methods for Sanksrit lexical analysis. 
    
        This class mostly reuses Dr. Dhaval Patel's work in wrapping
        Inria XML data 
    """
    def __init__(self):
        self.dynamic_scoreboard = {}

        # Borrowed from https://github.com/drdhaval2785/samasasplitter/split.py
        # Thank you, Dr. Dhaval Patel!
        self.sandhi_map = dict( [
            ('A',('A_','a_a','a_a','A_A','A_A','A_A')),
            ('I',('I_','i_i','i_i','I_I','I_I')),
            ('U',('U_','u_u','u_u','U_U','U_U')),
            ('F',('F_','f_f','f_f','x_x','F_F','x_x','F_F')),
            ('e',('e_','e_e','a_a','a_a','A_A','A_A')),
            ('o',('o_','o_o','a_a','a_a','A_A','A_A','aH_','aH_a','a_a')),
            ('E',('E_','a_a','A_A','a_a','A_A')),
            ('O',('O_','a_a','A_A','a_a','A_A')),
            ('ar',('af','ar')),  # Why this?
            ('d',('t_','d_'),),
            ('H',('H_','s_'),),
            ('S',('S_','s_','H_')),
            ('M',('m_','M_')),
            ('y',('y_','i_','I_')),
            ('N',('N_','M_')),
            ('Y',('Y_','M_')),
            ('R',('R_','M_')),
            ('n',('n_','M_')),
            ('m',('m_','M_')),
            ('v',('v_','u_','U_')),
            ('r',('r_','s_','H_')),] )
        # FIXME : check if this covers all combos and annotate with sutras
        # Can't see the rAmAH + iha = rAmA iha / rAmAy iha options
        # Ditto for rAme iha = rama iha / ramayiha etc.
        # But this is a start.
        # FIXME: Lack of right context in this map worries me.
        # Can't put a finger to it right now.
        
        self.tagmap = {
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
        self.tag_cache = {}
        
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
              list : Hierarchical list of all possible splits
        '''
        # Transform to internal canonical form
        s = o.transcoded(SanskritBase.SLP1)
        return self._possible_splits(s,debug)
    
    def _possible_splits(self,s,debug=False):
        ''' private method to dynamically compute all sandhi splits

        Used by getSandhiSplits
           Params: 
              s(string): Input SLP1 encoded string
            Returns:
              list : Hierarchical list of all possible splits
        '''
        if debug:
            print "Splitting ", s
        def _is_valid_word(ss):
            r = sanskritmark.analyser(ss,split=False)
            if r=="????":
                r=False
            self.tag_cache[ss]=r
            return r
        splits = []
        
        # Dynamic programming - remember substrings that've been seen before
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
            #do all possible sandhi replacements of c, get s_c_list= [(s_c_left0, s_c_right0), ...]
            s_c_list = []
            
            if c in self.sandhi_map: 
                for cm in self.sandhi_map[c]:
                    cml,cmr=cm.split("_")
                    # FIXME check added to prevent infinite loops like A-A_A etc.
                    # Check if this causes real problems
                    if rsstr: # Non-null, no problem
                        s_c_list.append([lsstr[0:-1]+cml, cmr+rsstr])
                    else:   #Null, do not prepend to rsstr
                        # Insert only if necessary to avoid dupes
                        if [lsstr[0:-1]+cml, None] not in s_c_list: 
                            s_c_list.append([lsstr[0:-1]+cml, None])
            else:
                s_c_list.append([lsstr,rsstr])
            if debug:
                print "s_c_list:", s_c_list
            for (s_c_left,s_c_right) in s_c_list:
                # Is the left side a valid word?
                if _is_valid_word(s_c_left):
                    if debug:
                        print "Valid left split: ", s_c_left, self.tag_cache[s_c_left]
                    # For each split with a valid left part, check it there are valid splits of the right part
                    if s_c_right:
                        if debug:
                            print "Trying to split:",s_c_right
                        ps = self._possible_splits(s_c_right,debug)
                        # if there are valid splits of the right side
                        if ps:
                            # Extend splits list with (s_c_left, (possible splits of s_c_right))
                            splits.append([s_c_left,ps])
                    else: # Null right part
                        splits.append([s_c_left,None])
                else:
                    if debug:
                        print "Invalid left word: ", s_c_left
        # Update scoreboard for this substring, so we don't have to split again  
        self.dynamic_scoreboard[s]=splits
        if debug:
            print "Returning: ",splits
        return splits   

if __name__ == "__main__":
    import argparse
    def getArgs():
        """
          Argparse routine. 
          Returns args variable
        """
        # Parser Setup
        parser = argparse.ArgumentParser(description='Lexical Analyzer')
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
        return parser.parse_args()

    def main():
        args=getArgs()
        print args.data
 
        s=SanskritLexicalAnalyzer()
        i=SanskritBase.SanskritObject(args.data,encoding=args.input_encoding)
        if not args.split:
            ts=s.getInriaLexicalTags(i)
            print ts
            if args.tag_set or args.base:
                if args.tag_set:
                    g=set(args.tag_set)
                print s.hasInriaTag(i,SanskritBase.SanskritObject(args.base),g)
        else:
            from time import strftime
            print "Start split:", strftime("%a, %d %b %Y %H:%M:%S")
            splits=s.getSandhiSplits(i,debug=args.debug)
            print "End split:", strftime("%a, %d %b %Y %H:%M:%S")
            print splits

    main()
