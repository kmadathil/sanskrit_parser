# -*- coding: utf-8 -*-
"""
Utils to manage the data files included in the package

"""

import importlib_resources
import atexit
from contextlib import ExitStack


def data_file_path(filename):
    file_manager = ExitStack()
    atexit.register(file_manager.close)
    ref = importlib_resources.files('sanskrit_parser') / 'data' / filename
    path = file_manager.enter_context(
        importlib_resources.as_file(ref))
    return str(path)
