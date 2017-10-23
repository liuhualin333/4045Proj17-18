# Author : SHI ZIJI
# Use an off-the-shelf tool to stem the tokens.
# Based on the comparison from nltk.org, snowball stemming is preferred over porter stemming for higher accuracy
import sys

import re
from io import StringIO

import os
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from collections import Counter

# StringBuilder class, using StringIO() to struct python string fast
class StringBuilder:
     _file_str = None

     def __init__(self):
         self._file_str = StringIO()

     def Append(self, str):
         self._file_str.write(str)

     def __str__(self):
         return self._file_str.getvalue()


def removeDuplicate(ls):
    newList = []
    for elt in ls:
        if elt not in newList:
            newList.append(elt)
    return newList

def Tokenize(text):
    return word_tokenize(text)

def main(file):
    # Create an English stemmer insatnce
    stemmer = SnowballStemmer("english")
    source = open(file).read()
    code_secs = re.compile("<code>.*?</code>", flags=re.S | re.M).finditer(source)
    tokens_file=StringBuilder()
    sortedTokens_file=StringBuilder()
    reducedSortedTokens_file=StringBuilder()
    # file_anchor mark the current position in current file, before which has been processed already
    file_anchor = 0
    sb_file = StringBuilder()
    # Skip the first line
    anchor_answer = re.compile(re.escape('Id|Body')).search(source, 0)
    anchor_post = re.compile(re.escape('Id|Title|Body')).search(source, 0)
    if (anchor_answer != None):
        file_anchor = anchor_answer.end()
    elif (anchor_post != None):
        file_anchor = anchor_post.end()
    else:
        file_anchor = 0
    sb_file.Append(source[0:file_anchor])
    # Define text as "not code"
    for code_sec in code_secs:
        code_start = code_sec.start()
        code_end = code_sec.end()
        text = source[file_anchor:code_start]

        tokenList = Tokenize(text)
        print(tokenList[0])

        # Sort the token list based on occurance
        sortedTokens = sorted(tokenList, key=Counter(tokenList).get, reverse=True)
        print(sortedTokens[0])
        reducedTokens= removeDuplicate(sortedTokens)
        print(reducedTokens[0])

        stemmedTokens = []
        for token in tokenList:
            stemmedTokens.append(stemmer.stem(token))

        # Add to file for output
        tokens_file.Append(tokenList)
        sortedTokens_file.Append(str(sortedTokens))
        reducedSortedTokens_file.Append(reducedTokens)

        file_anchor = code_end

    # Create annotated file
    with open("Tokens.txt", "w+") as t_file:
        t_file.write(tokens_file.__str__())
    with open("SortedTokens.txt","w+") as s_file:
        s_file.write(sortedTokens_file.__str__())
    with open("rSortedTokens.txt", "w+") as rs_file:
        rs_file.write(reducedSortedTokens_file.__str__())

if __name__ == "__main__":
    for file in sys.argv[1:]:
        main(file)