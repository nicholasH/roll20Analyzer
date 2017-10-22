import random
import sqlite3
from datetime import datetime, date, timedelta

import pickle


def creatDB():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE test
                 (id INTEGER PRIMARY KEY,name text, test text)''')

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

tr =  str(random.randint(1,100))
lol = ""
testlol = 'tswo'
c.execute('INSERT INTO test (name,test) VALUES (?,?)', (tr,lol))
c.execute('UPDATE test SET test = (?) WHERE test = ""',(testlol,) )
c.execute("SELECT name FROM test WHERE test = (?)", (testlol,))



rows = c.fetchall()
for row in rows:
    print(row)

conn.commit()
conn.close()


print(rows)



printDB()