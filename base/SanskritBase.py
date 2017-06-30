#!/usr/bin/env python
from indic_transliteration import sanscript
from indic_transliteration import detect

# Wrap scheme names defined in sanscript
BENGALI = sanscript.BENGALI
DEVANAGARI = sanscript.DEVANAGARI
GUJARATI = sanscript.GUJARATI
GURMUKHI = sanscript.GURMUKHI
KANNADA = sanscript.KANNADA
MALAYALAM = sanscript.MALAYALAM
ORIYA = sanscript.ORIYA
TAMIL = sanscript.TAMIL
TELUGU = sanscript.TELUGU
HK = sanscript.HK
IAST = sanscript.IAST
ITRANS = sanscript.ITRANS
KOLKATA = sanscript.KOLKATA
SLP1 = sanscript.SLP1
VELTHUIS = sanscript.VELTHUIS
WX = sanscript.WX

# Dict defined so autodetect can work
SCHEMES={
    'BENGALI':BENGALI,
    'DEVANAGARI':DEVANAGARI,
    'GUJARATI':GUJARATI,
    'GURMUKHI':GURMUKHI,
    'KANNADA':KANNADA,
    'MALAYALAM':MALAYALAM,
    'ORIYA':ORIYA,
    'TAMIL':TAMIL,
    'TELUGU':TELUGU,
    'HK':HK,
    'IAST':IAST,
    'ITRANS':ITRANS,
    'KOLKATA':KOLKATA,
    'SLP1':SLP1,
    'VELTHUIS':VELTHUIS,
    'WX':WX
}

class SanskritObject(object):
    """ Sanskrit Object Class: Base of the class hierarcy
        
        Attributes:
           thing(str)   : thing to be represented
           encoding(str): SanskritBase encoding of thing as passed (eg: SanskritBase.HK, SanskritBase.DEVANAGARI)
        Args:
           thing(str):    As above
           encoding(str): As above
    
    """
    def __init__(self,thing=None,encoding=None):
        self.thing=thing
        self.encoding=encoding
        if self.encoding is None:
            if thing is not None:
                # Autodetect Encoding
                self.encoding=SCHEMES[detect.detect(self.thing)]

    def transcoded(self,encoding=None):
        """ Return a transcoded version of self

            Args:
              encoding(SanskritObject.Scheme): 
            Returns:
              str: transcoded version
        """
        return sanscript.transliterate(self.thing,self.encoding,encoding)
    def __str__(self):
        return self.transcoded(HK)

if __name__ == "__main__":
    import argparse
    from gooey import GooeyParser, Gooey
     #@Gooey
    def getArgs():
        """
          Argparse routine. 
          Returns args variable
        """
        # Parser Setup
        parser = GooeyParser(description='SanskritObject')
        # Babylon ti~Nanta data
        parser.add_argument('data',type=str,default="idam adbhutam")

        return parser.parse_args()

    def main():
        args=getArgs()
        print args.data
        s=SanskritObject(args.data,HK)
        print s.transcoded(DEVANAGARI)
    main()
    
