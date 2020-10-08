from paninian_object import PaninianObject

class Pratyaya(PaninianObject):
    """ Sanskrit Object Class: Derived From SanskritString

     Attributes:
        
    """
    def __init__(self, thing=None, its=[], encoding=None, unicode_encoding='utf-8',
                 strict_io=True, replace_ending_visarga='s'):
            super().__init__(thing, encoding, unicode_encoding, strict_io, replace_ending_visarga)
            self.inPrakriya = True
            self.its = its
            self.setTag("pratyayaH")

tuk = Pratyaya("t",its=["k"])
