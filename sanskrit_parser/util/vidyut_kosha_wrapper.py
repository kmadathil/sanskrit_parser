# -*- coding: utf-8 -*-
"""
Wrapper around vidyut data
"""

from __future__ import print_function
import logging
from sanskrit_parser.util.lexical_lookup import LexicalLookup
from sanskrit_parser.base.sanskrit_base import SanskritImmutableString
from indic_transliteration import sanscript
from sanskrit_parser.util.data_manager import data_file_path

from vidyut.kosha import Kosha

import os

kosha_path = os.path.dirname(__file__) + "/../../../vidyut_data/kosha"


class VidyutWrapper(LexicalLookup):

    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.kosha = Kosha(kosha_path)
        self.logger.debug("Using kosha at %s", kosha_path)

    def valid(self, word):
        return word in self.kosha

    def get_tags(self, word, tmap=True):
        if word in self.kosha:
            return self.kosha[word]
        return None


if __name__ == "__main__":
    args = LexicalLookup.getArgs()
    if args.loglevel:
        numeric_level = getattr(logging, args.loglevel.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError("Invalid log level: %s" % args.loglevel)
        logging.basicConfig(level=numeric_level)
    VidyutWrapper().main(args)
