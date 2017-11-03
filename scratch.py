import os
import sys
from tkinter import filedialog
from tkinter import *
from apply import apply

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



# the constructor syntax is:
# OptionMenu(master, variable, *values)

OPTIONS = [
    "egg",
    "bunny",
    "chicken"
]

master = Tk()

variable = StringVar(master)
variable.set(OPTIONS[0]) # default value

w = apply(OptionMenu, (master, variable) + tuple(OPTIONS))
w.pack()

mainloop()

