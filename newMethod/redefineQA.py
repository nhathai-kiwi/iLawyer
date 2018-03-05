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

def readDataJSON():
	f = open('redefineQA2.txt', "w")

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
			url = qa['url']
			f.write("Question Number: " + str(cnt) + "\n")
			f.write("Question:\n")
			f.write(ques + "\n")
			f.write("Answer:\n")
			f.write(ans + "\n")
			f.write("Url:\n")
			f.write(url + "\n")
			f.write("Article:\n")
readDataJSON()

