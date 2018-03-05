#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
import basicFunction as bf
#os.system("java -Xmx2g -jar VnCoreNLP-1.0.jar -fin question.txt -fout output.txt")


#input: fileInput contains text(string)
#output: array contains words after seperating words from text in fileInput
def processFile(fileInput):
	print "ProcessFile from runVNCoreNLP"
	#run terminal command
	#Output fileOutput with special format, example: 2	công_ty	N	O	1	nmod
	# the word we need to return is 2nd elements in format: công_ty

	fileOutput = fileInput.replace('.txt', 'WordInForm.txt')

	cmd = "java -Xmx2g -jar VnCoreNLP-1.0.jar -fin " + fileInput + " -fout "  + fileOutput
	os.system(cmd)

	
	# #read data from fileOuput
	lines = bf.getTextFromFile(fileOutput)
	#print (len(lines))

	# #copy word from fileOuput into words array and return 
	#processing text each element in lines: get 2nd elemnts in each line
	words = []

	for line in lines:
		texts = line.split(chr(9))
		if (len(texts) == 6):
			text = texts[1].replace('_', ' ')
			text = text.lower()
			words.append(text)
	
	#write words into file

	fileOutput = fileOutput.replace('.txt', 'WordList.txt')
	f = open(fileOutput, 'w')
	for word in words:
		f.write(word + "\n")
	f.close()

	return words

def processString(text):
	print "ProcessString from runVNcoreNLP"
	print bf.fileNameForRunVnCore
	f = open(bf.fileNameForRunVnCore, 'w')
	f.write(text)
	f.close()
	return processFile(bf.fileNameForRunVnCore)
