from yondeoku.languageAPI import languageAPI

# [{Lemma}...] -> [ [{Definition}...] ... ]
def makeDefinitionListFromLemmaList(language, lemmaList):
	'''A method to which returns a list of lists of {Definition}
	objects. The input must take the form of a list of {Lemma}
	objects. All Lemma objects must be from the same language,
	which is to be specified when calling the function so that
	the correct definer will be instantiated.'''
	try:
		assert language in languageAPI.keys()
	except:
		raise ValueError

	if lemmaList == []:
		return []

	#{Lemma} -> [{Definition}...]
	def makeDefinitionList(language, Lemma, definer):

		try:
			assert language in languageAPI.keys()
		except:
			raise ValueError

		if Lemma.word == '':
			return []

		return definer.define(Lemma.word)

	definer = languageAPI[language].definer()
	definitionListList = map(
		lambda x: makeDefinitionList(language, x, definer),
		lemmaList)
	return definitionListList