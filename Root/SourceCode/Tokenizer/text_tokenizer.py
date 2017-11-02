import re
import sys
import os
import pdb
from io import StringIO

# Python 3 string is unicode compatible. Python 2 will report error

# text = '''Albert Einstein (14 March 1879 – 18 April 1955) was a German-born theoretical physicist.[5]
# Einstein developed the theory of relativity, one of the two pillars of modern physics (alongside quantum mechanics).[4][6]:274
# Einstein's work is also known for its influence on the philosophy of science.[7][8]
# Einstein is best known by the general public for his mass–energy equivalence formula E = mc2 (which has been dubbed "the world's most famous equation").[9]
# He received the 1921 Nobel Prize in Physics "for his services to theoretical physics, and especially for his discovery of the law of the photoelectric effect",[10] a pivotal step in the evolution of quantum theory.'''
text = '''While I tested this with CPython, its quite likely most/all other Python implementations use an array to store lists internally. So unless they use a sophisticated data structure designed for efficient list re-sizing, they likely have the same performance characteristic.'''


class StringBuilder:
    _file_str = None

    def __init__(self):
        self._file_str = StringIO()

    def Append(self, str):
        self._file_str.write(str)

    def __str__(self):
        return self._file_str.getvalue()


class TextTokenizer:
    _sb = None
    _tokens = None
    _text = None

    def __init__(self, text, answer_flag=False, post_flag=False):
        self._tokens = []
        self._text = text
        self._sb = StringBuilder()
        self.answer_flag = answer_flag
        self.post_flag = post_flag
        self.tokenizer(text)

    def tokenizer(self, text):
        # Split on whitespace
        sentenceList = text.splitlines()
        notSPFlag = False
        # For names and special pronouns
        specialPronounFlag = False
        # Combine equal sign with previous and next words
        equalSignFlag = False
        # Counter for how long the flag is effective
        counter = 0
        # For Money (e.g. 550,5500.00)
        moneyPattern = re.compile(r'[0-9]*\.[0-9]+')
        for sentence in sentenceList:
            tokenList = []
            lastWord = ' '
            wordList = []
            try:
                if (self.post_flag == True):
                    wordList.extend(sentence.split('|')[-2].split())
                    wordList.extend(sentence.split('|')[-1].split())
                else:
                    wordList.extend(sentence.split('|')[-1].split())
            except:
                wordList.extend(sentence.split('|')[-1].split())
            for word in wordList:
                if (word == ''):
                    continue
                if (lastWord == ''):
                    lastWord = ' '
                # if (word=='RESTful'):
                # pdb.set_trace()
                if (not word[-1].isalnum()):
                    notSPFlag = True
                    counter += 1
                if (lastWord[0].isupper() and word[0].isupper() and notSPFlag == False and word != "I"):
                    tokenList = tokenList[:-1]  # Delete last token (ground step to form special pronoun)
                    lastWord = lastWord + ' ' + word  # Form current special pronoun
                    specialPronounFlag = True
                elif (word == '='):
                    notSPFlag = False
                    tokenList = tokenList[:-1]
                    lastWord = lastWord + ' ' + word  # Concatenate previous word with '='
                    equalSignFlag = True
                else:
                    if (counter > 0):
                        counter -= 1
                    else:
                        notSPFlag = False
                    if (specialPronounFlag == True):
                        tokenList.append(lastWord.strip('.,?!:'))  # Append finalized special noun
                        specialPronounFlag = False
                    elif (equalSignFlag == True):
                        tokenList.append(
                            (lastWord + ' ' + word).strip('.,?!:'))  # Append finalized formula (with current word)
                        equalSignFlag = False
                        continue
                    # Handle Ph.D. and case like science.[7][8]
                    if (not moneyPattern.match(word)):
                        if (word.count('.') < 2):
                            word = re.split(r',|\.|\?|:|!', word)  # split on ,.?:!
                    if (type(word) is str):
                        tmp = word
                        word = []
                        word.append(tmp)
                    for elm in word:
                        elm = elm.strip('()\"\':?!')
                        if (elm == ""):
                            lastWord = elm
                            continue
                        tokenList.append(elm)
                        lastWord = elm
            # print(tokenList[:-1])
            if (specialPronounFlag == True or equalSignFlag == True):
                tokenList.append(lastWord)
                specialPronounFlag = False
                equalSignFlag = False
            self._tokens.extend(tokenList)

    def annotate(self):
        assert self._sb.__str__() == '', "_sb already has value!"
        text_anchor = 0
        if (len(self._tokens) == 0):
            return self._text
        try:
            for token in self._tokens:
                try:
                    search = re.compile(re.escape(token)).search(self._text, text_anchor)
                    search_start = search.start()
                    search_end = search.end()
                    if (token.isdigit()):
                        search1 = re.compile('\n[0-9]*' + re.escape(token) + '[0-9]*\|').search(self._text, text_anchor)
                        try:
                            if (search_start >= search1.start() and search_end <= search1.end()):
                                search = re.compile(re.escape(token)).search(self._text, search1.end())
                                search_start = search.start()
                                search_end = search.end()
                        except:
                            pass
                    self._sb.Append(self._text[text_anchor: search_start])
                    self._sb.Append('<t>' + token + '</t>')
                    text_anchor = search_end
                except:
                    continue
            self._sb.Append(self._text[text_anchor:])
        except Exception as e:
            print(e, "code: \n", self._text, "tokens: \n", self._tokens)
            pdb.set_trace()
            raise e
        return self._sb.__str__()


def main(file):
    source = open(file).read()
    code_secs = re.compile("<code>.*?</code>", flags=re.S | re.M).finditer(source)
    sb_file = StringBuilder()
    # iterate all non-codes area, defined by <code> ... </code>
    file_anchor = 0
    # Skip the first line
    anchor_answer = re.compile(re.escape('Id|Body')).search(source, 0)
    anchor_post = re.compile(re.escape('Id|Title|Body')).search(source, 0)
    answer_flag = False
    post_flag = False
    if (anchor_answer != None):
        file_anchor = anchor_answer.end()
        answer_flag = True
    elif (anchor_post != None):
        file_anchor = anchor_post.end()
        post_flag = True
    else:
        file_anchor = 0
    sb_file.Append(source[0:file_anchor])
    # Define text as "not code"
    for code_sec in code_secs:
        code_start = code_sec.start()
        code_end = code_sec.end()
        text = source[file_anchor:code_start]
        tt = TextTokenizer(text, answer_flag=answer_flag, post_flag=post_flag)
        annotated_text = tt.annotate()
        # Add annotated_text
        sb_file.Append(annotated_text)
        # Add code section
        sb_file.Append(source[code_start:code_end])
        file_anchor = code_end
    # For the last part
    text = source[file_anchor:len(source)]
    sb_file.Append(TextTokenizer(text).annotate())
    file_sep = os.path.splitext(file)
    # Create annotated file
    with open(file_sep[0] + "_textAnno" + file_sep[1], 'w') as new_file:
        new_file.write(sb_file.__str__())


if __name__ == "__main__":
    for file in sys.argv[1:]:
        main(file)
