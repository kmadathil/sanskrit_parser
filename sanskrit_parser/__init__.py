"""

Parser
==========

Sanskrit parser is a python library to help parse Sanskrit input

It provides three main levels of output, in order of increasing complexity:
  1. *tags* - Morphological analysis of a word
  2. *sandhi* - Sandhi Split of a phrase
  3. *vakya* - Morpho-syntactic Analysis of a sentence (after Sandhi split)


Code resides at: https://github.com/kmadathil/sanskrit_parser/

Please report any issues at: https://github.com/kmadathil/sanskrit_parser/issues

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


__version__ = '0.2.4-post1'
__all__ = ['Parser', '__version__']
