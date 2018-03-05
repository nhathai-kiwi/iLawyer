#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
import json
import pprint
import re
import codecs
import myTokenizer as mt
from collections import OrderedDict

def processText():
	data = ''
	lines = []
	with open('seperateQuestion.txt', 'r') as myfile:
		#data = myfile.read().replace('\n', ' ')
		for line in myfile:
			lines.append(line)

	f = open('VnCoreNLP.txt', "w")
	data = []
	for ith in range(0, len(lines)):
		line = lines[ith]
		texts = line.split(chr(9))
		if (len(texts) == 6):
			#print texts[1]
			text = texts[1].replace('_', ' ')
			text = text.lower()
			#if (text[0].isalpha() or text[0].isdigit()):
			data.append(text)
			#print text

	ith = 0
	cnt = 0
	while (ith < len(data)):
		if (data[ith] == "question"):
			#print ith
			#cnt += 1
			#print "Câu hỏi " + data[ith + 1] + ":\n"
			f.write("Câu hỏi " + data[ith + 1] + ":\n")
			jth = ith + 3
			while (jth < len(data)):
				#print "\t" + data[jth]
				if (jth == len(data) - 1):
					ith = len(data)
				if (data[jth] == "question"):
					ith = jth
					break
				f.write("\t" + data[jth] + "\n")
				jth += 1
				
		#print lines[ith]
	#print cnt
	
processText()