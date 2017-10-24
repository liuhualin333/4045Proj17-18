from nltk import word_tokenize, pos_tag

with open ("./POS-tagging_source.txt","r") as infile:
    content=infile.readlines()

    sentenseList = [x.strip('\n') for x in content]

    for sentense in sentenseList:
        tokens = word_tokenize(sentense)
        tagged = pos_tag(tokens)
        print(tagged)