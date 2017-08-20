import sqlite3
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.animation import Animation
from kivy.clock import Clock, mainthread
from kivy.uix.gridlayout import GridLayout
import threading
import time
import DBhandler

from datetime import datetime

day0 = datetime(2017,7,10)
day1 = datetime(2017,7,18)



def addToExample():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    x = 1
    while(x < 28):
        day = datetime(2017,7,x).strptime("")
        name = "NAME"+ str(x)
        exe = 'INSERT INTO NameDate VALUES (?,?);',(
            name,
            day
        )
        c.execute(exe)
    conn.commit()
    conn.close()


def createDB():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    exe = 'CREATE TABLE NameDate (Name STRING, Date date);'
    c.execute(exe)
    conn.commit()
    conn.close()

def destroyDB():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    exe = 'DROP TABLE IF EXISTS NameDate;'
    c.execute(exe)
    conn.commit()
    conn.close()


def printDB():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("SELECT * FROM NameDate;")
    conn.commit()
    rows = c.fetchall()
    for row in rows:
        print(row)

    conn.close()
DBhandler.printDB()
data = DBhandler.getMessageDateTime(day0)
print("=============================================================================")
for x in data:
    print(x)