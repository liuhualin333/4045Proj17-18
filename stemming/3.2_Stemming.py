# Author : SHI ZIJI
# Use an off-the-shelf tool to stem the tokens.
# Based on the comparison from nltk.org, snowball stemming is preferred over porter stemming for higher accuracy
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from collections import Counter

def removeDuplicate(ls):
    newList = []
    for elt in ls:
        if elt not in newList:
            newList.append(elt)
    return newList

# Create an English stemmer insatnce
stemmer = SnowballStemmer("english")

myfile = open("/Users/StevenShi/PycharmProjects/NTUNLP/posts/answers_training_clean.txt", encoding="utf-8")
# Attention here : inreader is a single string
inreader = myfile.read()
tokens = word_tokenize(inreader)
# tokens = ['caresses', 'sized','sized','sized','flies', 'dies', 'mules', 'denied','died', 'agreed', 'owned', 'flies','humbled', 'sized','meeting', 'stating', 'siezing', 'itemization','sensational', 'traditional', 'reference', 'colonizer','plotted']

sortedTokens =sorted(tokens, key=Counter(tokens).get, reverse=True)

print(tokens)
print(removeDuplicate(sortedTokens))

# TODO : Stemming the tokens
stemmedTokens = []

for token in tokens:
    stemmedTokens.append(stemmer.stem(token))

# Compare results
print(stemmedTokens)


myfile.close()