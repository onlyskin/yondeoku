#! /usr/bin/env python                                                        
# -*- coding: utf-8 -*-

#Notes on the lemmaDict.json file
#This was generated from the 'lemmatization-pl.txt' file
#which was downloaded from http://www.lexiconista.com/datasets/lemmatization/
#I generated a json dict mapping from {inflected: [base, ...]}
#The problem is the original file didn't contain the base forms of words among
#the inflected forms, which means that in the case that you input a base
#form of a word which is also an inflected form of another word, you will
#get back a list with the base form of the other word, but not the base form of this word
#hopefully this shouldn't cause too many issues in general as it should be a fairly
#rare occurence

DICT_PATH = u'lemmaDict.json'
DATA_PATH = u'data/'
LEKTOREK_CACHE_PATH = u'lektorek_cache.json'
PUNCTUATION_STRING = u'!?,.:;()[]{}/„”‚’-"\''