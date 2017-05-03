import os
import time

import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException




path = os.path.join(sys.path[0], "config")

f = open(path)
EMAIL = ''
PASSWORD = ''
for line in f:
        if "Email:" in line:
            EMAIL = line.split("Email:")[1].strip()
        if "Password:" in line:
            PASSWORD = line.split("Password:")[1].strip()
print(EMAIL + PASSWORD)

f.close()





URL = 'https://app.roll20.net/sessions/new'
jarUrl = 'https://app.roll20.net/campaigns/chatarchive/1610304'
URL2 = 'https://app.roll20.net/campaigns/chatarchive/1644807'

chromeDriver = os.path.join(sys.path[0],"chromedriver.exe")
browser = webdriver.Chrome(chromeDriver)
browser.set_window_size(20, 20)
browser.set_window_position(50, 50)
browser.get(URL)

usernameElements = browser.find_elements_by_name("email")
passwordElements = browser.find_elements_by_name("password")

for e in usernameElements:
    try:
        e.send_keys(EMAIL)
    except ElementNotVisibleException:
        print()


for e in passwordElements:
    try:
        e.send_keys(PASSWORD)
    except ElementNotVisibleException:
        print()

test = browser.find_element_by_class_name("calltoaction").click()
browser.get(jarUrl)
time.sleep(10)

html = browser.page_source
browser.close()




soup = BeautifulSoup(html)



print(soup)



'''
browser = RoboBrowser()


browser.open(URL)
forms = browser.get_forms()
form = forms[0]

form['email'].value = EMAIL
form['password'].value = PASSWORD
browser.submit_form(form)

browser.open(jarUrl)


data = browser.session



print(data)
'''







'''
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
'''