from bs4 import BeautifulSoup
import re

test = []
f = open("E:\\GitProjects\\roll20Analyzer\\data\\Chat Log for Caramohn's Level.html")

soup = BeautifulSoup(f.read(), 'html.parser')  # make soup that is parse-able by bs

generalmatch = re.compile('message \w+')

chatContent = soup.findAll("div", {"class": generalmatch})

for message in chatContent:
    if "rollresult" in message.attrs["class"]:
        print("worked")


print("")


def diceCounter(diceFomula):
    s = diceFomula.attrs.get("class")
    critsuc = 0
    critfail = 0
    dices = []

    if any("formattedformula" in t for t in s):
        for child in diceFomula.descendants:
            if not isinstance(child, NavigableString):
                childClass = child.attrs["class"]
                if any("dicegrouping" in at for at in childClass):
                    c = child

                    print()

    return [critsuc, critfail, dices]


dice = diceFomula.next_element.next_element.contents
if len(dice) > 0:
    dices.append(dice[1])
    for di in dice:
        if not isinstance(di, NavigableString):
            d = di.attrs["class"]
            if any("critsuccess" in t for t in d):
                critsuc += 1
            if any("critfail" in t for t in d):
                critfail += 1