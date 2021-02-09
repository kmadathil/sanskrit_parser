"""
Introduction
===========

Sanskrit parser is a python library to help parse Sanskrit input

It provides three main levels of output, in order of increasing complexity:
  1. *tags* - Morphological analysis of a word
  2. *sandhi* - Sandhi Split of a phrase
  3. *vakya* - Morpho-syntactic Analysis of a sentence (after Sandhi split)

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

    $ dot -Tpng vakya_split0.dot -o vakya_split0.png
    $ eog vakya.png
    $ dot -Tpng vakya_split0_parse0.dot -o vakya_split0_parse0.png
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
from .api import Parser
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def enable_console_logger(level=logging.INFO,
                          fmt='%(levelname)-8s %(message)s'):
    '''Enable logger Console Logging for sanskrit_parser

       Params
           level: log level
           fmt  : log format
    '''
    logger = logging.getLogger(__name__)
    console = logging.StreamHandler()
    console.setLevel(level)
    # set a format which is simpler for console use
    formatter = logging.Formatter(fmt)
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logger.addHandler(console)


def enable_file_logger(log_file_name='SanskritParser.log',
                       level=logging.INFO,
                       fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    '''Enable logger File Logging for sanskrit_parser

       Params
           log_file_name(str): Log file Name
           level: log level
           fmt  : log format
    '''
    logger = logging.getLogger(__name__)
    # create file handler which logs even debug messages
    formatter = logging.Formatter(fmt)
    fh = logging.FileHandler(log_file_name)
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


__all__ = ['Parser']
