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
		self.sectionizer = sectionizer
		self.lemmatizer = lemmatizer
		self.definer = definer
		self.grammarWords = grammarWords

plTools = LangTools(plSectionizer, plLemmatizer, plDefiner, plGrammarWords)
jaTools = LangTools(jaSectionizer, jaLemmatizer, jaDefiner, jaGrammarWords)

languageAPI = {'pl': plTools,
				'ja': jaTools}

supported_languages = languageAPI.keys()
