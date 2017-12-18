#!/usr/bin/env python
from __future__ import print_function
from indic_transliteration import sanscript
from indic_transliteration import detect
from sanskrit_parser.util import normalization

from contextlib import contextmanager
import logging
import six

# Wrap scheme names defined in sanscript
BENGALI = sanscript.BENGALI
DEVANAGARI = sanscript.DEVANAGARI
GUJARATI = sanscript.GUJARATI
GURMUKHI = sanscript.GURMUKHI
KANNADA = sanscript.KANNADA
MALAYALAM = sanscript.MALAYALAM
ORIYA = sanscript.ORIYA
TAMIL = sanscript.TAMIL
TELUGU = sanscript.TELUGU
HK = sanscript.HK
IAST = sanscript.IAST
ITRANS = sanscript.ITRANS
KOLKATA = sanscript.KOLKATA
SLP1 = sanscript.SLP1
VELTHUIS = sanscript.VELTHUIS
WX = sanscript.WX

# Dict defined so autodetect can work
SCHEMES = {
    'Bengali': BENGALI,
    'Devanagari': DEVANAGARI,
    'Gujarati': GUJARATI,
    'Gurmukhi': GURMUKHI,
    'Kannada': KANNADA,
    'Malayalam': MALAYALAM,
    'Oriya': ORIYA,
    'Tamil': TAMIL,
    'Telugu': TELUGU,
    'HK': HK,
    'IAST': IAST,
    'ITRANS': ITRANS,
    'Kolkata': KOLKATA,
    'SLP1': SLP1,
    'Velthuis': VELTHUIS,
    'WX': WX
}

logger = logging.getLogger(__name__)
denormalize = False


class SanskritObject(object):
    """ Sanskrit Object Class: Base of the class hierarchy

        Attributes:
           thing(str)   : thing to be represented
           encoding(str): SanskritBase encoding of thing as passed (eg: SanskritBase.HK, SanskritBase.DEVANAGARI)
        Args:
           thing(str):    As above
           encoding(str): As above

    """

    def __init__(self, thing=None, encoding=None, unicode_encoding='utf-8', strict_io=True):
        assert isinstance(thing, six.string_types)
        # Encode early, unicode everywhere, decode late is the philosophy
        # However, we need to accept both unicode and non unicode strings
        # We are udAramatiH
        if isinstance(thing, six.text_type):
            self.thing = thing
        else:
            self.thing = six.text_type(thing, unicode_encoding)
        self.encoding = encoding
        if self.encoding is None:
            if thing is not None:
                # Autodetect Encoding
                self.encoding = SCHEMES[detect.detect(self.thing)]
        if not strict_io:
            # Convert to SLP1 and normalize
            self.thing = self.canonical()
            self.encoding = SLP1
            logger.debug("Before normalization: %s", self.thing)
            self.thing = normalization.normalize(self.thing)
            logger.debug("After normalization: %s", self.thing)
        # Tags will go here as
        # { lexical_tag : [possible morphologies] }
        self.tags = []

    def transcoded(self, encoding=None):
        """ Return a transcoded version of self

            Args:
              encoding(SanskritObject.Scheme):
            Returns:
              str: transcoded version
        """
        return sanscript.transliterate(self.thing, self.encoding, encoding)

    def canonical(self, strict_io=True):
        """ Return canonical transcoding (SLP1) of self
        """
        s = self.transcoded(SLP1)
        if not strict_io:
            s = normalization.denormalize(s)
        return s

    def devanagari(self, strict_io=True):
        """ Return devanagari transcoding of self
        """
        s = self.transcoded(SLP1)
        if not strict_io:
            s = normalization.denormalize(s)
        return sanscript.transliterate(s, SLP1, DEVANAGARI)

    def setLexicalTags(self, t):
        """ Set Lexical Tags on Sanskrit Object

            Params:
               t (list): List of lexical tags
        """
        for tt in t:
            # of the form (dhatu_or_prAtipadikam : set([tags]))
            # FIXME: Incorporate morphological associations
            self.tags.append(tt)
        return self.tags

    def getTags(self):
        """ Tags on object """
        return self.tags

    def __str__(self):
        global denormalize
        s = self.transcoded(SLP1)
        if denormalize:
            s = normalization.denormalize(s)
        return s

    def __repr__(self):
        return str(self)


@contextmanager
def outputctx(strict_io):
    global denormalize
    save_denormalize = denormalize
    denormalize = not strict_io
    yield
    denormalize = save_denormalize


if __name__ == "__main__":
    import argparse

    def getArgs():
        """
          Argparse routine.
          Returns args variable
        """
        # Parser Setup
        parser = argparse.ArgumentParser(description='SanskritObject')
        # String to encode
        parser.add_argument('data', nargs="?", type=str, default="idam adbhutam")
        # Input Encoding (autodetect by default)
        parser.add_argument('--input-encoding', type=str, default=None)
        # Output Encoding (Devanagari by default)
        parser.add_argument('--output-encoding', type=str, default="Devanagari")

        return parser.parse_args()

    def main():
        args = getArgs()
        print(args.data)
        if args.input_encoding is None:
            ie = None
        else:
            ie = SCHEMES[args.input_encoding]

        oe = SCHEMES[args.output_encoding]

        s = SanskritObject(args.data, ie)
        print(s.transcoded(oe))

    main()
