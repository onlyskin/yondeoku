#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import json

from yondeokuApp import app as realApp
from flask import url_for

from yondeoku.japanese.grammarWords import jaGrammarWords

realApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/fake.db'
realApp.config['TESTING'] = True

@pytest.fixture
def app(request):
    ctx = realApp.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return realApp

def test_get_grammatical_words_route_returns_200(client):
	assert client.get(url_for('getGrammaticalWords', language='pl')).status_code == 200

def test_get_grammatical_words_route_returns_correct_length_json(client):
	returnedJSON = client.get(url_for('getGrammaticalWords', language='ja')).json
	assert len(returnedJSON) == len(jaGrammarWords)

def test_index_route_returns_html(app):
	client = realApp.test_client()
	response = client.get('/').response
	assert 'html' in list(response)[0]


#####THIS FILE CURRENTLY KEEPS GETTING BROKEN WHEN WE
# RUN THE FULL TEST SUITE - SOMETHING SOMEWHERE IS
# ERASING THE 'fake.db' DATABASE DURING THE TESTS
# FIX THIS NEXT, RIGHT NOW WHEN IT HAPPENS WE CAN
# RUN THE FILE create_fake_db.py WHICH WILL REMAKE IT
def test_user_data_route(app):
	client = realApp.test_client()
	response = client.get(url_for('getUserData', username='fakeUser'))
	data = response.data
	data_keys = json.loads(data).keys()
	data_keys.sort()
	assert data_keys == ['blocks', 'id', 'known', 'threshold', 'username']





