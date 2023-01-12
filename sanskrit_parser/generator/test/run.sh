#! /bin/bash

# -n for parallel execution.
# needs 'pip install pytest-xdist'
pytest -n 6 test_list.py
pytest -n 6 test_ajanta_pum.py
pytest -n 6 test_ajanta_stri.py
pytest -n 6 test_ajanta_napum.py
