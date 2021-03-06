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

def evaluate_regex_output(Data_Root, msg):
	x_predict, y_predict = get_data(Data_Root+'posts_training_clean_Predicted.txt') 
	x_truth, y_truth = get_data(Data_Root+"posts_manual_tokenized.txt")
	Y_predict = [item for sublist in y_predict for item in sublist]
	Y_truth = [item for sublist in y_truth for item in sublist]
	test_correctness(y_truth, y_predict, x_predict)
	x_predict, y_predict = get_data(Data_Root+'answers_training_clean_Predicted.txt') 
	x_truth, y_truth = get_data(Data_Root+"answers_manual_tokenized.txt")
	Y_predict.extend([item for sublist in y_predict for item in sublist])
	Y_truth.extend([item for sublist in y_truth for item in sublist])
	print(msg)
	print_evaluation(Y_truth, Y_predict)

def check_test():
	x_predict, y_predict = get_data('../../posts/posts_training_clean_Annotated.txt') 
	x_truth, y_truth = get_data("../../Training/posts_annotated.txt")
	Y_predict = [item for sublist in y_predict for item in sublist]
	Y_truth = [item for sublist in y_truth for item in sublist]
	pdb.set_trace()
	#x_predict, y_predict = get_data('../../posts/answers_training_clean_Annotated.txt') 
	#x_truth, y_truth = get_data("../../Training/answers_annotated.txt")
	#Y_predict.extend([item for sublist in y_predict for item in sublist])
	#Y_truth.extend([item for sublist in y_truth for item in sublist])
	#pdb.set_trace()
	print_evaluation(Y_truth, Y_predict)

def test_correctness(y_truth, y_predict, x_predict):
	diff = []
	for i in range(len(y_truth)):
		if(len(y_predict[i]) != len(y_truth[i])):
			diff.append(i)

	diff.append('\n')
	for i in range(len(y_truth)):
		if(len(y_predict[i]) != len(x_predict[i])):
			diff.append(i)
	return diff

class state:
	last_T_pos = None
	T_pos = None
	output = False
	def updateFlag(self, label, i):
		self.output = False
		self.last_T_pos = False
		if(label  == 'E'):
			self.last_T_pos = self.T_pos
		elif(label  in ['U','O']):
			self.T_pos = None
		elif(label == 'T'):
			self.T_pos = i
		if(label in ['U','E']):
			self.output = True



def get_tp_tokens(Y_truth, X_truth, Y_predict, X_predict):
	true_positive = set()
	false_positive = set()
	false_negative = set()
	truth_state = state()
	predict_state = state()

	#try:
	i = staart = 0
	while(i < len(Y_truth) and i < len(Y_predict)):
		truth_state.updateFlag(Y_truth[i], i)
		predict_state.updateFlag(Y_predict[i], i)
		if(Y_truth[i] == 'U' == Y_predict[i]):
			true_positive.add(X_truth[i])
		elif((Y_truth[i] == 'E' == Y_predict[i]) and truth_state.last_T_pos == predict_state.last_T_pos):
			true_positive.add(X_truth[truth_state.last_T_pos : i+1])
		else:
			if(truth_state.output):
				if(Y_truth[i] == 'U'):
					false_negative.add(X_truth[i])
				else:

					false_negative.add(X_truth[truth_state.last_T_pos : i+1])
			if(predict_state.output):
				if(Y_predict[i] == 'U'):
					false_positive.add(X_predict[i])
				else:
					false_positive.add(X_predict[predict_state.last_T_pos : i+1])
		i += 1
	if(i < len(Y_truth)):
		while(i < len(Y_truth)):
			truth_state.updateFlag(Y_truth[i], i)
			if(Y_truth[i] == 'U'):
				false_negative.add(X_truth[i])
			elif(Y_truth[i] == 'E' and truth_state.last_T_pos):
				false_negative.add(X_truth[truth_state.last_T_pos : i+1])
			i += 1
	elif(i < len(Y_predict)):
		while(i < len(Y_predict)):
			pdb.set_trace()
			predict_state.updateFlag(Y_predict[i], i)
			if(Y_predict[i] == 'U'):
				false_positive.add(X_predict[i])
			elif(Y_predict[i] == 'E' and predict_state.last_T_pos):
				false_positive.add(X_predict[predict_state.last_T_pos : i+1])
			i += 1

	#except Exception as e:
	#	print("Error in evaluate: ", e)
	#	pdb.set_trace()
	#	pass
	return true_positive, false_positive, false_negative



def getTPfromFile(truthfile='../tokenizer/crf/val_true.txt', predictfile='../tokenizer/crf/val_predict.txt'):
	x_predict, y_predict = RawMixedAnno2Tokens(open(predictfile).read()) 
	x_truth, y_truth = RawMixedAnno2Tokens(open(truthfile).read())
	Y_predict = [item for sublist in y_predict for item in sublist]
	Y_truth = [item for sublist in y_truth for item in sublist]
	X_predict = ''.join([item for sublist in x_predict for item in sublist])
	X_truth = ''.join([item for sublist in x_truth for item in sublist])
	return get_tp_tokens(Y_truth, X_truth, Y_predict, X_predict)


def count_tp_tokens(Y_truth, Y_predict):
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
	precision_token = true_positive / predict_tokens
	recall_token = true_positive / true_tokens
	f1_token = 2 * (precision_token * recall_token) / (precision_token + recall_token)
	return precision_token, recall_token, f1_token


'''
arguments:
	Y_truth, Y_predict: a list of char, each char in ['U','T','E','O','I']
	shape of Y_truth == shape of Y_predict
'''
def print_evaluation(Y_truth, Y_predict):
	
	#'''
	#'''
	'''
	print("statistics on regex, in order of (U, T, E, O, I) :")
	print("Precision score for regex: ", precision_score(Y_truth, Y_predict, average=None, labels=['U','T','E','O','I']))
	print("Recall score for regex:    ", recall_score(Y_truth, Y_predict, average=None, labels=['U','T','E','O','I']))
	print("F1 score for regex:        ", f1_score(Y_truth, Y_predict, average=None, labels=['U','T','E','O','I']))
	print("Weighted F1 score for regex:        ", f1_score(Y_truth, Y_predict, average='weighted'))
	'''
	precision_token, recall_token, f1_token = count_tp_tokens(Y_truth, Y_predict)
	print("Precision score: ", precision_token)
	print("Recall score:    ", recall_token)
	print("F1 score:        ", f1_token)
	#'''

'''
arguments:
	Y_truth, Y_predict: a list of string, each char in string is in ['U','T','E','O','I']
	shape of Y_truth == shape of Y_predict
'''
def evaluate_nested(y_predict, y_truth):
	Y_predict = [item for sublist in y_predict for item in sublist]
	Y_truth = [item for sublist in y_truth for item in sublist]
	print_evaluation(Y_truth, Y_predict)

def evaluate_nested_dual(yt_predict, yt_truth, yc_predict, yc_truth, verbose):
	Y_predict = [item for sublist in yt_predict for item in sublist]
	Y_truth = [item for sublist in yt_truth for item in sublist]
	Y_predict.extend([item for sublist in yc_predict for item in sublist])
	Y_truth.extend([item for sublist in yc_truth for item in sublist])
	if(verbose):
		print_evaluation(Y_truth, Y_predict)
	return count_tp_tokens(Y_truth, Y_predict)

def evaluate_nested_score(y_predict, y_truth):
	Y_predict = [item for sublist in y_predict for item in sublist]
	Y_truth = [item for sublist in y_truth for item in sublist]
	return count_tp_tokens(Y_truth, Y_predict)
