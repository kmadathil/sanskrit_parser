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

# bha when applied to prAtipadikas only!
# FIXME - maybe have two yats?
yat = Pratyaya("ya",its=["t"], other_tags=["Ba"])
Ryat = Pratyaya("ya",its=["t", "R"])
GaY = Pratyaya("a",its=["G", "Y"])
Ric = Pratyaya("i",its=["R", "c"])
