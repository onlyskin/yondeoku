#! /usr/bin/env python                                                        
# -*- coding: utf-8 -*-

import re
import editdistance

from yondeoku.polish.Token import Token

class Block(object):

	def __init__(self, text, myLemmatizer):
		self.text = text
		self.tokens = self.makeTokens(text)
		self.lemmaList = map(lambda x: myLemmatizer.lookupLemma(x.strippedText), self.tokens)
		self.bestLemmaList = map(lambda x: self.getBestLemma(x, self.tokens), enumerate(self.lemmaList))
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
		result += list.__repr__(self.tokens)
		result += u'\nlemmaList:'
		result += list.__repr__(self.lemmaList)
		result += u'\n'
		return result

	@staticmethod
	def getBestLemma(lemma_enum, tokenList):
		i, lemmas = lemma_enum
		if len(lemmas) == 1:
			return lemmas[0]
		closest_distance = 1000
		closest_lemma = u''
		for lemma in lemmas:
			distance = editdistance.eval(tokenList[i].strippedText, lemma)
			if distance < closest_distance:
				closest_lemma = lemma
				closest_distance = distance
		return closest_lemma

	@staticmethod
	def makeTokens(text):
		'''Static method used in the Block class's __init__
		method. Breaking the text into tokens on whitespace
		it returns a list of Token objects whose properties
		are: the original text, and a stripped version with
		no punctuation on the edges, the original index the
		token started at in the Block's text + the stripped
		token text original index.'''
		pattern = re.compile(r'\s+')
		startIndex = 0
		tokens = []
		match = pattern.search(text)
		#catch the case where there is no whitespace
		if match == None:
			onlyToken = Token(text, 0)
			return [onlyToken]
		#get the token preceding each piece of whitespace
		while match:
			whitespaceSpan = match.span()
			#set token to slice from end of previous whitespace
			#to start of current whitespace
			tokenText = text[startIndex:whitespaceSpan[0]]
			currentToken = Token(tokenText, startIndex)
			tokens.append(currentToken)

			#update new startIndex and search again
			startIndex = whitespaceSpan[1]
			match = pattern.search(text, startIndex)

		#catch the token remaining after no more whitespace is found
		finalTokenText = text[startIndex:]
		finalToken = Token(finalTokenText, startIndex)
		tokens.append(finalToken)

		return tokens

	def setReadTokens(self, indexIn, indexOut):
		'''Takes an index in and index out on the Block's text
		property. Sets to True in the 'read' array any tokens
		whose tokenStrippedText is entirely encompassed in the
		original text by this index span. Does not include any
		punctuation in this calculation. The indices work as
		for slicing - in is inclusive, out is exclusive.

		NB - there could be an issue at some point that any
		tokens containing entirely punctuation that gets stripped
		will only get set as 'read' by this function when indexOut
		reaches the index of the end of the previous token's
		UNSTRIPPED text'''
		for i, token in enumerate(self.tokens):
			tokenTextStart = token.strippedStartIndex
			tokenTextEnd = tokenTextStart + len(token.strippedText)
			if tokenTextStart >= indexIn and tokenTextEnd <= indexOut:
				self.readTokens[i] = True
		return self
