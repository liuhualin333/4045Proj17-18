from bs4 import BeautifulSoup
from datetime import datetime

basetime = datetime.strptime('2008-01-01T00:00:00.997656', "%Y-%m-%dT%H:%M:%S.%f")
postList = {}
f = open('posts/2008Posts.xml', 'w')
with open("posts/Posts.xml") as infile:
	i = 0
	for line in infile:
		if i > 1000:
			f.close()
			break
		soup = BeautifulSoup(line, features="xml")
		if (len(soup.find_all('row'))!=0):
			for row in soup.find_all('row'):
				if (datetime.strptime(row["CreationDate"], "%Y-%m-%dT%H:%M:%S.%f") > basetime):
					if (row['PostTypeId'] == '1' \
						and "python" in row['Tags'] \
						and int(row["AnswerCount"]) > 3 \
						and int(row["ViewCount"]) > 200000):
						print(line)
						postList[row["Id"]] = int(row["AnswerCount"])
						f.write(line)
						i+=1
					if (row['PostTypeId'] == '2' \
						and row['ParentId'] in postList.keys()):
						print(line)
						postList[row['ParentId']] -= 1
						f.write(line)
						if (postList[row['ParentId']] <= 0):
							del postList[row['ParentId']]