import sqlite3
from sqlite3 import Error

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

db_file = 'posts/2008Posts.db' 
db_conn = create_connection(db_file)
cursor = db_conn.cursor()

#Sample testing code
cursor.execute('''SELECT COUNT(Id) FROM posts''')
r = cursor.fetchone()
print(tuple(r))

cursor.execute('''SELECT * FROM posts''')
r = cursor.fetchone()
print(tuple(r))

