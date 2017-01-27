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
from yondeoku.polish.settings import DATA_PATH

DEBUG = True
PORT = 4000
HOST = '0.0.0.0'

testLemmatizer = Lemmatizer(u'mock/testDict.json')

polishLemmatizer = Lemmatizer(u'lemmaDict.json')
@app.route('/polishlemmatizer/<word>', methods=['GET'])
def lookupLemma(word):
	return json.dumps(polishLemmatizer.lookupLemma(word))

@app.route('/')
def index():
	return render_template('main.html')

@app.route('/userOverview')
def userOverview():
	return render_template('userdata.html')

@app.route('/getUserData/<username>', methods=['GET'])
def getUserData(username):
	'''This retrieves the user data for user with specific
	username and returns it as json to the webpage.'''
	activeUser = User.loadUserDataFromPickle(username)
	return jsonpickle.encode(activeUser)

#@app.route('/setReadTokens/<username>', methods=['POST'])
#def setReadTokens(username):
#	currentUser = User.loadUserDataFromPickle(username)
#	currentUser.Blocks[0]
#	print request.form

@app.route('/addBlock/<username>', methods=['POST'])
def addBlock(username):
	'''the POST body must contain a json dict,
	and have mimetype set to application/json
	dict has text property'''
	currentUser = User.loadUserDataFromPickle(username)
	newBlockText = request.get_json()['text']
	newBlock = Block(newBlockText, polishLemmatizer)
	currentUser.addBlock(newBlock)
	currentUser.saveUserDataToPickle()
	return jsonpickle.encode(currentUser)

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

@app.route('/setThreshold/<username>/<threshold>', methods=['POST'])
def setThreshold(username, threshold):
	currentUser = User.loadUserDataFromPickle(username)
	currentUser.threshold = int(threshold)
	currentUser.saveUserDataToPickle()
	return jsonify(currentUser.threshold)

@app.route('/getVocabList/<username>', methods=['POST'])
def getVocabList(username):
	'''the POST body must contain a json dict,
	and have mimetype set to application/json
	dict has text property'''
	currentUser = User.loadUserDataFromPickle(username)
	newText = request.get_json()['text']
	vocabList = currentUser.makeVocabList(newText, polishLemmatizer)
	return json.dumps(vocabList)

if __name__ == '__main__':
	app.run(debug=DEBUG, host=HOST, port=PORT)