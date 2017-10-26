from itertools import chain

import nltk
import sklearn
import scipy.stats
from sklearn.metrics import make_scorer
from sklearn.cross_validation import cross_val_score
from sklearn.grid_search import RandomizedSearchCV

import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics

import numpy as np


def word2features(input, i):
    word = input[i][0]
    token = input[i][1]

    features = {
        'bias': 1.0,
        'lower': word.lower(),
        'isUpper': word.isupper(),
        'isTitle': word.istitle(),
        'isDigit': word.isdigit(),
        'token': token,
    }

    if i > 0:
        word1 = input[i-1][0]
        token1 = input[i-1][1]
        features.update({
            'preLower': word1.lower(),
            'preIsUpper': word1.isupper(),
            'preIsTitle': word1.istitle(),
            'preIsDigit':word1.isdigit(),
            'preToken': token1
        })
    else:
        features['BOS'] = True

    if i < len(input)-1:
        word1 = input[i - 1][0]
        token1 = input[i - 1][1]
        features.update({
            'nextLower': word1.lower(),
            'nextIsUpper': word1.isupper(),
            'nextIsTitle': word1.istitle(),
            'nextIsDigit': word1.isdigit(),
            'nextToken': token1
        })
    else:
        features['EOS'] = True

    return features


def input2features(input):
    return [word2features(input, i) for i in range(len(input))]


def input2tokens(input):
    return [token for word, token in input]


def input2words(input):
    return [word for word, token in input]


train_input = [[('I','U'),('love','U'),('New','B'),('York.','E')],[('Bei','B'),('Jing','E'),('is','U'),('far','U')]]
test_input = [[('This','U'),('is','U'),('Shang','B'),('Hai','E'),('city.','U')]]

x_train = [input2features(s) for s in train_input]
y_train = [input2tokens(s) for s in train_input]

x_test = [input2features(s) for s in test_input]
y_test = [input2tokens(s) for s in test_input]


crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True
)

crf.fit(x_train, y_train)

labels = list(crf.classes_)

y_pred = crf.predict(x_test)
print(y_pred)
metrics.flat_f1_score(y_test, y_pred,
                      average='weighted', labels=labels)

sorted_labels = sorted(
    labels,
    key=lambda name: (name[1:], name[0])
)
print(metrics.flat_classification_report(
    y_test, y_pred, labels=sorted_labels, digits=3
))