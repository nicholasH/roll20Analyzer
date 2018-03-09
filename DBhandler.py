import os
import sqlite3
from datetime import datetime, date, timedelta
import pickle
import errors
import sys

DBVersion = "1.1"

# messageTable
Message_table = 'Message'

MessageID_field = "MessageID"
MessageType_field = "MessageType"
By_field = 'BY'
Avatar_field = "Avatar"
Time_field = "Time"

# userIDTable
User_table = 'User'

UserID_field = 'UserID'
MessageID_field_UserTable = MessageID_field

# FormulaTable
Formula_table = 'Fourmula'

Roll_Formula_field = 'RollFormula'
TotalRoll_field = 'TotalRoll'
Formula_ID_field = 'FormulaID'
MessageID_field_FormulaTable = MessageID_field

# diceTable
Dice_table = "Dice"

Sides_field = "Sides"
Roll_field = "Roll"
Crit_field = 'Crit'
Dice_ID_field = 'DiceID'

# dice formula Junction
Dice_Formula_junction_table = 'Dice_Formula_JT'

Formula_ID_field_JT = Formula_ID_field + "_JT"
Dice_ID_field_JT = Dice_ID_field + "_JT"

# game Table
GameData_table = 'gameData'
GameName_feild = 'name'
GameUrl_feild = 'url'
DBVersion_feild = "DBVersion"

# tag table
Tag_table = "Tags"
MessageID_tag_field = MessageID_field
Tag_name_field = "TagName"

# active_table
tag_active_table = "tags_active"

Tag_Active_name_field = Tag_name_field
tag_type_field = "TagType"
tag_data_field = "Data"
tag_self_feild = "Self"
tag_Avatar_field = Avatar_field
tag_Active_playerID_feild = UserID_field

integer_field_type = 'INTEGER'
string_field_type = 'STRING'
Date_field_type = "date"
Tstamp_field = 'timestamp'

db = None


# creates all the DBs tables and sets the metaData for the DB
def createDB(name, url):
    setDB(name)
    createMessageTable()
    createUserTable()
    createFormulaTable()
    createDiceTable()
    createDiceFormulaTable()
    createGameDataTable()
    createTagTable()
    createActiveTageTable()

    setdata(name, url)


# creates the messageTable
def createMessageTable():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    exe = 'CREATE TABLE {tn} ({MID} {fts} PRIMARY KEY, {MT} {fts}, {AVA} {fts}, {By} {fts}, {TF} {ftts})' \
        .format(tn=Message_table,

                MID=MessageID_field,
                MT=MessageType_field,
                AVA=Avatar_field,
                By=By_field,
                TF=Time_field

                , fts=string_field_type, ftd=Date_field_type, ftts=Tstamp_field)

    c.execute(exe)


# creates the UserTable
def createUserTable():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    exe = 'CREATE TABLE {tn} ({MIDU} {fts}, {UID} {fts}, FOREIGN KEY({MIDU}) REFERENCES {MTN}({MID}))' \
        .format(
        tn=User_table,
        MID=MessageID_field,
        MIDU=MessageID_field_UserTable,
        MTN=Message_table,
        UID=UserID_field
        , fts=string_field_type)
    c.execute(exe)

    conn.close()


# creates the FormulaTable
def createFormulaTable():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()

    exe = 'CREATE TABLE {tn} ({FID} {fti} primary key AUTOINCREMENT, {MIDF} {fts},{TR} {fti}, {RF} {fts}, FOREIGN KEY({MIDF}) REFERENCES {MTN}({MID}))' \
        .format(tn=Formula_table,

                FID=Formula_ID_field,
                MID=MessageID_field,
                MIDF=MessageID_field_FormulaTable,
                MTN=Message_table,
                TR=TotalRoll_field,
                RF=Roll_Formula_field

                , fts=string_field_type, fti=integer_field_type)
    c.execute(exe)

    conn.close()


# creates the CreateDice Table
def createDiceTable():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    exe = 'CREATE TABLE {tn} ({DID} {fti} primary key AUTOINCREMENT, {SD} {fti}, {CT} {fts}, {RL} {fts})' \
        .format(tn=Dice_table,

                DID=Dice_ID_field,
                SD=Sides_field,
                CT=Crit_field,
                RL=Roll_field

                , fts=string_field_type, fti=integer_field_type)
    c.execute(exe)
    conn.close()


# creates the Dice Formula table
def createDiceFormulaTable():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    exe = 'CREATE TABLE {tn} ({FID} {fti}, {DID} {fti}, FOREIGN KEY({DID}) REFERENCES {DTN}({DTID}), FOREIGN KEY({FID}) REFERENCES {FTN}({FTID}))' \
        .format(tn=Dice_Formula_junction_table,

                DTN=Dice_table,
                DTID=Dice_ID_field,
                FTN=Formula_table,
                FTID=Formula_ID_field,
                DID=Dice_ID_field_JT,
                FID=Formula_ID_field_JT

                , fts=string_field_type, fti=integer_field_type)
    c.execute(exe)
    conn.close()


# creates the GameDataTable
def createGameDataTable():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    exe = "CREATE TABLE {tn} ({n} {fts}, {url} {fts} , {vn} {fts})".format(
        tn=GameData_table,
        n=GameName_feild,
        url=GameUrl_feild,
        vn=DBVersion_feild,
        fts=string_field_type
    )
    c.execute(exe)
    conn.close()


# creates the Tag table
def createTagTable():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    exe = "CREATE TABLE {tn} ({mf} {fts}, {tan} {fts}, FOREIGN KEY({mf}) REFERENCES {MTN}({TMID}))".format(
        tn=Tag_table,
        MTN=Message_table,
        TMID=MessageID_field,
        mf=MessageID_tag_field,
        tan=Tag_name_field,
        fts=string_field_type
    )
    c.execute(exe)
    conn.close()


# creates the active tag table
def createActiveTageTable():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    exe = "CREATE TABLE {tn} (id {fit} PRIMARY KEY,{ta} {fts}, {tt} {fts}, {td} {fts}, {slf} {fit}, {ava} {fts}, {uf} {fts})".format(
        tn=tag_active_table,
        ta=Tag_Active_name_field,
        tt=tag_type_field,
        td=tag_data_field,
        slf=tag_self_feild,
        ava=tag_Avatar_field,
        uf=tag_Active_playerID_feild,

        fit=integer_field_type,
        fts=string_field_type
    )
    c.execute(exe)
    conn.close()


################################################################################################################################


# sets the meta data of the game
def setdata(name, url):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("INSERT INTO gameData VALUES (?,?,?)", (name, url, DBVersion))
    conn.commit()
    conn.close()


# loads an DB from storage
def loadDB(path):
    global db
    db = path


# sets a new db
def setDB(name):
    global db
    dbName = name + '.db'
    db = os.path.join(sys.path[0], "data", "dataBase", dbName)
    if not os.path.exists(os.path.join(sys.path[0], "data", "dataBase")):
        os.makedirs(os.path.join(sys.path[0], "data", "dataBase"))


# creates the gets the path for the DB
def getDBPath():
    if db == "" or db == None:
        raise errors.DBNotLoaded
    return db


# Destroys the DB
def destroyDB():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS ' + Message_table)
    c.execute('DROP TABLE IF EXISTS ' + User_table)
    c.execute('DROP TABLE IF EXISTS ' + Formula_table)
    c.execute('DROP TABLE IF EXISTS ' + Dice_table)
    c.execute('DROP TABLE IF EXISTS ' + Dice_Formula_junction_table)
    c.execute('DROP TABLE IF EXISTS ' + GameData_table)
    c.execute('DROP TABLE IF EXISTS ' + Tag_table)
    c.execute('DROP TABLE IF EXISTS ' + tag_active_table)

    conn.commit()
    conn.close()

def clearActive():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute('DELETE FROM ' + tag_active_table)
    conn.commit()
    conn.close()


# ADD
########################################################################################################################

# add many Messages to the DB
def addManyToMessageTable(allmessage):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    exe = "INSERT OR IGNORE INTO Message ( " + MessageID_field + "," + MessageType_field + "," + Avatar_field + "," + By_field + "," + Time_field + " ) VALUES (?,?,?,?,?)"
    c.executemany(exe, allmessage)
    conn.commit()
    conn.close()


# add  list of users to the UserTable
# allUser is list of (MessageID, UserID)
def addManyToUserIDTable(allusers):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    exe = "INSERT INTO " + User_table + " VALUES (?,?)"
    c.executemany(exe, allusers)
    conn.commit()
    conn.close()


# add a list of formulas to Formula Table
def addManytoFormulaTable(cursor, allformula):
    cursor.execute("SELECT max(" + Formula_ID_field + ") FROM " + Formula_table)
    A_ID = cursor.fetchone()[0]
    exe = "INSERT INTO " + Formula_table + "( " + MessageID_field_FormulaTable + ", " + Roll_Formula_field + ", " + TotalRoll_field + ") VALUES (?,?,?)"
    cursor.executemany(exe, allformula)

    cursor.execute("SELECT max(" + Formula_ID_field + ") FROM " + Formula_table)
    B_ID = cursor.fetchone()[0]

    if A_ID is None:
        A_ID = 1
    else:
        A_ID = A_ID + 1

    return [A_ID, B_ID]


# adds a list of dice to the Dice Table
def addManyToDiceTable(cursor, diceList):
    cursor.execute("SELECT max(" + Dice_ID_field + ") FROM " + Dice_table)
    A_ID = cursor.fetchone()[0]

    exe = "INSERT INTO " + Dice_table + "( " + Sides_field + ", " + Crit_field + ", " + Roll_field + ") VALUES (?,?,?)"
    cursor.executemany(exe, diceList)
    cursor.execute("SELECT max(" + Dice_ID_field + ") FROM " + Dice_table)
    B_ID = cursor.fetchone()[0]

    if A_ID is None:
        A_ID = 1
    else:
        A_ID = A_ID + 1

    return [A_ID, B_ID]


# add a list of Dice fromulaID and DiceID
def addManyToDiceFormulaJunkTable(cursor, diceFormula):
    exe = "INSERT INTO " + Dice_Formula_junction_table + " VALUES (?,?)"
    cursor.executemany(exe, diceFormula)

# todo take this out of DB to ChatParser
# gets array of tagDetails and addeds the tag to the active tag table
# tagArray is a list  that can inclued one - three items
def addtoTagActiveTable(userID, tagName, tagType, tagDetails, Avatar, self):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute(
        "INSERT INTO tags_active (TagName, TagType, Data, Self,  Avatar, UserID)VALUES (?,?,?,?,?,?)", (
            tagName,
            tagType,
            pickle.dumps(tagDetails),
            int(self),
            Avatar,
            userID
        ))
    conn.commit()
    conn.close()


# todo make a add many for Active Tags

# get messageID and playerID and adds all active tags to the DB and assosiates them with the MessageID
def addtag(messageID, playerID, tstamp):
    tags = list(set(getActiveTagsAndUpdate(playerID, tstamp)))
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    for tag in tags:
        c.execute(
            "INSERT INTO Tags VALUES (?,?)", (
                messageID,
                tag[0],
            ))
    conn.commit()
    conn.close()


# add a list of messageID and tags
def addManyToTag(allTags):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.executemany("INSERT INTO Tags VALUES (?,?)", allTags)
    conn.commit()
    conn.close()




def addManyFormulaAndDice(allformulaAndDice):
    if len(allformulaAndDice) == 0:
        return
    allformulas, alldices = zip(*allformulaAndDice)

    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()

    formulaIDRandge = addManytoFormulaTable(c, allformulas)

    diceRanges = list()
    for dice in alldices:
        diceRanges.append(addManyToDiceTable(c, dice))

    x = 0
    for formID in range(formulaIDRandge[0], formulaIDRandge[1] + 1):
        dices = list(range(diceRanges[x][0], diceRanges[x][1] + 1))
        fIDs = [formID] * len(dices)
        formulaIDAndDiceIDS = list(zip(fIDs, dices))
        addManyToDiceFormulaJunkTable(c, formulaIDAndDiceIDS)
        x += 1
    conn.commit()
    conn.close()


# Get
#######################################################################################################################

# Gets all the message in the DB and returns a list
def getMessages():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT * FROM Message")
    conn.commit()
    data = c.fetchall()
    conn.close()

    return makeList(data)


# returns a list of all dice
# returns a (MessageID,RollType,BY,UserID,FourmulaID,Roll,TotalRoll,DiceSide,Crite,Roll)
def getMessagesRolls():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    exe = "SELECT {MT}.{MID}, {Type}, {BY} ,{UID},{FT}.{FID},{RF},{TotR},{Side},{Crit},{Roll} " \
          "FROM {MT} " \
          "LEFT JOIN {UT} " \
          "ON ({UT}.{MID} = {MT}.{MID}) " \
          "JOIN {FT} " \
          "ON ({FT}.{MID} = {MT}.{MID}) " \
          "JOIN {DFJT} " \
          "ON ({DFJT}.{FIDJ} = {FT}.{FID}) " \
          "JOIN {DT} " \
          "ON ({DT}.{DID} = {DFJT}.{DIDJ}) ".format(
        MT=Message_table,
        FT=Formula_table,
        UT=User_table,
        DT=Dice_table,
        DFJT=Dice_Formula_junction_table,

        MID=MessageID_field,
        BY=By_field,
        Type=MessageType_field,
        UID=UserID_field,
        RF=Roll_Formula_field,
        TotR=TotalRoll_field,
        Side=Sides_field,
        Crit=Crit_field,
        Roll=Roll_field,
        FID=Formula_ID_field,
        DIDJ=Dice_ID_field_JT,
        FIDJ=Formula_ID_field_JT,
        DID=Dice_ID_field

    )
    print(exe)
    c.execute(exe)
    conn.commit()
    data = c.fetchall()
    conn.close()
    return makeDiceList(data)


# All the Distinct Tags names
def getAllTags():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    exe = "SELECT DISTINCT {TN} FROM {TT}".format(
        TT=Tag_table,
        TN=Tag_name_field
    )
    c.execute(exe)
    conn.commit()
    data = c.fetchall()
    conn.close()
    return makeList(data)


# get data that make a list out of it
def makeList(data):
    listTurn = list()

    for datum in data:
        listTurn.append(datum)

    return listTurn

def makeActiveList(data):
    listTurn = list()
    for datum in data:
        listTurn.append([datum[0],datum[1],datum[2],pickle.loads(datum[3]),datum[4],datum[5]])
    return listTurn


# Make a list of dictionary and return it
def makeDiceList(data):
    diceColumnName = [MessageID_field, MessageType_field, By_field, UserID_field, Formula_ID_field, Roll_Formula_field,
                      TotalRoll_field, Sides_field, Crit_field, Roll_field]

    listTurn = list()
    for datum in data:
        dic = dict(zip(diceColumnName, datum))
        listTurn.append(dic)
    return listTurn




# get the url or the gamedata
def getURL():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT url FROM gameData")
    conn.commit()
    url = c.fetchone()
    conn.close()
    return url[0]


# get the Game number from the url
def getGameNumber():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT url FROM gameData")
    conn.commit()
    url = c.fetchone()
    conn.close()
    return str(url[0]).split("/")[-1]


# get the name of the game
def getGameName():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT name FROM gameData")
    conn.commit()
    name = c.fetchone()
    conn.close()
    return name[0]


# gets the last message in the DB
def getlastMessage():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("select count(*) from sqlite_master where type='table' and name='Message'")
    exist = c.fetchone()[0]
    if exist:
        c.execute('SELECT max({ID}) FROM {tn}'.format(
            tn=Message_table,
            ID=MessageID_field
        ))

        max_ID = c.fetchone()[0]
        conn.close()
        return max_ID
    else:
        conn.close()
        return None


# get a single dateTime object and returns message on that date
def getRollresultDateTime(dateTime):
    dateA = dateTime
    dateB = datetime(dateA.year, dateA.month, dateA.day, 23, 59, 59)
    return getRollresultDateTimeRange(dateA, dateB)


# get two date time objects and gets the range of them
def getRollresultDateTimeRange(dateTimeA, dateTimeB):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    exe = "SELECT {MT}.{MID}, {Type}, {BY} ,{UID},{FT}.{FID},{RF},{TotR},{Side},{Crit},{Roll} " \
          "FROM {MT} " \
          "LEFT JOIN {UT} " \
          "ON ({UT}.{MID} = {MT}.{MID}) " \
          "JOIN {FT} " \
          "ON ({FT}.{MID} = {MT}.{MID}) " \
          "JOIN {DFJT} " \
          "ON ({DFJT}.{FIDJ} = {FT}.{FID}) " \
          "JOIN {DT} " \
          "ON ({DT}.{DID} = {DFJT}.{DIDJ}) " \
          "WHERE {tf} BETWEEN \"{DA}\" AND \"{DB}\"".format(
        MT=Message_table,
        FT=Formula_table,
        UT=User_table,
        DT=Dice_table,
        DFJT=Dice_Formula_junction_table,

        MID=MessageID_field,
        BY=By_field,
        Type=MessageType_field,
        UID=UserID_field,
        RF=Roll_Formula_field,
        TotR=TotalRoll_field,
        Side=Sides_field,
        Crit=Crit_field,
        Roll=Roll_field,
        FID=Formula_ID_field,
        DIDJ=Dice_ID_field_JT,
        FIDJ=Formula_ID_field_JT,
        DID=Dice_ID_field,
        tf=Time_field,
        DA=dateTimeA,
        DB=dateTimeB
    )
    print(exe)

    c.execute(exe)
    data = c.fetchall()
    c.close()
    return makeDiceList(data)


# remove a activetag by tagname from the DB
def removeActiveByNameAndTagType(tagName, tagType):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute('DELETE FROM tags_active WHERE TagName = (?) and TagType = (?)', (tagName, tagType))
    conn.commit()
    conn.close()


# remove the ActiveTag by index from the DB
def removeActiveByIndex(index):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute('DELETE FROM tags_active WHERE id = (?)', (index,))
    conn.commit()
    conn.close()


# removes timed tags that are timed out from the DB
def cleanActiveTime(time):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT * FROM tags_active WHERE TagType ='timed'")
    conn.commit()
    rows = c.fetchall()
    conn.close()
    for row in rows:
        data = pickle.loads(row[3])

        if data[0] is "":
            data[0] = time
            conn = sqlite3.connect(getDBPath())
            c = conn.cursor()
            c.execute("UPDATE tags_active SET Data = (?) Where id = (?)", (pickle.dumps(data), row[0]))
            conn.commit()
            conn.close()

        timeToStop = ""
        if data[2] == "m":
            timeToStop = data[0] + timedelta(minutes=int(data[1]))
        elif data[2] == "h":
            timeToStop = data[0] + timedelta(hours=int(data[1]))

        if time > timeToStop:
            removeActiveByIndex(row[0])


# Remove single use tags from the DB
def cleanActiveSingles():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute('DELETE FROM tags_active WHERE TagType = "single"')
    conn.commit()
    conn.close()


# todo make this return a list of strings
# gets all the active tags from the DB
def getActiveTagsNames():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT tagName FROM tags_active")
    conn.commit()
    rows = c.fetchall()
    conn.close()
    return rows

def getActiveTags():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT UserID, TagName, TagType, Data, Avatar, Self FROM tags_active")
    conn.commit()
    rows = c.fetchall()
    conn.close()
    return makeActiveList(rows)


# todo make this return a list of strings
# this will clean the Db of old tags and update the self tags with the player id
# if player ID is None returns only the game tag not the self tags
# returns all the activeTags
def getActiveTagsAndUpdate(playerID, time):
    cleanActiveTime(time)
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute('UPDATE tags_active SET UserID = (?) WHERE UserID = "" AND self = 1', (playerID,))
    c.execute("SELECT tagName FROM tags_active WHERE UserID = (?) OR self = 0", (playerID,))
    conn.commit()
    rows = c.fetchall()
    conn.close()
    cleanActiveSingles()
    return rows


# removes a Active tag by name
def endtag(tagName):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute('DELETE FROM tags_active WHERE TagName = (?)', (tagName,))
    conn.commit()
    conn.close()


# removes all active tags
def endAlltag():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("DELETE FROM tags_active")
    conn.commit()
    conn.close()


# gets all the messages it a tags name
def getMessagesWithTags(tagName):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    exe = "SELECT {MT}.{MID}, {Type}, {BY} ,{UID},{FT}.{FID},{RF},{TotR},{Side},{Crit},{Roll} " \
          "FROM {MT} " \
          "LEFT JOIN {UT} " \
          "ON ({UT}.{MID} = {MT}.{MID}) " \
          "JOIN {FT} " \
          "ON ({FT}.{MID} = {MT}.{MID}) " \
          "JOIN {DFJT} " \
          "ON ({DFJT}.{FIDJ} = {FT}.{FID}) " \
          "JOIN {DT} " \
          "ON ({DT}.{DID} = {DFJT}.{DIDJ}) " \
          "JOIN {TT} " \
          "ON ({TT}.{MID} = {MT}.{MID})" \
          "WHERE {Tname} = (?)".format(
        MT=Message_table,
        FT=Formula_table,
        UT=User_table,
        DT=Dice_table,
        DFJT=Dice_Formula_junction_table,
        TT=Tag_table,

        MID=MessageID_field,
        BY=By_field,
        Type=MessageType_field,
        UID=UserID_field,
        RF=Roll_Formula_field,
        TotR=TotalRoll_field,
        Side=Sides_field,
        Crit=Crit_field,
        Roll=Roll_field,
        FID=Formula_ID_field,
        DIDJ=Dice_ID_field_JT,
        FIDJ=Formula_ID_field_JT,
        DID=Dice_ID_field,
        Tname=Tag_name_field

    )
    c.execute(exe, (tagName,))
    conn.commit()
    data = c.fetchall()
    conn.close()

    return makeDiceList(data)


def getMessagesWithTagsBYDate(tagName, dateTime):
    dateA = dateTime
    dateB = datetime(dateA.year, dateA.month, dateA.day, 23, 59, 59)
    return getMessagesWithTagsBYDateRange(tagName, dateA, dateB)


def getMessagesWithTagsBYDateRange(tagName, dateTimeA, dateTimeB):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    exe = "SELECT {MT}.{MID}, {Type}, {BY} ,{UID},{FT}.{FID},{RF},{TotR},{Side},{Crit},{Roll} " \
          "FROM {MT} " \
          "LEFT JOIN {UT} " \
          "ON ({UT}.{MID} = {MT}.{MID}) " \
          "JOIN {FT} " \
          "ON ({FT}.{MID} = {MT}.{MID}) " \
          "JOIN {DFJT} " \
          "ON ({DFJT}.{FIDJ} = {FT}.{FID}) " \
          "JOIN {DT} " \
          "ON ({DT}.{DID} = {DFJT}.{DIDJ}) " \
          "JOIN {TT} " \
          "ON ({TT}.{MID} = {MT}.{MID})" \
          "WHERE {Tname} = (?) " \
          "AND {Time} BETWEEN ? AND ?".format(
        MT=Message_table,
        FT=Formula_table,
        UT=User_table,
        DT=Dice_table,
        DFJT=Dice_Formula_junction_table,
        TT=Tag_table,

        MID=MessageID_field,
        BY=By_field,
        Type=MessageType_field,
        UID=UserID_field,
        RF=Roll_Formula_field,
        TotR=TotalRoll_field,
        Side=Sides_field,
        Crit=Crit_field,
        Roll=Roll_field,
        FID=Formula_ID_field,
        DIDJ=Dice_ID_field_JT,
        FIDJ=Formula_ID_field_JT,
        DID=Dice_ID_field,
        Tname=Tag_name_field,
        Time=Time_field

    )

    c.execute(exe, (tagName, dateTimeA, dateTimeB))
    conn.commit()
    data = c.fetchall()
    c.close()
    return makeDiceList(data)


# get date and return a tagnames from that date
def getTagNamesByDate(dateTime):
    dateA = dateTime
    dateB = datetime(dateA.year, dateA.month, dateA.day, 23, 59, 59)
    return getTagNamesByDateRange(dateA, dateB)


def getTagNamesByDateRange(dateTimeA, dateTimeB):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT Tags.TagName FROM Tags "
              "JOIN Message "
              "ON Message.MessageID = Tags.MessageID "
              "WHERE Time BETWEEN \"(?)\" AND \"(?)\" AND MessageType ='rollresult'", [dateTimeA, dateTimeB])
    conn.commit()
    data = c.fetchall()
    c.close()
    return data


# returns all the names that have every been used
def getAllNames():
    try:
        conn = sqlite3.connect(getDBPath())
    except(TypeError):
        return [""]
    c = conn.cursor()
    c.execute('SELECT DISTINCT BY FROM Message')
    conn.commit()
    data = c.fetchall()
    conn.close()
    listTurn = []
    for d in data:
        listTurn.append(d[0])
    return listTurn


# gets a name and returns all the message with the name
def getMessagesByName(name):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    exe = "SELECT {MT}.{MID}, {Type}, {BY} ,{UID},{FT}.{FID},{RF},{TotR},{Side},{Crit},{Roll} " \
          "FROM {MT} " \
          "LEFT JOIN {UT} " \
          "ON ({UT}.{MID} = {MT}.{MID}) " \
          "JOIN {FT} " \
          "ON ({FT}.{MID} = {MT}.{MID}) " \
          "JOIN {DFJT} " \
          "ON ({DFJT}.{FIDJ} = {FT}.{FID}) " \
          "JOIN {DT} " \
          "ON ({DT}.{DID} = {DFJT}.{DIDJ}) " \
          "WHERE {BY} = (?) ".format(
        MT=Message_table,
        FT=Formula_table,
        UT=User_table,
        DT=Dice_table,
        DFJT=Dice_Formula_junction_table,
        TT=Tag_table,

        MID=MessageID_field,
        BY=By_field,
        Type=MessageType_field,
        UID=UserID_field,
        RF=Roll_Formula_field,
        TotR=TotalRoll_field,
        Side=Sides_field,
        Crit=Crit_field,
        Roll=Roll_field,
        FID=Formula_ID_field,
        DIDJ=Dice_ID_field_JT,
        FIDJ=Formula_ID_field_JT,
        DID=Dice_ID_field,
    )

    c.execute(exe, (name,))
    conn.commit()
    data = c.fetchall()
    conn.close()

    return makeDiceList(data)


def getMessagesByNameByDate(name, dateTime):
    dateA = dateTime
    dateB = datetime(dateA.year, dateA.month, dateA.day, 23, 59, 59)
    return getMessagesByNameByDateRange(name, dateA, dateB)


def getMessagesByNameByDateRange(name, dateTimeA, dateTimeB):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    exe = "SELECT {MT}.{MID}, {Type}, {BY} ,{UID},{FT}.{FID},{RF},{TotR},{Side},{Crit},{Roll} " \
          "FROM {MT} " \
          "LEFT JOIN {UT} " \
          "ON ({UT}.{MID} = {MT}.{MID}) " \
          "JOIN {FT} " \
          "ON ({FT}.{MID} = {MT}.{MID}) " \
          "JOIN {DFJT} " \
          "ON ({DFJT}.{FIDJ} = {FT}.{FID}) " \
          "JOIN {DT} " \
          "ON ({DT}.{DID} = {DFJT}.{DIDJ}) " \
          "WHERE {BY} = (?) " \
          "AND {TIME} BETWEEN ? AND ?".format(
        MT=Message_table,
        FT=Formula_table,
        UT=User_table,
        DT=Dice_table,
        DFJT=Dice_Formula_junction_table,
        TT=Tag_table,

        MID=MessageID_field,
        BY=By_field,
        Type=MessageType_field,
        UID=UserID_field,
        RF=Roll_Formula_field,
        TotR=TotalRoll_field,
        Side=Sides_field,
        Crit=Crit_field,
        Roll=Roll_field,
        FID=Formula_ID_field,
        DIDJ=Dice_ID_field_JT,
        FIDJ=Formula_ID_field_JT,
        DID=Dice_ID_field,
        TIME=Time_field
    )

    c.execute(exe, (name, dateTimeA, dateTimeB))
    conn.commit()
    data = c.fetchall()
    c.close()
    return makeDiceList(data)


# get a taglist and a character name and returns all messages that have all of them
def getMessagesByTagAndName(tagNameList, name):
    exe = "SELECT {MT}.{MID}, {Type}, {BY} ,{UID},{FT}.{FID},{RF},{TotR},{Side},{Crit},{Roll} " \
          "FROM {MT} " \
          "LEFT JOIN {UT} " \
          "ON ({UT}.{MID} = {MT}.{MID}) " \
          "JOIN {FT} " \
          "ON ({FT}.{MID} = {MT}.{MID}) " \
          "JOIN {DFJT} " \
          "ON ({DFJT}.{FIDJ} = {FT}.{FID}) " \
          "JOIN {DT} " \
          "ON ({DT}.{DID} = {DFJT}.{DIDJ}) " \
          "JOIN {TT} " \
          "ON ({TT}.{MID} = {MT}.{MID}) " \
          "WHERE {BY} = (?) ".format(
        MT=Message_table,
        FT=Formula_table,
        UT=User_table,
        DT=Dice_table,
        DFJT=Dice_Formula_junction_table,
        TT=Tag_table,

        MID=MessageID_field,
        BY=By_field,
        Type=MessageType_field,
        UID=UserID_field,
        RF=Roll_Formula_field,
        TotR=TotalRoll_field,
        Side=Sides_field,
        Crit=Crit_field,
        Roll=Roll_field,
        FID=Formula_ID_field,
        DIDJ=Dice_ID_field_JT,
        FIDJ=Formula_ID_field_JT,
        DID=Dice_ID_field,
        TIME=Time_field
    )
    andTag = "And Tags.TagName = ? "

    exeVar = [name]

    for tag in tagNameList:
        exe = exe + andTag
        exeVar.append(tag)

    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute(exe, exeVar)
    conn.commit()
    data = c.fetchall()
    conn.close()
    return makeDiceList(data)


def getMessagesByTagAndNameByDate(tagNameList, name, dateTime):
    dateA = dateTime
    dateB = datetime(dateA.year, dateA.month, dateA.day, 23, 59, 59)
    return getMessagesByTagAndNameByDateRange(tagNameList, name, dateA, dateB)


def getMessagesByTagAndNameByDateRange(tagNameList, name, dateTimeA, dateTimeB):
    exe = "SELECT {MT}.{MID}, {Type}, {BY} ,{UID},{FT}.{FID},{RF},{TotR},{Side},{Crit},{Roll} " \
          "FROM {MT} " \
          "LEFT JOIN {UT} " \
          "ON ({UT}.{MID} = {MT}.{MID}) " \
          "JOIN {FT} " \
          "ON ({FT}.{MID} = {MT}.{MID}) " \
          "JOIN {DFJT} " \
          "ON ({DFJT}.{FIDJ} = {FT}.{FID}) " \
          "JOIN {DT} " \
          "ON ({DT}.{DID} = {DFJT}.{DIDJ}) " \
          "JOIN {TT} " \
          "ON ({TT}.{MID} = {MT}.{MID}) " \
          "WHERE {TIME} BETWEEN ? AND ? " \
          "AND {BY} = (?) ".format(
        MT=Message_table,
        FT=Formula_table,
        UT=User_table,
        DT=Dice_table,
        DFJT=Dice_Formula_junction_table,
        TT=Tag_table,

        MID=MessageID_field,
        BY=By_field,
        Type=MessageType_field,
        UID=UserID_field,
        RF=Roll_Formula_field,
        TotR=TotalRoll_field,
        Side=Sides_field,
        Crit=Crit_field,
        Roll=Roll_field,
        FID=Formula_ID_field,
        DIDJ=Dice_ID_field_JT,
        FIDJ=Formula_ID_field_JT,
        DID=Dice_ID_field,
        TIME=Time_field
    )

    exe = "SELECT Message.* FROM Message " \
          "JOIN Tags " \
          "ON Message.MessageID = Tags.MessageID " \
          "WHERE Time BETWEEN ? AND ? AND Message.by = ? AND MessageType ='rollresult' OR Time BETWEEN ? AND ? AND Message.by = ? AND MessageType='characterSheet'"
    andTag = " AND Tags.TagName = ? "

    exeVar = [dateTimeA, dateTimeB, name, dateTimeA, dateTimeB, name]

    for tag in tagNameList:
        exe = exe + andTag
        exeVar.append(tag)

    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute(exe, exeVar)
    conn.commit()
    data = c.fetchall()
    conn.close()

    return makeDiceList(data)


def getPlayerID():
    setTurn = set()
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute('SELECT DISTINCT UserID FROM Message WHERE MessageType="rollresult"')
    conn.commit()
    data = c.fetchall()
    conn.close()
    listTurn = []
    for d in data:
        set.add(d[0])
    return listTurn


# Print
#######################################################################################################################
# prints the DB
def printDB():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT * FROM Message")
    conn.commit()
    rows = c.fetchall()
    for row in rows:
        print(row)

    conn.close()


def printUserTable():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    exe = "SELECT * FROM " + User_table
    c.execute(exe)
    conn.commit()
    rows = c.fetchall()
    for row in rows:
        print(row)

    conn.close()


def printFormulaAndDiceJT():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    exe = "SELECT * FROM {JT}".format(
        FT=Formula_table,
        DT=Dice_table,
        FTID=Formula_ID_field,
        DTID=Dice_ID_field,
        JT=Dice_Formula_junction_table,
        DJID=Dice_ID_field_JT,
        FJID=Formula_ID_field_JT
    )
    print(exe)
    c.execute(exe)
    conn.commit()
    rows = c.fetchall()
    for row in rows:
        print(row)

    conn.close()


def printFormulaAndDice():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    exe = "SELECT * " \
          "FROM {JT} " \
          "JOIN {FT} " \
          "ON ({JT}.{FJID} = {FT}.{FTID}) " \
          "JOIN {DT} " \
          "ON ({JT}.{DJID} = {DT}.{DTID})".format(
        FT=Formula_table,
        DT=Dice_table,
        FTID=Formula_ID_field,
        DTID=Dice_ID_field,
        JT=Dice_Formula_junction_table,
        DJID=Dice_ID_field_JT,
        FJID=Formula_ID_field_JT
    )
    c.execute(exe)
    conn.commit()
    rows = c.fetchall()
    for row in rows:
        print(row)

    conn.close()


# pints all the tags that have ever been used in the DB
def printDBAlltags():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT * FROM AllTags")
    conn.commit()
    rows = c.fetchall()
    for row in rows:
        print(row)
    conn.close()


# prints all the active tags in the DB
def printDBActiveTags():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT * FROM tags_active")
    conn.commit()
    rows = c.fetchall()
    for row in rows:
        print(row)
    conn.close()


# prints the Roleresults
def printDBRoleresult():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT * FROM Message WHERE MessageType='rollresult'")
    conn.commit()
    rows = c.fetchall()
    for row in rows:
        print(row)

    conn.close()


# prints the gameData from the DB
def printDBData():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT * FROM gameData")
    conn.commit()
    rows = c.fetchall()
    for row in rows:
        print(row)

    conn.close()


# prints the tags table
def printTags():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT * FROM Tags")
    conn.commit()
    rows = c.fetchall()
    for row in rows:
        print(row)

    conn.close()
