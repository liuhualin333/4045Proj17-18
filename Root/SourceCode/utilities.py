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
	#tokens = re.compile(annoTag[0]+".*?"+annoTag[1], flags=re.S | re.M).finditer(annoText)
	tokens = re.compile(r"(<t>.*?</t>)|(<c>.*?</c>)", flags=re.S | re.M).finditer(annoText)
	token_list = []
	for token in tokens:
		token_start = token.start() + 3
		token_end = token.end() - 4
		if(token_end > token_start + 1):
			token_list.append(annoText[token_start:token_end])
	return token_list

def RawMixedAnno2Tokens(annoText):
	tags = re.compile(r"<t>|<c>|</t>|", flags=re.S | re.M).finditer(annoText)
	anno_anchor = 0
	is_in = False
	origin_text = StringBuilder()
	origin_label = StringBuilder()
	def Appendtxtlabel(_txt, _label):
		origin_text.Append(_txt)
		origin_label.Append(_label)
	while(anno_anchor < len(annoText)):
		if(anno_anchor < len(annoText) - 4):
			if((anno_anchor < len(annoText) - 7) and annoText[anno_anchor:anno_anchor+3] in ['<t>','<c>'] and annoText[anno_anchor+4:anno_anchor+8] in ['</t>','</c>']):
				is_in = False
				Appendtxtlabel(annoText[anno_anchor+3], 'U')
				anno_anchor += 8
			elif(annoText[anno_anchor:anno_anchor+3] in ['<t>','<c>']):
				is_in = True
				Appendtxtlabel(annoText[anno_anchor+3], 'T')
				anno_anchor += 4
			elif(annoText[anno_anchor+1:anno_anchor+5] in ['</t>','</c>']):
				is_in = False
				Appendtxtlabel(annoText[anno_anchor], 'E')
				anno_anchor += 5
			else:
				if(is_in):
					Appendtxtlabel(annoText[anno_anchor], 'I')
				else:
					Appendtxtlabel(annoText[anno_anchor], 'O')
				anno_anchor += 1
		else:
			if(is_in):
				Appendtxtlabel(annoText[anno_anchor], 'I')
			else:
				Appendtxtlabel(annoText[anno_anchor], 'O')
			anno_anchor += 1
	return origin_text.__str__(), origin_label.__str__()
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
	#tokens = re.compile(annoTag[0]+".*?"+annoTag[1], flags=re.S | re.M).finditer(annoText)
	tokens = re.compile(r"(<t>.*?</t>)|(<c>.*?</c>)", flags=re.S | re.M).finditer(annoText)
	anno_anchor = 0
	def Appendtxtlabel(_txt, _label):
		origin_text.Append(_txt)
		origin_label.Append(_label)
	for token in tokens:
		token_start = token.start() + 3
		token_end = token.end() - 4
		Appendtxtlabel(annoText[anno_anchor:token.start()],'O'*(token.start() - anno_anchor))
		if(token_end == token_start + 1):
			Appendtxtlabel(annoText[token_start],'U')
		else:
			if(token_end > token_start + 1):
				Appendtxtlabel(annoText[token_start],'T')
			if(token_end - token_start >= 3):
				Appendtxtlabel(annoText[token_start+1:token_end-1],'I'*(token_end-token_start-2))
			if(token_end - token_start >= 2):
				Appendtxtlabel(annoText[token_end-1],'E')
		anno_anchor = token.end()
	Appendtxtlabel(annoText[anno_anchor:],'O'*(len(annoText) - anno_anchor))
	#pdb.set_trace()
	return origin_text.__str__(), origin_label.__str__()

# from mixed annotated text to clean text(remove <c></c> <t></t> tag) and output the corresponding tag
def MixAnno2charsTokens(annoText):
	#origin_txt = StringBuilder()
	#origin_label = StringBuilder()
	origin_txt, origin_label, original_types = [], [], []
	anno_anchor = 0
	code_tag = ['<c>', '</c>']
	text_tag = ['<t>', '</t>']
	code_secs = re.compile("<code>(.*?)</code>", flags=re.S | re.M).finditer(annoText)
	def Appendtxtlabel(_txt, _label, _btypes):
		#origin_txt.Append(_txt)
		#origin_label.Append(_label)
		origin_txt.append(_txt)
		origin_label.append(_label)
		original_types.append(_btypes)
	# iterate all codes area, defined by <code> ... </code>
	#pdb.set_trace()
	for code_sec in code_secs:
		# +6 and -7 to exclude <code> & </code> tags
		code_start = code_sec.start() + 6
		code_end = code_sec.end() - 7
		# Append the origin text, orinal label from anno_anchor to code_start
		Appendtxtlabel(*anno2charsTokens(annoText[anno_anchor : code_sec.start()], text_tag), 't')
		# Init a new CodesTokenizer with codes, append the annotated codes to sb_file
		Appendtxtlabel(*anno2charsTokens(annoText[code_start : code_end], code_tag), 'c')
		anno_anchor = code_sec.end()

	Appendtxtlabel(*anno2charsTokens(annoText[anno_anchor : ], text_tag), 't')
	#return origin_txt.__str__(), origin_label.__str__()
	return origin_txt, origin_label, original_types

def get_data(filepath):
	X, Y = [], []
	with open(filepath) as f:
		file_text = f.read()
		if(r'Id|Body' in file_text[:15]):
			flag = 'answer'
			file_text = file_text[8:]
			pattern = re.compile(r'^\d+\|\"(.*?)\"\n(?=\d+\|)', flags = re.S|re.M)
			end_pattern = re.compile(r'^\d+\|\"(.*)\"$', flags = re.S|re.M)
		else:
			flag = 'post'
			file_text = file_text[14:]
			pattern = re.compile(r'^\d+\|([^\n\|]*?)\|\"(.*?)\"\n(?=\d+\|)', flags = re.S|re.M)
			end_pattern = re.compile(r'^\d+\|([^\n\|]*?)\|\"(.*)\"$', flags = re.S|re.M)
		#pdb.set_trace()
		def post2XY(post):
			_text, _label, _ = MixAnno2charsTokens(post.group(1))
			X.extend(_text)
			Y.extend(_label)
			if(flag == 'post'):
				_text, _label, _ = MixAnno2charsTokens(post.group(2))
				X.extend(_text)
				Y.extend(_label)
		for post in pattern.finditer(file_text):
			post2XY(post)
		if(post):
			last_post = end_pattern.search(file_text, post.end())
		else:
			last_post = end_pattern.search(file_text)
		post2XY(last_post)
	Y = [list(str) for str in Y]
	return X, Y




class rpost:
	ptype = None
	pid = None
	ptitle = []
	ptitle_label = []
	ptitle_block_type = []
	pbody = []
	pbody_label = []
	pbody_block_type = []
	
	def __init__(self, ptype, pid):
		self.ptype = ptype
		if(ptype == 'answer'):
			self.ptitle = None
			self.ptitle_block_type = None
		self.pid = pid
	
	def addTitle(self, ptitle, label, block_type):
		self.ptitle = ptitle
		self.ptitle_label = [list(str) for str in label]
		self.ptitle_block_type = block_type

	def addBody(self, pbody, label, block_type):
		self.pbody = pbody
		self.pbody_label = [list(str) for str in label]
		self.pbody_block_type = block_type

def split_train_text(file_text):
	rpost_list = []
	if(r'Id|Body' in file_text[:15]):
		ptype = 'answer'
		file_text = file_text[8:]
		pattern = re.compile(r'^(\d+)\|\"(.*?)\"\n(?=\d+\|)', flags = re.S|re.M)
		end_pattern = re.compile(r'^(\d+)\|\"(.*)\"$', flags = re.S|re.M)
	else:
		ptype = 'post'
		file_text = file_text[14:]
		pattern = re.compile(r'^(\d+)\|([^\n\|]*?)\|\"(.*?)\"\n(?=\d+\|)', flags = re.S|re.M)
		end_pattern = re.compile(r'^(\d+)\|([^\n\|]*?)\|\"(.*)\"$', flags = re.S|re.M)
	#pdb.set_trace()
	def post2rpost(post):
		# initialize the post
		p = rpost(ptype, post.group(1))
		_text, _label, _types = MixAnno2charsTokens(post.group(2))
		if(ptype == 'post'):
			p.addTitle(_text, _label, _types)
			_text, _label, _types = MixAnno2charsTokens(post.group(3))
			p.addBody(_text, _label, _types)
		else:
			p.addBody(_text, _label, _types)
		rpost_list.append(p)
	try:
		for post in pattern.finditer(file_text):
			post2rpost(post)
		last_post = end_pattern.search(file_text, post.end())
		post2rpost(last_post)
	except Exception as e:
		pdb.set_trace()
		pass
	return rpost_list

def TextFromFile(filepath):
	text = StringBuilder()
	rpost_list = split_train_text(open(filepath).read())
	for p in rpost_list:
		if(p.ptype == 'post'):
			text.Append(' '.join([tb for tb in p.ptitle]))
		text.Append(' '.join([tb for tb in p.pbody]))
		text.Append(' ')
	return text.__str__()






# X, Y: strings
# X contains block of text
# Y contains block tag (U,E,I,T,O)
def crfTokens2Anno(X, Y, tag=['<t>','</t>']):
	assert len(X) == len(Y)
	text = StringBuilder()
	for x,y in zip(X, Y):
		if(y == 'T'):
			text.Append(tag[0]+x)
		elif(y == 'E'):
			text.Append(x+tag[1])
		elif(y == 'U'):
			text.Append(tag[0]+x+tag[1])
		else:
			text.Append(x)
	#pdb.set_trace()
	return text.__str__()

# receive a raw text and annotate
def crfText2Anno(crf, file_text):
	new_file_text = StringBuilder()
	if(r'Id|Body' in file_text[:15]):
		flag = 'answer'
		new_file_text.Append(file_text[:8])
		file_text = file_text[8:]
		pattern = re.compile(r'^(\d+)\|\"(.*?)\"\n(?=\d+\|)', flags = re.S|re.M)
		end_pattern = re.compile(r'^(\d+)\|\"(.*)\"$', flags = re.S|re.M)
	else:
		flag = 'post'
		new_file_text.Append(file_text[:14])
		file_text = file_text[14:]
		pattern = re.compile(r'^(\d+)\|([^\n\|]*?)\|\"(.*?)\"\n(?=\d+\|)', flags = re.S|re.M)
		end_pattern = re.compile(r'^(\d+)\|([^\n\|]*?)\|\"(.*)\"$', flags = re.S|re.M)
	
	def predictMixed(txt):
		code_secs = re.compile("<code>(.*?)</code>", flags=re.S | re.M).finditer(txt)
		predcit_label = []
		pred_anchor = 0
		for code_sec in code_secs:
			# +6 and -7 to exclude <code> & </code> tags
			#pdb.set_trace()
			predcit_label.extend(crf.predict([txt[pred_anchor : code_sec.start()]])[0])
			code_start = code_sec.start() + 6
			code_end = code_sec.end() - 7
			predcit_label.extend(['O']*6 + crf.predict([txt[code_start : code_end]])[0] + ['O']*7)
			pred_anchor = code_sec.end()

		predcit_label.extend(crf.predict([txt[pred_anchor : ]])[0])
		return predcit_label

	def post2txt(post):
		_txt = StringBuilder()
		_txt.Append(post.group(1)+'|')
		if(flag == 'post'):
			_txt.Append(crfTokens2Anno(post.group(2), predictMixed(post.group(2)) ) + '|')
			_txt.Append('"' + crfTokens2Anno(post.group(3), predictMixed(post.group(2)) ) + '"\n')
		else:
			_txt.Append('"' + crfTokens2Anno(post.group(2), predictMixed(post.group(2)) ) + '"\n')
		new_file_text.Append(_txt.__str__())

	for post in pattern.finditer(file_text):
		post2txt(post)
	last_post = end_pattern.search(file_text, post.end())
	post2txt(last_post)
	return new_file_text.__str__()

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
