"""

    This program aims to find the precision, recall and f1 value of regular expression tokenizer.

    Usage: python evaluate.py truth_file predict_file

"""
import sys
import codecs
import re
from collections import Counter
import pdb

def evaluate(truth, predict):
    true_positive = 0
    for token in predict:
        if token not in truth:
            continue
        else:
            true_positive += min(predict[token], truth[token])
    false_positive = sum(predict.values()) - true_positive
    false_negative = sum(truth.values()) - true_positive
    return true_positive / (true_positive+false_positive), true_positive / (true_positive + false_negative)

def eval(truth_source, predict_source):
    # regular expression to extract code and text token
    re_code = re.compile("<c>(.*?)</c>", flags = re.S|re.M)
    re_text = re.compile("<t>(.*?)</t>", flags = re.S|re.M)

    # regular expression to split each post
    re_post = re.compile('(\d+)\|(.*?)\n"', flags = re.S|re.M)

    # find all tokens in train and test
    predict_tokens = re_text.findall(predict_source) + re_code.findall(predict_source)
    truth_tokens = re_text.findall(truth_source) + re_code.findall(truth_source)

    # count token
    predict_tokens_count = Counter(predict_tokens)
    truth_tokens_count = Counter(truth_tokens)

    # compute precision
    precision, recall = evaluate(truth_tokens_count, predict_tokens_count)
    f1 = 2 * recall * precision / (recall + precision)
    print('Precision: ', precision)
    print('Recall:    ', recall)
    print('F1 score:  ', f1)

def main(truth_path="../Training/posts_annotated.txt", predict_path='../posts/posts_training_clean_Annotated.txt'):

    truth_source = codecs.open(truth_path, encoding='UTF-8').read()
    predict_source = codecs.open(predict_path, encoding='UTF-8').read()


    # regular expression to extract code and text token
    re_code = re.compile("<c>(.*?)</c>", flags = re.S|re.M)
    re_text = re.compile("<t>(.*?)</t>", flags = re.S|re.M)

    # regular expression to split each post
    re_post = re.compile('(\d+)\|(.*?)\n"', flags = re.S|re.M)

    # find all tokens in train and test
    predict_tokens = re_text.findall(predict_source) + re_code.findall(predict_source)
    truth_tokens = re_text.findall(truth_source) + re_code.findall(truth_source)

    # print(len(train_tokens))
    # print(len(test_tokens))

    # count token
    predict_tokens_count = Counter(predict_tokens)
    truth_tokens_count = Counter(truth_tokens)

    # compute precision
    precision, recall = evaluate(truth_tokens_count, predict_tokens_count)
    f1 = 2 * recall * precision / (recall + precision)
    print('Precision: ', precision)
    print('Recall:    ', recall)
    print('F1 score:  ', f1)


    # train_post_list = re_post.findall(train_source)
    # test_post_list = re_post.findall(test_source)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    else:
        test = sys.argv[1]
        train = sys.argv[2]
        main(test, train)