import os
from HTMLParser import HTMLParser

import sys


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
        stats = {"photos":set(),"names":set(),"totCrtSus":0,"totCrt":0,"nat20":0,"nat1":0}
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
            player["names"].add(line)








print(playerStats)
f.close()



