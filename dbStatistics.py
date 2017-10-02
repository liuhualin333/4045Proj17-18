import sqlite3
from sqlite3 import Error
import matplotlib.pyplot as plt

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
cursor.execute('''SELECT answercount, count(id)  FROM posts group by answercount''')
r = cursor.fetchall()
print(tuple(r))

plt.figure()
x = [ele[0] for ele in list(r)]
y = [ele[1] for ele in list(r)]
plt.bar(x,y)
plt.xlabel('Answer count')
plt.ylabel('Number of posts')
plt.title('Distribution of answers for posts in database')
plt.savefig('AnswerDistribution(AnswerCount).png')
plt.show()

cursor.execute('''SELECT count(id) FROM posts''')
p = cursor.fetchone()
print(tuple(p))

cursor.execute('''SELECT count(id) FROM answers''')
a = cursor.fetchone()
print(tuple(a))

plt.figure()
labels = ['posts','answers']
x = [0,1]
y = [p[0],a[0]]
plt.bar(x, y, tick_label=labels)
for x, y in zip(x, y):
    plt.text(x, y + 0.1, '%d' % y, ha = 'center', va = 'bottom')
plt.xlabel('Categories')
plt.ylabel('Number of posts/answers')
plt.title('Count of answers/posts')
plt.savefig('Answers_Posts(Count).png')
plt.show()
