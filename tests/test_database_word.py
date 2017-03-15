#! /usr/bin/env python                                                        
# -*- coding: utf-8 -*-
import pytest
import os

from sqlalchemy.exc import IntegrityError

from yondeokuApp import app as realApp
from yondeokuApp import db as _db
from yondeokuApp import User, Block, Word

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

def test_word_created(session):
    kw = Word(language='pl', word='kot')
    user = User(username='sam', password='password')
    session.add(user)
    session.add(kw)
    session.commit()
    assert kw.id > 0 and kw.language == 'pl' and kw.word == 'kot'

def test_same_word_same_lang_raises_error(session):
    kw1 = Word(language='pl', word='kot')
    kw2 = Word(language='pl', word='kot')
    session.add(kw1)
    session.add(kw2)
    with pytest.raises(IntegrityError):
        session.commit()

def test_same_word_diff_lang_is_okay(session):
    kw1 = Word(language='pl', word='kot')
    kw2 = Word(language='jp', word='kot')
    session.add(kw1)
    session.add(kw2)
    session.commit()

def test_diff_word_same_lang_is_okay(session):
    kw1 = Word(language='pl', word='kot')
    kw2 = Word(language='pl', word='pies')
    session.add(kw1)
    session.add(kw2)
    session.commit()

def test_word_language_cannot_be_empty_string(session):
    kw = Word(language='', word='kot')
    session.add(kw)
    with pytest.raises(IntegrityError):
        session.commit()

def test_word_word_cannot_be_empty_string(session):
    kw = Word(language='pl', word='')
    session.add(kw)
    with pytest.raises(IntegrityError):
        session.commit()

def test_user_has_two_known_words(session):
    sam = User(username='sam', password='password')
    kw1 = Word(language='pl', word='kot')
    kw2 = Word(language='pl', word='pies')
    sam.known.append(kw1)
    sam.known.append(kw2)
    session.add(sam)
    session.commit()
    sam_known = list(session.query(User).first().known)
    assert kw1 in sam_known and kw2 in sam_known

def test_known_word_has_two_users(session):
    sam = User(username='sam', password='password')
    hector = User(username='hector', password='password')
    kw1 = Word(language='pl', word='pies')
    sam.known.append(kw1)
    hector.known.append(kw1)
    session.add(kw1)
    session.commit()
    pies_users = list(session.query(Word).first().users)
    assert sam in pies_users and hector in pies_users
