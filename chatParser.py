import os
import re
from datetime import datetime, timedelta
import sys

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException, TimeoutException
import selenium.webdriver.support.ui as ui

import DBhandler

#todo have user define stamped
global stamped
stamped = False

global size,current
current = 0
size = 1


def getScrapParse():
    # todo remove code
    # DBhandler.destroyDB()
    # DBhandler.createDB()
    # todo remove above code



    URL = 'https://app.roll20.net/sessions/new'

    gameURL = DBhandler.getURL()

    chromeDriver = os.path.join(sys.path[0], "chromedriver.exe")
    browser = webdriver.Chrome(chromeDriver)
    # browser.set_window_size(20, 20)
    # browser.set_window_position(50, 50)
    browser.get(URL)

    wait = ui.WebDriverWait(browser, 120)  # timeout after 120 seconds

    # todo remove this login
    # Loging
    ######################################################################################

    path = os.path.join(sys.path[0], "config.txt")

    f = open(path)
    EMAIL = ''
    PASSWORD = ''
    for line in f:
        if "Email:" in line:
            EMAIL = line.split("Email:")[1].strip()
        if "Password:" in line:
            PASSWORD = line.split("Password:")[1].strip()

    f.close()
    
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
            browser.get(gameURL)
            html = browser.page_source
            browser.close()
        else:
            print("error website changes")
    except TimeoutException:
        browser.close()
        print("error timeout")

    soup = BeautifulSoup(html, 'html.parser')  # make soup that is parse-able by bs
    generalmatch = re.compile('message \w+')

    global size
    lastMessage = DBhandler.getlastMessage()
    if isinstance(lastMessage, type(None)):
        chatContent = soup.findAll("div", {"class": generalmatch})
        size = len(chatContent)
        return chatContent
    else:
        c = soup.find("div", {"data-messageid": lastMessage})
        chatContent = soup.findAll("div", {"class": generalmatch})
        chatContent = chatContent[chatContent.index(c) + 1:]
        size = len(chatContent)
        return chatContent


# get the chat content from a path
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
                        elif chTime < firstTime - timedelta(seconds=hoursBack):
                            return chatContent[len(chatContent) - index:]
    return chatContent



#Gets a path to a file and 2 date strings to return a subset of the parsed data
def getParseTimeRange(date1String, date2String):
    # chatContent = getParse(path)
    chatContent = getScrapParse()
    date1 = datetime.strptime(date1String, '%m %d %Y')
    date2 = datetime.strptime(date2String, '%m %d %Y')

    startMessageIndex = 0
    startFound = False
    endMessageIndex = len(chatContent)
    lastDateFound = ""

    if date2.date() < date1.date():
        return chatContent[startMessageIndex: endMessageIndex]

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
                            return chatContent[startMessageIndex: endMessageIndex]

    return chatContent[startMessageIndex: endMessageIndex]


class static:
    by = ""
    tstamp = ""
    timeStamp = ""

#roll20 has 3 types of messages this sorts them and adds them to the db
def addToDb():
    global current
    chatContent = getScrapParse()
    static.timeStamp = ""
    x =0
    for c in chatContent:
        current = x
        print(DBhandler.getActiveTagsNames())
        s = c["class"]

        if "rollresult" in s:
            addRollresult(c)
            pass
        elif "general" in s:
            addGeneral(c)
        elif "emote" in s:
            addEmote(c)
            pass
        else:
            print("unknown message type: ", c)
        x += 1

#adds the rollresults messages to the DB
#Also links active tags to the message ID
def addRollresult(datum):
    message = dict.fromkeys(DBhandler.columnName, "")
    playerID = datum.attrs.get("data-playerid")
    messageID = datum.attrs.get("data-messageid")
    photo = ""
    dicerolls = ""
    dice = ""
    roll = ""
    dateAddToDb = datetime.now()

    for content in datum.contents:
        if isinstance(content, Tag):
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

    DBhandler.addtag(messageID, playerID,static.tstamp)
    DBhandler.addMessage(message)


# find a way to get the roll data
# right now the only way to get that data is to load in the game
# stores MessageID, by, time, timeadd to DB
# todo consider adding message text to the databace. right now the info stored is limited
def addGeneral(datum):
    message = dict.fromkeys(DBhandler.columnName, "")
    messageID = datum.attrs.get("data-messageid")
    dateAddToDb = datetime.now()

    for content in datum.contents:
        if isinstance(content, Tag):
            s = content.attrs.get("class")
            if not isinstance(s, type(None)):

                if "by" in s:
                    static.by = content.text
                elif "tstamp" in s:
                    addTime(content.text)

    message[DBhandler.MessageType_field] = 'general'
    message[DBhandler.MessageID_field] = messageID
    message[DBhandler.By_field] = static.by
    message[DBhandler.Time_field] = static.tstamp
    message[DBhandler.TimeAddedToDB_field] = dateAddToDb

    DBhandler.addMessage(message)


# adds emote to the database
# finds emotes with tag and adds the tags to the active tag table
# stores MessageID, time, timeadd to DB
# todo consider adding message text to the databace. right now the info stored is limited
def addEmote(datum):
    for content in datum.contents:
        if isinstance(content, Tag):
            s = content.attrs.get("class")
            if not isinstance(s, type(None)):

                if "by" in s:
                    static.by = content.text
                elif "tstamp" in s:
                    addTime(content.text)

    message = dict.fromkeys(DBhandler.columnName, "")
    messageID = datum.attrs.get("data-messageid")
    dateAddToDb = datetime.now()

    emote = datum.text.lower()
    if "#ts" in emote:
        match = re.search(r'\d{2}/\d{2}/\d{4}', datum.text)
        date = datetime.strptime(match.group(), '%m/%d/%Y')
        static.timeStamp = date
    regex = r'\^\w+( *-+\w+){0,2}'

    m = re.search(regex, datum.text)

    if m is not None:
        tagData = m.group().split("-")

        if len(tagData) == 1:
            tagName = tagData[0].replace("^", "").strip()
            tagType = "single"
            tagDetails = [static.tstamp]
            self = False
            DBhandler.addTagActive(tagName, tagType, tagDetails, self)

        elif len(tagData) == 2:
            td = tagData[1].lower()
            tagName = tagData[0].replace("^", "").strip()
            self = False

            timeRegex = re.search(r'\d+(h|m)', td)
            if timeRegex is not None:
                timeNum = td[:-1]
                timeType = td[-1:]
                tagDetails = ["", timeNum, timeType]#[startTime,Number of hours/min,hours or min]#startTime is time of the next roll
                tagType = "timed"
                DBhandler.addTagActive(tagName, tagType, tagDetails, self)

            elif "start" in td:
                tagType = "indefinite"
                tagDetails = [static.tstamp]
                DBhandler.addTagActive(tagName, tagType, tagDetails, self)


            elif "end" in td:
                if 'endall' in td:
                    DBhandler.endAlltag()
                else:
                    DBhandler.endtag(tagName)
            elif "self" in td:
                tagType = "single"
                tagDetails = [static.tstamp]
                self = False
                DBhandler.addTagActive(tagName, tagType, tagDetails, self)

            else:
                print("bad tag: ", m.group())

        elif len(tagData) == 3:
            td = tagData[1].lower()
            tagName = tagData[0].replace("^", "").strip()
            self = 'self' in tagData[2]

            if "self" in td:
                td = tagData[2].lower()
                self = 'self' in tagData[1]

            timeRegex = re.search(r'\d+(h|m)', td)
            if timeRegex is not None:
                timeNum = td[:-1]
                timeType = td[-1:]
                tagDetails = ["", timeNum, timeType]#[startTime,Number of hours/min,hours or min]#startTime is time of the next roll
                tagType = "timed"
                DBhandler.addTagActive(tagName, tagType, tagDetails, self)

            elif "start" in td:
                tagType = "indefinite"
                tagDetails = [static.tstamp]
                DBhandler.addTagActive(tagName, tagType, tagDetails, self)


            elif "end" in td:
                if 'endall' in td:
                    DBhandler.endAlltag()
                else:
                    DBhandler.endtag(tagName)


            else:
                tagType = "single"
                tagDetails = [static.tstamp]
                self = False
                DBhandler.addTagActive(tagName, tagType, tagDetails, self)

    message[DBhandler.MessageType_field] = 'emote'
    message[DBhandler.MessageID_field] = messageID
    message[DBhandler.Time_field] = static.tstamp
    message[DBhandler.TimeAddedToDB_field] = dateAddToDb

    DBhandler.addMessage(message)


# adds time tstamp to the static class
# first trys a (Month day, year time) if that fails it takes todays date and just takes the time that it gets from the given time
#stamped is unimplemented, it is away to set the date for the chat by the user
def addTime(timeString):
    try:
        static.tstamp = datetime.strptime(timeString, "%B %d, %Y %I:%M%p")

    except ValueError:
        try:
            hourDt = datetime.strptime(timeString, "%I:%M%p")

            if stamped:
                if static.timeStamp == "":
                    static.tstamp = None
                else:
                    date = static.timeStamp
                    date.replace(hour=hourDt.hour, minute=hourDt.minute)
                    static.tstamp = date
            else:
                today = datetime.today()
                today = today.replace(hour=hourDt.hour, minute=hourDt.minute)
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
            if any("diceroll" in t for t in s):
                dice = ' '.join(s)
                roll = c.text
                rlist.append([dice, roll])

    return rlist