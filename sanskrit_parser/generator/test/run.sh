#! /bin/bash

# -n for parallel execution, worksteal to rebalance uneven test durations.
# needs 'pip install pytest-xdist'
pytest -n 8 --dist worksteal
