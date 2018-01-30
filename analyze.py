import os
import sys
from collections import Counter

from datetime import datetime
import chatParser
import DBhandler
import re

global playerStats  # PlayerId:dict() states
playerStats = dict()

path = ""

real = ""
realDice = ["d4", "d6", "d10", "d12", "d20"]


# old method that use to be used to get html that the user downloaded
def getPath():
    path = ""
    # looks for the data in the data folder
    for file in os.listdir(os.path.join(sys.path[0], "data")):
        if file.endswith(".html") and file.startswith("Chat Log for"):
            path = os.path.join(sys.path[0], "data", file)

    return path


def analyze(offline):
    if not offline:
        chatParser.addScrapParseToDB()

    analyzeDB(DBhandler.getMessagesRoleresult())
    return returnStats()


def analyzeToday(offline):
    if not offline:
        chatParser.addScrapParseToDB()

    startToday = datetime(datetime.today().year, datetime.today().month, datetime.today().day)

    analyzeDB(DBhandler.getRollresultDateTime(startToday))
    return returnStats()


# Gets 1 Datetime and returns the messages of that date
def analyzeDate(date, offline):
    if not offline:
        chatParser.addScrapParseToDB()
    analyzeDB(DBhandler.getRollresultDateTime(date))
    return returnStats()


# Gets 2 datestimes and returns the messages between the dates
def analyzeDateRange(date0, date1, offline):
    if not offline:
        chatParser.addScrapParseToDB()
    analyzeDB(DBhandler.getRollresultDateTimeRange(date0, date1))
    return returnStats()


# get a tag name and return the messages with the tags
def analyzeByTag(tagName, offline):
    if not offline:
        chatParser.addScrapParseToDB()
    DBhandler.printTags()
    analyzeDB(DBhandler.getMessagesWithTags(tagName))
    return returnStats()


def analyzeByTagToday(tagName, offline):
    if not offline:
        chatParser.addScrapParseToDB()
    startToday = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    analyzeDB(DBhandler.getMessagesWithTagsBYDate(tagName, startToday))
    return returnStats()


def analyzeByTagDate(tagName, date, offline):
    if not offline:
        chatParser.addScrapParseToDB()
    analyzeDB(DBhandler.getMessagesWithTagsBYDate(tagName, date))
    return returnStats()


def analyzeByTagDateRange(tagName, date0, date1, offline):
    if not offline:
        chatParser.addScrapParseToDB()
    analyzeDB(DBhandler.getMessagesWithTagsBYDateRange(tagName, date0, date1))
    return returnStats()


# gets a players name and returns all the messages with that name
def analyzeByName(name, offline):
    if not offline:
        chatParser.addScrapParseToDB()
    analyzeDB(DBhandler.getMessagesByName(name))
    return returnStats()


def analyzeByNameToday(name, offline):
    if not offline:
        chatParser.addScrapParseToDB()
    startToday = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    analyzeDB(DBhandler.getMessagesByNameByDate(name, startToday))
    return returnStats()


def analyzeByNameByDate(name, date, offline):
    if not offline:
        chatParser.addScrapParseToDB()
    analyzeDB(DBhandler.getMessagesByNameByDate(name, date))
    return returnStats()


def analyzeByNameByDateRange(name, dateA, dateB, offline):
    if not offline:
        chatParser.addScrapParseToDB()
    analyzeDB(DBhandler.getMessagesByNameByDateRange(name, dateA, dateB))
    return returnStats()

#get name and a list of tags and returns all the messages that have all
#the list of tag name is for future feature
def analyzeByTagAndName(name, tagNameList, offline):
    if not offline:
        chatParser.addScrapParseToDB()
    analyzeDB(DBhandler.getMessagesByTagAndName(tagNameList, name))
    return returnStats()


def analyzeByTagAndNameToday(name, tagNameList, offline):
    if not offline:
        chatParser.addScrapParseToDB()
    startToday = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    analyzeDB(DBhandler.getMessagesByTagAndNameByDate(tagNameList, name, startToday))
    return returnStats()


def analyzeByTagAndNameByDate(name, tagNameList, date, offline):
    if not offline:
        chatParser.addScrapParseToDB()
    analyzeDB(DBhandler.getMessagesByTagAndNameByDate(tagNameList, name, date))
    return returnStats()


def analyzeByTagAndNameByDateRange(name, tagNameList, dateA, dateB, offline):
    if not offline:
        chatParser.addScrapParseToDB()
    analyzeDB(DBhandler.getMessagesByTagAndNameByDateRange(tagNameList, name, dateA, dateB))
    return returnStats()

def getGivenPath():
    return path

# todo make this look good
def returnStats():
    s = ""
    for player, values in playerStats.items():
        # s = s + player
        s = s + str(values["names"]) + " " + str(len(values["names"])) + "\n"
        s = s + "Total Number of Rolls " + str(sum(values["diceRolls"].values())) + "\n"
        s = s + str("Crit success: {}, Nat20: {}, Crit fail: {}, Nat1: {}".format(values["totCrtSus"], values["nat20"],
                                                                                  values["totCrtFail"],
                                                                                  values["nat1"])) + "\n"
        s = s + str(values["diceRolls"]) + "\n"
        s = s + "highest roll " + str(values["highestRoll"]) + "\n"
        s = s + "Top 5 Formual" + str(values["topFormual"].most_common(5)) + "\n"
        s = s + "points " + str(values["points"])
        s = s + ('\n\n')

    s = s + str(findWinner(""))+"\n\n"
    s = s +"Current Active Tags"+ str(DBhandler.getActiveTagsNames())
    s = s + "\n" + "#" * 100
    print(s)
    return s


# todo add in a way to excluded players like the DM
#finds the winner of the current search results
#gives 20 points to a player that wins a star
#ties are given to the player with the lower amount of total rolls
def findWinner(exclude):
    s = ""
    hightroll = [None, 0]
    highestCritsus = [None, 0]
    highestNats = [None, 0]
    highestCritFail =[None,0]
    highestNatOnes =[None,0]

    stars = [highestCritsus,highestCritsus,highestNats,highestCritFail,highestNatOnes]

    for player, values in playerStats.items():
        if hightroll[1] < values["highestRoll"]:
            if hightroll[1] == values["highestRoll"]:
                if playerAHaveMoreRolls(hightroll[0], player):
                    hightroll = [player, values["highestRoll"]]
            else:
                hightroll = [player, values["highestRoll"]]

        if highestCritsus[1] < values["totCrtSus"]:
            if hightroll[1] == values["totCrtSus"]:
                if playerAHaveMoreRolls(hightroll[0], player):
                    highestCritsus = [player, values["totCrtSus"]]
            else:
                highestCritsus = [player, values["totCrtSus"]]

        if highestNats[1] < values["nat20"]:
            if highestNats[1] == values["nat20"]:
                if playerAHaveMoreRolls(highestNats[0], player):
                    highestNats = [player, values["nat20"]]
            else:
                highestNats = [player, values["nat20"]]

        if highestCritFail[1] < values["totCrtFail"]:
            if highestCritFail[1] == values["totCrtFail"]:
                if playerAHaveMoreRolls(highestCritFail[0],player):
                    highestCritFail = [player,values["totCrtFail"]]
            else:
                highestCritFail = [player,values["totCrtFail"]]

        if highestNatOnes[1] < values["nat1"]:
            if highestNatOnes[1] == values["nat1"]:
                if playerAHaveMoreRolls(highestCritFail[0],player):
                    highestNatOnes = [player,values["nat1"]]
            else:
                highestNatOnes = [player,values["nat1"]]

    if all(a is None for a in [highestNats[0], highestCritsus[0], hightroll[0], highestCritFail[0],highestNats[0]]):
        return ""

    print(player)
    for val in stars:
        if val[0] is None:
            val[0] = player

    val = playerStats[hightroll[0]]
    val["points"] += 10
    playerStats[hightroll[0]] = val

    val = playerStats[highestCritsus[0]]
    val["points"] += 10
    playerStats[highestCritsus[0]] = val

    val = playerStats[highestNats[0]]
    val["points"] += 10
    playerStats[highestNats[0]] = val

    val = playerStats[highestCritFail[0]]
    val["points"] += 10
    playerStats[highestCritFail[0]] = val

    scores = []
    for player, values in playerStats.items():
        scores.append((values["names"], values["points"]))

    return sorted(scores, key=lambda score: score[1])

#get 2 players and finds if player A has more rolls
def playerAHaveMoreRolls(playerA, playerB):
    if playerA == None:
        return True
    else:
        return sum(playerStats[playerA]["diceRolls"].values()) > sum(playerStats[playerB]["diceRolls"].values())

#gets lists of messages and adds up each stat in set stat
def analyzeDB(messages):
    global playerStats
    playerStats = dict()

    for message in messages:
        stats = {"names": set(), "totCrtSus": 0, "totCrtFail": 0, "nat20": 0, "nat1": 0, "diceRolls": Counter(),
                 "topFormual": Counter(), "highestRoll": 0, "points": 0}

        id = message["UserID"]
        if id in playerStats:
            stats = playerStats[id]
        else:
            playerStats[id] = stats

        stats["names"].add(message["BY"])

        rolled = message["Rolled"]
        rollFomula = message["RolledFormula"]
        rollList = message["RolledResultsList"]

        count = stats["diceRolls"]
        stats["topFormual"][rollFomula] += 1

        for roll in rollList:
            m = re.search('d\d+', roll[0])
            if m:
                count[m.group(0)] += 1
            else:
                print("error at for roll in rollList ", message)

            if "critfail" in roll[0]:
                if "d20" in roll[0]:
                    stats["nat1"] += 1
                    stats["totCrtFail"] += 1

                else:
                    stats["totCrtFail"] += 1
            elif "critsuccess" in roll[0]:
                if not isinstance(m, type(None)):
                    val = int(m.group()[1:])
                else:
                    val = 0
                    print("error at for roll in rollList ", message)

                stats["points"] = stats["points"] + val
                if "d20" in roll[0]:

                    stats["nat20"] += 1
                    stats["totCrtSus"] += 1
                else:
                    stats["totCrtSus"] += 1

        stats["diceRolls"] = count

        lastHigestRoll = stats.get("highestRoll")
        if not isinstance(rolled, str):
            if (rolled > lastHigestRoll):
                stats["highestRoll"] = rolled
