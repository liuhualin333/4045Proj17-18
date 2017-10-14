from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP, tok_name, COMMENT, LPAR, RPAR
from io import BytesIO, StringIO
import nltk
import codecs
import re
import sys, os

s = '''Traceback ('''

tokens = []
#g = tokenize(BytesIO(s.encode('utf-8')).readline)
prev_num = 0
prev_val = None
prev_end = -1
ss = s.splitlines()
for line in ss:
	g = tokenize(BytesIO(line.encode('utf-8')).readline)
	try:
		for toknum, tokval, starrt, eend, _ in g:
			if(toknum in [NAME, COMMENT, STRING, OP, NUMBER] and re.compile(r"^(?<![a-zA-Z])[,)\-\"'\[\]]+(?![a-zA-Z])$").search(tokval) == None):
				if(((prev_num == NAME and tokval == '(') or (prev_val == '&' and (tokval == 'lt' or tokval == 'gt')) ) and prev_end == starrt):
					tokens[-1] = tokens[-1] + tokval
				elif(tokval == '('):
					pass
				else:
					tokens.append(tokval)
			prev_num = toknum
			prev_val = tokval
			prev_end = eend
	except Exception as e:
		#import pdb; pdb.set_trace()
		print("Error in __setTokens__" + str(e), end = '')
		print(line)
		pass
print(tokens)