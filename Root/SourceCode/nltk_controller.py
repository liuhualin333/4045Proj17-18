'''
This is the controller for 3.2 Stemming and POS-tagging and 3.4 Further Analysis.
'''
import sys
sys.path.insert(0, './Stemming_and_POStagging')
sys.path.insert(0, './utilities')
import utilities
import Root.SourceCode.Stemming_and_POStagging.Tokenization_And_Stemming as ts


def doNLTK():
    def doStem():
        print()
        print(">>> It may take a few minutes to finish processing :)")
        stemmed_tkn_list = ts.main("../Data/All_Posts.txt",True)
        unstemmed_tkn_list = ts.main("../Data/All_Posts.txt", False)
        # stemmed_tkn_list=[('>', 93016), ('<', 92745), ("''", 52246), ('p', 23261), ('/p', 23249), (',', 18417), (':', 15211), ('.', 12136), ('pre', 11362), ('/pre', 11357), ('use', 6380), ('i', 5953), (')', 5609), ('python', 5575), ('(', 5390), ('/a', 4050), ('href=', 4050), ('rel=', 3046), ("'s", 2688), ('noreferr', 2606)]
        # unstemmed_tkn_list=[('>', 93016), ('<', 92745), ("''", 52246), ('p', 23252), ('/p', 23249), (',', 18417), (':', 15211), ('.', 12136), ('pre', 11362), ('/pre', 11357), ('I', 5953), (')', 5609), ('(', 5390), ('Python', 4067), ('href=', 4050), ('/a', 4050), ('use', 3081), ('rel=', 3046), ("'s", 2688), ('noreferrer', 2606)]

        print()
        print(">>> Tokenization finished. LHS is the rank of tokens without being stemmed, and RHS is tokens after stemming.")
        print("Unstemmed         Occurance    |   Stemmed             Occurance")
        print("-----------------------------------------------------------------")
        for i in range(20):
            print("   {:10}   ".format(unstemmed_tkn_list[i][0])+"   {:6}   ".format(unstemmed_tkn_list[i][1])+"   |    {:10}   ".format(stemmed_tkn_list[i][0])+"   {:10}   ".format(stemmed_tkn_list[i][1]))

    def doPOSTag():
        from nltk import word_tokenize, pos_tag

        with open("../Data/Pos-Tag-source.txt","r") as infile:
            content = infile.readlines()
            sentenseList = [x.strip('\n') for x in content]
            for sentense in sentenseList:
                tokens = word_tokenize(sentense)
                tagged = pos_tag(tokens)
                print(tagged)

    doStem()
    ipt = input(">>> Do you want to continue with POS-tagging? [y/n]:")
    if ipt=='y':
        doPOSTag()
    return

def doIrregularCheck():
    print("We will first tokenize the dataset using our own tokenizer, ")
    print("followed by selecting 10 existing sentences that contains the irregular tokens.")


    return

if __name__ == "__main__":
    while True:
        print()
        choice = int(input(
            ">>> Please select whether you wish to (1): Perform tokenization using off nltk tokenizer (assignment 3.2); or (2) using our tokenizer (assignment3.4) ? [1/2]:"))
        if choice == 1:  # Perform tokenization using nltk
            doNLTK()
        elif choice == 2:
            doIrregularCheck()
        else:
            break


