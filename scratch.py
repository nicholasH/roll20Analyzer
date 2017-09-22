import tkinter as tk
import analyze

class app(tk.Tk):


    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        container = tk.Frame(self,bg="red")
        container.pack(fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames ={}
        frame = mainPage(container, self)

        frame.pack(fill="both", expand=1)

        self.frames[mainPage] = frame



        self.show_frame(mainPage)


    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

def run(textbox):
    textbox.insert(tk.END,analyze.analyze())

    print("run")
def run_today(textbox):
    textbox.text = analyze.analyzeToday()
    print("today")
def run_by_data(d1,m1,y1):
    print(d1,m1,y1)

    print("date")

def limitSizeDay(dayString):
    value = dayString.get()
    if len(value) > 2: dayString.set(value[:2])
    if value in '0123456789.-+':
        try:
            float(value)
            return True
        except ValueError:
            return False



class mainPage(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        uiFrame = tk.Frame(self)
        textBoxFrame = tk.Frame(self)

        dayString = tk.StringVar()
        dayString.trace("w", lambda name, index, mode, dayString=dayString: limitSizeDay(dayString))

        monthString = tk.StringVar()
        monthString.trace("w", lambda name, index, mode, monthString=monthString: limitSizeDay(monthString))

        day_entry = tk.Entry(uiFrame,width=2,textvariable=dayString)
        month_entry = tk.Entry(uiFrame, width = 2,textvariable=monthString)
        year_entry= tk.Entry(uiFrame,width = 4)

        day1_lable = tk.Label(uiFrame,text="day 1")

        fSlash1 = tk.Label(uiFrame,text = "/")
        fSlash2 = tk.Label(uiFrame,text = "/")


        text_box = tk.Text(textBoxFrame)
        run_all_btn = tk.Button(uiFrame,text ="run all",command= lambda:run(text_box))
        today_btn = tk.Button(uiFrame,text = "today",command= lambda: run_today(text_box))
        run_by_date_btn = tk.Button(uiFrame,text = "run by date",command= lambda: run_by_data(day_entry.get(),month_entry.get(),year_entry.get()))



        uiFrame.pack()
        run_all_btn.pack(side="left")
        today_btn.pack(side="left")
        run_by_date_btn.pack(side="left")
        day1_lable.pack(side="left")
        day_entry.pack(side="left")
        month_entry.pack(side="left")
        year_entry.pack(side="left")




        textBoxFrame.pack(fill="both",expand=True)
        text_box.pack(fill="both",expand=True)






app = app()
app.mainloop()

