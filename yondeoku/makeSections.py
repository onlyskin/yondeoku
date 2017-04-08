import re
from yondeoku.Section import Section

def makeSections(text, sentence_breakers, end_quote):
	'''Returns the text as a [{Section}...], the sentence_breakers
	is a list of strings denoting sentence boundaries - e.g. '.!?'
	The end_quote is a single char representing a closing quote in
	a given language.'''

	sections = []

	# returns a regex which will capture any of the sentence breakers, or any of the
	# sentence breakers plus an end quote
	regexString = '(' + u'|'.join(
        	[c + end_quote + '\n+' for c in sentence_breakers] +
        	[c + '\n+' for c in sentence_breakers] +
        	[c + end_quote for c in sentence_breakers] +
            [c for c in sentence_breakers]
	) + ')'
	pattern = re.compile(regexString)
	separators = re.finditer(pattern, text)
	separatorsList = list(separators)
	if len(separatorsList) == 0:
		return [Section(0, len(text), text)]
	for i, m in enumerate(separatorsList):
		#if it's the first separator, the start index is 0
		if i == 0:
			_in = 0
		#otherwise the start index is the end of the last separator
		else:
			_in = separatorsList[i-1].end()
		_out = m.end()
		subtext = text[_in:_out]
		section = Section(_in, _out, subtext)
		sections.append(section)
	#if the final separator ends before the end of the text
	lastFoundSepEnd = separatorsList[-1].end()
	if lastFoundSepEnd < len(text):
		finalSubText = text[lastFoundSepEnd:]
		finalSection = Section(lastFoundSepEnd, len(text), finalSubText)
		sections.append(finalSection)
	return sections