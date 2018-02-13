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

global size,current,cancel
current = 0
size = 1

cancel = False

def resetGlobal():
    global size,current,cancel
    current = 0
    size = 1
    cancel = False


def addScrapParseToDB():
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
    gameNumber = DBhandler.getGameNumber()
    game="https://app.roll20.net/editor/setcampaign/"+gameNumber

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
            browser.get(game)
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
    else:
        c = soup.find("div", {"data-messageid": lastMessage})
        chatContent = soup.findAll("div", {"class": generalmatch})
        chatContent = chatContent[chatContent.index(c) + 1:]
        size = len(chatContent)

    addToDb(chatContent)

# get the chat content from a path
def addParseToDB(path):
    with open(path, encoding='utf8') as infile:
        soup = BeautifulSoup(infile, "html.parser") # make soup that is parse-able by bs

    infile.close()

    generalmatch = re.compile('message \w+')

    global size
    lastMessage = DBhandler.getlastMessage()
    if isinstance(lastMessage, type(None)):
        chatContent = soup.findAll("div", {"class": generalmatch})
        size = len(chatContent)
    else:
        c = soup.find("div", {"data-messageid": lastMessage})
        chatContent = soup.findAll("div", {"class": generalmatch})
        chatContent = chatContent[chatContent.index(c) + 1:]
        size = len(chatContent)
    addToDb(chatContent)


class static:
    by = ""
    tstamp = ""
    timeStamp = ""
    photo = ""


def updatePhoto(content):
    childen = content.findChildren()
    for c in childen:
        if not isinstance(c, type(None)):
            p = str(c.attrs.get("src"))
            last = p.rfind("/")
            static.photo = p[:last]



#roll20 has 3 types of messages this sorts them and adds them to the db
def addToDb(chatContent):
    global current,cancel
    static.timeStamp = ""
    x =1
    for c in chatContent:
        if(not cancel):
            current = x
            test = c.attrs.get("data-messageid")
            print(test)
            #print(DBhandler.getActiveTagsNames())
            s = c["class"]
            if "rollresult" in s:
                addRollresult(c)
            elif "general" in s:
                addGeneral(c)
            elif "emote" in s:
                addEmote(c)
            else:
                print("unknown message type: ", c)
            x += 1
        else:
            print("chatPar has been canceled")
            return

#adds the rollresults messages to the DB
#Also links active tags to the message ID
def addRollresult(datum):
    playerID = datum.attrs.get("data-playerid")
    messageID = datum.attrs.get("data-messageid")
    dicerolls = ""
    fromula = ""
    roll = ""

    for content in datum.contents:
        if isinstance(content, Tag):
            s = content.attrs.get("class")
            if not isinstance(s, type(None)):

                if "by" in s:
                    static.by = content.text
                elif "tstamp" in s:
                    addTime(content.text)
                elif "avatar" in s:
                    updatePhoto(content)

                elif "formula" in s:
                    if "formattedformula" in s:
                        dicerolls = getDiceRolls(content.findChildren())
                    else:
                        fromula = content.text.strip()
                elif "rolled" in s:
                    roll = content.text.strip()

    messageType = 'rollresult'
    avatar = static.photo
    by = static.by
    time = static.tstamp

    DBhandler.addRollResult(messageID,messageType,avatar,playerID,by,dicerolls,fromula,roll,time)


# find a way to get the roll data
# right now the only way to get that data is to load in the game
# stores MessageID, by, time, timeadd to DB
# todo consider adding message text to the databace. right now the info stored is limited
def addGeneral(datum):
    message = dict.fromkeys(DBhandler.columnName, "")
    messageID = datum.attrs.get("data-messageid")
    dateAddToDb = datetime.now()
    charSheet = False
    for content in datum.contents:
        if isinstance(content, Tag):
            s = content.attrs.get("class")
            if not isinstance(s, type(None)):

                if "by" in s:
                    static.by = content.text
                elif "tstamp" in s:
                    addTime(content.text)
                elif "avatar" in s:
                    updatePhoto(content)

                elif any("sheet-rolltemplate" in c for c in s):
                    charSheet = True
                    char = content


    if charSheet:
        message[DBhandler.MessageID_field] = messageID
        message[DBhandler.Avatar_field] = static.photo
        message[DBhandler.By_field] = static.by
        message[DBhandler.Time_field] = static.tstamp
        message[DBhandler.TimeAddedToDB_field] = dateAddToDb


        charSheetRoll(char, message)
    else:
        #todo get rid of below code, why keep useless data
        message[DBhandler.MessageType_field] = 'general'
        message[DBhandler.MessageID_field] = messageID
        message[DBhandler.Avatar_field] = static.photo
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
                if "avatar" in s:
                    updatePhoto(content)

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
            DBhandler.addTagActive(tagName, tagType, tagDetails, static.photo, self)

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
                DBhandler.addTagActive(tagName, tagType, tagDetails,static.photo, self)

            elif "start" in td:
                tagType = "indefinite"
                tagDetails = [static.tstamp]
                DBhandler.addTagActive(tagName, tagType, tagDetails,static.photo, self)


            elif "end" in td:
                if 'endall' in td:
                    DBhandler.endAlltag()
                else:
                    DBhandler.endtag(tagName)
            elif "self" in td:
                tagType = "single"
                tagDetails = [static.tstamp]
                self = False
                DBhandler.addTagActive(tagName, tagType, tagDetails,static.photo, self)

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
                DBhandler.addTagActive(tagName, tagType, tagDetails,static.photo, self)

            elif "start" in td:
                tagType = "indefinite"
                tagDetails = [static.tstamp]
                DBhandler.addTagActive(tagName, tagType, tagDetails,static.photo, self)


            elif "end" in td:
                if 'endall' in td:
                    DBhandler.endAlltag()
                else:
                    DBhandler.endtag(tagName)


            else:
                tagType = "single"
                tagDetails = [static.tstamp]
                self = False
                DBhandler.addTagActive(tagName, tagType, tagDetails,static.photo, self)

    message[DBhandler.MessageType_field] = 'emote'
    message[DBhandler.MessageID_field] = messageID
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

#todo make this return [side,crit,roll,type]
def getDiceRolls(contents):
    rlist = list()
    for c in contents:
        s = c.attrs.get("class")
        if not isinstance(s, type(None)):
            if any("diceroll" in t for t in s):
                for con in s:



                    if "crit" in con:
                        crit = con
                    elif re.match("[a-zA-Z_]\d+",con) is not None:
                        type = re.search("[a-zA-Z_]",con)
                        side = re.search("\d+",con)
                roll = c.text

                rlist.append([side,crit,roll,type])

    return rlist

def charSheetRoll(content,message):
    childContent = content.findChildren()
    for cc in childContent:
        ccClass = cc.attrs.get("class")
        if not isinstance(ccClass,type(None)):
            if any("inlinerollresult" in t for t in ccClass):

                ccTitle = cc.attrs.get("title")
                roll = cc.text
                soup = BeautifulSoup(ccTitle, 'html.parser')

                rollResults_Formula = parseCharterSheetroll(soup)

                if rollResults_Formula is None:
                    print(message["MessageID"])
                    #may make continue
                    continue

                rollResults = rollResults_Formula[0]
                formula = rollResults_Formula[1]

                message[DBhandler.MessageType_field] = 'characterSheet'
                message[DBhandler.RolledResultsList_field] = rollResults
                message[DBhandler.RolledFormula_field] = formula
                message[DBhandler.totalRolled_Field] = roll
                message[DBhandler.Time_field] = static.tstamp

                DBhandler.addtag(message[DBhandler.MessageID_field], None ,static.tstamp)
                DBhandler.addMessage(message)

def parseCharterSheetroll(soup):
    dicerolls = list()
    crit = list()
    for s in soup.contents:
        test = str(s)
        if "rolling" in str(s).lower():
            formula = str(s).split("=")[0]
            reg = re.search("\d+d\d+", formula)

            if reg is None:
                print("unkown formula")
                print(formula)
                return None
            else:
                side = reg.group(0).split("d")[-1]
                side = "d" + side

        if "basicdiceroll" in str(s).lower():
            dicerolls.append(s.text)
            if len(s.attrs["class"]) >= 3:
                crit.append(s.attrs["class"][1])
            else:
                crit.append("")

    sides = [side] * len(dicerolls)
    rollResults = list(zip(sides, crit, dicerolls))

    return [rollResults,formula]

def cancelParser():
    global cancel
    cancel = True