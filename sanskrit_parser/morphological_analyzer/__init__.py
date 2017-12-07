"""
Usage
======

The ``SanskritMorphologicalAnalyzer`` class has a similar interface to
``SanskritLexicalAnalyzer``, and has a ``constrainPath()`` method which
can find whether a particular split has a valid morphology, and output
all such valid morphologies.

.. code:: python

    >>> from sanskrit_parser.base.sanskrit_base import SanskritObject, SLP1
    >>> from sanskrit_parser.morphological_analyzer.SanskritMorphologicalAnalyzer import SanskritMorphologicalAnalyzer
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
    [(asti, ('as#1', set([kartari, law, ekavacanam, prATamikaH, praTamapuruzaH]))), (uttarasyAm, ('uttara#2', set([strIliNgam, saptamIviBaktiH, ekavacanam])))]
    [(asti, ('as#1', set([kartari, law, ekavacanam, prATamikaH, praTamapuruzaH]))), (uttarasyAm, ('uttara#1', set([strIliNgam, saptamIviBaktiH, ekavacanam])))]
    ('Lexical Split:', [asti, uttara, syAm])
    No valid morphologies for this split
    ('Lexical Split:', [asti, ut, tara, syAm])
    No valid morphologies for this split
"""