from nltk import word_tokenize, pos_tag

with open ("","r") as infile:

    tokens = word_tokenize(sentence)
    tagged = pos_tag(tokens)
