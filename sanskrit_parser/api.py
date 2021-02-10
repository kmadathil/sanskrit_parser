# -*- coding: utf-8 -*-
"""

Usage
======

The ``Parser`` class can be used to generate vakya parses thus:

.. code-block:: python

        from itertools import islice
        from sanskrit_parser import Parser
        string = "astyuttarasyAMdiSi"
        input_encoding = "SLP1"
        output_encoding = "SLP1"
        parser = Parser(input_encoding=input_encoding,
                        output_encoding=output_encoding,
                        replace_ending_visarga='s')
        parse_result = parser.parse(string)
        if parse_result is not None:
            print('Splits:')
            for split in parse_result.splits(max_splits=10):
                print(f'Lexical Split: {split}')
                for i, parse in enumerate(islice(split.parses(), 3)):
                    print(f'Parse {i}')
                    print(f'{parse}')
        else:
            print('No splits found.  Please check the input to ensure there are no typos.')


This produces the output::

    Lexical Split: ['asti', 'uttarasyAm', 'diSi']
    Parse 0
    asti => (asti, ['samAsapUrvapadanAmapadam', 'strIliNgam']) : samasta of uttarasyAm
    uttarasyAm => (uttara#1, ['saptamIviBaktiH', 'strIliNgam', 'ekavacanam'])
    diSi => (diS, ['saptamIviBaktiH', 'ekavacanam', 'strIliNgam']) : viSezaRa of uttarasyAm
    Parse 1
    asti => (asti, ['samAsapUrvapadanAmapadam', 'strIliNgam']) : samasta of uttarasyAm
    uttarasyAm => (uttara#2, ['saptamIviBaktiH', 'strIliNgam', 'ekavacanam']) : viSezaRa of diSi
    diSi => (diS#2, ['saptamIviBaktiH', 'strIliNgam', 'ekavacanam'])
    Parse 2
    asti => (as#1, ['kartari', 'praTamapuruzaH', 'law', 'parasmEpadam', 'ekavacanam', 'prATamikaH'])
    uttarasyAm => (uttara#2, ['saptamIviBaktiH', 'strIliNgam', 'ekavacanam']) : viSezaRa of diSi
    diSi => (diS, ['saptamIviBaktiH', 'ekavacanam', 'strIliNgam']) : aDikaraRam of asti

@author: avinashvarna
"""

import time
import json
import abc
import warnings
from dataclasses import dataclass
from typing import Sequence
import itertools
from sanskrit_parser.base.sanskrit_base import SCHEMES, SanskritObject, SLP1
from sanskrit_parser.base.sanskrit_base import SanskritNormalizedString, SanskritString
from sanskrit_parser.parser.sandhi_analyzer import LexicalSandhiAnalyzer
from sanskrit_parser.parser.datastructures import VakyaGraph, VakyaGraphNode
from sanskrit_parser.parser.datastructures import SandhiGraph
import logging

logger = logging.getLogger(__name__)


class Serializable(abc.ABC):
    """ Base class to indicate an object is serializable into JSON """

    @abc.abstractmethod
    def serializable(self):
        ''' Return an object that can be serialized by json.JSONEncoder '''
        pass


class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, Serializable):
            return o.serializable()
        return super().default(o)


class Parser():

    def __init__(self, strict_io: bool = False, input_encoding: str = None,
                 output_encoding: str = 'SLP1', lexical_lookup: str = "combined",
                 score: bool = True, split_above: int = 5,
                 replace_ending_visarga: str = None, fast_merge: bool = True):
        self.strict_io = strict_io
        if input_encoding is not None:
            self.input_encoding = SCHEMES[input_encoding]
        else:
            self.input_encoding = None
        self.output_encoding = SCHEMES[output_encoding]
        self.lexical_lookup = lexical_lookup
        self.score = score
        self.split_above = split_above
        self.replace_ending_visarga = replace_ending_visarga
        self.fast_merge = fast_merge

    def parse(self,
              input_string: str,
              pre_segmented: False,
              ):
        sandhi_analyzer = LexicalSandhiAnalyzer(self.lexical_lookup)
        if pre_segmented:
            logger.debug("Pre-Segmented")
            s = []
            for seg in input_string.split(" "):
                o = SanskritObject(seg,
                                   encoding=self.input_encoding,
                                   strict_io=self.strict_io,
                                   replace_ending_visarga='r')
                ts = sandhi_analyzer.getMorphologicalTags(o, tmap=True)
                if ts is None:
                    # Possible sakaranta
                    # Try by replacing end visarga with 's' instead
                    o = SanskritObject(seg,
                                       encoding=self.input_encoding,
                                       strict_io=self.strict_io,
                                       replace_ending_visarga='s')
                    ts = sandhi_analyzer.getMorphologicalTags(o, tmap=True)
                if ts is None:
                    logger.warning(f"Unknown pada {seg} - will be split")
                    _p = self.parse(seg, False)
                    _s = list(itertools.islice(_p.splits(), 1))[0]
                    logger.info(f"Split {_s}")
                    s.extend(_s.split)
                    if _s is None:
                        logger.warning(f"Unknown pada {seg} - cannot be split")
                else:
                    s.append(o)
            logger.info(f"Input String in SLP1: {' '.join([x.canonical() for x in s])}")
            graph = sandhi_analyzer.preSegmented(s, tag=True)
            logger.debug("End DAG generation")
        else:
            s = SanskritNormalizedString(input_string,
                                         encoding=self.input_encoding,
                                         strict_io=self.strict_io,
                                         replace_ending_visarga=self.replace_ending_visarga)
            logger.info(f"Input String in SLP1: {s.canonical()}")
            logger.debug("Start Split")
            graph = sandhi_analyzer.getSandhiSplits(s, tag=True)
            logger.debug("End DAG generation")
        if graph is None:
            warnings.warn("No splits found. Please check the input to ensure there are no typos.")
            return None
        return ParseResult(self, input_string, graph)


@dataclass
class ParseResult(Serializable):
    parser: Parser
    input_string: str
    sandhi_graph: SandhiGraph

    def __str__(self):
        return f"ParseResult('{self.input_string}')"

    def splits(self, max_splits: int = 10):
        split_results = self.sandhi_graph.find_all_paths(max_paths=max_splits,
                                                         sort=True,
                                                         score=self.parser.score)
        logger.debug("End pathfinding")
        logger.debug("Splits:")
        for split in split_results:
            logger.debug(f"Lexical Split: {split}")
            yield Split(self.parser, self.input_string, split)

    def serializable(self):
        return list(self.splits(10))

    def write_dot(self, basepath):
        self.sandhi_graph.write_dot(basepath)


@dataclass
class Split(Serializable):
    parser: Parser
    input_string: str
    split: Sequence[SanskritObject]
    vgraph: VakyaGraph = None

    def __repr__(self):
        return f'Split({self.input_string}) = {self.split}'

    def __str__(self):
        strict_io = self.parser.strict_io
        encoding = self.parser.output_encoding
        out = [t.transcoded(encoding, strict_io) for t in self.split]
        return str(out)

    def parses(self, min_cost_only=False):
        self.vgraph = VakyaGraph(self.split,
                                 fast_merge=self.parser.fast_merge,
                                 max_parse_dc=self.parser.split_above)
        min_cost = self.vgraph.parse_costs[0]
        if min_cost_only:
            it = enumerate(itertools.compress(self.vgraph.parses,
                                              [x == min_cost for x in self.vgraph.parse_costs]))
        else:
            it = enumerate(self.vgraph.parses)
        for (ix, parse_graph) in it:
            logger.debug(f"Parse {ix}, Cost {self.vgraph.parse_costs[ix]}")
            yield Parse(self, parse_graph, self.vgraph.parse_costs[ix])

    def write_dot(self, basepath):
        self.vgraph.write_dot(basepath)

    def serializable(self):
        strict_io = self.parser.strict_io
        encoding = self.parser.output_encoding
        out = [t.transcoded(encoding, strict_io) for t in self.split]
        return {'split': out,
                'parses': list(self.parses())
                }


@dataclass
class ParseTag(Serializable):
    root: str
    tags: Sequence[str]

    def serializable(self):
        return {'root': self.root, 'tags': self.tags}

    def __str__(self):
        return f'({self.root}, {self.tags})'


class ParseNode(Serializable):
    def __init__(self, node: VakyaGraphNode,
                 strict_io: bool,
                 encoding: str):
        self.pada = node.pada.transcoded(encoding, strict_io)
        tag = node.getMorphologicalTags()
        self.parse_tag = ParseTag(tag[0].transcoded(encoding, strict_io),
                                  [t.transcoded(encoding, strict_io) for t in tag[1]]
                                  )
        self.index = node.index

    def __str__(self):
        return f'{self.pada} => {self.parse_tag}'

    def serializable(self):
        d = {'pada': self.pada}
        d.update(self.parse_tag.serializable())
        return d


@dataclass
class ParseEdge(Serializable):
    predecessor: ParseNode
    node: ParseNode
    label: str

    def __str__(self):
        return f'{self.node} : {self.label} of {self.predecessor.pada}'

    def serializable(self):
        return {'node': self.node,
                'predecessor': self.predecessor,
                'sambandha': self.label
                }


class Parse(Serializable):

    def __init__(self, split: Split, parse_graph, cost):
        strict_io = split.parser.strict_io
        encoding = split.parser.output_encoding
        graph = []
        for n in sorted(list(parse_graph), key=lambda x: x.index):
            node = ParseNode(n, strict_io, encoding)
            preds = list(parse_graph.predecessors(n))
            if preds:
                pred = preds[0]  # Only one
                # Multigraph
                # Ugh - surely this can be better
                lbl = list(parse_graph[pred][n].values())[0]['label']
                pred_node = ParseNode(pred, strict_io, encoding)
                edge = ParseEdge(pred_node,
                                 node,
                                 SanskritString(lbl, encoding=SLP1).transcoded(encoding, strict_io)
                                 )
                graph.append(edge)
            else:
                graph.append(node)
        self.graph = graph
        self.cost = cost

    def __str__(self):
        return '\n'.join([str(t) for t in self.graph])

    def __iter__(self):
        return iter(self.graph)

    def to_conll(self):
        r = []
        for t in self.graph:
            if isinstance(t, ParseNode):
                r.append([str(t.index+1), str(t.pada), "_",
                          str(t.parse_tag.root), str(t.parse_tag.tags),
                          "0", "root"])
            else:
                r.append([str(t.node.index+1), str(t.node.pada), "_",
                          str(t.node.parse_tag.root), str(t.node.parse_tag.tags),
                          str(t.predecessor.index+1), str(t.label)])
        return r

    def serializable(self):
        return {'graph': self.graph}


if __name__ == "__main__":
    start_time = time.time()

    def api_example(string, output_encoding):
        parser = Parser(output_encoding=output_encoding,
                        replace_ending_visarga='s')
        parse_result = parser.parse(string)
        print('Splits:')
        for split in parse_result.splits(max_splits=10):
            print(f'Lexical Split: {split}')
            for i, parse in enumerate(itertools.islice(split.parses(), 2)):
                print(f'Parse {i}')
                print(f'{parse}')
            break
        print(json.dumps(split,
                         ensure_ascii=False,
                         indent=2,
                         cls=JSONEncoder)
              )

    def main():
        examples = [('devadattogrAmaMgacCati', 'SLP1'),
                    ('astyuttarasyAMdishidevatAtmA', 'Devanagari')
                    ]
        for string, encoding in examples:
            api_example(string, encoding)

    main()
    print(f'Took {time.time() - start_time} s')
