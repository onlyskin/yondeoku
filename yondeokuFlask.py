#! /usr/bin/env python                                                        
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import json
import os
import jsonpickle

from yondeoku.polish.User import User
from yondeoku.polish.Block import Block
from yondeoku.polish.Lemmatizer import Lemmatizer
from yondeoku.polish.settings import DATA_PATH, LEKTOREK_CACHE_PATH
from yondeoku.polish.getLektorekDef import getLektorekDef
from yondeoku.UserEncoder import UserEncoder
from yondeoku.japanese.getDefinition import getDefinition

DEBUG = True
PORT = 3000
HOST = '0.0.0.0'

testLemmatizer = Lemmatizer(u'mock/testDict.json')

#polishLemmatizer = Lemmatizer(u'lemmaDict.json')

#  .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
# / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
#`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
#### Root Pages ####

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/old')
def old():
	return render_template('main.html')

@app.route('/userOverview')
def userOverview():
	return render_template('userdata.html')

#  .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
# / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
#`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
#### MODEL UPDATE ROUTES ####

@app.route('/getUserData/<username>', methods=['GET'])
def getUserData(username):
	'''This retrieves the user data for user with specific
	username and returns it as json to the webpage.'''
	activeUser = User.loadUserDataFromPickle(username)
	return json.dumps(activeUser, cls=UserEncoder, sort_keys=True, indent=4, separators=(',', ': '))

#.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
@app.route('/addBlock/<username>', methods=['POST'])
def addBlock(username):
	'''POST to this route. JSON body. {"text": "[[Block.text]]"}
	Route returns new user data.'''
	currentUser = User.loadUserDataFromPickle(username)
	newBlockText = request.get_json()['text']
	newBlock = Block(newBlockText, polishLemmatizer)
	currentUser.addBlock(newBlock)
	currentUser.saveUserDataToPickle()
	return json.dumps(currentUser, cls=UserEncoder, sort_keys=True, indent=4, separators=(',', ': '))

@app.route('/deleteBlock/<username>', methods=['POST'])
def deleteBlock(username):
	'''POST to this route. JSON body. {"text": "[[Block.text]]"}
	Route returns new user data.'''
	currentUser = User.loadUserDataFromPickle(username)
	blockText = request.get_json()['text']
	deleted = currentUser.deleteBlock(blockText)
	#deleted will be None if no block matched the text
	if deleted:
		currentUser.saveUserDataToPickle()
		return json.dumps(currentUser, cls=UserEncoder, sort_keys=True, indent=4, separators=(',', ': '))

#.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
@app.route('/setKnownWords/<username>', methods=['POST'])
def setKnownWords(username):
	'''POST body: {japanese: boolean, words: [word, ...]}
	mimetype application/json'''
	currentUser = User.loadUserDataFromPickle(username)
	data = request.get_json()
	japanese = data['japanese']
	words = data['words']
	if japanese:
		for word in words:
			currentUser.jKnown.add(word)
	else:
		for word in words:
			currentUser.known.add(word)
	currentUser.saveUserDataToPickle()
	return json.dumps(currentUser, cls=UserEncoder, sort_keys=True, indent=4, separators=(',', ': '))

@app.route('/removeKnownWords/<username>', methods=['POST'])
def removeKnownWords(username):
	'''POST body: {japanese: boolean, words: [word, ...]}
	mimetype application/json'''
	currentUser = User.loadUserDataFromPickle(username)
	data = request.get_json()
	japanese = data['japanese']
	words = data['words']
	if japanese:
		for word in words:
				currentUser.jKnown.remove(word)
	else:
		for word in words:
			currentUser.known.remove(word)
	currentUser.saveUserDataToPickle()
	return json.dumps(currentUser, cls=UserEncoder, sort_keys=True, indent=4, separators=(',', ': '))

#.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
@app.route('/setThreshold/<username>/<threshold>', methods=['POST'])
def setThreshold(username, threshold):
	currentUser = User.loadUserDataFromPickle(username)
	currentUser.threshold = int(threshold)
	currentUser.saveUserDataToPickle()
	return json.dumps(currentUser, cls=UserEncoder, sort_keys=True, indent=4, separators=(',', ': '))

#.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
@app.route('/setReadTokens/<username>', methods=['POST'])
def setReadTokens(username):
	'''POST to the route to set a values in the Block's readTokens
	array. The JSON POSTed includes the blockText of the block, an
	index in and index out of tokens to be set, and the boolean to
	set the readToken values to.

	POST body: {"blockText": "[[Block.text]]",
					"readIn": int,
					"readOut": int,
					"readValue": Boolean}

	mimetype application/json'''
	JSON = request.get_json()
	blockText = JSON['blockText']
	readIn = JSON['readIn']
	readOut = JSON['readOut']
	print readIn, readOut
	readValue = JSON['readValue']
	currentUser = User.loadUserDataFromPickle(username)
	if JSON['japanese']:
		filteredBlocks = filter(lambda x: 'jText' in vars(x).keys(), currentUser.Blocks)
		activeBlock = next(Block for Block in filteredBlocks if Block.jText == blockText)
		for i, value in enumerate(activeBlock.readSentences):
			if i >= readIn and i < readOut:
				activeBlock.readSentences[i] = readValue
	else:
		filteredBlocks = filter(lambda x: 'text' in vars(x).keys(), currentUser.Blocks)
		activeBlock = next(Block for Block in filteredBlocks if Block.text == blockText)
		for i, value in enumerate(activeBlock.readTokens):
			if i >= readIn and i < readOut:
				activeBlock.readTokens[i] = readValue
	print currentUser.Blocks[3].readSentences
	currentUser.saveUserDataToPickle()
	return json.dumps(currentUser, cls=UserEncoder, sort_keys=True, indent=4, separators=(',', ': '))

#  .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
# / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
#`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
#### STUDYING VIEW ROUTES ####

@app.route('/getDef', methods=['POST'])
def getDef():
	'''the POST body must contain a json dict with {'word': 'x'}
	the function returns a list of definitions'''
	word = request.get_json()['word']
	definition = getLektorekDef(word, LEKTOREK_CACHE_PATH)
	return json.dumps(definition, sort_keys=True, indent=4, separators=(',', ': '))

@app.route('/getDefs', methods=['POST'])
def getDefs():
	'''the POST body must contain a json dict with {'words': [word, ...]}
	the function returns a list of definition lists'''
	words = request.get_json()['words']
	definitions = []
	for word in words:
		definition = getLektorekDef(word, LEKTOREK_CACHE_PATH)
		definitions.append(definition)
	return json.dumps(definitions, sort_keys=True, indent=4, separators=(',', ': '))

@app.route('/getJapaneseDef', methods=['POST'])
def getJapaneseDef():
	'''the POST body must contain a json dict with {'word': lemma}
	the function returns a list of objects. Each object in the list
	has 'japanese' and 'glosses' properties'''
	word = request.get_json()['word']
	print word
	definitionList = getDefinition(word)
	return json.dumps(definitionList, sort_keys=True, indent=4, separators=(',', ': '))

@app.route('/getJapaneseDefs', methods=['POST'])
def getJapaneseDefs():
	'''the POST body must contain a json dict with {'words': [word, ...]}
	the function returns a list of lists of objects. Each list of objects
	is a list of objects with 'japanese' and 'glosses' properties'''
	words = request.get_json()['words']
	definitions = []
	for word in words:
		print word
		definitionObjectList = getDefinition(word)
		definitions.append(definitionObjectList)
	return json.dumps(definitions, sort_keys=True, indent=4, separators=(',', ': '))


#  .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
# / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
#`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'

if __name__ == '__main__':
	app.run(debug=DEBUG, host=HOST, port=PORT)