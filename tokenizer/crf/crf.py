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

CONFIG = {'single':{'c1':0.1093, 'c2':0.0018}, 'code':{'c1':0.17152979310101085,'c2':0.0033942419604758856}, 'text':{'c1':0.25, 'c2':0.22}}
# default configuration
#CONFIG = {'single':{'c1':0.1, 'c2':0.1}, 'code':{'c1':0.1,'c2':0.1}, 'text':{'c1':0.1, 'c2':0.1}}
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

def list2xy(tlist, x, y):
    for p in tlist:
        if(p.ptype == 'post'):
            x.extend(p.ptitle)
            y.extend(p.ptitle_label)
        x.extend(p.pbody)
        y.extend(p.pbody_label)

def list2D(tlist, D):
    for p in tlist:
        if(p.ptype == 'post'):
            assert len(p.ptitle) == len(p.ptitle_label) == len(p.ptitle_block_type)
            for title, label, btype in zip(p.ptitle, p.ptitle_label, p.ptitle_block_type):
                if(btype == 'c'):
                    D['x_code'].append(title)
                    D['y_code'].append(label)
                else:
                    D['x_text'].append(title)
                    D['y_text'].append(label)
        assert len(p.pbody) == len(p.pbody_label) == len(p.pbody_block_type)
        for title, label, btype in zip(p.pbody, p.pbody_label, p.pbody_block_type):
            if(btype == 'c'):
                D['x_code'].append(title)
                D['y_code'].append(label)
            else:
                D['x_text'].append(title)
                D['y_text'].append(label)

def hyperParameter_search_dual():
    with open('../../Training/posts_annotated.txt') as f:
        post_list = split_train_text(f.read())
    with open('../../Training/answers_annotated.txt') as f:
        post_list.extend(split_train_text(f.read()))
    shuffle(post_list)
    Train = {'x_code':[],'y_code':[],'x_text':[],'y_text':[]}
    list2D(post_list, Train)
    print("Code crf hyper parameter search: ")
    __hyperParameter_search(Train['x_code'], Train['y_code'])
    print("Text crf hyper parameter search: ")
    __hyperParameter_search(Train['x_text'], Train['y_text'])

def hyperParameter_search():
    with open('../../Training/posts_annotated.txt') as f:
        post_list = split_train_text(f.read())
    with open('../../Training/answers_annotated.txt') as f:
        post_list.extend(split_train_text(f.read()))
    shuffle(post_list)
    x_train, y_train = [], []
    list2xy(post_list, x_train, y_train)
    __hyperParameter_search(x_train, y_train)

def __hyperParameter_search(x_train, y_train):
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
    f1_scorer = make_scorer(evaluate_nested_score[2])
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
    input("enter key to continue")

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

def predictTofile_dual(filepath, post_list, crf_text, crf_code):
    with open(filepath, 'w') as f:
        file_text = StringBuilder()
        text_tag = ['<t>','</t>']
        code_tag = ['<c>','</c>']
        for post in post_list:
            file_text.Append(post.pid+"|")
            if(post.ptype == 'post'):
                for title_block, btype in zip(post.ptitle, post.ptitle_block_type):
                    if(btype == 'c'):
                        file_text.Append('<code>' + crfTokens2Anno(title_block, crf_code.predict([title_block])[0], code_tag)+'</code>')
                    else:
                        file_text.Append(crfTokens2Anno(title_block, crf_text.predict([title_block])[0]))
                file_text.Append('|')
            file_text.Append('"')
            for body_block, btype in zip(post.pbody, post.pbody_block_type):
                if(btype == 'c'):
                    file_text.Append('<code>' + crfTokens2Anno(body_block, crf_code.predict([body_block])[0], code_tag)+'</code>')
                else:
                    file_text.Append(crfTokens2Anno(body_block, crf_text.predict([body_block])[0]))
            file_text.Append('"\n')
        f.write(file_text.__str__())

def sample_output_dual(filename, val_ratio=0.2):
    with open('../../Training/posts_annotated.txt') as f:
        post_list = split_train_text(f.read())
    with open('../../Training/answers_annotated.txt') as f:
        post_list.extend(split_train_text(f.read()))
    #shuffle(post_list)
    val_length = int(val_ratio*len(post_list))
    staart = 0
    ennd = val_length - 1
    train_list = post_list[:staart] + post_list[ennd:]
    val_list = post_list[staart:ennd]
    Train = {'x_code':[],'y_code':[],'x_text':[],'y_text':[]}
    Val = {'x_code':[],'y_code':[],'x_text':[],'y_text':[]}
    list2D(train_list, Train)
    list2D(val_list, Val)
    # build model
    crf_code = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=CONFIG['code']['c1'],
        c2=CONFIG['code']['c2'],
        max_iterations=100,
        all_possible_transitions=True
    )
    crf_text = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=CONFIG['text']['c1'],
        c2=CONFIG['text']['c2'],
        max_iterations=100,
        all_possible_transitions=True
    )
    # train model
    crf_code.fit(Train['x_code'], Train['y_code'])
    crf_text.fit(Train['x_text'], Train['y_text'])
    y_pred_code = crf_code.predict(Val['x_code'])
    y_pred_text = crf_text.predict(Val['x_text'])
    evaluate_nested(y_pred_code, Val['y_code'])
    evaluate_nested(y_pred_text, Val['y_text'])
    predictTofile_dual(filename, val_list, crf_text, crf_code)

def sample_output(filename, val_ratio=0.2):
    with open('../../Training/posts_annotated.txt') as f:
        post_list = split_train_text(f.read())
    with open('../../Training/answers_annotated.txt') as f:
        post_list.extend(split_train_text(f.read()))
    #shuffle(post_list)
    val_length = int(val_ratio*len(post_list))
    staart = 0
    ennd = val_length
    train_list = post_list[:staart] + post_list[ennd:]
    val_list = post_list[staart:ennd]
    x_train, y_train = [], []
    x_val, y_val = [], []
    list2xy(train_list, x_train, y_train)
    list2xy(val_list, x_val, y_val)
    # build model
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=CONFIG['single']['c1'],
        c2=CONFIG['single']['c2'],
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

def cross_validation_dual(val_ratio=0.2):
    with open('../../Training/posts_annotated.txt') as f:
        post_list = split_train_text(f.read())
    with open('../../Training/answers_annotated.txt') as f:
        post_list.extend(split_train_text(f.read()))
    shuffle(post_list)
    val_length = int(val_ratio*len(post_list))
    staart = 0
    ennd = val_length - 1
    cross_round = 1
    score_all = []
    while(ennd <= len(post_list)):
        train_list = post_list[:staart] + post_list[ennd:]
        val_list = post_list[staart:ennd]
        Train = {'x_code':[],'y_code':[],'x_text':[],'y_text':[]}
        Val = {'x_code':[],'y_code':[],'x_text':[],'y_text':[]}
        list2D(train_list, Train)
        list2D(val_list, Val)
        # build model
        crf_code = sklearn_crfsuite.CRF(
            algorithm='lbfgs',
            c1=CONFIG['code']['c1'],
            c2=CONFIG['code']['c2'],
            max_iterations=100,
            all_possible_transitions=True
        )
        crf_text = sklearn_crfsuite.CRF(
            algorithm='lbfgs',
            c1=CONFIG['text']['c1'],
            c2=CONFIG['text']['c2'],
            max_iterations=100,
            all_possible_transitions=True
        )
        # train model
        crf_code.fit(Train['x_code'], Train['y_code'])
        crf_text.fit(Train['x_text'], Train['y_text'])
        y_pred_code = crf_code.predict(Val['x_code'])
        y_pred_text = crf_text.predict(Val['x_text'])
        print("Cross validation round ", cross_round, " :")
        print("Code:")
        evaluate_nested(y_pred_code, Val['y_code'])
        print("Text:")
        evaluate_nested(y_pred_text, Val['y_text'])
        print("Dual:")
        score_all.append(evaluate_nested_dual(y_pred_text, Val['y_text'], y_pred_code, Val['y_code']))
        staart += val_length
        ennd += val_length
        cross_round += 1
    print("average precision of CRF tokenization in {}-fold corss validation: {:0.4}".format(int(1/val_ratio), sum([score[0] for score in score_all])/len(score_all)))
    print("average recall of CRF tokenization in {}-fold corss validation:    {:0.4}".format(int(1/val_ratio), sum([score[1] for score in score_all])/len(score_all)))
    print("average f1 score of CRF tokenization in {}-fold corss validation:  {:0.4}".format(int(1/val_ratio), sum([score[2] for score in score_all])/len(score_all)))

def cross_validation(val_ratio=0.2):
    with open('../../Training/posts_annotated.txt') as f:
        post_list = split_train_text(f.read())
    with open('../../Training/answers_annotated.txt') as f:
        post_list.extend(split_train_text(f.read()))
    shuffle(post_list)
    val_length = int(val_ratio*len(post_list))
    staart = 0
    ennd = val_length
    cross_round = 1
    score_all = []
    #pdb.set_trace()
    while(ennd <= len(post_list)):
        train_list = post_list[:staart] + post_list[ennd:]
        val_list = post_list[staart:ennd]
        x_train, y_train = [], []
        x_val, y_val = [], []
        list2xy(train_list, x_train, y_train)
        list2xy(val_list, x_val, y_val)
        # build model
        crf = sklearn_crfsuite.CRF(
            algorithm='lbfgs',
            c1=CONFIG['single']['c1'],
            c2=CONFIG['single']['c2'],
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
        score_all.append(evaluate_nested_score(y_pred, y_val))
        staart += val_length
        ennd += val_length
        cross_round += 1
    print("average precision of CRF tokenization in {}-fold corss validation: {:0.4}".format(int(1/val_ratio), sum([score[0] for score in score_all])/len(score_all)))
    print("average recall of CRF tokenization in {}-fold corss validation:    {:0.4}".format(int(1/val_ratio), sum([score[1] for score in score_all])/len(score_all)))
    print("average f1 score of CRF tokenization in {}-fold corss validation:  {:0.4}".format(int(1/val_ratio), sum([score[2] for score in score_all])/len(score_all)))

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", dest="filename",
                  default='val_predict.txt',
                  help="(default val_predict.txt) write sample output to FILENAME, if mode is sample")
    parser.add_option("-m",
                  dest="mode", default='sample_dual',
                  help="(default sample_dual) change mode: cv/cv_dual/sample/sample_dual/hyper_search/hyper_search_dual")
    parser.add_option("-r",
                  dest="ratio", default=0.2,
                  help="(default 0.2) change validation ratio, default 0.2")
    (options, args) = parser.parse_args()
    if(options.mode == 'sample'):
        sample_output(options.filename, float(options.ratio))
    if(options.mode == 'sample_dual'):
        sample_output_dual(options.filename, float(options.ratio))
    elif(options.mode == 'cv'):
        cross_validation(float(options.ratio))
    elif(options.mode == 'cv_dual'):
        cross_validation_dual(float(options.ratio))
    elif(options.mode == 'hyper_search'):
        hyperParameter_search()
    elif(options.mode == 'hyper_search_dual'):
        hyperParameter_search_dual()