import os
import sys
from tkinter import filedialog, ttk
from tkinter import *
from tkinter.ttk import Combobox

from apply import apply

import DBhandler

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




class App:

    value_of_combo = 'X'


    def __init__(self, parent):
        self.parent = parent
        self.combo()

    def combo(self):
        self.box_value = StringVar()
        self.box = ttk.Combobox(self.parent, textvariable=self.box_value)
        self.box['values'] = ('X', 'Y', 'Z')
        self.box.current(0)
        self.box.grid(column=0, row=0)
        self.run_all_btn = Button(self.parent, text="run all", command=self.run)
        self.run_all_btn.grid(column=0, row=1)

    def run(self):
        print(self.box.get())

if __name__ == '__main__':
    root = Tk()
    app = App(root)
    root.mainloop()