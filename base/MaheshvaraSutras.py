#! /usr/bin/env python
# -*- coding: utf-8 -*-

import base.SanskritBase as SanskritBase
import re

class MaheshvaraSutras(object):
    """ Singleton MaheshvaraSutras class
    
        Attributes:
           MS(SanskritObject): Internal representation of Maheshvara Sutras
          MSS(str)           : Transcoded(HK) string representation
    """
    def __init__(self):
        """ Initialize Maheshvara Sutras object
        """
        self.MS=SanskritBase.SanskritObject(
            u'अइउण् ऋऌक् एओङ् ऐऔच् हयवरट् लण् ञमङणनम् झभञ् घढधष् जबगडदश् खछठथचटतव् कपय् शषसर् हल् ',SanskritBase.DEVANAGARI)
        self.MSS=self.MS.transcoded(SanskritBase.HK)
    def __str__(self):
        return self.MSS

    def getPratyahara(self,p):
        """ Return list of varnas covered by a pratyahara

            Args:
              p(:class:SanskritObject): Pratyahara
              encoding(:optional:): encoding of p (SanskritBase.HK by default)
            Returns
              (SanskritObject): List of varnas to the same encoding as p
        """
        # HK encoded pratyahara string
        ps=p.transcoded(SanskritBase.HK)
        # it - halantyam
        pit=ps[-1]
        # Non it - all except it
        pnit=ps[:-1]
        # Non it position
        pnpos=self.MSS.find(pnit)
        # It position
        pitpos=self.MSS.find(pit+' ',pnpos)
        # Substring. This includes intermediate its and spaces
        ts = self.MSS[pnpos:pitpos]
        # Replace its and spaces
        ts = re.sub('. ','',ts) 
        return SanskritBase.SanskritObject(ts)
    def isInPratyahara(self,p,v):
        """ Checks whether a given varna is in a pratyahara

            Args:
              p(SanskritObject): Pratyahara
              v(SanskritObject): Varna
            Returns
              boolean: Is v in p?
        """
        # Convert Pratyahara into String
        pos = self.getPratyahara(p).transcoded(SanskritBase.DEVANAGARI)
        # Check if varna String is in Pratyahara String
        vs  = v.transcoded(SanskritBase.DEVANAGARI)
        #print unicode(pos),unicode(vs)
        return (pos.find(vs)!=-1)
        # FIXME
        #  bug: jha is in hal, but jh is not
        #  fix: check whether v is a terminated (or terminated by another svara)
        #       or not. Modify behavior appropriately

        # FIXME
        #  limitation: Need a "long" / "short" pratyahara option
        #  eg: aN pratyahara has two possibilities
    
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

        return parser.parse_args()
    def main():
        args = getArgs()
        m=MaheshvaraSutras()
        print m
        p=SanskritBase.SanskritObject(args.pratyahara,SanskritBase.HK)
        print p
        print m.getPratyahara(p)
        if args.varna is not None:
            v=SanskritBase.SanskritObject(args.varna,SanskritBase.HK)
            print u"Is {} in {}?".format(v.transcoded(SanskritBase.DEVANAGARI),
                                        p.transcoded(SanskritBase.DEVANAGARI))
            print m.isInPratyahara(p,v)
    main()
