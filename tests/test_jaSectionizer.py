#! /usr/bin/env python                                                        
# -*- coding: utf-8 -*-
import pytest

from yondeoku.japanese.jaSectionizer import jaSectionizer

def test_it_has_lang():
	assert jaSectionizer().language == 'ja'
