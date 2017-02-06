#! /usr/bin/env python                                                        
# -*- coding: utf-8 -*-

SENTENCE_BREAKERS = u'。！？'
PUNCTUATION = u'「」『』（）〟〝、'

####################
Blocks:
- treat a little differently as we dont currently have a way to get the direct
correspondence between the exact section of the text and the tokens
sentences: [{
	startIndex (into original text):
	charLength:
	tokens: (generated with makeTokens at block creation)
}]
