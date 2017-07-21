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


#test -KQvQkIky9CA9LUmZUC8 -KpCjRGD9Zv1TU72jOl5 Nicholas H: (GM):
# July 16, 2017 4:23PM | 2017-07-20 19:23:41.502803

def get():
    s = DBhandler.getlastMessage()
    print(getScrapParse())
    print(s)




def getScrapParse():
    #todo remove code
    DBhandler.destroyDB()
    DBhandler.createDB()
    #todo remove above code


    path = os.path.join(sys.path[0], "config")

    f = open(path)
    EMAIL = ''
    PASSWORD = ''
    for line in f:
        if "Email:" in line:
            EMAIL = line.split("Email:")[1].strip()
        if "Password:" in line:
            PASSWORD = line.split("Password:")[1].strip()

    f.close()

    URL = 'https://app.roll20.net/sessions/new'
    jarUrl = 'https://app.roll20.net/campaigns/chatarchive/1610304'#todo take this out of hard code
    testUrl = "https://app.roll20.net/campaigns/chatarchive/1644807"


    chromeDriver = os.path.join(sys.path[0], "chromedriver.exe")
    browser = webdriver.Chrome(chromeDriver)
    #browser.set_window_size(20, 20)
    #browser.set_window_position(50, 50)
    browser.get(URL)

    try:
        WebDriverWait(browser, 5).until(EC.presence_of_element_located(
            browser.find_element_by_name('calltoaction')))
    except:
        print()


    usernameElements = browser.find_elements_by_name("email")
    passwordElements = browser.find_elements_by_name("password")

    for e in usernameElements:
        try:
            e.send_keys(EMAIL)
        except ElementNotVisibleException:
            print()

    for e in passwordElements:
        try:
            e.send_keys(PASSWORD)
        except ElementNotVisibleException:
            print()

    browser.find_element_by_class_name("calltoaction").click()
    browser.get(testUrl)
    try:
        WebDriverWait(browser, 5).until(EC.presence_of_element_located(
            browser.find_element_by_xpath('//*[@id="textchat"]/div')))
    except:
        print()

    html = browser.page_source
    browser.close()

    soup = BeautifulSoup(html, 'html.parser')  # make soup that is parse-able by bs

    generalmatch = re.compile('message \w+')
    g = re.compile('.')
    chatContent = soup.findAll("div", {"class": generalmatch})
    c = soup.findAll("div", {"data-messageid": "-KojdNK_7QMFvWL8b1dz"})



    return c

get()