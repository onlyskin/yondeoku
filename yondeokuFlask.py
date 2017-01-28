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

DEBUG = True
PORT = 4000
HOST = '0.0.0.0'

testLemmatizer = Lemmatizer(u'mock/testDict.json')

polishLemmatizer = Lemmatizer(u'lemmaDict.json')

#  .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
# / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
#`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
#### Root Pages ####

@app.route('/')
def index():
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
	return jsonpickle.encode(activeUser)

#.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
@app.route('/addBlock/<username>', methods=['POST'])
def addBlock(username):
	'''The POST body must contain a json dict, and have mimetype set to
	application/json dict, has text property with the Block text. Route
	returns the jsonpickled Block, intended to be appended to the block
	list in the client side state.'''
	currentUser = User.loadUserDataFromPickle(username)
	newBlockText = request.get_json()['text']
	newBlock = Block(newBlockText, polishLemmatizer)
	currentUser.addBlock(newBlock)
	currentUser.saveUserDataToPickle()
	return jsonpickle.encode(newBlock)

@app.route('/deleteBlock/<username>', methods=['POST'])
def deleteBlock(username):
	'''POST to this route. JSON body. {"text": "[[Block.text]]"}
	Route returns deleted to confirm Block removal. Client to AWAIT
	confirmation.'''
	currentUser = User.loadUserDataFromPickle(username)
	blockText = request.get_json()['text']
	deleted = currentUser.deleteBlock(blockText)
	#deleted will be None if no block matched the text
	if deleted:
		currentUser.saveUserDataToPickle()
		return 'deleted'

#.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
@app.route('/setKnownWords/<username>', methods=['POST'])
def setKnownWords(username):
	'''the POST body must contain a json list,
	and have mimetype set to application/json'''
	currentUser = User.loadUserDataFromPickle(username)
	words = request.get_json()
	for word in words:
		currentUser.known.add(word)
	currentUser.saveUserDataToPickle()
	return jsonify(currentUser.known)

@app.route('/removeKnownWords/<username>', methods=['POST'])
def removeKnownWords(username):
	'''the POST body must contain a json list,
	and have mimetype set to application/json'''
	currentUser = User.loadUserDataFromPickle(username)
	words = request.get_json()
	for word in words:
		currentUser.known.remove(word)
	currentUser.saveUserDataToPickle()
	return jsonify(currentUser.known)

#.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
@app.route('/setThreshold/<username>/<threshold>', methods=['POST'])
def setThreshold(username, threshold):
	currentUser = User.loadUserDataFromPickle(username)
	currentUser.threshold = int(threshold)
	currentUser.saveUserDataToPickle()
	return jsonify(currentUser.threshold)

#.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.


#@app.route('/setReadTokens/<username>', methods=['POST'])
#def setReadTokens(username):
#	currentUser = User.loadUserDataFromPickle(username)
#	currentUser.Blocks[0]
#	print request.form


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
	return json.dumps(definition)

@app.route('/getDefs', methods=['POST'])
def getDefs():
	'''the POST body must contain a json dict with {'words': [word, ...]}
	the function returns a list of definition lists'''
	words = request.get_json()['words']
	definitions = []
	for word in words:
		definition = getLektorekDef(word, LEKTOREK_CACHE_PATH)
		definitions.append(definition)
	return json.dumps(definitions)

#  .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
# / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
#`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'

if __name__ == '__main__':
	app.run(debug=DEBUG, host=HOST, port=PORT)