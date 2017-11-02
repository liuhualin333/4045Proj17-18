'''
Author  : SHI ZIJI

This code is used for tokenize the dataset and identify the top 20 most frequently used words that are not standard English word, with other morphological origin.

Usage : python3 3.4_Analysis.py

'''

import re
from collections import Counter

source = open('../posts/all_answers_clean_Annotated.csv', encoding='utf-8').read().lower()
questions = open('../posts/all_posts_clean_Annotated.csv', encoding='utf-8').read().lower()

# Define regex that will match the content of both text token or code token
text_regex = "<t>(.+?)<\/t>"
code_regex = "<c>(.+?)<\/c>"
text_tokens_ans = re.findall(text_regex, source)
code_tokens_ans = re.findall(code_regex,source)
text_tokens_qus = re.findall(text_regex, questions)
code_tokens_qus = re.findall(code_regex,questions)

text_result_ans = Counter(text_tokens_ans)
code_result_ans = Counter(code_tokens_ans)
text_result_qus = Counter(text_tokens_qus)
code_result_qus = Counter(code_tokens_qus)

# Join all counter objects
jointA = text_result_ans | code_result_ans
jointQ =  text_result_qus| code_result_qus
joint = jointA | jointQ

for i in joint.most_common(150):
    print(i)



