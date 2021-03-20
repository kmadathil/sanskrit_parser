#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
""" Sanskrit Parser Data Structures

    @author: Karthik Madathil (github: @kmadathil)
"""

from sanskrit_parser.base.sanskrit_base import SanskritObject, SanskritImmutableString, SLP1
import networkx as nx
from itertools import islice, product
import logging
import operator
from copy import copy
import six
import time
from collections import defaultdict
from os.path import dirname, basename, splitext, join
from sanskrit_parser.util import lexical_scorer
from sanskrit_parser.util.disjoint_set import DisjointSet
from sanskrit_parser.util.DhatuWrapper import DhatuWrapper
from functools import reduce

__all__ = ['SandhiGraph', 'VakyaGraph', 'VakyaParse', 'getSLP1Tagset']

dw = DhatuWrapper()


logger = logging.getLogger(__name__)


class SandhiGraph(object):
    """ DAG class to hold Sandhi Lexical Analysis Results

        Represents the results of lexical sandhi analysis as a DAG
        Nodes are SanskritObjects
    """
    start = "__start__"
    end = "__end__"

    def __init__(self):
        ''' DAG Class Init

        Params:
            elem (SanskritObject :optional:): Optional initial element
            end  (bool :optional:): Add end edge to initial element
        '''
        self.roots = []
        self.G = nx.DiGraph()
        self.scorer = lexical_scorer.Scorer()

    def __iter__(self):
        ''' Iterate over nodes '''
        return self.G.__iter__()

    def has_node(self, t):
        ''' Does a given node exist in the graph?

            Params:
               t (SanskritObject): Node
            Returns:
               boolean
        '''
        return t in self.G

    def append_to_node(self, t, nodes):
        """ Create edges from t to nodes

            Params:
                t (SanskritObject)      : Node to append to
                nodes (iterator(nodes)) : Nodes to append to t
        """
        # t is in our graph
        assert t in self.G
        for r in nodes:
            self.G.add_edge(t, r)

    def add_node(self, node):
        """ Extend dag with node inserted at root

            Params:
                Node (SanskritObject)      : Node to add
                root (Boolean)             : Make a root node
                end  (Boolean)             : Add an edge to end
        """
        assert node not in self.G
        self.G.add_node(node)

    def add_end_edge(self, node):
        ''' Add an edge from node to end '''
        assert node in self.G
        self.G.add_edge(node, self.end)

    def add_roots(self, roots):
        self.roots.extend(roots)

    def lock_start(self):
        ''' Make the graph ready for search by adding a start node

        Add a start node, add arcs to all current root nodes, and clear
        self.roots
        '''
        self.G.add_node(self.start)
        for r in self.roots:
            self.G.add_edge(self.start, r)
        self.roots = []

    def score_graph(self):
        edges = self.G.edges()
        edges_list = []
        edges_to_score = []
        for edge in edges:
            edges_list.append(edge)
            if edge[0] == self.start:
                edges_to_score.append([edge[1]])
            elif edge[1] == self.end:
                edges_to_score.append([edge[0]])
            else:
                edges_to_score.append(edge)
        scores = self.scorer.score_splits(edges_to_score)
        for edge, score in zip(edges_list, scores):
            # Score is log-likelihood, so higher is better.
            # For graph path-finding, smaller weight is better, so use negative
            edges[edge]['weight'] = -score
        for u, v, w in self.G.edges(data='weight'):
            logger.debug("u = %s, v = %s, w = %s", u, v, w)

    def find_all_paths(self, max_paths=10, sort=True, score=True):
        """ Find all paths through DAG to End

            Params:
               max_paths (int :default:=10): Number of paths to find
                          If this is > 1000, all paths will be found
               sort (bool)                 : If True (default), sort paths
                                             in ascending order of length
        """
        if self.roots:
            self.lock_start()
        if score:
            self.score_graph()
        # shortest_simple_paths is slow for >1000 paths
        if max_paths <= 1000:
            if score:
                paths = list(six.moves.map(lambda x: x[1:-1],
                                           islice(nx.shortest_simple_paths(
                                                        self.G, self.start, self.end, weight='weight'),
                                                  max_paths)))
                scores = self.scorer.score_splits(paths)
                path_scores = zip(paths, scores)
                sorted_path_scores = sorted(path_scores, key=operator.itemgetter(1), reverse=True)
                logger.debug("Sorted paths with scores:\n %s", sorted_path_scores)
                # Strip the scores from the returned result, to be consistent with no-scoring option
                sorted_paths, _ = zip(*sorted_path_scores)
                return list(sorted_paths)
            else:
                paths = list(six.moves.map(lambda x: x[1:-1],
                                           islice(nx.shortest_simple_paths(
                                                        self.G, self.start, self.end),
                                                  max_paths)))
                return paths
        else:  # Fall back to all_simple_paths
            ps = list(six.moves.map(lambda x: x[1:-1],
                                    nx.all_simple_paths(self.G, self.start, self.end)))
            # If we do not intend to display paths, no need to sort them
            if sort:
                ps.sort(key=lambda x: len(x))
            return ps

    def __str__(self):
        """ Print representation of DAG """
        return str(self.G)

    def draw(self, *args, **kwargs):
        _ncache = {}

        def _uniq(s):
            if s not in _ncache:
                _ncache[s] = 0
                return s
            else:
                _ncache[s] = _ncache[s] + 1
                return s + "_" + str(_ncache[s])

        nx.draw(self.G, *args, **kwargs,
                pos=nx.spring_layout(self.G),
                labels={x: _uniq(str(x)) for x in self})

    def write_dot(self, path):
        # H = nx.convert_node_labels_to_integers(G, label_attribute=’node_label’)
        # H_layout = nx.nx_pydot.pydot_layout(G, prog=’dot’)
        # G_layout = {H.nodes[n][‘node_label’]: p for n, p in H_layout.items()}
        nx.drawing.nx_pydot.write_dot(self.G, path)


lakaras = set(['law', 'liw', 'luw', 'lrw', 'low', 'laN', 'liN', 'luN', 'lfN',
               'viDiliN', 'ASIrliN'])
krtverbs = set(['ktvA', 'Satf', 'SAnac', 'tumun', 'kta', 'ktavatu', 'lyap'])
purvakala = set(['ktvA', 'lyap'])
samanakala = set(['Satf', 'Sanac'])
nishta = set(['kta', 'ktavatu'])
karmani = set(['karmaRi'])
samastas = set(['samAsapUrvapadanAmapadam'])
nijanta = set(['RijantaH'])
# Vibhaktis
_vibhaktis = ['praTamAviBaktiH', 'dvitIyAviBaktiH', 'tftIyAviBaktiH',
              'caturTIviBaktiH', 'paYcamIviBaktiH', 'zazWIviBaktiH',
              'saptamIviBaktiH', 'saMboDanaviBaktiH']
prathama = _vibhaktis[1-1]
dvitiya = _vibhaktis[2-1]
tritiya = _vibhaktis[3-1]
chaturthi = _vibhaktis[4-1]
pancami = _vibhaktis[5-1]
shashthi = _vibhaktis[6-1]
saptami = _vibhaktis[7-1]
sambodhana = _vibhaktis[8-1]
vibhaktis = set(_vibhaktis)
# Vacanas
vacanas = set(['ekavacanam', 'dvivacanam', 'bahuvacanam'])
# Puruzas
puruzas = 'praTamapuruzaH', 'maDyamapuruzaH', 'uttamapuruzaH'
karakas = set(['kartA', 'karma', 'karaRam', 'apAdAnam', 'sampradAnam', 'aDikaraRam', 'hetu-kartA'])
predicative_verbs = set(['as', 'BU', 'vft'])
_lingas = ['puMlliNgam', 'napuMsakaliNgam', 'strIliNgam', 'triliNgam']
lingas = set(_lingas)
napumsakam = _lingas[1]

avyaya = set(['avyayam'])
kriyavisheshana = set(['kriyAviSezaRam'])
nishedha = set(['na'])
# FIXME - api and su (pUjAyaM) in here temporarily - need a better solution
karmap_null = set(['su', 'api'])
avyaya_kriyav = set(['kila', 'bata', 'aho', 'nanu', 'hanta', 'eva', 'tu'])
projlabels = karakas.union(kriyavisheshana)
# sambaddha links are projective
samplabels = {'sambadDa-'+lbl for lbl in projlabels}.union({'saMbadDakriyA'})
projlabels.update(samplabels)
sentence_conjunctions = {"yad": {"tad", None},
                         "yadi": {"tarhi"},
                         "yatra": {"tatra"},
                         "yAvat": {"tAvat"},
                         "yadA": {"tadA"},
                         "yaTA": {"taTA"},
                         "api": {None},
                         "cet": {None},
                         "natu": {None},
                         }
conjunctions = {"ca"}
disjunctions = {"uta", "vA"}


# Non Karaka Vibhakti
non_karaka_vibhaktis = {
    2: ["antarA", "antareRa", "pfTak", "vinA", "nAnA"],
    3: ["saha", "pfTak", "vinA", "nAnA"],
    4: ["namaH", "svasti", "svAhA", "alam", "vazaw"],
    5: ["anya", "Arat", "itara", "fte", "pfTak", "vinA", "nAnA"],
}
# FIXME Merge these with above
karmap_2 = set(['anu', 'upa',  'prati', 'aBi', 'aDi', 'ati'])
karmap_5 = set(['apa', 'pari', 'A', 'prati'])

# Edge costs used for ordering
edge_cost = defaultdict(lambda: 1)
for k in karakas:
    edge_cost[k] = 0.9
edge_cost['karma'] = 0.85
edge_cost['kartA'] = 0.8
edge_cost['samasta'] = 0.7
edge_cost['samuccitam'] = 0.7
edge_cost['upasargaH'] = 0.65
# for k in karakas:
#     edge_cost['sambadDa-'+k] = edge_cost[k]
edge_cost['vAkyasambanDaH'] = 0.3
# edge_cost['zazWI-sambanDa'] = 1
edge_cost_const = ['vAkyasambanDaH', 'samuccitam', 'BAvalakzaRam']


class VakyaGraph(object):
    """ DAG class for Sanskrit Vakya Analysis

        Represents Sanskrit Vakya Analysis as a DAG
        Nodes are SanskritObjects with morphological tags
        Edges are potential relationships between them
    """
    def __init__(self, path, max_parse_dc=4, fast_merge=True):
        ''' DAG Class Init

        Params:
             path: Path from SandhiGraph
        '''
        self.max_parse_dc = max_parse_dc
        self.fast_merge = fast_merge
        self.roots = []
        self.isLocked = False
        # Multigraph
        self.G = nx.MultiDiGraph()  # Allow parallel edges
        # Need this many nodes in the extracted subgraphs
        self.path_node_count = len(path)
        logger.debug(f"{self.path_node_count} sets of orthogonal nodes")
        self.partitions = []
        for (ix, sobj) in enumerate(path):
            vnlist = []
            mtags = sobj.getMorphologicalTags()
            for mtag in mtags:
                ncopy = SanskritObject(sobj.canonical(),
                                       encoding=SLP1,
                                       replace_ending_visarga=None)
                ncopy.setMorphologicalTags(mtag)
                pn = VakyaGraphNode(ncopy, ix)
                vnlist.append(pn)
            for vn in vnlist:
                self.add_node(vn)
            self.partitions.append(set(vnlist))
        logger.debug(f"Node Partitions {self.partitions} Len {len(self.partitions)}")
        self.lock()
        self.add_edges()
        # Remove isolated nodes (with no edges)
        isolates = list(nx.isolates(self.G))
        self.G.remove_nodes_from(isolates)
        for (ix, s) in enumerate(self.partitions):
            s.difference_update(isolates)
            if len(s) == 0:
                logger.error(f"Partition {ix}: {path[ix]} went to zero length!")
        start_parse = time.time()
        self.parses = self.get_parses_dc()
        end_parse = time.time()
        self.check_parse_validity()
        end_check = time.time()
        self.parses, self.parse_costs = _order_parses(self.parses)
        logger.info(f"Time for parse: {(end_parse-start_parse):1.6f}s")
        logger.info(f"Total for Global Check: {(end_check-end_parse):1.6f}s")
        logger.info(f"Total Time for parse: {(end_check-start_parse):1.6f}s")

    def __iter__(self):
        ''' Iterate over nodes '''
        return self.G.__iter__()

    def __str__(self):
        """ Print representation of DAG """
        return str(self.G)

    def lock(self):
        self.isLocked = True

    def add_node(self, node):
        """ Extend dag with node inserted at root

            Params:
                Node (VakyaGraphNode)      : Node to add
        """
        assert node not in self.G
        assert not self.isLocked
        self.G.add_node(node)

    def add_edges(self):
        assert self.isLocked
        laks = self.find_lakaras()
        krts = self.find_krtverbs()
        bases = []
        bases.extend(laks)
        bases.extend(krts)
        logger.debug("Processing Conjuctions")
        self.add_conjunctions(bases)  # Needs to happen before kAraka
        logger.debug("Adding Edges")
        self.add_karakas(bases)
        self.add_samastas()
        self.add_shashthi()
        self.add_kriyavisheshana(bases)  # FIXME Parallel edge problem
        self.add_visheshana()
        self.add_kriya_kriya(laks, krts)
        self.add_avyayas(bases)
        self.add_bhavalakshana(krts, laks)
        self.add_non_karaka_vibhaktis()
        self.add_vipsa()
        self.add_sentence_conjunctions(laks, krts)

    def find_krtverbs(self):
        ''' Find non ti~Nanta verbs'''
        rlist = []
        for n in self.G:
            if n.node_is_a(krtverbs):
                logger.debug(f"{n} is a possible Krt Dhatu")
                rlist.append(n)
        return rlist

    def find_lakaras(self):
        ''' Find the ti~Nanta '''
        rlist = []
        for n in self.G:
            if n.node_is_a(lakaras):
                logger.debug(f"{n} is a possible Dhatu")
                rlist.append(n)
        return rlist

    def add_visheshana(self):
        for n in self.G:
            if n.node_is_a(vibhaktis):
                for no in self.G:
                    if (not _is_same_partition(n, no)) and match_linga_vacana_vibhakti(n, no):
                        if _get_base(n) != _get_base(no):
                            logger.debug(f"Adding viSezaRa edge: {n,no}")
                            self.G.add_edge(n, no, label="viSezaRam")

    def add_vipsa(self):
        for n in self.G:
            for no in self.G:
                if (n.index == (no.index-1)) and \
                   (n.pada.canonical() == no.pada.canonical()):
                    logger.debug(f"Adding vIpsa edge: {n, no}")
                    self.G.add_edge(n, no, label="vIpsA")

    def add_samastas(self):
        ''' Add samasta links from next samasta/tiN '''
        for (i, s) in enumerate(self.partitions):
            for n in s:
                # If node is a samasta, check options for
                # next node, and add samasta links if tiN
                if n.node_is_a(samastas):
                    # Cant have samasta as last node
                    if i < (len(self.partitions)-1):
                        nextset = self.partitions[i+1]
                        for nn in nextset:
                            if nn.node_is_a(vibhaktis) or \
                               nn.node_is_a(samastas):
                                logger.debug(f"Adding samasta edge: {n,nn}")
                                self.G.add_edge(nn, n, label="samasta")

    def add_shashthi(self):
        ''' Add zazWI-sambanDa links to next tiN '''
        for (i, s) in enumerate(self.partitions):
            for n in s:
                # If node is a shashthi, check
                # next node, and add links if tiN
                if n.node_is_a(shashthi):
                    # Cant have sambandha open at last node
                    if i < (len(self.partitions)-1):
                        nextset = self.partitions[i+1]
                        for nn in nextset:
                            if nn.node_is_a(vibhaktis) or \
                               nn.node_is_a(samastas):
                                logger.debug(f"Adding shashthi-sambandha edge: {n,nn}")
                                self.G.add_edge(nn, n, label="zazWI-sambanDa")

    def add_karakas(self, bases):
        ''' Add karaka edges from base node (dhatu) base '''
        for d in bases:
            logger.debug(f"Processing {d}")
            dh = _get_base(d).canonical()
            hpos = dh.find("#")
            if hpos != -1:
                dh = dh[:hpos]
            if d.node_is_a(lakaras) or d.node_is_a('avyayaDAturUpa'):
                is_sak = dw.is_sakarmaka(dh)
                is_dvik = dw.is_dvikarmaka(dh)
            else:
                is_sak = True  # No way of knowing, set True
                is_dvik = False
            logger.debug(f"Dhatu: {dh} Sakarmaka {is_sak} Dvikarmaka {is_dvik}")
            if d.node_is_a(karmani):
                logger.debug("Karmani")
            else:
                logger.debug("Kartari")
                if d.node_is_a(nijanta):
                    logger.info("Nijanta Dhatu")
            for n in self.G:
                if not _is_same_partition(d, n):
                    if d.node_is_a(karmani):
                        if n.node_is_a(tritiya):
                            if d.node_is_a(nijanta):
                                logger.debug(f"Adding hetu-kartA edge to {n}")
                                self.G.add_edge(d, n, label="hetu-kartA")
                            logger.debug(f"Adding kartA edge to {n}")
                            self.G.add_edge(d, n, label="kartA")
                        elif (n.node_is_a(prathama) and match_purusha_vacana(d, n)
                              and d.node_is_a(lakaras) and is_sak):
                            # Only Lakaras and kartari krts are allowed
                            # Karma
                            logger.debug(f"Adding karma edge to {n}")
                            self.G.add_edge(d, n, label="karma")
                            if is_dvik:
                                logger.debug(f"Adding gauRakarma edge to {n}")
                                self.G.add_edge(d, n, label="gauRa-karma")
                    else:
                        if n.node_is_a(prathama) and d.node_is_a(lakaras) and match_purusha_vacana(d, n):
                            if d.node_is_a(nijanta):
                                logger.debug(f"Adding hetu-kartA edge to {n}")
                                self.G.add_edge(d, n, label="hetu-kartA")
                            else:
                                logger.debug(f"Adding kartA edge to {n}")
                                self.G.add_edge(d, n, label="kartA")
                        elif n.node_is_a(tritiya) and d.node_is_a(nijanta):
                            logger.debug(f"Adding kartA edge to {n}")
                            self.G.add_edge(d, n, label="kartA")
                        elif (n.node_is_a(dvitiya) and is_sak):
                            # Lakaras and Kartari krts are allowed
                            # Karma
                            logger.debug(f"Adding karma edge to {n}")
                            self.G.add_edge(d, n, label="karma")
                            if is_dvik:
                                logger.debug(f"Adding gauRakarma edge to {n}")
                                self.G.add_edge(d, n, label="gauRa-karma")
                    if n.node_is_a(tritiya):
                        logger.debug(f"Adding karana edge to {n}")
                        self.G.add_edge(d, n, label="karaRam")
                    elif n.node_is_a(chaturthi):
                        logger.debug(f"Adding sampradana edge to {n}")
                        self.G.add_edge(d, n, label="sampradAnam")
                    elif n.node_is_a(pancami):
                        logger.debug(f"Adding apadana edge to {n}")
                        self.G.add_edge(d, n, label="apAdanam")
                    elif n.node_is_a(saptami):
                        logger.debug(f"Adding adhikarana edge to {n}")
                        self.G.add_edge(d, n, label="aDikaraRam")
                    elif n.node_is_a(sambodhana) and check_sambodhya(d, n):
                        logger.debug(f"Adding sambodhya edge to {n}")
                        self.G.add_edge(d, n, label="samboDyam")

    def add_kriyavisheshana(self, bases):
        ''' Add kriyaviSezaRa edges from base node (dhatu) base '''
        for d in bases:
            for n in self.G:
                if not _is_same_partition(d, n):
                    if n.node_is_a(avyaya) and \
                         (n.node_is_a(kriyavisheshana) or
                          _get_base(n) in avyaya_kriyav):
                        logger.debug(f"Adding kriyAviSezaRa edge to {n}")
                        self.G.add_edge(d, n, label="kriyAviSezaRam")

    def add_kriya_kriya(self, lakaras, krts):
        ''' Add kriya-kriya edges from lakaras to krts'''
        for d in lakaras:
            for n in krts:
                if not _is_same_partition(d, n):
                    if n.node_is_a(purvakala):
                        logger.debug(f"Adding pUrvakAlaH edge to {n}")
                        self.G.add_edge(d, n, label="pUrvakAlaH")
                    elif n.node_is_a('tumun'):
                        logger.debug(f"Adding prayojanam edge to {n}")
                        self.G.add_edge(d, n, label="prayojanam")
                    elif n.node_is_a(samanakala) and n.node_is_a(prathama) and match_purusha_vacana(d, n):
                        logger.debug(f"Adding samAnakAlaH edge to {n}")
                        self.G.add_edge(d, n, label="samAnakAlaH")

    def add_conjunctions(self, bases):
        ''' Add samuccita links for conjunctions/disjunctions '''
        # First pass, add samuccitam edges
        for (i, s) in enumerate(self.partitions):
            for n in s:
                if n.node_is_a(avyaya) and ((_get_base(n) in conjunctions) or (_get_base(n) in disjunctions)):
                    # Add samuccitam to previous node
                    prevset = self.partitions[i-1]
                    for nn in prevset:
                        if nn.node_is_a(vibhaktis):
                            logger.info(f"Adding samuccitam edge: {n,nn}")
                            self.G.add_edge(n, nn, label="samuccitam")
                            vibhakti = nn.get_vibhakti()
                            n.setTags(vibhakti)  # Keep as strings for now since we may delete this
                            logger.debug(f'Node with temporary vibhakti {n}')
                            ni = i-2
                            while ni >= 0:
                                ppset = self.partitions[ni]
                                isconj = False
                                for nnn in ppset:
                                    # logger.info(f'Node in partition {ni} {nnn}')
                                    if nnn.get_vibhakti() == vibhakti:
                                        # if further previous node is the same conjunction, add samuccitam to that and stop
                                        if (ni == (i-2)) and nnn.node_is_a(avyaya) and _get_base(n) == _get_base(nnn):
                                            logger.info(f"Adding samuccitam edge to conj/disjunction: {nn,nnn}")
                                            self.G.add_edge(nn, nnn, label="samuccitam")
                                            isconj = True
                                        elif not ((_get_base(nnn) in conjunctions) or (_get_base(nnn) in disjunctions)):
                                            # Else, If further previous nodes are the same vibhakti, add samuccitam to those
                                            logger.info(f"Adding samuccitam edge to similar vibhakti: {n,nnn}")
                                            self.G.add_edge(n, nnn, label="samuccitam")
                                # Force exit from while loop if we hit another conjuction/disjunction
                                # FIXME: unclear how to handle the case where ca/uta/vA can refer to objects (sattva), ignoring
                                if isconj:
                                    break
                                else:
                                    ni = ni - 1
                        elif nn.node_is_a(lakaras):
                            logger.info(f"Adding samuccitam edge: {n,nn}")
                            self.G.add_edge(n, nn, label="samuccitam")
                            lakara = nn.get_lakara()
                            puruza = nn.get_purusha()
                            vacana = nn.get_vacana()
                            n.setTags(lakara | puruza | vacana)  # Keep as strings for now since we may delete this
                            logger.debug(f'Node with temporary lakara {n}')
                            ni = i-2
                            while ni >= 0:
                                ppset = self.partitions[ni]
                                isconj = False
                                for nnn in ppset:
                                    # logger.info(f'Node in partition {ni} {nnn}')
                                    if (nnn.get_lakara() == lakara) and match_purusha_vacana(nnn, nn):
                                        # if further previous node is the same conjunction, add samuccitam to that and stop
                                        if (ni == (i-2)) and nnn.node_is_a(avyaya) and _get_base(n) == _get_base(nnn):
                                            logger.info(f"Adding samuccitam edge to conj/disjunction: {nn,nnn}")
                                            self.G.add_edge(nn, nnn, label="samuccitam")
                                            isconj = True
                                        elif not ((_get_base(nnn) in conjunctions) or (_get_base(nnn) in disjunctions)):
                                            # Else, If further previous nodes are the same vibhakti, add samuccitam to those
                                            logger.info(f"Adding samuccitam edge to similar lakara: {n,nnn}")
                                            self.G.add_edge(n, nnn, label="samuccitam")
                                # Force exit from while loop if we hit another conjuction/disjunction
                                # FIXME: unclear how to handle the case where ca/uta/vA can refer to objects (sattva), ignoring
                                if isconj:
                                    break
                                else:
                                    ni = ni - 1

        # Second pass, remove vibhaktis
        for (i, s) in enumerate(self.partitions):
            for n in s:
                if n.node_is_a(avyaya) and ((_get_base(n) in conjunctions) or (_get_base(n) in disjunctions)):
                    # We would have set a vibhakti or lakara string
                    v = n.get_vibhakti()
                    lk = n.get_lakara()
                    vc = n.get_vacana()
                    p = n.get_purusha()
                    for e in self.G.in_edges(n, data=True):  # Note: keys=False
                        if e[2]['label'] == 'samuccitam':
                            if v:
                                logger.debug(f'removing vibhakti {v} from {n}')
                                n.deleteTags(v)
                                logger.debug(f'removed  vibhakti {v} from {n}')
                            if lk:
                                logger.debug(f'removing lakara {lk | vc | p} from {n}')
                                n.deleteTags(lk | vc | p)
                                logger.debug(f'removed  lakara {lk | vc | p} from {n}')
                    # Still there!
                    if lk and n.node_is_a(lk):  # Lakara need not be set
                        # logger.info(f'Node before lakara locked {n}')
                        n.deleteTags(lk | vc | p | v)
                        # n.setTags(set([SanskritObject(_v, SLP1) for _v in list(lk | vc | p)]))
                        logger.info(f'Node with lakara removed {n}')
                    elif v and n.node_is_a(v):
                        n.deleteTags(v)
                        n.setTags(set([SanskritObject(_v, SLP1) for _v in list(v)]))
                        logger.info(f'Node with vibhakti locked {n}')
                        # Compute vacanam and lingam: Conjunctions
                        is_conj = (_get_base(n) in conjunctions)
                        vacana = ''
                        linga = 'strIliNgam'

                        def _vacana(v1, v2, is_conj=True):
                            logger.debug(f'{v1, v2, is_conj}')
                            if is_conj:
                                if v1 == 'ekavacanam' and v2 == 'ekavacanam':
                                    return 'dvivacanam'
                                else:
                                    return 'bahuvacanam'
                            else:
                                if v1 == 'ekavacanam' and v2 == 'ekavacanam':
                                    return 'ekavacanam'
                                elif v1 == 'bahuvacanam' or v2 == 'bahuvacanam':
                                    return 'bahuvacanam'
                                else:
                                    return 'dvivacanam'

                        def _linga(l1, l2):
                            logger.debug(f'{l1,l2}')
                            if l1 == 'napuMsakaliNgam' or l2 == 'napuMsakaliNgam':
                                return 'napuMsakaliNgam'
                            elif l1 == 'puMlliNgam' or l2 == 'puMlliNgam':
                                return 'puMlliNgam'
                            else:
                                return 'strIliNgam'

                        # Depth first (we only get samuccitam edges)
                        for (nn, sl) in nx.dfs_successors(self.G, source=n).items():
                            for s in sl:
                                logger.info(f'DFS {s} from {nn} root {n}')
                                _v = s.get_vacana()
                                _l = s.get_linga()
                                if vacana == '':
                                    vacana = list(_v)[0]
                                elif _v:
                                    vacana = _vacana(vacana, list(_v)[0], is_conj)
                                if _l:
                                    linga = _linga(linga, list(_l)[0])
                        n.setTags({SanskritObject(vacana, SLP1), SanskritObject(linga, SLP1)})
                        logger.info(f'Node with vacana/linga locked {n}')

    def add_avyayas(self, bases):
        ''' Add Avyaya Links '''
        # Upasargas
        for (i, s) in enumerate(self.partitions):
            for n in s:
                if n.node_is_a('upasargaH'):
                    # Cant have upasargas at last node
                    if i < (len(self.partitions)-1):
                        nextset = self.partitions[i+1]
                        # Upasarga to upasarga links ok
                        # Upasarga to any verb form barring ktvA
                        for nn in nextset:
                            if ((nn in bases) and not nn.node_is_a('ktvA')) or \
                               nn.node_is_a('upasargaH'):
                                logger.debug(f"Adding upasarga edge: {n,nn}")
                                self.G.add_edge(nn, n, label="upasargaH")
                elif n.node_is_a(avyaya) and (_get_base(n) in nishedha):
                    for b in bases:
                        if not _is_same_partition(n, b):
                            logger.debug(f"Adding nishedha edge: {n, b}")
                            self.G.add_edge(b, n, label="nizeDa")
                elif n.node_is_a('karmapravacanIyaH') and not (_get_base(n) in avyaya_kriyav) and not(_get_base(n) in karmap_null):
                    for b in bases:
                        if not _is_same_partition(n, b):
                            logger.debug(f"Adding karmapravacaniya edge: {n, b}")
                            self.G.add_edge(b, n, label="karmapravacanIyaH")
                    if i < (len(self.partitions)-1):
                        nextset = self.partitions[i+1]
                    else:
                        nextset = set([])
                    if i > 0:
                        prevset = self.partitions[i-1]
                    else:
                        prevset = set([])
                    for nn in nextset.union(prevset):
                        if nn.node_is_a(dvitiya) and (_get_base(n) in karmap_2):
                            logger.debug(f"Adding karmapravacaniya upapada 2 edge: {n,nn}")
                            self.G.add_edge(n, nn, label="upapada-dvitIyA")
                        elif nn.node_is_a(pancami) and (_get_base(n) in karmap_5):
                            logger.debug(f"Adding karmapravacaniya upapada 5 edge: {n,nn}")
                            self.G.add_edge(n, nn, label="upapada-pancamI")

    def add_bhavalakshana(self, krts, laks):
        ''' Add bhavalakshana edges from saptami krts to lakaras '''
        for k in krts:
            if k.node_is_a(saptami):
                for lak in laks:
                    if not _is_same_partition(k, lak):
                        logger.debug(f"Adding Bhavalakshana edge: {k, lak}")
                        self.G.add_edge(lak, k, label="BAvalakzaRam")

    def add_non_karaka_vibhaktis(self):
        ''' Add Non-Karaka Vibhaktis '''
        for n in self.G:
            nb = _get_base(n)
            for ix in range(7):
                if (ix+1 in non_karaka_vibhaktis) and \
                   (nb in non_karaka_vibhaktis[ix+1]):
                    for nn in self.G:
                        vlabel = ("upapada-"+_vibhaktis[ix]).replace("viBakti", "")
                        if nn.node_is_a(_vibhaktis[ix]) and \
                           (not _is_same_partition(nn, n)):
                            logger.debug(f"Adding {vlabel} edge {nn, n}")
                            self.G.add_edge(n, nn, label=vlabel)

    def add_sentence_conjunctions(self, laks, krts):
        ''' Add sentence conjunction links

        For all nodes which match sentence_conjuction keys
        add vAkyasambanDaH link between y-t pair (if vibhakti matches where relevant)
        Reverse all edges to node, add sambadDa- to link label (eg sambadDa-karma, if node is not vIpsa
        if node is saMyojakaH, and not vIpsA add saMbadDakriyA links to verbs
        if associated t* doesn't exist vAkyasambanDaH links from verbs
        '''
        def _is_vipsa(n):
            for p, kd in self.G.pred[n].items():
                # Multigraph
                for k, d in kd.items():
                    if d['label'] == 'vIpsA':
                        return True
            return False
        # Only prathama krts are needed here. The rest aren't relevant
        bases = []
        bases.extend(laks)
        bases.extend([n for n in krts if n.node_is_a(prathama)])
        sentence_conjunctions_y = set(sentence_conjunctions.keys())
        for n in self.G:
            nb = _get_base(n)
            if nb in sentence_conjunctions_y:
                if not _is_vipsa(n):
                    # Reverse edges, add sambadDa label
                    # for MG, G.pred[n].items() is an iterator of (node, edgeitem) pairs
                    for p, kd in list(self.G.pred[n].items()):
                        # edgeitem.items() is an iterator of num, dict pairs
                        for k, d in list(kd.items()):
                            # self.G.remove_edge(p, n)
                            if d['label'] == 'viSezaRam':
                                # Need to invert following edge as well
                                for p_p, p_kd in list(self.G.pred[p].items()):
                                    for p_k, p_d in list(p_kd.items()):
                                        # self.G.remove_edge(p, n)
                                        if p_d['label'][:9] != 'sambadDa-':
                                            self.G.add_edge(p, p_p, label='sambadDa-'+p_d['label'])
                            self.G.add_edge(n, p, label='sambadDa-'+d['label'])

                    # Matching pair
                    s_t = sentence_conjunctions[nb]
                    for nn in self.G:
                        if (not _is_vipsa(nn)) and (_get_base(nn) in s_t) and (not _is_same_partition(n, nn)):
                            if match_linga_vacana(n, nn):
                                logger.info(f"Adding vAkyasambanDaH edge: {nn, n}")
                                self.G.add_edge(nn, n, label="vAkyasambanDaH")
                        if n.node_is_a('saMyojakaH') and (nn in bases) and (not _is_same_partition(n, nn)):
                            logger.info(f"Adding saMbadDakriyA edge: {nn, n}")
                            self.G.add_edge(n, nn, label='saMbadDakriyA')
                            if None in s_t:
                                logger.info(f"Adding vAkyasambanDaH edge: {nn, n}")
                                self.G.add_edge(nn, n, label="vAkyasambanDaH")

    def get_parses_dc(self):
        ''' Returns all parses

            Uses modified Kruskal Algorithm to compute (generalized) spanning
            tree of k-partite VakyaGraph
        '''
        logger.debug("Computing Parses (Divide & Conquer)")

        def _get_parse_sub(mn, mx):
            # Iterate over subsets of disjoint nodesets
            for (i, ns) in enumerate(islice(self.partitions, mn, mx)):
                logger.debug(f"Node set number {i} {ns}")
                if i == 0:
                    # Partial parses = phi + all predecessors
                    partial_parses = set()
                    partial_parses.add(VakyaParse(None))  # Null partial parse
                    # For all input edges to this set
                    for n in ns:
                        logger.debug(f"Traversing node {n}")
                        for pred in self.G.predecessors(n):
                            logger.debug(f"Traversing predecessor {pred} -> {n}")
                            partial_parses.add(VakyaParse((pred, n)))
                else:
                    store_parses = set()
                    small_parses = set()
                    for ps in partial_parses:  # For each partial parse
                        if len(ps) < i:  # Small parses to be removed
                            small_parses.add(ps)
                        for n in ns:  # For all input edges to this set
                            logger.debug(f"Traversing node {n}")
                            for pred in self.G.predecessors(n):
                                logger.debug(f"Traversing predecessor {pred} -> {n}")
                                # If edge is compatible with partial parse, add and create new partial parse
                                logger.debug(f"Trying to extend parse {ps}")
                                if ps.is_safe(pred, n):
                                    logger.debug(f"{pred} - {n} is safe for {ps}")
                                    psc = ps.copy()  # Copy the nodeset and DisjointSet structures
                                    psc.extend(pred, n)
                                    if self.on_the_fly(psc):
                                        store_parses.add(psc)
                    partial_parses.difference_update(small_parses)
                    partial_parses.update(store_parses)
                logger.debug("Partial Parses")
                for p in partial_parses:
                    logger.debug(p)
            return partial_parses

        # Divide & Conquer routine
        def _dc(mn, mx):
            logger.info(f"Divide And Conquer {mn, mx}")
            if (mx - mn) > self.max_parse_dc:
                md = int((mx + mn)/2)
                return _merge_partials(_dc(mn, md), _dc(md, mx), mx, mn)
            else:
                t = _get_parse_sub(mn, mx)
                return t

        def _merge_partials(pp1, pp2, mx, mn):
            logger.info(f"Merging between {mn, mx} {len(pp1)} x {len(pp2)}")
            start_time = time.time()
            logger.debug(f"Merging {pp1, pp2}")
            ppmt = set()
            for ppa in pp1:
                for ppb in pp2:
                    if self.fast_merge:
                        if ppa.can_merge(ppb, mx-mn-1):
                            merged = ppa.merge_f(ppb)
                            if merged and self.on_the_fly(merged):
                                ppmt.add(merged)
                    else:  # Slow Merge
                        merged = ppa.merge_s(ppb, mx-mn-1)
                        if merged and self.on_the_fly(merged):
                            ppmt.add(merged)
            logger.debug(f"{len(ppmt)} parses")
            logger.debug(f"Merged {ppmt}")
            end_time = time.time()
            logger.info(f"Time for merge {end_time-start_time}")
            return ppmt

        partial_parses = _dc(0, self.path_node_count)
        logger.debug(f"Partial Parses Before Return {partial_parses}")
        # Multigraph: convert VakyaParse to subgraph
        return set([self.G.edge_subgraph(m) for p in partial_parses for m in multiedgesets(p, self.G)])

    def check_parse_validity(self):
        ''' Final Validity Check for parses

            Remove parses with double kArakas
            Remove parses with multiple to edges into a node
            Remove parses with cycles
        '''
        iv = set()
        logger.debug(f"Parses before validity check {len(self.parses)}")
        for p in self.parses:
            if not _check_parse(p):
                logger.debug(f"Will remove {p}")
                iv.add(p)  # Collect invalid parses
        # Remove them
        self.parses.difference_update(iv)
        logger.info(f"Parses after validity check {len(self.parses)}")

    def on_the_fly(self, p):
        ''' On-the-fly Validity Check for parses

            Remove parses with double kArakas
            Remove parses with multiple to edges into a node
            Remove parses with cycles
        '''
        # Have to convert VakyaParse to subgraph before checking
        # Note: could be multiple subgraphs for the same edge-set (parallel edges)
        parses = set([self.G.edge_subgraph(m) for m in multiedgesets(p, self.G)])
        return reduce(lambda x, y: x or _check_parse(y, on_the_fly=True), parses, False)

    def draw(self, *args, **kwargs):
        _ncache = {}

        def _uniq(s):
            if s not in _ncache:
                _ncache[s] = 0
                return s
            else:
                _ncache[s] = _ncache[s] + 1
                return s + "_" + str(_ncache[s])

        nx.draw(self.G, *args, **kwargs,
                pos=nx.graph_layout(self),
                labels={x: _uniq(str(x)) for x in self})

    def write_dot(self, path):
        nx.drawing.nx_pydot.write_dot(self.G, path)
        d = dirname(path)
        be = basename(path)
        b, e = splitext(be)
        logger.debug(f"Path {d} {b} {e}")
        for i, p in enumerate(self.parses):
            pt = join(d, b+f"_parse{i}"+e)
            nx.drawing.nx_pydot.write_dot(p, pt)

    def get_dot_dict(self):
        from io import StringIO
        s = StringIO()
        r = {}
        nx.drawing.nx_pydot.write_dot(self.G, s)
        r["split"] = s.getvalue()
        for i, p in enumerate(self.parses):
            s = StringIO()
            nx.drawing.nx_pydot.write_dot(p, s)
            r[i] = s.getvalue()
        return r


class VakyaGraphNode(object):
    """ Class for VakyaGraph nodes

        This has pada (a SanskritObject) plus a list of disjoint nodes
        to which edges cannot be created from this node
    """
    def __init__(self, sobj, index):
        self._pada = sobj
        self._index = index
        self._cache_str()

    @property
    def pada(self):
        return self._pada

    @pada.setter
    def _set_pada(self, pada):
        self._pada = pada
        self._cache_str()

    @property
    def index(self):
        return self._index

    @index.setter
    def _set_index(self, index):
        self._index = index
        self._cache_str()

    def _cache_str(self):
        ''' Cache the string representation for speedup.

            See https://github.com/kmadathil/sanskrit_parser/issues/160
        '''
        self._str = str(self._pada) + " " + str(self._pada.getMorphologicalTags()) + \
            " " + str(self._index)

    def getMorphologicalTags(self):
        return self._pada.getMorphologicalTags()

    def getNodeTagset(self):
        ''' Given a Node, extract the tagset '''
        return getSLP1Tagset(self.getMorphologicalTags())

    def deleteTags(self, t):
        self._pada.tags[1].difference_update(t)
        self._cache_str()
        return self

    def setTags(self, t):
        self._pada.tags[1].update(t)
        self._cache_str()
        return t

    def node_is_a(self, st):
        ''' Check if node matches a particular tag or any of a set of tags '''
        if isinstance(st, str):
            return st in self.getNodeTagset()
        elif isinstance(st, set):
            return not st.isdisjoint(self.getNodeTagset())
        else:
            logger.error(f"node_is_a: expecting str or set, got {st} of type {type(st)}")

    def get_vibhakti(self):
        ''' Get Node vacana '''
        return self.getNodeTagset().intersection(vibhaktis)

    def get_lakara(self):
        ''' Get Node vacana '''
        return self.getNodeTagset().intersection(lakaras)

    def get_vacana(self):
        ''' Get Node vacana '''
        return self.getNodeTagset().intersection(vacanas)

    def get_linga(self):
        ''' Get Node linga '''
        return self.getNodeTagset().intersection(lingas)

    def get_purusha(self):
        ''' Get Node puruza '''
        return self.getNodeTagset().intersection(puruzas)

    def __str__(self):
        return self._str

    def __repr__(self):
        return str(self)


class VakyaParse(object):
    def __init__(self, nodepair):
        ''' Initializes a partial parse with a node pair (or []) '''
        # DisjointSet  (as in Kruskal)
        self.connections = DisjointSet()
        # "Extinguished" nodes - nodes from partitions whose representatives
        # Have been added to the forest/ST already
        self.extinguished = set()
        # Nodes in the forest/ST
        self.activenodes = set()
        if nodepair is not None:
            self._populate(nodepair)
        else:
            # Edges in the forest/ST
            self.edges = set()

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str([(u.pada.canonical(), v.pada.canonical()) for (u, v) in self.edges])

    def _populate(self, nodepair):
        # Add first edge to forest
        self.edges = set([(nodepair[0], nodepair[1])])
        for n in nodepair:
            self.activate_and_extinguish_alternatives(n)
        self.connections.union(nodepair[0], nodepair[1])

    def activate_and_extinguish_alternatives(self, node):
        ''' Make node active, extinguish other nodes in its partition '''
        self.activenodes.add(node)
        self.extinguished.add(node.index)

    def is_extinguished(self, node):
        ''' Is a node extinguished '''
        return (node.index in self.extinguished) and \
            (node not in self.activenodes)

    def is_safe(self, pred, node):
        ''' Checks if a partial parse is compatible with a given node and predecessor pair '''
        if self.is_extinguished(pred) or self.is_extinguished(node):
            r = False
        elif (pred in self.activenodes) and (node in self.activenodes):
            r = not self.connections.connected(pred, node)
        else:
            r = True
        return r

    def extend(self, pred, node):
        ''' Extend current parse with edge from pred to node '''
        if not self.activenodes:
            logger.debug(f"Populating {self.edges} with {(pred,node)}")
            self._populate((pred, node))
        else:
            logger.debug(f"Extending {self.edges} with {(pred,node)}")
            if pred not in self.activenodes:
                self.activate_and_extinguish_alternatives(pred)
            if node not in self.activenodes:
                self.activate_and_extinguish_alternatives(node)
            self.edges.add((pred, node))
            self.connections.union(pred, node)
        logger.debug(f"Edges {self.edges}")

    def can_merge(self, other, length):
        ''' Can we merge two VakyaParses '''
        # Proper length
        if (len(other.edges) + len(self.edges)) < length:
            return False
        # No extinguished nodes
        for x in other.activenodes:
            if self.is_extinguished(x):
                return False
        conn = self.connections.copy()
        # No cycles
        for (u, v) in other.edges:
            if conn.connected(u, v):
                return False
            else:
                conn.union(u, v)
        return True

    def merge_f(self, other):
        ''' Merge two VakyaParses: Fast method '''
        t = self.copy()
        logger.debug("Merging")
        t.extinguished.update(other.extinguished)
        t.activenodes.update(other.activenodes)
        t.edges.update(other.edges)
        for (u, v) in other.edges:
            t.connections.union(u, v)
        return t

    def merge_s(self, other, length):
        ''' Merge two VakyaParses: Slow method '''
        # Proper length
        if (len(other.edges) + len(self.edges)) < length:
            return False
        t = self.copy()
        for (u, v) in other.edges:
            if t.is_safe(u, v):
                t.extend(u, v)
            else:
                return False
        return t

    def __len__(self):
        return len(self.edges)

    def copy(self):
        ''' Return a one level deep copy - in between a shallow and a fully deep copy '''
        t = VakyaParse(None)
        t.activenodes = copy(self.activenodes)
        t.edges = copy(self.edges)
        t.extinguished = copy(self.extinguished)
        t.connections = self.connections.copy()
        return t


def getSLP1Tagset(n):
    ''' Given a (base, tagset) pair, extract the tagset '''
    return set(map(lambda x: x if isinstance(x, str) else x.canonical(), list(n[1])))


def match_purusha_vacana(d, n):
    ''' Check vacana/puruza compatibility for a Dhatu d and node n '''
    n_base = _get_base(n)
    if n_base == 'asmad':
        n_purusha = set([puruzas[2]])
    elif n_base == 'yuzmad':
        n_purusha = set([puruzas[1]])
    else:
        n_purusha = set([puruzas[0]])
    return (d.get_vacana() == n.get_vacana()) and (d.get_purusha() == n_purusha)


def match_linga_vacana(n1, n2):
    ''' Check linga/puruza compatibility for two nodes '''
    return (n1.get_vacana() == n2.get_vacana()) and \
        (n1.get_linga() == n2.get_linga())


def match_linga_vacana_vibhakti(n1, n2):
    return (n1.get_vacana() == n2.get_vacana()) and \
        (n1.get_linga() == n2.get_linga()) and \
        (n1.get_vibhakti() == n2.get_vibhakti())


def check_sambodhya(d, n):
    ''' Check sambodhya compatibility for dhatu d and node n '''
    return (d.get_vacana() == n.get_vacana()) and \
        (d.get_purusha() == set([puruzas[1]]))


def jedge(pred, node, label, strict_io=False):
    return (node.pada.canonical(strict_io=strict_io),
            jtag(node.getMorphologicalTags(), strict_io),
            SanskritImmutableString(label, encoding=SLP1).canonical(strict_io=strict_io),
            pred.pada.canonical(strict_io=strict_io))


def jnode(node, strict_io=False):
    """ Helper to translate parse node into serializable format"""
    return (node.pada.canonical(strict_io=strict_io),
            jtag(node.getMorphologicalTags(), strict_io), "", "")


def jtag(tag, strict_io=False):
    """ Helper to translate tag to serializable format"""
    return (tag[0].canonical(strict_io=strict_io), [t.canonical(strict_io=strict_io) for t in list(tag[1])])


def _non_projective(u, v, w, x):
    """ Checks if an edge pair is non-projective """
    mnu = min(u, v)
    mxu = max(u, v)
    mnw = min(w, x)
    mxw = max(w, x)
    if mnu < mnw:
        return (mxu < mxw) and (mxu > mnw)
    elif mxu > mxw:
        return (mnu > mnw) and (mnu < mxw)


def _is_same_partition(n1, n2):
    ''' Are the two nodes n1 and n2 are in the same partition in psets '''
    return n1.index == n2.index


def _get_base(n):
    return n.getMorphologicalTags()[0]


def _order_parses(pu):
    '''
        Order a set of parses by weight.
        '''
    # Sigma abs(n1-n2)
    def _parse_cost(parse):
        w = 0
        # Multigraph (keys=False)
        for (u, v, l) in parse.edges(data='label'):
            if l in edge_cost_const:
                _w = edge_cost[l]
            else:
                # Abs Edge length times edge_type cost
                _w = abs(u.index - v.index) * edge_cost[l]
            if u.node_is_a(lakaras):
                # Lakaras are preferred
                _w = 0.9 * _w
            w = w + _w
        return round(w, 3)
    t = sorted(pu, key=_parse_cost)
    return t, [_parse_cost(te) for te in t]


# Check a parse for validity
def _check_parse(parse, on_the_fly=False):
    r = True
    smbds = samplabels
    count = defaultdict(lambda: defaultdict(int))
    edges = {}
    toedge = defaultdict(int)
    fromv = defaultdict(int)
    tov = defaultdict(int)
    sk = defaultdict(int)
    vsmbd = {}
    vsmbd_t = {}
    conj = defaultdict(lambda: {"from": 0, "to": 0})
    sckeys = set(sentence_conjunctions.keys())

    # Multigraph (keys=False)
    for (u, v, l) in parse.edges(data='label'):
        if l in karakas:
            count[u][l] = count[u][l]+1
            toedge[v] = toedge[v]+1
        if l in ['sambadDa-'+x for x in karakas]:
            ll = l[9:]  # Strip off sambadDa-
            ll = l.replace('sambadDa-', '')  # Strip off sambadDa-
            # Cant have x and sambadDa-x to the same dhAturUpa
            # Note that sambadDa-x arcs are reversed
            count[v][ll] = count[v][ll]+1
            toedge[v] = toedge[v]+1
        if l in 'viSezaRam':
            fromv[u] = fromv[u] + 1
            tov[v] = tov[v] + 1
        if l in projlabels:  # Labels with sannidhi expectation
            edges[(u.index, v.index)] = 1
        if l in smbds:
            sk[u] = sk[u] + 1
        if l in 'vAkyasambanDaH':
            vsmbd[u.index] = v.index
            vsmbd[v.index] = u.index
            vsmbd_t[v.index] = True
        # Conjuction nodes must have in and out edges
        if _get_base(u) in sckeys:
            conj[u]["from"] = conj[u]["from"] + 1
        if _get_base(v) in sckeys:
            conj[v]["to"] = conj[v]["to"] + 1

    for u in count:  # Dhatu
        for k in count[u]:  # Each karaka should count only once
            if count[u][k] > 1:
                logger.debug(f"Count for {u} {k} is {count[u][k]} - violates constraint")
                return False
    for (ui, vi) in edges:
        for (wi, xi) in edges:
            if _non_projective(ui, vi, wi, xi):  # Non-projective
                logger.debug(f"Sannidhi violation {ui} - {vi} : {wi} - {xi}")
                return False
    for v in toedge:
        if toedge[v] > 1:
            logger.debug(f"Toedges for {v} is {toedge[v]} - violates constraint")
            return False
    for u in sk:   # Sambaddhakaraka = only one allowed from node
        if sk[u] > 1:
            logger.debug(f"Sambaddha karaka edges for {u} is {sk[u]} - violates  constraint")
            return False
    for v in tov:
        if v in fromv:
            logger.debug(f"Viseshana has visheshana {v} - violates constraint")
            return False
    # Vakyasambabdha nodes - yadi/tarhi yatra/tatra etc cannot have links
    # beyond their partner
    # Multigraph (keys=False)
    for (u, v, l) in parse.edges(data='label'):
        if u.index in vsmbd:
            if ((vsmbd[u.index] > u.index) and (v.index > vsmbd[u.index])) or \
               ((vsmbd[u.index] < u.index) and (v.index < vsmbd[u.index])):
                logger.debug(f"Sannidhi violation for vAkyasambadDa {u.index} - {v.index} {l} : {u} {vsmbd[u.index]}")
                return False
        if v.index in vsmbd:
            if ((vsmbd[v.index] > v.index) and (u.index > vsmbd[v.index])) or \
               ((vsmbd[v.index] < v.index) and (u.index < vsmbd[v.index])):
                logger.debug(f"Sannidhi violation for vAkyasambadDa {u.index} - {v.index} {l} : {v} {vsmbd[v.index]}")
                return False
        if (not on_the_fly) and (u.index not in vsmbd_t) and l[:9] == 'sambadDa-':
            logger.debug(f"SambadDa edge from non vAkyasambanDa node {u.index} - {v.index}: {l}")
            return False

    # Conjunctions have to have one to and from edge
    if (not on_the_fly):
        for u in conj:
            if (conj[u]["from"] != 1) or (conj[u]["to"] != 1):
                logger.debug(f"Samyojaka violation for {u.index} {conj[u]}")
                return False
    return r


# Multigraph
def multiedgesets(p, G):
    medges = []
    for e in p.edges:
        medges.append([(e[0], e[1], k) for k in G[e[0]][e[1]]])
    return [list(x) for x in product(*medges)]
