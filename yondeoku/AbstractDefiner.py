class AbstractDefiner(object):
	'''Abstract Definer class. Subclass for a given language,
	implement init to set self.language to appropriate language
	string, implement the define method.'''

	def __init__(self, language):
		self.language = language

	def define(self):
		raise NotImplementedError("Should have implemented this")
