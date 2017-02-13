#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase

from yondeoku.polish.plDefiner import plDefiner

class Test_plDefiner(TestCase):

	@classmethod
	def setUpClass(cls):
		cls.plDefinerInstance = plDefiner()
		cls.defineResult = plDefinerInstance.define(u'przyjaciel')

	def test_define_returns_list(self):
		self.assertIsInstance(
			self.defineResult,
			list
		)

	def test_first_result_is_Definition(self):
		self.assertIsInstance(
			self.defineResult[0],
			Definition
			)