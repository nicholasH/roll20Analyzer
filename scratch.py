from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException

EMAIL = 'add email'
PASSWORD = 'add password'



URL = 'https://app.roll20.net/sessions/new'
jarUrl = 'https://app.roll20.net/campaigns/chatarchive/1610304'
URL2 = 'https://app.roll20.net/campaigns/chatarchive/1644807'

gitUrl  = 'https://github.com/login'
gitUrl2 = 'https://github.com/settings/emails'


browser = webdriver.Chrome("C:\\Users\\Nick\\Documents\GitHub\\roll20Analyzer\\chromedriver.exe")
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

html = browser.page_source
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