import os
from tkinter import filedialog
from tkinter import *


#start a tag
"&"
#the word affter the & is the tag name. A tag like this will only work the the next roll
"&tag"

#this  tag will tag every post for the next 24 hours
'&tag -24h'

#this will tag every thing in the next 60 min
'&tag -24m'

#this tag will tag all post with out end
'&tag -start'

#this is end a tag by this tag name
'&tag -end'

#this will end all tags for every one
'&tag -endall'

#this make tags only for the oneself
'&tag -self'
'&tag -24m -self'