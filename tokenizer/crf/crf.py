import sklearn_crfsuite
from sklearn_crfsuite import metrics
import pdb
import os
import sys
from io import BytesIO, StringIO
import re
sys.path.insert(0, '../../utilities')
from utilities import *
sys.path.insert(0, '../../evaluate')
from evaluation import *

def get_char_feature(char, index):
    return {
        index+'bias': 1.0,
        index+'lower': char.lower(),
        index+'isUpper': char.isupper(),
        index+'isDigit': char.isdigit(),
        index+'isChar': char.isalpha()
    }

# chars to features
def chars2features(chars):
    # how many chars before/after should be considered in features extraction
    cl = 5
    chars_features = []
    for i in range(len(chars)):
        char_features = {}
        for j in range(-cl,cl+1):
            if(i+j >= 0 and i+j < len(chars)):
                char = chars[i+j]
                char_features.update(get_char_feature(char, str(j)))
        chars_features.append(char_features)
    return chars_features

def main():
    # read data
    x_train = []
    y_train = []
    x_test = []
    y_test = []
    '''
    try:
        with open('train.txt') as train:
            for line in train:
                if(len(line)==1):
                    continue
                x_train.append(line[0])
                y_train.append(line[2])

        with open('test.txt') as test:
            for line in test:
                if(len(line)==1):
                    continue
                x_test.append(line[0])
                y_test.append(line[2])
    except Exception as e:
        print(e)
        pdb.set_trace()
        pass    
    x_train = [chars2features(x_train)]
    y_train = [y_train]
    x_test = [chars2features(x_test)]
    y_test = [y_test]
    '''
    x_train, y_train = get_data("training.txt")
    x_test, y_test = get_data('testing.txt') 
    #x_train = [chars2features(block) for block in x_train]
    #x_test = [chars2features(block) for block in x_test]

    #pdb.set_trace()
    # build model
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True
    )

    # train model
    crf.fit(x_train, y_train)

    labels = list(crf.classes_)

    # predict model
    y_pred = crf.predict(x_test)
    #print(y_pred)
    #pdb.set_trace()
    evaluate_nested(y_pred, y_test)
    # show metrics
    metrics.flat_f1_score(y_test, y_pred,
                          average='weighted', labels=labels)

    sorted_labels = sorted(
        labels,
        key=lambda name: (name[1:], name[0])
    )
    print(metrics.flat_classification_report(
        y_test, y_pred, labels=sorted_labels, digits=3
    ))
    with open('output.txt','w') as f:
        f.write(crfFile2File(crf, 'testing_clean.txt'))
    return crf

if __name__ == '__main__':
    main()