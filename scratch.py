import tkinter as tk
from tkinter import ttk

class Main(tk.Frame):
    def __init__(self, master):
        master.geometry('500x350')
        self.master = master
        tk.Frame.__init__(self, master)
        self.tree = ttk.Treeview(self.master, height=15)
        self.tree.pack(fill='x')
        self.btn = tk.Button(master, text='click', command=self.clickbtn)
        self.btn.pack()
        self.rclick = RightClick(self.master)
        self.num = 0

        # attach popup to treeview widget
        self.tree.bind('<Button-3>', self.rclick.popup)
    def clickbtn(self):
        text = 'Hello ' + str(self.num)
        self.tree.insert('', 'end', text=text)
        self.num += 1

class RightClick:
    def __init__(self, master):

        # create a popup menu
        self.aMenu = tk.Menu(master, tearoff=0)
        self.aMenu.add_command(label='Delete', command=self.delete)
        self.aMenu.add_command(label='Say Hello', command=self.hello)

        self.tree_item = ''

    def delete(self):
        if self.tree_item:
            app.tree.delete(self.tree_item)

    def hello(self):
        print ('hello!')

    def popup(self, event):
        self.aMenu.post(event.x_root, event.y_root)
        self.tree_item = app.tree.focus()

root = tk.Tk()
app=Main(root)
root.mainloop()