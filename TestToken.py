from unittest import TestCase

from yondeoku.polish.Token import Token

class TestToken(TestCase):

	@classmethod
	def setUpClass(cls):
		cls.realToken = Token(',.real,', 20)

	def test_tokenText(self):
		self.assertEquals(
			self.realToken.tokenText,
			',.real,'
		)

	def test_strippedText(self):
		self.assertEquals(
			self.realToken.strippedText,
			'real'
		)

	def test_startIndex(self):
		self.assertEquals(
			self.realToken.startIndex,
			20
		)

	def test_strippedStartIndex(self):
		self.assertEquals(
			self.realToken.strippedStartIndex,
			22
		)