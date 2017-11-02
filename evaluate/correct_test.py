from evaluation import *
x_predict, y_predict = get_data('../tokenizer/crf/val_predict.txt') 
x_truth, y_truth = get_data("../tokenizer/crf/val_true.txt")
X_predict = [item for sublist in x_predict for item in sublist]
X_truth = [item for sublist in x_truth for item in sublist]
def test_correctness():
	for i in range(len(X_predict)):
		if(X_predict[i] != X_truth[i]):
			return i
			break

i = test_correctness()
print(i)
print(''.join(X_predict[i:i+40]))
print(''.join(X_truth[i:i+40]))
print("\n")
print(X_truth[i-5:i+10])
print(X_predict[i-5:i+10])