#! /usr/bin/env python                                                        
# -*- coding: utf-8 -*-
import re

from yondeoku.AbstractSectionizer import AbstractSectionizer
from yondeoku.Section import Section
from yondeoku.makeSections import makeSections

class plSectionizer(AbstractSectionizer):
	'''Concrete Polish Sectionizer class.'''

	def __init__(self):
		super(plSectionizer, self).__init__('pl')
	
	def sectionize(self, text):
		'''Returns a list of {Section} objects given a
		{gBlock} object.'''
		sections = makeSections(text, [u'\.', u'!', u'\?'], u'”')
		return sections
