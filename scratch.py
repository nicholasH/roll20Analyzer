from tkinter import *
from tkinter import ttk

def calculate():
    try:
        value = float(feet.get())
        meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass

def limitSizeDay(*args):
    value = dayValue.get()
    if len(value) > 2: dayValue.set(value[:2])
    if value in '0123456789.-+':
        try:
            float(value)
            return True
        except ValueError:
            return False
    else:
        return False





root = Tk()
root.title("Feet to Meters")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0)
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

dayValue = StringVar()
dayValue.trace('w', limitSizeDay)
day_entry1=Entry(mainframe, width=2, textvariable=dayValue)


ttk.Button(mainframe, text="run", command=calculate).grid(column=1, row=1)
ttk.Button(mainframe, text = "today").grid(column=2,row =1)
ttk.Button(mainframe, text= "by date").grid(column=3,row=1)
ttk.Label(mainframe, text="Date 1").grid(column =4,row=1)
day_entry1.grid(column=6,row=1)





root.bind('<Return>', calculate)

root.mainloop()