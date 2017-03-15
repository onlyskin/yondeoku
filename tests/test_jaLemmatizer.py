#! /usr/bin/env python                                                        
# -*- coding: utf-8 -*-
import pytest

from yondeoku.Section import Section
from yondeoku.Lemma import Lemma
from yondeoku.japanese.jaLemmatizer import jaLemmatizer

def test_it_has_lang():
	assert jaLemmatizer().language == 'ja'

def test_lemmatize_():
	test_section = Section(0, 2, u'私が')
	assert jaLemmatizer().lemmatize(test_section) == {Lemma(u'私'), Lemma(u'が')}
