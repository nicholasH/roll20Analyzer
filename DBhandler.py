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


def createDB():
    conn = sqlite3.connect('Chatlog.db')
    c = conn.cursor()
    # Creating a new SQLite table with 1 column
    c.execute(
        'CREATE TABLE {tn} ({MID} {fts}, {MT} {fts},  {UI} {fts},{By} {fts}, {AV} {fts}, {TF} {ftts}, {TAD} {ftd}, {RF} {fts}, {RL} {fts}, {Roll} {fti}, {Text} {fts})'
            .format(tn=Message_table,
                    MID=MessageID_field,
                    MT=MessageType_field,
                    UI=UserID_field,
                    By=By_field,
                    AV=Avatar_field,
                    TF=Time_field,
                    TAD=TimeAddedToDB_field,
                    RF=RolledFormula_field,
                    RL=RolledResultsList_field,
                    Roll=Rolled_Field,
                    Text=Text_Field
                    , fts=string_field_type, fti=integer_field_type, ftd=Date_field_type, ftts= Tstamp_field))
    conn.close()


def destroyDB():
    conn = sqlite3.connect('Chatlog.db')
    c = conn.cursor()
    c.execute('drop table if exists ' + Message_table)
    conn.commit()
    conn.close()


def addMessage(messageDic: dict):
    conn = sqlite3.connect('Chatlog.db')
    c = conn.cursor()

    c.execute(
        "INSERT INTO Message VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
            messageDic.get(MessageID_field),
            messageDic.get(MessageType_field),
            messageDic.get(UserID_field),
            messageDic.get(By_field),
            messageDic.get(Avatar_field),
            messageDic.get(Time_field),
            messageDic.get(TimeAddedToDB_field),
            messageDic.get(RolledFormula_field),
            pickle.dumps(messageDic.get(RolledResultsList_field)),
            messageDic.get(Rolled_Field),
            messageDic.get(Text_Field)
        ))
    conn.commit()
    conn.close()


def getMessage(messageObj):
    print("need to make")


def printDB():
    conn = sqlite3.connect('Chatlog.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Message")
    print(c.fetchall())
    conn.close()