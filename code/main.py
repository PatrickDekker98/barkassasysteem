import sqlite3 as sql
import tkinter
import datetime

db = '../barkassasysteem.db'
conn = sql.connect(db)
cursor = conn.cursor()

class messageBox:
    def __init__(self, title, message, type='info'):
        self.top = tkinter.Toplevel()
        self.top.title(title)

        iconFrame = tkinter.Frame(self.top)
        contentFrame = tkinter.Frame(self.top)
        buttonFrame = tkinter.Frame(self.top)

        iconFrame.grid(column=0, row=0)
        contentFrame.grid(column=1, row=0)
        buttonFrame.grid(column=1, row=1)

        self.top.grid_rowconfigure(2, minsize=10)

        icon = tkinter.PhotoImage(file='tkinter_src/' + type + '.gif')
        tkinter.Label(iconFrame, image=icon).pack()
        tkinter.Message(contentFrame, text=message, anchor='n', aspect=700).pack()
        tkinter.Button(buttonFrame, text='OK', command=self.close).pack()

        self.center(self.top)
        self.top.mainloop()


    def close(self):
        self.top.destroy()


    def center(self, master):
        master.update_idletasks()
        w = master.winfo_screenwidth()
        h = master.winfo_screenheight()
        size = tuple(int(_) for _ in master.geometry().split('+')[0].split('x'))
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2
        master.geometry("%dx%d+%d+%d" % (size + (x, y)))


def inputGui(question):
    """Ask for input in GUI"""
    return input(question)  # use python console input, for now

#messageBox('title', 'content')
