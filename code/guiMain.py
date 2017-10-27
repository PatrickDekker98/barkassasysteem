from main import *
import tkinter, guiCustomers, guiNewTransaction, guiCategories, guiProducts
import tkinter.simpledialog as simpledialog

class topLevelWindow:
    'Creates the main screen, which is to contain all frame'
    def __init__(self, master):
        self.master = master
        self.master.title("Bar Kassa Systeem")
        #self.master.wm_attributes('-fullscreen', 'true')

        menuFrame = tkinter.Frame(self.master, bg='lightblue')
        contentFrame = tkinter.Frame(self.master)
        footerFrame = tkinter.Frame(self.master)

        self.master.columnconfigure(0, minsize=50, weight=2)
        self.master.columnconfigure(1, weight=9)
        self.master.columnconfigure(3, minsize=50, weight=2)
        self.master.rowconfigure(0, minsize=50, weight=10)
        self.master.rowconfigure(1, weight=85)
        self.master.rowconfigure(2, minsize=50, weight=5)

        menuFrame.grid(column=1,row=0,columnspan=2, sticky='new')
        contentFrame.grid(column=1,row=1, sticky='news')
        footerFrame.grid(column=1,row=2,columnspan=2, sticky='ews')

        self.menu = buildMenu(menuFrame)
        self.content = buildContent(contentFrame)
        self.footer = buildFooter(footerFrame)

        self.content.callTransaction()


class buildMenu:
    'Class to build the main menu, presented in the top portion of the screen'
    def __init__(self, master):
        master.rowconfigure(0, weight=1)
        for c in range(4):  #   Pre-configures weight of all columns, so they will be sized evenly when the screen resizes
            master.columnconfigure(c, weight=1)
        font = ('Arial Black', 15)
        tkinter.Button(master, width=200, height=3, font=font, bg='lightblue', text='Transaction', command=lambda: my_gui.content.callTransaction()).grid(column=0,row=0, sticky='news')
        tkinter.Button(master, width=200, height=3, font=font, bg='lightblue',text='Klanten', command=lambda: my_gui.content.callCustomers()).grid(column=1,row=0, sticky='news')
        tkinter.Button(master, width=200, height=3, font=font, bg='lightblue',text='Producten', command=lambda: my_gui.content.callProducts()).grid(column=2,row=0, sticky='news')
        tkinter.Button(master, width=200, height=3, font=font, bg='lightblue',text='Categorieën', command=lambda: my_gui.content.callCategories()).grid(column=3,row=0, sticky='news')


class buildContent:
    'Build the contentframe by calling classes in other scripts, containing the rest of the GUI'
    def __init__(self,master):
        self.master = master

    def callTransaction(self):
        'Calls the transaction GUI'
        self.resetContent()
        guiNewTransaction.newTransaction(self.master)

    def callCustomers(self):
        'Calls the customers GUI'
        self.resetContent()
        guiCustomers.customers(self.master)

    def callProducts(self):
        'calls the products GUI'
        self.resetContent()
        guiProducts.productMain(self.master)

    def callCategories(self):
        'calls the categories GUI'
        self.resetContent()
        guiCategories.categoriesOverview(self.master)

    def resetContent(self):
        'resets the contentframe, preparing it for new content'
        for widget in self.master.winfo_children():
            widget.destroy()


class buildFooter:
    'Class to build the main screens footer'
    def __init__(self,master):
        text = 'Dit programma is geschreven in opdracht van Hogeschool Utrecht, door studenten Nico, Patrick, Lars en Bart uit klas V1H. \u00a9 2017'
        tkinter.Label(master,text=text).pack()


root = tkinter.Tk()
my_gui = topLevelWindow(root)
root.mainloop()
