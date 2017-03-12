f = open("E:\\GitProjects\\roll20Analyzer\\data\\chatLogDataCopyPaste.txt",'r')

#the names of that my friends us in roll 20
#I really need to find a way to not have this hard coded
#Add roll names to make it more search able
nickNames = ["Nicholas H.","BUBBLEs"]
nick = "nick"
jarredNames = ["Jarred M.","Lo-Keg"]
jarred = "jear bear"
mikeNames = ["Michael L.","Vux'olna","Loth (Mike)","Lotherial"]
mike = "mike"
vaasNames =["Morthos","Kyle","Rhy","Rhyvos"]
vaas = "vaas"
meechNames = ["meech n.","Meerno Durthee-son"]
meech = "meech"
genevieveNames = ["Rowan Tealeaf-Tosscobble","Genevieve J"]
genevieve = "genevieve"


names = nickNames + jarredNames + mikeNames + vaasNames + meechNames + genevieveNames

index = f.tell()
line = f.readline()
chatIndex = []


while line:
    if any(s in line for s in names):
        name = ""
        if any(s in line for s in nickNames):
            name = nick
            chatList =[name,index]
        if any(s in line for s in jarredNames):
            name = jarred
            chatList =[name,index]
        if any(s in line for s in mikeNames):
            name = mike
            chatList =[name,index]
        if any(s in line for s in vaasNames):
            name = vaas
            chatList =[name,index]
        if any(s in line for s in meechNames):
            name = meech
            chatList =[name,index]
        if any(s in line for s in genevieveNames):
            name = genevieve
            chatList =[name,index]
        
        chatIndex.append(chatList)
    index = f.tell()
    #end of the main while loop 
    line = f.readline()
    
    
    
print(chatIndex)
f.seek(0)
f.seek(308)
line = f.readline()
print(line)
        
        
        

f.close()

