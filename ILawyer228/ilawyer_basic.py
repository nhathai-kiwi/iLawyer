#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ilawyer basic functions
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import openpyxl
import os
dict
# delete file has a name inp_fileName
def process_delete_file(inp_fileName):
    cmd = "rm -rf " + inp_fileName
    os.system(cmd)
    return 0
# DONE


# generate questions (string array) from xlsx file
# by default questions are stored in 2nd column from the second row
def gen_questions_from_xlsx(inp_xlsx, num_rows, num_cols):
    questions = []
    # ADD YOUR CODE HERE. when done, please add # DONE after return line
    book = openpyxl.load_workbook(inp_xlsx)
    sheet = book.active
    for row in range(2, num_rows + 1): # ignore 1st row which is preserved for column title
        question = sheet.cell(row=row, column=2).value # store all questions in column 2
        questions.append(question)
    return questions
# DONE


# by default articles are stored in 2nd colums from the second row
# get article has id = answer_number --> return index( row = answer_number + 1, colums = 2)
def print_txt_from_prediction(inp_xlsx, num_rows, num_cols, answer_number, out_txt):
    # get article: answer_number from inp_xlsx file
    book = openpyxl.load_workbook(inp_xlsx)
    sheet = book.active
    article = sheet.cell(row = answer_number + 1, column = 2).value

    # write article to txt file
    f = open(out_txt, "w")
    f.write(article)
    f.close()
    return 0
# DONE


# print array to txt file, each element in a line
def print_txt_from_array(string_array, out_txt):
    # ADD YOUR CODE HERE
    f = open(out_txt, "w")
    for each_string in string_array:
        f.write(str(each_string) + "\n")
    f.close()
    return 0
# DONE


# process vncore
# input: file name of a txt file
# output: TODO add description here
def process_vncore(inp_txt, out_txt):
    # ADD YOUR CODE HERE
    cmd = "java -Xmx2g -jar VnCoreNLP-1.0.jar -fin " + inp_txt + " -fout " + out_txt
    os.system(cmd)
    return 0
# DONE


# generate string array from txt file
def gen_array_from_txt(inp_txt):
    string_array = []
    f = open(inp_txt, 'r')
    for each_string in f:
        string_array.append(each_string)
    f.close()
    return string_array
# DONE


# remove identical element from an array
def gen_distinct_array(inp_arr):
    out_arr = []
    # ADD YOUR CODE HERE
    dicts = {}
    for element in inp_arr:
        value = dicts.get(element, 0)
        dicts[element] = value + 1
    for key, value in dicts.iteritems():
        out_arr.append(key)
    return out_arr
# DONE


# generate words (string array) from output of vncore
# TODO add details about what we need to do with vncore output format
# eg: delete words that appear more than once or start with number, etc
def gen_words_from_vncore_out_txt(vn_core_out_txt):
    words = []
    # ADD YOUR CODE HERE
    lines = gen_array_from_txt(vn_core_out_txt)
    words_replicated = []
    for line in lines:
        texts = line.split(chr(9))
        if len(texts) == 6:
            text = texts[1]
            if not text[0].isdigit(): # ignore all words starting with digit
                word = text.replace('_', ' ').lower() # replace underscore by space, change all characters to lower case
                # TODO find a way to remove all words with single syllable, those have tiny impact on guessing
                # TODO remove text that contains special characters

                words_replicated.append(word)
    # remove all words that appear more than once
    #words = gen_distinct_array(words_replicated)
    return words_replicated


# generate labels (numeric array) from xlsx file
def gen_labels_from_xlsx(inp_xlsx, num_rows):
    labels = []
    # ADD YOUR CODE HERE
    book = openpyxl.load_workbook(inp_xlsx)
    sheet = book.active
    for row in range(2, num_rows + 1): # ignore 1st row which is preserved for column title
        label = sheet.cell(row = row, column = 3).value # store all in column 3
        labels.append(label)
    return labels
# DONE


# generate feature vector (numeric array)
def gen_feature_vector(string_array):
    global dict
    feature_vector = []
    # ADD YOUR CODE HERE
    dictStringArray = {} # remove all the string duplicate in string_array by dictinary - STL python
    for element in string_array:
        value = dictStringArray.get(element, 0)
        dictStringArray[element] = value + 1

    for word in dict:
        #print word, " ", len(word) #check word have a charater ('\n')
        #check word in dict exist in string_array, if it exist then value of feature = 1, else value of feature = 0
        if word in dictStringArray:
            feature_vector.append(1)
        else:
            feature_vector.append(0)
    return feature_vector
# DONE


# generate feature vector (numeric 1D array) from a question
def gen_input_vector_from_txt(inp_txt, dictMain):
    global dict
    dict = dictMain

    print_txt_from_array(inp_txt, 'vncore_inp.txt')
    process_vncore('vncore_inp.txt', 'vncore_out.txt')
    string_array = gen_words_from_vncore_out_txt('vncore_out.txt')

    inp_vector = gen_feature_vector(string_array)

    # TODO delete vncore_inp.txt and vncore_out.txt
    process_delete_file('vncore_inp.txt')
    process_delete_file('vncore_out.txt')

    return inp_vector
# DONE


# generate feature table (numeric 2D array) from a training set stored in xlsx
def gen_feature_table_from_xlsx(inp_xlsx, num_rows, num_cols, dictMain):
    separator = 'separator'
    feature_table = []
    all_questions = gen_questions_from_xlsx(inp_xlsx, num_rows, num_cols)
    global dict
    dict = dictMain

    questions_with_seperator = []
    for question in all_questions:
        # add 'separator' before each question for convenient process
        questions_with_seperator.append(separator)
        questions_with_seperator.append(question)

    print_txt_from_array(questions_with_seperator, 'vncore_inp.txt')
    process_vncore('vncore_inp.txt', 'vncore_out.txt')
    string_array = gen_words_from_vncore_out_txt('vncore_out.txt')

    # seperating question and get it's feature vector
    question = []
    cnt = 0
    for each_string in string_array:
        if each_string == separator:
            if len(question) == 0:
                continue
            feature_vector = gen_feature_vector(question)
            feature_table.append(feature_vector)
            question = []
        else:
            question.append(each_string)

    # add a last feature_vector question
    feature_vector = gen_feature_vector(question)
    feature_table.append(feature_vector)

    # TODO delete vncore_inp.txt and vncore_out.txt
    process_delete_file('vncore_inp.txt')
    process_delete_file('vncore_out.txt')

    return feature_table
# DONE





