#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
import basicFunction as bf
import runVnCoreNLP as nlp

# read data from fileName (type .xlsx)  and gen Dictionary from this file
def getDictionary(fileName, rows, cols):
    bf.writeDataXlxsToTxt(fileName, rows, cols)
    fileDataTxt = fileName.replace('.xlsx', '.txt')
    words = nlp.processFile(fileDataTxt)

    dicts = bf.distinctWords(words)

    #print len(dicts)

    f = open('keyword.txt', 'w')
    ret = []
    for key, value in dicts.iteritems():
        #print key, value
        ret.append(key.lower())

    ret.sort()
    for word in ret:
        f.write(word + '\n')
    return ret

if __name__ == '__main__':
    print "getDictionaryFrom100Question"
    getDictionary('tableTraining.xlsx', 101, 3)
