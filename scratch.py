import os
import sys
from threading import Thread
from tkinter import filedialog, ttk
import tkinter as tk
from tkinter.ttk import Combobox

import time

import DBhandler
import analyze
from collections import Counter
import random

"^"
#the word after the ^ is the tag name. A tag like this will only work the the next roll
"^tag"

#this  tag will tag every post for the next 24 hours, time starts at the next time given
#the game must be analyzed after the time is done
'^tag -24h' #todo consider make timeDeta by real time and tstamps

#this will tag every thing in the next 60 min. This might fail if the number of min is too low and the time has not updated.
#the game must be analyzed after the time is done
#every 6 roll times updates
#todo find the min time need for a update
'^tag -24m'

#this tag will tag all post with out end
'^tag -start'

#this is end a tag by this tag name
'^tag -end'

#this will end all tags for every one
'^tag -endall'

'^ -endall'

#this make tags only for the oneself
'^tag -self'
'^tag -24m -self'
'^tag -start -self'


#bad inputs
'^ -'
'^tag -start -do'
'^tag -4543 -self'

#todo add a way to excuded tags


count = Counter()

count["test"] =+1

print(0/4)

print(list(range(5,6)))


roll = 10000000
t=0
totElam = 0
totsf = 0
totps = 0

"""
for r in range(0,roll):
    eldam1 = random.randint(1,10)
    eldam2 = random.randint(1,10)
    eldam3 = random.randint(1,10)

    eldam = eldam1 + eldam2 + eldam3 + 5
    totElam = totElam + eldam

    sf1 = random.randint(1,8)
    sf2 = random.randint(1,8)
    sf3 = random.randint(1,8)

    sf = sf1 + sf2 + sf3 + 4
    totsf = totsf + sf


    ps1 = random.randint(1,12)
    ps2 = random.randint(1,12)
    ps3 = random.randint(1,12)

    ps = ps1 + ps2 + ps3
    totps = totps + ps


print(totElam/roll)
print(totsf/roll)
print(totps/roll)
"""

tests = [0,1,2,3,4,5,6,7,8,9,10]
index = 0

for test in tests:
    if test == 3:
        tests.remove(index)
    print(index,test)
    index +=1
print(tests)

