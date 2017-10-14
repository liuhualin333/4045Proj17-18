import re
#Python 3 string is unicode compatible. Python 2 will report error

#text = '''Albert Einstein (14 March 1879 – 18 April 1955) was a German-born theoretical physicist.[5]
#Einstein developed the theory of relativity, one of the two pillars of modern physics (alongside quantum mechanics).[4][6]:274 
#Einstein's work is also known for its influence on the philosophy of science.[7][8]
#Einstein is best known by the general public for his mass–energy equivalence formula E = mc2 (which has been dubbed "the world's most famous equation").[9]
#He received the 1921 Nobel Prize in Physics "for his services to theoretical physics, and especially for his discovery of the law of the photoelectric effect",[10] a pivotal step in the evolution of quantum theory.'''
text = '''While I tested this with CPython, its quite likely most/all other Python implementations use an array to store lists internally. So unless they use a sophisticated data structure designed for efficient list re-sizing, they likely have the same performance characteristic.'''
def tokenizer(text, special_words=[]):
	# Split on whitespace
	wordList = text.split()
	
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

	tokenList = []
	lastWord = ' '
	#For names and special pronouns
	specialPronounFlag = False
	#Combine equal sign with previous and next words
	equalSignFlag = False
	#For Money (e.g. 550,5500.00)
	moneyPattern = re.compile(r'[0-9]*\.[0-9]+')
	for word in wordList:
		if (word == ''):
			continue
		if (lastWord == ''):
			lastWord = ' '
		if (lastWord[0].isupper() and word[0].isupper()):
			tokenList = tokenList[:-1]
			lastWord = lastWord + ' ' + word
			specialPronounFlag = True
		elif (word == '='):
			tokenList = tokenList[:-1]
			lastWord = lastWord + ' ' + word
			equalSignFlag = True
		else:
			if (specialPronounFlag == True):
				tokenList.append(lastWord)
				specialPronounFlag = False
			elif (equalSignFlag == True):
				tokenList.append(lastWord + ' ' + word)
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
				elm = elm.strip('()\"\'')
				if (not equalSignFlag and elm != ''):
					tokenList.append(elm)
				else:
					equalSignFlag = False
				lastWord = elm
	#print(tokenList[:-1])
	return tokenList

if __name__ == "__main__":
	tokenizer(text)
