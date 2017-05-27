import pytest
from mock import Mock

from yondeokuApp import _get_all_read_sections, _get_lemmas_from_sections

def test_it_returns_sections():
    double = [
        Mock(sections=[Mock(read=True), Mock(read=False), Mock(read=False)]),
        Mock(sections=[Mock(read=True), Mock(read=True), Mock(read=False)])
    ]
    assert len(_get_all_read_sections(double)) == 3

def test_it_returns_lemmas():
    double = [
        Mock(lemmas=[1, 2, 3]),
        Mock(lemmas=[4, 5, 6])
    ]
    assert _get_lemmas_from_sections(double) == [1, 2, 3, 4, 5, 6]

