from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP
from io import BytesIO
import nltk
def decistmt(s):
	result = []
    g = tokenize(BytesIO(s.encode('utf-8')).readline)  # tokenize the string
    for toknum, tokval, _, _, _ in g:
        if toknum == NUMBER and '.' in tokval:  # replace NUMBER tokens
            result.extend([
                (NAME, 'Decimal'),
                (OP, '('),
                (STRING, repr(tokval)),
                (OP, ')')
            ])
        else:
            result.append((toknum, tokval))
    #return untokenize(result).decode('utf-8')
    return result

s = open('text_tokenizer.py').read()
tokens = decistmt(s)

