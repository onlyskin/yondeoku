class Lemma(object):
	'''Language independent Lemma class. Objects of this type
	are to be found in the 'lemma' Array on Section instances.
	Lemm's currently are implemented as a container on the word
	property only.'''

	def __init__(self, lemma):
		self.word = lemma

	def __hash__(self):
		return hash(self.word)

	def __eq__(a, b):
		return a.word == b.word
