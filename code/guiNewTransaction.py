from main import *
import categories


class newTransaction:
    def __init__(self, master):
        self.master = master

        productSelectionFrame = tkinter.Frame(self.master)
        currentTransactionFrame = tkinter.Frame(self.master)
        numpadFrame = tkinter.Frame(self.master)

        self.productSelection = self.buildProductSelection(productSelectionFrame)
        self.currentTransaction = self.buildTransactionOverview(currentTransactionFrame)
        self.numpad = self.buildNumpadClass(numpadFrame)

        productSelectionFrame.grid(column=0, row=0, columnspan=2, sticky='nw')
        currentTransactionFrame.grid(column=2, row=0, sticky='e')
        numpadFrame.grid(column=1, row=1, columnspan=2, sticky='se')


    def buildProductSelection(self,master):
        selectionFrame = tkinter.Frame(master)
        categoryFrame = tkinter.Frame(master)
        productsFrame = tkinter.Frame(master)
        selectionFrame.grid(column=0,row=0,sticky='w')
        categoryFrame.grid(column=0,row=1,sticky='w')
        productsFrame.grid(column=0,row=2,sticky='w')

        tkinter.Label(selectionFrame, text="Geselecteerd:", font=('Arial', 20), height=2).pack(side='left')
        self.selectedProductLabel = tkinter.Label(selectionFrame, text="", font=("Arial", 20), height=2)
        self.selectedProductLabel.pack(side='left')
        self.selectedProduct = None

        self.categoryProductsDict = self.fetchProducts()
        for category in self.categoryProductsDict:
            cmd = lambda products = self.categoryProductsDict[category]: self.productButtons(productsFrame, products)
            tkinter.Button(categoryFrame, text=category[1], font=('Arial', 15), height=2, width=15, command=cmd, bg='lightblue').pack(side='left')

    def productButtons(self, master, products):
        r = 1
        c = 0

        for product in products:
            cmd = lambda id=product[0]: self.set(id)
            tkinter.Button(master, text=product[1][:13], font=('Arial', 15), height=2, width=15, command=cmd).grid(row=r, column=c)
            c += 1
            if c > 2:
                c = 0
                r += 1

    def set(self,productid):
        productname = lookupProductName(productid)
        self.selectedProduct = productid
        self.selectedProductLabel.config(text=productname)

    def fetchProducts(self):
        epochTime = str(datetime.date.today())
        products = dict()
        for category in categories.getCategories():
            cursor.execute('''SELECT productId, name FROM product WHERE datetimeStart < ? AND (datetimeEnd > ? OR datetimeEnd IS NULL) AND categoryId IS ?''',(epochTime, epochTime, category[0]))
            products[category] = cursor.fetchall()
        cursor.execute('''SELECT productId, name FROM product WHERE datetimeStart < ? AND (datetimeEnd > ? OR datetimeEnd IS NULL) AND categoryId IS NULL''',(epochTime, epochTime))
        products[('NULL', 'Anders')] = cursor.fetchall()
        return products

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



def lookupProductName(id):
    cursor.execute('''SELECT name FROM Product WHERE productId = ?''', (id,))
    productname = cursor.fetchone()[0]
    return productname


def calculateProductPrice(productid):
    epochTime = str(datetime.date.today())
    cursor.execute('''SELECT EXISTS(SELECT * FROM discount d WHERE d.productid = ? AND d.datetimeStart < ? AND (d.datetimeEnd > ? OR d.datetimeEnd IS NULL))''', (productid, epochTime, epochTime))
    if cursor.fetchone()[0] == 1:
        cursor.execute('''SELECT d.productId, p.value, d.percentage FROM discount d INNER JOIN price p ON p.productId = d.productId WHERE d.productid = ? AND d.datetimeStart < ? AND (d.datetimeEnd > ? OR d.datetimeEnd IS NULL)''',(productid, epochTime, epochTime))
        productDiscount = cursor.fetchone()
        productPrice = productDiscount[1] * productDiscount[2]
        return eval('{:.2f}'.format(productPrice))
    else:
        try:
            cursor.execute('''SELECT p.value FROM price p WHERE p.productid = ? AND p.datetimeStart < ? AND (p.datetimeEnd > ? OR p.datetimeEnd IS NULL)''',(productid, epochTime, epochTime))
            productPrice = cursor.fetchone()
            return productPrice[0]
        except:
            messageBox('Geen product geselecteerd','U heeft geen product geselecteerd. Selecteer een product voordat u deze toe wilt voegen aan te transactie.','error')
            return

if __name__ == "__main__":
    root = tkinter.Tk()
    my_gui = newTransaction(root)
    root.mainloop()