#!/usr/bin/env python
from __future__ import print_function
from indic_transliteration import sanscript
from indic_transliteration import detect
from sanskrit_parser.util import normalization

from contextlib import contextmanager
import logging
import six

logger = logging.getLogger(__name__)
denormalize = False


class SanskritString(object):
    """ Sanskrit String Class: Base of the class hierarchy

        Attributes:
           thing(str)   : thing to be represented
           encoding(str): SanskritBase encoding of thing as passed (eg: sanscript.HK, sanscript.DEVANAGARI)
        Args:
           thing(str):    As above
           encoding(str): As above

    """

    def __init__(self, thing, encoding=None, unicode_encoding='utf-8'):
        assert isinstance(thing, six.string_types)
        # Encode early, unicode everywhere, decode late is the philosophy
        # However, we need to accept both unicode and non unicode strings
        # We are udAramatiH
        if isinstance(thing, six.text_type):
            self.thing = thing
        else:
            self.thing = six.text_type(thing, unicode_encoding)
        if encoding is None:
            # Autodetect Encoding
            encoding = detect.detect(self.thing)
        if encoding != sanscript.SLP1:
            # Convert to SLP1
            self.thing = sanscript.transliterate(self.thing, encoding, sanscript.SLP1)
            # At this point, we are guaranteed that internal
            # representation is in SLP1

    def transcoded(self, encoding=None, strict_io=True):
        """ Return a transcoded version of self

            Args:
              encoding(SanskritObject.Scheme):
            Returns:
              str: transcoded version
        """
        s = self.thing
        if not strict_io:
            s = normalization.denormalize(s)
        return sanscript.transliterate(s, sanscript.SLP1, encoding)

    def canonical(self, strict_io=True):
        """ Return canonical transcoding (SLP1) of self
        """
        return self.transcoded(sanscript.SLP1, strict_io)

    def devanagari(self, strict_io=True):
        """ Return devanagari transcoding of self
        """
        return self.transcoded(sanscript.DEVANAGARI, strict_io)

    # Updates internal string, leaves everything else alone
    # Not to be used in all cases, as this is very limited
    def update(self, s, encoding=None):
        self.thing = s
        if encoding is not None:
            self.encoding = encoding

    def __str__(self):
        global denormalize
        s = self.transcoded(sanscript.SLP1)
        if denormalize:
            s = normalization.denormalize(s)
        return s

    def __repr__(self):
        return str(self)

    def __getitem__(self, i):
        return self.canonical()[i]

    def __len__(self):
        return len(self.canonical())


class SanskritImmutableString(SanskritString):
    """ Immutable version of SanskritString
    """
    def __init__(self, thing=None, encoding=None, unicode_encoding='utf-8'):
        super().__init__(thing, encoding, unicode_encoding)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return str(self) != str(other)


class SanskritNormalizedString(SanskritString):
    """ SanskritString plus Normalization of input
    """
    def __init__(self, thing=None, encoding=None, unicode_encoding='utf-8',
                 strict_io=True, replace_ending_visarga='s'):
        super().__init__(thing, encoding, unicode_encoding)
        if not strict_io:
            # Normalize
            logger.debug("Before normalization: %s", self.thing)
            tmp = normalization.normalize(self.thing)
            if replace_ending_visarga == 's':
                self.thing = normalization.replace_ending_visarga_s(tmp)
            elif replace_ending_visarga == 'r':
                self.thing = normalization.replace_ending_visarga_r(tmp)
            else:
                self.thing = tmp
            # Lazy Anusvaras (see issue #103)
            try:
                self.thing = sanscript.SLP1.fix_lazy_anusvaara(self.thing)
            except (NameError, AttributeError):
                print("Not fixing lazy anusvaras, you probably have an older version of indic_transliteration")
            logger.debug("After normalization: %s", self.thing)


class SanskritObject(SanskritNormalizedString):
    """ Sanskrit Object Class: Derived From SanskritString

        Attributes:

    """
    def __init__(self, thing=None, encoding=None, unicode_encoding='utf-8',
                 strict_io=True, replace_ending_visarga='s'):
        super().__init__(thing, encoding, unicode_encoding, strict_io, replace_ending_visarga)
        # Tags will go here as
        self.tags = []

    def setMorphologicalTags(self, t):
        """ Set Morphological Tags on Sanskrit Object

            Params:
               t (list): List of morphological tags
        """
        self.tags.extend(t)
        return self.tags

    def getMorphologicalTags(self):
        """ Morphological Tags on object """
        return self.tags


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
            ie = args.input_encoding

        oe = args.output_encoding

        s = SanskritObject(args.data, ie)
        print(s.transcoded(oe))

    main()
