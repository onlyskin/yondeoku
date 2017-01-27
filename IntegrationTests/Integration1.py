#! /usr/bin/env python                                                        
# -*- coding: utf-8 -*-

from unittest import TestCase

from yondeoku.polish.User import User
from yondeoku.polish.Block import Block
from yondeoku.polish.Lemmatizer import Lemmatizer

class IntegrationTest(TestCase):

	@classmethod
	def setUpClass(cls):
		print 'instantiating lemmatizer...'
		cls.myLemmatizer = Lemmatizer(u'lemmaDict.json')
		print 'lemmatizer instantiated'
		cls.test_user = User(u'integrationTest1')
		cls.test_block_1 = Block(u'Jesień 2010 roku była jeszcze bardziej świetlista i jasna, niż bywa na ogół w Tokio. Liście miłorzębów długo pozostawały zielone i w końcu niepostrzeżenie, niemal z dnia na dzień, potężne drzewo koło mojego domu stanęło w jaskrawożółtych płomieniach, a najlżejszy podmuch wiatru sprawiał, że sypało iskrami. Starsze panie w białych płóciennych kapeluszach i fartuchach, przygarbione, pałąkonogie i niewielkie jak skrzaty, co ranka z wielką zaciętością zamiatały chodnik, ale zaraz po ich odejściu pokrywała go warstwa liści o sercowatym kształcie. Zainspirował on niegdyś Goethego do napisania miłosnego wiersza dla Marianne, kolejnej miłości jego życia. Pod tekstem dwa własnoręcznie przyklejone przez wieszcza listki splatają się w miłosnym uścisku i jednocześnie odchylają od siebie.', cls.myLemmatizer)
		temp_length = len(cls.test_block_1.text)
		cls.test_user.addBlock(cls.test_block_1)
		cls.test_block_1.setReadTokens(0, temp_length)
		new_text_1 = u'W Japonii miłorząb budzi nie tylko skojarzenia miłosne.'
		cls.vocab_list_text_1 = cls.test_user.makeVocabList(new_text_1, cls.myLemmatizer)
		print 'vocab list:\n', cls.vocab_list_text_1

	def test_vocab_list_text_1(self):
		self.assertEquals(
			self.vocab_list_text_1,
			[]
			)
