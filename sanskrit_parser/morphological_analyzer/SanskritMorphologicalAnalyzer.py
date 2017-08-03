#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
  Morphological Analyzer for Sanskrit Sentences. 


'''
from __future__ import print_function
import sanskrit_parser.base.SanskritBase as SanskritBase
import sanskrit_parser.lexical_analyzer.SanskritLexicalAnalyzer as SanskritLexicalAnalyzer
import constraint

import logging
logger = logging.getLogger(__name__)


# Rules for morphological analyzer
# Only one lakara
_lakaras=set(['law','liw','luw','lrw','low','laN','liN','luN','lfN'])
def oneLakara(*nodes):
    ''' Only one Lakara is allowed '''
    # lakaras in SLP1
    l=0
    for n in nodes:
        nset=set(map(lambda x: x.transcoded(SanskritBase.SLP1),list(n[1])))
        if not(_lakaras.isdisjoint(nset)):
            l=l+1
    return l<=1

# padas in prathamA must match vacana of lakara
def prathamA(*nodes):
    ''' Only one Lakara is allowed '''
    return True


# all padas in same case must match in linga, purusha and vacana

# samAsa constituents must be followed by another samasa constiuent or subanta
# upasarga rules
# karmapravcanIya rules


class SanskritMorphologicalAnalyzer(SanskritLexicalAnalyzer.SanskritLexicalAnalyzer):
    """ Singleton class to hold methods for Sanksrit morphological analysis. 
    
    """
    def __init__(self):
        super(SanskritMorphologicalAnalyzer,self).__init__()

    def constrainPath(self,path):
        ''' Apply Morphological Constraints on path

        Params:
            path(list): List of SanskritObjects (tagged)
        '''
        _ncache={}
        vlist=[]
        def _uniq(s):
            if s not in _ncache:
                _ncache[s]=0
                return s
            else:
                _ncache[s]=_ncache[s]+1
                return s+"_"+str(_ncache[s])
        # Ensure we have tags
        for p in path:
            assert p.tags, "No tags for {}".format(p)
        # Solver
        problem = constraint.Problem()
        for p in path:
            v=_uniq(str(p))
            vlist.append(v)
            logger.debug("Added Variable {} {}".format(v,p.tags))
            problem.addVariable(v,p.tags)
        problem.addConstraint(oneLakara)
        s=problem.getSolutions()
        return s
    
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
        parser.add_argument('data',nargs="?",type=str,default="astyuttarasyAMdishidevatAtmA")
        # Input Encoding (autodetect by default)
        parser.add_argument('--input-encoding',type=str,default=None)
        # Filter by base name
        parser.add_argument('--debug',action='store_true')
        parser.add_argument('--max-paths',type=int,default=10)
        return parser.parse_args()

    def main():
        args=getArgs()
        print("Input String:", args.data)

        if args.debug:
            logging.basicConfig(filename='MorphologicalAnalyzer.log', filemode='w', level=logging.DEBUG)
        else:
            logging.basicConfig(filename='MorphologicalAnalyzer.log', filemode='w', level=logging.INFO)
        logger.info("Begun Logging")
        s=SanskritMorphologicalAnalyzer()
        if args.input_encoding is None:
            ie = None
        else:
            ie = SanskritBase.SCHEMES[args.input_encoding]
        i=SanskritBase.SanskritObject(args.data,encoding=ie)
        print("Input String in SLP1:",i.transcoded(SanskritBase.SLP1))
        import datetime
        print("Start Split:", datetime.datetime.now())
        graph=s.getSandhiSplits(i,tag=True,debug=args.debug)
        print("End DAG generation:", datetime.datetime.now())
        if graph:
            splits=graph.findAllPaths(max_paths=args.max_paths,debug=args.debug)
            print("End pathfinding:", datetime.datetime.now())
            print("Splits:")
            for sp in splits:
                print(sp)
            p=map(s.constrainPath,splits)
            map(lambda x: map(print,x),p)
        else:
            print("No Valid Splits Found")
            return
            
    main()

