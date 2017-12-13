# -*- coding: utf-8 -*-
"""
Tests for the ullekhanam API.
"""

from __future__ import absolute_import

import logging

import pytest
import json

from sanskrit_parser.rest_api.run import app

logging.basicConfig(
  level=logging.DEBUG,
  format="%(levelname)s: %(asctime)s {%(filename)s:%(lineno)d}: %(message)s "
)


@pytest.fixture(scope='module')
def app_fixture(request):
  app = run.app.test_client()
  return app


def test_analyses(app_fixture):
  url = "analyses/astyuttarasyAm"
  response = app_fixture.get(url)
  analysis = json.loads(response.data)
  log.debug(str(analysis))
  assert analysis.__len__() > 0

def test_splits(app_fixture):
  url = "splits/astyuttarasyAm"
  response = app_fixture.get(url)
  split = json.loads(response.data)
  log.debug(str(split))
  assert split.__len__() > 0

