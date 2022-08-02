from flask import Blueprint
import flask_restx
from flask_restx import Resource
from flask import request
# import subprocess
# from os import path
# from flask import redirect
from indic_transliteration import sanscript
from sanskrit_parser.base.sanskrit_base import SanskritObject
from sanskrit_parser.parser.sandhi_analyzer import LexicalSandhiAnalyzer
from sanskrit_parser import __version__
from sanskrit_parser import Parser

URL_PREFIX = '/v1'
api_blueprint = Blueprint(
    'sanskrit_parser', __name__,
    template_folder='templates'
)

api = flask_restx.Api(app=api_blueprint, version='1.0', title='sanskrit_parser API',
                      description='For detailed intro and to report issues: see <a href="https://github.com/kmadathil/sanskrit_parser">here</a>. '
                      'A list of REST and non-REST API routes avalilable on this server: <a href="../sitemap">sitemap</a>.',
                      default_label=api_blueprint.name,
                      prefix=URL_PREFIX, doc='/docs')

analyzer = LexicalSandhiAnalyzer()


def jedge(pred, node, label):
    return (node.pada.devanagari(strict_io=False),
            jtag(node.getMorphologicalTags()),
            SanskritObject(label, encoding=sanscript.SLP1).devanagari(strict_io=False),
            pred.pada.devanagari(strict_io=False))


def jnode(node):
    """ Helper to translate parse node into serializable format"""
    return (node.pada.devanagari(strict_io=False),
            jtag(node.getMorphologicalTags()), "", "")


def jtag(tag):
    """ Helper to translate tag to serializable format"""
    return (tag[0].devanagari(strict_io=False), [t.devanagari(strict_io=False) for t in list(tag[1])])


def jtags(tags):
    """ Helper to translate tags to serializable format"""
    return [jtag(x) for x in tags]


@api.route('/version/')
class Version(Resource):
    def get(self):
        """Library Version"""
        r = {"version": str(__version__)}
        return r


@api.route('/tags/<string:p>')
class Tags(Resource):
    def get(self, p):
        """ Get lexical tags for p """
        pobj = SanskritObject(p, strict_io=False)
        tags = analyzer.getMorphologicalTags(pobj)
        if tags is not None:
            ptags = jtags(tags)
        else:
            ptags = []
        r = {"input": p, "devanagari": pobj.devanagari(), "tags": ptags}
        return r


@api.route('/splits/<string:v>')
class Splits(Resource):
    def get(self, v):
        """ Get lexical tags for v """
        strict_p = True
        if request.args.get("strict") == "false":
            strict_p = False
        vobj = SanskritObject(v, strict_io=strict_p, replace_ending_visarga=None)
        g = analyzer.getSandhiSplits(vobj)
        if g:
            splits = g.find_all_paths(10)
            # We don't get output with visargas here.
            # Why? Because this will need to be parsed later, and we need to distinguish s/r
            # We rely on the UI to handle display correctly
            jsplits = [[ss.devanagari(strict_io=True) for ss in s] for s in splits]
        else:
            jsplits = []
        r = {"input": v, "devanagari": vobj.devanagari(), "splits": jsplits}
        return r


@api.route('/parse-presegmented/<string:v>')
class Parse_Presegmented(Resource):
    def get(self, v):
        """ Parse a presegmented sentence """
        strict_p = True
        if request.args.get("strict") == "false":
            strict_p = False
        vobj = SanskritObject(v, strict_io=strict_p, replace_ending_visarga=None)
        # We set strict_io to False so we get output with visargas
        # If further processing is desired, this needs to be set to True
        # And the UI must handle display
        parser = Parser(input_encoding=sanscript.SLP1,
                        output_encoding=sanscript.DEVANAGARI,
                        strict_io=False,   
                        replace_ending_visarga='s')
        mres = []
        for split in parser.split(vobj.canonical(), limit=10, pre_segmented=True):
            parses = list(split.parse(limit=10))
            sdot = split.to_dot()
            mres = [x.serializable() for x in parses]
            pdots = [x.to_dot() for x in parses]
        r = {"input": v, "devanagari": vobj.devanagari(), "analysis": mres,
             "split_dot": sdot,
             "parse_dots": pdots}
        return r


@api.route('/presegmented/<string:v>')
class Presegmented(Resource):
    def get(self, v):
        """ Presegmented Split """
        vobj = SanskritObject(v, strict_io=True, replace_ending_visarga=None)
        parser = Parser(input_encoding=sanscript.SLP1,
                        output_encoding=sanscript.DEVANAGARI,
                        replace_ending_visarga='s')
        splits = parser.split(vobj.canonical(), limit=10, pre_segmented=True)
        r = {"input": v, "devanagari": vobj.devanagari(), "splits": [x.serializable()['split'] for x in splits]}
        return r
