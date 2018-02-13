import random
import sqlite3
from datetime import datetime, date, timedelta
import time

import pickle

import DBhandler


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
    time.sleep(3)
    scratch.update("test")
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

def cDB():

    DBhandler.createDB("name","https://app.roll20.net/campaigns/chatarchive/1644807")


global x
x = 0
global max
maax = 1000000

def countToMax():
    global x,maax
    while(x<maax):
        x += 1
        print(x)





cDB()

"""
#dis()
#creatDB()
#creatDB2()
testname = [('bill'),
            ('tom'),
            ('kyle'),
            ('tom'),]
#conn = sqlite3.connect('example.db')

conn = sqlite3.connect('C:\\Users\\Nick\\Documents\\GitHub\\roll20Analyzer\\data\\dataBase\\test.db')
c = conn.cursor()
tag = "-Kz2334kdVOUgwyno4mX"
c.execute("SELECT Message.* FROM Message JOIN Tags ON Message.MessageID = Tags.MessageID WHERE Time BETWEEN '2017-11-27' AND '2017-12-27'")

conn.commit()
data = c.fetchall()
conn.close()

for d in data:
    print(d)
    
"""
