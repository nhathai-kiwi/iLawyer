#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
import runVnCoreNLP as nlp
import basicFunction as bf

if __name__ == '__main__':
	#print "Hello"
	# fileInput = '1500Question.txt'
	# words = nlp.processText(fileInput)
	# print len(words)
	fileInput = '1500QuestionwordInFormwordList.txt'
	bf.countingDistinctWords(fileInput)

