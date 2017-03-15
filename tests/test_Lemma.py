import pytest

from yondeoku.Lemma import Lemma

def test_it_hashes_the_same():
	lemma1 = Lemma(u'test')
	lemma2 = Lemma (u'test')
	test_set = {lemma1, lemma2}
	assert len(test_set) == 1