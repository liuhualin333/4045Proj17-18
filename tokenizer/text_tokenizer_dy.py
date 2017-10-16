import nltk
import sqlite3
import re

text = '''Albert Einstein (14 March 1879 – 18 April 1955) was a German-born theoretical physicist.[5]
Einstein developed the theory of relativity, one of the two pillars of modern physics (alongside quantum mechanics).[4][6]:274 
Einstein's work is also known for its influence on the philosophy of science.[7][8]
Einstein is best known by the general public for his mass–energy equivalence formula E = mc2 (which has been dubbed "the world's most famous equation").[9]
He received the 1921 Nobel Prize in Physics "for his services to theoretical physics, and especially for his discovery of the law of the photoelectric effect",[10] a pivotal step in the evolution of quantum theory.'''


tokens = nltk.word_tokenize(text)
# print(tokens)


def tokenizer(text):
    # Split on whitespace
    wordList = text.split()
    tokenList = []
    lastWord = ' '
    #For names and special pronouns
    specialPronounFlag = False
    #Combine equal sign with previous and next words
    equalSignFlag = False
    #For Money (e.g. 550,5500.00)
    moneyPattern = re.compile(r'[0-9]*\.[0-9]+')
    for word in wordList:
        if (word == ''):
            continue
        if (lastWord == ''):
            lastWord = ' '
        if (lastWord[0].isupper() and word[0].isupper()):
            tokenList = tokenList[:-1]
            lastWord = lastWord + ' ' + word
            specialPronounFlag = True
        elif (word == '='):
            tokenList = tokenList[:-1]
            lastWord = lastWord + ' ' + word
            equalSignFlag = True
        else:
            if (specialPronounFlag == True):
                tokenList.append(lastWord)
                specialPronounFlag = False
            elif (equalSignFlag == True):
                tokenList.append(lastWord + ' ' + word)
            # Handle Ph.D. and case like science.[7][8]
            if (not moneyPattern.match(word)):
                if (word.count('.') < 2):
                    word = re.split(r',|\.', word)#split on ,.
                else:
                    word = word.split(',')
            if (type(word) is str):
                # todo
                # word = word.strip('()')
                if (not equalSignFlag):
                    tokenList.append(word)
                else:
                    equalSignFlag = False
                lastWord = word
                continue
            for elm in word:
                # todo
                # elm = elm.strip('()\"\'')
                if (not equalSignFlag and elm != ''):
                    tokenList.append(elm)
                else:
                    equalSignFlag = False
                lastWord = elm
    # todo
    return tokenList


database = "../posts/2008Posts.db"
conn = sqlite3.connect(database)
cur = conn.cursor()

cur.execute("SELECT body FROM posts")
posts = cur.fetchall()
cur.execute("SELECT body FROM answers")
answers = cur.fetchall()

for answer in answers[:1]:
    text = answer[0]
    print(text)

    # remove code content
    text = re.sub('<code>[\s\S]*?</code>', '', text)
    # remove tags
    text = re.sub('<[^>]*>', '', text)

    print('--------')
    print(text)
    print(tokenizer(text))

