from sanskrit_parser.generator.process_yaml import process_yaml
import yaml

import logging
logger = logging.getLogger(__name__)

sutra_list = []
sutra_dict = {}

f = open("ach_sandhi.yaml", "r")
y = yaml.load(f, Loader=yaml.FullLoader)
sutra_dict = process_yaml(y)    
sutra_list = sutra_dict.values()
logger.info(sutra_dict)

__all__ = ["sutra_list", "sutra_dict"]
