import re

from yondeoku.AbstractLemmatizer import AbstractLemmatizer
from yondeoku.Lemma import Lemma
from yondeoku.polish.Lemmatizer import Lemmatizer
from yondeoku.polish.settings import DICT_PATH, PUNCTUATION_STRING

def plLemmatizer():
	'''Initializes a plLemmatizer with the full dictionary.'''
	return generic_plLemmatizer(DICT_PATH)

def testing_plLemmatizer():
	'''Initializes a plLemmatizer with a reduced dictionary.'''
	return generic_plLemmatizer('mock/testDict.json')

class generic_plLemmatizer(AbstractLemmatizer):
	'''Concrete Polish Lemmatizer class. Must be passed a string
	specifying the dictionary file to initialise. with. The above
	plLemmatizer and testing_plLemmatizer provide a consistent
	API as the dictionary file is to be specified within the
	plLemmatizer backend. It has only been extracted for testing.'''

	def __init__(self, dictionary_path):
		print 'Initializing plLemmatizer'
		super(generic_plLemmatizer, self).__init__('pl')
		self.myLemmatizer = Lemmatizer(dictionary_path)

	def lemmatize(self, Section):
		'''Takes a {Section} object, returns a list
		[{Definition}...] objects based on the Section's
		text property.'''
		text = Section.text
		wordList = self.splitAndStrip(text)
		lemmaSet = set()
		for word in wordList:
			lemmaList = self.myLemmatizer.lookupLemma(word)
			for lemma in lemmaList:
				lemmaSet.add(Lemma(lemma))
		return lemmaSet

	def splitAndStrip(self, text):
		'''This method breaks a text into tokens on whitespace
		and strips any punctuation away. Returns a list of strings.'''
		pattern = re.compile(r'\s+')
		startIndex = 0
		tokens = []
		match = pattern.search(text)
		#catch the case where there is no whitespace
		if match == None:
			return [text.strip(PUNCTUATION_STRING).lower()]
		#get the token preceding each piece of whitespace
		while match:
			whitespaceSpan = match.span()
			#set token to slice from end of previous whitespace
			#to start of current whitespace
			tokenText = text[startIndex:whitespaceSpan[0]]
			tokens.append(tokenText)

			#update new startIndex and search again
			startIndex = whitespaceSpan[1]
			match = pattern.search(text, startIndex)

		#catch the token remaining after no more whitespace is found
		finalTokenText = text[startIndex:]
		tokens.append(finalTokenText)
		tokens = map(lambda x: x.strip(PUNCTUATION_STRING).lower(), tokens)
		return tokens