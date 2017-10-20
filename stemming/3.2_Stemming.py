# Author : SHI ZIJI
# Use an off-the-shelf tool to stem the tokens.
# Based on the comparison from nltk.org, snowball stemming is preferred over porter stemming for higher accuracy
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.porter import PorterStemmer
from nltk import tokenize
from collections import Counter

# Create an English stemmer insatnce
stemmer = SnowballStemmer("english")
stemmer2= PorterStemmer()

# TODO : Get a list of tokens from dataset and sort in order of occurrence
myfile = open("/Users/StevenShi/PycharmProjects/NTUNLP/posts/answers_training_clean.txt")
inreader = myfile.read().decode('utf8').encode('utf-8')
myfile.close()

tokens = []
for line in inreader:
    tokens = tokens+ tokenize(line)

# tokens = ['caresses', 'sized','sized','sized','flies', 'dies', 'mules', 'denied','died', 'agreed', 'owned', 'flies','humbled', 'sized','meeting', 'stating', 'siezing', 'itemization','sensational', 'traditional', 'reference', 'colonizer','plotted']
sortedTokens =sorted(tokens, key=Counter(tokens).get, reverse=True)

print(tokens)
print(sortedTokens)

# TODO : Stemming the tokens
stemmedTokens = []
porterStemmed = []
for token in tokens:
    stemmedTokens.append(stemmer.stem(token))
    porterStemmed.append(stemmer2.stem(token))

# Compare results
print(stemmedTokens)
print(porterStemmed)


