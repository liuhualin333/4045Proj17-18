'''
Author : SHI ZIJI

Use an off-the-shelf tool to stem the tokens.
Based on the comparison from nltk.org, snowball stemmer , a variant of porter stemmer, is used here for higher accuracy.

Tested input : /Root/Data/All_Posts.txt
'''

import re
from io import StringIO

from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
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

def mostCommon(tknlst,top):
    # Return 20 most common tokens
    obj = Counter(tknlst)
    return obj.most_common(top)

def Tokenize(text):
    return word_tokenize(text)

def main(filepath, stemFlag):
    source = open(filepath).read()
    # Escape tokenizing on code section
    code_secs = re.compile("<code>.*?</code>", flags=re.S | re.M).finditer(source)

    reducedSortedTokens_file=StringBuilder() # sorted tokens without duplicates
    # file_anchor mark the current position in current file, before which has been processed already
    file_anchor = 0
    # Define text as "not code"
    filteredTokenList=[]

    for code_sec in code_secs:
        code_start = code_sec.start()
        code_end = code_sec.end()
        text = source[file_anchor:code_start]
        tokenList = Tokenize(text)
        #remove stop words
        filteredTokenList += [word for word in tokenList if word not in stopwords.words('english')]
        file_anchor = code_end


    if stemFlag:
        # Create an English stemmer insatnce
        print("Stemming tokens using nltk.SnowballStemmer")
        stemmer = SnowballStemmer("english")
        stemmedTokens = []
        for token in filteredTokenList:
            stemmedTokens.append(stemmer.stem(token))
        # return top 20 most common tokens
        sortedTokens = mostCommon(stemmedTokens,20)
    else:
        sortedTokens = mostCommon(filteredTokenList,20)

    return sortedTokens
