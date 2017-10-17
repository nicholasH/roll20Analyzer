import sqlite3
from datetime import datetime, date, timedelta

import pickle


def creatDB():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE test
                 (id INTEGER PRIMARY KEY,name text)''')

    conn.commit()
    conn.close()

def dis():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS test')

    conn.commit()
    conn.close()

def printDB():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("SELECT * FROM test")
    conn.commit()
    rows = c.fetchall()
    for row in rows:
        print(row)

    conn.close()
#dis()
#creatDB()
print("end")
testname = [('bill'),
            ('tom'),
            ('kyle'),
            ('tom'),]

conn = sqlite3.connect('example.db')
c = conn.cursor()

day = datetime.today()
testlist = [day,"1","M"]

print(testlist)

t =pickle.dumps(testlist)


print(pickle.loads(t))

tr = t
c.execute('INSERT INTO test (name) VALUES (?)', (tr,))

c.execute('SELECT name from test')

rows = c.fetchall()

conn.commit()
conn.close()


print(rows)



printDB()