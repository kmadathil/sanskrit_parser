#!/usr/bin/env python
# -*- encoding: utf-8 -*-


def pytest_addoption(parser):
    """Custom options for pytest command line
    """
    # Add an option to limit number of tests generated.
    parser.addoption("--test-count", action="store", default=0,
                     help="Number of tests to generate")


def get_testcount(config):
    """Gets number of tests to generate.

    :param config: pytest configuration
    """
    return int(config.getoption("--test-count"))
