from sanskrit_parser.base.sanskrit_base import SanskritObject, SanskritImmutableString

class PaninianObject(SanskritObject):
        """ Paninian Object Class: Derived From SanskritObject

        Attributes:
        
        """
        def __init__(self, thing=None, encoding=None, unicode_encoding='utf-8',
                 strict_io=True, replace_ending_visarga='s'):
            super().__init__(thing, encoding, unicode_encoding, strict_io, replace_ending_visarga)
            self.inPrakriya = True
        # Prakriya Related Tags are ephemeral
        def hasTag(self, t):
                return t in self.tags
        def deleteTag(self,t):
                return self.tags.remove(t)
        def setTag(self, t):
                if t not in self.tags:
                        self.tags.append(t)
                return t
        def fix(self):
                self.inPrakriya = False

        def isPada(self):
                return self.hasTag("pada")
