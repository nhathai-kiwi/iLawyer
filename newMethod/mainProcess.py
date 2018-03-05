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

import myTokenizer as mt
from heapq import heappush, heappop


#connect database
config = {
	'user': 'root',
	'password': 'root',
	'port': '8889',
	'host': '127.0.0.1',
	'database': 'iLawyerV18_02',
 }

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()


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
	query = "SELECT keyword, percentage FROM keywordquestions WHERE id_question = %s" % numberQuestion  
	cursor.execute(query)
	cnt = 0
	ret = cursor.fetchall()
	for row in ret:
	    cnt += 1
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
	#textInput = reformat(textInput)
	#print textInput
	x = mt.MyTokenizer(textInput)
	#words = mt.MyTokenizer(mainText)
	#words = x.getTopWords()
	retInput = x.getTopWords()
	wordQuestion = []
	for i in retInput:
		wordQuestion.append((i.word, i.percentage))

	# for i in retInput:
	# 	print i.cnt, " ", i.word, i.percentage
	# 	print type(i)

	quantityQuestion = getQuantityQuestion()
	print "VALUE: ", quantityQuestion

	# for i in retInput:
	#  	print i[0], " ", i[1]
	minDistance = 1e9
	pos = -1
	for i in range(0, quantityQuestion):
		questionIth = getValue(i)
		distanceIth = euclideanDistance(wordQuestion, questionIth)
		if (minDistance > distanceIth):
			minDistance = distanceIth
			pos = i
	print "minDistance: ", minDistance, "pos ", pos
	# print "Question: "
	# getQuestion(pos)
	# print "Answer: "
	f = open('answerQuestion.txt', "w")
	#answer = getAnswer(pos)
	answer = "HungNM"
	f.write(answer)
processInput()
