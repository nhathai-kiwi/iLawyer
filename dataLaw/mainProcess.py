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
#connect database
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

#reading vnWord11K
def loadVnWord():
	global vnWords
	vnWords = []
	with open('Viet11K.txt') as words:
		#vnWords.append(words)
		for line in words:
			vnWords.append(line[:-1])
loadVnWord()

#format String: remove character neither alpha nor digit
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

#check string b is subString of a: 
def checkSubString(a, b):
	if (b.find(a) > -1):
		return True
	return False

#get keyword from text
sizePop = 20
def extractKeyWord(mainText):
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
	
	ret = []
	for i in range(len(topWord) - 1, -1, -1):
		numTop += 1
		if (numTop > 10):
			break
		top = topWord[i]
		per = (100.0 * top[0]) / lengthMainText
		#id_keyword = top[1] + 1
		#print top[0], " ", vnWords[top[1]], " ", top[1], " ", per
		ret.append((top[1] + 1, per))
	return ret

def euclideanDistance(a, b):
	#print "euclideanDistance"
	ret = 0.0
	for i in a:
		value = 0.0
		for j in b:
			if (j[0] == i[0]):
				value = j[1]
				break
		ret += (i[1] - value) * (i[1] - value)
	return ret
def getQuantityQuestion():
	query = "SELECT id from questions"
	cursor.execute(query)
	#ret = cursor.rowcount
	cnt = 0
	for i in cursor.fetchall():
		cnt += 1
	#print "CNT = ", cnt
	# #cursor.close()
	#cnx.close()
	return cnt
	

def getValue(numberQuestion):
	query = "SELECT id_keyword, percentage FROM keywordquestions WHERE id_question = %s" % numberQuestion  
	cursor.execute(query)
	cnt = 0
	ret = cursor.fetchall()
	for row in ret:
	    cnt += 1
	    #print "Cnt = ", cnt
	    #print "cnt = ", cnt, row
	#     #print row['id_keyword'], " ", row[percentage]
	#     #print type(row)
	#     #print row[0], " ", row[1]
	# #print type(ret)
	#cursor.close()
	#cnx.close()
	return ret
def getAnswer(numberQuestion):
	query = "SELECT * FROM answers WHERE id = %s" % numberQuestion  
	cursor.execute(query)
	cnt = 0
	ret = cursor.fetchall()
	for row in ret:
	    cnt += 1
	return row[1]
	    ##print "cnt = ", cnt, row
	#     #print row['id_keyword'], " ", row[percentage]
	#     #print type(row)
	#     #print row[0], " ", row[1]
	# #print type(ret)
	#cursor.close()
	#cnx.close()
	#return ret
def getQuestion(numberQuestion):
	query = "SELECT * FROM questions WHERE id = %s" % numberQuestion  
	cursor.execute(query)
	cnt = 0
	ret = cursor.fetchall()
	for row in ret:
	    cnt += 1
	    print row[1]
	    ##print "cnt = ", cnt, row
	#     #print row['id_keyword'], " ", row[percentage]
	#     #print type(row)
	#     #print row[0], " ", row[1]
	# #print type(ret)
	#cursor.close()
	#cnx.close()
	#return ret

def processInput():
	textInput = ""
	
	with open('inputQuestion.txt', "r") as myfile:
		data = myfile.read().replace('\n', '')
		textInput = data.decode('utf-8')
	#print "textInput ", textInput
	textInput = reformat(textInput)
	#print textInput
	retInput = extractKeyWord(textInput)
	#getQuantityQuestion()
	#quantityQuestion = getQuantityQuestion()
	#print "type input: ", type(retInput), 
	quantityQuestion = getQuantityQuestion()
	print "VALUE: ", quantityQuestion

	# for i in retInput:
	#  	print i[0], " ", i[1]
	minDistance = 1e9
	pos = -1
	for i in range(0, quantityQuestion):
		questionIth = getValue(i)
		distanceIth = euclideanDistance(retInput, questionIth)
		if (minDistance > distanceIth):
			minDistance = distanceIth
			pos = i
	print "minDistance: ", minDistance, "pos ", pos
	# print "Question: "
	# getQuestion(pos)
	# print "Answer: "
	f = open('answerQuestion.txt', "w")
	answer = getAnswer(pos)
	# print "Type = ", type(answer)
	# for i in answer:
	# 	f.write(str(i))
	f.write(answer)
processInput()
