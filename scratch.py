import os
import re
import time

import sys
from telnetlib import EC

from aiohttp.hdrs import PRAGMA
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException
import sqlite3
from datetime import datetime, date,timedelta
import pickle

from selenium.webdriver.support.wait import WebDriverWait

import  DBhandler



def getDate():
    messages = DBhandler.getMessageDateTime(datetime(2017,7,10))

    for message in messages:
        print(message)


getDate()
#DBhandler.printDB()

