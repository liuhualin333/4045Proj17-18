"""
    This program aims to find top N keywords in each posts. It takes the following steps:

        1. read data
        2. tokenize read data
        3. computer keywords based on tfidf. You may refer to: https://en.wikipedia.org/wiki/Tf%E2%80%93idf

    Usage:
        python application.py file1 ...

"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.cluster import KMeans
import codecs
import re
from collections import OrderedDict
from collections import Counter
from math import log
import csv
import operator
import sys


def tf(word,doc):
    all_num = sum([doc[key] for key in doc])
    return float(doc[word])/all_num


def idf(word,doc_list):
    all_num = len(doc_list)
    word_count = 0
    for doc in doc_list:
        if word in doc:
            word_count += 1
    return log(all_num/word_count)


def tfidf(word, doc, doc_list):
    word_score = tf(word, doc)*idf(word, doc_list)
    return word_score


def main(post_path="../posts/posts_training_clean_codeAnno_textAnno.txt"):

    # top n keywords
    N = 3

    # read data
    post_source = codecs.open(post_path, encoding='UTF-8').read()

    # read stop words
    with open('stop_words.csv', newline='') as f:
        reader = csv.reader(f)
        stop_words = reader.__next__()

    # regular expression to extract code and text token
    re_code = re.compile("<c>(.*?)</c>", flags = re.S|re.M)
    re_text = re.compile("<t>(.*?)</t>", flags = re.S|re.M)

    # regular expression to split each post
    re_post = re.compile('(\d+)\|(.*?)\n"', flags = re.S|re.M)

    # find all tokens, used for k means
    # post_tokens = set(re_text.findall(post_source) + re_code.findall(post_source))
    # answer_tokens = set(re_text.findall(answer_source) + re_code.findall(answer_source))
    # all_tokens = list(post_tokens | answer_tokens)
    # all_tokens.sort()
    # token_num = len(all_tokens)

    # list to store all posts' token mapping [(id, {word1:n1, word2:n2,...})...]
    post_token_count_list = []

    # split posts [(id, post),...]
    post_list = re_post.findall(post_source)

    # count token in each post
    for p in post_list:
        p_tokens = re_text.findall(p[1]) + re_code.findall(p[1])
        # remove stop words and digits
        p_tokens = [i for i in p_tokens if not (i.lower() in stop_words or i.isdigit())]
        p_id = p[0]
        post_token_count_list.append((p_id, dict(Counter(p_tokens))))

    # combine all post word count to one, this is to help tfidf
    all_token_count_list = [i[1] for i in post_token_count_list]

    # dict to store all posts score mapping {id:[(w1:s1),...]...}
    post_score_mapping = {}

    for post_token_count in post_token_count_list:
        p_id = post_token_count[0]
        # print("-"*20)
        # print("post %s"%post_token_map[0])
        post_score_mapping[post_token_count[0]] = {}
        for token in post_token_count[1]:
            score = tfidf(token, post_token_count[1], all_token_count_list)
            post_score_mapping[p_id][token] = score

        # reverse sort dict by scores
        post_score_mapping[p_id] = sorted(post_score_mapping[post_token_count[0]].items(), key=operator.itemgetter(1), reverse=True)


    # store into current folder

    store_path = './' + post_path.split('/')[-1].split('.')[0] + '_top_%d_keywords.txt' % N
    with open(store_path,'w') as f:
        for p_id, score_list in post_score_mapping.items():
            top_n_keywords = [i[0] for i in score_list[:N]]
            f.write(p_id+','+','.join(top_n_keywords)+'\n')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    else:
        for file in sys.argv[1:]:
            main(file)


# k means application

# for p in post_list:
#     p_tokens = re_text.findall(p[1]) + re_code.findall(p[1])
#     p_token_map = OrderedDict((ele, 0) for ele in all_tokens)
#     for t in p_tokens:
#         p_token_map[t] += 1
#     post_token_vector_map[p[0]] = p_token_map.values()
# print(type(post_token_vector_map.values()))
#
# post_vectors = []
#
# for vector in post_token_vector_map.values():
#     post_vectors.append([int(x) for x in vector])
#
# post_vectors = np.array(post_vectors)
#
# kmeans = KMeans(n_clusters=5, random_state=0).fit(post_vectors)
#
# index = 0
# for post_id in post_token_vector_map.keys():
#     print(post_id, kmeans.labels_[index])
#     index += 1
#
# print(Counter(kmeans.labels_))

