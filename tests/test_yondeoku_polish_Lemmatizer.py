#! /usr/bin/env python                                                        
# -*- coding: utf-8 -*-

import pytest

from yondeoku.polish.Lemmatizer import Lemmatizer

test_Lemmatizer = Lemmatizer('mock/testDict.json')

def test_it_has_lemma_dict():
    assert test_Lemmatizer.lemmaDict[u'psom'] == [u'pies']

def test_word_yields_inflections():
    assert test_Lemmatizer.lookupLemma(u'lekarkami') == [u'lekarka']


def test_word_not_in_dict_returns_self_in_list():
    assert test_Lemmatizer.lookupLemma(u'awerioawer') == [u'awerioawer']

