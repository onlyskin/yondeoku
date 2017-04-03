import json
import codecs

import pytest

from yondeoku.polish.getLektorekDef import (getCorrectDef, checkLektorekCache,
        cacheLektorekResult, getLektorekJSONFromCache)

mock_cache_path = 'mock/mockLektorekCache.json'
emptyJSON = {}

def setup_module(module):
    with codecs.open('mock/testJSONLektorek.json', 'r', 'utf-8') as f:
        global testJSON
        testJSON = json.loads(f.read())
    with codecs.open(mock_cache_path, 'r', 'utf-8') as f:
        global mock_cache_original_state
        mock_cache_original_state = json.loads(f.read())

def teardown_module(module):
    with codecs.open(mock_cache_path, 'w', 'utf-8') as f:
        f.write(json.dumps(mock_cache_original_state, sort_keys=True, indent=4,
                    separators=(',', ': ')))

def test_it_gets_correct_polish_word():
        assert testJSON['results'][0]['polish_word'] == 'chmura'

def test_it_gets_correct_def():
    assert getCorrectDef(testJSON) == [u"<span class=\"bold\">chmura </span>" \
            "<span class=\"italics\">f </span>cloud"]

def test_it_gets_correct_from_empty_json():
    assert getCorrectDef(emptyJSON) == []

def test_check_lektorek_cache_true_for_pyszny():
    assert checkLektorekCache(u'pyszny', mock_cache_path)

def test_check_lektorek_cache_false_for_wiarygodny():
    assert not checkLektorekCache(u'wiarygodny', mock_cache_path)

def test_get_lektorek_json_from_cache():
    assert getLektorekJSONFromCache('pyszny', mock_cache_path) == {'tested': 'yes'}

def test_cache_lektorek_result():
    cacheLektorekResult('testing', {'testing a result': 'tested'},
            mock_cache_path)
    assert (getLektorekJSONFromCache('testing', mock_cache_path) ==
            {"testing a result": "tested"})

