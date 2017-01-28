#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import re
import codecs
import time
from pprint import pprint

from yondeoku.polish.settings import LEKTOREK_CACHE_PATH

#word -> boolean
def checkLektorekCache(word, LEKTOREK_CACHE_PATH):
	f = codecs.open(LEKTOREK_CACHE_PATH, 'r', 'utf-8')
	JSON = json.loads(f.read())
	f.close()
	if word in JSON:
		return True
	else:
		return False

#str word -> JSON
def getJSONfromURL(word):
	'''Makes an http request to lektorek and returns {} if it fails
	and a dict loaded from the entire returned json if it passes.'''
	print word
	url = api_url = "http://lektorek.org/dapi/v1/index.php/search/chomper/polish/" + word + "?diacritics=false&pos=all"
	r = requests.get(url)
	if r.status_code != 200:
		return {}
	else:
		requestJSON = json.loads(r.text)
		return requestJSON

#JSON -> [str] HTML
def getCorrectDef(JSON):
	'''Takes the raw JSON string (either cached or requested)
	and returns a list of definitions deemed to be correct by
	the function. This can be modified later, because we have
	saved the entire JSON in the cache.'''
	if JSON == {}:
		return []
	results = JSON[u'results']
	definitions = []
	for result in results:
		if result[u'polish_word'] == JSON[u'found_as']:
			definitions.append(result[u'embedded_definition'])
	return definitions

def cacheLektorekResult(word, JSON, LEKTOREK_CACHE_PATH):
	'''Caches the entire JSON from the getJSONfromURL call.'''
	f = codecs.open(LEKTOREK_CACHE_PATH, 'r', 'utf-8')
	cachedJSON = json.loads(f.read())
	f.close()
	cachedJSON[word] = JSON
	f = codecs.open(LEKTOREK_CACHE_PATH, 'w', 'utf-8')
	f.write(json.dumps(cachedJSON, sort_keys=True, indent=4, separators=(',', ': ')))
	f.close()

def getLektorekJSONFromCache(word, LEKTOREK_CACHE_PATH):
	f = codecs.open(LEKTOREK_CACHE_PATH, 'r', 'utf-8')
	JSON = json.loads(f.read())
	f.close()
	return JSON[word]

#Returns a [str] for the word
#Takes a base form, only returns words
#from the Lektorek JSON if they
#exactly equal the input string
###FOR USE WITH LEMMAS
def getLektorekDef(word, LEKTOREK_CACHE_PATH):
	if not checkLektorekCache(word, LEKTOREK_CACHE_PATH):
		JSON = getJSONfromURL(word)
		cacheLektorekResult(word, JSON, LEKTOREK_CACHE_PATH)
		result = getCorrectDef(JSON)
		return result
	else:
		JSON = getLektorekJSONFromCache(word, LEKTOREK_CACHE_PATH)
		result = getCorrectDef(JSON)
		return result