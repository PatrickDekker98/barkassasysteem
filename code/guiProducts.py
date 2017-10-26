from main import *


class newTransaction:
    def __init__(self, master):
        self.master = master
        self.activeContent = 'Menu'

        contentFrame = tkinter.Frame(self.master)
        returnFrame = tkinter.Frame(self.master)

        self.content = self.buildContent(contentFrame)
        self.returnFrame = self.buildReturn(returnFrame)

        contentFrame.pack(side='top')
        returnFrame.pack(side='top')


    def buildContent(self,master):


    def buildReturn(self, master):
        tkinter.Button(master,text='<', font=('Arial', 15), height=2, width=15, command=self.returnFunction).pack(side='left')

    def returnFunction(self):


    def fetchProducts(self):
        epochTime = str(datetime.date.today())
        products = dict()
        for category in self.fetchProductCategories():
            cursor.execute('''SELECT productId, name FROM product WHERE datetimeStart < ? AND (datetimeEnd > ? OR datetimeEnd IS NULL) AND categoryId IS ?''',(epochTime, epochTime, category[0]))
            products[category] = cursor.fetchall()
        cursor.execute('''SELECT productId, name FROM product WHERE datetimeStart < ? AND (datetimeEnd > ? OR datetimeEnd IS NULL) AND categoryId IS NULL''',(epochTime, epochTime))
        products[('NULL', 'Anders')] = cursor.fetchall()
        return products

    def fetchProductCategories(self):
        epochTime = str(datetime.date.today())
        cursor.execute('''SELECT categoryId, name FROM category WHERE datetimeStart < ? AND (datetimeEnd > ? OR datetimeEnd IS NULL)''',(epochTime, epochTime))
        categories = cursor.fetchall()
        return categories

    def productsReturnValue(self):
        value = self.selectedProduct
        self.selectedProduct = None
        self.selectedProductLabel.config(text='')
        return value

    def buildTransactionOverview(self,master):
        self.transaction = []
        self.total = 0
        self.overview = tkinter.Listbox(master, width=55)
        self.overview.grid(column=0, row=1, columnspan=4)
        tkinter.Label(master, text="{:20}     {:3}     {:7}".format('Product', 'Aantal', 'Prijs'), font=('Arial', 10)).grid(column=0, row=0,columnspan=2, sticky='w')
        self.totalLabel = tkinter.Label(master,text='€ {:.2f}'.format(self.total), font=('Arial', 20), height=1, width=10)
        self.totalLabel.grid(column=1, row=2)
        tkinter.Button(master, text="+", font=('Arial', 20), height=1, width=10, bg='lightgreen', command=self.addProduct).grid(column=0, row=3)
        tkinter.Button(master, text="-", font=('Arial', 20), height=1, width=10, bg='red',command=self.removeProduct).grid(column=1, row=3)
        tkinter.Button(master, text="Afrekenen", font=('Arial', 20), height=1, width=20, bg='green',command=self.endTransaction).grid(column=0, row=4,columnspan=2)

    def addProduct(self):
        product = self.productsReturnValue()
        amount = self.numpadReturnValue()
        if product == None:
            messageBox('Geen product geselecteerd', 'U heeft geen product geselecteerd. Selecteer een product voordat u deze toe wilt voegen aan te transactie.', 'error')
            return
        elif amount == str():
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

    def buildNumpadClass(self,master):
        self.numpadValue = str()
        tkinter.Label(master, text="Aantal:", font=('Arial', 20), height=5).grid(column=0, row=0)
        self.amount = tkinter.Label(master, text=self.numpadValue, font=("Arial", 20), height=5)
        self.amount.grid(column=1, row=0)

        self.buttons = ['1', '2', '3','4', '5', '6','7', '8', '9', '0']
        r = 1
        c = 0
        for b in self.buttons:
            cmd = lambda button=b: self.numpadAdd(button)
            tkinter.Button(master, text=b, font=('Arial', 15), height=2, width=15, command=cmd).grid(row=r, column=c)
            c += 1
            if c > 4:
                c = 0
                r += 1
        tkinter.Button(master, text='<', font=('Arial', 15), height=2, width=15, bg='red', command=self.numpadBackspace).grid(row=1, column=5)
        tkinter.Button(master, text='C', font=('Arial', 15), height=2, width=15, bg='red', command=self.numpadClear).grid(row=2, column=5)


    def numpadAdd(self, number):
        self.numpadValue = self.numpadValue + number
        self.amount.config(text=self.numpadValue)

    def numpadBackspace(self):
        self.numpadValue = self.numpadValue[:-1]
        self.amount.config(text=self.numpadValue)

    def numpadClear(self):
        self.numpadValue = ''
        self.amount.config(text=self.numpadValue)

    def numpadReturnValue(self):
        value = self.numpadValue
        self.numpadValue = str()
        self.amount.config(text=self.numpadValue)
        return int(value)

    def readyToCloseScreen(self):
        if self.numpadReturnValue() != 0 or self.selectedProduct != None or self.transaction != []:
            return tkinter.askokcancel('Waarschuwing', 'Uw data is nog niet opgeslagen, wilt u deze weggooien?')
        else:
            return False


if __name__ == "__main__":
    root = tkinter.Tk()
    my_gui = newTransaction(root)
    root.mainloop()