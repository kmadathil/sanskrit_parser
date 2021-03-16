Usage
=========================================

Command line usage
------------------

The ``sanskrit_parser`` script can be used to view parses, sandhi splits,
or morphological tags as below.

If the ``--dot`` option is provided, a graph is output in ``.dot`` fomat with
all the possible morphologies as nodes, and possible relations as
edges. The valid parses extracted from this graph are also written out
as ``_parse.dot`` files

It provides three main levels of output, in order of increasing complexity:
  1. *tags* - Morphological analysis of a word
  2. *sandhi* - Sandhi Split of a phrase
  3. *vakya* - Morpho-syntactic Analysis of a sentence (after Sandhi split)

Vakya Analysis
..............

::

    $ sanskrit_parser vakya devadattogrAmaNgacCati --input SLP1 --dot vakya.dot
    ...
    Parse 0 : (Cost = 2.205)
    devadattaH => (devadatta, ['ekavacanam', 'puMlliNgam', 'praTamAviBaktiH']) : kartA of gacCati
    grAmam => (grAma, ['ekavacanam', 'dvitIyAviBaktiH', 'napuMsakaliNgam']) : karma of gacCati
    gacCati => (gam, ['kartari', 'law', 'prATamikaH', 'ekavacanam', 'praTamapuruzaH', 'parasmEpadam'])
    Parse 1 : (Cost = 2.205)
    devadattaH => (devadatta, ['ekavacanam', 'puMlliNgam', 'praTamAviBaktiH']) : kartA of gacCati
    grAmam => (grAma, ['ekavacanam', 'dvitIyAviBaktiH', 'puMlliNgam']) : karma of gacCati
    gacCati => (gam, ['kartari', 'law', 'prATamikaH', 'ekavacanam', 'praTamapuruzaH', 'parasmEpadam'])
    ...

To view the generated dot files, convert them into png first. 
    
::
   
   $ dot -Tpng -O vakya*.dot 
   $ eog vakya_split0.png
   $ eog vakya_split0_parse0.png


Sandhi Split
............

::

    $ sanskrit_parser sandhi astyuttarasyAMdishidevatAtmA
    ...
    Splits:
    [asti, uttarasyAm, diSi, devatA, AtmA]
    [asti, uttara, syAm, diSi, devatA, AtmA]
    [astI, uttarasyAm, diSi, devatA, AtmA]
    [asti, uttarasyAm, diSi, devatAt, mA]
    [asti, uttarasyAm, diSi, devata, AtmA]
    [asti, uttarasyAm, diSi, devat, AtmA]
    [asti, uttarasyAm, diSi, devatAtmA]
    [asti, uttarasyAm, diSi, devatA, at, mA]
    [asti, uttara, syAm, diSi, devat, AtmA]
    [asti, uttarasyAm, di, Si, devatA, AtmA]
    -----------
    ..


Morphological Tags for a Word
.............................
::

    $ scripts/sanskrit_parser tags hares
    ...
    Morphological tags:
    ('hf#1', {ekavacanam, viDiliN, prATamikaH, kartari, maDyamapuruzaH})
    ('hari#1', {ekavacanam, puMlliNgam, paYcamIviBaktiH})
    ('hari#1', {ekavacanam, paYcamIviBaktiH, strIliNgam})
    ('hari#1', {zazWIviBaktiH, ekavacanam, puMlliNgam})
    ('hari#1', {zazWIviBaktiH, ekavacanam, strIliNgam})
    ('hari#2', {ekavacanam, puMlliNgam, paYcamIviBaktiH})
    ('hari#2', {ekavacanam, paYcamIviBaktiH, strIliNgam})
    ('hari#2', {zazWIviBaktiH, ekavacanam, puMlliNgam})
    ('hari#2', {zazWIviBaktiH, ekavacanam, strIliNgam})
    ('hf', {ekavacanam, parasmEpadam, viDiliN, maDyamapuruzaH})
    ('hari', {ekavacanam, puMlliNgam, paYcamIviBaktiH})
    ('hari', {ekavacanam, strIliNgam, paYcamIviBaktiH})
    ('hari', {zazWIviBaktiH, ekavacanam, puMlliNgam})
    ('hari', {zazWIviBaktiH, ekavacanam, strIliNgam})

Use as a Library
-----------------

An `example python notebook`_ is available, which can also be directly launched on `Binder`_.

.. _`example python notebook`: https://github.com/kmadathil/sanskrit_parser/blob/master/examples/basic_example.ipynb

.. _`Binder`:  https://mybinder.org/v2/gh/kmadathil/sanskrit_parser/HEAD?filepath=examples%2Fbasic_example.ipynb
