#!/usr/bin/env python
# encoding: utf-8

import sys
reload(sys)  
sys.setdefaultencoding('utf8')
import sys, re, math, unicodedata, numpy as np, codecs, pickle

import myTokenizer as mt

x = mt.MyTokenizer("Kính gửi: Luật Sư Luật Minh Gia. Thưa Luật sư,Công ty em là công ty cổ phần nhưng các cổ đông sáng lập đều là tổ chức cả (8 cổ đông sáng lập đều là công ty khác) vậy ngay")
arr = x.mainFunction()
for i in arr:
	print i