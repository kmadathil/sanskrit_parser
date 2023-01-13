# -*- coding: utf-8 -*-
"""
ac sandhi sutras generated through YAML processing

@author: kmadathil
"""
from sanskrit_parser.generator.process_yaml import process_yaml
import yaml
import os.path

import logging
#logger = logging.getLogger(__name__)

def SutraFactory(filename="sutras.yaml"):
    sutra_list = []
    sutra_dict = {}
    
    f = open(os.path.join(os.path.dirname(__file__), "sutras.yaml"), "r", encoding="utf-8")
    y = yaml.load(f, Loader=yaml.FullLoader)
    sutra_dict = process_yaml(y)
    sutra_list = sutra_dict.values()
    # logger.info(sutra_dict)
    f.close()
    return sutra_list

__all__ = ["SutraFactory"]
