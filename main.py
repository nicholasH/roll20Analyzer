import tkinter as tk
import analyze
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
        filemenu.add_command(label="New")
        filemenu.add_command(label="Open")

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        self.config(menu=menubar)

        self.frames = {}
        frame = mainPage(container, self)

        frame.pack(fill="both", expand=1)

        self.frames[mainPage] = frame

        self.show_frame(mainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


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
        yearString1.trace("w", lambda name, index, mode, yearString=dayString1: limitSizeDay(yearString, 4))

        self.show = tk.IntVar()
        showbox = tk.Checkbutton(uiFrame, text="to?", variable=self.show, command=self.cb)

        dayString2 = tk.StringVar()
        dayString2.trace("w", lambda name, index, mode, dayString=dayString2: limitSizeDay(dayString, 2))
        monthString2 = tk.StringVar()
        monthString2.trace("w", lambda name, index, mode, monthString=monthString2: limitSizeDay(monthString, 2))
        yearString2 = tk.StringVar()
        yearString2.trace("w", lambda name, index, mode, dayString=dayString2: limitSizeDay(yearString2, 4))

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

        uiFrame.pack()
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


app = app()
app.mainloop()

