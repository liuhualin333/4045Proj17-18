'''
This is the controller for 3.2 Stemming and POS-tagging and 3.4 Further Analysis.
'''
import sys
import sklearn_crfsuite
import os.path

sys.path.insert(0, '../')
sys.path.insert(0, '../Data')
sys.path.insert(0, './Stemming_and_POStagging')
sys.path.insert(0, './utilities')
import utilities
import SourceCode.Stemming_and_POStagging.Tokenization_And_Stemming as ts
import SourceCode.tokenizer as nlp
import SourceCode.Stemming_and_POStagging.Analyser as analyser


def doNLTK():
    def doStem():
        print()
        print(">>> It may take a few minutes to finish processing :)")
        stemmed_tkn_list = ts.main("../Data/all_answers.txt","../Data/all_posts.txt", True)
        unstemmed_tkn_list = ts.main("../Data/all_answers.txt","../Data/all_posts.txt", False)
        # stemmed_tkn_list=[('>', 93016), ('<', 92745), ("''", 52246), ('p', 23261), ('/p', 23249), (',', 18417), (':', 15211), ('.', 12136), ('pre', 11362), ('/pre', 11357), ('use', 6380), ('i', 5953), (')', 5609), ('python', 5575), ('(', 5390), ('/a', 4050), ('href=', 4050), ('rel=', 3046), ("'s", 2688), ('noreferr', 2606)]
        # unstemmed_tkn_list=[('>', 93016), ('<', 92745), ("''", 52246), ('p', 23252), ('/p', 23249), (',', 18417), (':', 15211), ('.', 12136), ('pre', 11362), ('/pre', 11357), ('I', 5953), (')', 5609), ('(', 5390), ('Python', 4067), ('href=', 4050), ('/a', 4050), ('use', 3081), ('rel=', 3046), ("'s", 2688), ('noreferrer', 2606)]

        print()
        print(
            ">>> Tokenization finished. LHS is the rank of tokens without being stemmed, and RHS is tokens after stemming.")
        print("Unstemmed         Occurance    |   Stemmed             Occurance")
        print("-----------------------------------------------------------------")
        for i in range(20):
            print("   {:10}   ".format(unstemmed_tkn_list[i][0]) + "   {:6}   ".format(
                unstemmed_tkn_list[i][1]) + "   |    {:10}   ".format(stemmed_tkn_list[i][0]) + "   {:10}   ".format(
                stemmed_tkn_list[i][1]))

    def doPOSTag():
        from nltk import word_tokenize, pos_tag

        with open("../Data/Pos-Tag-source.txt", "r") as infile:
            content = infile.readlines()
            sentenseList = [x.strip('\n') for x in content]
            for sentense in sentenseList:
                tokens = word_tokenize(sentense)
                tagged = pos_tag(tokens)
                print(tagged)

    doStem()
    ipt = input(">>> Do you want to continue with POS-tagging? [y/n]:")
    if ipt == 'y':
        doPOSTag()
    return


def doIrregularCheck():
    print("We will first tokenize the dataset using our own tokenizer, ")
    print("followed by selecting 10 existing sentences that contains the irregular tokens.")

    def doTokenize():
        #nlp.regex2File("../Data/all_posts_clean.txt")
        #print("Question tokenization finished.")
        #nlp.regex2File("../Data/all_answers_clean.txt")
        #print("Answers tokenization finished.")
        myTokens = analyser.Analyser("../Data/all_posts_clean_predicted.txt",
                                     "../Data/all_answers_clean_predicted.txt")
        tops = int(input("How many tokens do you want to see? [Suggested number : 50 ]"))
        myTokens.doRanking(top=tops)

    def doPOStag():
        data = [
            [('&', 'CC'), ('gt', 'NN'), (';', ':'), ('&', 'CC'), ('gt', 'NN'), (';', ':'), ('&', 'CC'), ('gt', 'NN'),
             (';', ':'), ('l', 'CC'), ('=', 'JJ'), ('list', 'NN'), ('(', '('), ('1', 'CD'), (',', ','), ('2', 'CD'),
             (',', ','), ('3', 'CD'), (')', ')')],
            [('def', 'NN'), ('uniq', 'NN'), ('(', '('), ('input', 'NN'), (')', ')'), (':', ':')],
            [('if', 'IN'), ('value', 'NN'), ('==', 'NNP'), ('None', 'NNP'), ('and', 'CC'), ('conditionMet', 'NN'),
             (':', ':')],
            [('Just', 'RB'), ('as', 'IN'), ('a', 'DT'), ('side', 'NN'), ('note', 'NN'), ('how', 'WRB'), ('would', 'MD'),
             ('the', 'DT'), ('implementation', 'NN'), ('change', 'NN'), ('if', 'IN'), ('there', 'EX'), ('is', 'VBZ'),
             ('a', 'DT'), ('dependency', 'NN'), ('between', 'IN'), ('foo', 'NN'), ('and', 'CC'), ('bar', 'NN'),
             ('.', '.')],
            [('I', 'PRP'), ('am', 'VBP'), ('hoping', 'VBG'), ('it', 'PRP'), ('is', 'VBZ'), ('possible', 'JJ'),
             ('to', 'TO'), ('do', 'VB'), ('without', 'IN'), ('tinkering', 'VBG'), ('with', 'IN'), ('sys.path', 'NN'),
             ('.', '.')],
            [('I', 'PRP'), ('have', 'VBP'), ('a', 'DT'), ('script', 'NN'), ('named', 'VBN'), ('test1.py', 'NN'),
             ('which', 'WDT'), ('is', 'VBZ'), ('not', 'RB'), ('in', 'IN'), ('a', 'DT'), ('module', 'NN'), ('.', '.')],
            [('while', 'IN'), ('len', 'VBN'), ('(', '('), ('alist', 'NN'), (')', ')'), ('&', 'CC'), ('gt', 'NN'),
             (';', ':'), ('0', 'CD'), (':', ':'), ('alist.pop', 'NN'), ('(', '('), (')', ')')],
            [('Python', 'NNP'), ('datetime', 'NN'), ('to', 'TO'), ('string', 'VBG'), ('without', 'IN'),
             ('microsecond', 'NN'), ('component', 'NN')],
            [('Actually', 'RB'), (',', ','), ('do', 'VBP'), ("n't", 'RB'), ('show', 'VB'), (',', ','), ('just', 'RB'),
             ('save', 'VB'), ('to', 'TO'), ('foo.png', 'VB')],
            [('plt.plot', 'NN'), ('(', '('), ('x', 'UH'), (',', ','), ('np.sin', 'JJ'), ('(', '('), ('x**2', 'NNP'),
             (')', ')'), (')', ')')]]
        for i in data:
            print(i)

    doTokenize()
    return


if __name__ == "__main__":
    while True:
        print()
        choice = int(input(
            ">>> Please select whether you wish to (1): Perform tokenization using off-the-shelf nltk tokenizer (assignment 3.2); or (2) using our tokenizer (assignment3.4) ? [1/2]:"))
        print()
        if choice == 1:  # Perform tokenization using nltk
            doNLTK()
        elif choice == 2:
            doIrregularCheck()
        else:
            break
