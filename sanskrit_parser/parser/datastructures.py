#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
""" Sanskrit Parser Data Structures

    @author: Karthik Madathil (github: @kmadathil)
"""

import sanskrit_parser.base.sanskrit_base as SanskritBase
import networkx as nx
from itertools import islice
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

__all__ = ['SandhiGraph', 'VakyaGraph', 'getSLP1Tagset']

dw = DhatuWrapper()


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _console_logging():
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logger.addHandler(console)


_console_logging()


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
        nx.drawing.nx_agraph.write_dot(self.G, path)


lakaras = set(['law', 'liw', 'luw', 'lrw', 'low', 'laN', 'liN', 'luN', 'lfN',
               'viDiliN', 'ASIrliN'])
karmani = set(['karmaRi'])
samastas = set(['samAsapUrvapadanAmapadam'])
# Vibhaktis
_vibhaktis = ['praTamAviBaktiH', 'dvitIyAviBaktiH', 'tftIyAviBaktiH',
              'caturTIviBaktiH', 'paNcamIviBaktiH', 'zazWIviBaktiH',
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
karakas = set(['kartA', 'karma', 'karaRa', 'apAdAna', 'sampradAna', 'aDikaraRa'])
predicative_verbs = set(['as', 'BU', 'vft'])
_lingas = ['puMlliNgam', 'napuMsakaliNgam', 'strIliNgam', 'triliNgam']
lingas = set(_lingas)
napumsakam = _lingas[1]


class VakyaGraph(object):
    """ DAG class for Sanskrit Vakya Analysis

        Represents Sanskrit Vakya Analysis as a DAG
        Nodes are SanskritObjects with morphological tags
        Edges are potential relationships between them
    """
    def __init__(self, path, max_parse_dc=4):
        ''' DAG Class Init

        Params:
             path: Path from SanghiGraph
        '''
        self.max_parse_dc = max_parse_dc
        self.roots = []
        self.isLocked = False
#        self.G = nx.MultDiGraph() # Allow parallel edges
        self.G = nx.DiGraph()
        # Need this many nodes in the extracted subgraphs
        self.path_node_count = len(path)
        logger.info(f"{self.path_node_count} sets of orthogonal nodes")
        self.nsets = DisjointSet()
        for (ix, sobj) in enumerate(path):
            vnlist = []
            mtags = sobj.getMorphologicalTags()
            for mtag in mtags:
                ncopy = SanskritBase.SanskritObject(sobj.canonical(),
                                                    encoding=SanskritBase.SLP1,
                                                    replace_ending_visarga=None)
                ncopy.setMorphologicalTags(mtag)
                pn = VakyaGraphNode(ncopy)
                vnlist.append(pn)
            for vn in vnlist:
                self.add_node(vn)
            self.nsets.addset(set(vnlist))
        logger.debug(f"Node sets {self.nsets} Len {len(self.nsets)}")
        self.lock()
        self.add_edges()
        # Remove isolated nodes (with no edges)
        isolates = list(nx.isolates(self.G))
        self.G.remove_nodes_from(isolates)
        self.nsets.remove(isolates)
        start_parse = time.time()
        self.parses = self.get_parses_dc()
        self.check_parse_validity()
        end_parse = time.time()
        logger.info(f"Time for parse: {(end_parse-start_parse):1.6f}s")

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
        bases = self.find_dhatu()
        logger.info("Adding Edges")
        self.add_karakas(bases)
        self.add_samastas()
        self.add_shashthi()
#       self.add_kriyavisheshana(bases) FIXME Parallel edge problem
        self.add_visheshana()

    def find_dhatu(self):
        ''' Find the ti~Nanta '''
        rlist = []
        for n in self.G:
            if n.node_is_a(lakaras):
                logger.info(f"{n} is a possible Dhatu")
                rlist.append(n)
        return rlist

    def add_visheshana(self):
        for n in self.G:
            if n.node_is_a(vibhaktis):
                for no in self.G:
                    if (not self.nsets.connected(n, no)) and match_linga_vacana_vibhakti(n, no):
                        logger.debug(f"Adding viSezaRa edge: {n,no}")
                        self.G.add_edge(n, no, label="viSezaRa")

    def add_samastas(self):
        ''' Add samasta links from next samasta/tiN '''
        for (i, s) in enumerate(self.nsets):
            for n in s:
                # If node is a samasta, check options for
                # next node, and add samasta links if tiN
                if n.node_is_a(samastas):
                    # Cant have samasta as last node
                    if i < (len(self.nsets)-1):
                        nextset = self.nsets[i+1]
                        for nn in nextset:
                            if nn.node_is_a(vibhaktis) or \
                               nn.node_is_a(samastas):
                                logger.debug(f"Adding samasta edge: {n,nn}")
                                self.G.add_edge(nn, n, label="samasta")

    def add_shashthi(self):
        ''' Add zazWI-sambanDa links to next tiN '''
        for (i, s) in enumerate(self.nsets):
            for n in s:
                # If node is a shashthi, check
                # next node, and add links if tiN
                if n.node_is_a(shashthi):
                    # Cant have sambandha open at last node
                    if i < (len(self.nsets)-1):
                        nextset = self.nsets[i+1]
                        for nn in nextset:
                            if nn.node_is_a(vibhaktis) or \
                               nn.node_is_a(samastas):
                                logger.debug(f"Adding shashthi-sambandha edge: {n,nn}")
                                self.G.add_edge(nn, n, label="zazWI-sambanDa")

    def add_karakas(self, bases):
        ''' Add karaka edges from base node (dhatu) base '''
        for d in bases:
            logger.debug(f"Processing {d}")
            dh = d.getMorphologicalTags()[0]
            hpos = dh.find("#")
            if hpos != -1:
                dh = dh[:hpos]
            logger.debug(f"Dhatu: {dh} Sakarmaka {dw.is_sakarmaka(dh)}")
            if d.node_is_a(karmani):
                logger.debug("Karmani")
                karta = tritiya
                karma = prathama
            else:
                logger.debug("Kartari")
                karta = prathama
                karma = dvitiya
            for n in self.G:
                if not self.nsets.connected(d, n):
                    if n.node_is_a(karta):
                        if match_purusha_vacana(d, n):
                            logger.debug(f"Adding kartA edge to {n}")
                            self.G.add_edge(d, n, label="kartA")
                        elif dh in predicative_verbs:
                            logger.debug(f"Adding kartfsamAnADikaraRa edge to {n}")
                            self.G.add_edge(d, n, label="kartfsamAnADikaraRa")
                    elif n.node_is_a(karma) and dw.is_sakarmaka(dh):
                        logger.debug(f"Adding karma edge to {n}")
                        self.G.add_edge(d, n, label="karma")
                    elif n.node_is_a(tritiya):
                        logger.debug(f"Adding karana edge to {n}")
                        self.G.add_edge(d, n, label="karaRa")
                    elif n.node_is_a(chaturthi):
                        logger.debug(f"Adding sampradana edge to {n}")
                        self.G.add_edge(d, n, label="sampradAna")
                    elif n.node_is_a(pancami):
                        logger.debug(f"Adding apadana edge to {n}")
                        self.G.add_edge(d, n, label="apAdana")
                    elif n.node_is_a(saptami):
                        logger.debug(f"Adding adhikarana edge to {n}")
                        self.G.add_edge(d, n, label="aDikaraRa")
                    elif n.node_is_a(sambodhana) and check_sambodhya(d, n):
                        logger.debug(f"Adding sambodhya edge to {n}")
                        self.G.add_edge(d, n, label="samboDya")

    def add_kriyavisheshana(self, bases):
        ''' Add kriyaviSezaRa edges from base node (dhatu) base '''
        for d in bases:
            for n in self.G:
                if not self.nsets.connected(d, n):
                    if n.node_is_a(prathama) and n.node_is_a(napumsakam):
                        logger.debug(f"Adding kriyAviSezaRa edge to {n}")
                        self.G.add_edge(d, n, label="kriyAviSezaRa")

    def get_parses_dc(self):
        ''' Returns all parses
        '''
        logger.debug("Computing Parses (Divide & Conquer)")

        def _get_parse_sub(mn, mx):
            # Iterate over subsets of disjoint nodesets
            for (i, ns) in enumerate(islice(self.nsets, mn, mx)):
                logger.debug(f"Node set number {i} {ns}")
                if i == 0:
                    # Partial parses = phi + all predecessors
                    partial_parses = set()
                    partial_parses.add(VakyaParse(None, self.nsets, self.G))  # Null partial parse
                    # For all input edges to this set
                    for n in ns:
                        logger.debug(f"Traversing node {n}")
                        for pred in self.G.predecessors(n):
                            logger.debug(f"Traversing predecessor {pred} -> {n}")
                            partial_parses.add(VakyaParse((pred, n), self.nsets, self.G))
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
                                if not ps.is_discordant(pred, n):
                                    logger.debug(f"{pred} - {n} is non-discordant with {ps}")
                                    psc = ps.copy()  # Copy the nodeset and DisjointSet structures
                                    psc.extend(pred, n)
                                    store_parses.add(psc)
                    partial_parses.difference_update(small_parses)
                    partial_parses.update(store_parses)
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
            logger.info(f"Merging between {mn, mx}")
            start_time = time.time()
            logger.debug(f"Merging {pp1, pp2}")
            ppmt = set()
            for ppa in pp1:
                for ppb in pp2:
                    if ppa.can_merge(ppb, mx-mn-1):
                        ppmt.add(ppa.merge(ppb))
            logger.debug(f"Merged {ppmt}")
            end_time = time.time()
            logger.info(f"Time for merge {end_time-start_time}")
            return ppmt

        partial_parses = _dc(0, self.path_node_count)
        logger.debug(f"Partial Parses Before Return {partial_parses}")
        return set([self.G.edge_subgraph(p.edges) for p in partial_parses])

    def check_parse_validity(self):
        ''' Validity Check for parses

            Remove parses with double kArakas
            Remove parses with multiple to edges into a node
            Remove parses with cycles
        '''
        # Check a parse for validity
        def _check(parse):
            r = True
            count = defaultdict(lambda: defaultdict(int))
            toedge = defaultdict(int)
            fromv = defaultdict(int)
            tov = defaultdict(int)
            for (u, v, l) in parse.edges(data='label'):
                if l in karakas:
                    count[u][l] = count[u][l]+1
                    toedge[v] = toedge[v]+1
                if l in 'viSezaRa':
                    fromv[u] = fromv[u] + 1
                    tov[v] = tov[v] + 1

            for u in count:  # Dhatu
                for k in count[u]:  # Each karaka should count only once
                    if count[u][k] > 1:
                        logger.info(f"Count for {u} {k} is {count[u][k]} - violates global constraint")
                        return False
            for v in toedge:
                if toedge[v] > 1:
                    logger.info(f"Toedges for {v} is {toedge[v]} - violates global constraint")
                    return False
            for v in tov:
                if v in fromv:
                    logger.info(f"Viseshana has visheshana {v} - violates global constraint")
                    return False
            return r
        iv = set()
        logger.debug(f"Parses before validity check {len(self.parses)}")
        for p in self.parses:
            if not _check(p):
                logger.info(f"Will remove {p}")
                iv.add(p)  # Collect invalid parses
        # Remove them
        self.parses.difference_update(iv)
        logger.info(f"Parses after validity check {len(self.parses)}")

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
        nx.drawing.nx_agraph.write_dot(self.G, path)
        d = dirname(path)
        be = basename(path)
        b, e = splitext(be)
        logger.info(f"Path {d} {b} {e}")
        for i, p in enumerate(self.parses):
            pt = join(d, b+f"_parse{i}"+e)
            nx.drawing.nx_agraph.write_dot(p, pt)


class VakyaGraphNode(object):
    """ Class for VakyaGraph nodes

        This has pada (a SanskritObject) plus a list of disjoint nodes
        to which edges cannot be created from this node
    """
    def __init__(self, sobj):
        self.pada = sobj
        self.disjointNodes = []

    # def isDisjoint(self, node):
    #     return node in self.disjointNodes

    # def makeDisjoint(self, nodes):
    #     self.disjointNodes.extend(nodes)

    def getMorphologicalTags(self):
        return self.pada.getMorphologicalTags()

    def getNodeTagset(self):
        ''' Given a Node, extract the tagset '''
        return getSLP1Tagset(self.getMorphologicalTags())

    def node_is_a(self, st):
        ''' Check if node matches a particular tag or any of a set of tags '''
        if isinstance(st, str):
            return st in self.getNodeTagset()
        elif isinstance(st, set):
            return not st.isdisjoint(self.getNodeTagset())
        else:
            logger.error(f"node_is_a: expecting str or set, got {st}")

    def get_vibhakti(self):
        ''' Get Node vacana '''
        return self.getNodeTagset().intersection(vibhaktis)

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
        return str(self.pada) + "=>" + str(self.pada.getMorphologicalTags())

    def __repr__(self):
        return str(self)


class VakyaParse(object):
    def __init__(self, nodes, nsets, G):
        ''' Initializes a partial parse with a node pair (or []) '''
        # Initialize disjoint sets DS
        self.dset = nsets.copy()
        self.G = G
        if nodes is not None:
            self._populate(nodes)
        else:
            self.elem = None
            self.nodes = set()
            self.edges = set()

    def __repr__(self):
        return repr(self.edges)

    def _populate(self, nodes):
        self.elem = nodes[0]
        self.nodes = set(nodes)
        self.edges = set([(nodes[0], nodes[1])])
        # Merge disjoint sets of initial nodes
        # Store the corresponding set as "eset" for
        # later merge operations
        self.eset = self.dset.union(self.elem, nodes[1])

    def is_discordant(self, pred, node):
        ''' Checks if a partial parse is compatible with a given node and predecessor pair '''
        elem = self.elem
        if elem is None:
            return False
        logger.debug(f"Pred in nodes: {pred in self.nodes} {self.nodes}")
        logger.debug(f"Node in nodes: {node in self.nodes} {self.nodes}")
        logger.debug(f"Connected pred {self.dset.connected(elem,pred)}")
        logger.debug(f"Connected node {self.dset.connected(elem,node)}")
        if ((pred in self.nodes) or (not self.dset.connected(elem, pred))) and \
           ((node in self.nodes) or (not self.dset.connected(elem, node))) and \
           ((node, pred) not in self.edges):   # Handle the bidi visheshana edges
            logger.debug(f"Non-Discoradant")
            return False
        else:
            logger.debug(f"Discordant")
            return True

    def extend(self, pred, node):
        ''' Extend current parse with edge from pred to node '''
        elem = self.elem
        if elem is None:
            logger.debug(f"Populating {self.elem}/{self.edges} with {(pred,node)}")
            self._populate((pred, node))
        else:
            logger.debug(f"Extending {self.edges} with {(pred,node)}")
            if pred not in self.nodes:
                self.nodes.add(pred)
                self.dset.union(elem, pred)
            if node not in self.nodes:
                self.nodes.add(node)
                self.dset.union(elem, node)
            self.edges.add((pred, node))
        logger.debug(f"Edges {self.edges} Dset {self.dset}")

    def can_merge(self, other, l):
        ''' Can we merge two VakyaParses '''
        # merge if all edges are not discordant
#        #for e in other.edges:
#        #    if self.is_discordant(e[0], e[1]):
#        #        return False
#        #return True
        # Updated can_merge algo  - This should be functionally same
        # But O(N) instead of O(N^2). Or is it?
        return ((len(other.edges) + len(self.edges)) == l) and \
               ((not ((other.nodes - self.nodes) & self.get_eset())) and
                (not ({tuple(reversed(x)) for x in other.edges} & self.edges)))

    def merge(self, other):
        ''' Merge two VakyaParses '''
        t = self.copy()
        logger.debug("Can merge")
        t.nodes.update(other.nodes)
        t.edges.update(other.edges)
        t.dset.union(self.elem, other.elem)
        return t

    def __len__(self):
        return len(self.edges)

    def copy(self):
        ''' Return a one level deep copy - in between a shallow and a fully deep copy '''
        t = VakyaParse(None, self.dset, self.G)
        t.nodes = copy(self.nodes)
        t.edges = copy(self.edges)
        t.elem = self.elem  # This will not change
        # We do not update t.eset to avoid making copy an O(N)
        # operation
        return t

    def get_eset(self):
        if hasattr(self, "eset"):
            return self.eset
        else:
            # Search once if needed
            for s in self.dset._sets:
                if self.elem in s:
                    self.eset = s
                    return self.eset


def getSLP1Tagset(n):
    ''' Given a (base, tagset) pair, extract the tagset '''
    return set(map(lambda x: x.canonical(), list(n[1])))


def match_purusha_vacana(d, n):
    ''' Check vacana/puruza compatibility for a Dhatu d and node n '''
    n_base = n.getMorphologicalTags()[0]
    if n_base == 'asmad':
        n_purusha = set([puruzas[2]])
    elif n_base == 'yuzmad':
        n_purusha = set([puruzas[1]])
    else:
        n_purusha = set([puruzas[0]])
    return (d.get_vacana() == n.get_vacana()) and (d.get_purusha() == n_purusha)


def match_linga_vacana(n1, n2):
    ''' Check linga/puruza compatibility for two nodes '''
    return (n1.get_vacana() == n2.get_vacana()) and (n1.get_linga() == n2.get_linga())


def match_linga_vacana_vibhakti(n1, n2):
    return (n1.get_vacana() == n2.get_vacana()) and (n1.get_linga() == n2.get_linga()) \
        and (n1.get_vibhakti() == n2.get_vibhakti())


def check_sambodhya(d, n):
    ''' Check sambodhya compatibility for dhatu d and node n '''
    return (d.get_vacana() == d.get_vacana()) and (d.get_purusha() == set([puruzas[1]]))
