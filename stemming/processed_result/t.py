try:
	cnt=0
	print(len(lst))
	print("error: "+str(cnt))
except (SyntaxError): 
	cnt+=1
	pass