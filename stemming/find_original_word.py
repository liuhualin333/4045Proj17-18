"""
Author : SHI ZIJI

A class to find all occurance of a list of stems in a corpura.

Usage : python3 find_original_word.py PostAndAnswer


"""
from nltk import word_tokenize, SnowballStemmer
import sys
from collections import defaultdict

class findOriginalWord:
    def __init__(self,*args):
        self.file = args[0]
        self.text = open(self.file).read()
        self.stemList = args[1]


    # create a dictionary of lists
    stemDict = defaultdict(list)

    def findOrigin(self):
        stemmer = SnowballStemmer("english")
        tokenList = word_tokenize(self.text)
        for token in tokenList:
            # Get the current token and stem it
            curStem=stemmer.stem(token)
            # if current token's stemmed version can be found in stemlist
            if curStem in self.stemList and token not in self.stemDict[curStem]:
                self.stemDict[curStem].append(token)

if __name__ == "__main__":
    file=sys.argv[1]
    stemList=['use', 'i', 'python', 'list', 'function', 'file', 'like', 'string', 'want', 'work', 'code', 'you', 'way', 'exampl', 'method', 'object', 'one', 'instal', 'need', 'get']

    finder = findOriginalWord(file,stemList)
    finder.findOrigin()
    print(finder.stemDict)