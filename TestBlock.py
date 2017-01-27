#! /usr/bin/env python                                                        
# -*- coding: utf-8 -*-

from unittest import TestCase

from yondeoku.polish.Block import Block
from yondeoku.polish.Lemmatizer import Lemmatizer
from yondeoku.polish.Token import Token

test_string_1 = u'przyjaciela'
test_string_2 = u'przyjaciela, ,brzmisz.'
test_string_3 = u'przyjaciela.. \n\n\nbrzmisz.,   \npsom stali'

class TestBlock(TestCase):

	@classmethod
	def setUpClass(cls):
		cls.Lemmatizer = Lemmatizer('mock/testDict.json')

		cls.fakeToken1_0 = Token(u'przyjaciela', 0)

		cls.fakeToken2_0 = Token(u'przyjaciela,', 0)
		cls.fakeToken2_1 = Token(u',brzmisz.', 13)

		cls.fakeToken3_0 = Token(u'przyjaciela..', 0)
		cls.fakeToken3_1 = Token(u'brzmisz.,', 17)
		cls.fakeToken3_2 = Token(u'psom', 30)
		cls.fakeToken3_3 = Token(u'stali', 35)

	def setUp(self):
		self.testBlock1 = Block(test_string_1, self.Lemmatizer)
		self.testBlock2 = Block(test_string_2, self.Lemmatizer)
		self.testBlock3 = Block(test_string_3, self.Lemmatizer)

	def test_block_1_text(self):
		self.assertEquals(
			self.testBlock1.text,
			u'przyjaciela'
			)

	def test_block_2_text(self):
		self.assertEquals(
			self.testBlock2.text,
			u'przyjaciela, ,brzmisz.'
			)

	def test_block_3_text(self):
		self.assertEquals(
			self.testBlock3.text,
			u'przyjaciela.. \n\n\nbrzmisz.,   \npsom stali'
			)

	def test_block_1_tokens(self):
		self.assertEquals(
			self.testBlock1.tokens,
			[self.fakeToken1_0]
			)

	def test_block_2_tokens(self):
		self.assertEquals(
			self.testBlock2.tokens,
			[self.fakeToken2_0, self.fakeToken2_1]
			)

	def test_block_3_tokens(self):
		self.assertEquals(
			self.testBlock3.tokens,
			[self.fakeToken3_0, self.fakeToken3_1, self.fakeToken3_2, self.fakeToken3_3]
			)

	def test_block_1_lemmaList(self):
		self.assertEquals(
			self.testBlock1.lemmaList,
			[[u'przyjaciel']]
			)

	def test_block_2_lemmaList(self):
		self.assertEquals(
			self.testBlock2.lemmaList,
			[[u'przyjaciel'], [u'brzmieć']]
			)

	def test_block_3_lemmaList(self):
		self.assertEquals(
			self.testBlock3.lemmaList,
			[[u'przyjaciel'], [u'brzmieć'], [u'pies'], [u'stać', u'stal', u'stały']]
			)

	def test_block_1_bestLemmaList(self):
		self.assertEquals(
			self.testBlock1.bestLemmaList,
			[u'przyjaciel']
			)

	def test_block_2_bestLemmaList(self):
		self.assertEquals(
			self.testBlock2.bestLemmaList,
			[u'przyjaciel', u'brzmieć']
			)

	def test_block_3_bestLemmaList(self):
		self.assertEquals(
			self.testBlock3.bestLemmaList,
			[u'przyjaciel', u'brzmieć', u'pies', u'stal']
			)

	def test_block_1_readTokens(self):
		self.assertEquals(
			self.testBlock1.readTokens,
			[False]
			)

	def test_block_2_readTokens(self):
		self.assertEquals(
			self.testBlock2.readTokens,
			[False, False]
			)

	def test_block_3_readTokens(self):
		self.assertEquals(
			self.testBlock3.readTokens,
			[False, False, False, False]
			)

	def test_block_3_set_token_2_to_read(self):
		self.testBlock3.setReadTokens(30, 34)
		self.assertEquals(
			self.testBlock3.readTokens,
			[False, False, True, False]
			)

	def test_block_2_set_token_1_to_read(self):
		self.testBlock2.setReadTokens(14, 21)
		self.assertEquals(
			self.testBlock2.readTokens,
			[False, True]
			)

	def test_block_3_set_token_0_to_read_1_still_not_read(self):
		self.testBlock3.setReadTokens(0, 20)
		self.assertEquals(
			self.testBlock3.readTokens,
			[True, False, False, False]
			)
