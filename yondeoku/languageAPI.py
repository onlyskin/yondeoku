from yondeoku.japanese.jaDefiner import jaDefiner
from yondeoku.japanese.jaSectionizer import jaSectionizer
from yondeoku.japanese.jaLemmatizer import jaLemmatizer
from yondeoku.japanese.grammarWords import jaGrammarWords
from yondeoku.polish.plDefiner import plDefiner
from yondeoku.polish.plSectionizer import plSectionizer
from yondeoku.polish.plLemmatizer import plLemmatizer
from yondeoku.polish.grammarWords import plGrammarWords

class LangTools(object):
	'''Object wrapper for the core tools which need to be
	defined for any new language.'''

	def __init__(self, sectionizer, lemmatizer, definer, grammarWords):
		self.sectionizer = sectionizer()
		self.lemmatizer = lemmatizer()
		self.definer = definer()
		self.grammarWords = grammarWords

plTools = None
jaTools = None

def getPlTools():
	global plTools
	if plTools == None:
		plTools = LangTools(plSectionizer, plLemmatizer, plDefiner, plGrammarWords)
		return plTools
	else:
		return plTools

def getJaTools():
	global jaTools
	if jaTools == None:
		jaTools = LangTools(jaSectionizer, jaLemmatizer, jaDefiner, jaGrammarWords)
		return jaTools
	else:
		return jaTools

languageAPI = {'pl': getPlTools,
				'ja': getJaTools}

supported_languages = languageAPI.keys()
