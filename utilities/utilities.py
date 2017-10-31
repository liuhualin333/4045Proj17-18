from io import BytesIO, StringIO
import re
import pdb
# Utility functions for NLP project

# StringBuilder class, using StringIO() to struct python string fast
class StringBuilder:
	 _file_str = None

	 def __init__(self):
		 self._file_str = StringIO()

	 def Append(self, str):
		 self._file_str.write(str)

	 def __str__(self):
		 return self._file_str.getvalue()

# annoText, annoTag: [<c>,</c>] or [<t>,</t>],
# return: [tokens]
def anno2Tokens(annoText, annoTag):
	tokens = re.compile(annoTag[0]+".*?"+annoTag[1], flags=re.S | re.M).finditer(annoText)
	token_list = []
	for token in tokens:
		token_start = token.start() + 3
		token_end = token.end() - 4
		if(token_end > token_start + 1):
			token_list.append(annoText[token_start:token_end])
	return token_list

# from mixed annotated text to clean text(remove <c></c> <t></t> tag) and output the corresponding tag
def MixAnno2Tokens(annoText):
	token_list = []
	anno_anchor = 0
	code_tag = ['<c>', '</c>']
	text_tag = ['<t>', '</t>']
	code_secs = re.compile("<code>.*?</code>", flags=re.S | re.M).finditer(annoText)
	# iterate all codes area, defined by <code> ... </code>
	for code_sec in code_secs:
		# +6 and -7 to exclude <code> & </code> tags
		code_start = code_sec.start() + 6
		code_end = code_sec.end() - 7
		# Append the origin text, orinal label from anno_anchor to code_start
		token_list.extend(anno2Tokens(annoText[anno_anchor : code_sec.start()], text_tag))
		# Init a new CodesTokenizer with codes, append the annotated codes to sb_file
		token_list.extend(anno2Tokens(annoText[code_start : code_end], code_tag))
		anno_anchor = code_sec.end()
	token_list.extend(anno2Tokens(annoText[anno_anchor : ], text_tag))
	return token_list




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
		pdb.set_trace()
		token_start = token.start() + 3
		token_end = token.end() - 4
		Appendtxtlabel(annoText[anno_anchor:token.start()],'O'*(token.start() - anno_anchor))
		Appendtxtlabel(annoText[token_start],'T')
		if(token_end - token_start >= 3):
				Appendtxtlabel(annoText[token_start+1:token_end-1],'I'*(token_end-token_start-2))
		if(token_end - token_start >= 2):
			Appendtxtlabel(annoText[token_end-1],'E')
		anno_anchor = token.end()
	return origin_text.__str__(), origin_label.__str__()

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
	return origin_txt.__str__(), origin_label.__str__()

#def crfAnno2text()

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
			pattern = re.compile(r'^\d+\|([^\n\|]*?)\|\"(.*?)\"(\n(?=\d+\|)|($))', flags = re.S|re.M)
		#pdb.set_trace()
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

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

def hash_str(str):
	return abs(hash(str))

def overlap(rg1, rg2):
	#if(rg1[0] > rg2[0]):
	#	rg1, rg2 = rg2, rg1
	assert rg1[0] <= rg2[0]
	return rg1[1] >= rg2[0]

def union(ll):
	# li is the list of index, element: which list(index of list in ll), which index(index of pointed list)
	li = [[i, 0] for i in range(len(ll)) if ll[i]]
	# lout is the output list
	lout = []
	# while there is index that hasn't reached its maximum
	temp = []
	#import pdb; pdb.set_trace()
	while(li):
		li.sort(key=lambda x: ll[x[0]][x[1]][0])
		# if temp is empty, put the first(smallest) in li as temp and increase the index
		if(temp == []):
			temp = ll[li[0][0]][li[0][1]]
			li[0][1] += 1
		# if temp is not empty, get the first in li and check if there is overlap
		else:
			ili = li[0]
			# if there is overlap, extend temp and increase ili index
			if(overlap(temp, ll[ili[0]][ili[1]])):
				temp[1] = max(ll[ili[0]][ili[1]][1], temp[1])
				ili[1] += 1
			# if there isn't overlap, append temp to lout and reset temp
			else:
				lout.append(temp)
				temp = []
		li = [ili for ili in li if ili[1] < len(ll[ili[0]])]
	if(temp):
		lout.append(temp)
	return lout

if __name__ == '__main__':
	ll = [[[0, 22]], [[13, 18]], [[1, 14], [17, 22]]]
	print(union(ll))
