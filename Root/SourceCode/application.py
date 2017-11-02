"""
    This program aims to find top N keywords in each posts. It takes the following steps:

        1. read data
        2. tokenize read data
        3. remove stop words
        4. computer keywords based on tfidf. You may refer to: https://en.wikipedia.org/wiki/Tf%E2%80%93idf
        5. choose top 3 keywords from text section, and 1 function name from code section.
            if there is no function name in code section, replace it with a token from text section

    Usage:
        python application.py file1 ...

"""
import re
from collections import Counter
from math import log
import operator
import sys
import random

def tf(word, doc):
    all_num = sum([doc[key] for key in doc])
    return float(doc[word])/all_num


def idf(word, doc_list):
    all_num = len(doc_list)
    word_count = 0
    for doc in doc_list:
        if word in doc:
            word_count += 1
    return log(all_num/word_count)


def tfidf(word, doc, doc_list):
    word_score = tf(word, doc)*idf(word, doc_list)
    return word_score


def main(post_path="../Data/all_posts_clean_predicted.txt"):

    # top n keywords
    N = 4

    # read data
    with open(post_path, encoding='UTF-8') as f:
        post_source = f.read()

    # read stop words
    # with open('stop_words.csv', newline='') as f:
    #     reader = csv.reader(f)
    #     stop_words = reader.__next__()
    stop_words = ", ,/,%,:,.,-,__,_,=,==,$,*,**,//,...,[],[,],<<,>>,\n,a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,would,yet,you,your,you're".split(',')


    # regular expression to extract code and text token
    re_code = re.compile("<c>(.*?)</c>", flags = re.S|re.M)
    re_text = re.compile("<t>(.*?)</t>", flags = re.S|re.M)

    # regular expression to split each post
    re_post = re.compile('(\d+)\|(.*?)\n"', flags = re.S|re.M)

    # list to store all posts' token mapping [(id, {word1:n1, word2:n2,...})...]
    post_token_count_list = []

    # split posts [(id, post),...]
    post_list = re_post.findall(post_source)

    # count token in each post
    for p in post_list:
        # todo
        # p_tokens = re_text.findall(p[1]) + re_code.findall(p[1])
        p_tokens = re_text.findall(p[1])
        p_tokens += [i for i in re_code.findall(p[1]) if re.match(".*?\(", i)]
        # remove stop words, digits, one letter and &gt
        p_tokens = [i for i in p_tokens if not (i.lower() in stop_words or i.isdigit() or
                                                len(i) <= 1 or '&' in i or '\n' in i or
                                                re.match('\d+?\.\d+?', i) is not None)]
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

    # remove similar keywords
    for post_id in post_score_mapping:
        word_list = post_score_mapping[post_id]
        # store keyword's index to be deleted
        remove_list = []
        index_i = 0
        while index_i < len(word_list) - 1:
            index_j = index_i + 1
            while index_j < len(word_list):
                # used to store index of shorter and longer tokens
                min_index = 0
                max_index = 0
                token_i = word_list[index_i][0].lower()
                token_j = word_list[index_j][0].lower()
                if token_i in token_j or token_j in token_i:
                    if len(token_i) <= len(token_j):
                        min_index = index_i
                        max_index = index_j
                    else:
                        min_index = index_j
                        max_index = index_i
                    remove_list.append(min_index)
                    # add the shorter tokens score to longer tokens score
                    word_list[max_index] += tuple([word_list[max_index][0],
                                                   word_list[max_index][1] + word_list[min_index][1]])
                index_j += 1
            index_i += 1

        # don't add tokens into new word list if it is in remove list
        new_word_list = list()
        index = 0
        for w in word_list:
            if index not in remove_list:
                new_word_list.append(w)
            index += 1

        # reorder by new score
        new_word_list.sort(key=lambda tup: tup[1], reverse=True)
        post_score_mapping[post_id] = new_word_list

    # store into current folder

    rand_ten_list = []
    store_path = './' + post_path.split('/')[-1].split('.')[0] + '_top_%d_keywords.txt' % N
    with open(store_path, 'w') as f:
        for p_id, score_list in post_score_mapping.items():
            try:
                top_n_keywords = [i[0] for i in score_list if '(' not in i[0]]
                top_n_keywords = top_n_keywords[:N]
                for i in score_list:
                    if '(' in i[0]:
                        top_n_keywords[-1] = i[0]
                        break
                f.write(p_id+','+','.join(top_n_keywords)+'\n')
                rand_ten_list.append(p_id+': '+', '.join(top_n_keywords))
            except UnicodeEncodeError:
                continue

    random.shuffle(rand_ten_list)
    print("Top 4 keywords in question posts:")
    for x in rand_ten_list[:10]:
        print("     Question post", x)

    print("     ......")
    print("Top 4 keywords for all posts have been stored in\n", store_path)



if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    else:
        for file in sys.argv[1:]:
            main(file)


