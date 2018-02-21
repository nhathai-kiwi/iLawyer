#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#as3:/usr/local/lib/python2.7/site-packages# cat sitecustomize.py
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
import MySQLdb
import json
import pprint
import mysql.connector
from heapq import heappush, heappop

from mysql.connector import (connection)


# db = MySQLdb.connect(host="localhost",     # your host, usually localhost
#                      user="root",         # your username
#                      passwd="root",
#                      db = "mysql")  # your password
# you must create a Cursor object. It will let
# you execute all the queries you need
def connectServer():
	db = connection.MySQLConnection(user='root', password='root',
                                 host='127.0.0.1', port = '8889',
                                 database='iLawyer')
	# # Use all the SQL you like
	cur = db.cursor()
	cur.execute("""CREATE TABLE IF NOT EXISTS Teacher(
    TeacherUsername VARCHAR(255) PRIMARY KEY,
    TeacherPassword TEXT)""")

	cur.execute("SHOW DATABASES")
	#ver = cur.fetchone()
	#print "Database version : %s " % ver
	# print all the first cell of all the rows
	#print "Database version: %s" % (cur.fetchone())
	cnt = 0
	for row in cur.fetchall():
	    cnt += 1
	    print "cnt = ", cnt, row

	db.close()

#connectServer()

global pairQAs
def convertDatabase():
	data = []
	global pairQAs
	pairQAs = []

	with open('result.json') as json_data:
		d = json.load(json_data)
		#print type(d)
		#detailQuestion = d["detailQuestion"]
		#answerQuestion = d["answerQuestion"]
		#print answerQuestion
		print len(d)

		for j in range(0, len(d)):
		# print type(d[0])
		# print type(d[0]['detailQuestion'])
		# print type(d[0]['answerQuestion'])
		# print len(d[0]['detailQuestion'])
			#print "Question number ", j
			ans = " "
			ques  = " "
			for h in d[j]['answerQuestion']:
				for i in h:
					if (i.isalpha() or i.isdigit() or i == ' '):
						ans += i
				#print type(i.isalpha()), " ", i, " ", i.isalpha()
				#print i.isalpha(), " ", i, " " , type(i), len(i), " ", type(i[0])  
			 	
			for h in d[j]['detailQuestion']:
				for i in h:
					if (i.isalpha() or i.isdigit() or i == ' '):
						ques += i
			ans += " "
			ques += " "
			#print ques 
			#print ans
			#iprint type(ques)
			pairQAs.append((ques, ans))

convertDatabase()
global vnWords
def loadVnWord():
	global vnWords
	vnWords = []
	with open('Viet11K.txt') as words:
		#vnWords.append(words)
		for line in words:
			vnWords.append(line[:-1])
			#print line
			#print type(line)
			#if (line.find(" ") > -1):
			#	vnWords.append(line[:-1])
loadVnWord()
def checkSubString(a, b):
	if (b.find(a) > -1):
		return True
	return False
	# if (a.find(b) > -1):
	# 	return -1 # b la subString cua a
	# if (b.find(a) > -1):
	# 	return 1 #a la subString cua b
	# return 0
def getKey(item):
	return item[0]
def mainProcess():
	global vnWords
	"""for i in vnWords:
		for j in pairQAs:
			k = " " + i + " "
			number = j[0].count(k) + j[1].count(k)
			if (number > 0):
				print "<----> tr count ",i , " ", number, " ", j[0], " < + > ", j[1]
	"""
	
	lengthWords = []
	lengthQAs = []
	f = open("word020518.txt", "w") 
	for i in pairQAs:
		leng =  i[0].count(" ")  + i[1].count(" ") -  2
		leng = max(leng, 0)
		lengthQAs.append(leng)

	# for i in range(0, 100):
	# 	f.write("Question Number: %s" % i + "\n")
	# 	f.write("\tQuestion: " + pairQAs[i][0] + "\n")
	# 	f.write("\tAnswer: " + pairQAs[i][1] + "\n")
	# 	f.write("\tNumber Words: %s" % lengthQAs[i] + "\n")
	# 	#print "Question Number: ", i
		#print "\tQuestion: ", pairQAs[i][0]
		#print "\tAnswer: ", pairQAs[i][1]
		#print "\tNumber Words: ", lengthQAs[i]
	for i in vnWords:
		leng =  i.count(" ") - 1
		leng = max(leng, 0)
		lengthWords.append(leng)

	sizePop = 20
	cnt = 0
	index = 0
	for j in pairQAs:
		pq = []
		for i in vnWords:
			k = " " + i + " "
			number = j[0].count(k) + j[1].count(k)
			if (number > 0):
				#print "<----> tr count ",i , " ", number, " ", j[0], " < + > ", j[1]
				len1 = (i.count(" ") + 1) * number
				heappush(pq, (len1, i))
				if (len(pq) > sizePop):
					heappop(pq)
		#print "Question Number: ", cnt
		f.write("Question Number: %s" % index + "\n")
		f.write("\tQuestion: " + pairQAs[index][0] + "\n")
		f.write("\tAnswer: " + pairQAs[index][1] + "\n")
		f.write("\tNumber Words: %s" % lengthQAs[index] + "\n")
		#print len(pq)
		f.write("Phase 01:\n")
		topWord = []
		while pq:
			i = heappop(pq)
			topWord.append(i)
		#f.write("\t Length: " + str(len(topWord)))
		for i in range(len(topWord) - 1, -1, -1):
			top = topWord[i]
			#print top[0], top[1]
			#f.write(top[1] + " " + str(top[0]) + "\n")
			#len1 = (top[1].count(" ") + 1 )
			#len2 = len1 * top[0]
			pro = (100.0 * top[0]) / lengthQAs[index]
			#print len1, " ", lengthQAs[index], " ", pro
			#f.write("\t" + str(top[1]) + " : " + str(len1 + 1) + " " + str(top[0]) + "\n")
			f.write("\t" + "Word: " + top[1] + "\t\tNumber Word: " + str(top[0])  + "\t\tPercentage: " + "%.02f" % (pro) + "%\n") 
		f.write("Phase 02: Remove SubString\n")
		
		valueTopFirst = []
		for top in topWord:
			valueTopFirst.append(top[0])
		for i in range(0, len(topWord)):
			top1 = topWord[i]
			for j in range(0, len(topWord)):
				top2 = topWord[j]
				#print top1, top2, (top1 != top2)
				if (top1 != top2):
					checkValue = checkSubString(top1[1], top2[1]) #top1[1] la xau con cua top2[1]
					if (checkValue == True):
						valueTopFirst[i] -= valueTopFirst[j] / (top2[1].count(" ") + 1)
						#print top1[0], " ", top2[0], type(top1[0]), type(top2[0])
		for i in range(0, len(topWord)):
			heappush(pq, (valueTopFirst[i], topWord[i][1]))
		topWord = []
		while pq:
			i = heappop(pq)
			topWord.append(i)
		#f.write("\t Length: " + str(len(topWord)))
		for i in range(len(topWord) - 1, -1, -1):
			top = topWord[i]
			#print top[0], top[1]
			#f.write(top[1] + " " + str(top[0]) + "\n")
			#len1 = (top[1].count(" ") + 1 )
			#len2 = len1 * top[0]
			pro = (100.0 * top[0]) / lengthQAs[index]
			#print len1, " ", lengthQAs[index], " ", pro
			#f.write("\t" + str(top[1]) + " : " + str(len1 + 1) + " " + str(top[0]) + "\n")
			f.write("\t" + "Word: " + top[1] + "\t\tNumber Word: " + str(top[0])  + "\t\tPercentage: " + "%.02f" % (pro) + "%\n") 
		
		# for i in range(0, len(topWord)):
		# 	#if (valueTopFirst[i] >= 0):
		# 	top = (valueTopFirst[i], topWord[i][1])
		# 	#print top[0], top[1]
		# 	pro = (1.0 * top[0]) / lengthQAs[index]
		# 	#print len1, " ", lengthQAs[index], " ", pro
		# 	#f.write("\t" + str(top[1]) + " : " + str(len1 + 1) + " " + str(top[0]) + "\n")
		# 	f.write("\t" + "Word: " + top[1] + "\tNumber Word: " + str(top[0]) + "\tProbability: " + "%.10f" % (pro) + "\n")
			
		index += 1
		# while pq:
		# 	top = heappop(pq)
		# 	#print type(top), " ", type(top[0]), " ", type(top[1])
			# len1 = (top[1].count(" ") + 1 ) * top[0]
			# pro = 1.0 * len1 / lengthQAs[index]
			# #print len1, " ", lengthQAs[index], " ", pro
			# #f.write("\t" + str(top[1]) + " : " + str(len1 + 1) + " " + str(top[0]) + "\n")
			# f.write("\t" + top[1] + ": " + str(len1) + " " + "%.10f" % (1.0 * len1 / lengthQAs[index]) + "\n")

mainProcess()
#print checkSubString("thuc rthi", "phap luat")
