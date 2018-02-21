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
from mysql.connector import (connection)
import re
import codecs
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

def getKeyWordQuestions(cursor):
	query = "SELECT * FROM keywordquestions"
	cursor.execute(query)
	cnt = 0
	for row in cursor.fetchall():
	    cnt += 1
	    print "cnt = ", cnt, row
	cursor.close()
	cnx.close()
getKeyWordQuestions(cursor)
