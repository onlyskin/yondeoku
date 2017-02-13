from yondeoku.AbstractDefiner import AbstractDefiner
from yondeoku.polish.getDefinition import getDefObjList

class plDefiner(AbstractDefiner):
	'''Concrete Polish Definer class.'''

	def __init__(self, language):
		self.language = 'pl'

	def define(self, word):
		'''Return a list of Definition objects.'''
		result = getDefObjList(word)
		return result