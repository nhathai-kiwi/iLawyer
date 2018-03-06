#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ilawyer library
import iLawyer_basic as ib


# generate dictionary from xlsx file
# TODO add description for input xlsx
def gen_dict_from_xlsx(inp_xlsx, num_cols, num_rows):
    all_questions = ib.gen_questions_from_xlsx(inp_xlsx, num_cols, num_rows)
    ib.print_txt_from_array(all_questions, out_txt='vncore_inp.txt') # print output to a file, this file will be deleted later
    ib.process_vncore('vncore_inp.txt', 'vncore_out.txt')
    dict_replicated = ib.gen_words_from_vncore_out_txt('vncore_out.txt')
    dict = ib.gen_distinct_array(dict_replicated)
    dict.sort()
    # TODO delete vncore_inp.txt and vncore_out.txt
    ib.process_delete_file('vncore_inp.txt')
    ib.process_delete_file('vncore_out.txt')
    return dict, len(dict)
# DONE

# generate feature table and labels from a training set stored in xlsx
# TODO add description for input xlsx
def gen_feature_table_labels(inp_xlsx, num_cols, num_rows, dict):
    feature_table = ib.gen_feature_table_from_xlsx(inp_xlsx, num_cols, num_rows, dict)
    labels = ib.gen_labels_from_xlsx(inp_xlsx, num_cols, num_rows)
    return feature_table, labels
