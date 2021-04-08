'''
Handles user-input and converts it into the format that internal modules expect
and vice-versa

@author:
'''

from __future__ import print_function, unicode_literals
import re
import logging

logger = logging.getLogger(__name__)

deletions = re.compile("[\u200b\u200c\u200d,'-;/().?!\"0123456789{}#\r]")


def normalize(s):
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
        logger.debug("Detected anusvAra at end of string. Replacing with m")
        s = s[:-1] + 'm'
    if s[-1] == 'o':
        logger.debug("Detected o at end of string. Replacing with aH")
        s = s[:-1] + 'aH'
    # FIXME - temporary changes to handle ISO5519 as pseudo-IAST
    # Remove once we have a full ISO5519 implementation in indic_transliterate
    s = s.replace('ṁ', 'M')
    s = s.replace('r̥', 'f')
    s = s.replace('r̥̄', 'F')
    s = s.replace('l̥', 'x')
    return s


def replace_ending_visarga_s(s):
    """ Replace the final visarga of a string with s """
    if (s[-1] == 'H'):
        logger.debug("Detected H at end of string. Replacing with s")
        s = s[:-1] + 's'
    return s


def replace_ending_visarga_r(s):
    """ Replace the final visarga of a string with r """
    if (s[-1] == 'H'):
        logger.debug("Detected H at end of string. Replacing with s")
        s = s[:-1] + 'r'
    return s


def denormalize(s):
    """ Converts internal representation into user-friendly output
    Input s is expected to be an SLP1 encoded string
    """
    logger.debug("Denormalizing %s", s)
    s = s.replace("s ", "H ")
    s = s.replace("r ", "H ")
    s = re.sub("[sr]$", "H", s)
    logger.debug("%s", s)
    return s
