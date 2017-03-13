import os
from HTMLParser import HTMLParser

import sys
from collections import Counter

class HTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        #print("Start tag:", tag)
        
        for attr in attrs:
            #print("     attr:", attr)
            wf.write(' '.join(str(s) for s in attr) + '\n');
            
    def handle_data(self, data):
        #print("Data     :", data)
        wf.write(data.strip() +"\n");


f = open(os.path.join(sys.path[0],"data\\Chat Log for Caramohn's Level.html"),'r')
wf = open(os.path.join(sys.path[0],"data\\scrub.txt"),'w')

parser = HTMLParser()
#maybe make a loading bar for this
for line in f:
    if "textchatcontainer" in line:
        parser.feed(f.next())
        break

f.close()
wf.close()
print("done with scrub")

f = open(os.path.join(sys.path[0],"data\\scrub.txt"),'r')

playerStats = dict()#PlayerId:dict() states
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
        f.next()
        f.next()
        line=f.next()
        if "class avatar" in line:
            line =f.next()
            photos = stats["photos"]
            photo = line.strip()
            photos.add(photo)
            stats["photos"] = photos
            playerStats[currentPlayer] = stats
f.seek(0)

for line in f:
    if "data-playerid" in line:
        s = line.split(" ")
        playerId = s[1]
        playerId = playerId.strip()
        currentPlayer = playerId
    if "class avatar" in line:
        s= f.next()
        currentPhotoId = s.strip()
    if "class by" in line:
        line = f.next()
        player = playerStats[currentPlayer]
        photos = player["photos"];
        if currentPhotoId in photos:
            player["names"].add(line.strip())
    if "diceroll" in line:
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
        player["diceRolls"].append(roll)

for player, values in playerStats.iteritems():
    print(values["names"],len(values["names"]))
    print(len(values["diceRolls"]))
    print("Crit success: {}, Nat 20: {}, Crit fail: {}, Nat 1 {}".format(values["totCrtSus"],values["nat20"],values["totCrtFail"],values["nat1"]))
    print(Counter(values["diceRolls"]))
    print('\n')

f.close()



