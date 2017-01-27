import ujson as json
import codecs

from yondeoku.polish.settings import DICT_PATH

class Lemmatizer(object):

	def __init__(self, dictPath=DICT_PATH):
		f = codecs.open(dictPath, mode='r', encoding='utf-8')
		self.lemmaDict = json.load(f)

	def lookupLemma(self, word):
		'''Bound method which returns a list of lemmas
		found in the internal dictionary for the given
		word.'''
		try:
			return self.lemmaDict[word]
		except KeyError:
			return [word]
