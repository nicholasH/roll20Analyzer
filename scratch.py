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

today = date.today()

now = datetime.now()


print(now)

messageDic = {DBhandler.MessageID_field:"messageID92834509",
              DBhandler.MessageType_field:"Roll",
              DBhandler.UserID_field: "User234808230",
              DBhandler.By_field: "bubbles",
              DBhandler.Avatar_field: "Avatar34",
              DBhandler.Time_field:now,
              DBhandler.TimeAddedToDB_field:today,
              DBhandler.RolledFormula_field: "3D5",
              DBhandler.RolledResultsList_field:[1,2,3,5],
              DBhandler.Rolled_Field:13,
              DBhandler.Text_Field: "textrolL"}

DBhandler.destroyDB()
DBhandler.createDB()



DBhandler.getMessages()



#-Kirdj3MZgeVxKmBBgT_