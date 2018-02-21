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


global vnWords

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

TABLES = {}
# TABLES['vnword11k'] = (
# 	"CREATE TABLE `vnword11k` ("
# 	"  `id` int(11) NOT NULL AUTO_INCREMENT,"
# 	"  `word` varchar(30) NOT NULL,"
# 	"  PRIMARY KEY (`id`)"
# 	") ENGINE=InnoDB")
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

# TABLES['employees'] = (
#     "CREATE TABLE `employees` ("
#     "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
#     "  `birth_date` date NOT NULL,"
#     "  `first_name` varchar(14) NOT NULL,"
#     "  `last_name` varchar(16) NOT NULL,"
#     "  `gender` enum('M','F') NOT NULL,"
#     "  `hire_date` date NOT NULL,"
#     "  PRIMARY KEY (`emp_no`)"
#     ") ENGINE=InnoDB")

# TABLES['departments'] = (
#     "CREATE TABLE `departments` ("
#     "  `dept_no` char(4) NOT NULL,"
#     "  `dept_name` varchar(40) NOT NULL,"
#     "  PRIMARY KEY (`dept_no`), UNIQUE KEY `dept_name` (`dept_name`)"
#     ") ENGINE=InnoDB")
TABLES['keyWordQuestions'] = (
    "CREATE TABLE `keywordquestions` ("
    "  `id_question` int(11) NOT NULL,"
    "  `id_keyword` int(11) NOT NULL,"
    "  `percentage` double NOT NULL,"
    "  PRIMARY KEY (`id_question`,`id_keyword`),"
    "  FOREIGN KEY (`id_question`) REFERENCES `questions` (`id`),"
    "  FOREIGN KEY (`id_keyword`) REFERENCES `vnword11k` (`id`)"
    ") ENGINE=InnoDB")

TABLES['keyWordAnswers'] = (
    "CREATE TABLE `keywordanswers` ("
    "  `id_answer` int(11) NOT NULL,"
    "  `id_keyword` int(11) NOT NULL,"
    "  `percentage` double NOT NULL,"
    "  PRIMARY KEY (`id_answer`,`id_keyword`),"
    "  FOREIGN KEY (`id_answer`) REFERENCES `answers` (`id`),"
    "  FOREIGN KEY (`id_keyword`) REFERENCES `vnword11k` (`id`)"
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
create_table(cursor)



def pushDataVnWord11k(cursor):
	global vnWords
	vnWords = []
	cnt = 0
	with open('Viet11K.txt') as words:
		for line in words:
			lineText = line[:-1]
			#print lineText
			query = "INSERT INTO vnword11k(word) VALUES ('%s')" % lineText
			#print query
			cursor.execute(query)
	#print len(vnWords)
	cnx.commit()
	cursor.close()
	cnx.close()
#pushDataVnWord11k(cursor)

def addslashes(s):
    l = ["\\", '"', "'", "\0", ]
    for i in l:
        if i in s:
            s = s.replace(i, '\\'+i)
    return s

def pushDataQAs(cursor):
	with open('lmgiaData.json') as json_data:
		d = json.load(json_data)
		data = d['item']
		print len(data)
		for qa in data:
			#print qa['url']
			query = "INSERT INTO questions(content, url) VALUES ('%s', '%s')" % (addslashes(qa['question']), qa['url'])
			#print query
			cursor.execute(query)
			query = "INSERT INTO answers(content) VALUES ('%s')" % addslashes(qa['answer'])
			cursor.execute(query)
	cnx.commit()
	cursor.close()
	cnx.close()
#pushDataQAs(cursor)
	
