import pytest

from yondeoku.japanese.jaDefiner import jaDefiner

def test_it_has_lang():
	assert jaDefiner().language == 'ja'
