from main import *
import tkinter, guiNewTransaction, guiCategories

class topLevelWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Bar Kassa Systeem")
        #self.master.wm_attributes('-fullscreen', 'true')

        menuFrame = tkinter.Frame(self.master)
        contentFrame = tkinter.Frame(self.master)
        brandingFrame = tkinter.Frame(self.master)
        footerFrame = tkinter.Frame(self.master)

        menuFrame.grid(column=0,row=0,columnspan=3)
        contentFrame.grid(column=1,row=1)
        brandingFrame.grid(column=2,row=1)
        footerFrame.grid(column=1,row=2,columnspan=3)

        self.menu = buildMenu(menuFrame)
        self.content = buildContent(contentFrame)
        # self.branding = buildBranding(brandingFrame)
        # self.footer = buildFooter(footerFrame)


class buildMenu:
    def __init__(self, master):
        self.master = master
        tkinter.Button(self.master, text='Transaction', command=lambda: my_gui.content.callTransaction()).grid(column=0,row=0)
        tkinter.Button(self.master, text='Klanten', command=lambda: my_gui.content.callCustomers()).grid(column=1,row=0)
        tkinter.Button(self.master, text='Producten', command=lambda: my_gui.content.callProducts()).grid(column=2,row=0)
        tkinter.Button(self.master, text='Categorieën', command=lambda: my_gui.content.callCategories()).grid(column=3,row=0)


class buildContent:
    def __init__(self,master):
        self.master = master

    def callTransaction(self):
        guiNewTransaction.newTransaction(self.master)

    def callCustomers(self):
        None

    def callProducts(self):
        None

    def callCategories(self):
        guiCategories.categoriesOverview(self.master)



root = tkinter.Tk()
my_gui = topLevelWindow(root)
root.mainloop()