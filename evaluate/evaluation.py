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

def main():
	x_predict, y_predict = get_data('../posts/posts_training_clean_Annotated.txt') 
	x_truth, y_truth = get_data("../Training/posts_annotated.txt")
	Y_predict = [item for sublist in y_predict for item in sublist]
	X_predict = [item for sublist in x_predict for item in sublist]
	Y_truth = [item for sublist in y_truth for item in sublist]
	X_truth = [item for sublist in x_truth for item in sublist]
	evaluate(Y_truth, Y_predict)

def test_correctness():
	diff = []
	for i in range(len(y_truth)):
		if(len(y_predict[i]) != len(y_truth[i])):
			diff.append(i)

	diff.append('\n')
	for i in range(len(y_truth)):
		if(len(y_predict[i]) != len(x_predict[i])):
			diff.append(i)
	return diff
#test_correctness()
#'''

'''
arguments:
	Y_truth, Y_predict: a list of char, each char in ['U','T','E','O','I']
	shape of Y_truth == shape of Y_predict
'''
def evaluate(Y_truth, Y_predict):
	true_positive = predict_tokens = true_tokens = 0
	try:
		i = staart = 0
		while(i < len(Y_truth)):
			# if this char is single char token
			if(Y_truth[i] == 'U'):
				true_positive += (Y_predict[i] == Y_truth[i])
				true_tokens += 1
			# if this char is start of a token 
			elif(Y_truth[i] == 'T'):
				staart = i
				match = True
				while(i < len(Y_truth) and Y_truth[i] != 'E'):
					match &= (Y_truth[i] == Y_predict[i])
					i += 1
				if(i < len(Y_truth) and Y_truth[i] == 'E'):
					match &= Y_truth[i] == Y_predict[i]
					true_positive += match
					true_tokens += 1
			i += 1
		
		i = 0
		while(i < len(Y_predict)):
			if(Y_predict[i] == 'U'):
				predict_tokens += 1
			# if this char is start of a token 
			elif(Y_predict[i] == 'T'):
				while(i < len(Y_predict) and Y_predict[i] != 'E'):
					i += 1
				if(i < len(Y_predict) and Y_predict[i] == 'E'):
					predict_tokens += 1
			i += 1

	except Exception as e:
		print("Error in evaluate: ", e)
		pass
	#'''
	#'''
	print("statistics on regex, in order of (U, T, E, O, I) :")
	print("Precision score for regex: ", precision_score(Y_truth, Y_predict, average=None, labels=['U','T','E','O','I']))
	print("Recall score for regex:    ", recall_score(Y_truth, Y_predict, average=None, labels=['U','T','E','O','I']))
	print("F1 score for regex:        ", f1_score(Y_truth, Y_predict, average=None, labels=['U','T','E','O','I']))
	print("Weighted F1 score for regex:        ", f1_score(Y_truth, Y_predict, average='weighted'))

	print("statistics on regex, for overall token matching:")
	precision_token = true_positive / predict_tokens
	recall_token = true_positive / true_tokens
	f1_token = 2 * (precision_token * recall_token) / (precision_token + recall_token)
	print("Precision score: ", precision_token)
	print("Recall score:    ", recall_token)
	print("F1 score:        ", f1_token)
	#'''

'''
arguments:
	Y_truth, Y_predict: a list of string, each char in string is in ['U','T','E','O','I']
	shape of Y_truth == shape of Y_predict
'''
def evaluate_nested(y_truth, y_predict):
	Y_predict = [item for sublist in y_predict for item in sublist]
	Y_truth = [item for sublist in y_truth for item in sublist]
	evaluate(Y_truth, Y_predict)
