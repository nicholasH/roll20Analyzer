import tkinter as tk

class app(tk.Tk):


    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        container = tk.Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames ={}
        frame = mainPage(container, self)
        self.frames[mainPage] = frame

        self.frames[mainPage]= frame

        frame.grid(row=0,column=0,sticky="nsew")

        self.show_frame(mainPage)


    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

def run():
    print("run")
def run_today():
    print("today")
def run_by_data():
    print("date")




class mainPage(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        run_all_btn = tk.Button(self,text ="run all",command= lambda: run())
        today_btn = tk.Button(self,text = "today",command= lambda: run_today())
        run_by_date_btn = tk.Button(self,text = "run by date",command= lambda: run_by_data())

        day_entry = tk.Entry(self,width=2)
        month_entry = tk.Entry(self, width = 2)
        year_entry= tk.Entry(self,width = 4)

        fSlash1 = tk.Label(self,text = "/")
        fSlash2 = tk.Label(self,text = "/")

        text_box = tk.Text(self)
        text_box.insert(tk.END, "Just a text Widget\nin two lines\n")

        column = 0
        row = 0
        run_by_date_btn.grid(row=1,column=column)
        column+=1

        run_all_btn.grid(row =1,column=column)
        column+=1

        today_btn.grid(row=1, column=column)
        column+=1

        day_entry.grid(row=1, column=column)
        column+=1

        fSlash1.grid(row=1, column =column)
        column+=1

        month_entry.grid(row=1,column=column)
        column+=1

        fSlash2.grid(row=1,column=column)
        column+=1

        year_entry.grid(row=1,column=column)
        column+=1

        text_box.grid(row = 2,column=0,columnspan=1000)
        







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


app = app()
app.mainloop()

