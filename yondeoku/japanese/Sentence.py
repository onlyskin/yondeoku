#! /usr/bin/env python                                                        
# -*- coding: utf-8 -*-

from jNlp.jTokenize import jTokenize

class Sentence(object):

	def __init__(self, index, length, text):
		self.index = index
		self.length = length
		self.text = text
		self.tokens = self.makeTokens(text)

	def __repr__(self):
		result = u'Sentence:\ntext: '
		result += self.text
		result += u'\ntokens: '
		result += ', '.join(self.tokens)
		return result

	#str -> [str]
	@staticmethod
	def makeTokens(text):
		text = text.replace('\n', '')
		return jTokenize(text)