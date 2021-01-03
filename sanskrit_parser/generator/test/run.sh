#! /bin/bash

pytest -n 6 test_list.py
pytest -n 6 test_ajanta_pum.py
pytest -n 6 test_ajanta_stri.py
pytest -n 6 test_ajanta_napum.py
