#! /usr/bin/env python
# -*- coding: utf-8 -*-

import base.SanskritBase as SanskritBase
import re

class MaheshvaraSutras(object):
    """ Singleton MaheshvaraSutras class
    
        Attributes:
           MS(SanskritObject): Internal representation of mAheshvara sutras
          MSS(str)           : Transcoded(SLP1) string representation
    """
    def __init__(self):
        """ Initialize Maheshvara Sutras object
        """
        # Note that a space is deliberately left after each it to help in
        # demarcating them.
        self.MS=SanskritBase.SanskritObject(
            u'अइउण् ऋऌक् एओङ् ऐऔच् हयवरट् लण् ञमङणनम् झभञ् घढधष् जबगडदश् खफछठथचटतव् कपय् शषसर् हल् ',SanskritBase.DEVANAGARI)
        # SLP1 version for internal operations
        self.MSS=self.MS.transcoded(SanskritBase.SLP1)
    def __str__(self):
        # Use SLP1 for default string output
        return self.MSS

    def getPratyahara(self,p,longp=True,remove_a=False,dirghas=False):
        """ Return list of varnas covered by a pratyahara

            Args:
              p(:class:SanskritObject): Pratyahara
              longp(boolean :optional:): When True (default), uses long pratyaharas 
              remove_a(boolean :optional:): When True, removes intermediate 'a'. 
                   This is better for computational use
              dirgas(boolean :optional:) When True (default=False) adds dirgha vowels
                    to the returned varnas
            Returns
              (SanskritObject): List of varnas to the same encoding as p
        """
        # SLP1 encoded pratyahara string
        ps=p.transcoded(SanskritBase.SLP1)
        # it - halantyam
        pit=ps[-1]
        # Non it - all except it
        pnit=ps[:-1]
        # Non it position
        pnpos=self.MSS.find(pnit)
        # It position - space added to match it marker in internal
        #representation
        if longp: # Find last occurence of it
            pitpos=self.MSS.rfind(pit+' ',pnpos)
        else:     # Find first occurence of it
            pitpos=self.MSS.find(pit+' ',pnpos)
        # Substring. This includes intermediate its and spaces
        ts = self.MSS[pnpos:pitpos]
        # Replace its and spaces
        ts = re.sub('. ','',ts)
        # Remove अकारः मुखसुखार्थः 
        if remove_a:
            ts = ts[0]+ts[1:].replace('a','')
        # Add dIrgha vowels if requested
        if dirghas:
            ts = ts.replace('a', 'aA').replace('i', 'iI').replace('u', 'uU').replace('f', 'fF').replace('x','xX')
        return SanskritBase.SanskritObject(ts,SanskritBase.SLP1)
    
    def isInPratyahara(self,p,v,longp=True):
        """ Checks whether a given varna is in a pratyahara

            Args:
              p(SanskritObject): Pratyahara
              v(SanskritObject): Varna
              longp(boolean :optional:): When True (default), uses long pratyaharas 
          Returns
              boolean: Is v in p?
        """
       
        vs  = v.transcoded(SanskritBase.SLP1)
        # १ . १ . ६९ अणुदित् सवर्णस्य चाप्रत्ययः 
        # So, we change long and pluta vowels to short ones in the input string
        # Replace long vowels with short ones (note SLP1 encoding)
        vs=re.sub('[AIUFX]+', lambda m: m.group(0).lower(), vs)
        # Remove pluta
        vs=vs.replace('3','')

        # Convert Pratyahara into String
        # the 'a' varna needs special treatment - we remove the
        # अकारः मुखसुखार्थः before searching!
        pos = self.getPratyahara(p,longp,remove_a=vs[0]=='a').transcoded(SanskritBase.SLP1)

        # Check if varna String is in Pratyahara String
        return (pos.find(vs)!=-1)
    
if __name__ == "__main__":
    import argparse
    def getArgs():
        """
          Argparse routine. 
          Returns args variable
        """
        # Parser Setup
        parser = argparse.ArgumentParser(description='SanskritObject')
        # Pratyahara - print out the list of varnas in this
        parser.add_argument('--pratyahara',type=str,default="ik")
        # Varna. Optional. Check if this varna is in pratyahara above
        parser.add_argument('--varna',type=str,default=None)
        # Encoding Optional
        parser.add_argument('--encoding',type=str,default=None)
        # Short pratyaharas
        parser.add_argument('--short',action='store_true')
        # Remove intermediate as
        parser.add_argument('--remove-a',action='store_true')
        # Include dIrghas when returning the pratyAhAra
        parser.add_argument('--dirghas',action='store_true', default=False)

        return parser.parse_args()
    def main():
        args = getArgs()
        m=MaheshvaraSutras()
        print m
        if args.encoding is not None:
            e=SanskritBase.SCHEMES[args.encoding]
        else:
            e=None
        p=SanskritBase.SanskritObject(args.pratyahara,e)
        l = not args.short
        print unicode(p.transcoded(SanskritBase.DEVANAGARI))
        print unicode(m.getPratyahara(p,l,args.remove_a,args.dirghas).transcoded(SanskritBase.DEVANAGARI))
        if args.varna is not None:
            v=SanskritBase.SanskritObject(args.varna,e)
            print u"Is {} in {}?".format(v.transcoded(SanskritBase.DEVANAGARI),
                                        p.transcoded(SanskritBase.DEVANAGARI))
            print m.isInPratyahara(p,v,l)
    main()
