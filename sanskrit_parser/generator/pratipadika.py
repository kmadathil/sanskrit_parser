from paninian_object import PaninianObject
from sanskrit_parser.base.sanskrit_base import SLP1

class Pratipadika(PaninianObject):
    """ Sanskrit Object Class: Derived From SanskritString

     Attributes:
        
    """
    def __init__(self, thing=None, linga= "pum",
                 other_tags=[], encoding=SLP1,
                 unicode_encoding='utf-8',
                 strict_io=True, replace_ending_visarga='s'):
            super().__init__(thing, encoding, unicode_encoding, strict_io, replace_ending_visarga)
            self.linga = linga
            self.inPrakriya = True
            self.setTag("prAtipadika")
            self.setTag("aNga")
            for t in other_tags:
                self.setTag(t)

    def anta(self):
        return self.canonical()[-1]


rAma = Pratipadika("rAma", "pum")
kavi = Pratipadika("kavi", "pum")
                
sarva = Pratipadika("sarva", "pum", other_tags=["sarvAdi", "sarvanAma"])
