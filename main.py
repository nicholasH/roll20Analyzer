import os
import tkinter as tk
from tkinter import filedialog

import sys

import analyze
import DBhandler
from datetime import datetime
from tkinter import messagebox


class app(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self, bg="red")
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command= self.new)
        filemenu.add_command(label="Open", command= self.loadDB)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.title("Roll 20 analyze")
        self.iconbitmap(os.path.join(sys.path[0],'ICON.ico'))
        self.config(menu=menubar)

        self.frames = {}
        frame = mainPage(container, self)

        frame.pack(fill="both", expand=1)

        self.frames[mainPage] = frame

        self.show_frame(mainPage)
        self.currentDB_string = tk.StringVar()
        self.currentGame_lable = tk.Label(textvariable = self.currentDB_string)
        self.currentGame_lable.pack(side="left")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def new(self):
        d = newDB(self)
        self.wait_window(d.top)

    def updatDBLable(self):
        message = "Game Name: " + DBhandler.getGameName() + "| URL: "+ DBhandler.getURL()
        self.currentDB_string.set(message)

    def loadDB(self):
        dateBase = os.path.join(os.sys.path[0], "data", "dataBase")
        self.filename = filedialog.askopenfilename(initialdir=dateBase, title="Select file",
                                                   filetypes=(("db files", "*.db"), ("all files", "*.*")))
        DBhandler.loadDB(self.filename)
        self.updatDBLable()



def limitSizeDay(dayString, limit):
    value = dayString.get()
    if len(value) > limit: dayString.set(value[:limit])
    if value in '0123456789.-+':
        try:
            float(value)
            return True
        except ValueError:
            return False


class mainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        uiFrame = tk.Frame(self)
        textBoxFrame = tk.Frame(self)
        dayString1 = tk.StringVar()
        dayString1.trace("w", lambda name, index, mode, dayString=dayString1: limitSizeDay(dayString, 2))

        monthString1 = tk.StringVar()
        monthString1.trace("w", lambda name, index, mode, monthString=monthString1: limitSizeDay(monthString, 2))

        yearString1 = tk.StringVar()
        yearString1.trace("w", lambda name, index, mode, yearString=yearString1: limitSizeDay(yearString, 4))

        self.show = tk.IntVar()
        showbox = tk.Checkbutton(uiFrame, text="to?", variable=self.show, command=self.cb)

        dayString2 = tk.StringVar()
        dayString2.trace("w", lambda name, index, mode, dayString=dayString2: limitSizeDay(dayString, 2))
        monthString2 = tk.StringVar()
        monthString2.trace("w", lambda name, index, mode, monthString=monthString2: limitSizeDay(monthString, 2))
        yearString2 = tk.StringVar()
        yearString2.trace("w", lambda name, index, mode, yearString=yearString2: limitSizeDay(yearString, 4))

        self.day_entry1 = tk.Entry(uiFrame, width=2, textvariable=dayString1)
        self.month_entry1 = tk.Entry(uiFrame, width=2, textvariable=monthString1)
        self.year_entry1 = tk.Entry(uiFrame, width=4, textvariable=yearString1)

        self.day_entry2 = tk.Entry(uiFrame, width=2, textvariable=dayString2)
        self.month_entry2 = tk.Entry(uiFrame, width=2, textvariable=monthString2)
        self.year_entry2 = tk.Entry(uiFrame, width=4, textvariable=yearString2)

        day1_lable = tk.Label(uiFrame, text="day 1")
        day2_lable = tk.Label(uiFrame, text="day 2")

        fSlash1 = tk.Label(uiFrame, text="/")
        fSlash2 = tk.Label(uiFrame, text="/")
        self.fSlash3 = tk.Label(uiFrame, text="/")
        self.fSlash4 = tk.Label(uiFrame, text="/")

        self.text_box = tk.Text(textBoxFrame)
        self.text_box.config(state="disabled")
        run_all_btn = tk.Button(uiFrame, text="run all", command=self.run)
        today_btn = tk.Button(uiFrame, text="today", command=self.run_today)
        run_by_date_btn = tk.Button(uiFrame, text="run by date", command=self.run_by_data)

        self.tag_text_entry = tk.Entry(uiFrame)
        tag_btn = tk.Button(uiFrame, text="tag", command= self.run_by_tag)


        uiFrame.pack()
        self.tag_text_entry.pack(side="left")
        tag_btn.pack(side="left")
        run_all_btn.pack(side="left")
        today_btn.pack(side="left")
        run_by_date_btn.pack(side="left")
        day1_lable.pack(side="left")
        self.month_entry1.pack(side="left")
        fSlash1.pack(side="left")
        self.day_entry1.pack(side="left")
        fSlash2.pack(side="left")
        self.year_entry1.pack(side="left")
        showbox.pack(side="left")
        day2_lable.pack(side="left")
        # line above must be at the end of the pack

        textBoxFrame.pack(fill="both", expand=True)
        self.text_box.pack(fill="both", expand=True)

    def cb(self):
        if self.show.get():
            self.month_entry2.pack(side="left")
            self.fSlash3.pack(side="left")
            self.day_entry2.pack(side="left")
            self.fSlash4.pack(side="left")
            self.year_entry2.pack(side="left")

        else:
            self.month_entry2.pack_forget()
            self.fSlash3.pack_forget()
            self.day_entry2.pack_forget()
            self.fSlash4.pack_forget()
            self.year_entry2.pack_forget()

    def run(self):
        self.update(analyze.analyze())

    def run_today(self):
        self.update(analyze.analyzeToday())

    def run_by_data(self):
        try:
            date0 = datetime(int(self.year_entry1.get()), int(self.month_entry1.get()), int(self.day_entry1.get()))
        except ValueError:

            messagebox.showerror("Error", "bad date")
            return

        if self.show.get():
            try:
                date1 = datetime(int(self.year_entry2.get()), int(self.month_entry2.get()), int(self.day_entry2.get()))
                print(date1)
            except ValueError:
                messagebox.showerror("Error", "bad date")
                return
            if date1 < date0:
                messagebox.showerror("Error", "error date is out of order")
                return
            self.update(analyze.analyzeDateRange(date0, date1))
        else:
            self.update(analyze.analyzeDate(date0))

    def update(self, text):
        self.text_box.config(state="normal")
        self.text_box.insert(tk.END, text)
        self.text_box.config(state="disable")

    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()
    def run_by_tag(self):
        self.update(analyze.analyzeByTag(self.tag_text_entry.get()))





class newDB:

    def __init__(self, parent):

        top = self.top = tk.Toplevel(parent)
        self.p = parent

        name_lable = tk.Label(top, text="Name of game")
        self.name_entry = tk.Entry(top)
        url_lable = tk.Label(top,text="Game arcive URL")
        self.url_entry = tk.Entry(top)
        ok_btn = tk.Button(top, text="OK", command=self.ok)
        cancel_btn = tk.Button(top,text ="cancel", command =self.cancel)

        self.url_entry.insert(0, "https://app.roll20.net/campaigns/chatarchive/1644807")

        name_lable.pack()
        self.name_entry.pack(padx=5)
        url_lable.pack()
        self.url_entry.pack(padx=5)
        ok_btn.pack(pady=5)
        cancel_btn.pack()

    def ok(self):
        print("value is", self.name_entry.get(),self.url_entry.get())
        DBhandler.createDB(self.name_entry.get(),self.url_entry.get())
        self.p.updatDBLable()
        self.top.destroy()

    def cancel(self):
        self.top.destroy()

app = app()
app.mainloop()

