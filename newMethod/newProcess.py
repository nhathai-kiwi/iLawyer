#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#as3:/usr/local/lib/python2.7/site-packages# cat sitecustomize.py
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
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
	'database': 'iLawyerV18_02',
 }

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

DB_NAME = 'iLawyerV18_02'

TABLES = {}
# TABLES['questions'] = (
# 	"CREATE TABLE `questions` ("
# 	"  `id` int(11) NOT NULL AUTO_INCREMENT,"
# 	"  `content` TEXT NOT NULL,"
# 	"  `url` TEXT NOT NULL,"
# 	"  PRIMARY KEY (`id`)"
# 	") ENGINE=InnoDB")

# TABLES['answers'] = (
# 	"CREATE TABLE `answers` ("
# 	"  `id` int(11) NOT NULL AUTO_INCREMENT,"
# 	"  `content` TEXT NOT NULL,"
# 	"  PRIMARY KEY (`id`)"
# 	") ENGINE=InnoDB")

TABLES['keyWordQuestions'] = (
    "CREATE TABLE `keywordquestions` ("
    "  `id_question` int(11) NOT NULL,"
    "  `keyword` varchar(22) NOT NULL,"
    "  `percentage` double NOT NULL,"
    "  PRIMARY KEY (`id_question`,`keyword`),"
    "  FOREIGN KEY (`id_question`) REFERENCES `questions` (`id`)"
    ") ENGINE=InnoDB")

TABLES['keyWordAnswers'] = (
    "CREATE TABLE `keywordanswers` ("
    "  `id_answer` int(11) NOT NULL,"
    "  `keyword` varchar(22) NOT NULL,"
    "  `percentage` double NOT NULL,"
    "  PRIMARY KEY (`id_answer`,`keyword`),"
    "  FOREIGN KEY (`id_answer`) REFERENCES `answers` (`id`)"
    ") ENGINE=InnoDB")

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)
	cursor.close()
    cnx.close()

def create_table(cursor):
	for name, ddl in TABLES.iteritems():
		print name
		print ddl
		try:
			print("Creating table {}: ".format(name))
			cursor.execute(ddl)
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
				print("already exists.")
			else:
				print(err.msg)
		else:
			print("OK")
	cursor.close()
	cnx.close()
#create_table(cursor)

def addslashes(s):
    l = ["\\", '"', "'", "\0", ]
    for i in l:
        if i in s:
            s = s.replace(i, '\\'+i)
    return s

def pushDataQAs():
	with open('lmgiaData.json') as json_data:
		d = json.load(json_data)
		data = d['item']
		print len(data)
		for qa in data:
			query = "INSERT INTO questions(content, url) VALUES ('%s', '%s')" % (addslashes(qa['question']), qa['url'])
			cursor.execute(query)
			query = "INSERT INTO answers(content) VALUES ('%s')" % addslashes(qa['answer'])
			cursor.execute(query)
	cnx.commit()
	cursor.close()
	cnx.close()
#pushDataQAs()
