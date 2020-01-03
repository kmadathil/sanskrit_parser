#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''  Morphological Analyzer for Sanskrit Sentences.

Usage
======

The ``SanskritMorphologicalAnalyzer`` class has a similar interface to
``SanskritSandhiAnalyzer``, and has a ``constrainPath()`` method which
can find whether a particular split has a valid morphology, and output
all such valid morphologies.

.. code:: python

    >>> from sanskrit_parser.base.sanskrit_base import SanskritObject, SLP1
    >>> from sanskrit_parser.morphological_analyzer.sanskrit_morphological_analyzer import SanskritMorphologicalAnalyzer
    >>> sentence = SanskritObject("astyuttarasyAm")
    >>> analyzer = SanskritMorphologicalAnalyzer()
    >>> graph=analyzer.getSandhiSplits(sentence,tag=True)
    >>> splits=graph.findAllPaths()
    >>> for sp in splits:
    >>>     print("Lexical Split:",sp)
    >>>     p=analyzer.constrainPath(sp)
    >>>     if p:
    >>>         print("Valid Morphologies")
    >>>         for pp in p:
    >>>             print([(spp,pp[str(spp)]) for spp in sp])
    >>>     else:
    >>>         print("No valid morphologies for this split")
    ...
    ('Lexical Split:', [asti, uttarasyAm])
    Valid Morphologies
    [(asti, ('as#1', set([kartari, law, ekavacanam, prATamikaH, praTamapuruzaH]))),
    (uttarasyAm, ('uttara#2', set([strIliNgam, saptamIviBaktiH, ekavacanam])))]
    [(asti, ('as#1', set([kartari, law, ekavacanam, prATamikaH, praTamapuruzaH]))),
    (uttarasyAm, ('uttara#1', set([strIliNgam, saptamIviBaktiH, ekavacanam])))]
    ('Lexical Split:', [asti, uttara, syAm])
    No valid morphologies for this split
    ('Lexical Split:', [asti, ut, tara, syAm])
    No valid morphologies for this split



Command line usage
==================

The sanskrit_parser script can be used to view parses as below.

If the --dot option is provided, a .dot file is created with all the possible
morphologies as nodes, and possible relations as edges. The valid parses
extracted from this graph are also written out as _parse.dot files


::

    $ sanskrit_parser vakya astyuttarasyAMdiSi --input SLP1 --dot vakya.dot
    ...
    Lexical Split: [asti, uttarasyAm, diSi]
    ...
    Parse 0
    asti=>['asti', {strIliNgam, samAsapUrvapadanAmapadam}]
    uttarasyAm=>['uttara#2', {ekavacanam, saptamIviBaktiH, strIliNgam}]
    diSi=>['diS', {saptamIviBaktiH, ekavacanam, strIliNgam}]
    Parse 1
    asti=>['asti', {strIliNgam, samAsapUrvapadanAmapadam}]
    uttarasyAm=>['uttara#1', {ekavacanam, saptamIviBaktiH, strIliNgam}]
    diSi=>['diS#2', {ekavacanam, saptamIviBaktiH, strIliNgam}]
    Parse 2
    asti=>['asti', {strIliNgam, samAsapUrvapadanAmapadam}]
    uttarasyAm=>['uttara#2', {ekavacanam, saptamIviBaktiH, strIliNgam}]
    diSi=>['diS#2', {ekavacanam, saptamIviBaktiH, strIliNgam}]
    Parse 3
    asti=>['asti', {strIliNgam, samAsapUrvapadanAmapadam}]
    uttarasyAm=>['uttara#1', {ekavacanam, saptamIviBaktiH, strIliNgam}]
    diSi=>['diS', {saptamIviBaktiH, ekavacanam, strIliNgam}]
    ...

    $ dot -Tpng vakya.dot -o vakya.png
    $ eog vakya.png

"""


'''
from __future__ import print_function
import sanskrit_parser.base.sanskrit_base as SanskritBase
from sanskrit_parser.parser.sandhi_analyzer import LexicalSandhiAnalyzer
from sanskrit_parser.util.DhatuWrapper import DhatuWrapper
from sanskrit_parser.parser.datastructures import VakyaGraph, getSLP1Tagset
from argparse import ArgumentParser
import constraint
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

need_lakara = False

dw = DhatuWrapper()

# Lakaras
_lakaras = set(['law', 'liw', 'luw', 'lrw', 'low', 'laN', 'liN', 'luN', 'lfN',
                'viDiliN', 'ASIrliN', 'law-karmaRi', 'liw-karmaRi', 'luw-karmaRi',
                'lrw-karmaRi', 'low-karmaRi', 'laN-karmaRi', 'liN-karmaRi',
                'luN-karmaRi', 'lfN-karmaRi'])
# Disallowed last padas
_ldis = set(['samAsapUrvapadanAmapadam', 'upasargaH'])
# Vacanas
_vacanas = set(['ekavacanam', 'dvivacanam', 'bahuvacanam'])
# Puruzas
_puruzas = ['praTamapuruzaH', 'maDyamapuruzaH', 'uttamapuruzaH']
prathama = 'praTamAviBaktiH'
# Lingas
_lingas = set(['puMlliNgam', 'napuMsakaliNgam', 'strIliNgam', 'triliNgam'])
_sankhya = set(['saNKyA'])
# Samastapada former parts
_samastas = set(['samAsapUrvapadanAmapadam'])
# tiGanta vibhaktis
_vibhaktis = set(['praTamAviBaktiH', 'dvitIyAviBaktiH', 'tritIyAviBaktiH',
                  'caturTIviBaktiH', 'paNcamIviBaktiH', 'zazWIviBaktiH',
                  'saptamIviBaktiH', 'saMboDanaviBaktiH'])
_dvitiya = 'dvitIyAviBaktiH'
_sambodhana = 'saMboDanaviBaktiH'

# Rules for morphological analyzer


# Disallow empty tagsets
def nonempty(*nodes):
    ''' No empty tagsets allowed '''
    for n in nodes:
        if list(n[1]) == []:
            return False
    return True


# Only one lakara
def oneLakara(*nodes):
    ''' Only one Lakara is allowed '''
    # lakaras in SLP1
    global need_lakara
    lakaras = 0
    for n in nodes:
        nset = getSLP1Tagset(n)
        if not(_lakaras.isdisjoint(nset)):
            lakaras = lakaras + 1
    # Variable to enforce a lakara
    if need_lakara:
        return lakaras == 1
    else:
        return lakaras <= 1


# Last pada cannot be an upasarga or samasapurvapada
def lastWord(*nodes):
    n = nodes[-1]
    nset = getSLP1Tagset(n)
    r = _ldis.isdisjoint(nset)
    logger.debug(nset)
    return r


# Upasarga must be before a verb
def upasarga(*nodes):
    r = True
    for ix, n in enumerate(nodes):
        nset = getSLP1Tagset(n)
        if set(['upasargaH']) <= nset:
            r = r and (not _lakaras.isdisjoint(getSLP1Tagset(nodes[ix + 1])))
    return r


# Rules for prathamA/sambodhanA
def prathamA(*nodes):
    ''' Rules for prathamA, sambodhanA vibhaktis

        padas in prathamA ('kartr'/karman) must match the purusha / vacana of lakara
        sambodhana vibhakti rules: Lakara must be in madhyamapurusha

    '''
    r = True
    vacana = None
    puruza = None
    for n in nodes:
        nset = getSLP1Tagset(n)
        # Pick the first lakara
        if not(_lakaras.isdisjoint(nset)):
            vacana = nset.intersection(_vacanas)
            logger.debug("Found Lakara vacana:{}".format(vacana))
            assert len(vacana) == 1, "Only one vacana allowed: {}".format(list(vacana))
            vacana = list(vacana)[0]
            puruza = nset.intersection(_puruzas)
            logger.debug("Found Lakara puruza:{}".format(puruza))
            assert len(puruza) == 1, "Only one puruza allowed: {}".format(list(puruza))
            puruza = list(puruza)[0]
    # No lakara found
    if vacana is None:
        return not need_lakara
    pstem = None
    dstem = None
    dvacana = None
    yuzmad = False
    for n in nodes:
        nset = getSLP1Tagset(n)
        if prathama in nset:
            mvacana = nset.intersection(_vacanas)
            logger.debug("Found PrathamA {} vacana:{}".format(n[0], mvacana))
            assert len(mvacana) == 1, "Only one mvacana allowed: {}".format(list(mvacana))
            mvacana = list(mvacana)[0]
            logger.debug('Pre Prathama result:'.format(r))
            r = r and (mvacana == vacana)
            if puruza == _puruzas[1]:
                # Can't have asmad with madhyama
                r = r and (n[0] != 'asmad')
            elif puruza == _puruzas[2]:
                # Can't have yuzmad with uttama
                r = r and (n[0] != 'yuzmad')
            else:
                # Can't have either with prathama
                r = r and ((n[0] != 'yuzmad') and (n[0] != 'asmad'))
            pstem = n[0]
            yuzmad = yuzmad or (pstem == 'yuzmad')
            logger.debug('Temp Prathama result:'.format(r))
        if _sambodhana in nset:
            logger.debug('Pre Sambodhana result:'.format(r))
            dvacana = nset.intersection(_vacanas)
            logger.debug("Found Sambodhana {} vacana:{}".format(n[0], dvacana))
            assert len(dvacana) == 1, "Only one dvacana allowed: {}".format(list(dvacana))
            dvacana = list(dvacana)[0]
            # Lakara must be in madhyamapurusha
            if puruza is not None:
                r = r and (puruza == _puruzas[1])
                logger.debug('Temp Sambodhana result:'.format(r))
            dstem = n[0]
    if dvacana is not None:
        # All nodes has been seen, we have found a dvitiya
        if pstem is not None:
            # Must match Sambodhana vacana
            logger.debug('Sambodhana check: {} {}  Yushmad {} mvacana {} dvacana {}'.format(pstem, dstem, yuzmad, mvacana, dvacana))
            # # Prathama stem must be yuzmad
            # r = r and yuzmad
            r = r and (mvacana == dvacana)
    logger.debug('Returning:'.format(r))
    return r


# all padas in same case must match in linga and vacana
def vibhaktiAgreement(*nodes):
    ''' All padas in same vibhakti must agree in linga and vacana '''
    maps = {}
    for n in nodes:
        nset = getSLP1Tagset(n)
        vibhakti = _vibhaktis.intersection(nset)
        if vibhakti:
            assert len(vibhakti) == 1, "Only one vibhakti allowed: {}".format(list(vibhakti))
            logger.debug("Found vibhakti:{}".format(vibhakti))
            vibhakti = list(vibhakti)[0]
            vacana = nset.intersection(_vacanas)
            logger.debug("Found vacana:{}".format(vacana))
            assert len(vacana) == 1, "Only one vacana allowed: {}".format(list(vacana))
            vacana = list(vacana)[0]
            linga = nset.intersection(_lingas)
            logger.debug("Found linga:{}".format(linga))
            if len(linga) == 0:
                sankhya = nset.intersection(_sankhya)
                if sankhya:  # Is "Sankhya" type (kati etc.)
                    continue
            assert len(linga) == 1, "Only one linga allowed: {} : {} in {}".format(list(linga), list(nset), n)
            linga = list(linga)[0]
            slv = set([linga, vacana])
            if vibhakti in maps:
                if maps[vibhakti] != slv:
                    logger.debug("Unequal:{} {}".format(maps[vibhakti], slv))
                    return False
                else:
                    logger.debug("Equal:{} {}".format(maps[vibhakti], slv))
            else:
                maps[vibhakti] = slv
                logger.debug("Map: {} : {}".format(vibhakti, slv))
    return True


# Only sakarmaka dhatus are allowed karma
def sakarmakarule(*nodes):
    global dw  # DhatuWrapper
    dvitiya = False
    sakarmaka = False
    for n in nodes:
        nset = getSLP1Tagset(n)
        if _dvitiya in nset:
            # Found a dvitiya
            dvitiya = True
            logger.debug("Dvitiya: {} {}".format(n[0], list(nset)))
        if not(_lakaras.isdisjoint(nset)):
            # Found a lakara, can get the dhatu
            dh = n[0]
            hpos = dh.find('#')
            if hpos != -1:
                dh = dh[:hpos]
            logger.debug("Lakara: {} {}".format(dh, list(nset)))
            sakarmaka = dw.is_sakarmaka(dh)
            logger.debug("Sakarmakatva: {}".format(sakarmaka))
    return sakarmaka or (not dvitiya)


# samAsa constituents must be followed by another samasa constiuent or subanta
def samasarules(*nodes):
    ''' samasa constituents must be followed by tiGantas
        (or other samasa constituents)
    '''
    r = True
    ixmax = len(nodes) - 1
    for ix, n in enumerate(nodes):
        nset = getSLP1Tagset(n)
        if not _samastas.isdisjoint(nset):
            if ix == ixmax:
                return False
            else:
                nset1 = getSLP1Tagset(nodes[ix + 1])
                if _samastas.isdisjoint(nset1):
                    r = r and (not _vibhaktis.isdisjoint(nset1))
    return r


# upasarga rules
# karmapravcanIya rules


class VakyaAnalyzer(LexicalSandhiAnalyzer):
    """
    Singleton class to hold methods for Sanksrit vakya analysis.
    """

    def __init__(self, lexical_lookup="combined"):
        super(VakyaAnalyzer, self).__init__(lexical_lookup)

    def constrainPath(self, path):
        ''' (Deprecated) Apply Morphological Constraints on path

        Params:
            path(list): List of SanskritObjects (tagged)
        '''
        _ncache = {}
        vlist = []

        def _uniq(s):
            if s not in _ncache:
                _ncache[s] = 0
                return s
            else:
                _ncache[s] = _ncache[s] + 1
                return s + "_" + str(_ncache[s])
        # Ensure we have tags
        for p in path:
            assert p.tags, "No tags for {}".format(p)
        # Solver
        problem = constraint.Problem()
        for p in path:
            v = _uniq(str(p))
            vlist.append(v)
            logger.debug("Added Variable {} {}".format(v, p.tags))
            problem.addVariable(v, p.tags)
        problem.addConstraint(oneLakara)
        problem.addConstraint(lastWord, vlist)
        problem.addConstraint(upasarga, vlist)
        problem.addConstraint(prathamA, vlist)
        problem.addConstraint(samasarules, vlist)
        problem.addConstraint(vibhaktiAgreement, vlist)
        problem.addConstraint(sakarmakarule, vlist)
        problem.addConstraint(nonempty, vlist)
        s = problem.getSolutions()
        return s


def _console_logging():
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logger.addHandler(console)


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
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--max-paths', type=int, default=1)
    parser.add_argument('--constraint', action='store_true', help='Use Constraint Parser instead of Graph Algorithm (deprecated)')
    parser.add_argument('--lexical-lookup', type=str, default="combined")
    parser.add_argument('--strict-io', action='store_true',
                        help="Do not modify the input/output string to match conventions", default=False)
    return parser.parse_args(argv)


def main(argv=None):
    global need_lakara
    args = getArgs(argv)
    vgraph = None
    _console_logging()
    logger.info(f"Input String: {args.data}")
    need_lakara = args.need_lakara
    if args.debug:
        logging.basicConfig(filename='VakyaAnalyzer.log', filemode='w', level=logging.DEBUG)
    s = VakyaAnalyzer(args.lexical_lookup)
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
            splits = graph.find_all_paths(max_paths=args.max_paths)
            end_path = time.time()
            logger.info("End pathfinding")
            print("Splits:")
            spl_t = 0
            for sp in splits:
                print(f"Lexical Split: {sp}")
                if not args.constraint:
                    vgraph = VakyaGraph(sp)
                    for (ix, p) in enumerate(vgraph.parses):
                        print(f"Parse {ix}")
                        for n in p:
                            print(n)
                else:
                    start_c = time.time()
                    p = s.constrainPath(sp)
                    end_c = time.time()
                    if p:
                        print("Valid Morphologies")
                        for pp in p:
                            print([(spp, pp[str(spp)]) for spp in sp])
                    else:
                        logger.warning("No valid morphologies for this split")
                    logger.info(f"Time Taken for Constraint {end_c-start_c:0.6f}s")
                    spl_t = spl_t + (end_c-start_c)
            logger.info("End Morphological Analysis")
            logger.info("-----------")
            logger.info("Performance")
            logger.info("Time taken for split: {0:0.6f}s".format(end_split-start_split))
            logger.info(f"Time taken for path: {end_path-start_path:0.6f}s")
            if args.constraint:
                logger.info(f"Time taken for constraint: {spl_t:0.6f}s")
        else:
            logger.warning("No Valid Splits Found")
    return vgraph


if __name__ == "__main__":
    main()
