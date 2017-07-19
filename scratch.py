import os
import time

import sys

from aiohttp.hdrs import PRAGMA
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException
import sqlite3
from datetime import datetime, date,timedelta
import pickle
import  DBhandler
conn = sqlite3.connect('example.db')

def make():
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE stocks
                 (date text, trans text, symbol text, qty real, price real)''')

    # Insert a row of data
    c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    # Save (commit) the changes
    conn.commit()


def drop():
    c = conn.cursor()
    c.execute('''DROP TABLE stocks''')
def add():
    c = conn.cursor()
    x =0
    while x < 100:
        # Insert a row of data

        c.execute("INSERT INTO stocks VALUES ('2006-"+str(x)+"-05','BUY','RHAT',100,35.14)")
        x+=1
    conn.commit()


def printdb():
    c = conn.cursor()
    c.execute("SELECT * FROM stocks")
    conn.commit()
    print(c.fetchall())

DBhandler.printDB()
