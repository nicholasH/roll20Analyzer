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
#conn = sqlite3.connect('example.db')

conn = sqlite3.connect('E:\\GitProjects\\roll20Analyzer\\data\\dataBase\\jarredsGame.db')
c = conn.cursor()
tag = "-Kz2334kdVOUgwyno4mX"
c.execute("SELECT * FROM Message "
          "WHERE MessageID = (?)",(tag,))

conn.commit()
data = c.fetchall()
conn.close()
