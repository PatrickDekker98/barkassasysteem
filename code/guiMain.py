from main import *
import tkinter, guiNewTransaction, guiCategories

class topLevelWindow:
    def __init__(self, master):
        self.master = master
        #self.master.wm_attributes('-fullscreen', 'true')

        menuFrame = tkinter.Frame(self.master)
        contentFrame = tkinter.Frame(self.master)
        brandingFrame = tkinter.Frame(self.master)
        footerFrame = tkinter.Frame(self.master)

        self.master.columnconfigure(0, weight=2)
        self.master.columnconfigure(1, weight=86)
        self.master.columnconfigure(2, weight=10)
        self.master.columnconfigure(3, weight=2)
        self.master.rowconfigure(0, weight=10)
        self.master.rowconfigure(1, weight=85)
        self.master.rowconfigure(2, weight=5)
#
        menuFrame.grid(column=1,row=0,columnspan=2)
        contentFrame.grid(column=1,row=1, sticky='news')
        #brandingFrame.grid(column=2,row=1, sticky='news')
        footerFrame.grid(column=1,row=2,columnspan=2, sticky='news')

        self.menu = buildMenu(menuFrame)
        self.content = buildContent(contentFrame)
        #self.branding = buildBranding(brandingFrame)
        self.footer = buildFooter(footerFrame)




class buildMenu:
    def __init__(self, master):
        tkinter.Button(master, text='Transaction', command=lambda: my_gui.content.callTransaction()).grid(column=0,row=0, sticky='news')
        tkinter.Button(master, text='Klanten', command=lambda: my_gui.content.callCustomers()).grid(column=1,row=0, sticky='news')
        tkinter.Button(master, text='Producten', command=lambda: my_gui.content.callProducts()).grid(column=2,row=0, sticky='news')
        tkinter.Button(master, text='Categorieën', command=lambda: my_gui.content.callCategories()).grid(column=3,row=0, sticky='news')


class buildContent(topLevelWindow):
    def __init__(self,master):
        self.master = master

    def callTransaction(self):
        self.resetContent()
        guiNewTransaction.newTransaction(self.master)

    def callCustomers(self):
        self.resetContent()
        None

    def callProducts(self):
        self.resetContent()
        None

    def callCategories(self):
        self.resetContent()
        guiCategories.categoriesOverview(self.master)

    def resetContent(self):
        for widget in self.master.winfo_children():
            widget.destroy()

class buildFooter:
    def __init__(self,master):
        text = 'Dit programma is geschreven in opdracht van Hogeschool Utrecht, door studenten Nico, Patrick, Lars en Bart uit klas V1H. \u00a9 2017'
        tkinter.Label(master,text=text).pack()

root = tkinter.Tk()
my_gui = topLevelWindow(root)
root.mainloop()