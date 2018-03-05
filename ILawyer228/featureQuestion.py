#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import basicFunction as bf
import runVnCoreNLP as nlp

#list words from keyword.txt file
global keywords

#return vector feature for question: textQuestion
def getFeatureQuestion(words):
    #print "GenFeatureQuestion"
    global keywords
    #print "Len keyWords: ",  len(keywords)

    dicts = {}
    for word in words:
        if (word[0].isdigit() == False):
            value = dicts.get(word, 0)
            dicts[word] = value + 1

    #for key, value in dicts.iteritems():
    #    print key, value, type(key)
    #print "Len keywords: ", len(keywords)

    feature = []
    cnt = 0
    for i in range(0, len(keywords)):
        word = keywords[i]
        word = word[0:len(word) - 1]
        #print "Word ", word, " " , type(word)
        if word in dicts:
            feature.append(1)
            cnt += 1
        else:
            feature.append(0)
    #print "Len feature vector: ", len(feature), " ", cnt
    #print "Feature: X = ", feature
    return feature

#return maxtrix Feature from 100 question in filename (.xlsx)
def getMatrixFeature(fileName, numberOfRows, numberOfCols):
    #init keywords

    global keywords
    keywords = bf.getkeyWord()

    rows = bf.readFileXlsx(fileName, numberOfRows, numberOfCols)
    ret = []
    label = []
    textAllQuestion = ''
    for i in range(1, len(rows)):
        question = rows[i][1]
        y = rows[i][2]
        label.append(y)
        textAllQuestion += " qa " + question

    words = nlp.processString(textAllQuestion)
    lenWords = len(words)
    print "lenWords ", lenWords

    #vector keywords for each question
    vectorWords = []

    #init keywords for each question
    ith = 0
    while (ith < lenWords):
        if (words[ith] == 'qa'):
            jth = ith + 1
            keywordIth = []
            while (jth < lenWords):
                if (jth == lenWords - 1):
                    ith = lenWords
                if (words[jth] == 'qa'):
                    ith = jth
                    break
                keywordIth.append(words[jth])
                jth += 1
            vectorWords.append(keywordIth)

    #get vector feature for each question
    matrixFeature = []
    for i in vectorWords:
        feature = getFeatureQuestion(i)
        matrixFeature.append(feature)

    #write matrix feature into file
    f = open("feature100Question.txt", 'w')
    for i in range(0, len(matrixFeature)):
        #print label[i], " ", matrixFeature[i]
        f.write('Label: ' + str( int (label[i]) ) + '\n\tFeature: ' + str( matrixFeature[i] ) )
    f.close()

    return matrixFeature

if __name__ == '__main__':
    print "genFeatureQuestion"
    getMatrixFeature('tableTraining.xlsx', 101, 3)