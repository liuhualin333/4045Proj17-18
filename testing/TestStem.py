from nltk import SnowballStemmer

stemmer = SnowballStemmer("english")
filteredTokenList=['use', "''", 'Calling', 'function', 'module', 'string', 'function', "'s", 'name', "''", '|', "''", 'What', 'best', 'way', 'go', 'calling', 'function', 'given', 'string', 'function', "'s", 'name', 'Python', 'program', '.', 'For', 'example', ',', 'let', "'s", 'say', 'I', 'module', ',', 'I', 'string', 'whose', 'contents', '.', 'What', 'best', 'way', 'go', 'calling', '?', 'I', 'need', 'get', 'return', 'value', 'function', ',', 'I', "n't", 'use']
lst=[]
for token in filteredTokenList:
    print(stemmer.stem(token))
    lst.append(stemmer.stem(token))
print(lst)