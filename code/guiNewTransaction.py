from main import *
import categories, products, balance


class newTransaction:
    'Prepares and places new frames to be filled by other functions'
    def __init__(self, master):
        self.master = master

        productSelectionFrame = tkinter.Frame(self.master)
        currentTransactionFrame = tkinter.Frame(self.master)
        numpadFrame = tkinter.Frame(self.master)

        self.productSelection = self.buildProductSelection(productSelectionFrame)
        self.currentTransaction = self.buildTransactionOverview(currentTransactionFrame)
        self.numpad = self.buildNumpad(numpadFrame)

        productSelectionFrame.grid(column=0, row=0, columnspan=2, sticky='nw')
        currentTransactionFrame.grid(column=2, row=0, sticky='e')
        numpadFrame.grid(column=1, row=1, columnspan=2, sticky='se')


    def buildProductSelection(self,master):
        'Builds the productSelection, which is categorised by productCategories'
        selectionFrame = tkinter.Frame(master)
        categoryFrame = tkinter.Frame(master)
        productsFrame = tkinter.Frame(master)
        selectionFrame.grid(column=0,row=0,sticky='w')
        categoryFrame.grid(column=0,row=1,sticky='w')
        productsFrame.grid(column=0,row=2,sticky='w')

        tkinter.Label(selectionFrame, text="Geselecteerd:", font=('Arial', 20)).pack(side='left')
        self.selectedProductLabel = tkinter.Label(selectionFrame, text="", font=("Arial", 20), height=2)
        self.selectedProductLabel.pack(side='left')
        self.selectedProduct = None

        r = 1
        c = 0
        self.categoryProductsDict = products.fetchProductsPerCategory(categories.getCategories())
        for category in self.categoryProductsDict:  #   for every category, create a button to filter the products
            cmd = lambda products = self.categoryProductsDict[category]: self.productButtons(productsFrame, products)
            tkinter.Button(categoryFrame, text=category[1], font=('Arial', 15), height=2, width=15, command=cmd, bg='lightblue').grid(row=r, column=c)
            c += 1
            if c > 2:
                c = 0
                r += 1


    def resetContent(self,master):
        'Destroys contents of a given Frame'
        for widget in master.winfo_children():
            widget.destroy()


    def productButtons(self, master, products):
        'Creates buttons for productselection, by given list(which is filtered to only 1 category)'
        self.resetContent(master)
        r = 1
        c = 0

        for product in products:    #   for every prodcut, create a button
            cmd = lambda id=product[0]: self.set(id)
            tkinter.Button(master, text=product[1][:13], font=('Arial', 15), height=2, width=15, command=cmd).grid(row=r, column=c)
            c += 1
            if c > 2:
                c = 0
                r += 1

    def set(self,productid):
        'sets selected product to the pressed button'
        productname = products.lookupProductName(productid)
        self.selectedProduct = productid
        self.selectedProductLabel.config(text=productname)


    def productsReturnValue(self):
        'Returns the last pressed button, then reset the selection label'
        try:
            value = int(self.selectedProduct)
        except:
            tkinter.messagebox.showwarning('Geen product geselecteerd','U heeft geen product geselecteerd. Selecteer een product voordat u deze toe wilt voegen aan te transactie.')
            return
        self.resetProductSelection()
        return value


    def resetProductSelection(self):
        'resets productselection'
        self.selectedProduct = None
        self.selectedProductLabel.config(text='')


    def buildTransactionOverview(self,master):
        'Builds the overview of the current transaction'
        self.transaction = []
        self.total = 0
        self.overview = tkinter.Listbox(master, width=55, font='consolas',)
        self.overview.grid(column=0, row=1, columnspan=4)
        tkinter.Label(master, text="{:73}     {:9}     {:7}".format('Product', 'Aantal', 'Prijs'), font=('Arial', 10)).grid(column=0, row=0,columnspan=2, sticky='w')
        self.totalLabel = tkinter.Label(master,text='€ {:.2f}'.format(self.total), font=('Arial', 20), height=1, width=10)
        self.totalLabel.grid(column=1, row=2)
        tkinter.Button(master, text="+", font=('Arial', 20), height=1, width=10, bg='lightgreen', command=self.addProduct).grid(column=0, row=3)
        tkinter.Button(master, text="-", font=('Arial', 20), height=1, width=10, bg='red',command=self.removeProduct).grid(column=1, row=3)
        tkinter.Button(master, text="Afrekenen", font=('Arial', 20), height=1, width=20, bg='green',command=self.endTransaction).grid(column=0, row=4,columnspan=2)

    def addProduct(self):
        'adds a product to the transaction. Requires data from numpad, and productselectionframes'
        product = self.productsReturnValue()
        amount = self.numpadReturnValue()

        if product == None:
            tkinter.messagebox.showwarning('Geen product geselecteerd', 'U heeft geen product geselecteerd. Selecteer een product voordat u deze toe wilt voegen aan te transactie.')
            return
        elif amount == str():
            tkinter.messagebox.showwarning('Geen aantal gekozen', 'U heeft geen aantal aangegeven. Geef aan hoeveelheid aan voordat u dit toe wilt voegen aan de transactie')
            return
        pricePerItem = products.calculateProductPrice(product)
        for bestaandProduct in self.transaction:    #   If the newproduct already exists in the transaction, the amounts will be added up together
            if product == bestaandProduct[0]:
                bestaandProduct[1] += amount
                self.updateTransactionListbox()
                return
        self.transaction.append([product,amount, pricePerItem])
        self.updateTransactionListbox()

    def updateTransactionListbox(self):
        'Empties and rebuildt the transactionoverview listbox'
        self.overview.delete(0,'end')
        self.calculateTotal()
        for product in self.transaction:    #   Every product gets inserted
            self.overview.insert('end', '{:<30}x{:<5}€ {:<4.2f}'.format(products.lookupProductName(product[0]),product[1],(product[1] * product[2])))

    def removeProduct(self):
        'removes selected product from current transaction'
        productindex = self.overview.index('active')
        del self.transaction[productindex]
        self.updateTransactionListbox()

    def calculateTotal(self):
        'calculates the total cost of all products in the transaction'
        self.total = 0
        for product in self.transaction:    #   Price of each product gets added to the total
            self.total += (product[1] * product[2])
        self.totalLabel.config(text='€ {:.2f}'.format(self.total))

    def endTransaction(self):
        'Ends the transaction and writes it to the database'
        transaction = self.transaction
        if self.total == 0:
            tkinter.messagebox.showinfo('Lege transactie', 'Dit is een lege transactie. Voeg eerst producten toe voordat u wil afrekenen!')
        else:
            tkinter.messagebox.showinfo('Betaling','U bent klaar om te betalen. Het te betalen bedrag is € {:.2f}'.format(self.total))
            customerId = simpledialog.askstring("KlantenID", "Geef uw klantenID in")    #   To be replaced by QRcode or NFC tag scanner
            if balance.writeNewTransaction(customerId, transaction):
                self.numpadClear()
                self.resetProductSelection()
                self.transaction = []
                self.updateTransactionListbox()
            else:
                tkinter.messagebox.showwarning('Waarschuwing','Er is iets missgegaan met afrekenen. Probeer het opnieuw.!')
                return

    def buildNumpad(self, master):
        'Builds the numpadframe'
        self.numpadValue = str()
        tkinter.Label(master, text="Aantal:", font=('Arial', 20), height=5).grid(column=0, row=0)
        self.amount = tkinter.Label(master, text=self.numpadValue, font=("Arial", 20), height=5)
        self.amount.grid(column=1, row=0)

        self.buttons = ['1', '2', '3','4', '5', '6','7', '8', '9', '0']
        r = 1
        c = 0
        for b in self.buttons:  #   Every button gets created, with a maximum of 5 columns
            cmd = lambda button=b: self.numpadAdd(button)
            tkinter.Button(master, text=b, font=('Arial', 15), height=2, width=15, command=cmd).grid(row=r, column=c)
            c += 1
            if c > 4:
                c = 0
                r += 1
        tkinter.Button(master, text='<', font=('Arial', 15), height=2, width=15, bg='red', command=self.numpadBackspace).grid(row=1, column=5)
        tkinter.Button(master, text='C', font=('Arial', 15), height=2, width=15, bg='red', command=self.numpadClear).grid(row=2, column=5)


    def numpadAdd(self, number):
        'The pressed buttons value gets appended to the totalvalue'
        self.numpadValue = self.numpadValue + number
        self.amount.config(text=self.numpadValue)

    def numpadBackspace(self):
        'The last digit gets removed from the total value'
        self.numpadValue = self.numpadValue[:-1]
        self.amount.config(text=self.numpadValue)

    def numpadClear(self):
        'The numpad gets Cleared'
        self.numpadValue = ''
        self.amount.config(text=self.numpadValue)

    def numpadReturnValue(self):
        'Returns the numpads Value'
        value = int(self.numpadValue)
        self.numpadValue = str()
        self.amount.config(text=self.numpadValue)
        return int(value)





if __name__ == "__main__":
    root = tkinter.Tk()
    my_gui = newTransaction(root)
    root.mainloop()