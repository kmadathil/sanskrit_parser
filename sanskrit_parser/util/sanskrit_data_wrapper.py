# -*- coding: utf-8 -*-
'''
Wrapper around data from Sanskrit data project

@author: avinashvarna
'''

from __future__ import print_function
import logging
import sanskrit_util.analyze
import sanskrit_util.context
from sanskrit_util.schema import Nominal, Indeclinable, Verb, Gerund, Infinitive, ParticipleStem
from sanskrit_parser.util.lexical_lookup import LexicalLookup
from sanskrit_parser.base.sanskrit_base import SanskritImmutableString
from indic_transliteration import sanscript
from sanskrit_parser.util.data_manager import data_file_path


class SanskritDataWrapper(LexicalLookup):

    db_file = 'sanskrit_data.db'

    def __init__(self, logger=None):
        self.db_file = data_file_path(self.db_file)
        config = {
            "DATABASE_URI": 'sqlite:///' + self.db_file,
            "DATA_PATH": ""}
        ctx = sanskrit_util.context.Context(config)
        self.analyzer = sanskrit_util.analyze.SimpleAnalyzer(ctx)
        self.tag_cache = {}
        self.logger = logger or logging.getLogger(__name__)

    def valid(self, word):
        self.logger.debug("Checking if %s is valid", word)
        if word in self.tag_cache:
            self.logger.debug("Cache hit")
            return True
        else:
            tags = self.get_tags(word, tmap=False)
            if tags is not None:
                self.logger.debug("Found tags")
                return True
        self.logger.debug("Returning False")
        return False

    def get_tags(self, word, tmap=True):
        self.logger.debug("Looking up tags for %s", word)
        if word in self.tag_cache:
            self.logger.debug("Cache hit")
            tags = self.tag_cache[word]
            self.logger.debug("Found tags %s", tags)
        else:
            tags = self.analyzer.analyze(word)
            if tags != []:
                self.logger.debug("Found tags %s", tags)
                self.tag_cache[word] = tags
        if tmap:
            tags = self.map_tags(tags)
            self.logger.debug("Found tags %s", tags)
        if tags != []:
            return tags
        else:
            return None

    vacanam = ['एकवचनम्', 'द्विवचनम्', 'बहुवचनम्']
    lingam = ['पुंल्लिङ्गम्', 'स्त्रीलिङ्गम्', 'नपुंसकलिङ्गम्', 'त्रिलिङ्गम्']
    vibhakti = ['प्रथमाविभक्तिः', 'द्वितीयाविभक्तिः', 'तृतीयाविभक्तिः',
                'चतुर्थीविभक्तिः', 'पञ्चमीविभक्तिः', 'षष्ठीविभक्तिः',
                'सप्तमीविभक्तिः', 'संबोधनविभक्तिः']
    lakAra = ['लट्', 'लुङ्', 'लङ्', 'लिट्', 'लृट्', 'लुट्', 'लृङ्', 'विधिलिङ्', 'लोट्', 'आशीर्लिङ्', 'आगमाभावयुक्तलुङ्']
    pada_prayoga = ['परस्मैपदम्', 'आत्मनेपदम्', 'उभयपदम्', 'कर्तरि', 'कर्मणि']
    puruSha = ['उत्तमपुरुषः', 'मध्यमपुरुषः', 'प्रथमपुरुषः']
    kRdanta = {
        ('fut', 'para'): ['Satf', 'Bavizyat', 'kartari'],  # 'कर्तरिभविष्यत्कृदन्त-परस्मैपदी',
        ('fut', 'atma'): ['SAnac', 'Bavizyat', 'kartari'],  # 'कर्तरिभविष्यत्कृदन्त-आत्मनेपदी',
        ('fut', 'pass'): ['kftya', 'Bavizyat', 'karmaRi'],  # 'कर्मणिभविष्यत्कृदन्तः',
        ('pres', 'para'): ['Satf', 'kartari'],  # 'कर्तरिवर्तमानकृदन्त-परस्मैपदी',
        ('pres', 'atma'): ['SAnac', 'kartari'],  # 'कर्तरिवर्तमानकृदन्त-आत्मनेपदी',
        ('pres', 'pass'): ['SAnac', 'karmaRi'],  # 'कर्मणिवर्तमानकृदन्तः',
        ('past', 'active'): ['ktavatu', 'kartari'],  # 'कर्तरिभूतकृदन्तः',
        ('past', 'pass'): ['kta', 'karmaRi'],  # 'कर्मणिभूतकृदन्तः',
        ('perf', 'para'): ['kvasu'],  # 'पूर्णभूतकृदन्त-परस्मैपदी',
        ('perf', 'atma'): ['kAnac'],  # 'पूर्णभूतकृदन्त-आत्मनेपदी'
    }

    def refresh(self, obj):
        if hasattr(obj, "id") and obj.id is not None:
            return self.analyzer.session.query(type(obj)).populate_existing().get(obj.id)
        else:
            return obj

    def map_nominal(self, obj):
        self.logger.debug("map_nominal %s", obj)
        tagset = set()
        obj = self.refresh(obj)
#         self.logger.debug("%s, gender_id = %d", obj, obj.gender_id)
        tagset.add(SanskritImmutableString(self.lingam[obj.gender_id - 1], sanscript.DEVANAGARI))
        if obj.compounded:
            tagset.add(SanskritImmutableString("समासपूर्वपदनामपदम्", sanscript.DEVANAGARI))
        else:
            tagset.add(SanskritImmutableString(self.vacanam[obj.number_id - 1], sanscript.DEVANAGARI))
            tagset.add(SanskritImmutableString(self.vibhakti[obj.case_id - 1], sanscript.DEVANAGARI))
        stem = obj.stem
        if type(stem) == ParticipleStem:
            mode = stem.mode.abbr
            voice = stem.voice.abbr
            for t in self.kRdanta[(mode, voice)]:
                tagset.add(SanskritImmutableString(t, sanscript.SLP1))
        return (SanskritImmutableString(stem.name, sanscript.SLP1), tagset)

    def map_verb(self, obj):
        tagset = set()
        newobj = self.refresh(obj)
        tagset.add(SanskritImmutableString(self.lakAra[newobj.mode.id - 1], sanscript.DEVANAGARI))
        tagset.add(SanskritImmutableString(self.pada_prayoga[newobj.voice.id - 1], sanscript.DEVANAGARI))
        tagset.add(SanskritImmutableString(self.puruSha[newobj.person.id - 1], sanscript.DEVANAGARI))
        tagset.add(SanskritImmutableString(self.vacanam[newobj.number.id - 1], sanscript.DEVANAGARI))
        return (SanskritImmutableString(newobj.root.name, sanscript.SLP1), tagset)

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
                out.append((SanskritImmutableString(t.name, sanscript.SLP1),
                            set([SanskritImmutableString('avyayam', sanscript.SLP1)])))
            elif type(t) == Gerund:
                newobj = self.refresh(t)
                out.append((SanskritImmutableString(newobj.root.name, sanscript.SLP1),
                            set([SanskritImmutableString('ktvA', sanscript.SLP1)])))
            elif type(t) == Infinitive:
                newobj = self.refresh(t)
                out.append((SanskritImmutableString(newobj.root.name, sanscript.SLP1),
                            set([SanskritImmutableString('tumun', sanscript.SLP1)])))
            else:
                out.append(t)
        return out


if __name__ == "__main__":
    args = LexicalLookup.getArgs()
    if args.loglevel:
        numeric_level = getattr(logging, args.loglevel.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % args.loglevel)
        logging.basicConfig(level=numeric_level)
    SanskritDataWrapper().main(args)
