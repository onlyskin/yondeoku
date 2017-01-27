import json
import codecs

from unittest import TestCase

from yondeoku.polish.getLektorekDef import getCorrectDef, checkLektorekCache, cacheLektorekResult, getLektorekDefFromCache

class TestGetLektorekDef(TestCase):

	@classmethod
	def setUpClass(cls):
		cls.emptyJSON = {}
		f = open('mock/testJSONLektorek.json', 'r')
		cls.testJSON = json.loads(f.read())
		f.close()
		cls.mock_cache_path = 'mock/mockLektorekCache.json'
		f = codecs.open(cls.mock_cache_path, 'r', 'utf-8')
		cls.mock_cache_original_state = json.loads(f.read())
		f.close()

	@classmethod
	def tearDownClass(cls):
		f = codecs.open(cls.mock_cache_path, 'w', 'utf-8')
		f.write(json.dumps(cls.mock_cache_original_state, sort_keys=True, indent=4, separators=(',', ': ')))

	def test_right_polish_word(self):
		self.assertEquals(
			self.testJSON['results'][0]['polish_word'],
			'chmura'
		)

	def test_get_correct_def(self):
		self.assertEquals(
			getCorrectDef(self.testJSON),
			[u"<span class=\"bold\">chmura </span><span class=\"italics\">f </span>cloud"]
			)

	def test_empty_json_correct(self):
		self.assertEquals(
			getCorrectDef(self.emptyJSON),
			[]
			)

	def test_check_lektorek_cache_true_for_pyszny(self):
		self.assertTrue(checkLektorekCache(u'pyszny', self.mock_cache_path))

	def test_check_lektorek_cache_false_for_wiarygodny(self):
		self.assertFalse(checkLektorekCache(u'wiarygodny', self.mock_cache_path))

	def test_get_lektorek_def_from_cache(self):
		self.assertEquals(
			getLektorekDefFromCache('pyszny', self.mock_cache_path),
			["<span class=\"bold\">pyszny </span><span class=\"italics\">aj </span>elegant, luxurious. <span class=\"italics\">av </span><span class=\"bold\">pysznie</span>"]
			)

	def test_cache_lektorek_result(self):
		cacheLektorekResult('testing', ["testing a result"], self.mock_cache_path)
		self.assertEquals(
			getLektorekDefFromCache('testing', self.mock_cache_path),
			["testing a result"]
			)