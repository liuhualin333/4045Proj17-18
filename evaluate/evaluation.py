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

true_positive = predict_tokens = true_tokens = 0
try:
	i = staart = 0
	while(i < len(Y_anno)):
		# if this char is single char token
		if(Y_anno[i] == 'U'):
			true_positive += (Y_regex[i] == Y_anno[i])
			true_tokens += 1
		# if this char is start of a token 
		elif(Y_anno[i] == 'T'):
			staart = i
			match = True
			while(i < len(Y_anno) and Y_anno[i] != 'E'):
				match &= (Y_anno[i] == Y_regex[i])
				i += 1
			if(i < len(Y_anno) and Y_anno[i] == 'E'):
				match &= Y_anno[i] == Y_regex[i]
				true_positive += match
				true_tokens += 1
		i += 1
	
	i = 0
	while(i < len(Y_regex)):
		if(Y_regex[i] == 'U'):
			predict_tokens += 1
		# if this char is start of a token 
		elif(Y_regex[i] == 'T'):
			while(i < len(Y_anno) and Y_anno[i] != 'E'):
				i += 1
			if(i < len(Y_regex) and Y_regex[i] == 'E'):
				predict_tokens += 1
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

print("statistics on regex, for overall token matching:")
precision_token = true_positive / predict_tokens
recall_token = true_positive / true_tokens
f1_token = 2 * (precision_token * recall_token) / (precision_token + recall_token)
print("Precision score: ", precision_token)
print("Recall score: ", recall_token)
print("F1 score: ", f1_token)
#'''

