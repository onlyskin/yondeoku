import pytest

from yondeoku.overlap import normalizeRanges

def test_normalizes_empty_range():
	assert normalizeRanges([]) == []

def test_normalizes_single_item_range():
	assert normalizeRanges([[1, 3]]) == [[1, 3]]

def test_normalizes_contained_overlap():
	assert normalizeRanges([[0, 5], [2, 3], [8, 10]]) == [[0, 5], [8, 10]]

def test_normalizes_part_overlap():
	assert normalizeRanges([[0, 5], [4, 7], [9, 11]]) == [[0, 7], [9, 11]]

def test_normalizes_touching_overlap():
	assert normalizeRanges([[0, 5], [5, 7], [9, 11]]) == [[0, 7], [9, 11]]

def test_keeps_non_overlap_same():
	assert normalizeRanges([[0, 5], [6, 7]]) == [[0, 5], [6, 7]]

