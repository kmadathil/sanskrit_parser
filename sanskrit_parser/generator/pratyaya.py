from paninian_object import PaninianObject

class Pratyaya(PaninianObject):
    """ Sanskrit Object Class: Derived From SanskritString

     Attributes:
        
    """
    def __init__(self, thing=None, its=[], other_tags=[], encoding=None,
                 unicode_encoding='utf-8',
                 strict_io=True, replace_ending_visarga='s'):
            super().__init__(thing, encoding, unicode_encoding, strict_io, replace_ending_visarga)
            self.inPrakriya = True
            self.its = its
            self.setTag("pratyaya")
            for t in other_tags:
                self.setTag(t)
                
    def hasIt(self, it):
        return it in self.its

tuk = Pratyaya("t",its=["k"])


Ryat = Pratyaya("ya",its=["t", "R"], other_tags=["ArDaDAtuka"])
GaY = Pratyaya("a",its=["G", "Y"], other_tags=["ArDaDAtuka"])
Ric = Pratyaya("i",its=["R", "c"], other_tags=["ArDaDAtuka"])
tfc = Pratyaya("tf",its=["c"], other_tags=["ArDaDAtuka"])
Sap = Pratyaya("a",its=["S", "p"], other_tags=["sArvaDAtuka"])
tip = Pratyaya("ti",its=["p"], other_tags=["sArvaDAtuka"])
yat = Pratyaya("ya",its=["t"], other_tags=["ArDaDAtuka"])
yak = Pratyaya("ya",its=["k"], other_tags=["ArDaDAtuka"])

# nIpAtAs
AN = Pratyaya("A",its=["N"], other_tags=["nipAta"])
mAN = Pratyaya("mA",its=["N"], other_tags=["nipAta"])


# bha when applied to prAtipadikas only!
# FIXME - maybe have two yats?
yat_t = Pratyaya("ya",its=["t"], other_tags=["svAdi", "tadDita"])
zyaY_t =  Pratyaya("ya",its=["z", "Y"], other_tags=["svAdi", "tadDita"])
yaY_t =  Pratyaya("ya",its=["Y"], other_tags=["svAdi", "tadDita"])
aR_t =  Pratyaya("a",its=["R"], other_tags=["svAdi", "tadDita"])
