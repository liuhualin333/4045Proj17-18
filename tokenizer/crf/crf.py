import sklearn_crfsuite
from sklearn_crfsuite import metrics
import pdb
import os
import sys
from io import BytesIO, StringIO
import re
# StringBuilder class, using StringIO() to struct python string fast
class StringBuilder:
     _file_str = None

     def __init__(self):
         self._file_str = StringIO()

     def Append(self, str):
         self._file_str.write(str)

     def value(self):
         return self._file_str.getvalue()

def get_char_feature(char, index):
    return {
        index+'bias': 1.0,
        index+'lower': char.lower(),
        index+'isUpper': char.isupper(),
        index+'isDigit': char.isdigit(),
        index+'isChar': char.isalpha()
    }

# chars to features
def chars2features(chars):
    # how many chars before/after should be considered in features extraction
    cl = 5
    chars_features = []
    for i in range(len(chars)):
        char_features = {}
        for j in range(-cl,cl+1):
            if(i+j >= 0 and i+j < len(chars)):
                char = chars[i+j]
                char_features.update(get_char_feature(char, str(j)))
        chars_features.append(char_features)
    return chars_features

    

def word2features(sentence, i):
    word = sentence[i][0]
    token = sentence[i][1]

    features = {
        'bias': 1.0,
        'lower': word.lower(),
        'isUpper': word.isupper(),
        'isTitle': word.istitle(),
        'isDigit': word.isdigit(),
    }

    if i > 0:
        word1 = sentence[i-1][0]
        token1 = sentence[i-1][1]
        features.update({
            'preLower': word1.lower(),
            'preIsUpper': word1.isupper(),
            'preIsTitle': word1.istitle(),
            'preIsDigit':word1.isdigit(),
        })
    else:
        features['BOS'] = True

    if i < len(sentence)-1:
        word1 = sentence[i - 1][0]
        token1 = sentence[i - 1][1]
        features.update({
            'nextLower': word1.lower(),
            'nextIsUpper': word1.isupper(),
            'nextIsTitle': word1.istitle(),
            'nextIsDigit': word1.isdigit(),
        })
    else:
        features['EOS'] = True

    return features


def sentence2features(sentence):
    return [word2features(sentence, i) for i in range(len(sentence))]


def sentence2tokens(sentence):
    return [token for word, token in sentence]


def sentence2words(sentence):
    return [word for word, token in sentence]

# annoText, annoTag: [<c>,</c>] or [<t>,</t>],
# return: original_text, original_label
def anno2charsTokens(annoText, annoTag):
    origin_text = StringBuilder()
    origin_label = StringBuilder()
    tokens = re.compile(annoTag[0]+".*?"+annoTag[1], flags=re.S | re.M).finditer(annoText)
    anno_anchor = 0
    def Appendtxtlabel(_txt, _label):
        origin_text.Append(_txt)
        origin_label.Append(_label)
    for token in tokens:
        token_start = token.start() + 3
        token_end = token.end() - 4
        Appendtxtlabel(annoText[anno_anchor:token.start()],'O'*(token.start() - anno_anchor))
        Appendtxtlabel(annoText[token_start],'T')
        if(token_end - token_start >= 3):
                Appendtxtlabel(annoText[token_start+1:token_end-1],'I'*(token_end-token_start-2))
        if(token_end - token_start >= 2):
            Appendtxtlabel(annoText[token_end-1],'E')
        anno_anchor = token.end()
    return origin_text.value(), origin_label.value()



# from mixed annotated text to clean text(remove <c></c> <t></t> tag) and output the corresponding tag
def MixAnno2charsTokens(annoText):
    origin_txt = StringBuilder()
    origin_label = StringBuilder()
    anno_anchor = 0
    code_tag = ['<c>', '</c>']
    text_tag = ['<t>', '</t>']
    code_secs = re.compile("<code>.*?</code>", flags=re.S | re.M).finditer(annoText)
    def Appendtxtlabel(_txt, _label):
        origin_txt.Append(_txt)
        origin_label.Append(_label)
    # iterate all codes area, defined by <code> ... </code>
    for code_sec in code_secs:
        # +6 and -7 to exclude <code> & </code> tags
        code_start = code_sec.start() + 6
        code_end = code_sec.end() - 7
        # Append the origin text, orinal label from anno_anchor to code_start
        Appendtxtlabel(*anno2charsTokens(annoText[anno_anchor : code_sec.start()], text_tag))
        # Init a new CodesTokenizer with codes, append the annotated codes to sb_file
        Appendtxtlabel(*anno2charsTokens(annoText[code_start : code_end], code_tag))
        anno_anchor = code_sec.end()

    Appendtxtlabel(*anno2charsTokens(annoText[anno_anchor : ], text_tag))
    return origin_txt.value(), origin_label.value()

def get_data(filepath):
    X, Y = [], []
    with open(filepath) as f:
        file_text = f.read()
        if(r'Id|Body' in file_text[:15]):
            flag = 'answer'
            file_text = file_text[8:]
            pattern = re.compile(r'^\d+\|\"(.*?)\"(\n(?=\d+\|)|($))', flags = re.S|re.M)
        else:
            flag = 'post'
            file_text = file_text[14:]
            pattern = re.compile(r'^\d+\|([^\n\|]*?)\|\"(\n(?=\d+\|)|($))', flags = re.S|re.M)
        for post in pattern.finditer(file_text):
            _text, _label = MixAnno2charsTokens(post.group(1))
            _x = _text
            _y = _label
            if(flag == 'post'):
                _text, _label = MixAnno2charsTokens(post.group(2))
                _x += _text
                _y += _label
            X.append(_x)
            Y.append(_y)
    Y = [list(str) for str in Y]
    return X, Y

def main():
    # read data
    # rules defined in training data
    '''
    train_sentence = [[('I','U'),('love','U'),('New','B'),('York.','E')],[('Bei','B'),('Jing','E'),('is','U'),('far','U')],[('Machine','B'),('Learning','E'),('tools','U'),('Are','U'),('great.','U')]]
    test_sentence = [[('This','U'),('is','U'),('Shang','B'),('Hai','E'),('city.','U')]]

    x_train_ = [sentence2features(s) for s in train_sentence]
    y_train = [sentence2tokens(s) for s in train_sentence]

    x_test = [sentence2features(s) for s in test_sentence]
    y_test = [sentence2tokens(s) for s in test_sentence]
    #pdb.set_trace()
    '''
    x_train = []
    y_train = []
    x_test = []
    y_test = []
    '''
    try:
        with open('train.txt') as train:
            for line in train:
                if(len(line)==1):
                    continue
                x_train.append(line[0])
                y_train.append(line[2])

        with open('test.txt') as test:
            for line in test:
                if(len(line)==1):
                    continue
                x_test.append(line[0])
                y_test.append(line[2])
    except Exception as e:
        print(e)
        pdb.set_trace()
        pass    
    x_train = [chars2features(x_train)]
    y_train = [y_train]
    x_test = [chars2features(x_test)]
    y_test = [y_test]
    '''

    x_train, y_train = get_data('training.txt')
    x_test, y_test = get_data('testing.txt')
    x_train = [chars2features(block) for block in x_train]
    x_test = [chars2features(block) for block in x_test]

    #pdb.set_trace()


    #pdb.set_trace()
    # build model
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True
    )

    # train model
    crf.fit(x_train, y_train)

    labels = list(crf.classes_)

    # predict model
    y_pred = crf.predict(x_test)
    print(y_pred)

    # show metrics
    metrics.flat_f1_score(y_test, y_pred,
                          average='weighted', labels=labels)

    sorted_labels = sorted(
        labels,
        key=lambda name: (name[1:], name[0])
    )
    print(metrics.flat_classification_report(
        y_test, y_pred, labels=sorted_labels, digits=3
    ))

if __name__ == '__main__':
    main()