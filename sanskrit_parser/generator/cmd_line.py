# -*- coding: utf-8 -*-
"""
@author: Karthik Madathil (github: @kmadathil)

"""
from os.path import dirname, basename, splitext, join
from argparse import ArgumentParser, Action
import logging
from sanskrit_parser.base.sanskrit_base import SLP1, DEVANAGARI
from sanskrit_parser.generator.paninian_object import PaninianObject
from sanskrit_parser.generator.prakriya import Prakriya, PrakriyaVakya
from sanskrit_parser.generator.pratyaya import *
from sanskrit_parser.generator.dhatu import *
from sanskrit_parser.generator.pratipadika import *
from sutras_yaml import sutra_list
from sanskrit_parser import enable_file_logger, enable_console_logger

logger = logging.getLogger(__name__)

def run_pp(s):
    pl = []
    # Assemble list of inputs
    for i in range(len(s)):
        def _gen_obj(s, i):
            if isinstance(s[i], tuple) or isinstance(s[i], list):
                l = [_gen_obj(s[i], ii) for (ii, ss) in enumerate(s[i])]
            else:
                l = s[i]
            return l
        l = _gen_obj(s, i)
        pl.append(l)
    p = Prakriya(sutra_list,PrakriyaVakya(pl))
    p.execute()
    p.describe()
    o = p.output()
    return o

last_option = False

class CustomAction(Action):
       def __init__(self, option_strings, dest, nargs=None, **kwargs):
           # if nargs is not None:
           #   raise ValueError("nargs not allowed")
           super(CustomAction, self).__init__(option_strings, dest, nargs, **kwargs)
           logger.debug(f"Initializing CustomAction {option_strings}, {dest}")
       def __call__(self, parser, namespace, values, option_string=None):
           logger.debug('%r %r %r' % (namespace, values, option_string))
           global last_option
           assert not last_option, f"Option {option_string} added after avasana"
           if getattr(namespace, self.dest) is None:
               _n = []
               # This tracks the hierarchical input list
               setattr(namespace, self.dest, _n)
               # Last item of this is always the current level of the input
               setattr(namespace, "pointer", [_n])
           if values is not None:
               if isinstance(values, str):
                   values = [values]
               for v in values:
                   assert v in globals(), f"{v} is not defined!"
                   getattr(namespace, "pointer")[-1].append(globals()[v])
           else:
               if option_string == "-o": # Open
                   _l = []
                   # Add a new level at the end of current list
                   getattr(namespace, "pointer")[-1].append(_l)
                   # Designate new list as current list
                   getattr(namespace, "pointer").append(_l)
               elif option_string == "-c": # Close
                   # Current is updated to previous
                   getattr(namespace, "pointer").pop()
               elif option_string == "-a": # AvasAna
                   # Add avasana
                   l = getattr(namespace, self.dest)
                   setattr(namespace, self.dest, [l, avasAna])
                   last_option = True
               else:
                   logger.error(f"Unrecognized Option {option_string}")
class CustomActionString(Action):
       def __init__(self, option_strings, dest, nargs=None, encoding=SLP1, **kwargs):
           # if nargs is not None:
           #   raise ValueError("nargs not allowed")
           self.encoding = encoding
           super(CustomActionString, self).__init__(option_strings, dest, nargs, **kwargs)
           logger.debug(f"Initializing CustomAction {option_strings}, {dest}")
       def __call__(self, parser, namespace, values, option_string=None):
           global last_option
           assert not last_option, f"Option {option_string} added after avasana"
           def _exec(value):
               # Shortcuts for two input tests not using predefined objects
               # If a string in the first place ends with * it's an anga
               # Else it's a pada
               # For everything else, use predefined objects
               if (value[-1] == "*"):
                   value =  value[:-1]
                   value = PaninianObject(value, encoding)
                   value.setTag("aNga")
               elif (value[-1] == "_"):
                   value =  value[:-1]
                   value = PaninianObject(value, encoding)
                   value.setTag("pada")
               else:
                   value = PaninianObject(value, encoding)
               getattr(namespace, "pointer")[-1].append(value) 

           encoding = self.encoding
           logger.info('%r %r %r' % (namespace, values, option_string))
           if getattr(namespace, self.dest) is None:
               _n = []
               # This tracks the hierarchical input list
               setattr(namespace, self.dest, _n)
               # Last item of this is always the current level of the input
               setattr(namespace, "pointer", [_n])
           if isinstance(values, list):
               for v in values:
                   _exec(v)
           else:
               _exec(values)

def get_args(argv=None):
    """
      Argparse routine.
      Returns args variable
    """

    parser = ArgumentParser(description='Paninian Generator: Prakriti + Pratyaya')
    # String to encode
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('-p', '--pratyaya', nargs="+", dest="inputs", action=CustomAction)
    parser.add_argument('-d', '--dhatu', dest="inputs", action=CustomAction)
    parser.add_argument('-t', '--pratipadika', dest="inputs", action=CustomAction)
    parser.add_argument('-s', '--string', nargs="+", dest="inputs", encoding=SLP1, action=CustomActionString)
    parser.add_argument('-o', nargs="?", dest="inputs",action=CustomAction, help="Open bracket") # Open Brace
    parser.add_argument('-c', nargs="?", dest="inputs",action=CustomAction, help="Close bracket")
    parser.add_argument('-a', nargs="?", dest="inputs",action=CustomAction, help="Avasana")

    return parser.parse_args(argv)

def cmd_line():
    # Logging
    enable_console_logger()
    args = get_args()
    if args.debug:
        enable_file_logger(level=logging.DEBUG)
    logger.info(f"Inputs {args.inputs}")
    for i in args.inputs:
        def _i(x):
            if isinstance(x, list):
                for _x in x:
                    _i(_x)
            else:
                logger.info(f"{x} {x.tags}")
        _i(i)            
    logger.info("End Inputs")
    run_pp(args.inputs)
