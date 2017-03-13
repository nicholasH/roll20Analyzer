from html.parser import HTMLParser

class HTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        #print("Start tag:", tag)
        
        for attr in attrs:
            #print("     attr:", attr)
            wf.write(' '.join(str(s) for s in attr) + '\n');
            
    def handle_data(self, data):
        #print("Data     :", data)
        wf.write(data.strip() +"\n");
        
        

f = open("E:\\GitProjects\\roll20Analyzer\\data\\Chat Log for Caramohn's Level.html",'r')
wf = open("E:\\GitProjects\\roll20Analyzer\\data\\scrub.txt",'w')

parser = HTMLParser()
#maybe make a loading bar for this
for line in f:
    if "textchatcontainer" in line:
        parser.feed(f.readline())
        break

f.close()
wf.close()
print("done with scrub")

f = open("E:\\GitProjects\\roll20Analyzer\\data\\scrub.txt",'r')

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
        if currentPlayer in playerStats:
            continue
        stats = {"photos":set(),"names":set(),"totCrtSus":0,"totCrt":0,"nat20":0,"nat1":0}
    if "class avatar" in line:
        photoID = f.readline()
        currentPhotoId =photoID.strip()
    




for line in f:
    if "data-playerid"  in line:
        line.strip('\n')
        s = line.split(" ")
        playerId = s[1]
        playerId = playerId.strip()
        currentPlayer = playerId
        if currentPlayer in playerStats:
            continue
        
        
        stats = {"names":set(),"totCrtSus":0,"totCrt":0,"nat20":0,"nat1":0}
        playerStats.update({playerId:stats})
        '''
    if "class by" in line:
        print(currentPlayer)
        print(line)
        name = f.readline()
        print(name)
        stats = playerStats[currentPlayer]
        names = stats["names"]
        names.add(name)
        print(names)
        '''






print(playerStats)
f.close()

    

