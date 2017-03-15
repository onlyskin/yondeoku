import pytest

from yondeoku.polish.plDefiner import plDefiner

def test_it_has_lang():
	assert plDefiner().language == 'pl'
