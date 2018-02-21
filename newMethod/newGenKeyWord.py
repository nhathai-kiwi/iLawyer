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

config = {
	'user': 'root',
	'password': 'root',
	'port': '8889',
	'host': '127.0.0.1',
	'database': 'iLawyerV18_02',
 }

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()


listTable = ['keywordquestions', 'keywordanswers']
listAttribute = ['id_question', 'id_answer']

def extractKeyWord(cursor, id_question, mainText, typeTable):
	#print "Tuan"
	
	#x = mt.myTokenizer(mainText)
	x = mt.MyTokenizer(mainText)
	#words = mt.MyTokenizer(mainText)
	words = x.getTopWords()
	for i in words:
		#print i.word, " ", i.percentage, " ", i.cnt
		try:
			query = "INSERT INTO " + listTable[typeTable] + "(" + listAttribute[typeTable] + ", keyword, cnt, percentage) VALUES ('%s', '%s', '%s', '%s');" % (id_question, i.word, i.cnt, i.percentage)
			cursor.execute(query)
		except mysql.connector.Error as err:
			print("Failed INSERT: {}".format(err))
			pass

def readDataJSON():
	global originalQA
	global modifiedQA
	originalQA = []
	modifiedQA = []

	with open('lmgiaData.json') as json_data:
		d = json.load(json_data)
		data = d['item']
		print len(data)
		cnt = 0
		ans = " "
		ques = " "
		for i in range(0, len(data)):
			qa = data[i]
			cnt += 1
			print "Question Number: ", cnt 
			ques = qa['question']
			ans = qa['answer']
			#print ques
			#print ans
			# originalQA.append((qa['question'], qa['answer']))
			# modifiedQA.append((ques, ans))
			extractKeyWord(cursor, i + 1, ques, 0)
			extractKeyWord(cursor, i + 1, ans, 1)

	cnx.commit()
	cursor.close()
	cnx.close()


readDataJSON()

#print modifiedQA[0][0]
#extractKeyWord(modifiedQA[0][0])