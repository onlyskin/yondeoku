#!/usr/bin/env python
# -*- coding: utf-8

import re
from pprint import pprint
import itertools
from yondeoku.japanese.monash_edict_search import *

edict_path = 'yondeoku/japanese/edict2'

class fakeEdictEntry(object):
  
    def __init__(self, japanese=None, furigana=None, glosses=[], tags=set(), unparsed=[]):
        # Japanese - note, if only a kana reading is present, it's
        # stored as "japanese", and furigana is left as None.
        self.japanese = japanese
        self.furigana = furigana
        # Native language glosses
        self.glosses = glosses
        # Info fields should be inserted here as "tags".
        self.tags = tags
        # Currently unhandled stuff goes here...
        self.unparsed = unparsed

class fakeResult:
	def __init__(self):
		self.glosses = ''

#str -> [edictEntry object]
#edictEntry - {glosses[], unparsed[], furigana'', japanese'', tags[set]}
def searchEdict(query):
	kp = Parser(edict_path)
	results = []
	search = kp.search(query)
	for result in search:
		#removes any strings in brackets from the japanese definition
		result.japanese = re.sub('\(.*?\)', '', result.japanese)
		#adds multiple EdictEntry objects if any japanese definitions contain
		#multiple definitions, so that they can be compared for closeness
		#separately
		if ';' in result.japanese:
			parts = result.japanese.split(';')
			for part in parts:
				results.append(fakeEdictEntry(japanese=part, furigana=result.furigana,
						glosses=result.glosses, tags=result.tags, unparsed=result.unparsed))
		else:
			results.append(result)
	return results

#str, [obj] -> filtered[obj]
#filters the list of edictEntry objects returned by searchEdict
#to return a list of those edictEntry's whose Japanese is closest
#in length to the original search term
def getClosestEntries(word, candidateEntries):
	#first filter any results where the searched word is not actually in the Japanese
	candidateEntries = filter(lambda x: word in x.japanese, candidateEntries)
	#if there are no results left (or none to start with), just return a faked object
	if candidateEntries == []:
		x = fakeResult()
		return x
	wordLength = len(word)
	candidateWords = map(lambda x: x.japanese, candidateEntries)
	#prints the word and the current candidates to the console
	#this is so that we can continue to improve the way we select
	#the closest entries, as we need to see them before they're filtered
	#over time for different entries that come up
	developerInspection(word, candidateWords)
	candidateWordLengths = map(len, candidateWords)
	candidateWordDistances = map(lambda x: abs(wordLength - x), candidateWordLengths)
	#filter to return all entries with the minimum distance	
	minDistance = min(candidateWordDistances)
	selectors = [x == minDistance for x in candidateWordDistances]
	closestEntries = list(itertools.compress(candidateEntries, selectors))
	return closestEntries

#str => [{japanese: '', glosses: []}]
#returns all itesm from the edict which had the closest length to the
#original search term. I recommend checking to see if any add only extra
#kana when the final definition is presented to the user, as this should
#be the best match
def getDef(token):
	EdictEntries = searchEdict(token)
	filteredEdictEntries = getClosestEntries(token, EdictEntries)
	result = []
	for entry in filteredEdictEntries:
		japanese = entry.japanese
		glosses = entry.glosses[:3]
		output = {'japanese': japanese, 'glosses': glosses}
		result.append(output)
	return result

def developerInspection(word, candidateWords):
	print 'search token: ' + word + ':\n'
	print 'search results:\n' + '\n'.join(candidateWords) + '\n'
