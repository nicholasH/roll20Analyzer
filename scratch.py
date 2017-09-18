import tkinter as tk

class app(tk.Tk):


    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        container = tk.Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames ={}
        frame = StartPage(container,self)
        self.frames[StartPage] = frame

        self.frames[StartPage]= frame

        frame.grid(row=0,column=0,sticky="nsew")

        self.show_frame(StartPage)


    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text="start page")
        label.pack()



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

