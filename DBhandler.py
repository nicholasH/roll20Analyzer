import os
import sqlite3
from datetime import datetime, date, timedelta
import pickle
import errors
import sys

# messageTable
Message_table = 'Message'

MessageID_field = "MessageID"
MessageType_field = "MessageType"

UserID_field = 'UserID'
By_field = 'BY'

Avatar_field = "Avatar"

Time_field = "Time"
TimeAddedToDB_field = "TimeAddedToDB"

RolledFormula_field = "RolledFormula"
RolledResultsList_field = "RolledResultsList"
Rolled_Field = "Rolled"

Text_Field = "Text"

integer_field_type = 'INTEGER'
string_field_type = 'STRING'
Date_field_type = "date"
Tstamp_field = 'timestamp'

columnName = [MessageID_field,
              MessageType_field,
              Avatar_field,
              UserID_field,
              By_field,
              Time_field,
              TimeAddedToDB_field,
              RolledFormula_field,
              RolledResultsList_field,
              Rolled_Field]

# game Table
GameData_table = 'gameData'
GameName_feild = 'name'
GameUrl_feild = 'url'

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

# tagName
All_tags_table = 'AllTags'
all_tags_tag_names_feild = Tag_Active_name_field


global db
db = None


# creates all the DBs tables and sets the metaData for the DB
def createDB(name, url):
    setDB(name)
    createMessageTable()
    createGameDataTable()
    createTagTable()
    createActiveTageTable()
    createAlltagsTable()

    setdata(name, url)


# creates the messageTable
def createMessageTable():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()

    c.execute(
        'CREATE TABLE {tn} ({MID} {fts} PRIMARY KEY, {MT} {fts}, {AVA} {fts}, {UI} {fts}, {By} {fts}, {TF} {ftts}, {TAD} {ftd}, {RF} {fts}, {RL} {fts}, {Roll} {fts})'
            .format(tn=Message_table,
                    MID=MessageID_field,
                    MT=MessageType_field,
                    AVA=Avatar_field,
                    UI=UserID_field,
                    By=By_field,
                    TF=Time_field,
                    TAD=TimeAddedToDB_field,
                    RF=RolledFormula_field,
                    RL=RolledResultsList_field,
                    Roll=Rolled_Field

                    , fts=string_field_type, fti=integer_field_type, ftd=Date_field_type, ftts=Tstamp_field))
    conn.close()


# creates the GameDataTable
def createGameDataTable():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    exe = "CREATE TABLE {tn} ({n} {fts}, {url} {fts})".format(
        tn=GameData_table,
        n=GameName_feild,
        url=GameUrl_feild,
        fts=string_field_type
    )
    c.execute(exe)
    conn.close()


# creates the Tag table
def createTagTable():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    exe = "CREATE TABLE {tn} ({mf} {fts}, {tan} {fts})".format(
        tn=Tag_table,
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


# A table that conatans all tag names that has been used in the game
def createAlltagsTable():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    exe = "CREATE TABLE {tn} ({ta} {fts} PRIMARY KEY)".format(
        tn=All_tags_table,
        ta=Tag_Active_name_field,

        fts=string_field_type
    )
    c.execute(exe)
    conn.close()


# sets the meta data of the game
def setdata(name, url):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("INSERT INTO gameData VALUES (?,?)", (name, url))
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


def getDBPath():
    if db == "" or db == None:
        raise errors.DBNotLoaded
    return db


# Destroys the DB
def destroyDB():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS ' + Message_table)
    c.execute('DROP TABLE IF EXISTS ' + GameData_table)
    c.execute('DROP TABLE IF EXISTS ' + tag_active_table)
    c.execute('DROP TABLE IF EXISTS ' + Tag_table)
    c.execute('DROP TABLE IF EXISTS ' + All_tags_table)

    conn.commit()
    conn.close()


# adds a single message to the db
# gets a dict with all message feilds it add it to the db
#todo refactor my code so diffent messagetypes have diffent table
#todo add a table for individual rolls
def addMessage(messageDic: dict):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute(
        "INSERT OR IGNORE INTO Message VALUES (?,?,?,?,?,?,?,?,?,?)", (
            messageDic.get(MessageID_field),
            messageDic.get(MessageType_field),
            messageDic.get(Avatar_field),
            messageDic.get(UserID_field),
            messageDic.get(By_field),
            messageDic.get(Time_field),
            messageDic.get(TimeAddedToDB_field),
            messageDic.get(RolledFormula_field),
            pickle.dumps(messageDic.get(RolledResultsList_field)),
            messageDic.get(Rolled_Field),
        ))
    conn.commit()
    conn.close()


# Gets all the message in the DB and returns a list
def getMessages():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT * FROM Message")
    conn.commit()
    data = c.fetchall()
    conn.close()

    return makeList(data)


# returns a list of all rollresults
def getMessagesRolls():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT * FROM Message WHERE MessageType='rollresult' OR MessageType='characterSheet'")
    conn.commit()
    data = c.fetchall()
    conn.close()
    return makeList(data)


def makeList(data):
    listTurn = list()

    for datum in data:
        dic = dict(zip(columnName, datum))
        dic[RolledResultsList_field] = pickle.loads(dic[RolledResultsList_field])
        listTurn.append(dic)

    return listTurn


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

#pints all the tags that have ever been used in the DB
def printDBAlltags():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT * FROM AllTags")
    conn.commit()
    rows = c.fetchall()
    for row in rows:
        print(row)
    conn.close()

#prints all the active tags in the DB
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

#prints the gameData from the DB
def printDBData():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT * FROM gameData")
    conn.commit()
    rows = c.fetchall()
    for row in rows:
        print(row)

    conn.close()

#prints the tags table
def printTags():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT * FROM Tags")
    conn.commit()
    rows = c.fetchall()
    for row in rows:
        print(row)

    conn.close()

#get the url or the gamedata
def getURL():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT url FROM gameData")
    conn.commit()
    url = c.fetchone()
    conn.close()
    return url[0]

def getGameNumber():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT url FROM gameData")
    conn.commit()
    url = c.fetchone()
    conn.close()
    return str(url[0]).split("/")[-1]


#get the name of the game
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
    exe = "SELECT * FROM {tn} WHERE {tf} BETWEEN \"{DA}\" AND \"{DB}\" AND {mt}='rollresult' OR {tf} BETWEEN \"{DA}\" AND \"{DB}\" AND {mt}='characterSheet'".format(
        tn=Message_table,
        tf=Time_field,
        mt=MessageType_field,
        DA=dateTimeA,
        DB=dateTimeB)

    c.execute(exe)
    data = c.fetchall()
    c.close()
    return makeList(data)


# add a tag to alltags table
def addAllTags(tagName):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO AllTags VALUES (?)', (tagName,))
    conn.commit()
    conn.close()

#gets a list of all tags that have been ever used
def getAlltags():
    try:
        conn = sqlite3.connect(getDBPath())
    except(TypeError):
        return [""]

    c = conn.cursor()
    c.execute('SELECT * FROM AllTags')
    conn.commit()
    data = c.fetchall()
    conn.close()
    listTurn = []
    for d in data:
        listTurn.append(d[0])
    return listTurn

# gets array of tagDetails and addeds the tag to the active tag table
# tagArray is a list  that can inclued one - three items
def addTagActive(tagName, tagType, tagDetails,Avatar, self):
    addAllTags(tagName)
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute(
        "INSERT INTO tags_active (TagName, TagType, Data, Self,  Avatar, UserID)VALUES (?,?,?,?,?,?)", (
            tagName,
            tagType,
            pickle.dumps(tagDetails),
            int(self),
            Avatar,
            ""
        ))
    conn.commit()
    conn.close()

#remove a activetag by tagname from the DB
def removeActiveByNameAndTagType(tagName, tagType):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute('DELETE FROM tags_active WHERE TagName = (?) and TagType = (?)', (tagName, tagType))
    conn.commit()
    conn.close()

#remove the ActiveTag by index from the DB
def removeActiveByIndex(index):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute('DELETE FROM tags_active WHERE id = (?)', (index,))
    conn.commit()
    conn.close()

#removes timed tags that are timed out from the DB
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

#Remove single use tags from the DB
def cleanActiveSingles():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute('DELETE FROM tags_active WHERE TagType = "single"')
    conn.commit()
    conn.close()

#todo make this return a list of strings
#gets all the active tags from the DB
def getActiveTagsNames():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT tagName FROM tags_active")
    conn.commit()
    rows = c.fetchall()
    conn.close()
    return rows

#todo make this return a list of strings
# this will clean the Db of old tags and update the self tags with the player id
# if player ID is None returns only the game tag not the self tags
#returns all the activeTags
def getActiveTagsAndUpdate(playerID,time):
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

#get messageID and playerID and adds all active tags to the DB and assosiates them with the MessageID
def addtag(messageID, playerID,tstamp):
    tags = list(set(getActiveTagsAndUpdate(playerID,tstamp)))
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



#removes a Active tag by name
def endtag(tagName):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute('DELETE FROM tags_active WHERE TagName = (?)', (tagName,))
    conn.commit()
    conn.close()

#removes all active tags
def endAlltag():
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("DELETE FROM tags_active")
    conn.commit()
    conn.close()

#gets all the messages it a tags name
def getMessagesWithTags(tagName):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT Message.* FROM Message "
              "JOIN Tags "
              "ON Message.MessageID = Tags.MessageID "
              "WHERE Tags.TagName = (?)",(tagName,))
    conn.commit()
    data = c.fetchall()
    conn.close()

    return makeList(data)

def getMessagesWithTagsBYDate(tagName,dateTime):
    dateA = dateTime
    dateB = datetime(dateA.year, dateA.month, dateA.day, 23, 59, 59)
    return getMessagesWithTagsBYDateRange(tagName,dateA, dateB)



def getMessagesWithTagsBYDateRange(tagName,dateTimeA,dateTimeB):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT Message.* FROM Message "
              "JOIN Tags "
              "ON Message.MessageID = Tags.MessageID "
              "WHERE Tags.TagName = ?"
              "AND Time BETWEEN ? AND ?",(tagName,dateTimeA,dateTimeB))
    conn.commit()
    data = c.fetchall()
    c.close()
    return makeList(data)

#get date and return a tagnames from that date
def getTagNamesByDate(dateTime):
    dateA = dateTime
    dateB = datetime(dateA.year, dateA.month, dateA.day, 23, 59, 59)
    return getTagNamesByDateRange(dateA, dateB)

def getTagNamesByDateRange(dateTimeA,dateTimeB):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT Tags.TagName FROM Tags "
              "JOIN Message "
              "ON Message.MessageID = Tags.MessageID "
              "WHERE Time BETWEEN \"(?)\" AND \"(?)\" AND MessageType ='rollresult'",[dateTimeA,dateTimeB])
    conn.commit()
    data = c.fetchall()
    c.close()
    return data

#returns all the names that have every been used
def getAllNames():
    try:
        conn = sqlite3.connect(getDBPath())
    except(TypeError):
        return [""]
    c = conn.cursor()
    c.execute('SELECT DISTINCT BY FROM Message WHERE MessageType="rollresult" OR MessageType="characterSheet"')
    conn.commit()
    data = c.fetchall()
    conn.close()
    listTurn = []
    for d in data:
        listTurn.append(d[0])
    return listTurn

#gets a name and returns all the message with the name
def getMessagesByName(name):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT * FROM Message WHERE By = (?) AND MessageType ='rollresult' OR By = (?) AND MessageType='characterSheet'",(name,name))
    conn.commit()
    data = c.fetchall()
    conn.close()

    return makeList(data)

def getMessagesByNameByDate(name,dateTime):
    dateA = dateTime
    dateB = datetime(dateA.year, dateA.month, dateA.day, 23, 59, 59)
    return getMessagesByNameByDateRange(name,dateA, dateB)

def getMessagesByNameByDateRange(name,dateTimeA,dateTimeB):
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute("SELECT * FROM Message "
              "WHERE By = ? "
              "AND Time BETWEEN ? AND ? AND MessageType ='rollresult' "
              "OR By = ? "
              "AND Time BETWEEN ? AND ? "
              "AND MessageType='characterSheet'",(name,dateTimeA,dateTimeB,name,dateTimeA,dateTimeB))
    conn.commit()
    data = c.fetchall()
    c.close()
    return makeList(data)

#get a taglist and a character name and returns all messages that have all of them
def getMessagesByTagAndName(tagNameList,name):
    exe = "SELECT Message.* FROM Message "\
              "JOIN Tags "\
              "ON Message.MessageID = Tags.MessageID "\
              "WHERE (Message.by = ? AND MessageType ='rollresult' OR Message.by = ? AND MessageType ='characterSheet') "
    andTag = "And Tags.TagName = ? "

    exeVar = [name,name]

    for tag in tagNameList:
        exe = exe + andTag
        exeVar.append(tag)

    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute(exe, exeVar)
    conn.commit()
    data = c.fetchall()
    conn.close()
    return makeList(data)

def getMessagesByTagAndNameByDate(tagNameList,name,dateTime):
    dateA = dateTime
    dateB = datetime(dateA.year, dateA.month, dateA.day, 23, 59, 59)
    return getMessagesByTagAndNameByDateRange(tagNameList,name,dateA, dateB)

def getMessagesByTagAndNameByDateRange(tagNameList,name,dateTimeA,dateTimeB):
    exe = "SELECT Message.* FROM Message "\
              "JOIN Tags "\
              "ON Message.MessageID = Tags.MessageID "\
              "WHERE Time BETWEEN ? AND ? AND Message.by = ? AND MessageType ='rollresult' OR Time BETWEEN ? AND ? AND Message.by = ? AND MessageType='characterSheet'"
    andTag = " AND Tags.TagName = ? "

    exeVar = [dateTimeA,dateTimeB,name,dateTimeA,dateTimeB,name]

    for tag in tagNameList:
        exe = exe + andTag
        exeVar.append(tag)

    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()
    c.execute(exe, exeVar)
    conn.commit()
    data = c.fetchall()
    conn.close()

    return makeList(data)

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


