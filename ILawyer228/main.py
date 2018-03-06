# this file contains the whole program and is the only one to run
# the purpose is to build a program that gives suggestion in Law of Enterprises based on user's question
import ilawyer_lib as il
import ilawyer_basic as ib
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.multiclass import OutputCodeClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from openpyxl import Workbook

#########################
# Part 1: training process
# Part 1.1: pre-processing
# training data being stored in a file named "tableTraining.xlsx" with specific format TODO add file descritpion

# generate dictionary
dict_file_name = "tableTrainingv0.xlsx" # currently we use tableTraining.xlsx for generate dictionary
dict_num_rows = 101
dict_num_cols = 3
dict, num_words = il.gen_dict_from_xlsx(dict_file_name, dict_num_cols, dict_num_rows)
input_txt = 'input.txt'
performance_xlsx = 'performance.xlsx'

# search all keywords in tableTraining, reshape in matrix form (X, y)
training_file_name = "tableTraining.xlsx"
num_examples = 100
num_features = 71

X, y = il.gen_feature_table_labels(training_file_name, dict_num_rows, dict_num_cols, dict)


# 1.2: training


# training by support vector classification - http://scikit-learn.org/stable/tutorial/basic/tutorial.html
def training_by_support_vector_classification(X, y):
    clf = SVC(gamma=0.001, C=100.)
    return clf.fit(X, y)
# DONE

# training by One-Vs-One http://scikit-learn.org/stable/modules/multiclass.html#id1
def training_by_OneVsOneClassifier(X, y):
    clf = OneVsOneClassifier(LinearSVC(random_state=0))
    return clf.fit(X, y)
# DONE


# training by One-Vs-Rest http://scikit-learn.org/stable/modules/multiclass.html
def training_by_OneVsRestClassifier(X, y):
    clf = OneVsRestClassifier(LinearSVC(random_state=0))
    #clf = OneVsRestClassifier(estimator=SVC(random_state=0))
    return clf.fit(X, y)
# DONE


# training by Output-Codes http://scikit-learn.org/stable/modules/multiclass.html
def training_by_OutputCodeClassifier(X, y):
    clf = OutputCodeClassifier(LinearSVC(random_state=0), code_size=2, random_state=0)
    return clf.fit(X, y)
# DONE


# training by stochastic gradient descent classification - http://scikit-learn.org/stable/modules/sgd.html#classification
def training_by_SGDClassifier(X, y):
    clf = SGDClassifier(loss="hinge", penalty="l2")
    return clf.fit(X, y)
# DONE


# training by multi-layer perceptron (MLP) algorithm that trains using Backpropagation  -  http://scikit-learn.org/stable/modules/neural_networks_supervised.html#classification
def training_by_MLPClassifier(X, y):
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(num_features), random_state=1)
    return clf.fit(X, y)
# DONE

def gen_label_by_training(X, y):
    label_by_training = []
    label_by_training.append(training_by_support_vector_classification(X, y).predict(X))
    label_by_training.append(training_by_OneVsOneClassifier(X, y).predict(X))
    label_by_training.append(training_by_OneVsRestClassifier(X, y).predict(X))
    label_by_training.append(training_by_OutputCodeClassifier(X, y).predict(X))
    label_by_training.append(training_by_MLPClassifier(X, y).predict(X))
    print "Label type: ", type(label_by_training), " ", type(label_by_training[0])
    return label_by_training
    # print training_by_support_vector_classification(X, y).predict(X)
    # print training_by_OneVsOneClassifier(X, y).predict(X)
    # print training_by_OneVsRestClassifier(X, y).predict(X)
    # print training_by_OutputCodeClassifier(X, y).predict(X)
    # #print training_by_SGDClassifier(X, y).predict(X)
    # print training_by_MLPClassifier(X, y).predict(X)

def print_xlsx_performance(X, y):
    questions = ib.gen_questions_from_xlsx(training_file_name, dict_num_rows, dict_num_cols)
    labels = y
    labels_by_training = gen_label_by_training(X, y)

    book = Workbook()
    sheet = book.active

    sheet.append(("STT", "Question", "Label", "SVC", "OvOC", "OvRC", "OCC", "MLPC"))

    number_question = 0
    for i in range(0, len(questions)):
        number_question += 1
        question = questions[i]
        label = labels[i]
        label_svc = labels_by_training[0][i]
        label_ovoc = labels_by_training[1][i]
        label_ovrc = labels_by_training[2][i]
        label_occ = labels_by_training[3][i]
        label_mlpc = labels_by_training[4][i]
        row = (number_question, question, label, label_svc, label_ovoc, label_ovrc, label_occ, label_mlpc)
        sheet.append(row)

    book.save(performance_xlsx)
    return 0

print_xlsx_performance(X, y)
# DONE


def cal_model_performance(model):
    return 0



# 1.3: post-processing



#########################
# Part 2: cross evaluation





#########################
# Part 3: validation, prediction


# http://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html
