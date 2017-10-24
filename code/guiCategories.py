from main import *


class categoriesOverview(tkinter.Frame):
    transaction = []
    total = 0

    def __init__(self,master):
        self.master = master
        self.overview = tkinter.Listbox(self.master, width=55)
        self.overview.grid(column=0, row=1, columnspan=4)
        tkinter.Label(self.master, text="{:20}     {:3}".format('ID', 'Naam'), font=('Arial', 10)).grid(column=0, row=0,columnspan=2, sticky='w')
        self.totalLabel = tkinter.Label(self.master,text='€ {:.2f}'.format(self.total), font=('Arial', 20), height=1, width=10)
        self.totalLabel.grid(column=1, row=2)
        tkinter.Button(self.master, text="+", font=('Arial', 20), height=1, width=10, bg='lightgreen', command=self.addProduct).grid(column=0, row=3)
        tkinter.Button(self.master, text="-", font=('Arial', 20), height=1, width=10, bg='red',command=self.removeProduct).grid(column=1, row=3)
        tkinter.Button(self.master, text="Afrekenen", font=('Arial', 20), height=1, width=20, bg='green',command=self.endTransaction).grid(column=0, row=4,columnspan=2)


    def addProduct(self):
        try:
            product = my_gui.productSelection.returnValue()
        except:
            messageBox('Geen product geselecteerd', 'U heeft geen product geselecteerd. Selecteer een product voordat u deze toe wilt voegen aan te transactie.', 'error')
            return

        try:
            amount = my_gui.numpad.returnValue()
        except:
            messageBox('Geen aantal gekozen', 'U heeft geen aantal aangegeven. Geef aan hoeveelheid aan voordat u dit toe wilt voegen aan de transactie', 'error')
            return

        pricePerItem = calculateProductPrice(product)
        for bestaandProduct in self.transaction:
            if product == bestaandProduct[0]:
                bestaandProduct[1] += amount
                self.updateTransactionListbox()
                return
        self.transaction.append([product,amount, pricePerItem])
        self.updateTransactionListbox()


    def updateTransactionListbox(self):
        self.overview.delete(0,'end')
        self.calculateTotal()
        for product in self.transaction:
            print(product)
            self.overview.insert('end', '{:<50}x{:<7}€ {:<7.2f}'.format(lookupProductName(product[0]),product[1],(product[1] * product[2])))


    def removeProduct(self):
        productindex = self.overview.index('active')
        del self.transaction[productindex]
        self.updateTransactionListbox()


    def calculateTotal(self):
        self.total = 0
        for product in self.transaction:
            self.total += (product[1] * product[2])
        self.totalLabel.config(text='€ {:.2f}'.format(self.total))

    def endTransaction(self):
        if self.total == 0:
            messageBox('Lege transactie', 'Dit is een lege transactie. Voeg eerst producten toe voordat u wil afrekenen!', 'info')
        else:
            messageBox('Betaling','U bent klaar om te betalen. Het te betalen bedrag is € {:.2f}'.format(self.total))


if __name__ == "__main__":
    root = tkinter.Tk()
    my_gui = newTransaction(root)
    root.mainloop()