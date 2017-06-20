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
Message_table = 'Message'

DBhandler.createDB()
con = sqlite3.connect('Chatlog.db')
cursor = con.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

conn = sqlite3.connect('Chatlog.db')
c = conn.cursor()
print('DROP TABLE IF EXISTS ' + Message_table)
c.execute('DROP TABLE IF EXISTS ' + Message_table)
conn.commit()
conn.close()
