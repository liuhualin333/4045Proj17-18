# -*- coding: utf-8 -*-
'''
	This module converts tokenize the code sections defined by <code> ... </code> in the anwsers/posts.
	Code Token Definition: literals with only [] / {} / ' / " / , are not tokens
							XXX( is token denoting function/method call
							.	is token for special meaning
							Use normal word token for COMMENT / STRING (TODO: still use code tokenizer)
							Error messega path -> one token
							1.4.6 -> one token
	Usage:
		python code_tokenizer.py file1.txt ...
		(This will output file1_codeanno.txt)
	Token format:
		<c>XXX</c>
'''
from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP, tok_name, COMMENT, LPAR, RPAR, ERRORTOKEN
from io import BytesIO, StringIO
import nltk
import codecs
import re
import sys, os
import pdb
from utilities import *
import hashlib
code_tag = ['<c>', '</c>']

# StringBuilder class, using StringIO() to struct python string fast
class StringBuilder:
     _file_str = None

     def __init__(self):
         self._file_str = StringIO()

     def Append(self, str):
         self._file_str.write(str)

     def __str__(self):
         return self._file_str.getvalue()

# Main Tokenizer
class CodesTokenizer:
	# _sb is the internal string builder storing the annotated(tagged all tokens) "codes"
	# _tokens stores the tokens recognized given the "codes"
	# _codes is the given codes
	_sb = None
	_tokens = None
	_codes = None
	_reserve_codes = {}
	_processed_codes = None
	# Constructor, takes in the codes given, call __setTokens__ to set _tokens
	def __init__(self, codes):
		self._tokens = []
		self._codes = codes
		self._sb = StringBuilder()
		self.__setTokens__()

	# detec reserved tokens and store its signature in self._reserve_codes, replace those tokens with their corresponding signature(long int)
	def __ReplaceReserved__(self):
		paths = []
		consec_nums = []
		new_codes = StringBuilder()
		dashs = []
		lts_gts = []
		overall = []
		# get all paths 
		for path in re.finditer(re.compile(r"(\w\:)?((\\[^,;\'\" ]+)+|(/[^,;\'\" ]+)+)(\.\w+)?"), self._codes):
			paths.append([path.start(), path.end()])

		# get all 1.3.4 liked pattern
		for consec_num in re.finditer(re.compile(r"\d+(\.\d+)+"), self._codes):
			consec_nums.append([consec_num.start(), consec_num.end()])

		# get all python3-tk liked pattern
		for dash in re.finditer(re.compile(r"[\d\w]+(-[\d\w]+)+"), self._codes):
			dashs.append([dash.start(), dash.end()])

		# get all &lt; and &gt;
		for lt_gt in re.finditer(re.compile(r"&(lt|gt);"), self._codes):
			lts_gts.append([lt_gt.start(), lt_gt.end()])


		# custom union function to union the ranges of different reserved codes
		overall = union([paths, consec_nums, dashs, lts_gts])
		#pdb.set_trace()
		code_anchor = 0
		for start, end in overall:
			new_codes.Append(self._codes[code_anchor : start])
			hash_code = hash_str(self._codes[start : end])
			self._reserve_codes[hash_code] = self._codes[start : end]
			new_codes.Append(' ' + str(hash_code) + ' ')
			code_anchor = end
		if(code_anchor < len(self._codes)):
			new_codes.Append(self._codes[code_anchor:])
		self._processed_codes = new_codes.__str__()

	# __setTokens__: Based on _codes given, put all identified tokens to _tokens
	def __setTokens__(self):
		#g = tokenize(BytesIO(self._codes.encode('utf-8')).readline)  # tokenize the string
		prev_num = -1
		prev_val = None
		prev_end = -1
		self.__ReplaceReserved__()
		# Split _codes line by line and identify each line 
		ss = self._processed_codes.splitlines()
		#pdb.set_trace()
		for line in ss:
			# call python tokenize.tokenize and get the returned generator g
			g = tokenize(BytesIO(line.encode('utf-8')).readline)  # tokenize the string
			#pdb.set_trace()
			try:
				for toknum, tokval, starrt, eend, _ in g:
					chop_start = 0
					chop_end = len(tokval) - 1
					#pdb.set_trace()
					# if the token type is NAME / OP / NUMBER and not only consists of [,)\-\"';\[\]|..+]+
					if(toknum in [NAME, OP, NUMBER, ERRORTOKEN] and re.compile(r"^(?<![a-zA-Z])([,)\"';\[\]}\{]+|\.\.+)(?![a-zA-Z])$").search(tokval) == None):
						#pdb.set_trace()
						# Take xx( / &lt / &gt as one token, instead of two, eg. xx and (
						if(((prev_num == NAME and tokval == '(') or (prev_val == '&' and (tokval == 'lt' or tokval == 'gt')) ) and prev_end == starrt):
							self._tokens[-1] = self._tokens[-1] + tokval
						elif(tokval == '('):
							pass
						elif(toknum == NUMBER and int(tokval) in self._reserve_codes):
							self._tokens.append(self._reserve_codes[int(tokval)])
						else:
							self._tokens.append(tokval)
					# For comment / string, code 
					elif(toknum in [COMMENT, STRING]):
						#pdb.set_trace()
						if(toknum == STRING):
							# remove starting and ending ' / "
							while((tokval[chop_start] == '"' or tokval[chop_start] == "'") and chop_start < chop_end):
								chop_start += 1
							while((tokval[chop_end] == '"' or tokval[chop_end] == "'") and chop_start < chop_end):
								chop_end -= 1
						else:
							# remove starting # / ''' / """
							while((tokval[chop_start] == '#' and chop_start < chop_end)
								or (chop_end >= chop_start+3 and tokval[chop_start:chop_start+3] == "'''") 
								or (chop_end >= chop_start+3 and tokval[chop_start:chop_start+3] == '"""')):
								if(tokval[chop_start] == '#'):
									chop_start += 1
								else:
									chop_start += 3
						if(chop_start < chop_end or (tokval[chop_start] not in ['#', "'", '"'])):
							words = CodesTokenizer(tokval[chop_start:chop_end+1])._tokens
							if(words):
								self._tokens.extend(words)
					prev_num = toknum
					prev_val = tokval
					prev_end = eend
			except Exception as e:
				#print("Error in __setTokens__", e, line)
				#pdb.set_trace()
				pass
	# annotate: Based on _tokens and _codes, annotate the cooresponding tokens with token tags. 
	def annotate(self):
		assert self._sb.__str__() == '', "_sb already has value!"
		# code_anchor mark the current position in codes, before which has been processed already 
		code_anchor = 0
		if(len(self._tokens) == 0):
			return self._codes
		try:
			# For every token, find its starting pos and ending pos in codes, append original codes from code_anchor to starting pos
			#																	and append annotated(taged) token
			for token in self._tokens:
				search = re.compile(re.escape(token)).search(self._codes, code_anchor)
				search_start = search.start()
				search_end = search.end()
				self._sb.Append(self._codes[code_anchor : search_start])
				self._sb.Append(code_tag[0]+token+code_tag[1])
				# update code_anchor to ending pos of current token
				code_anchor = search_end
			self._sb.Append(self._codes[code_anchor:])
		except Exception as e:
			print(e, "code: \n", self._codes, "tokens: \n", self._tokens)
			#pdb.set_trace()
			raise()
		# return the annotated codes
		return self._sb.__str__()




def main(file):
	source = codecs.open(file, encoding='UTF-8').read()
	code_secs = re.compile("<code>.*?</code>", flags = re.S|re.M).finditer(source)
	sb_file = StringBuilder()
	# file_anchor mark the current position in current file, before which has been processed already 
	file_anchor = 0
	# iterate all codes area, defined by <code> ... </code>
	for code_sec in code_secs:
		# +6 and -7 to exclude <code> & </code> tags
		code_start = code_sec.start() + 6
		code_end = code_sec.end() - 7
		# Append the origin text from file_anchor to code_start
		sb_file.Append(source[file_anchor : code_start])
		#pdb.set_trace()
		# Init a new CodesTokenizer with codes, append the annotated codes to sb_file
		codes = source[code_start : code_end]
		ct = CodesTokenizer(codes)
		sb_file.Append(ct.annotate())
		file_anchor = code_end
	sb_file.Append(source[file_anchor:])
	file_sep = os.path.splitext(file)
	with open(file_sep[0] + "_codeAnno" + file_sep[1], 'w') as new_file:
			new_file.write(sb_file.__str__())

if __name__ == '__main__':
	# take in 1+ file(s) for processing
	for file in sys.argv[1:]:
		main(file)
