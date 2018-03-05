#!/usr/bin/env python
# -*- coding: utf-8 -*-
# this file is used for testing


import ilawyer_basic as ib
import ilawyer_lib as il
from sklearn import svm

inp_xlsx = 'tableTraining.xlsx'
out_txt = 'test.txt'
law_xlsx = 'law.xlsx'
inp_txt = 'inp.txt'
input_txt = 'input.txt'
out_txt = 'out.txt'
id_article = 5


# gen dictinary
dict, num_words = il.gen_dict_from_xlsx(inp_xlsx, 101, 3)
print "Test file: ", type(dict), len(dict)

# Training
# ib.gen_feature_table_from_xlsx(inp_xlsx, 101, 3, dict)

# gen feature vector from question in file inp_txt
#print ib.gen_input_vector_from_txt(inp_txt, dict)

# get the artilce sample
#ib.print_txt_from_prediction(law_xlsx, 101, 3, 3, out_txt)


# labels = ib.gen_labels_from_xlsx(inp_xlsx, 101, 3)
# for i in labels:
#     print i

X = ib.gen_feature_table_from_xlsx(inp_xlsx, 101, 3, dict)
y = ib.gen_labels_from_xlsx(inp_xlsx, 101, 3)
print y

# Training
clf = svm.SVC(decision_function_shape = 'ovo')
clf.fit(X, y)

dec = clf.predict(X)
print dec

X = []
z = ib.gen_input_vector_from_txt(input_txt, dict)
print "Vector Question: ", z
X.append(z)
dec = clf.predict(X)
print dec

