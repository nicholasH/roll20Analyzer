import os
from tkinter import filedialog
from tkinter import *

db = os.path.join(os.sys.path[0], "data", "dataBase")

root = Tk()


root.filename = filedialog.askopenfilename(initialdir=db, title="Select file",
                                           filetypes=(("db files", "*.db"), ("all files", "*.*")))
print(root.filename)