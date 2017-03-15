import cPickle as pickle
from yondeoku.polish.settings import DATA_PATH, DICT_PATH, LEKTOREK_CACHE_PATH
from yondeoku.polish.Block import Block
from yondeoku.polish.Lemmatizer import Lemmatizer
from yondeoku.polish.getLektorekDef import getLektorekDef

class gUser(object):

	#modify to allow loading from pickle
	def __init__(self, username):
		self.username = username
		self.Blocks = []
		self.pickleFilePath = DATA_PATH + self.username + u'.pickle'
		self.known = set()
		self.jKnown = set()
		self.threshold = 8

	def __repr__(self):
		result = 'username: {0}\n\nblocks:\n'.format(self.username)
		for Block in self.Blocks:
			result += str(Block)
			result += '\n'
		return result

	@staticmethod
	def loadUserDataFromPickle(username):
		'''str -> User

		Static method which returns a User object
		instance that was previously saved to pickle
		using the saveUserDataToPickle method with a
		User instance (in any session).'''
		f = open(DATA_PATH + username + '.pickle', 'r')
		userData = pickle.load(f)
		f.close()
		return userData

	def makeUserDataFile(self):
		'''User -> file created

		User object method creating a pickle file
		for the object to be saved into.'''
		f = open(self.pickleFilePath, 'w')
		f.close()

	def saveUserDataToPickle(self):
		'''User -> boolean

		User object method which dumps the User
		object into its pickle file in order to be
		used in subsequent sessions.'''
		f = open(self.pickleFilePath, 'w')
		pickle.dump(self, f)
		f.close()
		return True

	def addBlock(self, Block):
		'''Block -> [Block]

		Bound method which appends a new Block
		to the User's list of Blocks.'''
		if Block not in self.Blocks:
			self.Blocks.append(Block)
		return self.Blocks

	def deleteBlock(self, text):
		'''str -> [Block] OR None if no Block had that text'''
		for Block in self.Blocks:
			if Block.text == text:
				self.Blocks.remove(Block)
				return self.Blocks
		return None

	def instantiateLemmatizer(self, lemmatizerName, dictPath):
		'''Method to bind a particular lemmatizer to
		a User instance. Not currently using.'''
		self.lemmatizerName = Lemmatizer(dictPath)

	def getReadLemmas(self):
		'''-> {str: int, ...}

		Returns a dictionary of key, value mappings
		where each key is an encountered lemma and the
		corresponding values are how many times it has
		been encountered over all the read Block bits.'''
		result = {}
		for Block in self.Blocks:
			for i, lemmas in enumerate(Block.lemmaList):
				if Block.readTokens[i]:
					for lemma in lemmas:
						if lemma not in result.keys():
							result[lemma] = 1
						else:
							result[lemma] = result[lemma] + 1
		return result

	def getReadCountsForNewLemmas(self, newText, lemmatizerName):
		'''-> [(str, int), ...]

		Returns a list of tuples containing lemmas
		and the number of previous encounters of them
		in the order that the lemmas are found in the
		new text (intended as a 'pair of lists' which
		can then be further processed, e.g. to remove
		duplicates, etc. You also need to specify the
		lemmatizer the function should use. This will
		be instantiated as a property on the User.'''
		readLemmaOccurences = self.getReadLemmas()
		newTextBlock = Block(newText, lemmatizerName)
		result = []
		for lemmas in newTextBlock.lemmaList:
			for lemma in lemmas:
				try:
					result.append((lemma, readLemmaOccurences[lemma]))
				except KeyError:
					result.append((lemma, 0))
		return result

	def makeVocabList(self, newText, lemmatizerName):
		'''[(str, int), ...] -> [{lemma: str, definition: [str]}]

		Outputs a custom formatted vocab list. Currently
		simply removes duplicate new lemmas.'''
		filtering = []
		newLemmasReadCounts = self.getReadCountsForNewLemmas(newText,
														lemmatizerName)
		for lemmaCount in newLemmasReadCounts:
			if lemmaCount not in filtering and lemmaCount[0] not in self.known and lemmaCount[1] < self.threshold:
				filtering.append(lemmaCount)
		vocabList = []
		counter = 0
		for tuple in filtering:
			print str(counter) + '/' + str(len(filtering))
			counter = counter + 1
			vocabItem = {}
			vocabItem['lemma'] = tuple[0]
			vocabItem['definition'] = getLektorekDef(tuple[0], LEKTOREK_CACHE_PATH)
			vocabList.append(vocabItem)
		return vocabList

	def regenerateBlocks(self, myLemmatizer):
		'''-> [Block]

		Convenience method to update blocks when we
		change how we initialise the static properties
		for block.

		NOTE: will ERASE ANY READING HISTORY'''
		newBlocks = []
		for instance in self.Blocks:
			regeneratedBlock = Block(instance.text, myLemmatizer)
			newBlocks.append(regeneratedBlock)
		self.Blocks = newBlocks