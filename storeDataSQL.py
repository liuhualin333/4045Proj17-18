import sqlite3
from sqlite3 import Error
from bs4 import BeautifulSoup
 

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def create_table(db_conn):
	cursor = db_conn.cursor()
	try:
		cursor.execute('''
			CREATE TABLE posts(
				Id INTEGER PRIMARY KEY,
				CreationDate TEXT,
				Score INTEGER,
				ViewCount INTEGER,
				Body TEXT,
				Title TEXT,
				Tags TEXT,
				AnswerCount INTEGER,
				CommentCount INTEGER,
				FavoriteCount INTEGER
			)''')
		cursor.execute('''
			CREATE TABLE answers(
				Id INTEGER PRIMARY KEY,
				ParentId INTEGER,
				CreationDate TEXT,
				Score INTEGER,
				Body TEXT,
				CommentCount INTEGER,
				FOREIGN KEY (ParentId) REFERENCES posts(Id)
			)''')
		db_conn.commit()
	except Error as e:
		print(e)


db_file = 'posts/2008Posts.db' 
db_conn = create_connection(db_file)
create_table(db_conn)
cursor = db_conn.cursor()

with open("posts/2008Posts.xml") as infile:
	for line in infile:
		soup = BeautifulSoup(line, features="xml")
		for row in soup.find_all('row'):
			try:
				if (row['PostTypeId'] == '1'):
					cursor.execute('''
						INSERT INTO posts(Id,CreationDate,Score,
							ViewCount,Body,
							Title,Tags,
							AnswerCount,CommentCount,FavoriteCount) VALUES 
						(?,?,?,?,?,?,?,?,?,?)''',\
						(int(row['Id']),\
					 	row['CreationDate'],\
					 	#int(row['AcceptedAnswerId']),\
					 	int(row['Score']),\
					 	int(row['ViewCount']),\
					 	row['Body'],\
					 	#int(row['OwnerUserId']),\
					 	#row['LastActivityDate'],\
					 	row['Title'],\
					 	row['Tags'],\
					 	int(row['AnswerCount']),\
					 	int(row['CommentCount']),\
					 	int(row['FavoriteCount']))
						)
				elif (row['PostTypeId'] == '2'):
					cursor.execute('''
						INSERT INTO answers(Id,ParentId,CreationDate,Score,Body,
						CommentCount) VALUES 
						(?,?,?,?,?,?)''',\
						(int(row['Id']),
						int(row['ParentId']),\
						row['CreationDate'],\
				 		int(row['Score']),\
				 		row['Body'],\
				 		#int(row['OwnerUserId']),\
				 		#int(row['LastEditorUserId']),\
				 		#row['LastEditDate'],\
				 		#row['LastActivityDate'],\
				 		int(row['CommentCount'])))
				db_conn.commit()
			except:
				print(line)
db_conn.close()