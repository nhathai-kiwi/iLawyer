#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
import MySQLdb
import json
import pprint
import mysql.connector
from mysql.connector import (connection)
import re
import codecs

from heapq import heappush, heappop

global originalQA
global modifiedQA
global vnWords
def reformat(qa):
	lastChar = ""
	l = []
	l.append(' ')
	for c in qa:
		if (c.isalpha() or c.isdigit()):
			if (lastChar == " "):
				l.append(c)
			elif (lastChar.isalpha() or lastChar.isdigit()):
				l.append(c)
			else:
				l.append(' ')
				l.append(c)
		elif (c == " "):
			if (lastChar != " "):
				l.append(c)
		# elif (ord(c) != 10):
		# 	l.append(c)
		lastChar = c
	l.append(' ')
	#ret = ''.join(l)
	return ''.join(l)

def loadVnWord():
	global vnWords
	vnWords = []
	with open('Viet11K.txt') as words:
		#vnWords.append(words)
		for line in words:
			vnWords.append(line[:-1])
loadVnWord()

def checkSubString(a, b):
	if (b.find(a) > -1):
		return True
	return False
config = {
	'user': 'root',
	'password': 'root',
	'port': '8889',
	'host': '127.0.0.1',
	'database': 'iLawyer',
 }

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

DB_NAME = 'iLawyer'


sizePop = 20
listTable = ['keywordquestions', 'keywordanswers']
listAttribute = ['id_question', 'id_answer']

def extractKeyWord(cursor, id_question, mainText, typeTable):
	global sizePop
	print "Size: ", sizePop

	pq = []
	for i in range(0, len(vnWords)):
		k = " " + vnWords[i] + " "
		cnt = mainText.count(k)
		if (cnt > 0):
			len1 = (vnWords[i].count(" ") + 1) * cnt
			heappush(pq, (len1, i))
			if (len(pq) > sizePop):
				heappop(pq)

	lengthMainText = mainText.count(' ') - 2
	topWord = []
	# print "Phase 01:"
	# while pq:
	# 	i = heappop(pq)
	# 	topWord.append(i)
	# 	print i[0], vnWords[i[1] ]

	# for i in range(len(topWord) - 1, -1, -1):
	# 	top = topWord[i]
	# 	pro = (100.0 * top[0]) / lengthMainText
	# 	print top[0], " ", vnWords[ top[1] ], " ", pro
	
	# print "Phase 02:"

	valueTopFirst = []
	for top in topWord:
		valueTopFirst.append(top[0])

	for i in range(0, len(topWord)):
		top1 = topWord[i]
		for j in range(0, len(topWord)):
			top2 = topWord[j]
			if (top1 != top2):
				checkValue = checkSubString(vnWords[ top1[1] ], vnWords[ top2[1] ]) #top1[1] la xau con cua top2[1]
				if (checkValue == True):
					valueTopFirst[i] -= valueTopFirst[j] / (vnWords[ top2[1] ].count(" ") + 1)

	for i in range(0, len(topWord)):
		if (valueTopFirst[i] > 0):
			heappush(pq, (valueTopFirst[i], topWord[i][1]))

	topWord = []
	while pq:
		i = heappop(pq)
		topWord.append(i)
	numTop = 0

	for i in range(len(topWord) - 1, -1, -1):
		numTop += 1
		if (numTop > 10):
			break
		top = topWord[i]
		per = (100.0 * top[0]) / lengthMainText
		id_keyword = top[1] + 1
		print top[0], " ", vnWords[top[1]], " ", top[1], " ", per
		query = "INSERT INTO " + listTable[typeTable] + "(" + listAttribute[typeTable] + ", id_keyword, percentage) VALUES ('%s', '%s', '%s')" % (id_question, id_keyword, per)
		#print query
		cursor.execute(query)

def readDataJSON():
	global originalQA
	global modifiedQA
	originalQA = []
	modifiedQA = []

	with open('lmgiaData.json') as json_data:
		d = json.load(json_data)
		#print type(d)
		#detailQuestion = d["detailQuestion"]
		#answerQuestion = d["answerQuestion"]
		#print answerQuestion
		data = d['item']
		print len(data)
		cnt = 0
		ans = " "
		ques = " "
		for i in range(0, len(data)):
			qa = data[i]
			cnt += 1
			print "Question Number: ", cnt 
			# print "Question: ", qa['question']
			# print "Answer: ", qa['answer']
			# # # for h in qa['question']:
			# 	print h, type(h)
			ques = reformat(qa['question'])
			ans = reformat(qa['answer'])
			#print ques
			#print ans
			originalQA.append((qa['question'], qa['answer']))
			modifiedQA.append((ques, ans))
			# print ques
			# print ans
			extractKeyWord(cursor, i + 1, ques, 0)
			extractKeyWord(cursor, i + 1, ans, 1)

	cnx.commit()
	cursor.close()
	cnx.close()


readDataJSON()

#print modifiedQA[0][0]
#extractKeyWord(modifiedQA[0][0])