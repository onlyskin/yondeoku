import pytest

from yondeoku.gBlock import gBlock
from yondeokuApp import Block

test_model_block = Block(language='pl', text=u'przyjaciela brzmi. herbaty, stali! psom, lekarkami.', read_ranges='[[0, 3]]')
test_gblock = gBlock(test_model_block)
empty_block = Block(language='pl', text='testing', read_ranges='[]')

block_with_unsupported = Block(language='it', text='testing', read_ranges='[]')
block_with_bad_range = Block(language='pl', text='testing', read_ranges='[[0, 1, 2]]')

def test_gBlock_created_and_has_lang_and_text():
	assert test_gblock.language == 'pl' and test_gblock.text == u'przyjaciela brzmi. herbaty, stali! psom, lekarkami.'

def test_unsupported_lang_raises_error():
	with pytest.raises(ValueError):
		gBlock(block_with_unsupported)

def test_unsupported_range_len_raises_error():
	with pytest.raises(ValueError):
		gBlock(block_with_bad_range)

def test_it_has_empty_read_ranges():
	assert gBlock(empty_block).readRanges == []

def test_it_has_sections():
	assert len(test_gblock.sections) == 3

def test_it_has_read_sections():
	assert len(test_gblock.readSections) == 3

def test_it_has_read_ranges():
	assert test_gblock.readRanges == [[0, 3]]

def test_section_marked_as_read():
	mb = Block(language='pl', text=u'testing. this', read_ranges='[[0, 8]]')
	gb = gBlock(mb)
	assert gb.readSections == [True, False]

def test_section_not_marked_as_read():
	mb = Block(language='pl', text=u'testing. this', read_ranges='[[3, 10]]')
	gb = gBlock(mb)
	assert gb.readSections == [False, False]

