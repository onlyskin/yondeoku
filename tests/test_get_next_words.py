import pytest
from mock import Mock

from yondeoku._get_next_words import (_filter_lemmas_by_new,
    _get_next_n_words_and_section_indices, _enumerate_unread_sections)

def test_it_filters_lemmas():
    lemmas = ['c', 'c', 'b', 'b', 'e', 'b', 'c', 'd']
    exclude_set = set(['c', 'd'])
    assert _filter_lemmas_by_new(lemmas, exclude_set) == ['b', 'b', 'e', 'b']

def test_enumerate_unread_sections():
    section1 = Mock(read=True)
    section2 = Mock(read=False)
    section3 = Mock(read=False)
    double = Mock(sections=[section1, section2, section3])
    result = _enumerate_unread_sections(double)
    assert result == [(1, section2), (2, section3)]

def test_get_next_n_words_and_section_indices_first_over_n():
    exclude_set = set([])

    section1 = Mock(read=True, lemmas=['read', 'section'])
    section2 = Mock(read=False, lemmas=['a', 'b', 'c', 'd', 'e', 'f'])
    section3 = Mock(read=False, lemmas=['a', 'b', 'c'])
    double = Mock(sections=[section1, section2, section3])

    result = _get_next_n_words_and_section_indices(double, exclude_set, 5)

    assert result['indices'] == [1]
    assert result['lemmas'] == ['a', 'b', 'c', 'd', 'e', 'f']

def test_get_next_n_words_and_section_indices_second_pushes_over_n():
    exclude_set = set([])

    section1 = Mock(read=True, lemmas=['read', 'section'])
    section2 = Mock(read=False, lemmas=['a', 'b', 'c', 'd'])
    section3 = Mock(read=False, lemmas=['a', 'b', 'c'])
    double = Mock(sections=[section1, section2, section3])

    result = _get_next_n_words_and_section_indices(double, exclude_set, 5)

    assert result['indices'] == [1]
    assert result['lemmas'] == ['a', 'b', 'c', 'd']

def test_get_next_n_words_and_section_indices_first_exactly_n():
    exclude_set = set([])

    section1 = Mock(read=True, lemmas=['read', 'section'])
    section2 = Mock(read=False, lemmas=['a', 'b', 'c', 'd', 'e'])
    section3 = Mock(read=False, lemmas=['a', 'b', 'c'])
    double = Mock(sections=[section1, section2, section3])

    result = _get_next_n_words_and_section_indices(double, exclude_set, 5)

    assert result['indices'] == [1]
    assert result['lemmas'] == ['a', 'b', 'c', 'd', 'e']

def test_get_next_n_words_and_section_indices_first_plus_second_n():
    exclude_set = set([])

    section1 = Mock(read=True, lemmas=['read', 'section'])
    section2 = Mock(read=False, lemmas=['a', 'b', 'c'])
    section3 = Mock(read=False, lemmas=['d', 'e'])
    section4 = Mock(read=False, lemmas=['d', 'e'])
    double = Mock(sections=[section1, section2, section3, section4])

    result = _get_next_n_words_and_section_indices(double, exclude_set, 5)

    assert result['indices'] == [1, 2]
    assert result['lemmas'] == ['a', 'b', 'c', 'd', 'e']

def test_get_next_n_words_and_section_indices_less_than_n_total_left():
    exclude_set = set([])

    section1 = Mock(read=True, lemmas=['read', 'section'])
    section2 = Mock(read=False, lemmas=['a', 'b', 'c'])
    section3 = Mock(read=False, lemmas=['d'])
    double = Mock(sections=[section1, section2, section3])

    result = _get_next_n_words_and_section_indices(double, exclude_set, 5)

    assert result['indices'] == [1, 2]
    assert result['lemmas'] == ['a', 'b', 'c', 'd']

def test_get_next_n_words_and_section_indices_less_than_n_total_left():
    exclude_set = set([])

    section1 = Mock(read=True, lemmas=['read', 'section'])
    section2 = Mock(read=False, lemmas=[])
    section3 = Mock(read=False, lemmas=['d'])
    double = Mock(sections=[section1, section2, section3])

    result = _get_next_n_words_and_section_indices(double, exclude_set, 5)

    assert result['indices'] == [1, 2]
    assert result['lemmas'] == ['d']

