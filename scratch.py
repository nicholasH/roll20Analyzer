import os
import sys
from threading import Thread
from tkinter import filedialog, ttk
import tkinter as tk
from tkinter.ttk import Combobox

import time

import DBhandler
import DBscratch
import analyze

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





class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.button = ttk.Button(text="start", command=self.start)
        self.button.pack()
        self.progress = ttk.Progressbar(self, orient="horizontal",
                                        length=200, mode="determinate")
        self.progress.pack()

        self.bytes = 0
        self.maxbytes = 0

    def start(self):
        self.progress["value"] = 0
        self.maxbytes = 50000
        self.progress["maximum"] = 50000
        self.read_bytes()

    def read_bytes(self):
        '''simulate reading 500 bytes; update progress bar'''
        self.bytes += 500
        self.progress["value"] = self.bytes
        if self.bytes < self.maxbytes:
            # read more bytes after 100 ms
            self.after(100, self.read_bytes)

app = SampleApp()
app.mainloop()