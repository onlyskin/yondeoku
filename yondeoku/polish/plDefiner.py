from yondeoku.AbstractDefiner import AbstractDefiner
from yondeoku.polish.getLektorekDef import getDefObjList

class plDefiner(AbstractDefiner):
	'''Concrete Polish Definer class.'''

	def __init__(self):
		super(plDefiner, self).__init__('pl')

	def define(self, word):
		'''Return a list of {Definition} objects.'''
		result = getDefObjList(word)
		return result