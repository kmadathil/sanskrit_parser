"""
Usage
=====

Use the ``SanskritLexicalAnalyzer`` to split a sentence (wrapped in a
``SanskritObject``) and retrieve the top 10 splits:

.. code:: python

    >>> from __future__ import print_function
    >>> from sanskrit_parser.lexical_analyzer.sanskrit_lexical_analyzer import SanskritLexicalAnalyzer
    >>> from sanskrit_parser.base.sanskrit_base import SanskritObject, SLP1
    >>> sentence = SanskritObject("astyuttarasyAMdishidevatAtmA")
    >>> analyzer = SanskritLexicalAnalyzer()
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

    $ python -m sanskrit_parser.lexical_analyzer.sanskrit_lexical_analyzer astyuttarasyAMdishidevatAtmA --split
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

    $ python -m sanskrit_parser.lexical_analyzer.sanskrit_lexical_analyzer hares
    Input String: hares
    Input String in SLP1: hares
    [('hf#1', set(['cj', 'snd', 'prim', 'para', 'md', 'sys', 'prs', 'v', 'np', 'sg', 'op'])), ('hari#1', set(['na', 'mas', 'sg', 'gen'])),
 ('hari#1', set(['na', 'mas', 'abl', 'sg'])), ('hari#1', set(['na', 'fem', 'sg', 'gen'])), ('hari#1', set(['na', 'fem', 'abl', 'sg'])),
 ('hari#2', set(['na', 'mas', 'sg', 'gen'])), ('hari#2', set(['na', 'mas', 'abl', 'sg'])), ('hari#2', set(['na', 'fem', 'sg', 'gen'])),
 ('hari#2', set(['na', 'fem', 'abl', 'sg']))]

"""
