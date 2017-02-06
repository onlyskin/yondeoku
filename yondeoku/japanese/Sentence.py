#! /usr/bin/env python                                                        
# -*- coding: utf-8 -*-

from jNlp.jTokenize import jTokenize

class Sentence(object):

	def __init__(self, index, length, text):
		self.index = index
		self.length = length
		self.text = text
		self.tokens = self.makeTokens(text)

	@staticmethod
	def makeTokens(text):
		return jTokenize(text)