import json

from yondeoku.languageAPI import languageAPI, supported_languages
from yondeoku.overlap import normalizeRanges

class gBlock(object):
	'''Language independent Block class. Objects of this type
	are to be found in the 'gBlocks' Array on User instances.
	We initialize these gBlock objects from the Block model as
	a wrapper.'''

	def __init__(self, Block):
		'''We now initialize gBlocks from the db.Model
		objects returned by flask sqlalchemy.'''
		language = Block.language
		text = Block.text
		readRanges = json.loads(Block.read_ranges)

		try:
			assert language in supported_languages
		except:
			raise ValueError

		try:
			for i in readRanges:
				assert len(i) == 2
		except:
			raise ValueError

		tools = languageAPI[language]()
		sectionizer = tools.sectionizer
		lemmatizer = tools.lemmatizer

		#core properties which save to database
		self.id = Block.id
		self.language = language
		self.text = text
		#normalizes
		self.readRanges = normalizeRanges(readRanges)

		#implementation dependent properties, not stored
		self.sections = sectionizer.sectionize(text)
		def addLemmas(Section):
			Section.lemmas = lemmatizer.lemmatize(Section)
		map(lambda x: addLemmas(x), self.sections)
		self.readSections = self.computeReadSections()

	def update_readRanges(self, new_range):
		'''Updates the core readRanges array to include a new
		range. Normalises the ranges. Currently need to call
		computeReadSections again separately.'''
		self.readRanges.append(new_range)
		self.readRanges = normalizeRanges(self.readRanges)

	def computeReadSections(self):
		'''Computes a boolean array corresponding to the
		sections array based on the Block's core 'readRanges'
		property. This function is only to be called during
		Block initialisation.'''
		readSections = [False] * len(self.sections)
		for i, Section in enumerate(self.sections):
			sectionStart = Section.blockRef[0]
			sectionEnd = Section.blockRef[1]
			for r in self.readRanges:
				rangeStart = r[0]
				rangeEnd = r[1]
				if sectionStart >= rangeStart and sectionEnd <= rangeEnd:
					readSections[i] = True
		return readSections

	def makeReadRangeString(self):
		'''gBlock method which returns a jsonified
		string of the read_ranges [[]...] which updates
		the original Block Model.'''
		return json.dumps(self.readRanges)

