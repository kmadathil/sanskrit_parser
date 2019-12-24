"""
Usage
=====

Use the ``SanskritSandhiAnalyzer`` to split a sentence (wrapped in a
``SanskritObject``) and retrieve the top 10 splits:

.. code:: python

    >>> from __future__ import print_function
    >>> from sanskrit_parser.parser.sandhi_analyzer import SanskritSandhiAnalyzer
    >>> from sanskrit_parser.base.sanskrit_base import SanskritObject, SLP1
    >>> sentence = SanskritObject("astyuttarasyAMdishidevatAtmA")
    >>> analyzer = SanskritSandhiAnalyzer()
    >>> splits = analyzer.getSandhiSplits(sentence).findAllPaths(10)
    >>> for split in splits:
    ...    print(split)
    ...
    [u'asti', u'uttarasyAm', u'diSi', u'devatA', u'AtmA']
    [u'asti', u'uttarasyAm', u'diSi', u'devat', u'AtmA']
    [u'asti', u'uttarasyAm', u'diSi', u'devata', u'AtmA']
    [u'asti', u'uttara', u'syAm', u'diSi', u'devatA', u'AtmA']
    [u'asti', u'uttarasyAm', u'diSi', u'devatA', u'at', u'mA']
    [u'asti', u'uttarasyAm', u'diSi', u'de', u'vatA', u'AtmA']
    [u'asti', u'uttarasyAm', u'diSi', u'devata', u'at', u'mA']
    [u'asti', u'uttas', u'rasyAm', u'diSi', u'devat', u'AtmA']
    [u'asti', u'uttara', u'syAm', u'diSi', u'devat', u'AtmA']
    [u'asti', u'uttarasyAm', u'diSi', u'de', u'avatA', u'AtmA']

The lexical_analyzer can also be used to look up the tags for a given
word form: (Note that the database stores words
ending in visarga with an 's' at the end)

.. code:: python

    >>> word = SanskritObject('hares')
    >>> tags = analyzer.getLexicalTags(word)
    >>> for tag in tags:
    ...    print(tag)
    ...
    ('hf#1', set(['cj', 'snd', 'prim', 'para', 'md', 'sys', 'prs', 'v', 'np', 'sg', 'op']))
    ('hari#1', set(['na', 'mas', 'sg', 'gen']))
    ('hari#1', set(['na', 'mas', 'abl', 'sg']))
    ('hari#1', set(['na', 'fem', 'sg', 'gen']))
    ('hari#1', set(['na', 'fem', 'abl', 'sg']))
    ('hari#2', set(['na', 'mas', 'sg', 'gen']))
    ('hari#2', set(['na', 'mas', 'abl', 'sg']))
    ('hari#2', set(['na', 'fem', 'sg', 'gen']))
    ('hari#2', set(['na', 'fem', 'abl', 'sg']))


Command line usage
==================

::

    $ python -m sanskrit_parser.parser.sandhi_analyzer astyuttarasyAMdishidevatAtmA
    Splits:
    [u'asti', u'uttarasyAm', u'diSi', u'devat', u'AtmA']
    [u'asti', u'uttarasyAm', u'diSi', u'devata', u'AtmA']
    [u'asti', u'uttarasyAm', u'diSi', u'devatA', u'AtmA']
    [u'asti', u'uttara', u'syAm', u'diSi', u'devat', u'AtmA']
    [u'asti', u'uttarasyAm', u'diSi', u'devata', u'at', u'mA']
    [u'asti', u'uttarasyAm', u'diSi', u'de', u'vatAt', u'mA']
    [u'asti', u'uttarasyAm', u'diSi', u'devatA', u'at', u'mA']
    [u'asti', u'uttas', u'asyAm', u'diSi', u'devat', u'AtmA']
    [u'asti', u'uttara', u'syAm', u'diSi', u'devata', u'AtmA']
    [u'asti', u'uttarasyAm', u'diSi', u'de', u'vatA', u'AtmA']

    $ python -m sanskrit_parser.parser.sandhi_analyzer hares --tags
    Input String: hares
    Input String in SLP1: hares
    [('hf#1', set(['cj', 'snd', 'prim', 'para', 'md', 'sys', 'prs', 'v', 'np', 'sg', 'op'])), ('hari#1', set(['na', 'mas', 'sg', 'gen'])),
 ('hari#1', set(['na', 'mas', 'abl', 'sg'])), ('hari#1', set(['na', 'fem', 'sg', 'gen'])), ('hari#1', set(['na', 'fem', 'abl', 'sg'])),
 ('hari#2', set(['na', 'mas', 'sg', 'gen'])), ('hari#2', set(['na', 'mas', 'abl', 'sg'])), ('hari#2', set(['na', 'fem', 'sg', 'gen'])),
 ('hari#2', set(['na', 'fem', 'abl', 'sg']))]

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

::

    $ python -m sanskrit_parser.morphological_analyzer.sanskrit_morphological_analyzer astyuttarasyAm --input-encoding SLP1 --need-lakara
    Input String: astyuttarasyAm
    Input String in SLP1: astyuttarasyAm
    Start Split: 2017-10-01 11:16:10.489660
    End DAG generation: 2017-10-01 11:16:10.496199
    End pathfinding: 2017-10-01 11:16:10.497342
    Splits:
    Lexical Split: [asti, uttarasyAm]
    Valid Morphologies
    [(asti, ('as#1', set([kartari, law, ekavacanam, prATamikaH, praTamapuruzaH]))),
    (uttarasyAm, ('uttara#2', set([strIliNgam, saptamIviBaktiH, ekavacanam])))]
    [(asti, ('as#1', set([kartari, law, ekavacanam, prATamikaH, praTamapuruzaH]))),
    (uttarasyAm, ('uttara#1', set([strIliNgam, saptamIviBaktiH, ekavacanam])))]
    Lexical Split: [asti, uttara, syAm]
    No valid morphologies for this split
    Lexical Split: [asti, ut, tara, syAm]

"""
