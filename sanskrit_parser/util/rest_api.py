from flask import Flask
from flask_restplus import Resource, Api

from sanskrit_parser.lexical_analyzer.SanskritLexicalAnalyzer import SanskritLexicalAnalyzer
from sanskrit_parser.morphological_analyzer.SanskritMorphologicalAnalyzer import SanskritMorphologicalAnalyzer
from sanskrit_parser.base.sanskrit_base import SanskritObject, SLP1

app = Flask(__name__)
api = Api(app)

analyzer = SanskritMorphologicalAnalyzer()

def jtag(tag):
    """ Helper to translate tag to serializable format"""
    return (SanskritObject(tag[0]).devanagari(),[t.devanagari() for t in list(tag[1])])

def jtags(tags):
    """ Helper to translate tags to serializable format"""
    return [jtag(x) for x in tags]

class Tags(Resource):
    def get(self,p):
        """ Get lexical tags for p """
        pobj = SanskritObject(p)
        tags = analyzer.getLexicalTags(pobj)
        if tags is not None:
            ptags = jtags(tags)
        else:
            ptags = []
        r = {"input": p, "devanagari": pobj.devanagari(),"tags": ptags}
        return r
        
class Splits(Resource):
    def get(self,v):
        """ Get lexical tags for v """
        vobj = SanskritObject(v)
        g = analyzer.getSandhiSplits(vobj)
        if g:
            splits = g.findAllPaths(10)
            jsplits = [[ss.devanagari() for ss in s] for s in splits]
        else:
            jsplits = []
        r = {"input": v, "devanagari": vobj.devanagari(),"splits": jsplits}
        return r

class Morpho(Resource):
    def get(self,v):
        """ Get morphological tags for v """
        vobj = SanskritObject(v)
        g = analyzer.getSandhiSplits(vobj,tag=True)
        if g:
            splits = g.findAllPaths(10)
        else:
            splits = []
        mres   = {}
        for sp in splits:
            p=analyzer.constrainPath(sp)
            if p:
                sl="_".join([spp.devanagari() for spp in sp])
                mres[sl]=[]
                for pp in p:
                    mres[sl].append([(spp.devanagari(),jtag(pp[spp.canonical()])) for spp in sp])
        r = {"input": v, "devanagari": vobj.devanagari(),"analysis": mres}
        return r

    
api.add_resource(Tags, '/api/tags/<p>')
api.add_resource(Splits, '/api/split/<v>')
api.add_resource(Morpho, '/api/analyze/<v>')

#Commenting for flask-restful
#@app.route('/static')
#def root():
#    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
