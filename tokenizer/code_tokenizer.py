'''
	This module converts tokenize the code sections defined by <code> ... </code> in the anwsers/posts.
	Code Token Definition: literals with only [] / {} / ' / " / , are not tokens
							XXX( is token denoting function/method call
							.	is token for special meaning
							Use normal word token for COMMENT / STRING (TODO: still use code tokenizer)
	Usage:
		python code_tokenizer.py file1.txt ...
		(This will output file1_annotated.txt)
'''

from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP, tok_name, COMMENT, LPAR, RPAR
from io import BytesIO, StringIO
import nltk
import codecs
import re
import sys, os
from text_tokenizer import tokenizer
class StringBuilder:
     _file_str = None

     def __init__(self):
         self._file_str = StringIO()

     def Append(self, str):
         self._file_str.write(str)

     def __str__(self):
         return self._file_str.getvalue()

class CodesTokenizer:
	_sb = None
	_tokens = None
	_codes = None
	def __init__(self, codes):
		self._tokens = []
		self._codes = codes
		self._sb = StringBuilder()
		self.__setTokens__()

	def __setTokens__(self):
		#g = tokenize(BytesIO(self._codes.encode('utf-8')).readline)  # tokenize the string
		prev_num = -1
		prev_val = None
		prev_end = -1
		ss = self._codes.splitlines()
		for line in ss:
			g = tokenize(BytesIO(line.encode('utf-8')).readline)  # tokenize the string
			try:
				for toknum, tokval, starrt, eend, _ in g:
					if(toknum in [NAME, OP, NUMBER] and re.compile(r"^(?<![a-zA-Z])[,)\-\"';\[\]|..+]+(?![a-zA-Z])$").search(tokval) == None):
						if(((prev_num == NAME and tokval == '(') or (prev_val == '&' and (tokval == 'lt' or tokval == 'gt')) ) and prev_end == starrt):
							self._tokens[-1] = self._tokens[-1] + tokval
						elif(tokval == '('):
							pass
						else:
							self._tokens.append(tokval)
					elif(toknum in [COMMENT, STRING]):
						words = tokenizer(tokval,["#","*","/"])
						#words = nltk.word_tokenize(tokval)
						if(words):
							self._tokens.extend(words)
					prev_num = toknum
					prev_val = tokval
					prev_end = eend
			except Exception as e:
				print("Error in __setTokens__", e, line)
				#import pdb; pdb.set_trace()
				pass
	
	def annotate(self):
		assert self._sb.__str__() == '', "_sb already has value!"
		code_anchor = 0
		if(len(self._tokens) == 0):
			return self._codes
		try:
			for token in self._tokens:
				search = re.compile(re.escape(token)).search(self._codes, code_anchor)
				search_start = search.start()
				search_end = search.end()
				self._sb.Append(self._codes[code_anchor : search_start])
				self._sb.Append('<<'+token+'>>')
				code_anchor = search_end
			self._sb.Append(self._codes[code_anchor:])
		except Exception as e:
			print(e, "code: \n", self._codes, "tokens: \n", self._tokens)
			raise()
		return self._sb.__str__()




def main(file):
	source = open(file).read()
	code_secs = re.compile("<code>.*?</code>", flags = re.S|re.M).finditer(source)
	sb_file = StringBuilder()
	file_anchor = 0
	# iterate all codes area, defined by <code> ... </code>
	for code_sec in code_secs:
		# +6 and -7 to exclude <code> & </code> tags
		code_start = code_sec.start() + 6
		code_end = code_sec.end() - 7
		sb_file.Append(source[file_anchor : code_start])

		codes = source[code_start : code_end]
		ct = CodesTokenizer(codes)
		sb_file.Append(ct.annotate())

		file_anchor = code_end
	sb_file.Append(source[file_anchor:])
	file_sep = os.path.splitext(file)
	with open(file_sep[0] + "_annotated" + file_sep[1], 'w') as new_file:
			new_file.write(sb_file.__str__())

if __name__ == '__main__':
	for file in sys.argv[1:]:
		main(file)
