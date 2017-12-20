'''
Handles user-input and converts it into the format that internal modules expect
and vice-versa

@author:
'''

from __future__ import print_function, unicode_literals
import re
import logging

logger = logging.getLogger(__name__)

deletions = re.compile("[\u200b\u200c\u200d,'-;().?!\"0123456789{}#\r]")
rakarantas = ['punaH', 'antaH']


def normalize(s, replace_ending_visarga=True):
    """ Converts user-input into format expected by internal modules.
    Input s is expected to be an SLP1 encoded string
    """
    # Some bad visargas
    s = s.replace(':', 'H')
    # Remove Unicode Zero-Width characters, punctuation and numeric characters
    s = deletions.sub("", s)
    # Replace line-breaks with spaces
    s = s.replace('\n', ' ')
    if s[-1] == 'M':
        logger.warning("Detected anusvAra at end of string. Replacing with m")
        s = s[:-1] + 'm'
    if s[-1] == 'o':
        logger.warning("Detected o at end of string. Replacing with aH")
        s = s[:-1] + 'aH'
    if (s[-1] == 'H') & replace_ending_visarga:
        if s in rakarantas:
            logger.warning("Detected H at end of string. Replacing with r")
            s = s[:-1] + 'r'
        else:
            logger.warning("Detected H at end of string. Replacing with s")
            s = s[:-1] + 's'
    return s


def denormalize(s):
    """ Converts internal representation into user-friendly output
    Input s is expected to be an SLP1 encoded string
    """
    logger.debug("Denormalizing %s", s)
    s = s.replace("s ", "H ")
    s = re.sub("s$", "H", s)
    logger.debug("%s", s)
    return s
