import os
import tkinter as tk
from tkinter import filedialog, ttk

import sys

import DBscratch
import analyze
import DBhandler
from datetime import datetime
from tkinter import messagebox
from threading import Thread

import chatParser

about = 'Programed by:Nicholas Hoover\n' \
        '\n' \
        'How to analyse new game:\n' \
        'From the file Drop down menu click new\n' \
        'Input the name of the game(anything you want to save it as)\n' \
        'Input the archive url, it should look something like https://app.roll20.net/campaigns/chatarchive/9999999\n' \
        'The 9999999 is the game ID\n' \
        'Pressing any of the buttons run all, run today, and run by date will open a browser to the roll20 login page\n' \
        'login to you account and the program will start grabbing you data and start analysing\n' \
        'checking the offline? check box will make it so the program wont grab new data from roll20 \n' \
        '\n' \
        'How to add tags to my game:\n' \
        'There are 3 types of tag single Tags, timed tags, and indefinite tags\n' \
        'Tags must be typed into the roll20 chat as the game is played as an emote\n' \
        'The tag name must be a single word\n' \
        'The tag Name must have a ^ before the name as in ^tagName' \
        'Single tags only tag then next roll with given tag\n' \
        'example:\n' \
        '/em ^swordAtk (This will make the next roll be tagged with SwordAtk)\n\n' \
        'Time tags will tag everything with the tag for the number of min/hours given\n' \
        'example:\n' \
        '/em ^wizTower -5h (All rolls for the next 5 hours will be tagged with wizTower)\n' \
        '/em ^darkCave -30m (All rolls for the next 30 min will be tagged with darkCave)\n\n' \
        'Indefinite tags will everything with the tag until told to stop\n' \
        'example /em ^underDark -start (All rolls will be tagged with underDark until told to spop)\n\n' \
        'all of these tags can be given the self modifier to make the only apply to the next person who rolls\n' \
        'example:\n' \
        '/em ^wizTower -5h -self (All roll by the next person who rolls will be tagged with wizTower for the next 5 hours)\n' \
        '/em ^dawfFort -start -self (All roll by the next person who rolls will be tagged with dawfFort until told to stop)\n' \
        'The above examples can be the can also be writen like this /em ^wizTower -self -5h or /em ^dawfFort -self -start\n\n' \
        'Ending tags\n' \
        'there are 2 way to end a tag the -end and -endall\n' \
        '-end will stop all indefinite or timed tag early with the tag name given\n' \
        'any player a can end any tag, having a self modifier does not stop another player from ending a tag\n' \
        'example:\n' \
        '/em ^wizTower -end\n' \
        '/em ^underDark -end\n' \
        '-endall will stop all tags\n' \
        'example:\n' \
        '/em ^end -endall (This will end all current active tags)\n' \
        '\n' \
        'scoring:\n' \
        'Players get points for each crit success they get \n' \
        'example if player rolls a 8 on a d8 they get 8 points add to their total score\n' \
        'player also get bounce points if they have most of something\n' \
        'The player who get the most Nat20, CritSus, nat1, and critfails get 10 points\n' \
        'The player with the highest number roll also gets 10 points'

class app(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self, bg="red")
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.geometry('1000x600')

        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.new)
        filemenu.add_command(label="Open", command=self.loadDB)
        filemenu.add_command(label="About", command=self.about)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.title("Roll 20 analyzer")
        self.iconbitmap(os.path.join(sys.path[0], 'ICON.ico'))
        self.config(menu=menubar)

        self.frames = {}
        self.frame = mainPage(container, self)

        self.frame.pack(fill="both", expand=1)

        self.frames[mainPage] = self.frame

        self.show_frame(mainPage)
        self.currentDB_string = tk.StringVar()
        self.currentGame_lable = tk.Label(textvariable=self.currentDB_string)
        self.currentGame_lable.pack(side="left")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def new(self):
        d = newDB(self)
        d.top.grab_set()
        self.wait_window(d.top)

    def about(self):
        self.frame.updateText(about)

    def updatDBLable(self):
        message = "Game Name: " + DBhandler.getGameName() + "| URL: " + DBhandler.getURL()
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
        run_all_btn = tk.Button(uiFrame, text="run all", command=self.runThread)
        today_btn = tk.Button(uiFrame, text="today", command=self.runTodayThread)
        run_by_date_btn = tk.Button(uiFrame, text="run by date", command=self.runByDateThread)

        # search
        self.tagSearch = tk.IntVar()
        tagSearch = tk.Checkbutton(searchFrame, text="tags", variable=self.tagSearch)
        self.tag_combo_value = tk.StringVar()
        self.tag_combo = ttk.Combobox(searchFrame, textvariable=self.tag_combo_value, postcommand=self.updateMenus)
        self.tag_combo['values'] = [""]
        self.tag_combo.current(0)
        self.nameSearch = tk.IntVar()
        nameSearch = tk.Checkbutton(searchFrame, text="name", variable=self.nameSearch)
        self.name_combo_value = tk.StringVar()
        self.name_combo = ttk.Combobox(searchFrame, textvariable=self.name_combo_value, postcommand=self.updateMenus)
        self.name_combo['values'] = [""]
        self.name_combo.current(0)

        uiFrame.pack()
        offline_checkBox.pack(side="left")
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
        self.tag_combo.pack(side="left")
        tagSearch.pack(side="left")

        self.name_combo.pack(side="left")
        nameSearch.pack(side="left")

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

    def runThread(self):
        if not self.offline.get():
            chatParser.resetGlobal()
            d = cancel(self)
            d.top.grab_set()
            d.top.widgetName = "cancel"

        t1 = Thread(target=self.run)
        t1.start()

    def run(self):
        try:
            if self.tagSearch.get() and self.nameSearch.get():
                tagNameList = [self.tag_combo.get()]
                self.updateText(analyze.analyzeByTagAndName(self.name_combo.get(), tagNameList, self.offline.get()))
            elif self.tagSearch.get():
                self.updateText(analyze.analyzeByTag(self.tag_combo.get(), self.offline.get()))
            elif self.nameSearch.get():
                self.updateText((analyze.analyzeByName(self.name_combo.get(), self.offline.get())))
            else:
                self.updateText(analyze.analyze(self.offline.get()))
        except TypeError:
            for child in self.winfo_children():
                if child.widgetName == "cancel":
                    child.destroy()
            messagebox.showerror("Error", "No chat loaded")
            return

    def runTodayThread(self):
        if not self.offline.get():
            chatParser.resetGlobal()
            d = cancel(self)
            d.top.grab_set()
            d.top.widgetName = "cancel"
        t1 = Thread(target=self.run_today)
        t1.start()

    def run_today(self):
        try:
            if self.tagSearch.get() and self.nameSearch.get():
                tagNameList = [self.tag_combo.get()]
                self.updateText(
                    analyze.analyzeByTagAndNameToday(self.name_combo.get(), tagNameList, self.offline.get()))
            elif self.nameSearch.get():
                self.updateText(analyze.analyzeByNameToday(self.name_combo.get(), self.offline.get()))
            elif self.tagSearch.get():
                self.updateText(analyze.analyzeByTagToday(self.tag_combo.get(), self.offline.get()))
            else:
                self.updateText(analyze.analyzeToday(self.offline.get()))
        except TypeError:
            for child in self.winfo_children():
                if child.widgetName == "cancel":
                    child.destroy()
            messagebox.showerror("Error", "No chat loaded")
            return

    def runByDateThread(self):
        if not self.offline.get():
            chatParser.resetGlobal()
            d = cancel(self)
            d.top.grab_set()
            d.top.widgetName = "cancel"
        t1 = Thread(target=self.run_by_date)
        t1.start()

    def run_by_date(self):
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
                    self.updateText(
                        analyze.analyzeByTagAndNameByDateRange(self.name_combo.get(), tagNameList, date0, date1,
                                                               self.offline.get()))
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
                    self.updateText(analyze.analyzeByTagAndNameByDate(self.name_combo.get(), tagNameList, date0,
                                                                      self.offline.get()))
                elif self.nameSearch.get():
                    self.updateText(analyze.analyzeByNameByDate(self.name_combo.get(), date0, self.offline.get()))
                elif self.tagSearch.get():
                    self.updateText(analyze.analyzeByTagDate(self.tag_combo.get(), date0, self.offline.get()))
                else:
                    self.updateText(analyze.analyzeDate(date0, self.offline.get()))
        except ValueError:
            for child in self.winfo_children():
                if child.widgetName == "cancel":
                    child.destroy()
            messagebox.showerror("Error", "bad date: DD/MM/YYYY")
            return
        except TypeError:
            for child in self.winfo_children():
                if child.widgetName == "cancel":
                    child.destroy()
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
        url_lable = tk.Label(top, text="Game archive URL")
        self.url_entry = tk.Entry(top)
        ok_btn = tk.Button(top, text="OK", command=self.ok)
        cancel_btn = tk.Button(top, text="cancel", command=self.cancel)
        # todo take out this line of code
        self.url_entry.insert(0, "https://app.roll20.net/campaigns/chatarchive/1065012")

        name_lable.pack()
        self.name_entry.pack(padx=5)
        url_lable.pack()
        self.url_entry.pack(padx=5)
        ok_btn.pack(pady=5)
        cancel_btn.pack()

    def ok(self):
        print("value is", self.name_entry.get(), self.url_entry.get())
        DBhandler.createDB(self.name_entry.get(), self.url_entry.get())
        self.p.updatDBLable()
        self.top.destroy()

    def cancel(self):
        self.top.destroy()


class cancel(tk.Tk):
    def __init__(self, parent):
        tk.Tk.__init__(self)
        self.destroy()
        top = self.top = tk.Toplevel(parent)

        name_lable = tk.Label(top, text="Your game is being analyzed this may take a few minutes")

        cancel_btn = tk.Button(top, text="cancel", command=self.cancelAnalysis)

        self.progress = ttk.Progressbar(self.top, orient="horizontal", length=200, mode="determinate")

        name_lable.pack()
        self.progress.pack()
        cancel_btn.pack()
        self.loading()

    def loading(self):
        self.progress["value"] = chatParser.current
        self.maxMessages = chatParser.size
        self.progress["maximum"] = chatParser.size
        self.message = chatParser.current

        self.progress["value"] = self.message
        if self.message < self.maxMessages:
            print(self.message)
            print(self.maxMessages)
            self.after(100, self.loading)
        elif (self.message == self.maxMessages):
            self.top.destroy()

    def cancelAnalysis(self):
        chatParser.cancelParser()
        self.top.destroy()


app = app()
app.mainloop()
