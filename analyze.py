import operator
import os
from html.parser import HTMLParser

import sys
from collections import Counter

from datetime import datetime
import chatParser
from bs4.element import NavigableString
import DBhandler
import re

global playerStats   # PlayerId:dict() states
playerStats = dict()

path = ""

real = ""
realDice = ["d4","d6","d10","d12","d20"]

#old method that use to be used to get html that the user downloaded
def getPath():
    path = ""
    # looks for the data in the data folder
    for file in os.listdir(os.path.join(sys.path[0], "data")):
        if file.endswith(".html") and file.startswith("Chat Log for"):
            path = os.path.join(sys.path[0], "data", file)

    return path


def analyze():
    chatParser.addToDb()
    analyzeDB(DBhandler.getMessagesRoleresult())
    print(returnStats())
    return returnStats()


def analyzeToday():
    chatParser.addToDb()
    startToday = datetime(datetime.today().year,datetime.today().month,datetime.today().day)
    analyzeDB(DBhandler.getRollresultDateTime(startToday))
    print(returnStats())
    return returnStats()

#Gets 1 Datetime and returns the messages of that date
def analyzeDate(date):
    analyzeDB(DBhandler.getRollresultDateTime(date))
    print(returnStats())
    return returnStats()

#Gets 2 datestimes and returns the messaages between the dates
def analyzeDateRange(date0,date1):
    analyzeDB(DBhandler.getRollresultDateTimeRange(date0, date1))
    print(returnStats())
    return returnStats()

def analyzeByTag(tagName):
    print(tagName)
    DBhandler.printTags()
    analyzeDB(DBhandler.getMessagesWithTags(tagName))
    print(returnStats())
    return returnStats()

def diceCounter(diceFomula):
    s = diceFomula.attrs.get("class")
    critsuc = 0
    critfail = 0
    dices = []
    nat20 = 0
    nat1 = 0


    if any("formattedformula" in t for t in s):
        for child in diceFomula.descendants:
            if not isinstance(child, NavigableString):
                childClass = child.attrs["class"]
                if any("dicegrouping" in at for at in childClass):
                    for childCon in child.contents:
                        if not isinstance(childCon, NavigableString):
                            childConAttrsClass = childCon.attrs["class"]
                            if not any("dropped" in t for t in childConAttrsClass):
                                if any("withouticons" in t for t in childConAttrsClass):
                                    dice = childConAttrsClass[2]
                                    dices.extend([childConAttrsClass[1],dice])
                                else:
                                    dice = childConAttrsClass[1]
                                    dices.append(dice)
                                if any("critsuccess" in t for t in childConAttrsClass):
                                    critsuc += 1
                                    if "d20" in dice:
                                        nat20 += 1
                                if any("critfail" in t for t in childConAttrsClass):
                                    critfail += 1
                                    if "d20" in dice:
                                        nat1 += 1


    return [critsuc, critfail, dices,nat20,nat1]


def getStats(messages):
    for message in messages:
        if "rollresult" in message.attrs["class"]:
            stats = {"photos": set(), "names": set(), "totCrtSus": 0, "totCrtFail": 0, "nat20": 0, "nat1": 0,
                     "diceRolls": [], "highestRoll": 0}

            id = message.attrs["data-playerid"]
            if id in playerStats:
                stats = playerStats[id]
            else:
                playerStats[id] = stats
            for content in message.contents:

                if not isinstance(content, NavigableString):
                    s = content.attrs.get("class")
                    if not isinstance(s, type(None)):
                        if any("avtar" in t for t in s):
                            photo = content.next_element.attrs["src"]
                            stats["photos"].add(photo)
                        if any("by" in t for t in s):
                            by = content.text
                            stats["names"].add(by)

                        if any("formula" in t for t in s):
                            count = False
                            dice = diceCounter(content)

                            if real:
                                for realDi in realDice:
                                    if any(realDi == f for f in dice[2]):
                                        count = True
                            if count or not real:
                                stats["totCrtSus"] += dice[0]
                                stats["totCrtFail"] += dice[1]
                                stats["diceRolls"].extend(dice[2])
                                stats["nat20"] += dice[3]
                                stats["nat1"] += dice[4]

                        if any("rolled" in t for t in s):
                            if count or not real:
                                currntRoll = stats.get("highestRoll")
                                roll = int(content.text.strip())
                                if roll > currntRoll:
                                    stats["highestRoll"] = roll






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

    s = s + " " + str(findWinner(""))
    s = s +"\n"+ "#"*100
    return s



#todo add in a way to excluded players like the DM
def findWinner(exclude):

    s = ""
    hightroll = [None,0]
    highestCritsus = [None,0]
    highestNats = [None,0]

    for player, values in playerStats.items():
        if hightroll[1] < values["highestRoll"]:
            if hightroll[1] ==  values["highestRoll"]:
                if playerAHaveMoreRolls(hightroll[0],player):
                    hightroll = [player, values["highestRoll"]]
            else:
                hightroll = [player,values["highestRoll"]]

        if highestCritsus[1] < values["totCrtSus"]:
            if hightroll[1] == values["totCrtSus"]:
                if playerAHaveMoreRolls(hightroll[0],player):
                    highestCritsus = [player, values["totCrtSus"]]
            else:
                highestCritsus = [player,values["totCrtSus"]]

        if highestNats[1] < values["nat20"]:
            if highestNats[1] == values["nat20"]:
                if playerAHaveMoreRolls(highestNats[0], player):
                    highestNats = [player, values["nat20"]]
            else:
                highestNats = [player, values["nat20"]]

    if any(a is None for a in [highestNats[0], highestCritsus[0], hightroll[0]]):
        return ""

    val = playerStats[hightroll[0]]
    val["points"] += 20
    playerStats[hightroll[0]] = val

    val = playerStats[highestCritsus[0]]
    val["points"] += 20
    playerStats[highestCritsus[0]] = val

    val = playerStats[highestNats[0]]
    val["points"] += 20
    playerStats[highestNats[0]] = val

    scores = []
    for player, values in playerStats.items():
        scores.append((values["names"],values["points"]))


    return sorted(scores, key=lambda score: score[1])

def playerAHaveMoreRolls(playerA,playerB):
    if playerA == None:
        return True
    else:
        return sum(playerStats[playerA]["diceRolls"].values()) > sum(playerStats[playerB]["diceRolls"].values())




def analyzeDB(messages):
    global playerStats
    playerStats = dict()

    for message in messages:
        stats = {"names": set(), "totCrtSus": 0, "totCrtFail": 0, "nat20": 0, "nat1": 0,"diceRolls": Counter(), "topFormual":Counter(), "highestRoll": 0,"points": 0}

        id = message["UserID"]
        if id in playerStats:
            stats = playerStats[id]
        else:
            playerStats[id] = stats

        stats["names"].add(message["BY"])

        rolled = message["Rolled"]
        rollFomula = message["RolledFormula"]
        rollList =  message["RolledResultsList"]

        count = stats["diceRolls"]
        stats["topFormual"][rollFomula] += 1

        for roll in rollList:
            m = re.search('d\d+', roll[0])
            if m:
                count[m.group(0)] += 1
            else:
                print("error at for roll in rollList ",message)


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
                    print("error at for roll in rollList ", message)

                stats["points"] = stats["points"] + val
                if "d20" in roll[0]:

                    stats["nat20"] += 1
                    stats["totCrtSus"] += 1
                else:
                    stats["totCrtSus"] += 1

        stats["diceRolls"] = count


        lastHigestRoll = stats.get("highestRoll")
        if not isinstance(rolled,str):
            if(rolled > lastHigestRoll):
                stats["highestRoll"] = rolled





