from nltk import word_tokenize, pos_tag

with open ("/Users/StevenShi/PycharmProjects/NTUNLP/stemming/processed_result/3.4_POS-tagging_source","r") as infile:
    content=infile.readlines()

    sentenseList = [x.strip('\n') for x in content]

    for sentense in sentenseList:
        tokens = word_tokenize(sentense)
        tagged = pos_tag(tokens)
        print(tagged)
