#! /usr/bin/env python                                                        
# -*- coding: utf-8 -*-

from jNlp.jTokenize import jTokenize

class jBlock(object):

	def __init__(self, text):
		self.text = text
		self.tokens = self.makeTokens(text)
		self.lemmaList = self.tokens
		self.bestLemmaList = self.tokens
		self.readTokens = [False] * len(self.tokens)

	def __eq__(self, other):
		return self.text == other.text \
			and self.tokens == other.tokens \
			and self.lemmaList == other.lemmaList \
			and self.readTokens == other.readTokens

	def __repr__(self):
		result = u'Block:\ntext: '
		result += self.text
		result += u'\ntokens: '
		result += ', '.join(self.tokens)
		result += u'\nlemmaList:'
		result += ', '.join(self.lemmaList)
		result += u'\n'
		return result.encode('utf-8')

	@staticmethod
	def makeTokens(text):
		return jTokenize(text)

#	def setReadTokens(self, indexIn, indexOut):
#		'''Takes an index in and index out on the Block's text
#		property. Sets to True in the 'read' array any tokens
#		whose tokenStrippedText is entirely encompassed in the
#		original text by this index span. Does not include any
#		punctuation in this calculation. The indices work as
#		for slicing - in is inclusive, out is exclusive.
#
#		NB - there could be an issue at some point that any
#		tokens containing entirely punctuation that gets stripped
#		will only get set as 'read' by this function when indexOut
#		reaches the index of the end of the previous token's
#		UNSTRIPPED text'''
#		for i, token in enumerate(self.tokens):
#			tokenTextStart = token.strippedStartIndex
#			tokenTextEnd = tokenTextStart + len(token.strippedText)
#			if tokenTextStart >= indexIn and tokenTextEnd <= indexOut:
#				self.readTokens[i] = True
#		return self
