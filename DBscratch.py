import sqlite3


def creatDB():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE test
                 (id INTEGER PRIMARY KEY,name text)''')

    conn.commit()
    conn.close()

def dis():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS test')

    conn.commit()
    conn.close()

def printDB():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("SELECT * FROM test")
    conn.commit()
    rows = c.fetchall()
    for row in rows:
        print(row)

    conn.close()

#creatDB()
print("end")
testname = [('bill'),
            ('tom'),
            ('kyle'),
            ('tom'),]

conn = sqlite3.connect('example.db')
c = conn.cursor()

t = 'tddm'
c.execute('INSERT OR IGNORE INTO test (name) VALUES (?)', (t,))
conn.commit()
conn.close()

printDB()