import os
from html.parser import HTMLParser

import sys
from collections import Counter

#parses out the html of the chat log
class HTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        #print("Start tag:", tag)

        for attr in attrs:
            #print("     attr:", attr)
            wf.write(' '.join(str(s) for s in attr) + '\n');
            
    def handle_data(self, data):
        #print("Data     :", data)
        wf.write(data.strip() +"\n");


def getPath():
    path = ""
    # looks for the data in the data folder
    for file in os.listdir(os.path.join(sys.path[0], "data")):
        if file.endswith(".html") and file.startswith("Chat Log for"):
            path = os.path.join(sys.path[0], "data", file)

    return path


f = open(getPath(),'r')
scrubPath = os.path.join(sys.path[0],"data\\scrub.txt")
#the scrubing file that has all the usefull data in it
wf = open(scrubPath,'w')

parser = HTMLParser()
#todo maybe make a loading bar for this

read = False
for line in f:
    if "textchatcontainer" in line:# This is the container that has all the rolls and chat data
        read = True
    if "tmpl_chatmessage_general" in line:
        read = False
    if read:
        parser.feed(f.readline())


f.close()
wf.close()
print("done with scrub")

f = open(scrubPath,'r')

playerStats = dict()#PlayerId:dict() states
'''
roll 20 does not put the player Id when a user makes a general message
This means that if a player make a general message it can be by anyone
This also means associating human readable name like "krong the mighty" to the id  is annoying
Thankfully all posts have a player picture associated to them at appears when they make a post.
Im using that to help associate ID with names
'''
currentPlayer = ""
currentPhotoId = ""

#get the player ID and Photos
#Player needs to roll first before the type into chat or their will be hella problems
for line in f:
    if "data-playerid"  in line:
        line.strip('\n')
        s = line.split(" ")
        playerId = s[1]
        playerId = playerId.strip()
        currentPlayer = playerId
        stats = {"photos":set(),"names":set(),"totCrtSus":0,"totCrtFail":0,"nat20":0,"nat1":0,"diceRolls":[]}
        f.readline()
        f.readline()
        line=f.readline()
        if "class avatar" in line:
            line =f.readline()
            photos = stats["photos"]
            photo = line.strip()
            photos.add(photo)
            stats["photos"] = photos
            playerStats[currentPlayer] = stats

#makes F go back to first line.
f.seek(0)

for line in f:
    if "data-playerid" in line:#this gets the player of the message that is being analyzed
        s = line.split(" ")
        playerId = s[1]
        playerId = playerId.strip()
        currentPlayer = playerId
    if "class avatar" in line:#this gets the avatar of the message that is being analyzed
        s= f.readline()
        currentPhotoId = s.strip()
    if "class by" in line:
        line = f.readline()
        player = playerStats[currentPlayer]
        photos = player["photos"];
        if currentPhotoId in photos:
            player["names"].add(line.strip())
    if "diceroll" in line:#get all the dice rolls
        if "dropped" in line:
            continue
        player = playerStats[currentPlayer]
        if "critsuccess" in line:
            player["totCrtSus"]+= 1
            if "d20" in line:
                player["nat20"] += 1
        elif "critfail" in line:
            player["totCrtFail"] += 1
            if "d20" in line:
                player["nat1"] += 1
        roll = line.split(" ")[2].strip()
        if "withouticons" in roll:# some roll dont have icons those roll say that in the place that should have the D#
            player["diceRolls"].append(roll)
            roll = line.split(" ")[3].strip()
        player["diceRolls"].append(roll)


for player, values in playerStats.items():

    print(values["names"],len(values["names"]))
    print("Total Number of Rolls",len(values["diceRolls"]))
    print("Crit success: {}, Nat20: {}, Crit fail: {}, Nat1: {}".format(values["totCrtSus"],values["nat20"],values["totCrtFail"],values["nat1"]))
    print(Counter(values["diceRolls"]))
    print('\n')


f.close()

def talk():
    return returnStats()


#todo make this look good
def returnStats():
    s = ""
    for player, values in playerStats.items():
        s = s +  str(values["names"]) +" "+ str(len(values["names"]))
        s= s + "Total Number of Rolls " + str(len(values["diceRolls"]))
        s = s + str("Crit success: {}, Nat20: {}, Crit fail: {}, Nat1: {}".format(values["totCrtSus"], values["nat20"],
                                                                            values["totCrtFail"], values["nat1"]))
        s = s + str(Counter(values["diceRolls"]))
        s = s + ('\n')
    return s

