import os
import sys
from tkinter import filedialog
from tkinter import *


#start a tag
import sqlite3

import DBhandler

"^"
#the word affter the & is the tag name. A tag like this will only work the the next roll
"^tag"

#this  tag will tag every post for the next 24 hours
'^tag -24h'

#this will tag every thing in the next 60 min
'^tag -24m'

#this tag will tag all post with out end
'^tag -start'

#this is end a tag by this tag name
'^tag -end'

#this will end all tags for every one
'^tag -endall'

#this make tags only for the oneself
'^tag -self'
'^tag -24m -self'
'^tag -start -self'


#bad inputs
'^ -'
'^tag -start -do'
'^tag -4543 -self'

test = 'lool ^^tag -test ^test'

r = re.search(r'\^\w+( *-\w+){0,2}',test)

print(r.group())

test2 = 'endall'
print('end' in test)
print('end' in test2)
print(int(True))


