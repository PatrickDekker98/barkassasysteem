from main import *
from customerFuncs import *


class customers:
    'Creates a customersFrame'
    def __init__(self, master):
        self.master = master
        
        customerShowFrame = tkinter.Frame(self.master)
        customerShowFrame.grid(column = 4, row = 0, columnspan = 2, padx = 20, pady = 20)
        self.customerShow = customerTable(customerShowFrame)

        customerAddFrame = tkinter.Frame(self.master)
        customerAddFrame.grid(column = 6, row = 0, columnspan = 2, padx = 20, pady = 20)
        self.addFrame = addCustomerFrame(customerAddFrame)


class addCustomerFrame:
    'Creates an entry field for a new customer'
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

    #Checks if firstname or lastname is empty
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
    'Creates a table for the customer, plus three buttons to alter their information/data'
    def __init__(self, master):
        idColumn       = 1
        nameColumn     = 2
        moneyColumn    = 3
        telegramColumn = 4
        customerDict = returnAllCustomers()
        tkinter.Label(master, 
                text = 'Bewerk en/of verwijder klanten:', 
                font = ('Arial', 15), 
                height = 2).grid(column = 1, row = 0, columnspan = 3)

        tkinter.Label(master, text = "Id").grid(column = idColumn, row = 1, sticky = "W")
        tkinter.Label(master, text = "Naam").grid(column = nameColumn, row = 1, sticky = "W")
        tkinter.Label(master, text = "geld").grid(column = moneyColumn, row = 1, sticky = "W")
        tkinter.Label(master, text = "telegram").grid(column = telegramColumn, row = 1, sticky = "W")

        count = 2
        for customerKey in customerDict:    # Creates Labels and buttons for all customers in the database
            cmdDelete = lambda customerList = customerDict[customerKey], customerKey = customerKey: self.confirmUnset(master, customerList, customerKey)
            cmdTelegram = lambda customerList = customerDict[customerKey], customerKey = customerKey: self.addTelegramId(master, customerList, customerKey)
            cmdEdit = lambda customerList = customerDict[customerKey], customerKey = customerKey: self.confirmEdit(master, customerList, customerKey)
            customerList = customerDict[customerKey]
            
            if customerList[2] != None :
                text = customerList[0] + ' ' + customerList[2] + ' ' +customerList[1]
            else :
                text = customerList[0] + ' ' + customerList[1]

            if customerList[4] != None :
                telegramText = str(customerList[4])
            else :
                telegramText = 'geen'

            tkinter.Label(master, 
                    text = str(customerKey)).grid(column = idColumn, row = count, sticky = "W")
            tkinter.Label(master, 
                    text = text).grid(column = nameColumn, row = count, sticky = "W")
            tkinter.Label(master,
                    text = str(customerList[3])).grid(column = moneyColumn, row = count, sticky = "W")
            tkinter.Label(master,
                    text = telegramText).grid(column = telegramColumn, row = count, sticky = "W")

            tkinter.Button(master, 
                    text = "bewerk klant", 
                    height = 1, 
                    width = 15, 
                    bg = 'lightgreen', 
                    command = cmdEdit).grid(column = 5, row = count)
            tkinter.Button(master, 
                    text = "telegram",
                    height = 1, 
                    width = 15,
                    bg = 'blue',
                    fg = 'white',
                    command = cmdTelegram).grid(column = 6, row = count)
            tkinter.Button(master, 
                    text = "verwijder klant", 
                    height = 1, 
                    width = 15, 
                    bg = 'red', 
                    command = cmdDelete).grid(column = 7, row = count)
            
            count += 1


    def addTelegramId(self, master, customerList, customerKey):
        'Pops up a message, asking for a telegramID, which compells to certain requirements'
        popup = tkinter.Toplevel()
        popup.wm_title("Confirmation")
        popup.geometry('500x100')
        popup.resizable(width=False, height=False)

        if customerList[2] != None:
            text = "verander of voeg het telegramID van klant " + customerList[0] + ' ' + customerList[2] + ' ' +customerList[1] + ' met id ' + str(customerKey) + ' toe'
        else :
            text = "verander of voeg het telegramId van klant " + customerList[0] + ' ' +customerList[1] + ' met id ' + str(customerKey) + ' toe'
        label = tkinter.Label(popup, text = text).grid(row = 1, columnspan = 6)
        
        
        telegramIdLabel = tkinter.Label(popup,
                text = "telegramID:",
                height = 1,
                width = 12).grid(row = 2, column = 0)
        self.telegramIdEntry = tkinter.Entry(popup, width = 10)
        self.telegramIdEntry.grid(row = 2, column = 1)

        cancelButton = tkinter.Button(popup, 
                text = "annuleer", 
                height = 1, 
                width = 10, 
                command = lambda: popup.destroy()).grid(row = 2, column = 3)

        confirmButton = tkinter.Button(popup, 
                text = "ok", 
                height = 1, 
                width = 10, 
                command = lambda: self.addTelAndDestroy(popup, customerKey)).grid(row = 2, column = 4)


    def addTelAndDestroy(self, popup, customerKey):
        'Calls the telegram ID addfunction, and closes the popup'
        self.telegramIdAdd(customerKey)
        popup.destroy()


    def telegramIdAdd(self, customerKey):
        'Performs some check on the input on the entryfields and calls addTelegramId, which communicates with the database'
        telegramId = self.telegramIdEntry.get()
        if telegramId == '':
            popup = tkinter.Toplevel()
            popup.wm_title('Error')
            popup.geometry('500x100')
            popup.resizable(width=False, height=False)
            tkinter.Label(popup,
                    text = "een telegram id mag niet leeg zijn",
                    font = ('Arial', 15),
                    height = 2,).pack()
        elif len(telegramId) != 9:
            popup = tkinter.Toplevel()
            popup.wm_title('Error')
            popup.geometry('500x100')
            popup.resizable(width=False, height=False)
            tkinter.Label(popup,
                    text = "een telegram id moet 9 cijfers zijn",
                    font = ('Arial', 15),
                    height = 2,).pack()
        else :
            addTelegramId(customerKey, telegramId)
            popup = tkinter.Toplevel()
            popup.wm_title('succes')
            popup.geometry('500x100')
            popup.resizable(width=False, height=False)
            tkinter.Label(popup,
                    text = "Gelukt",
                    font = ('Arial', 15),
                    height = 2,).pack()
    

    def confirmEdit(self, master, customerList, customerKey):
        'Asks for the new name of the customer, then confirms it'
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
        'Function to call 2 other functions'
        self.customerEdit(customerKey)
        popup.destroy()


    def customerEdit(self, customerKey):
        'Checks if firstname and lastname arent empty, and returns lets user know if it succeeded'
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
        'Checks if you really want to remove the customer'
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
        'Function to call 2 other functions'
        deactivateCustomer(customerKey, True)
        popup.destroy()

if __name__ == "__main__":
    root = tkinter.Tk()
    my_gui = customer(root)
    root.mainloop()
