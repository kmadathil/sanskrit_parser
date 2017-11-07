from flask import Flask
from flask_restful import Resource, Api

from sanskrit_parser.lexical_analyzer.SanskritLexicalAnalyzer import SanskritLexicalAnalyzer
from sanskrit_parser.morphological_analyzer.SanskritMorphologicalAnalyzer import SanskritMorphologicalAnalyzer
from sanskrit_parser.base.SanskritBase import SanskritObject, SLP1

app = Flask(__name__)
api = Api(app)

analyzer = SanskritMorphologicalAnalyzer()

def jtag(tag):
    """ Helper to translate tag to serializable format"""
    return (tag[0],[str(t) for t in list(tag[1])])

def jtags(tags):
    """ Helper to translate tags to serializable format"""
    return [jtag(x) for x in tags]

class Tags(Resource):
    def get(self,p):
        """ Get lexical tags for p """
        pobj = SanskritObject(p)
        tags = analyzer.getLexicalTags(pobj)
        r = {"input": p, "canonical": pobj.canonical(),"tags": jtags(tags)}
        return r
        
class Splits(Resource):
    def get(self,v):
        """ Get lexical tags for v """
        vobj = SanskritObject(v)
        splits = analyzer.getSandhiSplits(vobj).findAllPaths(10)
        jsplits = [str(s) for s in splits]
        r = {"input": v, "canonical": vobj.canonical(),"tags": jsplits}
        return r

class Morpho(Resource):
    def get(self,v):
        """ Get morphological tags for v """
        vobj = SanskritObject(v)
        splits = analyzer.getSandhiSplits(vobj,tag=True).findAllPaths(10)
        mres   = {}
        for sp in splits:
            p=analyzer.constrainPath(sp)
            if p:
                sl="_".join([str(spp) for spp in sp])
                mres[sl]=[]
                for pp in p:
                    mres[sl].append([(str(spp),jtag(pp[str(spp)])) for spp in sp])
        r = {"input": v, "canonical": vobj.canonical(),"tags": mres}
        return r

    
api.add_resource(Tags, '/tags/<p>')
api.add_resource(Splits, '/split/<v>')
api.add_resource(Morpho, '/analyze/<v>')

if __name__ == '__main__':
    app.run(debug=True)
