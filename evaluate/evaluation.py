import sklearn_crfsuite
from sklearn_crfsuite import metrics
import pdb
import os
import sys
from io import BytesIO, StringIO
from sklearn.metrics import f1_score, precision_score, recall_score
import re
sys.path.insert(0, '../utilities')
from utilities import *

x_regex, y_regex = get_data('../posts/posts_training_clean_Annotated.txt') 
x_anno, y_anno = get_data("../Training/posts_annotated.txt")

def test_correctness():
	for i in range(50):
		if(len(y_regex[i]) != len(y_anno[i])):
			print(i)

	print('\n')
	for i in range(50):
		if(len(y_regex[i]) != len(x_regex[i])):
			print(i)
#test_correctness()
#'''
Y_regex = [item for sublist in y_regex for item in sublist]
X_regex = [item for sublist in x_regex for item in sublist]
Y_anno = [item for sublist in y_anno for item in sublist]
X_anno = [item for sublist in x_anno for item in sublist]

Y_regex_key = []
Y_anno_key = []
i = staart = 0
try:
	while(i < len(Y_anno)):
		# if this char is single char token
		if(Y_anno[i] == 'U'):
			Y_anno_key.append(True)
			Y_regex_key.append(Y_regex[i] == Y_anno[i])
		# if this char is start of a token 
		elif(Y_anno[i] == 'T'):
			staart = i
			match = True
			while(i < len(Y_anno) and Y_anno[i] != 'E'):
				match &= (Y_anno[i] == Y_regex[i])
				i += 1
			if(i < len(Y_anno) and Y_anno[i] == 'E'):
				match &= Y_anno[i] == Y_regex[i]
				Y_anno_key.append(True)
				Y_regex_key.append(match)
		i += 1
except Exception as e:
	pdb.set_trace()
	pass
#'''
#'''
print("statistics on regex, in order of (U, T, E, O, I) :")
print("Precision score for regex: ", precision_score(Y_anno, Y_regex, average=None, labels=['U','T','E','O','I']))
print("Recall score for regex:    ", recall_score(Y_anno, Y_regex, average=None, labels=['U','T','E','O','I']))
print("F1 score for regex:        ", f1_score(Y_anno, Y_regex, average=None, labels=['U','T','E','O','I']))
print("Weighted F1 score for regex:        ", f1_score(Y_anno, Y_regex, average='weighted'))
print("F1 score for regex in terms whether matched true tokens: ", f1_score(Y_anno_key, Y_regex_key))
#'''

