#! /usr/bin/env python                                                        
# -*- coding: utf-8 -*-
import pytest

from yondeoku.Section import Section
from yondeoku.Lemma import Lemma
from yondeoku.polish.plLemmatizer import testing_plLemmatizer
from yondeoku.polish.Lemmatizer import Lemmatizer

def test_it_has_lang():
	assert testing_plLemmatizer().language == 'pl'

def test_lemmatize_():
	test_section = Section(0, 15, u'stali psom')
	assert testing_plLemmatizer().lemmatize(test_section) == {Lemma(u'pies'), Lemma(u'stać'), Lemma(u'stal'), Lemma(u'stały')}
