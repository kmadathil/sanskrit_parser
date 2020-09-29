from .sutra_engine import SandhiSutra, GlobalTriggers
from .maheshvara import * 
from .guna_vriddhi import guna, vriddhi, ikoyan, ayavayav

# Sutra: "aad guRaH"
aadgunah = SandhiSutra("aad guRaH",
                       (6,1,87),
                       lambda l, r, e, f: isSavarna("a", e) and isInPratyahara("ik", f), # Condition
                       lambda e, f, lne, rnf: (lne, guna(f)+rnf), # Transformation
                       update=lambda l, r, e, f: setattr(GlobalTriggers, "uran_trigger", True) if isSavarna("f", f) else None  # State update
)

# Sutra: "vfdDireci"
vriddhirechi = SandhiSutra("vfdDireci",
                           (6,1,88),
                           lambda l, r, e, f: isSavarna("a", e) and  isInPratyahara("ec",f), # Condition
                           lambda e, f, lne, rnf: (lne, vriddhi(f)+rnf), # Transformation
)

# # Sutra: uraR raparaH
uranraprah = SandhiSutra("uraRraparaH",
                         (1,1,51),
                         None, # Condition
                         lambda e, f, lne, rnf: (lne+e, f+"r"+rnf), # Xform
                         trig=lambda : GlobalTriggers.uran_trigger, # Trigger
                         update=lambda l, r, e, f: setattr(GlobalTriggers, "uran_trigger", False) # State Update
)

# # Sutra  ikoyaRaci
ikoyanaci = SandhiSutra("ikoyaRaci",
                        (6,1,77),
                        lambda l, r, e, f: isInPratyahara("ik",e) and isInPratyahara("ac",f), # Condition
                        lambda e, f, lne, rnf: (lne+ikoyan(e), f+rnf), #Operation
)

# # Sutra ecoyavAyAvaH
ecoyavayavah = SandhiSutra("ecoyavAyAvaH",(6,1,78),
                           lambda l, r, e, f: isInPratyahara("ec",e) and isInPratyahara("ac",f), # Condition
                           lambda e, f, lne, rnf: (lne+ayavayav(e), f+rnf), #Operation                  
)


# # Sutra akaHsavarRedIrGaH
savarnadirgha = SandhiSutra("akaHsavarRedIrGaH",
                             (6,1,101),
                            lambda l, r, e, f: isInPratyahara("ak",e) and isSavarna(e, f), # Condition
                            lambda e, f, lne, rnf: (lne+e.upper(), rnf), #Operation                  
)


# # Sutra eNaHpadAntAdati
engahpadantadati = SandhiSutra("eNaHpadAntAdati",
                               (6,1,109),
                               lambda l, r, e, f: isInPratyahara("eN",e) and isSavarna("at",f), # Condition
                               lambda e, f, lne, rnf: (lne+e, rnf), #Operation                  
)            


sutra_list = [aadgunah, vriddhirechi, uranraprah, ikoyanaci, ecoyavayavah, savarnadirgha, engahpadantadati]

__all__ = ["sutra_list"]
