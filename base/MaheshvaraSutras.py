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
            u'अइउण् ऋऌक् एओङ् ऐऔच् हयवरट् लण् ञमङणनम् झभञ् घढधष् जबगडदश् खछठथचटतव् कपय् शषसर् हल्',SanskritBase.DEVANAGARI)
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
        pitpos=self.MSS.find(pit,pnpos)
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
        pos = self.getPratyahara(p).transcoded(SanskritBase.HK)
        # Check if varna String is in Pratyahara String
        return (pos.find(v.transcoded(SanskritBase.HK))!=-1)
    
if __name__ == "__main__":
    import sys
    def main():
        m=MaheshvaraSutras()
        print m
        if len(sys.argv)>1:
            p=sys.argv[1]
        else:
            p="ik"
        p=SanskritBase.SanskritObject(p,SanskritBase.HK)
        print p
        print m.getPratyahara(p)
        if len(sys.argv)>2:
            v=sys.argv[2]
            print m.isInPratyahara(p,SanskritBase.SanskritObject(v,SanskritBase.HK))
    main()
