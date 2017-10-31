import sklearn_crfsuite
from sklearn_crfsuite import metrics
import pdb
import os
import sys
from io import BytesIO, StringIO
import re
sys.path.insert(0, '../../utilities')
from utilities import *

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

    

def word2features(sentence, i):
    word = sentence[i][0]
    token = sentence[i][1]

    features = {
        'bias': 1.0,
        'lower': word.lower(),
        'isUpper': word.isupper(),
        'isTitle': word.istitle(),
        'isDigit': word.isdigit(),
    }

    if i > 0:
        word1 = sentence[i-1][0]
        token1 = sentence[i-1][1]
        features.update({
            'preLower': word1.lower(),
            'preIsUpper': word1.isupper(),
            'preIsTitle': word1.istitle(),
            'preIsDigit':word1.isdigit(),
        })
    else:
        features['BOS'] = True

    if i < len(sentence)-1:
        word1 = sentence[i - 1][0]
        token1 = sentence[i - 1][1]
        features.update({
            'nextLower': word1.lower(),
            'nextIsUpper': word1.isupper(),
            'nextIsTitle': word1.istitle(),
            'nextIsDigit': word1.isdigit(),
        })
    else:
        features['EOS'] = True

    return features


def sentence2features(sentence):
    return [word2features(sentence, i) for i in range(len(sentence))]


def sentence2tokens(sentence):
    return [token for word, token in sentence]


def sentence2words(sentence):
    return [word for word, token in sentence]


def main():
    # read data
    # rules defined in training data
    '''
    train_sentence = [[('I','U'),('love','U'),('New','B'),('York.','E')],[('Bei','B'),('Jing','E'),('is','U'),('far','U')],[('Machine','B'),('Learning','E'),('tools','U'),('Are','U'),('great.','U')]]
    test_sentence = [[('This','U'),('is','U'),('Shang','B'),('Hai','E'),('city.','U')]]

    x_train_ = [sentence2features(s) for s in train_sentence]
    y_train = [sentence2tokens(s) for s in train_sentence]

    x_test = [sentence2features(s) for s in test_sentence]
    y_test = [sentence2tokens(s) for s in test_sentence]
    #pdb.set_trace()
    '''
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
    x_test, y_test = get_data('../../posts/posts_training_clean_codeAnno_textAnno.txt')
    x_train, y_train = get_data("../../Training/posts_annotated.txt")
    #x_train = [chars2features(block) for block in x_train]
    #x_test = [chars2features(block) for block in x_test]

    pdb.set_trace()

    metrics.flat_f1_score(y_train, y_test,
                          average='weighted', labels=labels)

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
    print(y_pred)

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

if __name__ == '__main__':
    main()