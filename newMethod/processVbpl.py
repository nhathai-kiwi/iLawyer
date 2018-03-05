#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
import json
import pprint
import mysql.connector
from mysql.connector import (connection)
import re
import codecs
import myTokenizer as mt
from collections import OrderedDict

def processArticles(mainText):
	x = mt.MyTokenizer(mainText)
	#words = mt.MyTokenizer(mainText)
	#words = x.getTopWords()
	retInput = x.getTopWords()
	for i in retInput:
		print i.word, i.cnt
	x.printOut()
def processText():
	data = ''
	lines = []
	with open('wordSegmentation.txt', 'r') as myfile:
		#data = myfile.read().replace('\n', ' ')
		for line in myfile:
			lines.append(line)
	# print len(lines)
	# for  i in range(0, 10):
	# 	print lines[i]
	# 	texts = lines[i].split(" ")
	# 	print "\t", len(texts), len(lines[i])
	# print len(lines[0])
	# for i in range(0, len(lines[0])):
	# 	print i, " ", lines[0][i], " ", ord(lines[0][i]), chr(ord(lines[0][i]) )
	data = []
	for ith in range(0, len(lines)):
		line = lines[ith]
		texts = line.split(chr(9))
		if (len(texts) == 6):
			#print texts[1]
			text = texts[1].replace('_', ' ')
			text = text.lower()
			data.append(text)
			#print text
			#data +=
	# for i in range(0, 100):
	# 	print data[i]
	cnt = 0
	lenData = len(data)
	arr = []
	pos = 0
	while (pos < lenData):
		#cnt += 1
		if (data[pos][0] == '$'):
			#cnt += 1
			#print data[pos], data[pos + 1]
			newArr = []
			#arr.append([])
			for j in range(pos + 1, lenData):
				newArr.append(data[j])
				if (data[j][0] == '$'):
					pos = j
					break
				if (j == lenData - 1):
					pos = lenData
			arr.append(newArr)
		else:
			break
	f = open('keyword213Articles.txt', "w")

	for i in arr:
		dicts = {}
		#print "Dieu: ", i[0]
		f.write("Điều: " + i[0] + "\n")
		for j in i:
			if (j[0].isalpha()):
				#print j
				value = dicts.get(j , 0)
				dicts[j] = value + 1
		dictsSort = OrderedDict(sorted(dicts.items(), key=lambda x: x[1], reverse = True))
		maxWord = 0
		for key, value in dictsSort.items():
			#print key, " ", value
			f.write("\t" + key + " " + str(value) + "\n")
			maxWord += 1
			if (maxWord >= 20):
				break


	#print data
	# articles = data.split('$$$$')
	# print len(articles)
	# print articles[1]
	# for i in articles:
	# 	print i
	#print articles[1]
	#print articles[213]
	#for i in range(1, 214):
	#processArticles(articles[1])	

processText()
