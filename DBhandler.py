import sqlite3
from datetime import datetime, date, timedelta
import pickle

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
              UserID_field,
              By_field,
              Time_field,
              TimeAddedToDB_field,
              RolledFormula_field,
              RolledResultsList_field,
              Rolled_Field]





"""


roll is a string because some rolls might have more than just ints, ex 1d20<0 will aways roll 1 successes
"""

#todo test if changeing roll to fts to fti made any errors
def createDB():
    conn = sqlite3.connect('Chatlog.db')
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

                    , fts=string_field_type, fti=integer_field_type, ftd=Date_field_type, ftts= Tstamp_field))
    conn.close()


def destroyDB():
    conn = sqlite3.connect('Chatlog.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS ' + Message_table)
    conn.commit()
    conn.close()


def addMessage(messageDic: dict):
    conn = sqlite3.connect('Chatlog.db')
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

    conn = sqlite3.connect('Chatlog.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Message")
    conn.commit()
    data = c.fetchall()
    conn.close()

    listTurn = list()

    for datum in data:

        dic = dict(zip(columnName, datum))
        dic[RolledResultsList_field] = pickle.loads(dic[RolledResultsList_field])
        listTurn.append(dic)

    return listTurn


def printDB():
    conn = sqlite3.connect('Chatlog.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Message")
    conn.commit()
    rows = c.fetchall()
    for row in rows:
        print(row)

    conn.close()

def getlastMessage():
    conn = sqlite3.connect('Chatlog.db')
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

def getMessagesDate(dateString):
    year = datetime.today().year

    d = dateString + "/" + str(year)


    dateA = datetime.strptime(d,"%m/%d/%Y")
    dateB = dateA + timedelta(hours=24)



    conn = sqlite3.connect('chatlog.db')
    c = conn.cursor()
    c.execute("SELECT * FROM {tn} WHERE {tf} BETWEEN {DA} AND {DB}".format(
        tn = Message_table,
        tf = Time_field,
        DA = dateA.strftime("%Y-%m-%d"),
        DB = dateB.strftime("%Y-%m-%d")
    ))
    return c.fetchall()

