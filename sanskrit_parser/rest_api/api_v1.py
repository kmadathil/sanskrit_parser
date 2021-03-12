from flask import Blueprint
import flask_restx
from flask_restx import Resource
# import subprocess
# from os import path
# from flask import redirect

from sanskrit_parser.base.sanskrit_base import SanskritObject, SLP1
from sanskrit_parser.parser.sandhi_analyzer import LexicalSandhiAnalyzer
from sanskrit_parser.parser.datastructures import VakyaGraph

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
            SanskritObject(label, encoding=SLP1).devanagari(strict_io=False),
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
        vobj = SanskritObject(v, strict_io=True, replace_ending_visarga=None)
        g = analyzer.getSandhiSplits(vobj)
        if g:
            splits = g.find_all_paths(10)
            jsplits = [[ss.devanagari(strict_io=False) for ss in s] for s in splits]
        else:
            jsplits = []
        r = {"input": v, "devanagari": vobj.devanagari(), "splits": jsplits}
        return r


@api.route('/analyses/<string:v>')
class Morpho(Resource):
    def get(self, v):
        """ Get morphological tags for v """
        vobj = SanskritObject(v, strict_io=True, replace_ending_visarga=None)
        g = analyzer.getSandhiSplits(vobj, tag=True)
        if g:
            splits = g.find_all_paths(10, score=True)
        else:
            splits = []
        mres = {}
        dots = {}
        for sp in splits:
            # bn = f"{randint(0,9999):4}"
            vg = VakyaGraph(sp, max_parse_dc=5)
            sl = "_".join([n.devanagari(strict_io=False)
                           for n in sp])
            for (ix, p) in enumerate(vg.parses):
                if sl not in mres:
                    mres[sl] = []
                t = []
                for n in p:
                    preds = list(p.predecessors(n))
                    if preds:
                        pred = preds[0]  # Only one
                        lbl = list(p[pred][n].values())[0]['label']
                        t.append(jedge(pred, n, lbl))
                    else:
                        t.append(jnode(n))
                mres[sl].append(t)
            dots[sl] = {}
            try:
                dots[sl] = vg.get_dot_dict()
            except Exception:
                pass
        r = {"input": v, "devanagari": vobj.devanagari(), "analysis": mres,
             "dot": dots}
        return r

    # @api.route('/graph/<string:v>')
    # class Graph(Resource):
    #     def get(self, v):
    #         """ Get graph for v """
    #         if not path.exists(f"static/{v}.dot.png"):
    #             subprocess.run(f"dot -Tpng static/{v}.dot -O", shell=True)
    #         return redirect(f"/static/{v}.dot.png")
