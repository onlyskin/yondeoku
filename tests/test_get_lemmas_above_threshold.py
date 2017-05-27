import pytest
from mock import Mock

from yondeoku._get_lemmas_above_threshold import (_get_lemmas_above_threshold,
                                      _build_occurrences_dict)

def test_it_returns_dict():
    lemmas = ['a', 'a', 'a', 'b', 'b', 'c', 'd']
    assert _build_occurrences_dict(lemmas) == {'a': 3, 'b': 2, 'c': 1, 'd': 1}

def test_above_threshold_returns_a():
    lemmas = ['a', 'a', 'a', 'b', 'b', 'c', 'd']
    threshold = 3
    assert _get_lemmas_above_threshold(lemmas, threshold) == set(['a'])

def test_above_threshold_returns_b():
    lemmas = ['a', 'a', 'b', 'b', 'b', 'c', 'd']
    threshold = 3
    assert _get_lemmas_above_threshold(lemmas, threshold) == set(['b'])

def test_above_threshold_returns_b():
    lemmas = ['a', 'a', 'b', 'b', 'b', 'c', 'd']
    threshold = 3
    assert _get_lemmas_above_threshold(lemmas, threshold) == set(['b'])

def test_above_threshold_returns_b_and_c():
    lemmas = ['c', 'c', 'b', 'b', 'b', 'c', 'd']
    threshold = 3
    assert _get_lemmas_above_threshold(lemmas, threshold) == set(['b', 'c'])

