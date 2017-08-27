import os
import re
from datetime import datetime, timedelta
import time

import sys
from telnetlib import EC

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException, TimeoutException
import selenium.webdriver.support.ui as ui

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import DBhandler

#todo make this able to chanced by the user
global stamped
stamped = True


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

    wait = ui.WebDriverWait(browser, 120)  # timeout after 120 seconds


    #todo remove this login
    #Loging
    ######################################################################################
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
    #######################################################################################

    try:
        results = wait.until(lambda driver: driver.find_elements_by_class_name('loggedin'))

        if len(results) > 0:
            browser.get(testUrl)
            html = browser.page_source
            browser.close()
        else:
            print("error website changes")
    except TimeoutException:
        browser.close()
        print("error timeout")


    soup = BeautifulSoup(html, 'html.parser')  # make soup that is parse-able by bs
    generalmatch = re.compile('message \w+')

    lastMessage = DBhandler.getlastMessage()
    if isinstance(lastMessage,type(None)):
        chatContent = soup.findAll("div", {"class": generalmatch})
        return chatContent
    else:
        c = soup.find("div", {"data-messageid": lastMessage})
        chatContent = soup.findAll("div", {"class": generalmatch})
        return chatContent[chatContent.index(c)+1:]





def getParse(path):
    f = open(path)
    soup = BeautifulSoup(f.read(), 'html.parser')  # make soup that is parse-able by bs
    f.close()
    generalmatch = re.compile('message \w+')

    chatContent = soup.findAll("div", {"class": generalmatch})

    return chatContent

'''
gets a path to a file and a hour number returns a subset of the parsed data
that inclueds data between the first message how many hours befor the first message

This is a bad solution to roll 20 not showing a date for time stamps
'''
def getParseRollbackHours(path, hoursBack):
    chatContent = getParse(path)
    hoursBack = hoursBack * 3600
    first = True
    firstTime = ""

    for index, chat in enumerate(reversed(chatContent)):
        for ch in chat.contents:
            if not isinstance(ch, NavigableString):
                s = ch.attrs.get("class")
                if not isinstance(s, type(None)):
                    if any("tstamp" in f for f in s):
                        timeSplit = ch.string.split()
                        time = timeSplit.pop()
                        chTime = datetime.strptime(time, '%I:%M%p')

                        if first:
                            firstTime = chTime
                            first = False
                        elif chTime < firstTime - timedelta(seconds = hoursBack):
                            return chatContent[len(chatContent) - index:]
    return chatContent

'''
Gets a path to a file and 2 date strings to return a subset of the parsed data

This code is was broken since march 18 2017 roll20 now only shows the time in the roll not the full date
'''
def getParseTimeRange( date1String, date2String):
    #chatContent = getParse(path)
    chatContent = getScrapParse()
    date1 = datetime.strptime(date1String, '%m %d %Y')
    date2 = datetime.strptime(date2String, '%m %d %Y')

    startMessageIndex = 0
    startFound = False
    endMessageIndex = len(chatContent)
    lastDateFound = ""

    if date2.date() < date1.date():
        return chatContent[startMessageIndex : endMessageIndex]

    for index, chat in enumerate(chatContent):
        for ch in chat.contents:
            if not isinstance(ch, NavigableString):
                s = ch.attrs.get("class")
                if not isinstance(s, type(None)):
                    if any("tstamp" in f for f in s):
                        try:
                            chDate = datetime.strptime(ch.string, '%B %d, %Y %I:%M%p')
                            lastDateFound = chDate
                        except ValueError:
                            chDate = lastDateFound

                        if chDate.date() >= date1.date() and not startFound:
                            startMessageIndex = index
                            startFound = True
                        if date2.date() < chDate.date():
                            endMessageIndex = index - 1
                            return chatContent[startMessageIndex : endMessageIndex]

    return chatContent[startMessageIndex : endMessageIndex]



class static:
    by = ""
    tstamp = ""
    timeStamp = ""




def addToDb():
    chatContent = getScrapParse()
    static.timeStamp = ""
    for c in chatContent:

        s = c["class"]

        if "rollresult" in s:
            addRollresult(c)
            pass
        elif "general" in s:
            addGleneral(c)
        elif "emote" in s:
            addEmote(c)
            pass
        else:
            print("unknown message type")





def addRollresult(datum):
    message = dict.fromkeys(DBhandler.columnName, "")
    playerID = datum.attrs.get("data-playerid")
    messageID = datum.attrs.get("data-messageid")
    photo = ""
    dicerolls=""
    dice = ""
    roll = ""
    dateAddToDb = datetime.now()

    for content in datum.contents:
        if isinstance(content,Tag):
            s = content.attrs.get("class")
            if not isinstance(s, type(None)):

                if "by" in s:
                    static.by = content.text
                elif "tstamp" in s:
                    addTime(content.text)

                elif "formula" in s:
                    if "formattedformula" in s:
                        dicerolls = getDiceRolls(content.findChildren())
                    else:
                        dice = content.text.strip()
                elif "rolled" in s:
                    roll = content.text.strip()

    message[DBhandler.MessageType_field] = 'rollresult'
    message[DBhandler.MessageID_field] = messageID

    message[DBhandler.UserID_field] = playerID
    message[DBhandler.By_field] = static.by
    message[DBhandler.RolledResultsList_field] = dicerolls
    message[DBhandler.RolledFormula_field] = dice
    message[DBhandler.Rolled_Field] = roll
    message[DBhandler.Time_field] = static.tstamp
    message[DBhandler.TimeAddedToDB_field] = dateAddToDb

    print("test",playerID,messageID,static.by,static.tstamp,"|",dateAddToDb,dicerolls,dice.strip(),roll,)


    DBhandler.addMessage(message)



#find a way to get the roll data
#right now the only way to get that data is to load in the game
def addGleneral(datum):
    for content in datum.contents:
        if isinstance(content,Tag):
            s = content.attrs.get("class")
            if not isinstance(s, type(None)):

                if "by" in s:
                    static.by = content.text
                elif "tstamp" in s:
                    addTime(content.text)


def addEmote(datum):
    ts = datum.text.lower()
    if "#ts" in ts:
        match = re.search(r'\d{2}/\d{2}/\d{4}', datum.text)
        date = datetime.strptime(match.group(), '%m/%d/%Y')
        static.timeStamp =date
    for content in datum.contents:
        if isinstance(content,Tag):
            s = content.attrs.get("class")
            if not isinstance(s, type(None)):

                if "by" in s:
                    static.by = content.text
                elif "tstamp" in s:
                    addTime(content.text)

#adds time tstamp to the static class
#first trys a (Month day, year time) if that fails it takes todays date and just takes the time that it gets from the given time
def addTime(timeString):

    try:
        static.tstamp = datetime.strptime(timeString, "%B %d, %Y %I:%M%p")

    except ValueError:
        try:
            hourDt = datetime.strptime(timeString, "%I:%M%p")

            if stamped:
                if static.timeStamp == "":
                    static.tstamp =None
                else:
                    date = static.timeStamp
                    date.replace(hour=hourDt.hour, minute=hourDt.minute)
                    static.tstamp = date
            else:
                today = datetime.today()
                today.replace(hour=hourDt.hour, minute=hourDt.minute)
                static.tstamp = today
                print("not full time string" + timeString)









        except ValueError:
            print("Error Time " + timeString)
            static.tstamp = None



def getDiceRolls(contents):
    rlist = list()
    for c in contents:
        s = c.attrs.get("class")
        if not isinstance(s, type(None)):
            if any("diceroll" in t for t in s ):
                dice = ' '.join(s)
                roll = c.text
                rlist.append([dice,roll])

    return rlist



"""
 for content in contents:
        if not isinstance(content, NavigableString):
            s = content.attrs.get("class")
            if not isinstance(s, type(None)):
                if any("dicegrouping" in t for t in s):
                    diceRolls = content.contents
                    print("log")
"""
