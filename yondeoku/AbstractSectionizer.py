class AbstractSectionizer(object):
	'''Abstract Sectionizer class. Subclass for a given language,
	implement init to set self.language to appropriate language
	string, implement the sectionize method.'''

	def __init__(self, language):
		self.language = language

	def sectionize(self):
		raise NotImplementedError("Should have implemented this")
