import sqlite3

Roll_table = 'Roll'

UserID_field = 'UserID'

integer_field_type = 'INTEGER'
string_field_type = 'STRING'


# Connecting to the database file
conn = sqlite3.connect('Chatlog.db')
c = conn.cursor()

# Creating a new SQLite table with 1 column
c.execute('CREATE TABLE {tn} ({nf} {ft})'\
        .format(tn=Roll_table, nf=UserID_field, ft=integer_field_type))

# Creating a second table with 1 column and set it as PRIMARY KEY
# note that PRIMARY KEY column must consist of unique values!
c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
        .format(tn=table_name2, nf=new_field, ft=field_type))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()