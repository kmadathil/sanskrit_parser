'''
Handles user-input and converts it into the format that internal modules expect
and vice-versa

@author:
'''

from __future__ import print_function, unicode_literals
import re
import logging

logger = logging.getLogger(__name__)


def normalize(s):
    """ Converts user-input into format expected by internal modules.
    Input s is expected to be an SLP1 encoded string
    """
    def _dumpchars(s):
        # Remove Unicode Zero-Width characters
        s = re.sub("[\u200b\u200c\u200d]", "", s)
        # Punctuation and numeric characters
        for c in ",'-;().?!\"0123456789":
            s = s.replace(c, '')
        # Some bad visargas
        s = s.replace(':', 'H')
        # Replace line-breaks with spaces
        s = s.replace('\r\n', ' ').replace('\n', ' ')
        return s
    s = _dumpchars(s)
    if s[-1] == 'M':
        logger.warning("Detected anusvAra at end of string. Replacing with m")
        s = s[:-1] + 'm'
    if s[-1] == 'o':
        logger.warning("Detected o at end of string. Replacing with aH")
        s = s[:-1] + 'aH'
    if s[-1] == 'H':
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
