
from sanskrit_parser.generator.antaranga_prakriya import AntarangaPrakriya
from sanskrit_parser.generator.prakriya import HierPrakriya
import logging

logger = logging.getLogger(__name__)


def PrakriyaFactory(name, sutra_list, inputs):
    ''' Factory Method for Prakriya '''
    PrakriyaDict = {
        "HierPrakriya": HierPrakriya,
        "AntarangaPrakriya": AntarangaPrakriya
    }
    default = "AntarangaPrakriya"
    #default = "HierPrakriya"
    if name in PrakriyaDict:
        p = PrakriyaDict[name](sutra_list, inputs)
        logger.debug(f"Using Prakriya: {p.name()}")
        return p
    else:
        p = PrakriyaDict[default](sutra_list, inputs)
        logger.debug(f"Using Default Prakriya: {p.name()}")
        return p

