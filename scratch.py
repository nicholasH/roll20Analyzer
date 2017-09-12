from tkinter import *
from tkinter import ttk

def calculate():
    pass

root = Tk()
root.title("Feet to Meters")



mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0)
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)


ttk.Button(mainframe, text="run", command=calculate).grid(column=1, row=1)
ttk.Button(mainframe, text = "today").grid(column=2,row =1)




root.mainloop()