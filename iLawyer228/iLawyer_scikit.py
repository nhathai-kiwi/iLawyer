# collection of all functions using scikit

import iLawyer_basic as ib
import sklearn as sk

# from sklearn.neural_network import MLPClassifier
# from sklearn.linear_model import SGDClassifier
# from sklearn.multiclass import OutputCodeClassifier
# from sklearn.multiclass import OneVsOneClassifier
# from sklearn.multiclass import OneVsRestClassifier
# from sklearn.svm import LinearSVC


# training by support vector classification http://scikit-learn.org/stable/tutorial/basic/tutorial.html
def train_by_SVC(X, y):
    clf = sk.svm.SVC(gamma=0.001, C=100.)
    return clf.fit(X, y)


# training by One-Vs-One http://scikit-learn.org/stable/modules/multiclass.html#id1
def train_by_OneVsOneClassifier(X, y):
    clf = OneVsOneClassifier(LinearSVC(random_state=0))
    return clf.fit(X, y)
# DONE


# training by One-Vs-Rest http://scikit-learn.org/stable/modules/multiclass.html
def train_by_OneVsRestClassifier(X, y):
    clf = OneVsRestClassifier(LinearSVC(random_state=0))
    #clf = OneVsRestClassifier(estimator=SVC(random_state=0))
    return clf.fit(X, y)
# DONE


# training by Output-Codes http://scikit-learn.org/stable/modules/multiclass.html
def train_by_OutputCodeClassifier(X, y):
    clf = OutputCodeClassifier(LinearSVC(random_state=0), code_size=2, random_state=0)
    return clf.fit(X, y)
# DONE


# training by stochastic gradient descent classification http://scikit-learn.org/stable/modules/sgd.html#classification
def train_by_SGDClassifier(X, y):
    clf = SGDClassifier(loss="hinge", penalty="l2")
    return clf.fit(X, y)
# DONE


# training by multi-layer perceptron (MLP) algorithm that trains using Backpropagation
# http://scikit-learn.org/stable/modules/neural_networks_supervised.html#classification
def train_by_MLPClassifier(X, y):
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(num_features), random_state=1)
    return clf.fit(X, y)
# DONE


def gen_label_by_training(X, y):
    label_by_training = []
    label_by_training.append(train_by_SVC(X, y).predict(X))
    label_by_training.append(train_by_OneVsOneClassifier(X, y).predict(X))
    label_by_training.append(train_by_OneVsRestClassifier(X, y).predict(X))
    label_by_training.append(train_by_OutputCodeClassifier(X, y).predict(X))
    label_by_training.append(train_by_MLPClassifier(X, y).predict(X))
    print "Label type: ", type(label_by_training), " ", type(label_by_training[0])
    return label_by_training


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