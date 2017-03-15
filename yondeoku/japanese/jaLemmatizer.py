from jNlp.jTokenize import jTokenize

from yondeoku.AbstractLemmatizer import AbstractLemmatizer
from yondeoku.Lemma import Lemma

class jaLemmatizer(AbstractLemmatizer):
	'''Concrete Japanese Lemmatizer class.'''

	def __init__(self):
		super(jaLemmatizer, self).__init__('ja')

	def lemmatize(self, Section):
		'''Takes a {Section} object, returns a list
		[{Definition}...] objects based on the Section's
		text property.'''
		text = Section.text
		tokens = jTokenize(text)
		lemmas = map(lambda x: Lemma(x), tokens)
		return set(lemmas)