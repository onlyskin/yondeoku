#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from yondeoku.makeSections import makeSections

ja_sentence_breakers = [u'。', u'！', u'？']
ja_end_quote = u'」'

pl_sentence_breakers = [u'\.', u'!', u'\?']
pl_end_quote = u'”'

def test_make_sections_returns_one_section():
	text = u'思う。'
	result = makeSections(text, ja_sentence_breakers, ja_end_quote)
	assert len(result) == 1

def test_make_sections_returns_two_sections():
	text = u'''でも、どんない。\n思う。'''
	result = makeSections(text, ja_sentence_breakers, ja_end_quote)
	assert len(result) == 2

def test_make_sections_returns_three_sections():
	text = u'''とは、すった。\n\nしかし！　そうしてた。'''
	result = makeSections(text, ja_sentence_breakers, ja_end_quote)
	assert len(result) == 3

def test_Section_blockRef():
	text = u'''でも、どんない。\n思う。'''
	result = makeSections(text, ja_sentence_breakers, ja_end_quote)
	assert result[1].blockRef == [9, 12]

def test_Section_blockRef():
	text = u'''でも、どんない。\n思う。'''
	result = makeSections(text, ja_sentence_breakers, ja_end_quote)
	assert result[0].blockRef == [0, 9]

def test_Section_blockref_with_trailing_section():
	text = u'''でもない。思う'''
	result = makeSections(text, ja_sentence_breakers, ja_end_quote)
	assert result[1].blockRef == [5, 7] and result[1].text == u'思う'

def test_Section_text():
	text = u'''でも、どんない。\n思う。'''
	result = makeSections(text, ja_sentence_breakers, ja_end_quote)
	assert result[1].text == u'思う。'

def test_make_sections_returns_three_sections():
	text = u'''Czarne, zżarte. Ich. „Z chłop!”'''
	result = makeSections(text, pl_sentence_breakers, pl_end_quote)
	assert len(result) == 3

def it_returns_one_section():
	text = u'testing'
	assert makeSections(text, pl_sentence_breakers, pl_end_quote).text == u'testing'

def test_it_groups_two_new_lines_with_first_section():
	text = u'''でも、どんない。\n\n思う。'''
	result = makeSections(text, ja_sentence_breakers, ja_end_quote)
	assert result[1].text == u'思う。'
