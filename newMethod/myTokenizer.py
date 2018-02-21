#!/usr/bin/env python
# encoding: utf-8

import sys
reload(sys)  
sys.setdefaultencoding('utf8')
import sys, re, math, unicodedata, numpy as np, codecs, pickle
from heapq import heappush, heappop
from collections import OrderedDict

punct = [u'!', u',', u'.', u':', u';', u'?']  # TO DO : Add "..." etc
quotes = [u'"', u"'"]
brackets = [u'(', u')', u'[', u']', u'{', u'}']
mathsyms = [u'%', u'*', u'+', u'-', u'/', u'=', u'>', u'<']

class item:
	def __init__(self, word, cnt, percentage):
		self.word = word
		self.cnt = cnt
		self.percentage = percentage

	def word(self):
		return self.word
	def cnt(self):
		return self.cnt
	def percentage(self):
		return self.percentage

class MyTokenizer:
	def __init__(self, text):
		self.text = text
	
	def reformat(self):
		#print "SELF TEXT: ", self.text
		#mainText = unicode(self.text, "utf-8")
		mainText = self.text
		sents_ = []
		#print "Type mainText: ", type(mainText)
		sents = []
		sents.append(mainText.split())
		#print "SPLIT: ", mainText.split()
		for sent in sents:
			sent_ = []
			for word in sent:
				# First, check if acronym or abbreviation, i.e. Z., Y.Z., X.Y.Z. etc.
				if re.search('(.\.)+\Z', word) and word.isupper(): 
					sent_.append(word) # Checked.
					continue 
				# Second, check if it is a date.
				# DD.MM.YY.
				if re.search('\A[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{2}\.\Z', word):
					sent_.append(word) # Checked.
					continue
				# DD.MM.YYYY.
				if re.search('\A[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{4}\.\Z', word):
					sent_.append(word) # Checked.
					continue
				# If not, separate out punctuation mark at end of word.
				for char in punct:
					rm = re.search('\\' + char + '+\Z', word)
					if rm:
						word = re.sub('\\' + char + '+\Z', '', word) + ' ' + char
						break
				sent_.extend(word.split())	
				
			sents_.append(sent_)
		return sents_

	def separatingText(self):

		retWords = []
		output_file_name = './output.txt'
		model_file_name = './model.pkl'
		f = open(model_file_name, 'rb')
		words_ = pickle.load(f) # Words with smoothed log probs.

		# Break word formation when encounter these characters (detached from any word).
		not_words_ = [u'!', u'"',  u'&', u"'", u'(', u')', u'*', u'+', u',', u'-', u'.',
	                      u'/', u':', u';', u'=', u'>', u'?'] # u'%'
		f.close()	
		
		f = codecs.open(output_file_name, mode = 'w', encoding = 'utf-8')
		sents = [] # Tokenized sentences will be written here.
		sents_ = self.reformat()

		for line in sents_:
			sent = []
			word = []

			for syl in line: # Consider each syllable in this line.

				# Check if syl is a punctuation mark or special character.
				if syl in not_words_: 
					if len(word) > 0:
						sent.append(word)#sent.append('[' + ' '.join(word) + ']') # Write current word to sentence surrounded by [].
						word = [] # Flush word.
					sent.append(syl) # Add the punct or special character (NOT as a token).
					continue
				word.append(syl)
				word1 = ' '.join(word) # Form new word by appending current syllable.

				# Check if the word exists in lexicon.
				if word1 in words_: 
					continue # Do not write anything, continue.

				# Check if the word forms the initials of a person name: "X. Y.".
				if 0: # Disabled.
					if re.search('\A(.\. )+.\.\Z', word1) and word1.isupper():
						continue 
				# Check if it is a person name in the form "X. Y. Z. Xyz Abc"
				if 0: # Disabled.
					rm = re.search('\A(.\. )+', word1)
					if rm:
						word1a = re.sub('\A' + rm.group(), '', word1) # Strip initials.
						word1a = word1a.split()
						isName = 1
						for w_ in word1a:
							if w_[0].islower(): # Initial letter.
								isName = 0
								continue
						if isName == 1:
							continue # Then do not write anything now, continue.
				# Check if it is a person name in the form "Xyz Abc Lmn"
				if 0: # Disabled.
					word1a = word1.split()
					isName = 1
					for w_ in word1a:
						if w_[0].islower():
							isName = 0
							continue
					if isName == 1:
						continue
				
				# Otherwise, check if all syllables in current word are unknown, then keep going.
				# Reason: exploit the observation that unknown foreign words are usually clumped together as 				# single words. This improves P by 0.6 %, does not alter R, and improves F-ratio by 0.3 %.
				if 1:
					all_unk = 1
					for syl_ in word:
						if syl_ in words_:
							all_unk = 0
							continue 
					if all_unk:
						continue # i.e. clump together unknown words.

				# Check if it is a single unknown syllable.
				if len(word) == 1: # Keep it -> as it may be a bounded morpheme.
					continue # This test is not required, it is covered by the above test.

				# Check if first syllable is known, second unknown.
				# (Also, the first and second together do not make a valid word.)
				if len(word) == 2:
					sent.append(word[0]) #sent.append('[' + word[0] + ']') # Then add 1st syllable as a word to the sentence.
					word = [word[1]] # Begin new word with 2nd syllable.

				# Check 1-lookahead with overlap ambiguity resolution.
				# Compare log prob(a, b_c) vs. log prob(a_b, c) if a, b_c, a_b, c exists in lexicon.
				# and write (a, b_c) or (a_b, c) accordingly.
				if len(word) > 2:
					word2 = ' '.join(word[:-2]) # (a)
					word3 = ' '.join(word[-2:]) # (b_c)
					word4 = ' '.join(word[:-1]) # (a_b)
					word5 = word[-1] # (c)
					if word3 not in words_ or word2 not in words_:
						sent.append(word4)#sent.append('[' + word4 + ']')
						word = [word[-1]]
					elif word5 in words_ and word4 in words_:
						P1 = words_[word2] + words_[word3] # P(a, b_c)
						P2 = words_[word4] + words_[word5] # P(a_b, c)
						if P1 > P2:
							sent.append(word2)#sent.append('[' + word2 + ']')
							word = word[-2:]
						else:
							sent.append(word4)#sent.append('[' + word4 + ']')
							word = [word[-1]]
					else:
						# syl was an unknown word.
						sent.append(word4)#sent.append('[' + word4 + ']')
						word = [word[-1]]
			# Last sentence.
			if len(word) > 0:
				sent.append(word)#sent.append('[' + ' '.join(word) + ']')
			if len(sent) > 0:
				sents.append(sent)
			#print "Type SENT = ", type(sent)
			for i in sent:
				#print "Type ii = ", type(ii), " ", ii
				if (type(i) == list):
					for j in i:
						retWords.append(j)
				else:
					retWords.append(i)
				
			#f.write(' '.join(sent) + '\n')
		f.close()
		# for i in retWords:
		# 	print i
		return retWords

	def getTopWords(self):
		word = self.separatingText()
		words = []
		dicts = {}
		cntWords = 0
		for i in word:
			#print i[0]
			if (i[0].isalpha() or i[0].isdigit()):
				words.append(i.lower())
				cntWords += 1
		#print "cntWords: ", cntWords
		#words.sort()
		for i in words:
			#print i, " ", dicts.get(i,  0) 
			value = dicts.get(i , 0)
			dicts[i] = value + 1
			#print dicts[i]
			#dicts[i] += 1

		ret = []
		dictsSort = OrderedDict(sorted(dicts.items(), key=lambda x: x[1], reverse = True))
		#print type(dictsSort), " ", len(dictsSort)
		maxWord = 0
		for key, value in dictsSort.items() :
			#print key, " ", value
			per = (100.0 * value) / cntWords
			ret.append(item(key, value, per))
			#print key, " ", value, " ", per
			maxWord += 1
			if (maxWord >= 10):
				break
		#print type(ret)
		return ret

# x = MyTokenizer("Kính gửi: Luật Sư Luật Minh Gia. Thưa Luật sư,Công ty em là công ty cổ phần nhưng các cổ đông sáng lập đều là tổ chức cả (8 cổ đông sáng lập đều là công ty khác) vậy ngay")
# x.getTopWords()