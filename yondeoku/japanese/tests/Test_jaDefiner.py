#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase

from yondeoku.japanese.jaDefiner import jaDefiner

class Test_jaDefiner(TestCase):

	@classmethod
	def setUpClass(cls):
		cls.jaDefinerInstance = jaDefiner()
		cls.defineResult = jaDefinerInstance.define(u'林檎')

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