'''
Author : SHI ZIJI

Use an off-the-shelf tool to stem the tokens.
Based on the comparison from nltk.org, snowball stemmer , a variant of porter stemmer, is used here for higher accuracy.

Tested input : /post/post_training_clean.txt
Cannot directly apply on xml file.
'''
import sys

import re
from io import StringIO

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

# StringBuilder class, using StringIO() to struct python string fast
class StringBuilder:
     _file_str = None

     def __init__(self):
         self._file_str = StringIO()

     def Append(self, Str):
         self._file_str.write(Str)

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
    source = open(file).read()
    # Escape tokenizing on code section
    code_secs = re.compile("<code>.*?</code>", flags=re.S | re.M).finditer(source)
    tokens_file=StringBuilder()
    sortedTokens_file=StringBuilder()        # sort the tokens
    reducedSortedTokens_file=StringBuilder() # sorted tokens without duplicates
    # file_anchor mark the current position in current file, before which has been processed already
    file_anchor = 0
    # Define text as "not code"
    tokenList=[]

    for code_sec in code_secs:
        code_start = code_sec.start()
        code_end = code_sec.end()
        text = source[file_anchor:code_start]
        tokenList += Tokenize(text)
        file_anchor = code_end

    # Sort the token list based on occurance
    sortedTokens =sorted(tokenList, key=Counter(tokenList).get, reverse=True)
    reducedTokens = removeDuplicate(sortedTokens)

    # Add to file for output
    tokens_file.Append(str(tokenList))
    sortedTokens_file.Append(str(sortedTokens))
    reducedSortedTokens_file.Append(str(reducedTokens))

    # Write to output
    with open("Tokens.txt", "w+") as t_file:
        t_file.write(tokens_file.__str__())
    with open("SortedTokens.txt","w+") as s_file:
        s_file.write(sortedTokens_file.__str__())
    with open("rSortedTokens.txt", "w+") as rs_file:
        rs_file.write(reducedSortedTokens_file.__str__())

if __name__ == "__main__":
    for file in sys.argv[1:]:
        main(file)