#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import os
import json

from sqlalchemy.exc import IntegrityError

from yondeokuApp import app as realApp
from yondeokuApp import db as _db
from yondeokuApp import User, Block, Word, ModelEncoder

TESTDB_PATH = 'sqlite:////tmp/test.db'

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

    def teardown():
        _db.drop_all()
        # os.unlink(TESTDB_PATH)

    request.addfinalizer(teardown)
    return _db

@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session

def test_model_can_handle_unicode(session):
    hanako = User(username=u'花子', password='password')
    session.add(hanako)
    session.commit()
    assert hanako.username == u'花子'

def test_user_has_id_username_and_password(session):
	sam = User(username='sam', password='password')
	session.add(sam)
	session.commit()
	assert sam.id and sam.username == 'sam' and sam.password == 'password'

def test_user_username_must_be_unique(session):
    sam1 = User(username='sam')
    sam2 = User(username='sam')
    session.add(sam1)
    session.add(sam2)
    with pytest.raises(IntegrityError):
        session.commit()

def test_user_username_cannot_be_null(session):
    x = User(password='password')
    session.add(x)
    with pytest.raises(IntegrityError):
        session.commit()

def test_user_password_cannot_be_null(session):
    x = User(username='test')
    session.add(x)
    with pytest.raises(IntegrityError):
        session.commit()

def test_user_username_cannot_be_empty_string(session):
    x = User(username='', password='password')
    session.add(x)
    with pytest.raises(IntegrityError):
        session.commit()

def test_user_password_cannot_be_empty_string(session):
    x = User(username='test', password='')
    session.add(x)
    with pytest.raises(IntegrityError):
        session.commit()

def test_user_has_threshold(session):
    x = User(username='test', password='password', threshold=10)
    session.add(x)
    session.commit()
    assert x.threshold == 10

def test_threshold_defaults_to_8(session):
    x = User(username='test', password='password')
    session.add(x)
    session.commit()
    assert x.threshold == 8

def test_threshold_cannot_be_negative(session):
    x = User(username='test', password='password', threshold=-4)
    session.add(x)
    with pytest.raises(IntegrityError):
        session.commit()

def test_threshold_cannot_be_0(session):
    x = User(username='test', password='password', threshold=0)
    session.add(x)
    with pytest.raises(IntegrityError):
        session.commit()

def test_User_json_has_id_username_threshold(session):
    x = User(username='test', password='password')
    x.gBlocks = []
    session.add(x)
    session.commit()
    reconstituted_json = json.loads(json.dumps(x, cls=ModelEncoder))
    assert (reconstituted_json['id'] is not None
        and reconstituted_json['username'] is not None
        and reconstituted_json['threshold'] is not None)

def test_User_json_has_correct_len_known(session):
    x = User(username='test', password='password')
    x.gBlocks = []
    kw1 = Word(language='pl', word='kot')
    kw2 = Word(language='pl', word='pies')
    x.known.append(kw1)
    x.known.append(kw2)
    session.add(x)
    session.commit()
    reconstituted_json = json.loads(json.dumps(x, cls=ModelEncoder))
    assert len(reconstituted_json['known']) == 2

def test_Word_json_has_language_and_word(session):
    kw1 = Word(language='pl', word='kot')
    session.add(kw1)
    session.commit()
    reconstituted_json = json.loads(json.dumps(kw1, cls=ModelEncoder))
    assert (reconstituted_json['language'] is not None
        and reconstituted_json['word'] is not None)
