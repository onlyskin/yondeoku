#! /usr/bin/env python                                                        
# -*- coding: utf-8 -*-

from unittest import TestCase

from os.path import isfile
import os

from yondeoku.polish.User import User
from yondeoku.polish.Block import Block
from yondeoku.polish.Token import Token
from yondeoku.polish.Lemmatizer import Lemmatizer
from yondeoku.polish.settings import DATA_PATH

test_user_name = u'test_user_123'

class TestUser(TestCase):

	@classmethod
	def setUpClass(cls):
		cls.myLemmatizer = Lemmatizer(u'mock/testDict.json')
		cls.test_user = User(test_user_name)

		test001 = User('test001')
		test001.makeUserDataFile()
		test001.saveUserDataToPickle()

		test002 = User('test002')
		test002.addBlock(Block(u'przyjaciela, brzmisz.', cls.myLemmatizer))
		test002.addBlock(Block(u'psom\n\nlepszemu lekarkami', cls.myLemmatizer))
		test002.makeUserDataFile()
		test002.saveUserDataToPickle()

		cls.test001 = User.loadUserDataFromPickle('test001')
		cls.test002 = User.loadUserDataFromPickle('test002')

	@classmethod
	def tearDownClass(cls):
		os.remove(DATA_PATH + test_user_name + u'.pickle')
		os.remove(DATA_PATH + u'test001' + u'.pickle')
		os.remove(DATA_PATH + u'test002' + u'.pickle')

	def test_has_username(self):
		self.assertEquals(
			self.test_user.username,
			test_user_name
			)

	def test_make_user_file_created_file(self):
		self.test_user.makeUserDataFile()
		f = open(self.test_user.pickleFilePath)
		self.assertEquals(
			f.read(), ''
			)
		f.close()

	def test_saved_user_data_to_pickle(self):
		self.test_user.saveUserDataToPickle()
		f = open(self.test_user.pickleFilePath)
		self.assertFalse(
			f.read() == ''
			)
		f.close()

	def test_add_block(self):
		test_block = Block(u'testing', self.myLemmatizer)
		self.assertEquals(
			self.test_user.addBlock(test_block),
			[test_block]
			)

	def test_user_loaded_from_pickle_has_correct_username(self):
		self.assertEquals(
			self.test001.username,
			'test001'
			)

	def test_user_loaded_from_pickle_test001_Blocks_is_empty(self):
		self.assertEquals(
			self.test001.Blocks,
			[]
			)

	def test_user_test002_has_two_blocks(self):
		self.assertEquals(
			len(self.test002.Blocks),
			2
			)

	def test_user_test002_block1_token0_text(self):
		self.assertEquals(
			self.test002.Blocks[1].tokens[0].strippedText,
			u'psom'
			)

	def test_user_test002_block0_token1(self):
		self.assertEquals(
			self.test002.Blocks[0].tokens[0],
			Token(u'przyjaciela,', 0)
			)

