from main import *
from customerFuncs import *

class customers:
    def __init__(self, master):
        self.master = master
        
        customerShowFrame = tkinter.Frame(self.master)
        customerShowFrame.grid(column = 4, row = 1, columnspan = 2, padx = 20, pady = 20)
        self.customerShow = customerTable(customerShowFrame)

        customerAddFrame = tkinter.Frame(self.master)
        customerAddFrame.grid(column = 6, row = 1, columnspan = 2, padx = 20, pady = 20)
        self.addFrame = addCustomerFrame(customerAddFrame)

class addCustomerFrame:
    def __init__(self, master):
        tkinter.Label(master,
                text = "Voeg nieuwe klanten toe:",
                font = ('Arial', 15),
                height = 2,
                anchor = 'n').grid(column = 0, row = 0, sticky = 'N')
        fristNameLabel = tkinter.Label(master, 
                text = "voornaam:", 
                height = 1, 
                width = 12,
                anchor = "w").grid(row = 2, column = 0, sticky = 'W')
        self.firstNameEntry = tkinter.Entry(master, 
                width = 10)
        self.firstNameEntry.grid(row = 2, column = 1, sticky = 'W')
        insertionLabel = tkinter.Label(master,
                text = "tussenvoegsel:",
                height = 1,
                width = 12,
                anchor = "w").grid(row = 3, column = 0, sticky = 'W')
        self.insertionEntry = tkinter.Entry(master, 
                width = 5)
        self.insertionEntry.grid(row = 3, column = 1, sticky = 'W')
        lastNameLabel = tkinter.Label(master, 
                text = "achternaam:",
                height = 1,
                width = 12,
                anchor = 'w').grid(row = 4, column = 0, sticky = 'W')
        self.lastNameEntry = tkinter.Entry(master, 
                width = 10)
        self.lastNameEntry.grid(row = 4, column = 1, sticky = 'W')

        confirmButton = tkinter.Button(master, 
                text = "Toevoegen", 
                height = 2,
                width = 20,
                bg = "green",
                command = lambda: self.confirmAddition()).grid(row = 5, column = 0, columnspan = 2)

    def confirmAddition(self):
        firstName = self.firstNameEntry.get()
        insertion = self.insertionEntry.get()
        lastName = self.lastNameEntry.get()
        if firstName != '' and lastName != '':
            addCustomer(firstName, insertion, lastName)
            popup = tkinter.Toplevel()
            popup.wm_title('succes!')
            popup.geometry('500x100')
            popup.resizable(width=False, height=False)
            tkinter.Label(popup,
                    text = "Gelukt!",
                    font = ('Arial', 15),
                    height = 2,).pack()
        else :
            popup = tkinter.Toplevel()
            popup.wm_title('Error')
            popup.geometry('500x100')
            popup.resizable(width=False, height=False)
            tkinter.Label(popup,
                    text = "De klant moet een voor- en achternaam hebben",
                    font = ('Arial', 15),
                    height = 2,).pack()

class customerTable:
    def __init__(self, master):
        customerDict = returnAllCustomers()
        tkinter.Label(master, 
                text = 'Bewerk en/of verwijder klanten:', 
                font = ('Arial', 15), 
                height = 2).grid(column = 1, row = 0, columnspan = 3)

        tkinter.Label(master, text = "Id").grid(column = 1, row = 1, sticky = "W")
        tkinter.Label(master, text = "Naam").grid(column = 2, row = 1, sticky = "W")

        count = 2
        for customerKey in customerDict:
            cmdDelete = lambda customerList = customerDict[customerKey], customerKey = customerKey: self.confirmUnset(master, customerList, customerKey)
            cmdEdit = lambda customerList = customerDict[customerKey], customerKey = customerKey: self.confirmEdit(master, customerList, customerKey)
            customerList = customerDict[customerKey]
            
            if customerList[2] != None :
                text = customerList[0] + ' ' + customerList[2] + ' ' +customerList[1]
            else :
                text = customerList[0] + ' ' + customerList[1]

            tkinter.Label(master, text = str(customerKey)).grid(column = 1, row = count, sticky = "W")
            tkinter.Label(master, text = text).grid(column = 2, row = count, sticky = "W")
            tkinter.Button(master, 
                    text = "bewerk klant", 
                    height = 1, 
                    width = 15, 
                    bg = 'lightgreen', 
                    command = cmdEdit).grid(column = 3, row = count)
            tkinter.Button(master, 
                    text = "verwijder klant", 
                    height = 1, 
                    width = 15, 
                    bg = 'red', 
                    command = cmdDelete).grid(column = 4, row = count)
            
            count += 1

    def confirmEdit(self, master, customerList, customerKey):
        popup = tkinter.Toplevel()
        popup.wm_title("Confirmation")
        popup.geometry('500x100')
        popup.resizable(width=False, height=False)
        
        if customerList[2] != None:
            text = "weet je zeker dat je klant " + customerList[0] + ' ' + customerList[2] + ' ' +customerList[1] + ' met id ' + str(customerKey) + ' wilt bewerken?'
        else :
            text = "weet je zeker dat je klant " + customerList[0] + ' ' +customerList[1] + ' met id ' + str(customerKey) + ' wilt bewerken?'
        label = tkinter.Label(popup, text = text).grid(row = 1, columnspan = 6)

        fristNameLabel = tkinter.Label(popup, 
                text = "voornaam:", 
                height = 1, 
                width = 12).grid(row = 2, column = 0, sticky = 'E')
        self.firstNameEntry = tkinter.Entry(popup, 
                width = 10)
        self.firstNameEntry.grid(row = 2, column = 1, sticky = 'W')
        insertionLabel = tkinter.Label(popup,
                text = "tussenvoegsel:",
                height = 1,
                width = 12).grid(row = 3, column = 0, sticky = 'E')
        self.insertionEntry = tkinter.Entry(popup, 
                width = 5)
        self.insertionEntry.grid(row = 3, column = 1, sticky = 'W')
        lastNameLabel = tkinter.Label(popup, 
                text = "achternaam:",
                height = 1,
                width = 12).grid(row = 4, column = 0, sticky = 'E')
        self.lastNameEntry  = tkinter.Entry(popup, 
                width = 10)
        self.lastNameEntry.grid(row = 4, column = 1, sticky = 'W')

        cancelButton = tkinter.Button(popup, 
                text = "annuleer", 
                height = 1, 
                width = 10, 
                command = lambda: popup.destroy()).grid(row = 3, column = 3)

        confirmButton = tkinter.Button(popup, 
                text = "ok", 
                height = 1, 
                width = 10, 
                command = lambda: self.editAndDestroy(popup, customerKey)).grid(row = 3, column = 4)

    def editAndDestroy(self, popup, customerKey):
        self.customerEdit(customerKey)
        popup.destroy()

    def customerEdit(self, customerKey):
        firstName = self.firstNameEntry.get()
        insertion = self.insertionEntry.get()
        lastName  = self.lastNameEntry.get()
        if firstName != '' and lastName != '':
            editCustomer(customerKey, firstName, insertion, lastName, True)
            popup = tkinter.Toplevel()
            popup.wm_title('succes!')
            popup.geometry('500x100')
            popup.resizable(width=False, height=False)
            tkinter.Label(popup,
                    text = "Gelukt!",
                    font = ('Arial', 15),
                    height = 2,).pack()
        else :
            popup = tkinter.Toplevel()
            popup.wm_title('Error')
            popup.geometry('500x100')
            popup.resizable(width=False, height=False)
            tkinter.Label(popup,
                    text = "De klant moet een voor- en achternaam hebben",
                    font = ('Arial', 15),
                    height = 2,).pack()
        

    def confirmUnset(self, master, customerList, customerKey):
        popup = tkinter.Toplevel()
        popup.wm_title("Confirmation")
        if customerList[2] != None:
            text="weet je zeker dat je klant " + customerList[0] + ' ' + customerList[2] + ' ' +customerList[1] + ' met id ' + str(customerKey) + ' wilt verwijderen?'
        else :
            text="weet je zeker dat je klant " + customerList[0] + ' ' +customerList[1] + ' met id ' + str(customerKey) + ' wilt verwijderen?'

        label = tkinter.Label(popup, text = text).grid(row = 1, column = 0)

        cancelButton = tkinter.Button(popup, 
                text = "annuleer", 
                height = 1, 
                width = 10, 
                command = lambda: popup.destroy()).grid(row = 2, column = 0)

        confirmButton = tkinter.Button(popup, 
                text = "ok", 
                height = 1, 
                width = 10, 
                command = lambda: self.deactivateAndDestroy(popup, customerKey)).grid(row = 3, column = 0)

    def deactivateAndDestroy(self, popup, customerKey):
        deactivateCustomer(customerKey, True)
        popup.destroy()

if __name__ == "__main__":
    root = tkinter.Tk()
    my_gui = customer(root)
    root.mainloop()
