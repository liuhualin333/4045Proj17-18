"""
Author : SHI ZIJI

A class to find all occurance of a list of stems in a corpura.

"""
from nltk import word_tokenize, SnowballStemmer
from collections import defaultdict

class findOriginalWord():
    stemList=["sentens","bad"] # TODO : to be replaced by top 20 most frequent stems
    stemDict=defaultdict(list) # create a disctionary of lists
    stemmer = SnowballStemmer("english")
    text = "This is a testing sentense. And it is a badly bad example sentense too."
    tokenList = word_tokenize(text)

    def findOrigin(self):
        for token in self.tokenList:
            curStem=self.stemmer.stem(token)
            if curStem in self.stemList:
                self.stemDict[curStem].append(token)

finder = findOriginalWord()
finder.findOrigin()
print(finder.stemDict)