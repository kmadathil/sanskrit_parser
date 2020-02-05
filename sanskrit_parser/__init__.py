"""Intro
======

Sanskrit parser is a python library to help parse Sanskrit input

It provides three main levels of output, in order of increasing complexity:
  1. *tags* - Morphological analysis of a word
  2. *sandhi* - Sandhi Split of a phrase
  3. *vakya* - Morphological Analysis of a sentence (after Sandhi split)

This project is still under development. Please report any issues `here
<https://github.com/kmadathil/sanskrit_parser/issues>`_.

Command line usage
==================

The ``sanskrit_parser`` script can be used to view parses, sandhi splits,
or morphological tags as below.

If the ``--dot`` option is provided, a graph is output in ``.dot`` fomat with
all the possible morphologies as nodes, and possible relations as
edges. The valid parses extracted from this graph are also written out
as ``_parse.dot`` files


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

"""
import logging

log_file_name='SanskritParser.log'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console = logging.StreamHandler()
console.setLevel(logging.ERROR)
# set a format which is simpler for console use
formatter = logging.Formatter('%(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logger.addHandler(console)

# create file handler which logs even debug messages
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh = logging.FileHandler(log_file_name)
fh.setLevel(logging.ERROR)
fh.setFormatter(formatter)
logger.addHandler(fh)

