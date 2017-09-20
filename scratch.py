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
def run_by_data(d1,m1,):
    print("date")





class mainPage(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        uiFrame = tk.Frame(self,bg="blue")
        textBoxFrame = tk.Frame(self,bg="blue")






        text_box = tk.Text(textBoxFrame)
        run_all_btn = tk.Button(uiFrame,text ="run all",command= lambda:run(text_box))
        today_btn = tk.Button(uiFrame,text = "today",command= lambda: run_today(text_box))
        run_by_date_btn = tk.Button(uiFrame,text = "run by date",command= lambda: run_by_data())

        day_entry = tk.Entry(uiFrame,width=2)
        month_entry = tk.Entry(uiFrame, width = 2)
        year_entry= tk.Entry(uiFrame,width = 4)

        fSlash1 = tk.Label(uiFrame,text = "/")
        fSlash2 = tk.Label(uiFrame,text = "/")


        uiFrame.pack()
        run_all_btn.pack(side="left")
        today_btn.pack(side="left")




        textBoxFrame.pack(fill="both",expand=True)
        text_box.pack(fill="both",expand=True)










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

