import os

import sys

import DBhandler
import analyze
name = "jarredgame"
url = "https://app.roll20.net/campaigns/chatarchive/1610304"

DBhandler.setDB(name)
print(DBhandler.getDBPath())

DBhandler.destroyDB()
DBhandler.createDB(name,url)
DBhandler.printDBData()
print(DBhandler.getURL())

url = DBhandler.getURL()

print(analyze.analyze())

name2 = "testGame"
url2 ="https://app.roll20.net/campaigns/chatarchive/1644807"
DBhandler.setDB(name2)
DBhandler.createDB(name2,url2)
print(analyze.analyze())


DBhandler.printDBData()

