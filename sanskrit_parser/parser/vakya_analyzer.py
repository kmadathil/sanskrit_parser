#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Morphological Analyzer for Sanskrit Sentences.

Usage
======

The ``VakyaGraph`` class can be initialized with a split output from
``LexicalSandhiAnalyzer.getSandhiSplits``. The ``.parses`` member contains
all valid parses for that split

.. code-block:: python

        from sanskrit_parser.base.sanskrit_base import SanskritObject, SLP1
        from sanskrit_parser.parser.sandhi_analyzer import LexicalSandhiAnalyzer
        from sanskrit_parser.parser.datastructures import VakyaGraph
        sentence = SanskritObject("astyuttarasyAmdiSi",encoding=SLP1)
        analyzer = LexicalSandhiAnalyzer()
        graph=analyzer.getSandhiSplits(sentence,tag=True)
        splits=graph.find_all_paths(max_paths=1)
        for sp in splits:
            print("Lexical Split:",sp)
            vgraph = VakyaGraph(sp)
            if vgraph.parses:
              for (ix, p) in enumerate(vgraph.parses):
                  print(f"Parse {ix}")
                  for n in p:
                      print(n)
            else:
              print("No valid morphologies for this split")
        ...
        Parse 0
        diSi=>['diS#2', {strIliNgam, ekavacanam, saptamIviBaktiH}]
        asti=>['as', {parasmEpadam, praTamapuruzaH, ekavacanam, law}]
        uttarasyAm=>['uttara#1', {strIliNgam, ekavacanam, saptamIviBaktiH}]
        Parse 1
        diSi=>['diS#2', {dvitIyAviBaktiH, napuMsakaliNgam, bahuvacanam}]
        asti=>['as#1', {kartari, prATamikaH, ekavacanam, law, praTamapuruzaH}]
        uttarasyAm=>['uttara#1', {strIliNgam, ekavacanam, saptamIviBaktiH}]
        Parse 2
        diSi=>['diS#2', {strIliNgam, ekavacanam, saptamIviBaktiH}]
        asti=>['asti', {strIliNgam, samAsapUrvapadanAmapadam}]
        uttarasyAm=>['uttara#1', {strIliNgam, ekavacanam, saptamIviBaktiH}]
        Parse 3
        uttarasyAm=>['uttara#2', {strIliNgam, ekavacanam, saptamIviBaktiH}]
        diSi=>['diS', {saptamIviBaktiH, ekavacanam, strIliNgam}]
        asti=>['as', {parasmEpadam, praTamapuruzaH, ekavacanam, law}]



Command line usage
==================

The sanskrit_parser script can be used to view parses as below.

If the --dot option is provided, a graph is output in .dot fomat with
all the possible morphologies as nodes, and possible relations as
edges. The valid parses extracted from this graph are also written out
as _parse.dot files


::

    $ sanskrit_parser vakya astyuttarasyAMdiSi --input SLP1 --dot vakya.dot
    ...
    Lexical Split: [asti, uttarasyAm, diSi]
    ...
    Parse 0
    asti=>['as#1', {prATamikaH, praTamapuruzaH, kartari, ekavacanam, law}]
    diSi=>['diS#2', {ekavacanam, strIliNgam, saptamIviBaktiH}]
    uttarasyAm=>['uttara#1', {ekavacanam, strIliNgam, saptamIviBaktiH}]
    ...

    $ dot -Tpng vakya.dot -o vakya.png
    $ eog vakya.png
    $ dot -Tpng vakya_parse0.dot -o vakya.png
    $ eog vakya_parse0.png

'''

from __future__ import print_function
import sanskrit_parser.base.sanskrit_base as SanskritBase
from sanskrit_parser.parser.sandhi_analyzer import LexicalSandhiAnalyzer
from sanskrit_parser.parser.datastructures import VakyaGraph, jedge, jnode
from argparse import ArgumentParser
import logging

logger = logging.getLogger(__name__)


def getArgs(argv=None):
    """
      Argparse routine.
      Returns args variable
    """
    # Parser Setup
    parser = ArgumentParser(description='Vakya Analyzer')
    # String to encode
    parser.add_argument('data', nargs="?", type=str, default="astyuttarasyAMdishidevatAtmA")
    # Input Encoding (autodetect by default)
    parser.add_argument('--input-encoding', type=str, default=None)
    # Need a lakara
    parser.add_argument('--need-lakara', action='store_true')
    parser.add_argument('--max-paths', type=int, default=1)
    parser.add_argument('--split-above', type=int, default=5)
    parser.add_argument('--lexical-lookup', type=str, default="combined")
    parser.add_argument('--strict-io', action='store_true',
                        help="Do not modify the input/output string to match conventions", default=False)
    parser.add_argument('--score', dest="score", action='store_true',
                        help="Use the lexical scorer to score the splits and reorder them")
    parser.add_argument('--slow-merge', dest='fast_merge', action='store_false', help="Development Only: use if you see issues in divide and conquer")
    return parser.parse_args(argv)


def main(argv=None):
    global need_lakara
    args = getArgs(argv)
    vgraph = None
    logger.info(f"Input String: {args.data}")
    need_lakara = args.need_lakara
    s = LexicalSandhiAnalyzer(args.lexical_lookup)
    if args.input_encoding is None:
        ie = None
    else:
        ie = SanskritBase.SCHEMES[args.input_encoding]
    i = SanskritBase.SanskritNormalizedString(args.data, encoding=ie,
                                              strict_io=args.strict_io,
                                              replace_ending_visarga=None)
    logger.info(f"Input String in SLP1: {i.canonical()}")
    import time
    logger.info("Start Split")
    start_split = time.time()
    graph = s.getSandhiSplits(i, tag=True)
    end_split = time.time()
    logger.info("End DAG generation")
    with SanskritBase.outputctx(args.strict_io):
        if graph:
            start_path = time.time()
            splits = graph.find_all_paths(max_paths=args.max_paths, score=args.score)
            end_path = time.time()
            logger.info("End pathfinding")
            print("Splits:")
            for sp in splits:
                print(f"Lexical Split: {sp}")
                logger.info(f"Lexical Split: {sp}")
                vgraph = VakyaGraph(sp, max_parse_dc=args.split_above,
                                    fast_merge=args.fast_merge)
                for (ix, p) in enumerate(vgraph.parses):
                    print(f"Parse {ix}")
                    t = []
                    for n in sorted(list(p), key=lambda x: x.index):
                        preds = list(p.predecessors(n))
                        if preds:
                            pred = preds[0]  # Only one
                            lbl = p.edges[pred, n]['label']
                            t.append(jedge(pred, n, lbl, args.strict_io))
                        else:
                            t.append(jnode(n, args.strict_io))
                    for e in t:
                        if e[2]:
                            print(f"{e[0]} => {e[1]} : {e[2]} of {e[3]}")
                        else:
                            print(f"{e[0]} => {e[1]}")

            logger.info("End Morphological Analysis")
            logger.info("-----------")
            logger.info("Performance")
            logger.info("Time taken for split: {0:0.6f}s".format(end_split-start_split))
            logger.info(f"Time taken for path: {end_path-start_path:0.6f}s")
        else:
            logger.warning("No Valid Splits Found")
    return vgraph


if __name__ == "__main__":
    main()
