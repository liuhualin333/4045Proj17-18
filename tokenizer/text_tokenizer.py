import re
import sys
import os
from io import StringIO
#Python 3 string is unicode compatible. Python 2 will report error

#text = '''Albert Einstein (14 March 1879 – 18 April 1955) was a German-born theoretical physicist.[5]
#Einstein developed the theory of relativity, one of the two pillars of modern physics (alongside quantum mechanics).[4][6]:274 
#Einstein's work is also known for its influence on the philosophy of science.[7][8]
#Einstein is best known by the general public for his mass–energy equivalence formula E = mc2 (which has been dubbed "the world's most famous equation").[9]
#He received the 1921 Nobel Prize in Physics "for his services to theoretical physics, and especially for his discovery of the law of the photoelectric effect",[10] a pivotal step in the evolution of quantum theory.'''
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

	def __init__(self, text, special_words=[]):
		self._tokens = []
		self._text = text
		self._sb = StringBuilder()
		self.tokenizer(text,special_words)

	def tokenizer(self,text, special_words=[]):
		# Split on whitespace
		sentenceList = text.splitlines()
		""" This function needs rework
		if(len(special_words) > 0):
			_temp = []
			for special_word in special_words:
				for item in wordList:
					#item = list(filter(None, item.split(special_word)))
					if(special_word in item):
						_temp.extend(list(filter(None, item.split(special_word))))
					else:
						_temp.append(item)
				wordList = _temp
				_temp = []
		"""

		tokenList = []
		lastWord = ' '
		#For names and special pronouns
		specialPronounFlag = False
		#Combine equal sign with previous and next words
		equalSignFlag = False
		#For Money (e.g. 550,5500.00)
		moneyPattern = re.compile(r'[0-9]*\.[0-9]+')
		for sentence in sentenceList:
			tokenList = []
			lastWord = ' '
			wordList = sentence.split('|')[-1].split()
			for word in wordList:
				if (word == ''):
					continue
				if (lastWord == ''):
					lastWord = ' '
				if (lastWord[0].isupper() and word[0].isupper() and not lastWord[-1].isalnum()):
					tokenList = tokenList[:-1]
					lastWord = lastWord + ' ' + word
					specialPronounFlag = True
				elif (word == '='):
					tokenList = tokenList[:-1]
					lastWord = lastWord + ' ' + word
					equalSignFlag = True
				else:
					if (specialPronounFlag == True):
						tokenList.append(lastWord.strip('.,'))
						specialPronounFlag = False
					elif (equalSignFlag == True):
						tokenList.append((lastWord + ' ' + word).strip('.,'))
					# Handle Ph.D. and case like science.[7][8]
					if (not moneyPattern.match(word)):
						if (word.count('.') < 2):
							word = re.split(r',|\.', word)#split on ,.
						else:
							word = word.split(',')
					if (type(word) is str):
						word = word.strip('()')
						if (not equalSignFlag):
							tokenList.append(word)
						else:
							equalSignFlag = False
						lastWord = word
						continue
					for elm in word:
						elm = elm.strip('()\"\':')
						if (not equalSignFlag and elm != ''):
							tokenList.append(elm)
						else:
							equalSignFlag = False
						lastWord = elm
			#print(tokenList[:-1])
			self._tokens.extend(tokenList)

	def annotate(self):
		assert self._sb.__str__() == '', "_sb already has value!"
		text_anchor = 0
		if(len(self._tokens) == 0):
			return self._text
		try:
			for token in self._tokens:
				search = re.compile(re.escape(token)).search(self._text, text_anchor)
				search_start = search.start()
				search_end = search.end()
				self._sb.Append(self._text[text_anchor : search_start])
				self._sb.Append('<<'+token+'>>')
				text_anchor = search_end
			self._sb.Append(self._text[text_anchor:])
		except Exception as e:
			print(e, "code: \n", self._text, "tokens: \n", self._tokens)
			raise e
		return self._sb.__str__()

def main(file):
	source = open(file).read()
	code_secs = re.compile("<code>.*?</code>", flags = re.S|re.M).finditer(source)
	sb_file = StringBuilder()
	# iterate all non-codes area, defined by <code> ... </code>
	file_anchor = 0;
	# Skip the first line
	file_anchor = re.compile(re.escape('Id|Body')).search(source, 0).end()
	sb_file.Append(source[0:file_anchor])
	# Define text as "not code"
	for code_sec in code_secs:
		code_start = code_sec.start()
		code_end = code_sec.end()
		text = source[file_anchor:code_start]
		tt = TextTokenizer(text)
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
	with open(file_sep[0] + "_annotated" + file_sep[1], 'w') as new_file:
			new_file.write(sb_file.__str__())

if __name__ == "__main__":
	for file in sys.argv[1:]:
		main(file)
