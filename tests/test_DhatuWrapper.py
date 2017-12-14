"""
Tests for DhatuWrapper
"""
from sanskrit_parser.util import DhatuWrapper
from sanskrit_parser.base.sanskrit_base import SanskritObject, SLP1
import logging

logger = logging.getLogger(__name__)


def test_is_sakarmaka():
    s = SanskritObject("kf")
    it = s.transcoded(SLP1)
    w = DhatuWrapper.DhatuWrapper()

    is_sakarmaka = w.is_sakarmaka(it)

    assert is_sakarmaka is True