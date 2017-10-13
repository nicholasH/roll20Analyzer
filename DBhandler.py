import os
import sqlite3
from datetime import datetime, date, timedelta
import pickle

import sys

Message_table = 'Message'
GameData_table = 'gameData'

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
              UserID_field,
              By_field,
              Time_field,
              TimeAddedToDB_field,
              RolledFormula_field,
              RolledResultsList_field,
              Rolled_Field]


#tag table
Tag_table = "tags"
MessageID_tag_field = MessageID_field
Tag_name_field = "TagName"



tag_active_table = "tags_active"
Tag_Active_name = Tag_name_field
tag_type = "tagType"
tag_data = "Data"


"""
roll is a string because some rolls might have more than just ints, ex 1d20<0 will aways roll 1 successes
"""
global db
db = None

# todo test if changeing roll to fts to fti made any errors
def createDB(name,url):

    setDB(name)

    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute(
        'CREATE TABLE {tn} ({MID} {fts}, {MT} {fts},  {UI} {fts},{By} {fts}, {TF} {ftts}, {TAD} {ftd}, {RF} {fts}, {RL} {fts}, {Roll} {fts})'
            .format(tn=Message_table,
                    MID=MessageID_field,
                    MT=MessageType_field,
                    UI=UserID_field,
                    By=By_field,

                    TF=Time_field,
                    TAD=TimeAddedToDB_field,
                    RF=RolledFormula_field,
                    RL=RolledResultsList_field,
                    Roll=Rolled_Field

                    , fts=string_field_type, fti=integer_field_type, ftd=Date_field_type, ftts=Tstamp_field))


    exe = "CREATE TABLE {tn} (name {fts}, url {fts})".format(
        tn=GameData_table,
        fts=string_field_type
    )
    c.execute(exe)


    exe = "CREATE TABLE {tn} ({mf} {fts}, {tan} {fts})".format(
        tn=Tag_table,
        mf=MessageID_tag_field,
        tan=Tag_name_field,
        fts=string_field_type
    )
    c.execute(exe)

    exe = "CREATE TABLE {tn} ({ta} {fts}, {tt} {fts}, {td} {fts})".format(
        tn=tag_active_table,
        ta=Tag_Active_name,
        tt=tag_type,
        td=tag_data,
        fts=string_field_type
    )


    conn.close()
    setdata(name,url)


def createTagTable():
    pass

def setdata(name,url):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute("INSERT INTO gameData VALUES (?,?)",(name,url))

    conn.commit()
    conn.close()

def loadDB(path):
    global db
    db = path

def setDB(name):
    global db
    dbName = name +'.db'
    db = os.path.join(sys.path[0], "data", "dataBase", dbName)


def getDBPath():
    return db


def destroyDB():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS ' + Message_table)
    c.execute('DROP TABLE IF EXISTS ' + GameData_table)
    conn.commit()
    conn.close()


def addMessage(messageDic: dict):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute(
        "INSERT INTO Message VALUES (?,?,?,?,?,?,?,?,?)", (
            messageDic.get(MessageID_field),
            messageDic.get(MessageType_field),
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


"""Gets all the message in the DB"""


def getMessages():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT * FROM Message")
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



def printDB():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT * FROM Message")
    conn.commit()
    rows = c.fetchall()
    for row in rows:
        print(row)

    conn.close()

def printDBData():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT * FROM gameData")
    conn.commit()
    rows = c.fetchall()
    for row in rows:
        print(row)

    conn.close()

def getURL():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT url FROM gameData")
    conn.commit()
    url = c.fetchone()
    conn.close()
    return url[0]

def getGameName():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT name FROM gameData")
    conn.commit()
    name = c.fetchone()
    conn.close()
    return name[0]


def getlastMessage():
    conn = sqlite3.connect(db)
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
def getMessageDateTime(dateTime):
    dateA = dateTime
    dateB = datetime(dateA.year, dateA.month, dateA.day, 23, 59, 59)
    return getMessageDateTimeRange(dateA,dateB)

#get two date time objects and gets the range of them
def getMessageDateTimeRange(dateTimeA, dateTimeB):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    exe = "SELECT * FROM {tn} WHERE {tf} BETWEEN \"{DA}\" AND \"{DB}\"".format(
        tn=Message_table,
        tf=Time_field,
        DA=dateTimeA,
        DB=dateTimeB)

    c.execute(exe)
    data = c.fetchall()
    c.close()


    return makeList(data)
