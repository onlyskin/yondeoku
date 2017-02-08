#! /usr/bin/env python                                                        
# -*- coding: utf-8 -*-

import re
from yondeoku.japanese.Sentence import Sentence

class jBlock(object):

	def __init__(self, text):
		self.jText = text
		self.sentences = self.makeSentences(text)
		self.readSentences = [False] * len(self.sentences)

	def __eq__(self, other):
		return self.jText == other.jText \
			and self.sentences == other.sentences \
			and self.readSentences == other.readSentences

	def __repr__(self):
		result = u'Block:\ntext: '
		result += self.jText
		result += u'\nsentences: '
		result += ', '.join(self.sentences)
		return result.encode('utf-8')

	@staticmethod
	def makeSentences(text):
		sentences = []
		pattern = re.compile(ur'(。」|！」|？」|。|！|？)')
		separators = re.finditer(pattern, text)
		separatorsList = []
		for i in separators:
			separatorsList.append(i)
		for i, m in enumerate(separatorsList):
			print i, m, m.start(), m.end()
			#if it's the first separator, the start index is 0
			if i == 0:
				start = 0
			#otherwise the start index is the end of the last separator
			else:
				start = separatorsList[i-1].end()
			length = m.end() - start
			subtext = text[start:m.end()]
			section = Sentence(start, length, subtext)
			sentences.append(section)
		#if the final separator ends before the end of the text
		lastSeparatorIndex = separatorsList[-1].end()
		if lastSeparatorIndex < len(text):
			finalSubText = text[lastSeparatorIndex:]
			finalSection = Sentence(lastSeparatorIndex, len(finalSubText), finalSubText)
			sentences.append(finalSection)
		return sentences

	def setReadSentences(self, sentenceText):
		for i, sentence in enumerate(self.sentences):
			if sentenceText == sentence.text:
				self.readSentences[i] = True
