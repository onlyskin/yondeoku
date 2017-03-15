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

def test_block_created(session):
	test_block = Block(language='pl', text='test', read_ranges='')
	session.add(test_block)
	session.commit()
	assert test_block.id

def test_block_has_language_and_text(session):
	test_block = Block(language='pl', text='test', read_ranges='')
	session.add(test_block)
	session.commit()
	assert test_block.language == 'pl' and test_block.text == 'test'

def test_block_has_correct_user_id_attr(session):
	sam = User(username='sam', password='password')
	test_block = Block(language='pl', text='test', read_ranges='')
	sam.blocks.append(test_block)
	session.add(sam)
	session.commit()
	assert test_block.user == sam

def test_block_appended_to_user(session):
    sam = User(username='sam', password='password')
    test_block = Block(language='pl', text='test', read_ranges='')
    sam.blocks.append(test_block)
    session.add(sam)
    session.commit()
    assert len(session.query(User).first().blocks) == 1

def test_block_language_cannot_be_null(session):
    x = Block(text='testing', read_ranges='')
    session.add(x)
    with pytest.raises(IntegrityError):
        session.commit()

def test_block_text_cannot_be_null(session):
    x = Block(language='pl', read_ranges='')
    session.add(x)
    with pytest.raises(IntegrityError):
        session.commit()

def test_block_read_ranges_defaults_to_empty_list_string(session):
    x = Block(language='pl', text='testing')
    session.add(x)
    session.commit()
    assert x.read_ranges == '[]'

def test_block_text_cannot_be_empty_string(session):
    x = Block(language='pl', text='', read_ranges='[]')
    session.add(x)
    with pytest.raises(IntegrityError):
        session.commit()

def test_block_language_cannot_be_empty_string(session):
    x = Block(language='', text='testing', read_ranges='[]')
    session.add(x)
    with pytest.raises(IntegrityError):
        session.commit()
