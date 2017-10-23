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
def creatDB2():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE test2
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
    print("db1")
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("SELECT * FROM test")
    conn.commit()
    rows = c.fetchall()
    for row in rows:
        print(row)

    conn.close()
def printDB2():
    print("db2")
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("SELECT * FROM test2")
    conn.commit()
    rows = c.fetchall()
    for row in rows:
        print(row)

    conn.close()


#dis()
#creatDB()
#creatDB2()
testname = [('bill'),
            ('tom'),
            ('kyle'),
            ('tom'),]

conn = sqlite3.connect('example.db')
c = conn.cursor()

tr =  str(random.randint(1,10))
tr1 = str(random.randint(1,10))
lol = "lol"
testlol = 'tswo'
#c.execute('INSERT INTO test (name,test) VALUES (?,?)', (tr,lol))
#c.execute('INSERT INTO test2 (name,test) VALUES (?,?)', (tr1,lol))

c = conn.cursor()
c.execute("SELECT test.id, test.name, test.test FROM test "
          "JOIN test2 "
          "ON test.name = test2.name "
          "WHERE test2.test = (?)", ("lol",)
          )
data = c.fetchall()
conn.commit()
conn.close()
printDB()
printDB2()
print("data")
for da in data:
    print(da)