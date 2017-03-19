import os
from html.parser import HTMLParser

import sys
from collections import Counter
import chatParser
from bs4.element import NavigableString

playerStats = dict()  # PlayerId:dict() states

path = ""


def getPath():
    path = ""
    # looks for the data in the data folder
    for file in os.listdir(os.path.join(sys.path[0], "data")):
        if file.endswith(".html") and file.startswith("Chat Log for"):
            path = os.path.join(sys.path[0], "data", file)

    return path


def main(givenPath):
    global path
    global messages

    if not givenPath:
        path = getPath()
    else:
        path = givenPath
    getStats(chatParser.getParse(path))

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
                        if any("rolled" in t for t in s):
                            currntRoll = stats.get("highestRoll")
                            roll = int(content.text.strip())
                            if roll > currntRoll:
                                stats["highestRoll"] = roll
                        if any("formula" in t for t in s):
                            print(content.text)
                            breaktest = content.text.strip()
                            dice = diceCounter(content)
                            stats["totCrtSus"] += dice[0]
                            stats["totCrtFail"] += dice[1]
                            stats["diceRolls"].extend(dice[2])
                            stats["nat20"] += dice[3]
                            stats["nat1"] += dice[4]

            playerStats[id] = stats


def getGivenPath():
    return path


def talk():
    return returnStats()


# todo make this look good
def returnStats():
    s = ""
    for player, values in playerStats.items():
        # s = s + player
        s = s + str(values["names"]) + " " + str(len(values["names"])) + "\n"
        s = s + "Total Number of Rolls " + str(len(values["diceRolls"])) + "\n"
        s = s + str("Crit success: {}, Nat20: {}, Crit fail: {}, Nat1: {}".format(values["totCrtSus"], values["nat20"],
                                                                                  values["totCrtFail"],
                                                                                  values["nat1"])) + "\n"
        s = s + str(Counter(values["diceRolls"])) + "\n"
        s = s + "highest roll " + str(values["highestRoll"])
        s = s + ('\n\n')
    return s


main("")
