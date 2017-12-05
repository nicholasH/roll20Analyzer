import os
import tkinter as tk
from tkinter import filedialog, ttk

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
        self.frame = mainPage(container, self)

        self.frame.pack(fill="both", expand=1)

        self.frames[mainPage] = self.frame

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
        searchFrame = tk.Frame(self)
        textBoxFrame = tk.Frame(self)

        self.offline = tk.IntVar()
        offline_checkBox = tk.Checkbutton(uiFrame, text="Offline?", variable=self.offline)


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


        #search
        self.tagSearch = tk.IntVar()
        tagSearch = tk.Checkbutton(searchFrame,text="tags",variable=self.tagSearch)
        self.tag_combo_value = tk.StringVar()
        self.tag_combo = ttk.Combobox(searchFrame, textvariable=self.tag_combo_value, postcommand = self.updateMenus)
        self.tag_combo['values'] = [""]
        self.tag_combo.current(0)
        self.nameSearch = tk.IntVar()
        nameSearch = tk.Checkbutton(searchFrame,text="name",variable=self.nameSearch)
        self.name_combo_value = tk.StringVar()
        self.name_combo = ttk.Combobox(searchFrame,textvariable=self.name_combo_value, postcommand = self.updateMenus)
        self.name_combo['values'] = [""]
        self.name_combo.current(0)




        uiFrame.pack()
        offline_checkBox.pack(side = "left")
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

        searchFrame.pack()
        self.tag_combo.pack(side ="left")
        tagSearch.pack(side ="left")

        self.name_combo.pack(side = "left")
        nameSearch.pack(side ="left")



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
        try:
            if self.tagSearch.get() and self.nameSearch.get():
                tagNameList = [self.tag_combo.get()]
                self.updateText(analyze.analyzeByTagAndName(self.name_combo.get(),tagNameList,self.offline.get()))
            elif self.tagSearch.get():
                self.updateText(analyze.analyzeByTag(self.tag_combo.get(),self.offline.get()))
            elif self.nameSearch.get():
                self.updateText((analyze.analyzeByName(self.name_combo.get(),self.offline.get())))
            else:
                self.updateText(analyze.analyze(self.offline.get()))
        except TypeError:
            messagebox.showerror("Error", "No chat loaded")
            return

    def run_today(self):
        try:
            if self.tagSearch.get() and self.nameSearch.get():
                tagNameList = [self.tag_combo.get()]
                self.updateText(analyze.analyzeByTagAndNameToday(self.name_combo.get(),tagNameList,self.offline.get()))
            elif self.nameSearch.get():
                self.updateText(analyze.analyzeByNameToday(self.name_combo.get(),self.offline.get()))
            elif self.tagSearch.get():
                self.updateText(analyze.analyzeByTagToday(self.tag_combo.get(),self.offline.get()))
            else:
                self.updateText(analyze.analyzeToday(self.offline.get()))
        except TypeError:
            messagebox.showerror("Error", "No chat loaded")
            return

    def run_by_data(self):
        try:
            date0 = datetime(int(self.year_entry1.get()), int(self.month_entry1.get()), int(self.day_entry1.get()))
            if self.show.get():
                try:
                    date1 = datetime(int(self.year_entry2.get()), int(self.month_entry2.get()),
                                     int(self.day_entry2.get()))
                    print(date1)
                except ValueError:
                    messagebox.showerror("Error", "bad date")
                    return
                if date1 < date0:
                    messagebox.showerror("Error", "error date is out of order")
                    return
                if self.tagSearch.get() and self.nameSearch.get():
                    tagNameList = [self.tag_combo.get()]
                    self.updateText(analyze.analyzeByTagAndNameByDateRange(self.name_combo.get(),tagNameList,date0,date1,self.offline.get()))
                elif self.nameSearch.get():
                    self.updateText(
                        analyze.analyzeByNameByDateRange(self.name_combo.get(), date0, date1, self.offline.get()))
                elif self.tagSearch.get():
                    self.updateText(
                        analyze.analyzeByTagDateRange(self.tag_combo.get(), date0, date1, self.offline.get()))
                else:
                    self.updateText(analyze.analyzeDateRange(date0, date1, self.offline.get()))
            else:
                if self.tagSearch.get() and self.nameSearch.get():
                    tagNameList = [self.tag_combo.get()]
                    self.updateText(analyze.analyzeByTagAndNameByDate(self.name_combo.get(),tagNameList,date0,self.offline.get()))
                elif self.nameSearch.get():
                    self.updateText(analyze.analyzeByNameByDate(self.name_combo.get(), date0, self.offline.get()))
                elif self.tagSearch.get():
                    self.updateText(analyze.analyzeByTagDate(self.tag_combo.get(), date0, self.offline.get()))
                else:
                    self.updateText(analyze.analyzeDate(date0, self.offline.get()))
        except ValueError:

            messagebox.showerror("Error", "bad date")
            return
        except TypeError:
            messagebox.showerror("Error", "No chat loaded")
            return



    def updateText(self, text):
        self.text_box.config(state="normal")
        self.text_box.delete(0.0, tk.END)
        self.text_box.insert(tk.END, text)
        self.text_box.config(state="disable")

    def updateMenus(self):
        taglist = DBhandler.getAlltags()
        self.tag_combo['values'] = taglist
        nameList = DBhandler.getAllNames()
        self.name_combo['values'] = nameList

    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()
    def run_by_tag(self):
        self.updateText(analyze.analyzeByTag(self.tag_text_entry.get()))





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