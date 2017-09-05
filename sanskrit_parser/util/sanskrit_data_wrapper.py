# -*- coding: utf-8 -*-
'''
Wrapper around data from Sanskrit data project

@author: avinashvarna
'''

from __future__ import print_function
import logging
import os
import sanskrit.analyze
import sanskrit.context
from sanskrit.schema import Nominal, Indeclinable, Verb, Gerund, Infinitive
from sanskrit_parser.util.lexical_lookup import LexicalLookup
from sanskrit_parser.base.SanskritBase import SanskritObject, DEVANAGARI, SLP1

from sqlalchemy import inspect

#class SanskritDataTagMapper(object):
    
    

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
                return self.map_tags(tags)
            else:
                return None
            
    vacanam = ['एकवचनम्', 'द्विवचनम्', 'बहुवचनम्']
    lingam = ['पुंल्लिङ्गम्', 'स्त्रीलिङ्गम्', 'नपुंसकलिङ्गम्']
    vibhakti = ['प्रथमाविभक्तिः', 'द्वितीयाविभक्तिः', 'तृतीयाविभक्तिः', 'चतुर्थीविभक्तिः', 'पञ्चमीविभक्तिः', 'षष्ठीविभक्तिः', 'सप्तमीविभक्तिः', 'संबोधनविभक्तिः']
    lakAra = ['लट्', 'लुङ्', 'लङ्', 'लिट्', 'लृट्', 'लुट्', 'लृङ्', 'विधिलिङ्', 'लोट्', 'आशीर्लिङ्']
    pada_prayoga = ['परस्मैपदम्', 'आत्मनेपदम्', 'उभयपदम्', 'कर्तरि', 'कर्मणि']
                #'लट्-कर्मणि', 'लोट्-कर्मणि', 'विधिलिङ्-कर्मणि', 'लङ्-कर्मणि', 'आगमाभावयुक्तलुङ्']
    puruSha = ['उत्तमपुरुषः', 'मध्यमपुरुषः', 'प्रथमपुरुषः']
    
    def refresh(self, obj):
        return self.analyzer.session.query(type(obj)).populate_existing().get(obj.id)
              
    def map_nominal(self, obj):
        tagset = set()
        tagset.add(SanskritObject(self.lingam[obj.gender_id-1], DEVANAGARI).transcoded(SLP1))
        if obj.compounded:
            tagset.add(SanskritObject("समासपूर्वपदनामपदम्", DEVANAGARI).transcoded(SLP1))
        else:
            tagset.add(SanskritObject(self.vacanam[obj.number_id-1], DEVANAGARI).transcoded(SLP1))
            tagset.add(SanskritObject(self.vibhakti[obj.case_id-1], DEVANAGARI).transcoded(SLP1))
        return (obj.stem.name, tagset)
    
    def map_verb(self, obj):   
        tagset = set()
        newobj = self.refresh(obj)
        tagset.add(SanskritObject(self.lakAra[newobj.mode.id-1], DEVANAGARI).transcoded(SLP1))
        tagset.add(SanskritObject(self.pada_prayoga[newobj.voice.id-1], DEVANAGARI).transcoded(SLP1))
        tagset.add(SanskritObject(self.puruSha[newobj.person.id-1], DEVANAGARI).transcoded(SLP1))
        tagset.add(SanskritObject(self.vacanam[newobj.number.id-1], DEVANAGARI).transcoded(SLP1))
        return (newobj.root.name, tagset)
    
    def map_tags(self, tags):
        out = []
        for t in tags:
            if type(t) == Nominal:
                otags = self.map_nominal(t)
                if otags not in out:
                    out.append(otags)
            elif type(t) == Verb:
                out.append(self.map_verb(t))
            elif type(t) == Indeclinable:
                out.append((t.name, set(['avyayam'])))
            elif type(t) == Gerund:
                newobj = self.refresh(t)
                out.append((newobj.root.name, set(['ktvA'])))
            elif type(t) == Infinitive:
                newobj = self.refresh(t)
                out.append((newobj.root.name, set(['tumun'])))
            else:
                out.append(t)
        return out

if __name__ == "__main__":
    args=LexicalLookup.getArgs()
    if args.loglevel:
        numeric_level = getattr(logging, args.loglevel.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % args.loglevel)
        logging.basicConfig(level = numeric_level)
    SanskritDataWrapper().main(args)