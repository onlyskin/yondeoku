# DEFINERS
# All definers have:
# - 'language' property as ''
# - getDefinition method
# 	- returns [{Definition}...]
# 
# 
# DEFINITION OBJECTS
# - found as ''
# - definition []
# - pronunciation ''
# 
# 


from yondeoku.japanese.jaDefiner import jaDefiner
from yondeoku.polish.plDefiner import plDefiner

languageAPI = {'pl': {'Sectionizer': plSectionizer,
					  'Lemmatizer': plLemmatizer,
					  'Definer': plDefiner
					  },
				'ja': {'Sectionizer': jaSectionizer,
					   'Lemmatizer': jaLemmatizer,
					   'Definer': jaDefiner
					   }
			   }