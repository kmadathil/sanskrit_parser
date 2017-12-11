import logging

from flask import Blueprint
import flask_restplus
from flask_restplus import Resource

from sanskrit_parser.base.sanskrit_base import SanskritObject, SLP1
from sanskrit_parser.morphological_analyzer.SanskritMorphologicalAnalyzer import SanskritMorphologicalAnalyzer

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(asctime)s {%(filename)s:%(lineno)d}: %(message)s "
)

URL_PREFIX = '/v1'
api_blueprint = Blueprint(
    'sanskrit_parser', __name__,
    template_folder='templates'
)

api = flask_restplus.Api(app=api_blueprint, version='1.0', title='sanskrit_parser API',
                         description='For detailed intro and to report issues: see <a href="https://github.com/kmadathil/sanskrit_parser">here</a>. '
                                     'A list of REST and non-REST API routes avalilable on this server: <a href="../sitemap">sitemap</a>.',
                         default_label=api_blueprint.name,
                         prefix=URL_PREFIX, doc='/docs')

analyzer = SanskritMorphologicalAnalyzer()


def jtag(tag):
    """ Helper to translate tag to serializable format"""
    return (SanskritObject(tag[0], encoding=SLP1).devanagari(), [t.devanagari() for t in list(tag[1])])


def jtags(tags):
    """ Helper to translate tags to serializable format"""
    return [jtag(x) for x in tags]


@api.route('/tags/<string:p>')
class Tags(Resource):
    def get(self, p):
        """ Get lexical tags for p """
        pobj = SanskritObject(p, normalize=True)
        tags = analyzer.getLexicalTags(pobj)
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
        vobj = SanskritObject(v, normalize=True)
        g = analyzer.getSandhiSplits(vobj)
        if g:
            splits = g.findAllPaths(10)
            jsplits = [[ss.devanagari() for ss in s] for s in splits]
        else:
            jsplits = []
        r = {"input": v, "devanagari": vobj.devanagari(), "splits": jsplits}
        return r


@api.route('/analyses/<string:v>')
class Morpho(Resource):
    def get(self, v):
        """ Get morphological tags for v """
        vobj = SanskritObject(v, normalize=True)
        g = analyzer.getSandhiSplits(vobj, tag=True)
        if g:
            splits = g.findAllPaths(10)
        else:
            splits = []
        mres = {}
        for sp in splits:
            p = analyzer.constrainPath(sp)
            if p:
                sl = "_".join([spp.devanagari() for spp in sp])
                mres[sl] = []
                for pp in p:
                    mres[sl].append([(spp.devanagari(), jtag(pp[spp.canonical()])) for spp in sp])
        r = {"input": v, "devanagari": vobj.devanagari(), "analysis": mres}
        return r
