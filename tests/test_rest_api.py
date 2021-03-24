# -*- coding: utf-8 -*-
"""
Tests for the rest api
"""

from __future__ import absolute_import

import logging

import pytest
import json

from sanskrit_parser.rest_api import run

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(asctime)s {%(filename)s:%(lineno)d}: %(message)s "
)


@pytest.fixture(scope='module')
def app_fixture(request):
    app = run.app.test_client()
    logging.debug(str(app))
    return app


def test_analyses(app_fixture):
    url = "/sanskrit_parser/v1/parse-presegmented/astyuttarasyAm"
    response = app_fixture.get(url)
    analysis = json.loads(response.data)
    logging.debug(str(analysis))
    assert len(analysis["analysis"]) > 0


def test_splits(app_fixture):
    url = "/sanskrit_parser/v1/splits/astyuttarasyAm"
    response = app_fixture.get(url)
    split = json.loads(response.data)
    logging.debug(str(split))
    assert len(split["splits"]) > 0
