from main import *
from customerFuncs import *
import tkinter

class customers:
    def __init__(self, master):
        self.master = master
        
        customerShowFrame = tkinter.Frame(self.master)
        customerShowFrame.grid(column = 2, row = 2, columnspan = 2)
        self.customerShow = customerTable(customerShowFrame)

class customerTable:
    def __init__(self, master):
        customerDict = returnAllCustomers()
        tkinter.Label(master, text = 'alle klanten staan hieronder', font=('Arial', 20), height = 2).grid(column = 0, row = 0)
        count = 1

        for customerKey in customerDict:
            cmd = lambda customerList = customerDict[customerKey], customerKey = customerKey: self.confirmUnset(master, customerList, customerKey)
            customerList = customerDict[customerKey]
            if customerList[2] != None:
                tkinter.Label(master, text = customerList[0] + ' ' + customerList[2] + ' ' +customerList[1]).grid(column = 0, row = count)
            else :
                tkinter.Label(master, text = customerList[0] + ' ' + customerList[1]).grid(column = 0, row = count)
            tkinter.Button(master, text = "verwijder klant", height = 1, width = 20, bg = 'red', command = cmd).grid(column = 1, row = count)
            count += 1

    def confirmUnset(self, master, customerList, customerKey):
        popup = tkinter.Toplevel()
        popup.wm_title("Confirmation")
        if customerList[2] != None:
            text="weet je zeker dat je klant " + customerList[0] + ' ' + customerList[2] + ' ' +customerList[1] + ' met id ' + str(customerKey) + ' wilt verwijderen?'
        else :
            text="weet je zeker dat je klant " + customerList[0] + ' ' +customerList[1] + ' met id ' + str(customerKey) + ' wilt verwijderen?'

        label = tkinter.Label(popup, text = text)
        label.grid(row = 1, column = 0)
        cancelButton = tkinter.Button(popup, text = "annuleer", height = 1, width = 10, command = lambda: popup.destroy()).grid(row = 2, column = 0)
#        confirmButton = tkinter.Button(popup, text = "ok", height = 1, width = 10, command = lambda: )



#class addNewCustomer:
#    def __init__(self, master):


if __name__ == "__main__":
    root = tkinter.Tk()
    my_gui = customer(root)
    root.mainloop()
