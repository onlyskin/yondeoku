#! /usr/bin/env python                                                        
# -*- coding: utf-8 -*-

from yondeoku.polish.settings import PUNCTUATION_STRING

class Token(object):

	def __init__(self, tokenText, startIndex):
		self.tokenText = tokenText
		self.strippedText = tokenText.strip(PUNCTUATION_STRING).lower()
		self.startIndex = startIndex
		#handle the case where the token is entirely stripped, e.g. '-'
		#in this case an empty token appears in the token list, and the
		#strippedStartIndex is set so that the token will get marked as
		#read when the previous token to it is marked as read using the
		#Block.setReadTokens function
		if self.strippedText == '':
			self.strippedStartIndex = self.startIndex - len(self.tokenText)
		else:
			self.strippedStartIndex = startIndex + tokenText.lower().index(self.strippedText[0])

	def __eq__(self, other):
		return self.tokenText == other.tokenText \
			and self.strippedText == other.strippedText \
			and self.startIndex == other.startIndex \

	def __repr__(self):
		return 'tokenText: {0}, strippedText: {1}, startIndex: {2}, strippedStartIndex: {3}'.format(
			self.tokenText, self.strippedText, self.startIndex, self.strippedStartIndex
			)
