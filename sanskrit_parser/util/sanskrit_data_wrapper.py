'''
Wrapper around data from Sanskrit data project

@author: avinashvarna
'''

from __future__ import print_function
import logging
import os
import sanskrit.analyze
import sanskrit.context
from sanskrit_parser.util.lexical_lookup import LexicalLookup


class SanskritDataWrapper(LexicalLookup):
    
    def __init__(self, logger=None):
        config = {
            "DATABASE_URI":'sqlite:///' + os.path.join(self.base_dir, 'data.db'), 
            "DATA_PATH":""}
        ctx = sanskrit.context.Context(config)
        self.analyzer = sanskrit.analyze.SimpleAnalyzer(ctx)
        self.tag_cache = {}
        self.logger = logger or logging.getLogger(__name__)
        
    def valid(self, word):
        self.logger.debug("Checking if %s is valid", word)
        if word in self.tag_cache:
            self.logger.debug("Cache hit")
            return True
        else:
            tags = self.get_tags(word)
            if tags != None:
                self.logger.debug("Found tags")
                return True
        self.logger.debug("Returning False")
        return False
    
    def get_tags(self, word):
        self.logger.debug("Looking up tags for %s", word)
        if word in self.tag_cache:
            self.logger.debug("Cache hit")
            return self.tag_cache[word]
        else:
            tags = self.analyzer.analyze(word)
            if tags != []:
                self.logger.debug("Found tags %s", tags)
                self.tag_cache[word] = tags
                return tags
            else:
                return None

if __name__ == "__main__":
    args=LexicalLookup.getArgs()
    if args.loglevel:
        numeric_level = getattr(logging, args.loglevel.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % args.loglevel)
        logging.basicConfig(level = numeric_level)
    SanskritDataWrapper().main(args)