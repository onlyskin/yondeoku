import pytest

from yondeoku.define import makeDefinitionListFromLemmaList
from yondeoku.Lemma import Lemma

def test_returns_empty_list_when_empty_list_passed():
	result = makeDefinitionListFromLemmaList('pl', [])
	assert result == []

def test_raises_value_error_when_language_not_implemented():
	with pytest.raises(ValueError):
		makeDefinitionListFromLemmaList('zz', [])

def test_returns_length_three_object_when_passed_in_three_lemmas():
	result = makeDefinitionListFromLemmaList('pl', [Lemma('ochrona'), Lemma('pomidor'), Lemma('klucz')])
	assert len(result) == 3
