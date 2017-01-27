#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import re
import codecs
import time
from pprint import pprint

from yondeoku.polish.settings import LEKTOREK_CACHE_PATH

#str word -> JSON
def getJSONfromURL(word):
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
	if JSON == {}:
		return []
	results = JSON[u'results']
	definitions = []
	for result in results:
		if result[u'polish_word'] == JSON[u'found_as']:
			definitions.append(result[u'embedded_definition'])
	return definitions

#Returns a [str] for the word
#Takes a base form, only returns words
#from the Lektorek JSON if they
#exactly equal the input string
def getLektorekDef(word, LEKTOREK_CACHE_PATH):
	if not checkLektorekCache(word, LEKTOREK_CACHE_PATH):
		JSON = getJSONfromURL(word)
		result = getCorrectDef(JSON)
		cacheLektorekResult(word, result, LEKTOREK_CACHE_PATH)
		return result
	else:
		return getLektorekDefFromCache(word, LEKTOREK_CACHE_PATH)

#word -> boolean
def checkLektorekCache(word, LEKTOREK_CACHE_PATH):
	f = codecs.open(LEKTOREK_CACHE_PATH, 'r', 'utf-8')
	JSON = json.loads(f.read())
	f.close()
	if word in JSON:
		return True
	else:
		return False

def cacheLektorekResult(word, result, LEKTOREK_CACHE_PATH):
	f = codecs.open(LEKTOREK_CACHE_PATH, 'r', 'utf-8')
	JSON = json.loads(f.read())
	f.close()
	JSON[word] = result
	f = codecs.open(LEKTOREK_CACHE_PATH, 'w', 'utf-8')
	f.write(json.dumps(JSON, sort_keys=True, indent=4, separators=(',', ': ')))
	f.close()

def getLektorekDefFromCache(word, LEKTOREK_CACHE_PATH):
	f = codecs.open(LEKTOREK_CACHE_PATH, 'r', 'utf-8')
	JSON = json.loads(f.read())
	f.close()
	return JSON[word]