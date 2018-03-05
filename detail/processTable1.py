#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
import json
import pprint
import re
import codecs
from openpyxl import Workbook

def processText():
	data = ''
	lines = []
	cnt = 0
	with open('vbpl.txt', 'r') as myfile:
		for line in myfile:
			#lines.append(line)
			if (line[0] == '$'):
				line += '#'
				#print line
			lines.append(line)
		#data = myfile.read().replace('\n', ' ')
	for i in lines:
		data += i#.replace('\n', ' ')
	#print len(lines)
	# print data
	articles = data.split('$$$$')
	print len(articles)
	#print articles[1]
	book = Workbook()
	sheet = book.active
	sheet.append(("STT", "Nội dung"))
	number = 0
	for i in range(1, 214):
		number += 1
		content = articles[i].split('#')
		#print len(content)
		#for j in content:
		#	print j
		#print len(content)
		mainContent = content[0].split('. ')
		#print len(mainContent)
		#for j in mainContent:
		# 	print j
		row = (number, content[1])
		sheet.append(row)
		#rows = rows, ("Luật doanh nghiệp 2014", mainContent[0], mainContent[1], content[1])
	#print type(rows), type(rows[0]), len(rows)
	#print rows[1]

		
	# for row in rows:
	# 	sheet.append(row)
	book.save('law.xlsx')
processText()
