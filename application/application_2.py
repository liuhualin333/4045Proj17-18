"""
    This program aims to find top N keywords in each posts. It takes the following steps:

        1. read
        2. tokenize read data
        3. computer keywords based on tfidf. You may refer to: https://en.wikipedia.org/wiki/Tf%E2%80%93idf

    Usage:
        python application.py file1 ...

"""
import codecs
import re
from collections import Counter
from math import log
import csv
import operator
import sys
import sqlite3


def check_parent_post(ans_id):
    database = "../posts/2008Posts.db"
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT ParentId FROM answers WHERE id=%d"%int(ans_id))
    parent_id = cur.fetchall()[0][0]
    return parent_id


# compute term frequency
def tf(word, doc):
    all_num = sum([doc[key] for key in doc])
    return float(doc[word])/all_num

# compute inverse document frequency
def idf(word, doc_list):
    all_num = len(doc_list)
    word_count = 0
    for doc in doc_list:
        if word in doc:
            word_count += 1
    return log(all_num/word_count)


# product of term frequency and inverse document frequency
def tfidf(word, doc, doc_list):
    word_score = tf(word, doc)*idf(word, doc_list)
    return word_score


def main(post_path="../posts/all_posts_clean_codeAnno_textAnno.txt",
         answer_path="../posts/all_answers_clean_codeAnno_textAnno.txt"):

    # top n keywords
    N = 5

    # score weight for post and answers
    post_weight = 0.8
    answer_weight = 0.2

    # read data
    print("Reading data...")
    post_source = codecs.open(post_path, encoding='UTF-8').read()
    answer_source = codecs.open(answer_path, encoding='UTF-8').read()

    # read stop words
    with open('stop_words.csv', newline='') as f:
        reader = csv.reader(f)
        stop_words = reader.__next__()

    # regular expression to extract code and text token
    re_code = re.compile("<c>(.*?)</c>", flags = re.S|re.M)
    re_text = re.compile("<t>(.*?)</t>", flags = re.S|re.M)

    # regular expression to split each post
    re_post = re.compile('^(\d+)\|(.*?)\n"', flags=re.S | re.M)


    # split posts [(id, post),...]
    post_list = re_post.findall(post_source)
    answer_list = re_post.findall(answer_source)
    # {id:[post, ans1, ans2...]...}
    post_map = {}
    for p in post_list:
        post_map[p[0]] = [p[1]]

    for ans in answer_list:
        ans_id = ans[0]
        ans_parent_id = str(check_parent_post(ans_id))
        post_map[ans_parent_id].append(ans[1])

    # combine all post word count to one, this is to help tfidf [{w1:n1,...}...]
    all_token_count_list = []

    # list to store all posts' token mapping [(id, [{word1:n1, word2:n2,...}...])...]
    post_token_count_list = []

    # count token in each post
    print("Counting tokens...")
    for p_id in post_map.keys():

        token_count_list = []
        for c in post_map[p_id]:
            c_tokens = re_text.findall(c) + re_code.findall(c)
            # remove stop words, digits, one letter and &gt
            c_tokens = [i for i in c_tokens if not
                            (i.lower() in stop_words or i.isdigit() or
                             len(i) <= 1 or '&' in i or '\n' in i)]
            token_count_list.append(dict(Counter(c_tokens)))
            all_token_count_list.append(dict(Counter(c_tokens)))
        post_token_count_list.append((p_id, token_count_list))


    # dict to store all posts score mapping {id:[(w1:s1),...]...}
    post_score_mapping = {}

    print("Calculating scores...")
    for post_token_count in post_token_count_list[:100]:
        p_id = post_token_count[0]
        post_score_mapping[post_token_count[0]] = {}
        for content in post_token_count[1]:
            is_post = True
            for token in content:
                score = tfidf(token, content, all_token_count_list)
                if token not in post_score_mapping[p_id]:
                    post_score_mapping[p_id][token] = 0
                if is_post:
                    # if this is the question post
                    post_score_mapping[p_id][token] += score*post_weight
                else:
                    # if this is the answer post, split weight based on answer numbers
                    post_score_mapping[p_id][token] += score*answer_weight/(len(post_token_count[1]) - 1)

        # sort dict by scores reversely
        post_score_mapping[p_id] = sorted(post_score_mapping[post_token_count[0]].items(), key=operator.itemgetter(1), reverse=True)

    # remove similar tokens
    print("Remove similar tokens...")
    for p_id in post_score_mapping.keys():
        remove_list = []
        p_token = post_score_mapping[p_id][:10]
        i = 0
        while i < 10:
            j = i
            while j < 10:
                if post_score_mapping[p_id][i][0].lower() in post_score_mapping[p_id][j][0].lower() or \
                                post_score_mapping[p_id][j][0].lower() in post_score_mapping[p_id][i][0].lower():
                    min_index = 0
                    max_index = 0
                    if len(post_score_mapping[p_id][i][0]) <= len(post_score_mapping[p_id][i][0]):
                        min_index = i
                        max_index = j
                    else:
                        min_index = j
                        max_index = i
                    remove_list.append(min_index)
                    post_score_mapping[p_id][max_index] = tuple([post_score_mapping[p_id][max_index][0],
                                                           post_score_mapping[p_id][max_index][1] + post_score_mapping[p_id][min_index][1]])
                j += 1
            i += 1
        for r in remove_list:
            post_score_mapping[p_id].pop(r)

        # 重新排序
        # post_score_mapping[p_id].sort(key=lambda tup: tup[1], reverse=True)

        # store into current folder
    print("Storing files...")
    store_path = './post_top_%d_keywords_bb.txt' % N
    with open(store_path,'w') as f:
        for p_id, score_list in post_score_mapping.items():
            top_n_keywords = [i[0] for i in score_list[:N]]
            f.write(p_id+','+','.join(top_n_keywords)+'\n')

main()
# if __name__ == '__main__':
#     if len(sys.argv) == 1:
#         main()
#     else:
#         for file in sys.argv[1:]:
#             main(file)


