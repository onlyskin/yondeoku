#! /usr/bin/env python                                                        
# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import patch

from os.path import isfile
import os

from yondeoku.polish.User import User
from yondeoku.polish.Block import Block
from yondeoku.polish.Token import Token
from yondeoku.polish.Lemmatizer import Lemmatizer
from yondeoku.polish.settings import DATA_PATH

test_user_name = u'test_get_read_lemmas'

class TestUser(TestCase):

	@classmethod
	def setUpClass(cls):
		cls.myLemmatizer = Lemmatizer(u'mock/testDict.json')
		cls.test_user = User(test_user_name)
		test_user = cls.test_user
		block_1 = Block(u'przyjaciela, brzmisz.', cls.myLemmatizer)
		block_2 = Block(u'psom lekarkami brzmisz', cls.myLemmatizer)
		block_1.setReadTokens(0, len(block_1.text))
		block_2.setReadTokens(11, len(block_2.text))
		test_user.addBlock(block_1)
		test_user.addBlock(block_2)
		test_user.known.add(u'herbata')

		cls.test_user_read_lemmas = test_user.getReadLemmas()
		new_text_1 = u'przyjaciela brzmi lepszemu herbaty.'
		cls.read_counts_new_lemmas_test_1 = test_user.getReadCountsForNewLemmas(new_text_1, cls.myLemmatizer)
		cls.vocab_list_test_1 = test_user.makeVocabList(new_text_1, cls.myLemmatizer)
		new_text_2 = u'przyjaciela brzmi lepszemu herbaty. brzmisz'
		cls.read_counts_new_lemmas_test_2 = test_user.getReadCountsForNewLemmas(new_text_2, cls.myLemmatizer)
		cls.vocab_list_test_2 = test_user.makeVocabList(new_text_2, cls.myLemmatizer)

	def test_get_read_lemmas(self):
		self.assertEquals(
			self.test_user_read_lemmas,
			{u'przyjaciel': 1,
			 u'brzmieć': 2}
			)

	def test_read_counts_new_lemmas_test_1(self):
		self.assertEquals(
			self.read_counts_new_lemmas_test_1,
			[
			(u'przyjaciel', 1),
			(u'brzmieć', 2),
			(u'lepsze', 0),
			(u'lepszy', 0),
			(u'herbata', 0)
			]
			)

	@patch('yondeoku.polish.settings.LEKTOREK_CACHE_PATH')
	def test_vocab_list_test_1(self, 'mock/lektorekMockVocab.json'):
		self.assertEquals(
			self.vocab_list_test_1,
			[
			{'lemma': u'przyjaciel',
			'definition': [u'']},
			{'lemma': u'brzmieć',
			'definition': [u'']},
			{'lemma': u'lepsze',
			'definition': [u'']},
			{'lemma': u'lepszy',
			'definition': [u'']}
			],
			msg=self.vocab_list_test_1)

	def test_read_counts_new_lemmas_test_2(self):
		self.assertEquals(
			self.read_counts_new_lemmas_test_2,
			[
			(u'przyjaciel', 1),
			(u'brzmieć', 2),
			(u'lepsze', 0),
			(u'lepszy', 0),
			(u'herbata', 0),
			(u'brzmieć', 2)
			]
			)

	@patch('yondeoku.polish.settings.LEKTOREK_CACHE_PATH')
	def test_vocab_list_test_2(self, 'mock/lektorekMockVocab.json'):
		self.assertEquals(
			self.vocab_list_test_2,
			[
			{'lemma': u'przyjaciel',
			'definition': [u'']},
			{'lemma': u'brzmieć',
			'definition': [u'']},
			{'lemma': u'lepsze',
			'definition': [u'']},
			{'lemma': u'lepszy',
			'definition': [u'']}
			]
			)



