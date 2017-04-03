#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import json
import os

from yondeokuApp import app as realApp, db as _db, User
from flask import url_for

from yondeoku.japanese.grammarWords import jaGrammarWords

TESTDB_PATH = 'sqlite:////tmp/fake.db'
realApp.config['SQLALCHEMY_DATABASE_URI'] = TESTDB_PATH 
realApp.config['TESTING'] = True

@pytest.fixture(scope='session')
def app(request):
    ctx = realApp.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return realApp

@pytest.fixture(scope='function')
def db(app, request):
    """Session-wide test database."""

    if os.path.exists(TESTDB_PATH):
        os.unlink(TESTDB_PATH)
    _db.init_app(app)

    _db.create_all()

    fakeUser = User(username='fakeUser', password='password')
    _db.session.add(fakeUser)
    _db.session.commit()

    def teardown():
        _db.drop_all()
        # os.unlink(TESTDB_PATH)

    request.addfinalizer(teardown)
    return _db

def test_get_grammatical_words_route_returns_200(client):
	assert client.get(url_for('getGrammaticalWords', language='pl')).status_code == 200

def test_get_grammatical_words_route_returns_correct_length_json(client):
	returnedJSON = client.get(url_for('getGrammaticalWords', language='ja')).json
	assert len(returnedJSON) == len(jaGrammarWords)

def test_index_route_returns_html(app):
	client = realApp.test_client()
	response = client.get('/').response
	assert 'html' in list(response)[0]

def test_user_data_route(app, db):
	client = realApp.test_client()
	response = client.get(url_for('getUserData', username='fakeUser'))
	data = response.data
	data_keys = json.loads(data).keys()
	data_keys.sort()
	assert data_keys == ['blocks', 'id', 'known', 'threshold', 'username']


