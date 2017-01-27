#! /usr/bin/env python                                                        
# -*- coding: utf-8 -*-

from unittest import TestCase

from yondeoku.polish.Lemmatizer import Lemmatizer

class TestLemmatizer(TestCase):

	#instantiates the Lemmatizer once for all tests
	@classmethod
	def setUpClass(cls):
		cls.Lemmatizer = Lemmatizer('mock/testDict.json')

	def test_has_lemma_dict(self):
		self.assertEquals(
			self.Lemmatizer.lemmaDict[u'psom'],
			[u'pies']
			)

	def test_word_yields_inflections(self):
		self.assertEquals(
			self.Lemmatizer.lookupLemma(u'lekarkami'),
			[u'lekarka']
			)

	def test_word_not_in_dict_returns_self_in_list(self):
		self.assertEquals(
			self.Lemmatizer.lookupLemma(u'awerioawer'),
			[u'awerioawer']
		)