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


def getPath():
    path = ""
    # looks for the data in the data folder
    for file in os.listdir(os.path.join(sys.path[0], "data")):
        if file.endswith(".html") and file.startswith("Chat Log for"):
            path = os.path.join(sys.path[0], "data", file)

    return path


def analyze():

    chatParser.addToDb()
    analyzeDB(DBhandler.getMessages())

    analyzeDB(DBhandler.getMessageDateTime(datetime.today()))
    print(returnStats())


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
        s = s + ('\n\n')
    return s



def analyzeDB(messages):
    global playerStats
    playerStats = dict()

    for message in messages:
        stats = {"names": set(), "totCrtSus": 0, "totCrtFail": 0, "nat20": 0, "nat1": 0,"diceRolls": Counter(), "topFormual":Counter(), "highestRoll": 0}

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
                print("error at for roll in rollList ",roll)


            if "critfail" in roll[0]:
                if "d20" in roll[0]:
                    stats["nat1"] += 1
                    stats["totCrtFail"] += 1

                else:
                    stats["totCrtFail"] += 1
            elif "critsuccess" in roll[0]:
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





