import sklearn_crfsuite
from sklearn_crfsuite import metrics, scorers
import pdb
import os
import sys
from io import BytesIO, StringIO
import re
sys.path.insert(0, '../../utilities')
from utilities import *
sys.path.insert(0, '../../evaluate')
from evaluation import *
from random import shuffle
import matplotlib.pyplot as plt
import scipy.stats
from sklearn.metrics import make_scorer
from sklearn.model_selection import RandomizedSearchCV
from optparse import OptionParser

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

def hyperParameter_search():
    with open('../../Training/posts_annotated.txt') as f:
        post_list = split_train_text(f.read())
    with open('../../Training/answers_annotated.txt') as f:
        post_list.extend(split_train_text(f.read()))
    shuffle(post_list)
    x_train, y_train = [], []
    def list2xy(tlist, x, y):
        for p in tlist:
            if(p.ptype == 'post'):
                x.extend(p.ptitle)
                y.extend(p.ptitle_label)
            x.extend(p.pbody)
            y.extend(p.pbody_label)
    list2xy(post_list, x_train, y_train)
    # build model
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        max_iterations=100,
        all_possible_transitions=True
    )
    params_space = {
        'c1': scipy.stats.expon(scale=0.1),
        'c2': scipy.stats.expon(scale=0.1),
    }
    # use the same metric for evaluation
    f1_scorer = make_scorer(evaluate_nested_score)
    # search
    rs = RandomizedSearchCV(crf, params_space,
                            cv=5,
                            verbose=1,
                            n_jobs=-1,
                            n_iter=100,
                            scoring=f1_scorer)
    rs.fit(x_train, y_train)
    print('best params:', rs.best_params_)
    print('best CV score:', rs.best_score_)
    #pdb.set_trace()
    #print('model size: {:0.2f}M'.format(rs.best_estimator_.size_ / 1000000))
    _x = [s.parameters['c1'] for s in rs.grid_scores_]
    _y = [s.parameters['c2'] for s in rs.grid_scores_]
    _c = [s.mean_validation_score for s in rs.grid_scores_]
    plt.style.use('ggplot')
    fig = plt.figure()
    fig.set_size_inches(12, 12)
    ax = plt.gca()
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_xlabel('C1')
    ax.set_ylabel('C2')
    ax.set_title("Randomized Hyperparameter Search CV Results (min={:0.3}, max={:0.3})".format(
        min(_c), max(_c)
    ))

    ax.scatter(_x, _y, c=_c, s=60, alpha=0.9, edgecolors=[0,0,0])

    print("Dark blue => {:0.4}, dark red => {:0.4}".format(min(_c), max(_c)))
    fig.show()
    input()

def predictTofile(filepath, post_list, crf):
    with open(filepath, 'w') as f:
        file_text = StringBuilder()
        for post in post_list:
            file_text.Append(post.pid+"|")
            if(post.ptype == 'post'):
                for title_block in post.ptitle:
                    file_text.Append(crfTokens2Anno(title_block, crf.predict([title_block])[0]))
                file_text.Append('|')
            file_text.Append('"')
            for body_block in post.pbody:
                file_text.Append(crfTokens2Anno(body_block, crf.predict([body_block])[0]))
            file_text.Append('"\n')
        f.write(file_text.__str__())

def sample_output(filename, val_ratio=0.2):
    with open('../../Training/posts_annotated.txt') as f:
        post_list = split_train_text(f.read())
    with open('../../Training/answers_annotated.txt') as f:
        post_list.extend(split_train_text(f.read()))
    shuffle(post_list)
    val_length = int(val_ratio*len(post_list))
    staart = 0
    ennd = val_length - 1
    train_list = post_list[:staart] + post_list[ennd:]
    val_list = post_list[staart:ennd]
    x_train, y_train = [], []
    x_val, y_val = [], []
    def list2xy(tlist, x, y):
        for p in tlist:
            if(p.ptype == 'post'):
                x.extend(p.ptitle)
                y.extend(p.ptitle_label)
            x.extend(p.pbody)
            y.extend(p.pbody_label)
    list2xy(train_list, x_train, y_train)
    list2xy(val_list, x_val, y_val)
    # build model
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1093,
        c2=0.0018,
        max_iterations=100,
        all_possible_transitions=True
    )
    # train model
    crf.fit(x_train, y_train)

    labels = list(crf.classes_)

    # Remove I label, too many 
    # labels.remove('I')
    # predict model
    y_pred = crf.predict(x_val)
    evaluate_nested(y_pred, y_val)
    # show metrics
    metrics.flat_f1_score(y_val, y_pred,
                          average='weighted', labels=labels)

    sorted_labels = sorted(
        labels,
        key=lambda name: (name[1:], name[0])
    )
    print(metrics.flat_classification_report(
        y_val, y_pred, labels=sorted_labels, digits=3
    ))
    predictTofile(filename, val_list, crf)


def cross_validation(val_ratio=0.2):
    with open('../../Training/posts_annotated.txt') as f:
        post_list = split_train_text(f.read())
    with open('../../Training/answers_annotated.txt') as f:
        post_list.extend(split_train_text(f.read()))
    shuffle(post_list)
    val_length = int(val_ratio*len(post_list))
    staart = 0
    ennd = val_length - 1
    cross_round = 1
    f1_all = []
    #pdb.set_trace()
    while(ennd < len(post_list)):
        train_list = post_list[:staart] + post_list[ennd:]
        val_list = post_list[staart:ennd]
        x_train, y_train = [], []
        x_val, y_val = [], []
        def list2xy(tlist, x, y):
            for p in tlist:
                if(p.ptype == 'post'):
                    x.extend(p.ptitle)
                    y.extend(p.ptitle_label)
                x.extend(p.pbody)
                y.extend(p.pbody_label)
        list2xy(train_list, x_train, y_train)
        list2xy(val_list, x_val, y_val)
        # build model
        crf = sklearn_crfsuite.CRF(
            algorithm='lbfgs',
            c1=0.1093,
            c2=0.0018,
            max_iterations=100,
            all_possible_transitions=True
        )
        # train model
        crf.fit(x_train, y_train)

        labels = list(crf.classes_)

        # Remove I label, too many 
        labels.remove('I')
        # predict model
        y_pred = crf.predict(x_val)
        #print(y_pred)
        #pdb.set_trace()
        print("Cross validation round ", cross_round, " :")
        evaluate_nested(y_pred, y_val)
        f1_all.append(evaluate_nested_score(y_pred, y_val))
        '''
        # show metrics
        metrics.flat_f1_score(y_val, y_pred,
                              average='weighted', labels=labels)

        sorted_labels = sorted(
            labels,
            key=lambda name: (name[1:], name[0])
        )
        print(metrics.flat_classification_report(
            y_val, y_pred, labels=sorted_labels, digits=3
        ))
        '''
        staart += val_length
        ennd += val_length
        cross_round += 1
    print("average f1 score of CRF tokenization in {}-fold corss validation: {:0.4}".format(int(1/val_ratio), sum(f1_all)/len(f1_all)))

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--outfile", dest="filename",
                  default='val_predict.txt',
                  help="write sample output to FILENAME, if mode is sample")
    parser.add_option("-m", "--mode",
                  dest="mode", default='sample',
                  help="change mode: cv/sample/hyper_search")
    parser.add_option("-r", "--ratio",
                  dest="ratio", default=0.2,
                  help="change validation ratio, default 0.2")
    (options, args) = parser.parse_args()
    if(options.mode == 'sample'):
        sample_output(options.filename, options.ratio)
    elif(options.mode == 'cv'):
        cross_validation(options.ratio)
    elif(options.mode == 'hyper_search'):
        hyperParameter_search()