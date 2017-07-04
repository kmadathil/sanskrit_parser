#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Karthik Madathil <kmadathil@gmail.com>

""" Lexical Analyzer for words

    Mostly uses inriaxmlwrapper/sanskritmark
"""

import base.SanskritBase as SanskritBase
import sanskritmark

class SanskritLexicalAnalyzer(object):
    """ Singleton class to hold methods for Sanksrit lexical analysis. 
    
        This class mostly reuses Dr. Dhaval Patel's work in wrapping 
    """
    def __init__(self):
        pass
    def getInriaLexicalTags(self,obj):
        """ Get Inria-style lexical tags for a word

            Params:
                obj(SanskritObject): word
            Returns
                list: List of (base, tagset) pairs
        """
        s = sanskritmark.analyser(obj.transcoded(SanskritBase.SLP1))
        if s=="????":  # Not found
            return None
        else:
            # Split into list of tags
            l=s.split("|")
            # Further split each tag into a list
            l=[li.split("-") for li in l]
            # Convert into name, tagset pairs
            l=[(li[0],set(li[1:])) for li in l]
            return l
    def hasInriaTag(self,obj,name,tagset):
        l = self.getInriaLexicalTags(obj)
        assert (name is not None) or (tagset is not None)
        r = []
        for li in l:
            if ((name is None) or\
                name.transcoded(SanskritBase.SLP1)==li[0]) and \
               ((tagset is None) or\
                reduce(lambda x,y: x and y,[s in li[1] for s in tagset])):
               r.append(li)
        return r
            
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
        return parser.parse_args()

    def main():
        args=getArgs()
        print args.data
 
        s=SanskritLexicalAnalyzer()
        i=SanskritBase.SanskritObject(args.data,encoding=args.input_encoding)
        ts=s.getInriaLexicalTags(i)
        print ts
        g=set(['upsrg'])
        print s.hasInriaTag(i,SanskritBase.SanskritObject('adhi'),g)
    main()
