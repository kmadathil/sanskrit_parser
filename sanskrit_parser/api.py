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
        print('Splits:')
        for split in parse_result.splits(max_splits=10):
            print(f'Lexical Split: {split}')
            for i, parse in enumerate(islice(split.parses(), 3)):
                print(f'Parse {i}')
                print(f'{parse}')
        ...
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
from dataclasses import dataclass
from typing import Sequence
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


@dataclass
class Parser():
    strict_io: bool = False
    input_encoding: str = None
    output_encoding: str = 'SLP1'
    lexical_lookup: str = "combined"
    score: bool = True
    split_above: int = 5
    replace_ending_visarga: str = None
    fast_merge = True

    def parse(self,
              input_string: str,
              ):
        if self.input_encoding is not None:
            self.input_encoding = SCHEMES[self.input_encoding]
        if self.output_encoding is not None:
            self.output_encoding = SCHEMES[self.output_encoding]
        s = SanskritNormalizedString(input_string,
                                     encoding=self.input_encoding,
                                     strict_io=self.strict_io,
                                     replace_ending_visarga=self.replace_ending_visarga)
        logger.info(f"Input String in SLP1: {s.canonical()}")
        sandhi_analyzer = LexicalSandhiAnalyzer(self.lexical_lookup)
        logger.debug("Start Split")
        graph = sandhi_analyzer.getSandhiSplits(s, tag=True)
        logger.debug("End DAG generation")
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

    def parses(self):
        self.vgraph = VakyaGraph(self.split,
                                 fast_merge=self.parser.fast_merge,
                                 max_parse_dc=self.parser.split_above)
        for (ix, parse_graph) in enumerate(self.vgraph.parses):
            logger.debug(f"Parse {ix}")
            yield Parse(self, parse_graph)

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

    def __str__(self):
        return f'{self.pada} => {self.parse_tag}'

    def serializable(self):
        d = {'pada': self.pada}
        d.update(self.parse_tag.serializable())
        return d


@dataclass
class ParseEdge(Serializable):
    predecessor: str
    node: ParseNode
    label: str

    def __str__(self):
        return f'{self.node} : {self.label} of {self.predecessor}'

    def serializable(self):
        return {'node': self.node,
                'predecessor': self.predecessor,
                'sambandha': self.label
                }


class Parse(Serializable):

    def __init__(self, split: Split, parse_graph):
        strict_io = split.parser.strict_io
        encoding = split.parser.output_encoding
        graph = []
        for n in sorted(list(parse_graph), key=lambda x: x.index):
            node = ParseNode(n, strict_io, encoding)
            preds = list(parse_graph.predecessors(n))
            if preds:
                pred = preds[0]  # Only one
                lbl = parse_graph.edges[pred, n]['label']
                edge = ParseEdge(pred.pada.transcoded(encoding, strict_io),
                                 node,
                                 SanskritString(lbl, encoding=SLP1).transcoded(encoding, strict_io)
                                 )
                graph.append(edge)
            else:
                graph.append(node)
        self.graph = graph

    def __str__(self):
        return '\n'.join([str(t) for t in self.graph])

    def serializable(self):
        return {'graph': self.graph}


if __name__ == "__main__":
    start_time = time.time()

    def api_example(string, output_encoding):
        from itertools import islice
        parser = Parser(output_encoding=output_encoding,
                        replace_ending_visarga='s')
        parse_result = parser.parse(string)
        print('Splits:')
        for split in parse_result.splits(max_splits=10):
            print(f'Lexical Split: {split}')
            for i, parse in enumerate(islice(split.parses(), 2)):
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
