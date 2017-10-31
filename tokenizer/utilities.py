from io import BytesIO, StringIO
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
