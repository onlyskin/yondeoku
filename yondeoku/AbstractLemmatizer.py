class AbstractLemmatizer(object):
	'''Abstract Lemmatizer class. Subclass for a given language,
	implement init to set self.language to appropriate language
	string, implement the lemmatize method, which must take a
	{Section} object and return a [{Lemma}...]'''

	def __init__(self, language):
		self.language = language

	def lemmatize(self):
		raise NotImplementedError("Should have implemented this")
