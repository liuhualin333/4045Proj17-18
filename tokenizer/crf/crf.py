import sklearn_crfsuite
from sklearn_crfsuite import metrics
import pdb

def word2features(sentence, i):
    word = sentence[i][0]
    token = sentence[i][1]

    features = {
        'bias': 1.0,
        'lower': word.lower(),
        'isUpper': word.isupper(),
        'isTitle': word.istitle(),
        'isDigit': word.isdigit(),
        'token': token,
    }

    if i > 0:
        word1 = sentence[i-1][0]
        token1 = sentence[i-1][1]
        features.update({
            'preLower': word1.lower(),
            'preIsUpper': word1.isupper(),
            'preIsTitle': word1.istitle(),
            'preIsDigit':word1.isdigit(),
            'preToken': token1
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
            'nextToken': token1
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


def main():
    # read data
    train_sentence = [[('I','U'),('love','U'),('New','B'),('York.','E')],[('Bei','B'),('Jing','E'),('is','U'),('far','U')]]
    test_sentence = [[('This','U'),('is','U'),('Shang','B'),('Hai','E'),('city.','U')]]

    x_train = [sentence2features(s) for s in train_sentence]
    y_train = [sentence2tokens(s) for s in train_sentence]

    x_test = [sentence2features(s) for s in test_sentence]
    y_test = [sentence2tokens(s) for s in test_sentence]
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