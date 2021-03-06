from yondeoku.AbstractDefiner import AbstractDefiner
from yondeoku.japanese.getDefinition import getDefObjList

class jaDefiner(AbstractDefiner):
	'''Concrete Japanese Definer class.'''

	def __init__(self):
		super(jaDefiner, self).__init__('ja')

	def define(self, word):
		'''Return a list of {Definition} objects.'''
		result = getDefObjList(word)
		return result