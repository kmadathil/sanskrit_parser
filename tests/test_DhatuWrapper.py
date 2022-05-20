"""
Tests for DhatuWrapper
"""
from indic_transliteration import sanscript
from sanskrit_parser.util import DhatuWrapper
from sanskrit_parser.base.sanskrit_base import SanskritImmutableString
import logging

logger = logging.getLogger(__name__)


def test_is_sakarmaka():
    s = SanskritImmutableString("kf")
    it = s.transcoded(sanscript.SLP1)
    w = DhatuWrapper.DhatuWrapper()

    is_sakarmaka = w.is_sakarmaka(it)

    assert is_sakarmaka is True


def test_is_sakarmaka_for_dvikarmaka():
    s = SanskritImmutableString("nI")
    it = s.transcoded(sanscript.SLP1)
    w = DhatuWrapper.DhatuWrapper()

    is_sakarmaka = w.is_sakarmaka(it)

    assert is_sakarmaka is True
